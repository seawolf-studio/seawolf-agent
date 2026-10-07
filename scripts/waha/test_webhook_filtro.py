#!/usr/bin/env python3
"""Prueba del camino ENTRANTE: simula un webhook de WAHA contra el filtro real.
Usa un mensaje VERDE para no enviar alerta al WhatsApp del dueno."""
import json
import urllib.request

URL = "http://172.16.0.1:3011/"

payload = {
    "event": "message",
    "session": "seawolf",
    "payload": {
        "id": "false_test_1",
        "from": "573001112233@c.us",
        "fromMe": False,
        "body": "Buenas tardes, muchas gracias por la informacion del mantenimiento",
        "hasMedia": False,
        "media": None,
        "_data": {"Info": {"Chat": "573001112233@c.us"}},
    },
}

req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        print("filtro respondio HTTP", r.status)
except Exception as e:
    print("ERROR al llamar al filtro:", e)
