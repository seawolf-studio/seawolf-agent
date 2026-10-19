#!/usr/bin/env python3
# VIGIA (LOBO CAZADOR) v2 — barrido OpenStreetMap de COLOMBIA por frontera real (area.co, sin contaminacion)
# Negocios SIN pagina web y CON telefono (contactables). Escribe CSV.
import json, subprocess, csv, time, os

OVERPASS = "https://overpass-api.de/api/interpreter"
UA = "SeawolfVigia/1.0 (contact seawolfk.studio@gmail.com)"
KEYS = ["shop","amenity","office","craft","healthcare","leisure","tourism"]
OUT = "/opt/vigia/presas_CO.csv"
AREA = 'area["ISO3166-1"="CO"][admin_level=2]->.co;'

def query(key):
    q = '[out:json][timeout:600];%snwr["name"]["%s"][!"website"][!"contact:website"](area.co);out center tags;' % (AREA, key)
    for _ in range(4):
        r = subprocess.run(["curl","-s","-A",UA,"--max-time","660",OVERPASS,"--data-urlencode","data="+q],
                           capture_output=True, text=True)
        if r.stdout.strip().startswith("{"):
            try:
                return json.loads(r.stdout)
            except Exception:
                pass
        time.sleep(8)
    return None

def categoria(tags):
    for k in KEYS:
        if k in tags:
            return tags[k]
    return ""

def main():
    seen = set(); n = 0
    nuevo = not os.path.exists(OUT)
    f = open(OUT, "a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["nombre","categoria","ciudad","telefono","lat","lon"])
    for k in KEYS:
        d = query(k); got = 0
        if d:
            for el in d.get("elements", []):
                t = el.get("tags", {})
                nombre = t.get("name", "")
                tel = t.get("phone") or t.get("contact:phone") or ""
                if not nombre or not tel:
                    continue
                lat = el.get("lat") or (el.get("center") or {}).get("lat")
                lon = el.get("lon") or (el.get("center") or {}).get("lon")
                key = (nombre.lower(), tel)
                if key in seen:
                    continue
                seen.add(key)
                w.writerow([nombre, categoria(t), t.get("addr:city", ""), tel, lat, lon]); got += 1; n += 1
        f.flush()
        print("key %s ok=%s +%d total=%d" % (k, bool(d), got, n), flush=True)
        time.sleep(3)
    f.close()
    print("DONE total=%d" % n, flush=True)

main()
