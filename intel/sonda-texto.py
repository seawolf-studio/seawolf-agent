#!/usr/bin/env python3
# ¿Hay precios en mensajes de TEXTO (aparte de las fotos) en los 3 grupos sin caption-precio?
import json, urllib.request, re
GR = {"ropa_accesorios":"120363423850926129@g.us",
      "container2":"120363420001737849@g.us",
      "ultimas_tendencias":"120363422043942745@g.us"}
key=""
for l in open("/root/.waha.env", encoding="utf-8", errors="ignore"):
    if l.startswith("WHATSAPP_API_KEY=") or l.startswith("WAHA_API_KEY="):
        key=l.strip().split("=",1)[1].strip('"').strip("'")
base="http://127.0.0.1:3000"; H={"X-Api-Key":key}
def get(u):
    r=urllib.request.Request(u,headers=H)
    with urllib.request.urlopen(r,timeout=120) as f: return json.load(f)
for slug,cid in GR.items():
    msgs=get(f"{base}/api/seawolf/chats/{cid}/messages?limit=1000&downloadMedia=false")
    if isinstance(msgs,dict): msgs=msgs.get("messages",[])
    con_img=sum(1 for m in msgs if m.get("hasMedia"))
    tex=[m for m in msgs if m.get("body") and not m.get("hasMedia")]
    precios=[]
    for m in tex:
        mm=re.search(r"\$\s*([\d\.\,]{4,})", m.get("body") or "")
        if mm:
            v=re.sub(r"[^\d]","",mm.group(1))
            if v: precios.append(int(v))
    print(f"\n{slug}: {len(msgs)} msgs | con imagen {con_img} | texto-solo {len(tex)} | texto CON precio {len(precios)}")
    for m in tex[:5]:
        print("   ·", (m.get("body") or "")[:90].replace("\n"," "))
    if precios: print(f"   PRECIOS TEXTO: ${min(precios):,} - ${max(precios):,}")
