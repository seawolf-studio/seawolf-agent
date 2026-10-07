#!/usr/bin/env python3
"""Aplica la propuesta de modelo del Monarca al agente:
   primario = nemotron ultra (gratis) | respaldo = deepseek v4.1 flash.
Esquema segun docs: model.default + fallback_providers[{provider,model}]."""
import subprocess
import yaml

CFG = "/root/.hermes/config.yaml"
PRIMARIO = "nvidia/nemotron-3-ultra-550b-a55b:free"
RESPALDO = "deepseek/deepseek-v4.1-flash"

txt = open(CFG, encoding="utf-8").read()
open(CFG + ".bak-pre-modelo", "w", encoding="utf-8").write(txt)

antes = yaml.safe_load(txt)
print("modelo ANTES:", antes.get("model", {}).get("default"), "| fallbacks:", antes.get("fallback_providers"))

# 1) modelo primario
import re
txt = re.sub(r"(?m)^  default: .*$", "  default: " + PRIMARIO, txt, count=1)

# 2) cadena de respaldo
nuevo_fb = ("fallback_providers:\n"
            "  - provider: openrouter\n"
            "    model: " + RESPALDO + "\n")
if re.search(r"(?m)^fallback_providers:.*$", txt):
    txt = re.sub(r"(?m)^fallback_providers:.*$", nuevo_fb.rstrip("\n"), txt, count=1)
else:
    txt += "\n" + nuevo_fb

open(CFG, "w", encoding="utf-8").write(txt)

despues = yaml.safe_load(open(CFG, encoding="utf-8").read())
print("modelo DESPUES:", despues.get("model", {}).get("default"))
print("fallbacks DESPUES:", despues.get("fallback_providers"))
assert despues["model"]["default"] == PRIMARIO
assert despues["fallback_providers"][0]["model"] == RESPALDO
print("YAML valido y aplicado")

print()
print("=== hermes fallback list ===")
print(subprocess.run(["bash", "-lc", "hermes fallback list 2>&1 | head -8"],
                     capture_output=True, text=True).stdout)

print("=== prueba rapida de arranque con el modelo nuevo ===")
r = subprocess.run(["bash", "-lc",
                    "cd /opt/waha && timeout 120 hermes -z 'responde unicamente: LISTO' --yolo 2>&1 | tail -6"],
                   capture_output=True, text=True)
print(r.stdout[-600:])
