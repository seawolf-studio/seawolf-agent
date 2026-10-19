#!/usr/bin/env python3
# VIGIA v4 — RE-BARRIDO Colombia capturando ETIQUETAS DE SEGMENTACION (para separar privado/publico, cadenas, etc.)
# Salida: presas_v4.csv  | columnas: nombre,categoria,ciudad,telefono,tipo_operador,marca,educacion,lat,lon
import json, subprocess, csv, time, os

OVERPASS = "https://overpass-api.de/api/interpreter"
UA = "SeawolfVigia/1.0 (contact seawolfk.studio@gmail.com)"
KEYS = ["shop","amenity","office","craft","healthcare","leisure","tourism"]
OUT = "/opt/vigia/presas_v4.csv"
W,S,E,N = -79.3, -4.4, -66.7, 13.6
STEP = 2.0

def cells():
    lat = S
    while lat < N:
        lon = W
        while lon < E:
            yield (lon, lat, min(lon+STEP,E), min(lat+STEP,N))
            lon += STEP
        lat += STEP

def query(cell):
    w,s,e,n = cell
    parts = "".join('nwr["name"]["%s"][!"website"][!"contact:website"](area.co)(%.4f,%.4f,%.4f,%.4f);' % (k,s,w,n,e) for k in KEYS)
    q = '[out:json][timeout:180];area["ISO3166-1"="CO"][admin_level=2]->.co;(%s);out center tags;' % parts
    for _ in range(3):
        r = subprocess.run(["curl","-s","-A",UA,"--max-time","200",OVERPASS,"--data-urlencode","data="+q],
                           capture_output=True, text=True)
        if r.stdout.strip().startswith("{"):
            try:
                return json.loads(r.stdout)
            except Exception:
                pass
        time.sleep(6)
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
        w.writerow(["nombre","categoria","ciudad","telefono","tipo_operador","marca","educacion","lat","lon"])
    for cell in cells():
        d = query(cell); got = 0
        if d:
            for el in d.get("elements", []):
                t = el.get("tags", {})
                nombre = t.get("name", "")
                tel = t.get("phone") or t.get("contact:phone") or ""
                if not nombre or not tel:
                    continue
                key = (nombre.lower(), tel)
                if key in seen:
                    continue
                seen.add(key)
                w.writerow([nombre, categoria(t), t.get("addr:city",""),
                            tel, t.get("operator:type",""), t.get("brand",""),
                            t.get("isced:level",""),
                            el.get("lat") or (el.get("center") or {}).get("lat"),
                            el.get("lon") or (el.get("center") or {}).get("lon")])
                got += 1; n += 1
        f.flush()
        print("cell %s ok=%s +%d total=%d" % (cell, bool(d), got, n), flush=True)
        time.sleep(2)
    f.close()
    print("DONE total=%d" % n, flush=True)

main()
