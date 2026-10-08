#!/usr/bin/env python3
"""Inicializa el estado del responder desde el evento ACTUAL del bus
(para que no reprocese el historico de 104 eventos al arrancar)."""
import json
import sqlite3

c = sqlite3.connect("/opt/waha/bus.db")
mx = c.execute("SELECT MAX(id) FROM events").fetchone()[0] or 0
mo = c.execute("SELECT MAX(id) FROM events WHERE kind = ?", ("order",)).fetchone()[0] or 0
c.close()
json.dump({"ultimo_orden": mo, "ultimo_msg": mx},
          open("/opt/waha/responder_estado.json", "w"))
print("estado inicial -> ultimo_msg=%s ultimo_orden=%s (no reprocesa historico)" % (mx, mo))
print("pendientes.json se crea al primer propuesto")
