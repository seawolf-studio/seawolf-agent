#!/usr/bin/env python3
"""Prueba de GENERALIDAD del bus: cualquier situacion, no solo repos.
Usa una base temporal para no ensuciar el bus real."""
import os

os.environ["SEAWOLF_BUS_DB"] = "/tmp/bus_general.db"
if os.path.exists("/tmp/bus_general.db"):
    os.remove("/tmp/bus_general.db")

import bus  # noqa: E402  (tras fijar la DB)

bus.init()

# --- eventos de naturaleza MUY distinta, por canales distintos ---
bus.emit(channel="whatsapp", direction="in", kind="message",
         text="Buenas tardes, el ascensor del bloque 3 lleva tres dias sin funcionar y hay adultos mayores en el 5to piso",
         peer="573014445566@c.us", actor="573014445566@c.us", layer=1,
         artifacts=[{"type": "classification", "cat": "naranja",
                     "accion": "avisar a mantenimiento y poner aviso en el ascensor"}])
bus.emit(channel="whatsapp", direction="out", kind="alert",
         text="NARANJA: ascensor bloque 3 fuera de servicio hace 3 dias. Accion: llamar al tecnico",
         peer="self:L1", actor="seawolf-agent", layer=1)
bus.emit(channel="email", direction="out", kind="message",
         text="Circular a propietarios: cuota de administracion de octubre con 5% de descuento por pronto pago",
         peer="propietarios@conjunto.co", actor="seawolf-agent", layer=2,
         approved_by="monarca")
bus.emit(channel="webui", direction="in", kind="order",
         text="Pidele a Don Carlos el informe de seguridad del fin de semana y mandamelo resumido",
         peer="monarca", actor="monarca", layer=2)
bus.emit(channel="whatsapp", direction="out", kind="action",
         text="Se solicito a Don Carlos el informe de seguridad del fin de semana",
         peer="573017778899@c.us", actor="seawolf-agent", layer=2, approved_by="monarca")
bus.emit(channel="whatsapp", direction="in", kind="message",
         text="Senor administrador, mi apartamento 302 tiene una humedad en el techo desde la semana pasada",
         peer="573019990011@c.us", actor="573019990011@c.us", layer=1,
         artifacts=[{"type": "classification", "cat": "amarillo", "accion": "programar revision de humedad"}])

TESTS = [
    "que paso con el ascensor del bloque 3",
    "como va la cuota de administracion de octubre",
    "que le pedi a Don Carlos sobre seguridad",
    "el apartamento 302 con humedad en el techo",
    "que acciones hiciste que yo aprobe",
]
for t in TESTS:
    print("### " + t)
    rows = bus.search(t, limit=2)
    if not rows:
        print("   (sin resultados)")
    for r in rows:
        art = r["artifacts"]
        print("   -> [%s|%s|%s] %s" % (r["channel"], r["direction"], r["kind"], (r["text"] or "")[:95]))
    print()

print("=== stats ===")
bus.stats()
