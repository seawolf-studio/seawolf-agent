#!/usr/bin/env python3
# Baja imagenes + captions de TODOS los grupos objetivo, por carpeta.
import json, os, urllib.request, tarfile, unicodedata, re

GROUPS = [
    ("barcelona", "120363403121121040@g.us", 150),
    ("lobo_shoes", "120363416960559447@g.us", 200),
    ("hype_snks", "120363301738683176@g.us", 200),
    ("ropa_accesorios", "120363423850926129@g.us", 150),
    ("container2", "120363420001737849@g.us", 100),
    ("ultimas_tendencias", "120363422043942745@g.us", 60),
]
key = ""
for line in open("/root/.waha.env", encoding="utf-8", errors="ignore"):
    if line.startswith("WHATSAPP_API_KEY=") or line.startswith("WAHA_API_KEY="):
        key = line.strip().split("=", 1)[1].strip('"').strip("'")
base = "http://127.0.0.1:3000"
H = {"X-Api-Key": key}

def get(u, raw=False):
    r = urllib.request.Request(u, headers=H)
    with urllib.request.urlopen(r, timeout=120) as f:
        return f.read() if raw else json.load(f)

for slug, cid, cap in GROUPS:
    out = f"/tmp/barrido/{slug}"
    os.makedirs(out, exist_ok=True)
    try:
        msgs = get(f"{base}/api/seawolf/chats/{cid}/messages?limit=1200&downloadMedia=true")
        if isinstance(msgs, dict): msgs = msgs.get("messages", [])
    except Exception as e:
        print(f"{slug}: ERROR msgs {e}"); continue
    imgs = [m for m in msgs if (m.get("hasMedia") or m.get("media"))]
    imgs = imgs[-cap:]
    reg = []
    for i, m in enumerate(imgs, 1):
        url = ((m.get("media") or {}).get("url") or "")
        if url.startswith("http"): url = url.replace("localhost", "127.0.0.1")
        elif url.startswith("/"): url = base + url
        if not url: continue
        fn = f"{i:03d}.jpg"
        try:
            open(os.path.join(out, fn), "wb").write(get(url, raw=True))
            reg.append({"file": fn, "caption": (m.get("body") or ""), "ts": m.get("timestamp"), "id": m.get("id")})
        except Exception as e:
            print(f"  {slug}/{fn} err {e}")
    json.dump(reg, open(os.path.join(out, "captions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with tarfile.open(f"/tmp/barrido_{slug}.tgz", "w:gz") as t:
        t.add(out, arcname=slug)
    sz = os.path.getsize(f"/tmp/barrido_{slug}.tgz") // 1024
    print(f"{slug}: {len(reg)} imagenes | tar {sz}KB | OK")
print("BARRIDO OK")
