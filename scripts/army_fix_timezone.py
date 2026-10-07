#!/usr/bin/env python3
"""Corrige la zona horaria invalida ('(GMT-5)') en los configs de las sombras.
'America/Bogota' es la zona IANA correcta para el Monarca."""
import os
import re
import time

BASE = r"C:\Users\Admin\AppData\Local\hermes\profiles"
SOMBRAS = ["igris", "tank", "greed", "iron", "tusk", "kamish", "kaisel", "titan", "jima", "beru"]
STAMP = time.strftime("%Y%m%d-%H%M%S")
invalidas = re.compile(r"^\s*timezone:\s*['\"]?\(GMT[-+]\d+\)['\"]?\s*$", re.M)

print("ZONA HORARIA — correccion en las sombras")
for s in SOMBRAS:
    p = os.path.join(BASE, s, "config.yaml")
    if not os.path.exists(p):
        continue
    txt = open(p, encoding="utf-8").read()
    m = invalidas.search(txt)
    if m:
        open(p + ".bak-tz-" + STAMP, "w", encoding="utf-8").write(txt)
        nuevo = invalidas.sub("timezone: America/Bogota", txt)
        open(p, "w", encoding="utf-8").write(nuevo)
        print("  %-8s corregido: %s -> timezone: America/Bogota" % (s, m.group(0).strip()))
    else:
        print("  %-8s (sin zona invalida)" % s)

# reporte del global (no se toca sin autorizacion)
g = r"C:\Users\Admin\AppData\Local\hermes\config.yaml"
txt = open(g, encoding="utf-8").read()
mm = re.search(r"^\s*timezone:.*$", txt, re.M)
print("\nGLOBAL (default/Bellion): %s" % (mm.group(0).strip() if mm else "(sin timezone)"))
