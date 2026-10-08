#!/usr/bin/env python3
"""Verifica C1/C2 tras el fix: (a) latencia/costo de la clasificacion del filtro
con razonamiento activado vs desactivado; (b) el borrador ya devuelve texto real."""
import json
import os
import time
import urllib.request

KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("FILTRO_MODEL", "qwen/qwen3.7-flash")
SYS = ("Clasifica el mensaje de WhatsApp de un conjunto residencial. Devuelve SOLO JSON valido con las "
       "claves cat, motivo, accion; cat = rojo|naranja|amarillo|verde.")
MSG = ("Buenas tardes, el ascensor del bloque 3 lleva tres dias sin funcionar y hay adultos mayores "
       "en el 5to piso")


def call(extra, max_tokens=None):
    body = {"model": MODEL, "temperature": 0,
            "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": MSG}]}
    body.update(extra)
    if max_tokens:
        body["max_tokens"] = max_tokens
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                                data=json.dumps(body).encode(),
                                headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    dt = time.time() - t0
    u = d.get("usage") or {}
    c = (d["choices"][0]["message"].get("content") or "").strip()
    return dt, c, u


print("=== CLASIFICACION del filtro (Capa 1) ===")
for etiqueta, extra, mt in (("razonamiento ACTIVADO (actual)", {"response_format": {"type": "json_object"}}, None),
                            ("razonamiento DESACTIVADO", {"response_format": {"type": "json_object"},
                                                          "reasoning": {"enabled": False}}, None),
                            ("DESACTIVADO + max_tokens 400", {"response_format": {"type": "json_object"},
                                                              "reasoning": {"enabled": False}}, 400)):
    try:
        dt, c, u = call(extra, mt)
        ok = "JSON valido" if c.startswith("{") else "NO-JSON"
        print("  %-32s %5.1fs | %-10s | tok_in=%s tok_out=%s | cost=%.6f"
              % (etiqueta, dt, ok, u.get("prompt_tokens"), u.get("completion_tokens"), u.get("cost", 0)))
        print("     %s" % c[:110].replace("\n", " "))
    except Exception as e:
        print("  %-32s ERROR %s" % (etiqueta, str(e)[:100]))

print()
print("=== BORRADOR (Capa 2) con razonamiento desactivado ===")
import sys
sys.path.insert(0, "/opt/waha")
import responder
t0 = time.time()
txt = responder.borrador(MSG, "naranja", "un residente")
print("  latencia %.1fs | chars=%d" % (time.time() - t0, len(txt or "")))
print("  TEXTO: %s" % (txt or "(VACIO - sigue mal)"))
