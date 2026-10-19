#!/usr/bin/env python3
# RECORTE A COLOMBIA — filtra el CSV del Vigia por el poligono real de Colombia (point-in-polygon).
import json, csv, os, urllib.request

SRC = "/opt/vigia/presas_colombia.csv"
DST = "/opt/vigia/presas_colombia_co.csv"
GEO = "/opt/vigia/COL.geo.json"

if not os.path.exists(GEO):
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/COL.geo.json"
    req = urllib.request.Request(url, headers={"User-Agent": "SeawolfVigia/1.0"})
    open(GEO, "wb").write(urllib.request.urlopen(req, timeout=90).read())

gj = json.load(open(GEO))
geom = gj["features"][0]["geometry"]
polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]

def in_ring(lon, lat, ring):
    inside = False; n = len(ring); j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def inside(lon, lat):
    for poly in polys:
        if in_ring(lon, lat, poly[0]):
            if any(in_ring(lon, lat, h) for h in poly[1:]):
                continue
            return True
    return False

rows = list(csv.reader(open(SRC, encoding="utf-8")))
kept = 0
with open(DST, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["nombre", "categoria", "ciudad", "telefono", "lat", "lon"])
    for r in rows[1:]:
        if len(r) < 6:
            continue
        try:
            lat = float(r[4]); lon = float(r[5])
        except ValueError:
            continue
        if inside(lon, lat):
            w.writerow(r); kept += 1
print("total=%d dentro_CO=%d fuera=%d" % (len(rows) - 1, kept, (len(rows) - 1) - kept))
