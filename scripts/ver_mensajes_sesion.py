#!/usr/bin/env python3
"""Que hay REALMENTE registrado en la sesion del agente (linea 2).
Solo resume: remitente, fecha, tipo y si tiene media. No imprime contenido privado completo."""
import collections
import json
import os

LOG = "/opt/waha/messages.log"
if not os.path.exists(LOG):
    print("no hay messages.log")
    raise SystemExit

por_remitente = collections.Counter()
por_tipo = collections.Counter()
entrantes = []
total = 0
for linea in open(LOG, encoding="utf-8", errors="replace"):
    linea = linea.strip()
    if not linea:
        continue
    try:
        ev = json.loads(linea)
    except Exception:
        continue
    total += 1
    if ev.get("event") != "message":
        continue
    p = ev.get("payload") or {}
    if p.get("fromMe"):
        continue
    frm = str(p.get("from") or "?")
    por_remitente[frm] += 1
    has = p.get("hasMedia")
    mt = ((p.get("media") or {}).get("mimetype") or "").lower()
    tipo = ("voz" if mt.startswith("audio") else "video" if mt.startswith("video")
            else "imagen" if mt.startswith("image") else "documento" if mt.startswith("application")
            else "archivo" if has else "texto")
    por_tipo[tipo] += 1
    entrantes.append((ev.get("_ts") or p.get("timestamp") or "?",
                      frm[:24], tipo, (p.get("body") or "")[:60]))

print("Eventos totales en el sink: %d | mensajes ENTRANTES (fromMe=false): %d\n" % (total, len(entrantes)))
print("=== Por remitente ===")
for k, v in por_remitente.most_common(15):
    print("  %-30s %d" % (k, v))
print("\n=== Por tipo ===")
for k, v in por_tipo.most_common():
    print("  %-12s %d" % (k, v))
print("\n=== Ultimos 12 entrantes (remitente / tipo / inicio del texto) ===")
for ts, frm, tipo, body in entrantes[-12:]:
    print("  %-12s %-24s %-10s %s" % (str(ts)[:12], frm, tipo, body.replace("\n", " ")))
