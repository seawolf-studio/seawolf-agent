#!/usr/bin/env python3
"""Lista TODOS los modelos :free que soportan tools (sirven para agentes).
Marca tambien json/ctx/precio para elegir sustitutos de los 4 ids caidos."""
import json
import urllib.request

with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=60) as r:
    data = json.load(r)["data"]

free_tools = []
for m in data:
    mid = m["id"]
    if not mid.endswith(":free"):
        continue
    sp = m.get("supported_parameters", []) or []
    if "tools" not in sp:
        continue
    p = m.get("pricing", {})
    free_tools.append((mid, m.get("context_length"),
                       any(x in sp for x in ("response_format", "structured_outputs")),
                       float(p.get("prompt") or 0), float(p.get("completion") or 0)))

free_tools.sort(key=lambda x: -(x[1] or 0))
print("MODELOS :free CON tools=True  (total %d)\n" % len(free_tools))
print("%-52s %-9s %-6s %s" % ("ID", "contexto", "json", "precio real"))
for mid, ctx, js, pin, pout in free_tools:
    gratis = "0" if (pin == 0 and pout == 0) else "$%.4f/%.4f" % (pin, pout)
    print("%-52s %-9s %-6s %s" % (mid, ctx, "si" if js else "no", gratis))

print()
print("Familias utiles para reemplazos (variantes :free presentes):")
for fam in ("glm", "minimax", "qwen", "gemma", "nemotron", "deepseek", "llama", "mistral", "kimi", "seed"):
    hits = sorted(m for m, *_ in free_tools if fam in m.lower())
    if hits:
        print("  %-10s %s" % (fam, hits))
