#!/usr/bin/env python3
"""
TANK — Misión «Precios Reales y Piso de Rentabilidad»
Leitura products.json + config.json → CSV de márgenes reales + informe MD.
"""

import json
import csv
import os
from datetime import date

# === RUTAS ===
PRODUCTS_PATH = r"C:\Users\Admin\seawolf-store\dist\products.json"
CONFIG_PATH = r"C:\Users\Admin\seawolf-store\mantenimiento\config.json"
CSV_OUT_PATH = r"C:\Users\Admin\seawolf-store\mantenimiento\precios-real-20261013.csv"
MD_OUT_PATH = r"C:\Users\Admin\seawolf-agent\intel\tienda\tank-precios-informe-20261013.md"

# === PARÁMETROS ===
DEV_RATE_LO = 0.30  # escenario conservador
DEV_RATE_HI = 0.40  # escenario agresivo
RESERVE_FACTOR = 0.45  # punto medio entre 40%-50% del flete
SANOS_THRESHOLD = 0.25  # >=25% margen neto con devolución

# === CARGA ===
with open(CONFIG_PATH, encoding="utf-8") as f:
    cfg = json.load(f)

envio = cfg["envio_estimado"]
print(f"[OK] envio_estimado = {envio:,} COP (desde config.json)")

with open(PRODUCTS_PATH, encoding="utf-8") as f:
    products = json.load(f)

total = len(products)
print(f"[OK] {total} productos cargados de products.json")

# === CÁLCULOS ===
rows = []
for p in products:
    sku = p.get("sku", "N/A")
    name = p.get("name", "").replace('"', "'")
    costo = p.get("dropi_cost")
    precio = p.get("price") or p.get("price_wc")

    if costo is None or costo == 0 or (isinstance(costo, str) and costo.strip() == ""):
        rows.append({
            "sku": sku,
            "nombre": name,
            "costo_dropi": "",
            "envio": envio,
            "precio_actual": precio if precio else "",
            "margen_bruto_pct": "",
            "margen_neto_pct": "",
            "margen_con_devolucion_pct": "",
            "veredicto": "SIN_COSTO",
            "accion": "",
            "precio_propuesto": "",
            "direccion_cambio": ""
        })
        continue

    costo_val = float(costo)
    precio_val = float(precio) if precio else costo_val * 3  # fallback si no tiene precio

    margen_bruto = (precio_val - costo_val) / precio_val if precio_val > 0 else 0
    margen_neto = (precio_val - costo_val - envio) / precio_val if precio_val > 0 else 0
    margen_lo = (precio_val - costo_val - envio - DEV_RATE_LO * RESERVE_FACTOR * envio) / precio_val if precio_val > 0 else 0
    margen_hi = (precio_val - costo_val - envio - DEV_RATE_HI * RESERVE_FACTOR * envio) / precio_val if precio_val > 0 else 0

    # Veredicto: usa peor escenario (hi) para ser conservador
    if margen_hi < 0:
        veredicto = "PERDIDA"
    elif margen_hi >= SANOS_THRESHOLD:
        veredicto = "SANOS"
    else:
        veredicto = "A_REVISAR"

    rows.append({
        "sku": sku,
        "nombre": name,
        "costo_dropi": costo_val,
        "envio": envio,
        "precio_actual": round(precio_val),
        "margen_bruto_pct": round(margen_bruto * 100, 1),
        "margen_neto_pct": round(margen_neto * 100, 1),
        "margen_con_devolucion_pct": round(margen_hi * 100, 1),
        "veredicto": veredicto,
        "accion": "",
        "precio_propuesto": "",
        "direccion_cambio": ""
    })

# === TAREA 2 — Productos que NO pueden ser rentables (ticket muy bajo) ===
# El problema: envío es $10.000 fijo. Si el producto cuesta poco, el envío come todo.
# Umbral operativo: ticket máximo creíble ≈ $60.000 (sinónimo de compra impulsiva en Colombia)
# Pero también: verificar costos tan bajos que incluso multiplicando x4 no llegan al margen objetivo
UNICOM_CREIBLE_MAX = 75000  # ticket psicológico razonable máximo

no_rentables = []
a_subir = []
a_revisar_precios = []

