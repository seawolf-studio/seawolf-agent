#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EXTRACTOR DE PRODUCTOS DESDE IMÁGENES — Seawolf Studio
Lee las fotos con precio (WhatsApp del proveedor) y saca nombre, marca, modelo y precio.

  python extraer-productos.py "C:\\Users\\Admin\\zapatillas"            # procesa la carpeta
  python extraer-productos.py "C:\\Users\\Admin\\zapatillas" --test     # solo 1 imagen (prueba)
  python extraer-productos.py --csv                                     # re-exporta el CSV

Salida:  zapatillas/productos.json  +  zapatillas/productos.csv
Idempotente: no repite imágenes ya procesadas (por nombre+tamaño).
"""
import os, sys, json, base64, csv, hashlib, mimetypes, urllib.request, re

ENV = r"C:\Users\Admin\AppData\Local\hermes\.env"
MODEL = os.environ.get("VISION_MODEL", "deepseek/deepseek-v4-flash-vision-exp")
EXTS = (".jpg", ".jpeg", ".png", ".webp")

PROMPT = """Eres un extractor de datos de catálogo de calzado deportivo.
Analiza la imagen y devuelve SOLO un JSON válido (sin markdown, sin explicación) con esta forma exacta:
{"nombre":"", "marca":"", "modelo":"", "precio": 0, "moneda":"COP", "tallas":"", "colores":"", "genero":"", "categoria":"", "notas":""}
Reglas:
- "precio": número entero sin puntos ni símbolos. Si hay varios precios (mayorista/detal), toma el de MAYORISTA si está rotulado; si no, el primero.
- Si un campo no aparece, déjalo como cadena vacía (o 0 en precio). NO inventes.
- "nombre": como lo describe el vendedor (ej. "Nike Air Force 1 Blanca").
- "notas": cualquier dato extra visible (promoción, mínimo de compra, referencia, TALLA ÚNICA, etc.).
"""

def key():
    for l in open(ENV, encoding="utf-8", errors="ignore"):
        if l.startswith("OPENROUTER_API_KEY="):
            return l.strip().split("=", 1)[1]
    sys.exit("Falta OPENROUTER_API_KEY en .env")

def hash_img(p):
    h = hashlib.blake2b(digest_size=8)
    h.update(os.path.basename(p).encode("utf-8", "ignore"))
    h.update(str(os.path.getsize(p)).encode())
    return h.hexdigest()

def analizar(path, api_key):
    mt = mimetypes.guess_type(path)[0] or "image/jpeg"
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    body = {"model": MODEL, "messages": [{"role": "user", "content": [
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:{mt};base64,{b64}"}}]}],
        "temperature": 0.1, "max_tokens": 700, "reasoning": {"enabled": False}}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json", "User-Agent": "seawolf"})
    with urllib.request.urlopen(req, timeout=180) as f:
        r = json.load(f)
    txt = r["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", txt, re.S)
    if not m: return {"_error": "sin JSON", "_raw": txt[:200]}
    try: return json.loads(m.group(0))
    except Exception as e: return {"_error": str(e), "_raw": txt[:200]}

def a_csv(regs, base):
    campos = ["archivo","nombre","marca","modelo","precio","moneda","tallas","colores","genero","categoria","notas"]
    with open(os.path.join(base, "productos.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for r in regs: w.writerow(r)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = os.path.abspath(args[0]) if args else r"C:\Users\Admin\zapatillas"
    js = os.path.join(base, "productos.json")
    regs = json.load(open(js, encoding="utf-8")) if os.path.exists(js) else []
    hechos = {r.get("_hash") for r in regs}
    if "--csv" in sys.argv:
        a_csv(regs, base); print("CSV exportado:", len(regs), "productos"); return
    imgs = sorted(p for p in (os.path.join(base, f) for f in os.listdir(base)) if p.lower().endswith(EXTS))
    if "--test" in sys.argv: imgs = imgs[:1]
    pend = [p for p in imgs if hash_img(p) not in hechos]
    print(f"[Extractor] {len(imgs)} imágenes · {len(pend)} nuevas por procesar")
    if not pend: print("Nada nuevo."); return
    api = key()
    for i, p in enumerate(pend, 1):
        try: d = analizar(p, api)
        except Exception as e: d = {"_error": str(e)}
        d["archivo"] = os.path.basename(p); d["_hash"] = hash_img(p)
        regs.append(d)
        est = d.get("_error") or f"{d.get('nombre','?')} | {d.get('precio','?')} {d.get('moneda','')}"
        print(f"  [{i}/{len(pend)}] {os.path.basename(p)[:34]:<34} -> {est}")
        json.dump(regs, open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        a_csv(regs, base)
    print(f"\nTOTAL en catálogo: {len(regs)} · archivos: {js} / productos.csv")
    ok = [r for r in regs if not r.get("_error") and r.get("precio")]
    if ok:
        vals = [r["precio"] for r in ok if isinstance(r.get("precio"), (int, float))]
        if vals: print(f"Precio: min {min(vals):,.0f} · max {max(vals):,.0f} · promedio {sum(vals)/len(vals):,.0f} {ok[0].get('moneda','')}")

if __name__ == "__main__":
    main()
