#!/usr/bin/env python3
"""Aplica qwen/qwen3.7-flash (env) al filtro y al agente del VPS. Respaldos + verificacion."""
import datetime
import os
import shutil
import subprocess

FLASH = "qwen/qwen3.7-flash"
RESPALDOS = ["deepseek/deepseek-v4-flash-0731", "nvidia/nemotron-3-ultra-550b-a55b:free"]
STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

print("=== 1) FILTRO: FILTRO_MODEL -> %s ===" % FLASH)
ENVF = "/opt/waha/filtro.env"
shutil.copy2(ENVF, ENVF + ".bak-flash-" + STAMP)
lineas = open(ENVF, encoding="utf-8").read().splitlines()
nuevas, cambiado = [], False
for l in lineas:
    if l.startswith("FILTRO_MODEL="):
        nuevas.append("FILTRO_MODEL=" + FLASH)
        cambiado = True
    else:
        nuevas.append(l)
if not cambiado:
    nuevas.append("FILTRO_MODEL=" + FLASH)
open(ENVF, "w", encoding="utf-8").write("\n".join(nuevas) + "\n")
os.chmod(ENVF, 0o600)
print("  cambiado=%s" % cambiado)
for l in nuevas:
    if l.startswith(("FILTRO_MODEL=", "VISION_MODEL=", "STT_MODEL=")):
        print("   " + l)
print("  (VISION sigue en gemini-2.5-flash: necesita ver imagenes; qwen3.7-flash no es multimodal)")

print()
print("=== 2) AGENTE: model.default -> %s (+2 respaldos) ===" % FLASH)
CFG = "/root/.hermes/config.yaml"
import re
import yaml
txt = open(CFG, encoding="utf-8").read()
shutil.copy2(CFG, CFG + ".bak-flash-" + STAMP)
txt = re.sub(r"(?m)^  default: .*$", "  default: " + FLASH, txt, count=1)
fb = ("fallback_providers:\n" +
      "".join("  - provider: openrouter\n    model: %s\n" % m for m in RESPALDOS))
txt = re.sub(r"(?m)^fallback_providers:[\s\S]*?(?=\n\S|\Z)", fb.rstrip("\n"), txt, count=1)
open(CFG, "w", encoding="utf-8").write(txt)
c = yaml.safe_load(open(CFG, encoding="utf-8"))
print("  modelo: %s" % c["model"]["default"])
print("  respaldos: %s" % [x["model"] for x in c["fallback_providers"]])

print()
print("=== 3) REINICIO DEL FILTRO ===")
print(subprocess.run(["bash", "-lc", "systemctl restart seawolf-filtro.service && sleep 2 && systemctl is-active seawolf-filtro.service && ss -ltn | grep 3011"],
                     capture_output=True, text=True).stdout)

print("=== 4) PRUEBA REAL: clasificacion con el modelo nuevo ===")
import json
import urllib.request
payload = {"event": "message", "session": "seawolf", "payload": {
    "id": "flash_test_1", "from": "573001119999@c.us", "fromMe": False,
    "body": "Se rompio el tubo del bano del apto 501 y esta inundando el pasillo, vengan ya por favor",
    "hasMedia": False, "media": None, "_data": {"Info": {"Chat": "573001119999@c.us"}}}}
req = urllib.request.Request("http://172.16.0.1:3011/", data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        print("  filtro respondio HTTP %s" % r.status)
except Exception as e:
    print("  ERROR: %s" % e)
print("  ultima linea de filtro.log:")
print("   " + subprocess.run(["bash", "-lc", "tail -1 /opt/waha/filtro.log"], capture_output=True, text=True).stdout.strip()[:300])
print()
print("  (esa prueba enviara una alerta de prueba al WhatsApp del Monarca: es la prueba real)")
