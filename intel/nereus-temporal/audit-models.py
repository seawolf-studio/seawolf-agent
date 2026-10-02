#!/usr/bin/env python3
import json, urllib.request
env = open("/root/.hermes/.env", encoding="utf-8", errors="replace").read()
KEY = ""
for line in env.splitlines():
    if line.startswith("OPENROUTER_API_KEY="):
        KEY = line.split("=", 1)[1].strip().strip('"')
req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"Authorization": "Bearer " + KEY, "User-Agent": "seawolf"})
models = {m["id"]: m for m in json.load(urllib.request.urlopen(req, timeout=30))["data"]}
cands = [
    "deepseek/deepseek-v4-flash",
    "deepseek/deepseek-v4.1-flash",
    "deepseek/deepseek-v4.1-flash:batch",
    "qwen/qwen3.8-27b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "ibm-granite/granite-4.0-h-micro",
]
for c in cands:
    m = models.get(c)
    if not m:
        print(f"{c:52} (no encontrado)")
        continue
    p = m.get("supported_parameters") or []
    pr = m.get("pricing", {})
    print(f'{c:52} tools={"tools" in p} struct={"structured_outputs" in p} in={float(pr.get("prompt",0))*1e6:.4f} out={float(pr.get("completion",0))*1e6:.4f}')
