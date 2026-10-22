#!/usr/bin/env python3
# Baja las ultimas N imagenes del grupo BARCELONA MALL con su caption (precio/tallas).
import json, os, urllib.request, tarfile

CID = "120363403121121040@g.us"
N   = int(os.environ.get("N", "40"))
OUT = "/tmp/zap"
os.makedirs(OUT, exist_ok=True)

key = ""
for line in open("/root/.waha.env", encoding="utf-8", errors="ignore"):
    if line.startswith("WHATSAPP_API_KEY=") or line.startswith("WAHA_API_KEY="):
        key = line.strip().split("=", 1)[1].strip('"').strip("'")
base = "http://127.0.0.1:3000"
H = {"X-Api-Key": key}

def get(u, raw=False):
    r = urllib.request.Request(u, headers=H)
    with urllib.request.urlopen(r, timeout=60) as f:
        return f.read() if raw else json.load(f)

msgs = get(f"{base}/api/seawolf/chats/{CID}/messages?limit=200&downloadMedia=true")
if isinstance(msgs, dict): msgs = msgs.get("messages", [])
imgs = [m for m in msgs if (m.get("hasMedia") or m.get("media")) and "image" in str((m.get("media") or {}).get("mimetype", "image"))]
imgs = imgs[-N:]
reg = []
for i, m in enumerate(imgs, 1):
    url = ((m.get("media") or {}).get("url") or "")
    if url.startswith("http"): url = url.replace("localhost", "127.0.0.1")
    elif url.startswith("/"): url = base + url
    if not url: print(f"  {i:03d} sin url"); continue
    fn = f"{i:03d}.jpg"
    try:
        data = get(url, raw=True)
        open(os.path.join(OUT, fn), "wb").write(data)
        reg.append({"file": fn, "caption": (m.get("body") or ""), "ts": m.get("timestamp"), "id": m.get("id")})
        print(f"  {fn} {len(data)//1024}KB | {(m.get('body') or '')[:50].replace(chr(10),' ')}")
    except Exception as e:
        print(f"  {fn} ERROR {e}")
json.dump(reg, open(os.path.join(OUT, "captions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with tarfile.open("/tmp/zap.tgz", "w:gz") as t:
    t.add(OUT, arcname="zap")
print("OK", len(reg), "imagenes + captions.json")
