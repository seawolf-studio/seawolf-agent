#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CATALOGO POR GRUPO — caption (precio/tallas) + vision (marca/modelo/color y precio en foto).
Sirve para zapatillas, ropa y accesorios.

  python catalogo-grupo.py <carpeta> [--margen 0.35] [--limit N] [--cat zapatillas|ropa|accesorios]

Salida: <carpeta>/catalogo.json + <carpeta>/catalogo.csv   (idempotente, incremental)
"""
import os, sys, json, re, base64, mimetypes, urllib.request, csv

ENV = r"C:\Users\Admin\AppData\Local\hermes\.env"
MODEL = "deepseek/deepseek-v4-flash-vision-exp"
PROMPT = """Analiza la foto de este producto de moda y devuelve SOLO JSON valido:
{"marca":"","modelo":"","color":"","tipo":"","genero":"","precio_foto":0,"descripcion":""}
Reglas:
- Escribe SOLO lo que SE VE. Si no identificas marca o modelo, deja "".
- "precio_foto": si el precio viene ESCRITO SOBRE LA IMAGEN, ponlo como entero sin puntos ni simbolos. Si no aparece, 0.
- "tipo": categoría (sneaker/basket/running/urbano/bota/sandalias/camiseta/pantalon/gorra/gafas/medias/ropa/accesorio).
- "color": color dominante simple. "genero": dama/caballero/unisex/nino si se deduce.
- "descripcion": 6-12 palabras de lo que se ve.
NO inventes precios ni marcas."""

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
        "temperature":0.1,"max_tokens":700,"reasoning":{"enabled":False}}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization":"Bearer "+api,"Content-Type":"application/json","User-Agent":"seawolf"})
    try:
        with urllib.request.urlopen(req, timeout=180) as f: r=json.load(f)
    except Exception as e:
        print(f"      [api-error] {type(e).__name__}: {str(e)[:90]}")
        return {}
    if "choices" not in r:
        print(f"      [api] sin choices: {str(r)[:110]}")
        return {}
    txt = (r["choices"][0]["message"].get("content") or "").strip()
    m = re.search(r"\{.*\}", txt, re.S)
    if not m: return {}
    try: return json.loads(m.group(0))
    except Exception: return {}

def parse_caption(c):
    t = (c or "").replace("*","").replace("\n"," ")
    precio = None
    m = re.search(r"(?:💲|\$)\s*([\d\.\,]{4,})", t)
    if m:
        v = re.sub(r"[^\d]","",m.group(1))
        if v: precio = int(v)
    if precio is None:
        for m in re.finditer(r"\b(\d{2,3})\.(\d{3})\b", t):
            precio = int(m.group(1)+m.group(2)); break
    tallas = ""
    m = re.search(r"(?:del|tallas?|talla)\s*([0-9]{2}\s*(?:al|a|-|/)\s*[0-9]{2})", t, re.I)
    if m: tallas = m.group(1)
    else:
        ms = re.findall(r"\b(3[5-9]|4[0-5])\b", t)
        if len(ms) >= 2: tallas = f"{min(ms)}-{max(ms)}"
    nota = " ".join(k for k in ["EURO","UNISEX","DAMA","CABALLERO","NIÑO","TALLA UNICA","OFERTA"] if k.lower() in t.lower())
    return precio or 0, tallas, nota

def main():
    argv = sys.argv[1:]; args=[]; i=0
    while i < len(argv):
        if argv[i] in ("--margen","--limit","--cat"): i+=2; continue
        if argv[i].startswith("--"): i+=1; continue
        args.append(argv[i]); i+=1
    base = os.path.abspath(args[0]) if args else os.getcwd()
    margen = float(sys.argv[sys.argv.index("--margen")+1]) if "--margen" in sys.argv else 0.35
    limit = int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else None
    cat = sys.argv[sys.argv.index("--cat")+1] if "--cat" in sys.argv else "zapatillas"

    caps_p = os.path.join(base,"captions.json")
    caps = json.load(open(caps_p, encoding="utf-8")) if os.path.exists(caps_p) else []
    if not caps:
        files = sorted(f for f in os.listdir(base) if f.lower().endswith((".jpg",".jpeg",".png",".webp")))
        caps = [{"file":f,"caption":"","ts":0,"id":""} for f in files]
    out_js = os.path.join(base,"catalogo.json")
    regs = json.load(open(out_js, encoding="utf-8")) if os.path.exists(out_js) else []
    hechos = {r["archivo"] for r in regs}
    api = key()
    pend = [c for c in caps if c["file"] not in hechos and os.path.exists(os.path.join(base,c["file"]))]
    if limit: pend = pend[:limit]
    print(f"[{os.path.basename(base)}] {len(caps)} items · {len(pend)} por procesar · margen {margen:.0%}")
    for k,c in enumerate(pend,1):
        v = vision(os.path.join(base,c["file"]), api)
        pm_cap, tallas, nota = parse_caption(c.get("caption",""))
        pm_foto = v.get("precio_foto") or 0
        try: pm_foto = int(re.sub(r"[^\d]","",str(pm_foto)) or 0)
        except Exception: pm_foto = 0
        pm = pm_cap or pm_foto
        origen = "caption" if pm_cap else ("foto" if pm_foto else "")
        r = {"archivo": c["file"], "caption": c.get("caption",""),
             "marca": v.get("marca",""), "modelo": v.get("modelo",""), "color": v.get("color",""),
             "tipo": v.get("tipo","") or cat, "genero": v.get("genero",""), "descripcion": v.get("descripcion",""),
             "tallas": tallas, "notas": nota,
             "precio_mayorista": pm, "precio_origen": origen,
             "precio_venta": int(round(pm*(1+margen)/1000)*1000) if pm else 0}
        regs.append(r)
        print(f"  [{k}/{len(pend)}] {c['file']} | {r['marca']} {r['modelo']} | {r['tallas'] or '?'} | ${pm:,} ({origen or 's/p'})")
        json.dump(regs, open(out_js,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    campos=["archivo","marca","modelo","tipo","genero","color","tallas","precio_mayorista","precio_origen","precio_venta","descripcion","notas","caption"]
    with open(os.path.join(base,"catalogo.csv"),"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=campos,extrasaction="ignore"); w.writeheader()
        for r in regs: w.writerow(r)
    ps=[r["precio_mayorista"] for r in regs if r.get("precio_mayorista")]
    print(f"TOTAL {len(regs)} · con precio {len(ps)}" + (f" · ${min(ps):,}-${max(ps):,}" if ps else ""))

if __name__ == "__main__":
    main()
