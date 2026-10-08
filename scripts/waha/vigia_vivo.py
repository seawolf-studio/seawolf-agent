#!/usr/bin/env python3
"""Vigia en vivo de la Capa 2: muestra en orden cada paso de la cadena.
Uso: python3 vigia_vivo.py [segundos]"""
import os
import sqlite3
import sys
import time

seg = int(sys.argv[1]) if len(sys.argv) > 1 else 280
LOG = "/opt/waha/responder.log"
c = sqlite3.connect("/opt/waha/bus.db")
base = c.execute("SELECT MAX(id) FROM events").fetchone()[0]
logpos = os.path.getsize(LOG) if os.path.exists(LOG) else 0

print("VIGIA VIVO — marcador %s | %ds" % (base, seg))
print("(esperando lo que escriba la amiga del Monarca)\n")
vistos = set()
fin = time.time() + seg
while time.time() < fin:
    nuevos = list(c.execute("SELECT id,ts,kind,direction,actor,peer,substr(text,1,110) "
                            "FROM events WHERE id > ? ORDER BY id", (base,)))
    for r in nuevos:
        if r[0] in vistos:
            continue
        vistos.add(r[0])
        etiqueta = {"message": "MENSAJE ENTRA", "order": "ORDEN DEL DUENO",
                    "approval": "AVISO AL DUENO", "action": "RESPUESTA ENVIADA",
                    "order_processed": "ORDEN PROCESADA", "alert": "ALERTA"}.get(r[2], r[2].upper())
        print("[%s] %-18s %s" % (str(r[1])[11:19], etiqueta, str(r[6]).replace("\n", " ")))
        print("         actor=%s peer=%s" % (r[4], r[5]))
        # si entra un mensaje, refrescar las lineas nuevas del motor
        if r[2] == "message":
            time.sleep(8)
            with open(LOG, encoding="utf-8", errors="replace") as f:
                f.seek(logpos)
                for l in f:
                    if l.strip():
                        print("         motor> " + l.strip()[:130])
                logpos = f.tell()
    time.sleep(2)
print("\nVIGIA: %d eventos nuevos" % len(vistos))
