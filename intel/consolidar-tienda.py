#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CONSOLIDADOR DE TIENDA — une los catalogos de todos los grupos, perfila cada negocio
y busca el mismo modelo a distinto precio (arbitraje entre proveedores).

  python consolidar-tienda.py [--base C:\\Users\\Admin\\tienda] [--margen 0.35]
Salida: <base>/CONSOLIDADO.csv  +  <base>/informe-tienda.md
"""
import os, sys, json, csv, re, unicodedata
from collections import defaultdict

GRUPOS = {
 "barcelona":        ("BARCELONA MALL 11-12A", "zapatillas"),
 "lobo_shoes":       ("LOBO_STORE_SHOES #1", "zapatillas"),
 "hype_snks":        ("Difusión HYPE SNKS", "zapatillas"),
 "ropa_accesorios":  ("Ropa y Accesorios", "ropa"),
 "container2":       ("GRUPO CONTAINER 2", "mixto"),
 "ultimas_tendencias": ("Ultimas Tendencias Zapatillas", "zapatillas"),
}

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+"," ",s).strip()

def main():
    base = r"C:\Users\Admin\tienda"
    if "--base" in sys.argv: base = sys.argv[sys.argv.index("--base")+1]
    margen = 0.35
    if "--margen" in sys.argv: margen = float(sys.argv[sys.argv.index("--margen")+1])

    todos=[]; resumen=[]
    for slug,(nombre,cat) in GRUPOS.items():
        p = os.path.join(base, slug, "catalogo.json")
        if not os.path.exists(p):
            resumen.append({"slug":slug,"grupo":nombre,"n":0,"con_precio":0,"estado":"sin catalogo"}); continue
        d = json.load(open(p, encoding="utf-8"))
        con = [r for r in d if r.get("precio_mayorista")]
        ps = [r["precio_mayorista"] for r in con]
        marcas = defaultdict(int)
        for r in d: marcas[(r.get("marca") or "?").strip().title()] += 1
        for r in d:
            r["_grupo"]=nombre; r["_slug"]=slug; r["_cat"]=cat
        todos += d
        resumen.append({"slug":slug,"grupo":nombre,"n":len(d),"con_precio":len(con),
                        "pmin":min(ps) if ps else 0,"pmax":max(ps) if ps else 0,
                        "marcas":dict(sorted(marcas.items(), key=lambda x:-x[1])[:6]),"estado":"ok"})

    # consolidado
    campos=["_grupo","archivo","categoria","marca","modelo","tipo","genero","color","tallas",
            "precio_mayorista","precio_origen","precio_venta","descripcion","notas"]
    with open(os.path.join(base,"CONSOLIDADO.csv"),"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=campos,extrasaction="ignore"); w.writeheader()
        for r in todos:
            r2=dict(r); r2["categoria"]=r.get("_cat","")
            pm = r.get("precio_mayorista") or 0
            r2["precio_venta"] = int(round(pm*(1+margen)/1000)*1000) if pm else 0
            w.writerow(r2)

    # arbitraje: mismo marca+modelo en >1 grupo con precios distintos
    idx=defaultdict(list)
    for r in todos:
        k=(norm(r.get("marca")), norm(r.get("modelo")))
        if k[0] and k[1] and r.get("precio_mayorista"): idx[k].append(r)
    arb=[]
    for k,v in idx.items():
        gs={x["_grupo"] for x in v}
        if len(gs)>1:
            ps=sorted((x["precio_mayorista"], x["_grupo"], x["modelo"]) for x in v)
            if ps[0][0] < ps[-1][0]: arb.append((k, ps))
    arb.sort(key=lambda t:-(t[1][-1][0]-t[1][0][0]))

    L=[]
    L.append("# INFORME DE TIENDA — barrido de grupos de proveedores")
    L.append(f"\nGenerado por Bellion · margen asumido **{margen:.0%}**\n")
    L.append("## 1. Grupos barridos\n")
    L.append("| Grupo | Ítems | Con precio | Rango mayorista | Top marcas |")
    L.append("|---|---|---|---|---|")
    for r in resumen:
        rng = f"${r.get('pmin',0):,} – ${r.get('pmax',0):,}" if r.get("con_precio") else "—"
        mk = ", ".join(f"{k}({v})" for k,v in list(r.get("marcas",{}).items())[:4]) or "—"
        L.append(f"| {r['grupo']} | {r['n']} | {r['con_precio']} | {rng} | {mk} |")
    L.append("\n## 2. Listado ALTERNO — grupos que SÍ cumplen (imagen + precio)\n")
    cal = [r for r in resumen if r.get("con_precio",0) >= 5]
    L.append("| Grupo | Productos con precio | Se puede catalogar |")
    L.append("|---|---|---|")
    for r in cal: L.append(f"| {r['grupo']} | {r['con_precio']} | ✅ sí |")
    no = [r for r in resumen if 0 < r.get("n",0) and r.get("con_precio",0) < 5]
    for r in no: L.append(f"| {r['grupo']} | {r.get('con_precio',0)} | ⚠️ precio NO en el texto (hay que leerlo de la foto) |")
    L.append("\n## 3. Arbitraje entre proveedores (mismo modelo, distinto precio)\n")
    if arb:
        L.append("| Marca | Modelo | Más barato | Precio | Más caro | Precio | Ahorro |")
        L.append("|---|---|---|---|---|---|---|")
        for (mk,md), ps in arb[:25]:
            L.append(f"| {mk.title()} | {md} | {ps[0][1]} | ${ps[0][0]:,} | {ps[-1][1]} | ${ps[-1][0]:,} | ${ps[-1][0]-ps[0][0]:,} |")
    else:
        L.append("_Sin coincidencias exactas de modelo entre grupos (usar por marca/categoría)._")
    L.append(f"\n## 4. Totales\n")
    L.append(f"- Ítems totales: **{len(todos)}**")
    ps=[r['precio_mayorista'] for r in todos if r.get('precio_mayorista')]
    if ps: L.append(f"- Precio mayorista: **${min(ps):,} – ${max(ps):,}** (prom ${sum(ps)//len(ps):,})")
    L.append(f"- Archivos: `CONSOLIDADO.csv` + `catalogo.csv` por grupo")
    open(os.path.join(base,"informe-tienda.md"),"w",encoding="utf-8").write("\n".join(L))
    print("\n".join(L))
    print(f"\n-> {os.path.join(base,'informe-tienda.md')}")

if __name__=="__main__": main()
