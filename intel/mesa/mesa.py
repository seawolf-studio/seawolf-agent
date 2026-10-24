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
import json, os, sys, time, datetime, subprocess, re

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
        d = json.load(open(LOG, encoding="utf-8"))
        d.setdefault("mensajes", []); d.setdefault("susurros", [])
        return d
    return {"mensajes": [], "susurros": []}

def guardar(d):
    json.dump(d, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def habla(de, texto):
    d = cargar()
    d["mensajes"].append({"de": de, "texto": texto, "hora": hora()})
    guardar(d)
    print(f"+ [{de}] {texto[:70]}")

def susurra(de, para, texto):
    """El Monarca le habla AL OÍDO a una sombra: solo ellos dos lo ven."""
    d = cargar()
    d["susurros"].append({"de": de, "para": para, "texto": texto, "hora": hora()})
    guardar(d)
    print(f"~ [{de} -> {para}] {texto[:70]}")

def _limpiar(t):
    t = re.sub(r"hermes: .*could not be finished.*\n?", "", t)
    lineas = [l for l in t.splitlines() if l.strip() and not l.startswith("Resume this session")
              and not l.startswith("  hermes ") and not l.startswith("Title:")
              and not l.startswith("Duration:") and not l.startswith("Messages:")
              and not l.startswith("Query:") and "────" not in l and l.strip() != "☤ Hermes"]
    return "\n".join(lineas).strip()

def _parse(salida):
    ses = None
    m = re.search(r"Session:\s+(local-[0-9a-f]+)", salida)
    if m: ses = m.group(1)
    # la respuesta final vive entre el ultimo '☤ Hermes' y el cierre
    partes = salida.split("☤ Hermes")
    cuerpo = partes[-1] if len(partes) > 1 else salida
    cuerpo = cuerpo.split("Resume this session")[0]
    return ses, _limpiar(cuerpo)

def turno(mid, instruccion, sombra=None, titulo=None):
    """Avanza UNA misión un turno. Reanuda la sesión de la sombra para que RECUERDE."""
    d = cargar(); d.setdefault("misiones", [])
    mis = next((m for m in d["misiones"] if m["id"] == mid), None)
    if mis is None:
        mis = {"id": mid, "titulo": titulo or mid, "sombra": sombra or "tusk",
               "sesion": None, "turnos": [], "estado": "abierta"}
        d["misiones"].append(mis)
    cmd = ["hermes", "-p", mis["sombra"], "chat"]
    if mis.get("sesion"): cmd += ["--resume", mis["sesion"]]
    # la DIRECTIVA vigente viaja en el proximo turno -> el reencauce se cumple de verdad
    inst = instruccion
    if mis.get("directiva"):
        inst = (f"DIRECTIVA VIGENTE DEL MONARCA (obligatoria, reencauza el trabajo anterior): "
                f"{mis['directiva']}\n\n{instruccion}")
    cmd += ["-q", inst, "--oneshot"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600, encoding="utf-8", errors="ignore")
    ses, resp = _parse((r.stdout or "") + (r.stderr or ""))
    if ses: mis["sesion"] = ses
    n = len(mis["turnos"]) + 1
    mis["turnos"].append({"n": n, "quien": "monarca", "instruccion": instruccion,
                          "salida": resp, "hora": hora()})
    mis["estado"] = "esperando tu correccion"
    guardar(d)
    print(f"~ turno {n} de {mid} ({mis['sombra']}) sesion={mis.get('sesion')}")
    print(f"  -> {resp[:250]}")

def cambio(texto, antes="", despues=""):
    """INTERRUPCION COLECTIVA: el Monarca cambia el rumbo en medio del trabajo.
    Se propaga a (1) la conversacion, (2) las tareas en curso y (3) la memoria."""
    d = cargar(); d.setdefault("cambios", []); d.setdefault("misiones", [])
    c = {"id": f"c{len(d['cambios'])+1}", "texto": texto, "antes": antes, "despues": despues,
         "hora": hora(), "tareas": [], "memoria": False, "conversacion": False}
    # (2) TAREAS: toda mision viva queda marcada y su proximo turno carga la directiva
    for m in d["misiones"]:
        if m.get("estado") != "cerrada":
            m["reencauzada"] = True
            m["directiva"] = texto
            c["tareas"].append(m["id"])
    d["cambios"].append(c)
    # (1) CONVERSACION: el cambio entra a la mesa como mensaje del Monarca
    d["mensajes"].append({"de": "monarca", "texto": texto, "hora": hora(),
                          "cambio": True, "antes": antes, "despues": despues})
    c["conversacion"] = True
    # (3) MEMORIA: queda escrito para siempre (sobrevive a la sesion y a la compactacion)
    try:
        mem = os.path.join(BASE, "directivas.json")
        dm = json.load(open(mem, encoding="utf-8")) if os.path.exists(mem) else {"directivas": []}
        dm["directivas"].append({"id": c["id"], "texto": texto, "antes": antes,
                                 "despues": despues, "hora": hora()})
        json.dump(dm, open(mem, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        c["memoria"] = True
    except Exception as e:
        print("memoria:", e)
    guardar(d)
    print(f"⚡ REENCAUCE {c['id']}: {texto[:70]}")
    print(f"   propagado -> conversacion={c['conversacion']} tareas={c['tareas']} memoria={c['memoria']}")

def render():
    d = cargar()
    msjs = []
    for m in d["mensajes"]:
        p = ROSTER.get(m["de"], {"n":m["de"],"r":"","i":"•","c":"#7FA3A3"})
        msjs.append({**m, **p})
    sus = []
    for s in d["susurros"]:
        p = ROSTER.get(s["de"], {"n":s["de"],"r":"","i":"•","c":"#7FA3A3"})
        q = ROSTER.get(s["para"], {"n":s["para"],"r":"","i":"•","c":"#7FA3A3"})
        sus.append({**s, "n":p["n"], "c":p["c"], "i":p["i"], "pn":q["n"], "pc":q["c"], "pi":q["i"]})
    mis = []
    for m in d.get("misiones", []):
        p = ROSTER.get(m["sombra"], {"n":m["sombra"],"r":"","i":"•","c":"#7FA3A3"})
        mis.append({**m, "n":p["n"], "c":p["c"], "i":p["i"], "r":p["r"]})
    data = {
        "mensajes": msjs,
        "susurros": sus,
        "misiones": mis,
        "cambios": [
            {**c, "n_tareas": len(c.get("tareas", [])),
             "sombras": [ROSTER.get(next((m["sombra"] for m in d.get("misiones", []) if m["id"] == t), ""), {}).get("n", t)
                         for t in c.get("tareas", [])]}
            for c in d.get("cambios", [])
        ],
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
    if "--susurra" in a:
        i = a.index("--susurra")
        susurra(a[i+1], a[i+2], " ".join(a[i+3:]) or "(sin texto)")
    if "--responde" in a:
        i = a.index("--responde")
        susurra(a[i+1], a[i+2], " ".join(a[i+3:]) or "(sin texto)")
    if "--turno" in a:
        i = a.index("--turno")
        mid = a[i+1]
        resto = a[i+2:]
        som = None; tit = None
        if "--sombra" in resto:
            j = resto.index("--sombra"); som = resto[j+1]; resto = resto[:j] + resto[j+2:]
        if "--titulo" in resto:
            j = resto.index("--titulo"); tit = resto[j+1]; resto = resto[:j] + resto[j+2:]
        turno(mid, " ".join(resto) or "(sin instruccion)", sombra=som, titulo=tit)
    if "--cambio" in a:
        i = a.index("--cambio")
        resto = a[i+1:]; ant = ""; des = ""
        if "--antes" in resto:
            j = resto.index("--antes"); ant = resto[j+1]; resto = resto[:j] + resto[j+2:]
        if "--despues" in resto:
            j = resto.index("--despues"); des = resto[j+1]; resto = resto[:j] + resto[j+2:]
        cambio(" ".join(resto) or "(sin texto)", antes=ant, despues=des)
    render()

if __name__ == "__main__":
    main()
