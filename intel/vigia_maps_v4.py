import csv, re, time, os, unicodedata
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

SRC = "/opt/vigia/presas_final.csv"
DST = "/opt/vigia/presas_maps.csv"
MINTX = int(os.environ.get("MAPS_MINTX", "0"))
MINRT = float(os.environ.get("MAPS_MINRT", "4.0"))

def norm(s):
    s = (s or "").upper()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def overlap(a, b):
    ta, tb = set(a.split()), set(b.split())
    return len(ta & tb) / max(1, len(ta)) if ta and tb else 0

def scrape_one(pg, nombre, ciudad):
    q = (nombre + " " + (ciudad or "") + " Colombia").strip()
    pg.goto("https://www.google.com/maps/search/" + quote_plus(q) + "?hl=es", timeout=30000)
    pg.wait_for_timeout(3500)
    best, best_score = None, -1
    for c in pg.query_selector_all("div.Nv2PK"):
        try:
            txt = c.inner_text()
        except Exception:
            continue
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        if not lines:
            continue
        cname = lines[0]
        rating = None
        for l in lines:
            m = re.match(r"^(\d[.,]?\d*)$", l)
            if m:
                rating = float(m.group(1).replace(",", ".")); break
        if rating is None:
            m = re.search(r"(\d[.,]?\d*)\s*estrella", txt)
            if m:
                rating = float(m.group(1).replace(",", "."))
        closed = "Cerrado permanentemente" in txt
        sc = overlap(norm(nombre), norm(cname))
        if sc > best_score:
            best_score = sc
            best = {"match": cname, "rating": rating, "closed": closed, "score": round(sc, 2)}
    return best

def main():
    rows = list(csv.reader(open(SRC, encoding="utf-8")))[1:]
    done = set()
    if os.path.exists(DST):
        for r in csv.reader(open(DST, encoding="utf-8")):
            if len(r) > 3:
                done.add((r[0], r[2]))
    nuevo = not os.path.exists(DST)
    out = open(DST, "a", newline="", encoding="utf-8"); w = csv.writer(out)
    if nuevo:
        w.writerow(["nombre_osm", "ciudad", "telefono", "match", "rating", "cerrado", "score", "pasa"])
    print("por procesar:", len(rows) - len(done), "ya hechas:", len(done), flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(locale="es-CO")
        n = pasan = 0
        for row in rows:
            if len(row) < 6:
                continue
            nombre, ciudad, tel = row[0], row[2], row[3]
            if (nombre, tel) in done:
                continue
            try:
                best = scrape_one(pg, nombre, ciudad)
            except Exception:
                time.sleep(3); continue
            if not best or best.get("rating") is None:
                w.writerow([nombre, ciudad, tel, (best or {}).get("match", ""), "", "", (best or {}).get("score", ""), "no_match"])
            else:
                pasa = (not best["closed"]) and best["rating"] >= MINRT and best["score"] >= 0.5
                w.writerow([nombre, ciudad, tel, best["match"], best["rating"], best["closed"], best["score"], "SI" if pasa else "no"])
                if pasa:
                    pasan += 1
            n += 1
            if n % 20 == 0:
                out.flush(); print("procesadas=%d pasan=%d" % (n, pasan), flush=True)
            time.sleep(2.2)
        b.close()
    out.close()
    print("DONE procesadas=%d pasan=%d" % (n, pasan), flush=True)

main()