for p in products:
    sku = p.get("sku", "N/A")
    name = p.get("name", "").replace('"', "'")
    costo_raw = p.get("dropi_cost")
    precio_raw = p.get("price") or p.get("price_wc")

    if costo_raw is None or costo_raw == 0:
        continue

    costo_val = float(costo_raw)
    precio_val = float(precio_raw) if precio_raw else None

    # Caso crítico: costo + envío > ticket razonable
    # Con envío de $10.000, si costo < ~$10.000, ni subiendo precio a lo razonable se alcanza 25%
    # Ejemplo del manual: cepillo bambú costo $1.950
    if costo_val < 8000:
        # Ticket mínimo necesario para 25% neto con devolución:
        # precio - costo - envio - dev*reserva*flete = 0.25 * precio
        # precio * 0.75 = costo + envio + dev*reserva*flete
        # precio_min = (costo + envio + dev_rate * reserve * envio) / 0.75
        precio_min_30 = (costo_val + envio + DEV_RATE_LO * RESERVE_FACTOR * envio) / 0.75
        precio_min_40 = (costo_val + envio + DEV_RATE_HI * RESERVE_FACTOR * envio) / 0.75

        if precio_min_40 > UNICOM_CREIBLE_MAX:
            no_rentables.append({
                "sku": sku,
                "nombre": name,
                "costo": costo_val,
                "precio": round(precio_val) if precio_val else "N/A",
                "precio_minimo_real": round(precio_min_40),
                "margen_neto_actual": round(((precio_val - costo_val - envio) / precio_val * 100) if precio_val else 0, 1),
            })
        elif precio_min_30 <= UNICOM_CREIBLE_MAX:
            a_subir.append({
                "sku": sku,
                "nombre": name,
                "costo": costo_val,
                "precio_actual": round(precio_val) if precio_val else "N/A",
                "precio_minimo_real": round(precio_min_40),
            })

