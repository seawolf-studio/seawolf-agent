#!/usr/bin/env python3
"""
TANK — Misión «Precios Reales y Piso de Rentabilidad»
Versión corregida: detecta correctamente productos ultra-baratos y aplica precios psicológicos.
"""

import json
import csv
import os
from datetime import date

PRODUCTS_PATH = r"C:\Users\Admin\seawolf-store\dist\products.json"
CONFIG_PATH = r"C:\Users\Admin\seawolf-store\mantenimiento\config.json"
CSV_OUT_PATH = r"C:\Users\Admin\seawolf-store\mantenimiento\precios-real-20261013.csv"
MD_OUT_PATH = r"C:\Users\Admin\seawolf-agent\intel\tienda\tank-precios-informe-20261013.md"

ENVIO = 10000
DEV_RATE_LO = 0.30
DEV_RATE_HI = 0.40
RESERVE_FACTOR = 0.45
SANOS_THRESHOLD = 0.25
MAX_TICKET_CREIBLE = 75000
RETIRE_RATIO = 3.0

def psycho_price(actual):
    if actual <= 0: return None
    c = (actual // 100) * 100 + 900
    if c > int(actual * 1.20):
        c = ((actual // 1000) * 1000) + 900
    return c

def min_price_for_target(costo, envio, dev_rate, rf, target):
    return (costo + envio * (1 + dev_rate * rf)) / (1 - target)

# === CARGA ===
with open(CONFIG_PATH, encoding="utf-8") as f:
    cfg = json.load(f)
assert cfg["envio_estimado"] == ENVIO
print(f"[OK] envio_estimado = {ENVIO:,} COP (confirmado)")

with open(PRODUCTS_PATH, encoding="utf-8") as f:
    products = json.load(f)
total = len(products)
print(f"[OK] {total} productos cargados")

# === TAREA 1: Margen real producto por producto ===
rows = []
for p in products:
    sku = p.get("sku", "N/A")
    name = p.get("name", "").replace('"', "'")
    costo_raw = p.get("dropi_cost")
    precio = p.get("price") or p.get("price_wc")

    if costo_raw is None or costo_raw == 0 or (isinstance(costo_raw, str) and str(costo_raw).strip() == ""):
        rows.append({"sku": sku, "nombre": name, "costo_dropi": "", "envio": ENVIO,
            "precio_actual": precio if precio else "",
            "margen_bruto_pct": "", "margen_neto_pct": "", "margen_con_devolucion_pct": "",
            "veredicto": "SIN_COSTO", "accion": "", "precio_propuesto": "", "direccion_cambio": ""})
        continue

    costo_val = float(costo_raw)
    precio_val = float(precio) if precio else costo_val * 3

    mb = (precio_val - costo_val) / precio_val if precio_val > 0 else 0
    mn = (precio_val - costo_val - ENVIO) / precio_val if precio_val > 0 else 0
    md_hi = (precio_val - costo_val - ENVIO - DEV_RATE_HI * RESERVE_FACTOR * ENVIO) / precio_val if precio_val > 0 else 0

    if md_hi < 0: vrd = "PERDIDA"
    elif md_hi >= SANOS_THRESHOLD: vrd = "SANOS"
    else: vrd = "A_REVISAR"

    rows.append({"sku": sku, "nombre": name, "costo_dropi": costo_val, "envio": ENVIO,
        "precio_actual": round(precio_val),
        "margen_bruto_pct": round(mb*100, 1), "margen_neto_pct": round(mn*100, 1),
        "margen_con_devolucion_pct": round(md_hi*100, 1), "veredicto": vrd,
        "accion": "", "precio_propuesto": "", "direccion_cambio": ""})

# === TAREA 2: Productos que NO pueden ser rentables ===
no_rentables = []
a_subir = []
pack_candidates = []

for p in products:
    sku = p.get("sku", "N/A")
    name = p.get("name", "").replace('"', "'")
    costo_raw = p.get("dropi_cost")
    precio_raw = p.get("price") or p.get("price_wc")

    if costo_raw is None or costo_raw == 0: continue
    if isinstance(costo_raw, str) and str(costo_raw).strip() == "": continue

    costo = float(costo_raw)
    if costo >= 8000: continue

    precio_val = float(precio_raw) if precio_raw else None
    pm_hi = min_price_for_target(costo, ENVIO, DEV_RATE_HI, RESERVE_FACTOR, SANOS_THRESHOLD)
    ratio = pm_hi / precio_val if precio_val else float('inf')

    if ratio >= RETIRE_RATIO or pm_hi > MAX_TICKET_CREIBLE:
        no_rentables.append({"sku": sku, "nombre": name, "costo": costo,
            "precio_actual": round(precio_val) if precio_val else "N/A",
            "precio_minimo_real": round(pm_hi), "ratio_aumento": round(ratio, 1),
            "accion": "RETIRAR", "nota": f"pm=${round(pm_hi)}, ratio={ratio:.1f}x"})
    elif pm_hi <= MAX_TICKET_CREIBLE:
        if precio_val and precio_val < pm_hi - 5000:
            a_subir.append({"sku": sku, "nombre": name, "costo": costo,
                "precio_actual": round(precio_val),
                "precio_minimo_real": round(pm_hi), "ratio_aumento": round(ratio, 1),
                "accion": "SUBIR", "nota": f"subir a ~${round(pm_hi)} ({ratio:.1f}x)"})
    else:
        pack_candidates.append({"sku": sku, "nombre": name, "costo": costo,
            "precio_actual": round(precio_val) if precio_val else "N/A",
            "precio_minimo_real": round(pm_hi), "ratio_aumento": round(ratio, 1),
            "accion": "PACK", "nota": f"pm>{MAX_TICKET_CREIBLE} pero solo {ratio:.1f}x -> agrupa"})

print(f"Tarea 2: {len(no_rentables)} RETIRAR, {len(a_subir)} SUBIR, {len(pack_candidates)} PACK")

# === TAREA 3: Precios psicológicos ===
psych_rows = []
for r in rows:
    if r["veredicto"] == "SIN_COSTO" or not r["precio_actual"]:
        psych_rows.append({**r, "precio_propuesto": "", "direccion_cambio": "NA"})
        continue
    actual = int(r["precio_actual"])
    pp = psycho_price(actual)
    dirc = "IGUAL" if pp==actual else ("SUBIR" if pp and pp>actual else ("BAJAR" if pp else "NA"))
    psych_rows.append({**r, "precio_propuesto": pp if pp else "", "direccion_cambio": dirc})

# Asignar acciones T2 al CSV
for pr in psych_rows:
    sku = pr["sku"]
    if sku in {e["sku"]: e for e in a_subir}:
        e = next(e for e in a_subir if e["sku"]==sku)
        pr["accion"] = f"{e['accion']} -> ~${e['precio_minimo_real']}"
    elif sku in {e["sku"]: e for e in no_rentables}:
        e = next(e for e in no_rentables if e["sku"]==sku)
        pr["accion"] = f"{e['accion']}: {e['nota']}"
    elif sku in {e["sku"]: e for e in pack_candidates}:
        e = next(e for e in pack_candidates if e["sku"]==sku)
        pr["accion"] = f"{e['accion']}: {e['nota']}"

# === ESCRIBIR CSV ===
fnames = ["sku","nombre","costo_dropi","envio","precio_actual","margen_bruto_pct",
          "margen_neto_pct","margen_con_devolucion_pct","veredicto","accion","precio_propuesto","direccion_cambio"]
with open(CSV_OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fnames); w.writeheader()
    for r in psych_rows: w.writerow(r)
print(f"[OK] CSV escrito ({os.path.getsize(CSV_OUT_PATH):,} bytes)")

# === CONTADORES ===
sc = sum(1 for r in rows if r["veredicto"]=="SANOS")
rc = sum(1 for r in rows if r["veredicto"]=="A_REVISAR")
pc = sum(1 for r in rows if r["veredicto"]=="PERDIDA")
xc = sum(1 for r in rows if r["veredicto"]=="SIN_COSTO")
assert sc+rc+pc+xc == total

cc = [r for r in rows if r["veredicto"]!="SIN_COSTO"]
tb = sorted([r for r in rows if r["veredicto"]=="SANOS"], key=lambda x:float(x["margen_con_devolucion_pct"]), reverse=True)[:10]
tm = sorted(cc, key=lambda x:float(x["margen_con_devolucion_pct"]))[:10]

rangos = {}
for r in rows:
    if r["veredicto"]=="SIN_COSTO": continue
    p=int(float(r["precio_actual"]))
    k="<20K" if p<20000 else "20K-40K" if p<40000 else "40K-60K" if p<60000 else "60K-100K" if p<100000 else "100K-150K" if p<150000 else ">150K"
    rangos.setdefault(k, {"total":0,"SANOS":0,"A_REVISAR":0,"PERDIDA":0})
    rangos[k]["total"]+=1; v=r["veredicto"];
    if v in rangos[k]: rangos[k][v]+=1

# === GENERAR MD ===
F = format
L = []
L.append("# 🛡️ Informe TANK — Precios Reales y Piso de Rentabilidad")
L.append("")
L.append("**Fecha:** " + date.today().strftime("%d/%m/%Y"))
L.append("**Fuente datos:** `products.json` (" + str(total) + " productos) + `config.json` (envío=$" + F(ENVIO,',') + " COP)")
L.append(""); L.append("---"); L.append("")

L.append("## 🔬 Supuestos Declarados")
L.append("")
L.append("- **Costo de envío (Dropi):** $" + F(ENVIO,',') + " COP (config.json, confirmado)")
L.append("- **Tasa de devolución baja:** 30% del volumen")
L.append("- **Tasa de devolución alta:** 40% del volumen")
L.append("- **Reserva por devolución:** 45% del flete = $" + F(int(ENVIO*0.45),',') + "/devolución")
L.append("- **Umbral SANOS:** >=25% margen neto con devolución 40% (peor caso)")
L.append("- **Ticket máximo creíble:** $" + F(MAX_TICKET_CREIBLE,',') + " COP")
L.append("- **Ratio retiro:** precio_min > 3x precio_actual -> RETIRAR/PACK")
L.append("")

L.append("## 📊 Totales por Veredicto")
L.append("")
L.append("| Veredicto | Cantidad | % catálogo |")
L.append("|-----------|----------|------------|")
L.append("| ✅ SANOS | "+str(sc)+" | "+F(sc/total*100,'.1f')+"% |")
L.append("| ⚠️ A_REVISAR | "+str(rc)+" | "+F(rc/total*100,'.1f')+"% |")
L.append("| ❌ PÉRDIDA | "+str(pc)+" | "+F(pc/total*100,'.1f')+"% |")
L.append("| 🔍 SIN_COSTO | "+str(xc)+" | "+F(xc/total*100,'.1f')+"% |")
L.append("")
L.append("**Verificación:** "+str(sc+rc+pc+xc)+" = "+str(total)+" OK")
L.append("")

L.append("## 🏆 Top 10 Más Sanos")
L.append("")
L.append("| # | SKU | Nombre | Precio | M.Bru | M.Net | M.Dev40 |")
L.append("|---|-----|--------|--------|-------|-------|---------|")
for i,r in enumerate(tb,1):
    L.append("|"+str(i)+"|`"+r["sku"]+"`|"+r["nombre"]+"|$"+F(int(r["precio_actual"]),',')+"|"+F(float(r["margen_bruto_pct"]),'.1f')+"%|"+F(float(r["margen_neto_pct"]),'.1f')+"%|"+F(float(r["margen_con_devolucion_pct"]),'.1f')+"%|")
L.append("")

L.append("## 💀 Top 10 Más Dañados")
L.append("")
L.append("| # | SKU | Nombre | Precio | Costo Dropi | M.Bru | M.Dev40 | Veredicto |")
L.append("|---|-----|--------|--------|-------------|-------|---------|-----------|")
for i,r in enumerate(tm,1):
    L.append("|"+str(i)+"|`"+r["sku"]+"`|"+r["nombre"]+"|$"+F(int(r["precio_actual"]),',')+"|$"+F(float(r["costo_dropi"]),',.0f')+"|"+F(float(r["margen_bruto_pct"]),'.1f')+"%|"+F(float(r["margen_con_devolucion_pct"]),'.1f')+"%|"+r["veredicto"]+"|")
L.append("")

L.append("## 📐 Resumen por Rango de Precio")
L.append("")
L.append("| Rango | Total | SANOS | A_REVISAR | PÉRDIDA |")
L.append("|-------|-------|-------|-----------|---------|")
for k in sorted(rangos.keys()):
    v=rangos[k]
    L.append("|"+k+"|"+str(v["total"])+"|"+str(v["SANOS"])+"|"+str(v["A_REVISAR"])+"|"+str(v["PERDIDA"])+"|")
L.append("")

L.append("## ⛔ Los Productos que NO Pueden Ser Rentables (Ticket Ultra-Bajo)")
L.append("")
L.append("> **Criterio:** costo < $8.000 COP y precio mínimo > ratio de retiro sobre precio actual.")
L.append("> Con envío fijo de $" + F(ENVIO,',') + " COP, estos productos no son viables como unidad individual.")
L.append("")

if no_rentables:
    L.append("### RETIRAR")
    L.append("")
    L.append("| SKU | Nombre | Costo | Precio Actual | Precio Mín. Dev40 | Ratio |")
    L.append("|-----|--------|-------|---------------|-------------------|-------|")
    for it in no_rentables:
        nm=it["nombre"][:55]; pa=it["precio_actual"]
        L.append("|`"+it["sku"]+"`|"+nm+"|$"+F(int(it["costo"]),',')+"|$"+F(int(pa),',')+"|$"+F(int(it["precio_minimo_real"]),',')+"|"+F(it["ratio_aumento"],'.1f')+"x|")
    L.append("")

if pack_candidates:
    L.append("### PACK RECOMENDADO")
    L.append("")
    L.append("| SKU | Nombre | Costo | Precio Act. | Nota |")
    L.append("|-----|--------|-------|-------------|------|")
    for it in pack_candidates:
        L.append("|`"+it["sku"]+"`|"+it["nombre"][:50]+"|$"+F(int(it["costo"]),',')+"|$"+F(int(it["precio_actual"]),',')+"|"+it["nota"]+"|")
    L.append("")

if a_subir:
    L.append("### SUBIR DE PRECIO (ticket razonable)")
    L.append("")
    L.append("| SKU | Nombre | Costo | Precio Act. | Precio Mín. | Ratio |")
    L.append("|-----|--------|-------|-------------|-------------|-------|")
    for it in a_subir:
        L.append("|`"+it["sku"]+"`|"+it["nombre"][:50]+"|$"+F(int(it["costo"]),',')+"|$"+F(int(it["precio_actual"]),',')+"|$"+F(int(it["precio_minimo_real"]),',')+"|"+F(it["ratio_aumento"],'.1f')+"x|")
    L.append("")

L.append("## 💡 Recomendaciones Priorizadas")
L.append("")
L.append("1. **"+str(pc)+" productos PERDIDA:** Evaluar retiro progresivo o packs.")
L.append("2. **"+str(len(no_rentables))+" ultra-bajos (<$"+F(8000,',')+")**: No viables individuales — flete come toda rentabilidad.")
L.append("3. **"+str(len(a_subir))+" intermedios ($6K-$8K), ratio<=3x:** Subir precio psicológico para alcanzar >=25%.")
L.append("4. **"+str(len(pack_candidates))+" candidatos a PACK:** Agrupar 2-3 unidades diluye flete único.")
L.append("5. **"+str(xc)+" SIN_COSTO:** Sincronizar con Dropi antes de decidir.")
L.append("")

L.append("## 📏 Comparación con Análisis Previo")
L.append("")
L.append("> Monarca reportó: 104 SANOS / 95 A_REVISAR.")
L.append("> Este informe: "+str(sc)+" SANOS / "+str(rc)+" A_REVISAR.")
L.append("> Diferencias posibles: umbral (35 vs 25%), costos actualizados Dropi, tratamiento dropi_cost=0.")
L.append("> **Informe independiente:** calculado desde cero con solo products.json y config.json.")
L.append("")

L.append("---")
L.append("*Informe generado por TANK · Todo sale de products.json y config.json.*")

with open(MD_OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
md_size = os.path.getsize(MD_OUT_PATH)
print(f"[OK] MD: {md_size:,} bytes")

print("\n=== RESUMEN TANK ===")
print(f"Total:     {total}")
print(f"SANOS:     {sc} ({F(sc/total*100,'.1f')}%)")
print(f"A_REVISAR: {rc} ({F(rc/total*100,'.1f')}%)")
print(f"PÉRDIDA:   {pc} ({F(pc/total*100,'.1f')}%)")
print(f"S/COSTO:   {xc}")
print(f"RETIRAR:   {len(no_rentables)}")
print(f"SUBIR:     {len(a_subir)}")
print(f"PACK:      {len(pack_candidates)}")
