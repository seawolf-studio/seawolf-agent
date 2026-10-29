#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPANDIR — convierte enlaces de CARPETA de MediaFire en enlaces de ARCHIVO
(que MiPony SI entiende), usando la API publica de MediaFire (SIN cuenta).

Por que existe: MiPony build-2023 no sabe leer carpetas, y la pagina de la carpeta
carga la lista por JavaScript (no se puede raspar el HTML). La API si responde.

Uso:
   python expandir.py cola-enlaces-EJEMPLO.txt                -> INFORME (tamanos), no escribe
   python expandir.py cola-enlaces-EJEMPLO.txt --salida lista.txt   -> escribe la cola expandida
   python expandir.py --carpeta hevfsdd3wut80                 -> probar una carpeta suelta
"""
import os, re, sys, json, urllib.request, collections

API = "https://www.mediafire.com/api/1.5/folder/get_content.php"
BASE = os.path.dirname(os.path.abspath(__file__))

def human(n):
    n = float(n)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024: return f"{n:,.0f} {u}"
        n /= 1024
    return f"{n:,.1f} PB"

def api_carpeta(clave, verbose=False):
    """Devuelve [(nombre, quickkey, bytes)] de una carpeta de MediaFire."""
    out, chunk = [], 1
    while True:
        url = (f"{API}?folder_key={clave}&content_type=files"
               f"&chunk={chunk}&chunk_size=100&response_format=json")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode("utf-8", "ignore")).get("response", {})
        except Exception as e:
            if verbose: print(f"      !! error con {clave}: {e}")
            return out
        if d.get("result") != "Success":
            return out
        fc = d.get("folder_content") or {}
        fs = fc.get("files") or []
        for f in fs:
            out.append((f.get("filename", ""), f.get("quickkey", ""), int(f.get("size", 0) or 0)))
        if fc.get("more_chunks") != "yes" or not fs:
            break
        chunk += 1
    return out

def clave_carpeta(u):
    m = re.search(r"mediafire\.com/folder/([^/?#]+)", u, re.I)
    return m.group(1) if m else None

# ---------- mismo parseo de cajones que mipony.py ----------
def parse_bloques(ruta):
    bloques, actual = [], []
    for l in open(ruta, encoding="utf-8", errors="ignore"):
        if re.match(r"^\s*={3,}\s*$", l):
            bloques.append(actual); actual = []
        else:
            actual.append(l)
    bloques.append(actual)
    tandas = []
    for b in bloques:
        titulo = tipo = carpeta = password = None; urls = []
        for l in b:
            s = l.strip()
            if not s or s.startswith("#"): continue
            low = s.lower()
            if low.startswith("titulo:"): titulo = s.split(":", 1)[1].strip(); continue
            if low.startswith("tipo:"):   tipo = s.split(":", 1)[1].strip(); continue
            if low.startswith("carpeta:"): carpeta = s.split(":", 1)[1].strip(); continue
            if low.startswith(("password:", "contrasena:", "contraseña:", "clave:", "pass:")):
                password = s.split(":", 1)[1].strip(); continue
            if s.startswith("---"): continue
            m = re.search(r"https?://\S+", s)
            if m: urls.append(m.group(0))
        if urls:
            tandas.append({"titulo": titulo or "(sin titulo)", "tipo": tipo, "carpeta": carpeta,
                           "password": password, "urls": urls})
    return tandas

def main():
    a = sys.argv[1:]
    if "--carpeta" in a:
        i = a.index("--carpeta"); fs = api_carpeta(a[i+1], verbose=True)
        tot = sum(x[2] for x in fs)
        print(f"carpeta {a[i+1]}: {len(fs)} archivos · {human(tot)}")
        for n, k, s in fs[:20]: print(f"   {human(s):>10}  {n[:52]}  {k}")
        return
    if not a:
        print(__doc__); return
    ruta = a[0]
    salida = None
    if "--salida" in a:
        j = a.index("--salida"); salida = a[j+1]

    tandas = parse_bloques(ruta)
    print(f"ARCHIVO: {ruta}")
    print(f"CAJONES: {len(tandas)}\n")

    total_general = 0
    total_archivos = 0
    lineas_salida = []
    sin_expandir = []
    for t in tandas:
        n_arch = 0; peso = 0; exp = []
        for u in t["urls"]:
            k = clave_carpeta(u)
            if k:
                fs = api_carpeta(k)
                for nombre, qk, size in fs:
                    exp.append(f"http://www.mediafire.com/?{qk}")
                    peso += size; n_arch += 1
                if not fs:
                    sin_expandir.append((t["titulo"], u))
                    exp.append(u)          # se deja tal cual para no perderlo
            else:
                exp.append(u)              # ya era enlace de archivo
                n_arch += 1
        total_general += peso; total_archivos += n_arch
        print(f"  {t['titulo'][:44]:<46} {n_arch:>4} archivos   {human(peso):>10}   [{t['tipo'] or '?'}]")
        lineas_salida.append("titulo: " + t["titulo"])
        lineas_salida.append("tipo: " + (t["tipo"] or "pelicula"))
        lineas_salida.append("carpeta: " + (t["carpeta"] or "H:\\caida"))
        lineas_salida.append("password: " + (t["password"] or ""))
        lineas_salida.append("---")
        lineas_salida.extend(exp)
        lineas_salida.append("")
        lineas_salida.append("===")
        lineas_salida.append("")

    print(f"\n  {'TOTAL':<46} {total_archivos:>4} archivos   {human(total_general):>10}")
    if sin_expandir:
        print(f"\n  ⚠ {len(sin_expandir)} enlace(s) de carpeta NO se pudieron leer:")
        for tit, u in sin_expandir[:6]: print(f"      {tit[:30]} -> {u[:60]}")

    if salida:
        with open(salida, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_salida))
        print(f"\n  ✔ cola EXPANDIDA escrita en: {salida}")
    else:
        print("\n  (informe solamente — agregue  --salida nombre.txt  para escribir la cola expandida)")

if __name__ == "__main__":
    main()
