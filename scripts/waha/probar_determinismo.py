#!/usr/bin/env python3
"""Prueba la MEMORIA DE VEREDICTOS: el mismo contenido dos veces debe dar el mismo veredicto
(y la segunda debe ser un acierto de cache)."""
import json
import sys
import time
import urllib.request

URL = "http://172.16.0.1:3011/"
CACHE = "/opt/waha/clasificaciones.json"
TEXTO = ("PRUEBA DETERMINISMO: se cayo una matera del balcon del 801 y casi le pega a un nino "
         "que iba pasando con su mama")


def inyectar(marca):
    payload = {"event": "message", "session": "seawolf", "payload": {
        "id": "det_%s" % marca, "from": "573007778899@c.us", "fromMe": False,
        "body": TEXTO, "hasMedia": False, "media": None,
        "_data": {"Info": {"Chat": "573007778899@c.us"}}}}
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status


antes = len(json.load(open(CACHE))) if __import__("os").path.exists(CACHE) else 0
print("entradas de cache antes:", antes)
for i in (1, 2):
    print("  envio %d -> HTTP %s" % (i, inyectar(i)))
    time.sleep(6)
print()
print("=== las dos clasificaciones del MISMO contenido ===")
import sqlite3
c = sqlite3.connect("/opt/waha/bus.db")
for r in c.execute("SELECT ts,artifacts FROM events WHERE text = ? ORDER BY id DESC LIMIT 2", (TEXTO,)):
    a = json.loads(r[1])[0]
    print("  %s -> %s | cache=%s" % (r[0], a.get("cat"), a.get("cache")))
print()
print("=== cache ===")
d = json.load(open(CACHE))
print("  entradas ahora:", len(d))
for k, v in list(d.items())[-2:]:
    print("   %s... -> %s" % (k[:16], v.get("cat")))
