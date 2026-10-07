#!/usr/bin/env python3
"""Verificacion forense del estado real del ejercito (sobre el disco).
Distingue variables ACTIVAS de COMENTARIOS. Nunca imprime valores de secretos."""
import os

import yaml

BASE = r"C:\Users\Admin\AppData\Local\hermes\profiles"
SOMBRAS = ["igris", "tank", "greed", "iron", "tusk", "kamish", "kaisel", "titan", "jima", "beru"]

print("%-8s %-34s %-3s %-3s %-9s %s" % ("SOMBRA", "MODELO", "'/'", "FB", "TELEGRAM", "TZ"))
print("-" * 78)
ok_fb = ok_tg = 0
for s in SOMBRAS:
    d = os.path.join(BASE, s)
    c = yaml.safe_load(open(os.path.join(d, "config.yaml"), encoding="utf-8"))
    modelo = (c.get("model") or {}).get("default", "")
    fb = c.get("fallback_providers") or []
    tz = c.get("timezone", "")

    # telegram en .env: separar ACTIVAS de COMENTARIOS
    activas = []
    p = os.path.join(d, ".env")
    if os.path.exists(p):
        for l in open(p, encoding="utf-8", errors="replace").read().splitlines():
            ls = l.strip()
            if not ls or ls.startswith("#"):
                continue
            clave = ls.split("=", 1)[0].strip().upper()
            if "TELEGRAM" in clave or "BOT_TOKEN" in clave:
                activas.append(clave)
    if fb and len(fb) == 2:
        ok_fb += 1
    if not activas:
        ok_tg += 1
    print("%-8s %-34s %-3s %-3d %-9s %s" % (
        s, modelo[:34], "si" if "/" in modelo else "NO", len(fb),
        ("ACTIVAS:" + ",".join(activas)) if activas else "ninguna", tz))

print()
print("CONFIG con 2 fallbacks: %d/10   |   SIN telegram activo: %d/10" % (ok_fb, ok_tg))
print()
print("=== el unico match de 'telegram' que ve Beru (contexto, enmascarado) ===")
for s in SOMBRAS:
    p = os.path.join(BASE, s, ".env")
    if not os.path.exists(p):
        continue
    for l in open(p, encoding="utf-8", errors="replace").read().splitlines():
        if "telegram" in l.lower():
            espejo = l.strip()
            if "=" in espejo:
                k, v = espejo.split("=", 1)
                espejo = "%s=<oculto %d chars>" % (k, len(v))
            print("  %-8s %s" % (s, espejo[:90]))
