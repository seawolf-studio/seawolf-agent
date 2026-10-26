#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCUBRIR — herramienta de operador (local). Replica la seccion "Descubrir" de DooPlay.
Servidor local: el navegador habla con localhost; la clave TMDb NUNCA sale del PC.
Al agregar un titulo: escribe la fila en catalogo.csv (watch.py lo sube solo si esta activo).

Uso:  doble clic en INICIAR_DESCUBRIR.bat   ->  abre http://localhost:8090
"""
import http.server, socketserver, json, urllib.request, urllib.parse, csv, os, sys, webbrowser, threading, re

BASE = os.path.dirname(os.path.abspath(__file__))
TMDB_BASE = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p/w500"
PUERTO = 8090

# --- la clave vive en config.json (nunca en el HTML) ---
def cargar_clave():
    p = os.path.join(BASE, "config.json")
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)["tmdb_key"]
    except Exception:
        # respaldo: leerla de build.py
        try:
            t = open(os.path.join(BASE, "build.py"), encoding="utf-8", errors="ignore").read()
            m = re.search(r'TMDB_KEY\s*=\s*"([^"]+)"', t)
            if m: return m.group(1)
        except Exception: pass
    return ""

CLAVE = cargar_clave()

def tmdb(path, params=""):
    sep = "?" if "?" not in path else "&"
    url = f"{TMDB_BASE}{path}{sep}api_key={CLAVE}&language=es-ES"
    if params: url += "&" + params
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode())

def norm(x, tipo):
    return {
        "id": x.get("id"),
        "tipo": tipo,
        "titulo": x.get("title") or x.get("name") or "",
        "titulo_original": x.get("original_title") or x.get("original_name") or "",
        "anio": (x.get("release_date") or x.get("first_air_date") or "")[:4],
        "poster": (IMG + x["poster_path"]) if x.get("poster_path") else None,
        "sinopsis": x.get("overview") or "",
        "puntuacion": x.get("vote_average"),
        "generos": [g["name"] for g in x.get("genres", [])] if x.get("genres") else [],
    }

def buscar(q):
    d = tmdb("/search/multi", "query=" + urllib.parse.quote(q) + "&include_adult=false")
    out = []
    for x in (d or {}).get("results", []):
        if x.get("media_type") == "person": continue
        t = "serie" if x.get("media_type") == "tv" else "pelicula"
        out.append(norm(x, t))
    return [x for x in out if x["titulo"] and x["poster"]]

def por_anio(anio, paginas=3):
    pelis, series = [], []
    for pg in range(1, paginas + 1):
        try:
            d = tmdb("/discover/movie", f"primary_release_year={anio}&sort_by=popularity.desc&page={pg}&include_adult=false")
            pelis += [norm(x, "pelicula") for x in (d or {}).get("results", [])]
        except Exception as e: print("  [movie]", e)
        try:
            d = tmdb("/discover/tv", f"first_air_date_year={anio}&sort_by=popularity.desc&page={pg}&include_adult=false")
            series += [norm(x, "serie") for x in (d or {}).get("results", [])]
        except Exception as e: print("  [tv]", e)
    pelis = [x for x in pelis if x["poster"]]
    series = [x for x in series if x["poster"]]
    return {"peliculas": pelis, "series": series}

def detalle(tipo, mid):
    if tipo == "serie":
        d = tmdb(f"/tv/{mid}")
        cr = tmdb(f"/tv/{mid}/credits")
        vd = tmdb(f"/tv/{mid}/videos")
    else:
        d = tmdb(f"/movie/{mid}")
        cr = tmdb(f"/movie/{mid}/credits")
        vd = tmdb(f"/movie/{mid}/videos")
    if not d: return None
    reparto = [c["name"] for c in (cr or {}).get("cast", [])[:8]]
    director = next((c["name"] for c in (cr or {}).get("crew", []) if c.get("job") == "Director"), "")
    trailer = ""
    for v in (vd or {}).get("results", []):
        if v.get("type") == "Trailer" and v.get("site") == "YouTube":
            trailer = "https://www.youtube.com/embed/" + v["key"]; break
    out = norm(d, tipo)
    out.update({
        "sinopsis": d.get("overview") or "",
        "generos": [g["name"] for g in d.get("genres", [])],
        "reparto": reparto,
        "director": director,
        "trailer": trailer,
        "duracion": d.get("runtime") or (d.get("episode_run_time") or [""])[0],
        "temporadas": d.get("number_of_seasons"),
        "episodios": d.get("number_of_episodes"),
        "fondo": (IMG + d["backdrop_path"]) if d.get("backdrop_path") else "",
    })
    return out

def agregar(titulo, tipo, enlaces):
    """Escribe la fila en catalogo.csv. Devuelve el estado."""
    ruta = os.path.join(BASE, "catalogo.csv")
    # normaliza tipo al vocabulario del build.py
    tipo = (tipo or "pelicula").lower()
    if tipo in ("película", "pelicula"): tipo = "pelicula"
    if tipo in ("serie", "series"): tipo = "serie"
    if tipo in ("anime",): tipo = "anime"
    if tipo in ("comic", "comics"): tipo = "comics"
    # evita duplicados por titulo
    existentes = set()
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8", errors="ignore", newline="") as f:
            for row in csv.reader(f):
                if row and row[0].strip().lower() == titulo.strip().lower():
                    return {"ok": False, "motivo": "ya existe en el catalogo"}
    # append
    nuevo = not os.path.exists(ruta)
    with open(ruta, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if nuevo: w.writerow(["titulo", "tipo", "enlaces"])
        w.writerow([titulo, tipo, enlaces])
    return {"ok": True, "titulo": titulo, "tipo": tipo}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=BASE, **kw)
    def log_message(self, fmt, *args): pass
    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        try:
            if u.path == "/api/buscar":
                self._json(200, {"resultados": buscar(q.get("q", [""])[0])}); return
            if u.path == "/api/anio":
                a = q.get("anio", [""])[0]
                if not a.isdigit(): self._json(400, {"error": "anio invalido"}); return
                self._json(200, por_anio(a)); return
            if u.path == "/api/detalle":
                d = detalle(q.get("tipo", ["pelicula"])[0], q.get("id", [""])[0])
                self._json(200, d or {"error": "no encontrado"}); return
        except Exception as e:
            self._json(500, {"error": str(e)}); return
        if u.path in ("/", "/index.html"):
            self.path = "/descubrir.html"
        return super().do_GET()
    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path != "/api/agregar":
            self.send_response(404); self.end_headers(); return
        n = int(self.headers.get("Content-Length", 0))
        try:
            d = json.loads(self.rfile.read(n).decode() or "{}")
            r = agregar(d.get("titulo", ""), d.get("tipo", ""), d.get("enlaces", ""))
            self._json(200 if r.get("ok") else 409, r)
        except Exception as e:
            self._json(500, {"error": str(e)})

def main():
    if not CLAVE:
        print("AVISO: no encontre clave TMDb (config.json ni build.py).")
    print(f"DESCUBRIR — herramienta de operador")
    print(f"  Servidor local: http://localhost:{PUERTO}")
    print(f"  Clave TMDb: {'OK' if CLAVE else 'FALTA'}")
    print(f"  Abre el navegador. Ctrl+C para detener.\n")
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PUERTO}")).start()
    with socketserver.ThreadingTCPServer(("127.0.0.1", PUERTO), Handler) as s:
        s.allow_reuse_address = True
        try: s.serve_forever()
        except KeyboardInterrupt: print("\nDetenido.")

if __name__ == "__main__":
    main()
