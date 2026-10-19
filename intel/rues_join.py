import csv, unicodedata, re, datetime, os

def norm(s):
    s = (s or "").upper().strip()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

RUES = "/opt/vigia/rues_mat.csv"
SRC = "/opt/vigia/presas_final.csv"
DST = "/opt/vigia/presas_edad.csv"

idx = {}
with open(RUES, encoding="utf-8", errors="replace") as f:
    r = csv.reader(f); next(r, None)
    for row in r:
        if len(row) < 10:
            continue
        name = norm(row[3]); fecha = (row[6] or "").strip(); mun = row[9]
        if name and fecha:
            idx.setdefault(name, (fecha, mun))
print("RUES indexado:", len(idx), "razones sociales")

today = datetime.date.today()
rows = list(csv.reader(open(SRC, encoding="utf-8")))
matched = 0; total = 0
out = open(DST, "w", newline="", encoding="utf-8")
w = csv.writer(out); w.writerow(["nombre","ciudad","telefono","match","fecha_matricula","anios"])
for row in rows[1:]:
    if len(row) < 6:
        continue
    total += 1
    hit = idx.get(norm(row[0]))
    if hit:
        fecha, mun = hit
        try:
            anios = (today - datetime.date(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))).days / 365.25
        except Exception:
            anios = -1
        w.writerow([row[0], row[2], row[3], "SI", fecha, round(anios, 1)]); matched += 1
    else:
        w.writerow([row[0], row[2], row[3], "no", "", ""])
out.close()
print("total=%d match=%d (%.1f%%)" % (total, matched, 100.0 * matched / max(total, 1)))
