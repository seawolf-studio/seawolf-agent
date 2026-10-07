#!/usr/bin/env python3
"""VERIFICACION del arsenal contra el catalogo VIVO de OpenRouter.
Comprueba: existe el id? soporta tools? precio? contexto?
Propone sustitutos reales cuando un id no existe o no sirve para agentes con herramientas."""
import difflib
import json
import urllib.request

URL = "https://openrouter.ai/api/v1/models"
print("Descargando catalogo vivo de OpenRouter...")
with urllib.request.urlopen(URL, timeout=60) as r:
    data = json.load(r)["data"]
cat = {m["id"]: m for m in data}
print("Modelos en catalogo: %d\n" % len(cat))


def info(mid):
    m = cat.get(mid)
    if not m:
        return None
    p = m.get("pricing", {})
    sp = m.get("supported_parameters", []) or []
    return {
        "tools": "tools" in sp,
        "json": any(x in sp for x in ("response_format", "structured_outputs")),
        "ctx": m.get("context_length"),
        "pin": float(p.get("prompt") or 0) * 1e6,
        "pout": float(p.get("completion") or 0) * 1e6,
    }


# cadenas propuestas por sombra: (gratis, barato, pago)
CADENAS = {
    "igris":  ["z-ai/glm-5.2:free", "deepseek/deepseek-v4-flash-0731", "minimax/minimax-m3"],
    "tank":   ["google/gemma-4-31b-it:free", "qwen/qwen3.7-flash", "minimax/minimax-m2.7"],
    "greed":  ["minimax/minimax-m3:free", "bytedance-seed/seed-1.6-flash", "z-ai/glm-5.2"],
    "iron":   ["google/gemma-4-26b-a4b-it:free", "deepseek/deepseek-v4-flash-0731", "minimax/minimax-m2.7"],
    "tusk":   ["z-ai/glm-5.2:free", "qwen/qwen3.7-flash", "qwen/qwen3.5-plus-02-15"],
    "kamish": ["minimax/minimax-m3:free", "z-ai/glm-5.3-flash", "google/gemma-4-31b-it"],
    "kaisel": ["poolside/laguna-s-2.1:free", "qwen/qwen3-coder-30b-a3b-instruct", "z-ai/glm-5.2"],
    "titan":  ["google/gemma-4-31b-it:free", "qwen/qwen3-vl-32b-instruct", "minimax/minimax-m3"],
    "jima":   ["nvidia/nemotron-3.5-lightning:free", "qwen/qwen3-30b-a3b-instruct-2507", "minimax/minimax-m3"],
    "beru":   ["nvidia/nemotron-3-super-120b-a12b:free", "deepseek/deepseek-v4-pro", "z-ai/glm-5.2"],
}

os_ = {  # modelos SIN prefijo proveedor que hay que resolver
    "deepseek/deepseek-v4-flash-0731", "z-ai/glm-5.2:free", "z-ai/glm-5.3-flash",
}


def candidatos(frag, n=6):
    pasa = [m for m in cat if frag in m]
    return sorted(pasa)[:n]


faltan = []
for sombra, cadena in CADENAS.items():
    print("=" * 74)
    print("SOMBRA: %s" % sombra.upper())
    for rol, mid in zip(("GRATIS", "+BARATO", "PAGO"), cadena):
        i = info(mid)
        if i:
            print("  %-8s OK   %-44s tools=%-5s json=%-5s ctx=%-8s $%.3f/$%.3f por 1M"
                  % (rol, mid, i["tools"], i["json"], i["ctx"], i["pin"], i["pout"]))
        else:
            print("  %-8s FALTA %-43s" % (rol, mid))
            faltan.append((sombra, rol, mid))

print()
print("=" * 74)
print("IDs QUE NO EXISTEN (%d). Sugerencias por familia:" % len(faltan))
for sombra, rol, mid in faltan:
    clave = mid.split("/")[-1].replace(":free", "").split("-")[0]
    # buscar por familia/raiz
    fam = clave[:6]
    sug = [m for m in cat if fam.lower() in m.lower()]
    sug = sorted(sug)[:6]
    print("  %-8s %-7s %-40s -> %s" % (sombra, rol, mid, sug if sug else "(sin sugerencia)"))
