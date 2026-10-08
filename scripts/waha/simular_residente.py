#!/usr/bin/env python3
"""Simula un mensaje de un TERCERO (residente/guarda) entrando a la linea 2.
Uso: python3 simular_residente.py "<texto>" [remitente]"""
import json
import sys
import urllib.request

texto = sys.argv[1] if len(sys.argv) > 1 else "El ascensor del bloque 3 lleva tres dias sin funcionar"
remitente = sys.argv[2] if len(sys.argv) > 2 else "573001112233@c.us"

payload = {"event": "message", "session": "seawolf", "payload": {
    "id": "sim_%d" % __import__("time").time(), "from": remitente, "fromMe": False,
    "body": texto, "hasMedia": False, "media": None,
    "_data": {"Info": {"Chat": remitente}}}}
req = urllib.request.Request("http://172.16.0.1:3011/", data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        print("inyectado (HTTP %s): %s" % (r.status, texto[:70]))
except Exception as e:
    print("ERROR: %s" % e)
