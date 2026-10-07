#!/usr/bin/env python3
"""Verifica/restaura el NOMBRE visible de cada sombra en el panel de Bots.
(profile.yaml -> ui_meta.hermes-bots.title). No cambia forma, color ni posicion."""
import os
import time

import yaml

BASE = r"C:\Users\Admin\AppData\Local\hermes\profiles"
SOMBRAS = ["igris", "tank", "greed", "iron", "tusk", "kamish", "kaisel", "titan", "jima", "beru"]
STAMP = time.strftime("%Y%m%d-%H%M%S")

print("%-8s %-14s %-14s %-12s %s" % ("SOMBRA", "TITULO ACTUAL", "TITULO NUEVO", "FORMA", "COLOR"))
print("-" * 76)
arreglados = []
for s in SOMBRAS:
    p = os.path.join(BASE, s, "profile.yaml")
    if not os.path.exists(p):
        print("  %-8s (SIN profile.yaml -> no aparece en Bots)" % s)
        continue
    y = yaml.safe_load(open(p, encoding="utf-8")) or {}
    cab = (y.get("ui_meta") or {}).get("hermes-bots") or {}
    actual = (cab.get("title") or "").strip()
    nuevo = actual if actual else s.capitalize()
    if nuevo != actual:
        open(p + ".bak-title-" + STAMP, "w", encoding="utf-8").write(
            open(p, encoding="utf-8").read())
        cab["title"] = nuevo
        y.setdefault("ui_meta", {})["hermes-bots"] = cab
        with open(p, "w", encoding="utf-8") as f:
            yaml.safe_dump(y, f, allow_unicode=True, sort_keys=False)
        arreglados.append(s)
    print("  %-8s %-14s %-14s %-12s %s" % (s, actual or "(vacio)", nuevo,
                                           cab.get("shape", "?"), cab.get("color", "?")))

print()
print("  Tarjetas reparadas: %s" % (", ".join(arreglados) if arreglados else "(ninguna: todas tenian nombre)"))
