import csv, re, time, os, unicodedata
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

SRC = "/opt/vigia/presas_final.csv"
DST = "/opt/vigia/presas_maps.csv"
LIMIT = int(os.environ.get("MAPS_LIMIT", "0") or 0)
MINTX = int(os.environ.get("MAPS_MINTX", "10"))
MINRT = float(os.environ.get("MAPS_MINRT", "4.0"))

def norm(s):
    s = (s or "").upper()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def overlap(a, b):
    ta, tb = set(a.split()), set(b.split())
    return len(ta & tb) / max(1, len(ta)) if ta and tb else 0

def parse_label(lbl):
    # "4,5 estrellas 148 reseñas"
    m = re.search(r"(\d[.,]?\d*)\s*estrella", lbl or "")
    r = float(m.group(1).replace(",", ".")) if m else None
    n = re.search(r"([\d.,]+)\s*rese", lbl or "")
    rev = int(re.sub(r"[^0-9]", "", n.group(1)) or 0) if n else 0
    return r, rev

def scrape_one(pg, nombre, ciudad):
    q = (nombre + " " + (ciudad or "") + " Colombia").strip()
    pg.goto("https://www.google.com/maps/search/" + quote_plus(q) + "?hl=es", timeout=35000)
    pg.wait_for_timeout(3800)
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
        rating, reviews = None, 0
        el = c.query_selector("[aria-label*='estrella']")
        if el:
            rating, reviews = parse_label(el.get_attribute("aria-label"))
        if rating is None:
            m = re.search(r"(\d[.,]?\d*)\s*\(\s*([\d.,]+)\s*\)", txt)
            if m:
                rating = float(m.group(1).replace(",", ".")); reviews = int(re.sub(r"[^0-9]", "", m.group(2)) or 0)
        closed = "Cerrado permanentemente" in txt
        sc = overlap(norm(nombre), norm(cname))
        if sc > best_score:
            best_score = sc
            best = {"match": cname, "rating": rating, "reviews": reviews, "closed": closed, "score": round(sc, 2)}
    return best

def main():
    rows = list(csv.reader(open(SRC, encoding="utf-8")))[1:]
    if LIMIT:
        rows = rows[:LIMIT]
    nuevo = not os.path.exists(DST)
    out = open(DST, "a", newline="", encoding="utf-8"); w = csv.writer(out)
    if nuevo:
        w.writerow(["nombre_osm", "ciudad", "telefono", "match", "rating", "reviews", "cerrado", "score", "pasa"])
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(locale="es-CO")
        pasan = 0
        for i, row in enumerate(rows):
            if len(row) < 6:
                continue
            nombre, ciudad, tel = row[0], row[2], row[3]
            try:
                best = scrape_one(pg, nombre, ciudad)
            except Exception as e:
                w.writerow([nombre, ciudad, tel, "", "", "", "", "", "err"]); out.flush(); time.sleep(2); continue
            if not best or best.get("rating") is None:
                w.writerow([nombre, ciudad, tel, (best or {}).get("match", ""), "", "", "", (best or {}).get("score", ""), "no_match"]); out.flush(); time.sleep(2); continue
            pasa = (not best["closed"]) and best["rating"] >= MINRT and (best["reviews"] or 0) >= MINTX and best["score"] >= 0.5
            w.writerow([nombre, ciudad, tel, best["match"], best["rating"], best["reviews"], best["closed"], best["score"], "SI" if pasa else "no"])
            if pasa:
                pasan += 1
            out.flush()
            print("[%d] %s -> %s | r=%s tx=%s cer=%s %s" % (i, nombre[:26], best["match"][:26], best["rating"], best["reviews"], best["closed"], "PASA" if pasa else "no"), flush=True)
            time.sleep(2.5)
        b.close()
    out.close()
    print("DONE procesadas=%d pasan=%d" % (len(rows), pasan), flush=True)

main()