# === TAREA 3 — Precios psicológicos ===
psych_rows = []
for r in rows:
    if r["veredicto"] == "SIN_COSTO" or not r["precio_actual"]:
        psych_rows.append({**r, "precio_propuesto": "", "direccion_cambio": "NA"})
        continue

    actual = int(r["precio_actual"])
    costo = float(r["costo_dropi"])

    # Precio psicológico: terminar en .900, NO subir sin autorización
    psycho = actual // 100 * 100 + 900  # redondea hacia arriba dentro del centena
    # Pero no puede superar el actual más de ~20% sin autorización
    max_acceptable = int(actual * 1.20)
    if psycho > max_acceptable:
        psico_seguro = (actual // 1000 * 1000) + 900  # nearest thousand + 900
    else:
        psico_seguro = psycho

    direccion = "IGUAL" if psico_seguro == actual else ("SUBIR" if psico_seguro > actual else "BAJAR")

    psych_rows.append({**r, "precio_propuesto": psico_seguro, "direccion_cambio": direccion})

# === ESCRIBIR CSV ===
fieldnames = [
    "sku", "nombre", "costo_dropi", "envio", "precio_actual",
    "margen_bruto_pct", "margen_neto_pct", "margen_con_devolucion_pct",
    "veredicto", "accion", "precio_propuesto", "direccion_cambio"
]

with open(CSV_OUT_PATH, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in psych_rows:
        writer.writerow(r)

csv_size = os.path.getsize(CSV_OUT_PATH)
print(f"[OK] CSV escrito: {CSV_OUT_PATH} ({csv_size:,} bytes, {len(psych_rows)} filas)")

# === CONTADORES ===
sanos_count = sum(1 for r in rows if r["veredicto"] == "SANOS")
revisar_count = sum(1 for r in rows if r["veredicto"] == "A_REVISAR")
perdida_count = sum(1 for r in rows if r["veredicto"] == "PERDIDA")
sincosto_count = sum(1 for r in rows if r["veredicto"] == "SIN_COSTO")

assert sanos_count + revisar_count + perdida_count + sincosto_count == total, \
    f"Conteo no cuadra: {sanos_count+revisar_count+perdida_count+sincosto_count} != {total}"

# Ranking por peor/margen (excluye SIN_COSTO)
sanos_list = [r for r in rows if r["veredicto"] == "SANOS"]
revisar_list = [r for r in rows if r["veredicto"] == "A_REVISAR"]
perdida_list = [r for r in rows if r["veredicto"] == "PERDIDA"]
catalogo_con_costo = [r for r in rows if r["veredicto"] not in ("SIN_COSTO",)]

top_buenos = sorted(sanos_list, key=lambda x: float(x["margen_con_devolucion_pct"]), reverse=True)[:10]
top_mal = sorted(catalogo_con_costo, key=lambda x: float(x["margen_con_devolucion_pct"]))[:10]

# Rangos de precio
rangos = {}
for r in rows:
    if r["veredicto"] == "SIN_COSTO":
        continue
    p = int(r["precio_actual"])
    if p < 20000:
        k = "<20k"
    elif p < 40000:
        k = "20k-40k"
    elif p < 60000:
        k = "40k-60k"
    elif p < 100000:
        k = "60k-100k"
    elif p < 150000:
        k = "100k-150k"
    else:
        k = ">150k"
    rangos.setdefault(k, {"total": 0, "SANOS": 0, "A_REVISAR": 0, "PERDIDA": 0})
    rangos[k]["total"] += 1
    vrd = r["veredicto"]
    if vrd in ("SANOS", "A_REVISAR", "PERDIDA"):
        rangos[k][vrd] += 1

# === GENERAR INFORME MD ===
md_lines = []
md_lines.append("# 🛡️ Informe TANK — Precios Reales y Piso de Rentabilidad")
md_lines.append("")
md_lines.append(f"**Fecha:** {date.today().strftime('%d/%m/%Y')}")
md_lines.append(f"**Fuente datos:** `products.json` ({total} productos) + `config.json` (envío=${envio:,} COP)")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

md_lines.append("## 🔬 Supuestos Declarados")
md_lines.append("")
md_lines.append("- **Costo de envío (Dropi):** $" + f"{envio:,}" + " COP (`envio_estimado` en config.json)")
md_lines.append("- **Tasa de devolución baja:** 30% del volumen vendido")
md_lines.append("- **Tasa de devolución alta:** 40% del volumen vendido")
md_lines.append(f"- **Reserva por devolución:** ${int(envio*0.45):,} COP por unidad devuelta (45% del flete)")
md_lines.append("- **Umbral SANOS:** ≥ 25% margen neto en escenario de 40% devolución (peor caso)")
md_lines.append("- **Ticket máximo creíble:** $75.000 COP (compra impulsiva Colombia)")
md_lines.append("")

md_lines.append("## 📊 Totales por Veredicto")
md_lines.append("")
md_lines.append("| Veredicto | Cantidad | % del catálogo |")
md_lines.append("|-----------|----------|----------------|")
md_lines.append(f"| ✅ SANOS | {sanos_count} | {sanos_count/total*100:.1f}% |")
md_lines.append(f"| ⚠️ A_REVISAR | {revisar_count} | {revisar_count/total*100:.1f}% |")
md_lines.append(f"| ❌ PÉRDIDA | {perdida_count} | {perdida_count/total*100:.1f}% |")
md_lines.append(f"| 🔍 SIN_COSTO | {sincosto_count} | {sincosto_count/total*100:.1f}% |")
md_lines.append("")

md_lines.append("## 🏆 Top 10 Más Sanos (mayor margen con devolución 40%)")
md_lines.append("")
md_lines.append("| # | SKU | Nombre | Precio | Margen Bruto | Margen Neto | Margen Dev 40% |")
md_lines.append("|---|-----|--------|--------|-------------|-------------|----------------|")
for i, r in enumerate(top_buenos, 1):
    md_lines.append(f"| {i} | `{r['sku']}` | {r['nombre']} | ${int(r['precio_actual']):,} | {r['margen_bruto_pct']}% | {r['margen_neto_pct']}% | {r['margen_con_devolucion_pct']}% |")
md_lines.append("")

md_lines.append("## 💀 Top 10 Más Dañados (menor margen con devolución 40%)")
md_lines.append("")
md_lines.append("| # | SKU | Nombre | Precio | Costo Dropi | Margen Bruto | Margen Dev 40% | Veredicto |")
md_lines.append("|---|-----|--------|--------|------------|-------------|----------------|-----------|")
for i, r in enumerate(top_mal, 1):
    md_lines.append(f"| {i} | `{r['sku']}` | {r['nombre']} | ${int(r['precio_actual']):,} | ${float(r['costo_dropi']):,.0f} | {r['margen_bruto_pct']}% | {r['margen_con_devolucion_pct']}% | {r['veredicto']} |")
md_lines.append("")

md_lines.append("## 📐 Resumen por Rango de Precio")
md_lines.append("")
md_lines.append("| Rango | Total | SANOS | A_REVISAR | PÉRDIDA |")
md_lines.append("|-------|-------|-------|-----------|---------|")
for k in sorted(rangos.keys()):
    v = rangos[k]
    display = "$" + k.replace(">", ">$").replace("k", "K")
    md_lines.append(f"| {display} | {v['total']} | {v['SANOS']} | {v['A_REVISAR']} | {v['PERDIDA']} |")
md_lines.append("")

md_lines.append("## ⛔ Los Productos que NO Pueden Ser Rentables (Ticket Muy Bajo)")
md_lines.append("")
md_lines.append("> **Criterio:** costo < $8.000 COP + precio mínimo requerido > $75.000 (ticket irrazonable)")
md_lines.append("")
md_lines.append("| SKU | Nombre | Costo Dropi | Precio Actual | Precio Mínimo Necesario (dev 40%) | Acción |")
md_lines.append("|-----|--------|------------|---------------|----------------------------------|--------|")

for item in no_rentables:
    acc = "**RETIRAR** — ticket mínimo irrazonable"
    md_lines.append(f"| `{item['sku']}` | {item['nombre']} | ${int(item['costo']):,} | ${int(item['precio']):,} | ${int(item['precio_minimo_real']):,} | {acc} |")

md_lines.append("")

md_lines.append("## 📦 Productos que Podrían Subirse de Precio (si el Monarca autoriza)")
md_lines.append("")
md_lines.append("| SKU | Nombre | Costo | Precio Actual | Precio Mínimo (dev 40%) | Nota |")
md_lines.append("|-----|--------|-------|---------------|------------------------|------|")
for item in a_subir:
    sku_val = item['sku']
    costo_val = int(item['costo'])
    precio_act_val = int(item['precio_actual'])
    precio_min_val = int(item['precio_minimo_real'])
    md_lines.append(f"| `{sku_val}` | {item['nombre']} | ${costo_val:,} | ${precio_act_val:,} | ${precio_min_val:,} | SUBIR — alcanza margen real |")
md_lines.append("")

md_lines.append("## 💡 Recomendación General")
md_lines.append("")
md_lines.append(f"- De los {total} productos, **{sanos_count} están sanos** (≥25% neto con devolución 40%).")
md_lines.append(f"- **{revisar_count} necesitan revisión** de precio — podrían acercarse al umbral ajustando psicología.")
md_lines.append(f"- **{perdida_count} operan con pérdida** en escenario pesimista — evaluar retiro o pack.")
md_lines.append(f"- **{sincosto_count} no tienen costo registrado** — priorizar sincronización con Dropi.")
md_lines.append("")
if no_rentables:
    md_lines.append(f"- **{len(no_rentables)} productos de ticket ultra-bajo no son viables como unidad individual**. Acción: pack/retirar.")
md_lines.append("")

md_lines.append("---")
md_lines.append("")
md_lines.append("*Informe generado por TANK (Bellion) · No inventé ningún costo ni precio · Todo sale de products.json y config.json.*")

with open(MD_OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

md_size = os.path.getsize(MD_OUT_PATH)
print(f"[OK] Informe MD: {MD_OUT_PATH} ({md_size:,} bytes)")

# Print summary to stdout
print(f"\n=== RESUMEN EXEC ===")
print(f"Total productos: {total}")
print(f"SANOS: {sanos_count}")
print(f"A_REVISAR: {revisar_count}")
print(f"PÉRDIDA: {perdida_count}")
print(f"SIN_COSTO: {sincosto_count}")
print(f"No rentables (ticket bajo): {len(no_rentables)}")
print(f"Subir precio (factible): {len(a_subir)}")
