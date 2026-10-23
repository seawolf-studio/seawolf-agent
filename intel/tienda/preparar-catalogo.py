#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PASO 2 — SNEAKER HOUSE: SKU + slug + renombrado de fotos + data layer inicial.
Lee CONSOLIDADO.csv -> asigna SKU/slug unicos -> copia fotos a productos/ -> escribe productos.csv/json.

SKU  = SH-<MARCA3>-<NNNN>   ej: SH-NIK-0001, SH-JOR-0107   (marca en 3 letras; '?'->GEN; secuencial)
slug = marca-modelo-color-NNN  (URL-safe, unico; para rutas e imagen)
Foto -> productos/<slug>.jpg

Uso:
  python preparar-catalogo.py --dry-run     # solo muestra, NO escribe
  python preparar-catalogo.py               # aplica
Autor: Bellion para Seawolf Studio.
"""
import argparse, csv, json, os, re, shutil, unicodedata, collections

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "CONSOLIDADO.csv")
OUT = os.path.join(BASE, "productos")
IMG = os.path.join(OUT, "imagenes")

# grupo (CSV) -> carpeta de fotos en disco
GRUPO_DIR = {
    "BARCELONA MALL 11-12A": "barcelona",
    "LOBO_STORE_SHOES #1": "lobo_shoes",
    "Difusión HYPE SNKS": "hype_snks",
    "Ropa y Accesorios": "ropa_accesorios",
    "GRUPO CONTAINER 2": "container2",
    "Ultimas Tendencias Zapatillas": "ultimas_tendencias",
}


def slugify(txt):
    txt = unicodedata.normalize("NFKD", txt or "").encode("ascii", "ignore").decode()
    txt = re.sub(r"[^a-zA-Z0-9]+", "-", txt).strip("-").lower()
    return txt


def marca3(m):
    m = (m or "").strip()
    if not m or m == "?":
        return "GEN"
    return re.sub(r"[^A-Za-z]", "", m).upper()[:3] or "GEN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    with open(CSV, encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))

    vistos = collections.Counter()
    productos = []
    sin_precio = 0
    for i, r in enumerate(filas, 1):
        sku = f"SH-{marca3(r['marca'])}-{i:04d}"
        base = slugify(f"{r['marca']}-{r['modelo']}-{r['color']}") or "producto"
        vistos[base] += 1
        slug = base if vistos[base] == 1 else f"{base}-{vistos[base]}"
        pm = int(r["precio_mayorista"]) if (r["precio_mayorista"] or "").isdigit() else 0
        pv = int(r["precio_venta"]) if (r["precio_venta"] or "").isdigit() else 0
        if pm == 0:
            sin_precio += 1
        grupo = r["_grupo"]
        carpeta = GRUPO_DIR.get(grupo)
        origen = os.path.join(BASE, carpeta, r["archivo"]) if carpeta else None
        productos.append({
            "sku": sku, "slug": slug,
            "marca": r["marca"] or "", "modelo": r["modelo"] or "",
            "categoria": r["categoria"] or "", "tipo": r["tipo"] or "",
            "genero": r["genero"] or "", "color": r["color"] or "",
            "tallas": r["tallas"] or "",
            "precio_mayorista": pm, "precio_venta": pv,
            "descripcion": r["descripcion"] or "", "notas": r["notas"] or "",
            "grupo": grupo,
            "imagen": f"/imagenes/{slug}.jpg",
            "foto_origen": origen,
            "foto_existe": bool(origen and os.path.exists(origen)),
        })

    faltan = sum(1 for p in productos if not p["foto_existe"])
    print(f"productos: {len(productos)} | sin precio: {sin_precio} | fotos faltantes: {faltan}")
    print("ejemplos:")
    for p in productos[:5]:
        print(f"  {p['sku']}  {p['slug']:<40} {p['marca']}/{p['modelo']}  ${p['precio_venta']}  foto_ok={p['foto_existe']}")

    if a.dry_run:
        print("\n[DRY-RUN] no se escribio nada.")
        return

    os.makedirs(IMG, exist_ok=True)
    for p in productos:
        if p["foto_existe"]:
            shutil.copy2(p["foto_origen"], os.path.join(IMG, p["slug"] + ".jpg"))
    with open(os.path.join(OUT, "productos.json"), "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)
    cols = ["sku", "slug", "marca", "modelo", "categoria", "genero", "color", "tallas",
            "precio_mayorista", "precio_venta", "imagen", "grupo", "descripcion"]
    with open(os.path.join(OUT, "productos.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(productos)
    print(f"\n[ok] {OUT}\\productos.json + productos.csv + {len(productos)-faltan} fotos en imagenes/")


if __name__ == "__main__":
    main()
