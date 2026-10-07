#!/usr/bin/env python3
"""REARME DE CONFIGS — Seawolf Shadow Army.
Por sombra: modelo primario + cadena de respaldo (todo OpenRouter), fuera OmniRoute,
fuera Telegram. Respaldos por archivo. Nunca imprime valores de secretos.
"""
import os
import shutil
import time

import yaml

BASE = r"C:\Users\Admin\AppData\Local\hermes\profiles"
STAMP = time.strftime("%Y%m%d-%H%M%S")
OR = "https://openrouter.ai/api/v1"

# Cadena por sombra: (primario, respaldo1, respaldo2) — todos verificados en el catalogo vivo
# (tools=True + json donde aplica). Primario = modelo barato y CONFIABLE (la capa :free
# resulto no confiable: 429/403/vacio en el screening). El gratis entra solo donde se verifico apto.
CADENAS = {
    "igris":  ("deepseek/deepseek-v4-flash-0731", "qwen/qwen3.7-flash", "minimax/minimax-m3"),
    "tank":   ("qwen/qwen3.7-flash", "qwen/qwen3.5-plus-02-15", "minimax/minimax-m2.7"),
    "greed":  ("bytedance-seed/seed-1.6-flash", "z-ai/glm-5.3-flash", "google/gemma-4-31b-it"),
    "iron":   ("deepseek/deepseek-v4-flash-0731", "qwen/qwen3.7-flash", "minimax/minimax-m2.7"),
    "tusk":   ("qwen/qwen3.7-flash", "z-ai/glm-5.3-flash", "qwen/qwen3.5-plus-02-15"),
    "kamish": ("z-ai/glm-5.3-flash", "google/gemma-4-31b-it", "minimax/minimax-m2.7"),
    "kaisel": ("qwen/qwen3-coder-30b-a3b-instruct", "poolside/laguna-s-2.1:free", "z-ai/glm-5.2"),
    "titan":  ("qwen/qwen3-vl-32b-instruct", "google/gemma-4-31b-it", "minimax/minimax-m3"),
    "jima":   ("qwen/qwen3-30b-a3b-instruct-2507", "deepseek/deepseek-v4-flash-0731", "minimax/minimax-m3"),
    "beru":   ("deepseek/deepseek-v4-pro", "z-ai/glm-5.3-flash", "nvidia/nemotron-3-ultra-550b-a55b:free"),
}

TELEGRAM_HINT = ("telegram", "bot_token", "chat_id", "token")


def purga_telegram(d, ruta=""):
    """Borra cualquier clave de Telegram del dict. Devuelve las rutas borradas (solo nombres)."""
    quitadas = []
    if not isinstance(d, dict):
        return quitadas
    for k in list(d.keys()):
        p = (ruta + "." + k) if ruta else k
        kl = k.lower()
        if "telegram" in kl or kl in ("bot_token", "telegram_token", "telegram_bot_token"):
            d.pop(k)
            quitadas.append(p)
        elif isinstance(d[k], dict):
            quitadas += purga_telegram(d[k], p)
    return quitadas


print("REARME DE CONFIGS — %d sombras\n" % len(CADENAS))
print("=" * 78)
for sombra, (prim, fb1, fb2) in CADENAS.items():
    p = os.path.join(BASE, sombra, "config.yaml")
    if not os.path.exists(p):
        print("  [falta] %s" % sombra)
        continue
    shutil.copy2(p, p + ".bak-pre-army-" + STAMP)
    cfg = yaml.safe_load(open(p, encoding="utf-8")) or {}

    antes = (cfg.get("model") or {}).get("default")

    # 1) modelo directo a OpenRouter
    modelo = cfg.get("model") or {}
    modelo["default"] = prim
    modelo["provider"] = "openrouter"
    modelo["base_url"] = OR
    modelo["api_mode"] = "chat_completions"
    modelo.pop("key_env", None)
    cfg["model"] = modelo

    # 2) fuera OmniRoute (provider propio)
    omni = cfg.pop("providers", None)

    # 3) cadena de respaldo OpenRouter
    cfg["fallback_providers"] = [{"provider": "openrouter", "model": fb1},
                                 {"provider": "openrouter", "model": fb2}]

    # 4) fuera Telegram
    tg = purga_telegram(cfg)

    # 5) parametros de combate
    cfg["temperature"] = 0.3
    cfg["max_tokens"] = 8192

    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    # validacion
    nuevo = yaml.safe_load(open(p, encoding="utf-8"))
    ok = (nuevo["model"]["default"] == prim and len(nuevo["fallback_providers"]) == 2)
    print("  %-8s %-34s -> %-34s %s" % (sombra, str(antes)[:33], prim[:33], "OK" if ok else "FALLO"))
    print("           respaldos: %s , %s" % (fb1, fb2))
    print("           telegram eliminado: %s" % (", ".join(tg) if tg else "(nada)"))
    if omni:
        print("           omnicroute eliminado: providers[%s]" % ", ".join(omni.keys()))

print()
print("=== VALIDACION FINAL ===")
for sombra in CADENAS:
    p = os.path.join(BASE, sombra, "config.yaml")
    c = yaml.safe_load(open(p, encoding="utf-8"))
    tg = [k for k in yaml.safe_dump(c).lower().split() if "telegram" in k]
    print("  %-8s modelo=%-33s respaldos=%d telegram=%s volcado_ok=%s"
          % (sombra, c["model"]["default"], len(c.get("fallback_providers", [])),
             "NO" if not tg else "SI", bool(c)))
