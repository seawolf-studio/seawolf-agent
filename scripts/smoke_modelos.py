#!/usr/bin/env python3
"""Smoke test de modelos del Seawolf Agent (nemotron vs deepseek) — ejecutar en el VPS."""
import os, json, time, urllib.request

KEY = os.environ["OPENROUTER_API_KEY"]


def call(model, messages, tools=None, json_mode=False, max_tokens=400):
    body = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.2}
    if tools:
        body["tools"] = tools
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.load(r)
        return time.time() - t0, d["choices"][0]["message"], d.get("usage")
    except Exception as e:
        return time.time() - t0, {"ERROR": str(e)[:250]}, None


MSG = ("Senor admin, buenas tardes, se rompio el tubo del bano del apto 302 "
       "y esta inundando el pasillo, venga ya por favor")

PROMPT = ('Clasifica el mensaje de WhatsApp. Devuelve SOLO JSON: '
          '{"nivel":"rojo|naranja|amarillo|verde","accion":"...","resumen":"..."}\n'
          'rojo = seguridad/atencion inmediata. naranja = mitigable ahora, arreglo despues.')

print("=== CLASIFICACION (json_mode) ===")
for model in ["nvidia/nemotron-3-ultra-550b-a55b:free",
              "nvidia/nemotron-3-super-120b-a12b:free",
              "nvidia/nemotron-3.5-lightning:free",
              "deepseek/deepseek-v4.1-flash"]:
    dt, msg, usage = call(model, [{"role": "user", "content": PROMPT + "\n\nMENSAJE: " + MSG}], json_mode=True)
    content = msg.get("content") or msg.get("ERROR", "")
    ok = False
    try:
        json.loads(content)
        ok = True
    except Exception:
        pass
    print("--- " + model)
    print("    latencia: %.1fs | JSON valido: %s" % (dt, ok))
    print("    content: " + str(content)[:200].replace("\n", " "))
    if usage:
        print("    tokens: %s" % usage)
    print()

print("=== TOOL CALLING ===")
TOOLS = [{"type": "function", "function": {
    "name": "enviar_alerta", "description": "Envia alerta al dueno",
    "parameters": {"type": "object", "properties": {
        "nivel": {"type": "string"}, "texto": {"type": "string"}}, "required": ["nivel", "texto"]}}}]
for model in ["nvidia/nemotron-3-ultra-550b-a55b:free", "deepseek/deepseek-v4.1-flash"]:
    dt, msg, usage = call(model, [{"role": "user",
        "content": "Hay una inundacion en el 302, alerta al dueno usando tu herramienta."}], tools=TOOLS)
    tc = msg.get("tool_calls")
    print("--- TOOL CALL " + model)
    print("    latencia: %.1fs" % dt)
    print("    tool_calls: " + (json.dumps(tc)[:250] if tc else "NINGUNO"))
    if msg.get("ERROR"):
        print("    error: " + msg["ERROR"][:150])
    print()
