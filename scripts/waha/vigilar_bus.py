#!/usr/bin/env python3
"""Vigila el bus N segundos y reporta TODO lo nuevo: si su amiga escribe, se ve aqui."""
import sqlite3
import sys
import time

seg = int(sys.argv[1]) if len(sys.argv) > 1 else 120
c = sqlite3.connect("/opt/waha/bus.db")
base = c.execute("SELECT MAX(id) FROM events").fetchone()[0]
print("marcador inicial: %s | vigilando %ds..." % (base, seg))
vistos = set()
fin = time.time() + seg
while time.time() < fin:
    for r in c.execute("SELECT id,ts,kind,direction,actor,peer,substr(text,1,90) "
                       "FROM events WHERE id > ? ORDER BY id", (base,)):
        if r[0] in vistos:
            continue
        vistos.add(r[0])
        print("  [%s] %-14s %-3s %-22s -> %-22s | %s"
              % (str(r[1])[11:19], r[2], r[3], str(r[4])[:22], str(r[5])[:22], r[6]))
    time.sleep(3)
if not vistos:
    print("  (sin novedades en %ds)" % seg)
else:
    print("  -> %d eventos nuevos" % len(vistos))
