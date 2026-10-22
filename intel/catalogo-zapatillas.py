#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CATALOGO DE ZAPATILLAS — une CAPTION de WhatsApp (precio/tallas) + VISION (nombre/modelo/color).

  python catalogo-zapatillas.py [carpeta] [--margen 0.35] [--limit 10]

Entrada : <carpeta>/NNN.jpg + <carpeta>/captions.json
Salida  : <carpeta>/catalogo.json + <carpeta>/catalogo.csv

El precio y las tallas salen del TEXTO (vienen escritos por el proveedor) -> cero invencion.
La vision solo aporta lo que la foto dice (marca, modelo, color). Si no lo ve, lo deja vacio.
"""
import os, sys, json, re, base64, mimetypes, urllib.request, csv

ENV = r"C:\Users\Admin\AppData\Local\hermes\.env"
MODEL = "deepseek/deepseek-v4-flash-vision-exp"
PROMPT = """Mira la foto de este calzado y devuelve SOLO JSON valido:
{"marca":"","modelo":"","color":"","tipo":"","genero":""}
Reglas: escribe lo que SE VE en la foto. Si no puedes identificar la marca o el modelo, deja "".
No inventes, no adivines por moda. "tipo": sneaker/basket/running/urbano/bota/sandalias.
"color": color dominante en palabras simples."""

def key():
    for l in open(ENV, encoding="utf-8", errors="ignore"):
        if l.startswith("OPENROUTER_API_KEY="): return l.strip().split("=",1)[1]
    sys.exit("falta OPENROUTER_API_KEY")

def vision(path, api):
    mt = mimetypes.guess_type(path)[0] or "image/jpeg"
    b64 = base64.b64encode(open(path,"rb").read()).decode()
    body = {"model": MODEL, "messages":[{"role":"user","content":[
        {"type":"text","text":PROMPT},
        {"type":"image_url","image_url":{"url":f"data:{mt};base64,{b64}"}}]}],
        "temperature":0.1,"max_tokens":600,"reasoning":{"enabled":False}}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization":"Bearer "+api,"Content-Type":"application/json","User-Agent":"seawolf"})
    with urllib.request.urlopen(req, timeout=180) as f: r=json.load(f)
    txt = (r["choices"][0]["message"].get("content") or "").strip()
    if not txt: return {}
    m = re.search(r"\{.*\}", txt, re.S)
    if not m: return {}
    try: return json.loads(m.group(0))
    except Exception: return {}

def parse_caption(c):
    t = (c or "").replace("*","").replace("\n"," ")
    precio = None
    for pat in [r"\$\s*([\d\.\,]{5,})", r"([\d\.\,]{5,})\s*(?:pesos|cop)", r"💲\s*([\d\.\,]{5,})"]:
        m = re.search(pat, t, re.I)
        if m:
            v = re.sub(r"[^\d]", "", m.group(1))
            if v: precio = int(v); break
    if precio is None:
        for m in re.finditer(r"\b(\d{2,3})\.(\d{3})\b", t):
            precio = int(m.group(1)+m.group(2)); break
    tallas = ""
    m = re.search(r"(?:del|tallas?|talla)\s*([0-9]{2}\s*(?:al|a|-|/)\s*[0-9]{2})", t, re.I)
    if m: tallas = m.group(1)
    else:
        ms = re.findall(r"\b(3[5-9]|4[0-5])\b", t)
        if len(ms) >= 2: tallas = f"{min(ms)}-{max(ms)}"
    nota = ""
    for kw in ["EURO","UNISEX","DAMA","CABALLERO","NIÑO","TALLA UNICA"]:
        if kw.lower() in t.lower(): nota = (nota + kw.title() + " ").strip()
    return {"precio_mayorista": precio or 0, "tallas": tallas, "notas": nota}

def main():
    argv = sys.argv[1:]
    args = []
    i = 0
    while i < len(argv):
        if argv[i] in ("--margen", "--limit"):
            i += 2; continue
        if argv[i].startswith("--"):
            i += 1; continue
        args.append(argv[i]); i += 1
    base = os.path.abspath(args[0]) if args else r"C:\Users\Admin\zapatillas"
    margen = 0.35
    if "--margen" in sys.argv:
        margen = float(sys.argv[sys.argv.index("--margen")+1])
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit")+1])
    caps = json.load(open(os.path.join(base,"captions.json"), encoding="utf-8"))
    out_js = os.path.join(base,"catalogo.json")
    prev = json.load(open(out_js, encoding="utf-8")) if os.path.exists(out_js) else []
    hechos = {r["archivo"] for r in prev}
    api = key(); regs = prev[:]
    pend = [c for c in caps if c["file"] not in hechos and os.path.exists(os.path.join(base,c["file"]))]
    if limit: pend = pend[:limit]
    print(f"[Catalogo] {len(caps)} mensajes · {len(pend)} por procesar · margen {margen:.0%}")
    for i,c in enumerate(pend,1):
        p = os.path.join(base,c["file"])
        v = vision(p, api)
        cap = parse_caption(c.get("caption",""))
        pm = cap["precio_mayorista"]
        r = {"archivo": c["file"], "caption": c.get("caption",""),
             "marca": v.get("marca",""), "modelo": v.get("modelo",""), "color": v.get("color",""),
             "tipo": v.get("tipo",""), "genero": v.get("genero",""),
             "tallas": cap["tallas"], "notas": cap["notas"],
             "precio_mayorista": pm,
             "precio_venta": int(round(pm*(1+margen)/1000)*1000) if pm else 0}
        regs.append(r)
        print(f"  [{i}/{len(pend)}] {c['file']} | {r['marca']} {r['modelo']} | {r['tallas'] or '?'} | ${pm:,} -> ${r['precio_venta']:,}")
        json.dump(regs, open(out_js,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    campos=["archivo","marca","modelo","color","tipo","genero","tallas","precio_mayorista","precio_venta","notas","caption"]
    with open(os.path.join(base,"catalogo.csv"),"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=campos,extrasaction="ignore"); w.writeheader()
        for r in regs: w.writerow(r)
    print(f"\nTOTAL catalogo: {len(regs)} · {out_js}")
    ps=[r["precio_mayorista"] for r in regs if r.get("precio_mayorista")]
    if ps: print(f"Precio mayorista: min {min(ps):,} · max {max(ps):,} · prom {sum(ps)//len(ps):,} COP")

if __name__ == "__main__":
    main()
