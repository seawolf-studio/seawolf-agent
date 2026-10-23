#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compila la Smart Web de SNEAKER HOUSE: plantilla.html + productos.json + QR -> sneaker-house.html
Formato compacto por producto: [slug,marca,modelo,categoria,genero,color,tallas,pm,pv,descripcion]
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
pl = open(os.path.join(BASE, "plantilla.html"), encoding="utf-8").read()
prod = json.load(open(os.path.join(BASE, "productos.json"), encoding="utf-8"))
qr = open(os.path.join(BASE, "..", "mockup", "qr-datauri.txt"), encoding="utf-8").read().strip()

filas = [[p["slug"], p["marca"], p["modelo"], p["categoria"], p["genero"], p["color"],
          p["tallas"], p["precio_mayorista"], p["precio_venta"], (p["descripcion"] or "")[:160]]
         for p in prod]
datos = json.dumps(filas, ensure_ascii=False, separators=(",", ":"))

out = pl.replace("__DATOS__", datos).replace("__QR__", qr)
dest = os.path.join(BASE, "sneaker-house.html")
open(dest, "w", encoding="utf-8").write(out)
print(f"[ok] {dest}  ({len(out):,} bytes)  productos={len(filas)}".replace(",", "."))
