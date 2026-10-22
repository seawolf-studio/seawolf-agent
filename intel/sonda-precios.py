#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sonda: ¿el precio viene ESCRITO en las fotos de los grupos sin caption-precio?"""
import os, sys, json, base64, io, re, urllib.request
from PIL import Image

ENV = r"C:\Users\Admin\AppData\Local\hermes\.env"
MODEL = "deepseek/deepseek-v4-flash-vision-exp"
PROMPT = ("Transcribe TODO el texto visible en esta imagen, literal. "
          "Si ves un numero que parezca PRECIO (ej. 45.000 / $45.000 / 45000), "
          "devuelvelo al final en la linea: PRECIO=<numero sin puntos ni simbolos> "
          "Si no hay ningun precio, escribe PRECIO=0. No inventes.")

def key():
    for l in open(ENV, encoding="utf-8", errors="ignore"):
        if l.startswith("OPENROUTER_API_KEY="): return l.strip().split("=",1)[1]
    sys.exit("sin key")

def analizar(p, api):
    im = Image.open(p).convert("RGB"); im.thumbnail((1200,1200))
    buf = io.BytesIO(); im.save(buf,"JPEG",quality=88)
    b64 = base64.b64encode(buf.getvalue()).decode()
    body = {"model":MODEL,"messages":[{"role":"user","content":[
        {"type":"text","text":PROMPT},
        {"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+b64}}]}],
        "temperature":0,"max_tokens":700,"reasoning":{"enabled":False}}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization":"Bearer "+api,"Content-Type":"application/json","User-Agent":"seawolf"})
    try:
        with urllib.request.urlopen(req, timeout=120) as f: r=json.load(f)
    except Exception as e: return f"(error {type(e).__name__})"
    if "choices" not in r: return "(sin choices)"
    return (r["choices"][0]["message"].get("content") or "").strip()

def main():
    api = key()
    for grupo, n in [("ropa_accesorios", 3), ("container2", 3), ("ultimas_tendencias", 3)]:
        base = rf"C:\Users\Admin\tienda\{grupo}"
        imgs = sorted(f for f in os.listdir(base) if f.lower().endswith(".jpg"))[:n]
        print(f"\n===== {grupo} =====")
        for f in imgs:
            txt = analizar(os.path.join(base,f), api)
            m = re.search(r"PRECIO\s*=\s*([\d\.]+)", txt or "")
            pr = m.group(1) if m else "?"
            print(f"  {f}: PRECIO={pr}")
            print("     " + " | ".join(txt.split("\n")[:4])[:220].replace("\n"," "))
if __name__=="__main__": main()
