#!/usr/bin/env python3
# VIGIA — 2a PASADA: enriquecimiento por Google Places (New).
# Entrada: presas_CO.csv (OSM: sin web + telefono). Salida: presas_CO_google.csv
# Requiere: GOOGLE_PLACES_KEY en el entorno.
# Filtra: sin web (websiteUri ausente) + rating >= 4.0 + userRatingCount >= 10  (proxy ">80% positivas").
import csv, os, json, subprocess, time

SRC = "/opt/vigia/presas_CO.csv"
DST = "/opt/vigia/presas_CO_google.csv"
KEY = os.environ.get("GOOGLE_PLACES_KEY", "").strip()
if not KEY:
    raise SystemExit("Falta GOOGLE_PLACES_KEY")

URL = "https://places.googleapis.com/v1/places:searchText"
FIELDS = "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.websiteUri,places.nationalPhoneNumber,places.businessStatus"

def buscar(nombre, ciudad):
    q = "%s %s Colombia" % (nombre, ciudad or "")
    body = json.dumps({"textQuery": q, "languageCode": "es", "maxResultCount": 1})
    for _ in range(3):
        r = subprocess.run(["curl", "-s", "--max-time", "30", "-X", "POST", URL,
                            "-H", "Content-Type: application/json",
                            "-H", "X-Goog-Api-Key: " + KEY,
                            "-H", "X-Goog-FieldMask: " + FIELDS,
                            "--data", body], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception:
            time.sleep(2); continue
        if "error" in d:
            # 429/403 -> reintentar
            time.sleep(4); continue
        places = d.get("places", [])
        return places[0] if places else None
    return None

def main():
    rows = list(csv.reader(open(SRC, encoding="utf-8")))
    header, data = rows[0], rows[1:]
    nuevo = not os.path.exists(DST)
    f = open(DST, "a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["nombre","ciudad","telefono_osm","rating","resenas","web_google","tel_google","place_id","pasa"])
    ok = 0
    for i, r in enumerate(data):
        if len(r) < 6:
            continue
        nombre, ciudad, tel = r[0], r[2], r[3]
        p = buscar(nombre, ciudad)
        if not p:
            w.writerow([nombre, ciudad, tel, "", "", "", "", "", "no_match"]); continue
        rating = p.get("rating", "")
        resenas = p.get("userRatingCount", 0)
        web = p.get("websiteUri", "")
        telg = p.get("nationalPhoneNumber", "")
        pasa = (web == "" and float(rating or 0) >= 4.0 and int(resenas or 0) >= 10)
        w.writerow([nombre, ciudad, tel, rating, resenas, web, telg, p.get("id",""), "SI" if pasa else "no"])
        if pasa:
            ok += 1
        if i % 25 == 0:
            f.flush(); print("procesadas=%d pasan=%d" % (i, ok), flush=True)
        time.sleep(0.2)
    f.close()
    print("DONE procesadas=%d pasan=%d" % (len(data), ok), flush=True)

main()
