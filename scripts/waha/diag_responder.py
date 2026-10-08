#!/usr/bin/env python3
"""Diagnostico: (a) por que el borrador sale vacio; (b) procesos duplicados."""
import json
import os
import subprocess
import urllib.request

print("=== (a) llamada CRUDA al modelo de redaccion ===")
key = os.environ.get("OPENROUTER_API_KEY", "")
print("  OPENROUTER_API_KEY presente:", bool(key))
body = {"model": "qwen/qwen3.7-flash", "temperature": 0.4, "max_tokens": 220,
        "messages": [
            {"role": "system", "content": "Eres el asistente operativo de Key. Redactas LA RESPUESTA QUE Key daria a un residente. Breve, humano, espanol. Devuelve SOLO el texto, sin comillas."},
            {"role": "user", "content": "Nivel del filtro: naranja\nDe: un residente\nMensaje recibido: El ascensor del bloque 3 lleva tres dias sin funcionar y hay adultos mayores en el 5to piso\n\nRedacta la respuesta."}]}
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                            data=json.dumps(body).encode(),
                            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=90) as r:
    d = json.load(r)
ch = d["choices"][0]
msg = ch["message"]
print("  finish_reason:", ch.get("finish_reason"))
print("  keys del mensaje:", list(msg.keys()))
print("  content (%d chars): %r" % (len(msg.get("content") or ""), (msg.get("content") or "")[:160]))
print("  reasoning (%d chars): %r" % (len(msg.get("reasoning") or ""), (msg.get("reasoning") or "")[:160]))
print("  usage:", d.get("usage"))
print("  --- respuesta completa (primeros 700 chars) ---")
print(json.dumps(d, ensure_ascii=False)[:700])

print()
print("=== (b) procesos del responder ===")
out = subprocess.run(["bash", "-lc", "pgrep -af responder.py"], capture_output=True, text=True).stdout
print(out or "(ninguno)")
out = subprocess.run(["bash", "-lc", "systemctl status seawolf-responder.service --no-pager | head -12"],
                     capture_output=True, text=True).stdout
print(out)
