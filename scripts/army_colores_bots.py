#!/usr/bin/env python3
"""Asigna color a las tarjetas de Bots que no lo tenian (mismo formato hsl que las existentes)."""
import os
import time

import yaml

BASE = r"C:\Users\Admin\AppData\Local\hermes\profiles"
STAMP = time.strftime("%Y%m%d-%H%M%S")
# tonos elegidos por rol, separados de los ya usados (igris 182, tank 10, greed 9, iron 80, titan 124)
COLORES = {
    "kaisel": "hsl(205 68% 58%)",   # azul: arquitecto web
    "kamish": "hsl(320 68% 58%)",   # magenta: distribucion social
    "tusk":   "hsl(265 68% 58%)",   # violeta: trafico organico
    "jima":   "hsl(45 68% 58%)",    # ambar: automatizacion/nervios
    "beru":   "hsl(345 68% 58%)",   # carmesi: auditor implacable
}

print("%-8s %-16s %s" % ("SOMBRA", "COLOR ACTUAL", "COLOR NUEVO"))
print("-" * 48)
for s, color in COLORES.items():
    p = os.path.join(BASE, s, "profile.yaml")
    y = yaml.safe_load(open(p, encoding="utf-8")) or {}
    cab = (y.get("ui_meta") or {}).get("hermes-bots") or {}
    actual = cab.get("color", "(sin color)")
    if actual in ("(sin color)", "", None):
        open(p + ".bak-color-" + STAMP, "w", encoding="utf-8").write(open(p, encoding="utf-8").read())
        cab["color"] = color
        y.setdefault("ui_meta", {})["hermes-bots"] = cab
        with open(p, "w", encoding="utf-8") as f:
            yaml.safe_dump(y, f, allow_unicode=True, sort_keys=False)
        print("%-8s %-16s %s" % (s, actual, color))
    else:
        print("%-8s %-16s (ya tenia color, no se toca)" % (s, actual))
