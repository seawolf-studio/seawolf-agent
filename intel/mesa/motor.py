#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MOTOR DE LA MESA — reemplazo del auto-despacho del Kanban.
Bucle: revisa misiones EN COLA y las ejecuta por la via DIRECTA.
  python motor.py [--intervalo 20] [--una-vez]
"""
import sys, time, subprocess, os

MESA = r"C:\Users\Admin\intel\mesa\mesa.py"
INT = 20
if "--intervalo" in sys.argv: INT = int(sys.argv[sys.argv.index("--intervalo")+1])
UNA = "--una-vez" in sys.argv

def hay_cola():
    import json
    try:
        d = json.load(open(r"C:\Users\Admin\intel\mesa\mesa.json", encoding="utf-8"))
        return [m for m in d.get("misiones", []) if m.get("estado") == "en cola"]
    except Exception:
        return []

def corre():
    r = subprocess.run([sys.executable, MESA, "--corre"], capture_output=True, text=True,
                       timeout=1800, encoding="utf-8", errors="ignore")
    print((r.stdout or "").strip()[-600:], flush=True)

print(f"🐺 MOTOR DE LA MESA encendido (intervalo {INT}s)", flush=True)
while True:
    cola = hay_cola()
    if cola:
        print(f"[motor] {len(cola)} en cola -> ejecutando", flush=True)
        corre()
    if UNA:
        break
    time.sleep(INT)
print("motor detenido", flush=True)
