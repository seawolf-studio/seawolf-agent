#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LA MESA — el cuarto de guerra de Seawolf Studio.
Mesa donde el Monarca, Bellion y las sombras conversan.

  python mesa.py                 -> renderiza mesa.html desde mesa.json
  python mesa.py --habla jima "texto"   -> agrega un mensaje de una sombra
  python mesa.py --habla monarca "texto"
  python mesa.py --habla bellion "texto"

Salida: C:\\Users\\Admin\\intel\\mesa\\mesa.html
"""
import json, os, sys, time, datetime

BASE = r"C:\Users\Admin\intel\mesa"
LOG = os.path.join(BASE, "mesa.json")
OUT = os.path.join(BASE, "mesa.html")

ROSTER = {
  "bellion": {"n":"Bellion",   "r":"Gran Comandante",        "i":"🐺", "c":"#4CE8E7"},
  "monarca": {"n":"Monarca",   "r":"Key · Seawolf Studio",   "i":"👑", "c":"#FFD166"},
  "igris":   {"n":"Igris",     "r":"Copywriting",            "i":"✍️", "c":"#A78BFA"},
  "tank":    {"n":"Tank",      "r":"Ventas / WhatsApp",      "i":"🤝", "c":"#5BE58A"},
  "greed":   {"n":"Greed",     "r":"Ads / Tráfico",          "i":"🎯", "c":"#FF9F6B"},
  "iron":    {"n":"Iron",      "r":"Email / Secuencias",     "i":"📧", "c":"#67B7FF"},
  "tusk":    {"n":"Tusk",      "r":"SEO / Orgánico",         "i":"🔍", "c":"#FFC24B"},
  "kamish":  {"n":"Kamish",    "r":"Social / Distribución",  "i":"📣", "c":"#FF7BC1"},
  "kaisel":  {"n":"Kaisel",    "r":"Web Dev",                "i":"🌐", "c":"#7CE8C0"},
  "titan":   {"n":"Titan",     "r":"UX / UI",                "i":"🎨", "c":"#B7A6FF"},
  "jima":    {"n":"Jima",      "r":"Automatización",         "i":"⚙️", "c":"#8FD6FF"},
  "beru":    {"n":"Beru",      "r":"Auditoría",              "i":"🛡️", "c":"#FF8A8A"},
}

def hora():
    return datetime.datetime.now().strftime("%H:%M")

def cargar():
    if os.path.exists(LOG):
        return json.load(open(LOG, encoding="utf-8"))
    return {"mensajes": []}

def guardar(d):
    json.dump(d, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def habla(de, texto):
    d = cargar()
    d["mensajes"].append({"de": de, "texto": texto, "hora": hora()})
    guardar(d)
    print(f"+ [{de}] {texto[:70]}")

def render():
    d = cargar()
    msjs = []
    for m in d["mensajes"]:
        p = ROSTER.get(m["de"], {"n":m["de"],"r":"","i":"•","c":"#7FA3A3"})
        msjs.append({**m, **p})
    data = {
        "mensajes": msjs,
        "roster": [{"id":k, **v} for k,v in ROSTER.items() if k not in ("bellion","monarca")],
        "generado": hora(),
    }
    tpl = open(os.path.join(BASE, "plantilla.html"), encoding="utf-8").read()
    open(OUT, "w", encoding="utf-8").write(tpl.replace("/*__MESA__*/", json.dumps(data, ensure_ascii=False)))
    print(f"Mesa -> {OUT}  ({len(msjs)} mensajes)")

def main():
    a = sys.argv[1:]
    if "--habla" in a:
        i = a.index("--habla")
        habla(a[i+1], " ".join(a[i+2:]) or "(sin texto)")
    render()

if __name__ == "__main__":
    main()
