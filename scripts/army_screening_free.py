#!/usr/bin/env python3
"""SCREENING de los :free con tools: contenido NO vacio + tool call + latencia.
Se ejecuta en el VPS (usa su OPENROUTER_API_KEY)."""
import json
import os
import time
import urllib.request

KEY = os.environ["OPENROUTER_API_KEY"]

CANDIDATOS = [
    "thinkingmachines/inkling:free",
    "thinkingmachines/inkling-small:free",
    "dots-studio/dots-3-note-preview:free",
    "apodex/apodex-1.1-mini:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "inclusionai/ling-3.0-flash-sante:free",
    "poolside/laguna-s-2.1:free",
    "cohere/north-mini-code:free",
]

TOOLS = [{"type": "function", "function": {
    "name": "reportar", "description": "Reporta el resultado al comandante",
    "parameters": {"type": "object",
                   "properties": {"sombra": {"type": "string"}, "estado": {"type": "string"}},
                   "required": ["sombra", "estado"]}}}]

PROMPT = ("Eres Igris, especialista en copywriting de Seawolf Studio. "
          "Usa la herramienta 'reportar' para confirmar tu estado operativo y ademas "
          "escribe en una linea un titular de venta para un agente de IA. Español.")


def call(model):
    body = {"model": model, "max_tokens": 300, "temperature": 0.3,
            "messages": [{"role": "user", "content": PROMPT}], "tools": TOOLS}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
        dt = time.time() - t0
        m = d["choices"][0]["message"]
        return dt, m, d.get("usage", {})
    except Exception as e:
        return time.time() - t0, {"ERROR": str(e)[:160]}, {}


print("%-46s %-7s %-9s %-8s %s" % ("MODELO", "lat", "contenido", "tool_call", "nota"))
print("-" * 100)
resultados = {}
for mid in CANDIDATOS:
    dt, m, u = call(mid)
    content = (m.get("content") or "").strip()
    tc = m.get("tool_calls")
    err = m.get("ERROR", "")
    nota = ""
    if err:
        nota = err
    elif not content and not tc:
        nota = "VACIO (inutil)"
    elif content and len(content) < 8:
        nota = "contenido sospechosamente corto"
    if content and content.lower().startswith(("here's", "aquí", "1.", "**")):
        nota = (nota + " fuga-de-razonamiento").strip()
    print("%-46s %-7.1f %-9s %-8s %s" % (
        mid, dt, "si" if content else "NO", "si" if tc else "no", nota[:44]))
    resultados[mid] = {"lat": round(dt, 1), "content": bool(content), "tools": bool(tc),
                       "razona_fuga": "fuga" in nota, "vacio": "VACIO" in nota,
                       "costo": u.get("cost", 0)}

print()
print("=== APTOS (contenido + tool call, sin vacio) ===")
for k, v in resultados.items():
    if v["content"] and v["tools"] and not v["vacio"]:
        print("  %-46s %.1fs%s" % (k, v["lat"], "  (fuga de razonamiento)" if v["razona_fuga"] else ""))
json.dump(resultados, open("/opt/waha/screening_free.json", "w"), indent=2)
print("\n  guardado en /opt/waha/screening_free.json")
