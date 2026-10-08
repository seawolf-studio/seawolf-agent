#!/usr/bin/env python3
"""Elige el flash mas ECONOMICO para el uso real (entrada vs salida pesan distinto).
Perfiles: turno conversacional (1500 in / 250 out) y clasificacion de filtro (400 in / 80 out)."""
import json
import urllib.request

with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=60) as r:
    cat = {m["id"]: m for m in json.load(r)["data"]}

CAND = [
    "deepseek/deepseek-v4-flash-0731",
    "deepseek/deepseek-v4-flash",
    "deepseek/deepseek-v4-flash-0731",
    "deepseek/deepseek-v4-flash-latest",
    "qwen/qwen3.7-flash",
    "qwen/qwen3.6-flash",
    "qwen/qwen3-30b-a3b-instruct-2507",
    "qwen/qwen3.5-plus-02-15",
    "bytedance-seed/seed-1.6-flash",
    "google/gemini-2.5-flash",
    "z-ai/glm-5.3-flash",
]


def precios(mid):
    m = cat.get(mid)
    if not m:
        return None
    p = m.get("pricing", {})
    sp = m.get("supported_parameters", []) or []
    return (float(p.get("prompt") or 0) * 1e6, float(p.get("completion") or 0) * 1e6,
            m.get("context_length"), "tools" in sp)


CHAT_IN, CHAT_OUT = 1500, 250     # turno de conversacion
FILT_IN, FILT_OUT = 400, 80       # clasificacion de un mensaje

filas = []
for mid in sorted(set(CAND)):
    pr = precios(mid)
    if not pr:
        print("  (no existe) %s" % mid)
        continue
    pin, pout, ctx, tools = pr
    c_chat = (CHAT_IN * pin + CHAT_OUT * pout) / 1e6
    c_filt = (FILT_IN * pin + FILT_OUT * pout) / 1e6
    filas.append((c_chat, mid, pin, pout, ctx, tools, c_filt))

filas.sort()
print("%-38s %-9s %-9s %-12s %-12s %-6s %s" % ("MODELO", "$in/1M", "$out/1M", "USD/turno", "USD/filtro", "tools", "ctx"))
print("-" * 104)
for c_chat, mid, pin, pout, ctx, tools, c_filt in filas:
    print("%-38s %-9.3f %-9.3f $%-11.6f $%-11.7f %-6s %s" % (mid, pin, pout, c_chat, c_filt, tools, ctx))

print()
print("=== ESCALADO (1000 turnos de conversacion + 1000 clasificaciones) ===")
for c_chat, mid, *_ , c_filt in filas[:6]:
    total = c_chat * 1000 + c_filt * 1000
    print("  %-38s $%.2f al mes" % (mid, total * 30))

best = filas[0]
print()
print("GANADOR por costo real: %s  (%.3f in / %.3f out por 1M)" % (best[1], best[2], best[3]))
