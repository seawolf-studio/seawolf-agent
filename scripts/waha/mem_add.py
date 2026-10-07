#!/usr/bin/env python3
"""Agrega el hecho del bus de eventos a la memoria permanente del agente."""
P = "/root/.hermes/memories/MEMORY.md"

ENTRY = (
    "Memoria de canales (BUS DE EVENTOS): todo lo que entra o sale por WhatsApp, correo o WebUI "
    "queda registrado en /opt/waha/bus.db. Ante CUALQUIER pregunta sobre algo pasado "
    "(un repo que envie anoche, que paso con un mensaje, que pedi, que respondi, que aprobo el dueno), "
    "consulta SIEMPRE antes de responder: python3 /opt/waha/bus.py search \"<el tema>\" -n 5. "
    "Jamas digas que no tienes acceso a WhatsApp: si esta en el bus, lo sabes. "
    "Detalle en la skill seawolf-memoria-bus."
)

txt = open(P, encoding="utf-8").read().rstrip()
if "bus.py" in txt:
    print("ya estaba registrado")
else:
    open(P, "w", encoding="utf-8").write(txt + "\n§\n" + ENTRY + "\n")
    print("hecho agregado a la memoria del agente")
print("--- MEMORY.md ahora (ultima entrada) ---")
print(open(P, encoding="utf-8").read().strip().split("§")[-1].strip()[:400])
