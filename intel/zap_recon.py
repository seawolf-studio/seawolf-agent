#!/usr/bin/env python3
# Reconocimiento: cuantos mensajes/imagenes/precios tiene cada grupo objetivo.
import json, os, urllib.request, unicodedata, re

TARGETS = [
    "BARCELONA MALL 11-12A",
    "GRUPO CONTAINER 2",
    "Ropa", "Accesorios",
    "LOBO_STORE_SHOES",
    "HYPE SNKS",
    "Ultimas Tendencias Zapatillas",
]
key = ""
for line in open("/root/.waha.env", encoding="utf-8", errors="ignore"):
    if line.startswith("WHATSAPP_API_KEY=") or line.startswith("WAHA_API_KEY="):
        key = line.strip().split("=", 1)[1].strip('"').strip("'")
base = "http://127.0.0.1:3000"
H = {"X-Api-Key": key}

def get(u):
    r = urllib.request.Request(u, headers=H)
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.load(f)

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

ov = get(f"{base}/api/seawolf/chats/overview?limit=800")
if isinstance(ov, dict): ov = ov.get("chats", [])
print("chats totales:", len(ov))

founds = {}
for c in ov:
    n = norm(c.get("name") or "")
    if not n: continue
    for t in TARGETS:
        tn = norm(t)
        if tn and tn in n:
            founds.setdefault(t, []).append((c.get("id"), c.get("name")))

print("\n=== GRUPOS ENCONTRADOS ===")
for t in TARGETS:
    for cid, name in founds.get(t, []):
        print(f"  [{t}] -> {cid} | {name}")

print("\n=== RECONOCIMIENTO POR GRUPO ===")
res = []
seen = set()
for t in TARGETS:
    for cid, name in founds.get(t, []):
        if cid in seen: continue
        seen.add(cid)
        try:
            msgs = get(f"{base}/api/seawolf/chats/{cid}/messages?limit=1000&downloadMedia=false")
            if isinstance(msgs, dict): msgs = msgs.get("messages", [])
        except Exception as e:
            print(f"  {name}: ERROR {e}"); continue
        imgs = [m for m in msgs if m.get("hasMedia")]
        withp = [m for m in imgs if re.search(r"\d[\d\.]{4,}", (m.get("body") or ""))]
        precios = []
        for m in withp:
            mm = re.search(r"\$\s*([\d\.\,]{5,})", (m.get("body") or ""))
            if mm:
                v = re.sub(r"[^\d]", "", mm.group(1))
                if v: precios.append(int(v))
        r = {"grupo": name, "id": cid, "msgs": len(msgs), "imgs": len(imgs),
             "con_precio": len(withp), "pmin": min(precios) if precios else 0,
             "pmax": max(precios) if precios else 0, "n_precios": len(precios)}
        res.append(r)
        print(f"  {name[:40]:<40} msgs {len(msgs):>4} | imgs {len(imgs):>4} | c/precio {len(withp):>4} | ${r['pmin']:,}-${r['pmax']:,}")
json.dump(res, open("/tmp/recon.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nRECON OK")
