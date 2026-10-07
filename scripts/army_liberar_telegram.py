#!/usr/bin/env python3
"""Sueltа a las sombras de Telegram: quita las variables de Telegram de su .env.
Reporta SOLO los nombres de variable eliminados (nunca valores)."""
import os
import time

BASE = r"C:\Users\Admin\AppData\Local\hermes\profiles"
SOMBRAS = ["igris", "tank", "greed", "iron", "tusk", "kamish", "kaisel", "titan", "jima", "beru"]
STAMP = time.strftime("%Y%m%d-%H%M%S")
CLAVES = ("TELEGRAM", "TG_BOT", "BOT_TOKEN", "CHAT_ID")

for s in SOMBRAS:
    d = os.path.join(BASE, s)
    for nombre in (".env", "env"):
        p = os.path.join(d, nombre)
        if not os.path.exists(p):
            continue
        lineas = open(p, encoding="utf-8", errors="replace").read().splitlines()
        quedan, quitadas = [], []
        for l in lineas:
            ls = l.strip()
            if not ls or ls.startswith("#"):
                quedan.append(l)
                continue
            clave = ls.split("=", 1)[0].strip().upper()
            if any(c in clave for c in CLAVES):
                quitadas.append(clave)   # nombre, no valor
            else:
                quedan.append(l)
        if quitadas:
            open(p + ".bak-pre-army-" + STAMP, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
            open(p, "w", encoding="utf-8").write("\n".join(quedan) + "\n")
            print("  %-8s %-6s eliminadas: %s" % (s, nombre, ", ".join(quitadas)))
        else:
            print("  %-8s %-6s (sin variables de telegram)" % (s, nombre))
        break
    else:
        print("  %-8s (no hay .env)" % s)
