#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SEAwolf TOOLS — Modulo de OPTIMIZACION (motor)
Analiza discos: ranking de archivos mas pesados + buscador de duplicados, con
opcion de moverlos a la Papelera Seawolf (reversible) o borrar.

Comandos:
  python seawolf-tools.py scan  "C:\\ruta" [--top 30]     -> ranking de pesados
  python seawolf-tools.py dupes "C:\\ruta" [--min 1]       -> duplicados (MB minimo)
  python seawolf-tools.py papeles                          -> que hay en la Papelera
  python seawolf-tools.py rescatar N [--hard]              -> devuelve el archivo N
  python seawolf-tools.py limpiar --paths "a","b" [--hard] -> mueve/borra archivos
  python seawolf-tools.py serve ["C:\\ruta"] [--port 8770] -> APLICATIVO web local

SEGURIDAD: nunca toca nada sin que se lo pidas. Mueve (reversible) por defecto;
--hard borra de verdad. Guarda manifiesto para rescatar.
Elaborado por Bellion para el Monarca (codigo propio, limpio).
"""
import os, sys, json, hashlib, argparse, webbrowser
from collections import defaultdict
from datetime import datetime

PAPELERA = r"C:\Users\Admin\Seawolf_Papelera"
MANIFEST = os.path.join(PAPELERA, "_manifest.json")
SKIP_DIRS = {"$recycle.bin", "system volume information", "windows", "appdata", "node_modules", ".git", "__pycache__"}

def human(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n < 1024: return f"{n:.0f}{u}" if u=="B" else f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}PB"

def walk(root, skip=True):
    for dp, dns, fns in os.walk(root):
        if skip:
            dns[:] = [d for d in dns if d.lower() not in SKIP_DIRS and not d.startswith(".")]
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                if os.path.isfile(p): yield p, os.path.getsize(p)
            except OSError:
                continue

def scan(root, top=30):
    files = list(walk(root))
    files.sort(key=lambda x: -x[1])
    tot = sum(s for _, s in files)
    print(f"[Scan] {root}\n  {len(files)} archivos · {human(tot)} en total\n")
    print(f"  {'#':>3}  {'Tamano':>9}  Archivo")
    for i, (p, s) in enumerate(files[:top], 1):
        print(f"  {i:>3}  {human(s):>9}  {p}")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "optimizer-last-scan.json")
    json.dump({"root": root, "total": tot, "count": len(files), "top": [{"path": p, "size": s} for p, s in files[:top]]},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n[i] Reporte: {out}")
    return files

def dupes(root, min_mb=1):
    by_size = defaultdict(list)
    minsz = int(min_mb * 1024 * 1024)
    for p, s in walk(root):
        if s >= minsz: by_size[s].append(p)
    groups = []
    for s, paths in by_size.items():
        if len(paths) < 2: continue
        by_hash = defaultdict(list)
        for p in paths:
            try:
                h = hashlib.blake2b(digest_size=16)
                with open(p, "rb") as f: h.update(f.read(262144))
                by_hash[h.hexdigest()].append(p)
            except OSError: continue
        for hh, ps in by_hash.items():
            if len(ps) > 1: groups.append({"size": s, "files": ps})
    groups.sort(key=lambda g: -g["size"] * (len(g["files"]) - 1))
    waste = sum(g["size"] * (len(g["files"]) - 1) for g in groups)
    print(f"[Duplicados] {root}\n  {len(groups)} grupos · {human(waste)} desperdiciados\n")
    for i, g in enumerate(groups, 1):
        print(f"  Grupo {i}  ({len(g['files'])} copias · {human(g['size'])} c/u · desperdicia {human(g['size']*(len(g['files'])-1))})")
        for p in g["files"]: print(f"      {p}")
    return groups

def _manifest():
    if os.path.exists(MANIFEST):
        try: return json.load(open(MANIFEST, encoding="utf-8"))
        except Exception: return []
    return []
def _save(m): os.makedirs(PAPELERA, exist_ok=True); json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def limpiar(paths, hard=False):
    os.makedirs(PAPELERA, exist_ok=True)
    m = _manifest()
    for p in paths:
        if not os.path.isfile(p): print(f"  [x] no existe: {p}"); continue
        try:
            if hard:
                os.remove(p); print(f"  [BORRADO] {p}")
                m.append({"accion": "borrado", "path": p, "fecha": datetime.now().isoformat(timespec="seconds")})
            else:
                base = os.path.basename(p); dst = os.path.join(PAPELERA, base)
                if os.path.exists(dst): dst = os.path.join(PAPELERA, f"{datetime.now():%H%M%S}_{base}")
                import shutil; shutil.move(p, dst)
                print(f"  [A PAPELERA] {os.path.basename(dst)}")
                m.append({"accion": "papelera", "archivo": os.path.basename(dst), "original": p, "fecha": datetime.now().isoformat(timespec="seconds")})
        except OSError as e: print(f"  [x] error {p}: {e}")
    _save(m)

def papeles():
    m = _manifest()
    if not m: print("[i] Papelera vacia."); return
    for i, e in enumerate(m, 1):
        print(f"  {i}. [{e['accion']}] {e.get('archivo') or e.get('path')}  ({e['fecha']})")
def rescatar(n):
    m = _manifest()
    if not (1 <= n <= len(m)): print("[!] Numero invalido."); return
    e = m[n-1]
    if e["accion"] == "borrado": print("[!] Ese se borro. No hay rescate."); return
    import shutil
    src = os.path.join(PAPELERA, e["archivo"])
    if not os.path.exists(src): print("[!] No esta."); return
    os.makedirs(os.path.dirname(e["original"]), exist_ok=True); shutil.move(src, e["original"]); m.pop(n-1); _save(m)
    print(f"[OK] RESCATADO -> {e['original']}")

def serve(root, port):
    import http.server, socketserver, threading, urllib.parse
    state = {"files": [], "dupes": [], "root": root, "busy": True}
    def work():
        state["files"] = sorted(list(walk(root)), key=lambda x: -x[1])[:200]
        state["dupes"] = dupes_quiet(root); state["busy"] = False
    def dupes_quiet(r):
        by_size = defaultdict(list)
        for p, s in walk(r):
            if s >= 1048576: by_size[s].append(p)
        gs = []
        for s, ps in by_size.items():
            if len(ps) < 2: continue
            bh = defaultdict(list)
            for p in ps:
                try:
                    h = hashlib.blake2b(digest_size=16); f = open(p, "rb"); h.update(f.read(262144)); f.close(); bh[h.hexdigest()].append(p)
                except OSError: continue
            for _, pp in bh.items():
                if len(pp) > 1: gs.append({"size": s, "files": pp})
        gs.sort(key=lambda g: -g["size"]*(len(g["files"])-1)); return gs
    HTML = """<!doctype html><html lang=es><head><meta charset=utf-8><title>Seawolf Tools — Optimizacion</title>
<style>body{background:#0b1414;color:#e6fbfb;font-family:system-ui;margin:0;padding:18px}
h1{color:#4CE8E7;font-size:20px} .t{width:1100px;max-width:97vw}
table{border-collapse:collapse;width:100%;font-size:12.5px} th,td{padding:6px 8px;border-bottom:1px solid #1e3434;text-align:left}
th{color:#4CE8E7;font-size:11px;text-transform:uppercase} button{background:#4CE8E7;color:#04120f;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:600}
h2{color:#48E8D8;font-size:15px;margin-top:20px} .sz{color:#4CE8E7}</style></head><body><div class=t>
<h1>SEAWOLF TOOLS · Optimizacion de disco</h1><div id=st>Analizando…</div>
<h2>Archivos mas pesados</h2><table id=t1><thead><tr><th>#</th><th>Tamano</th><th>Archivo</th><th></th></tr></thead><tbody></tbody></table>
<h2>Duplicados</h2><div id=d></div></div>
<script>
async function load(){const r=await fetch('/api');const j=await r.json();
 document.getElementById('st').textContent=j.busy?'Analizando…':j.root;
 const tb=document.querySelector('#t1 tbody');tb.innerHTML='';
 (j.files||[]).forEach((f,i)=>{const tr=document.createElement('tr');
  tr.innerHTML='<td>'+(i+1)+'</td><td class=sz>'+f.h+'</td><td>'+f.p+'</td><td><button data-p="'+encodeURIComponent(f.p)+'">Mover</button></td>';
  tb.appendChild(tr);});
 const d=document.getElementById('d');d.innerHTML='';
 (j.dupes||[]).forEach(g=>{let h='<div style="margin:8px 0"><b>'+g.files.length+' copias · '+g.h+' c/u</b>';
  g.files.forEach(p=>{h+='<div><button data-p="'+encodeURIComponent(p)+'">Mover</button> '+p+'</div>';});d.innerHTML+=h+'</div>';});
 document.querySelectorAll('button[data-p]').forEach(b=>b.onclick=async()=>{await fetch('/mover',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({p:decodeURIComponent(b.dataset.p)})});b.textContent='✔ movido';});}
 if(j.busy) setTimeout(load,1500);}
load();
</script></body></html>"""
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _j(self, obj):
            b = json.dumps(obj).encode(); self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            if self.path.startswith("/api"):
                self._j({"busy": state["busy"], "root": state["root"],
                         "files": [{"p": p, "h": human(s)} for p, s in state["files"]],
                         "dupes": [{"h": human(g["size"]), "files": g["files"]} for g in state["dupes"][:40]]})
            else:
                b = HTML.encode(); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0)); data = json.loads(self.rfile.read(n) or b"{}")
            limpiar([data.get("p", "")], hard=False); self._j({"ok": True})
    threading.Thread(target=work, daemon=True).start()
    with socketserver.TCPServer(("127.0.0.1", port), H) as srv:
        print(f"[Seawolf Tools] http://127.0.0.1:{port}  (Ctrl+C para salir)")
        webbrowser.open(f"http://127.0.0.1:{port}")
        srv.serve_forever()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "dupes", "papeles", "rescatar", "limpiar", "serve"])
    ap.add_argument("arg", nargs="?", default=r"C:\Users\Admin")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--min", type=float, default=1)
    ap.add_argument("--port", type=int, default=8770)
    ap.add_argument("--paths", default="")
    ap.add_argument("--hard", action="store_true")
    a = ap.parse_args()
    if a.cmd == "scan": scan(a.arg, a.top)
    elif a.cmd == "dupes": dupes(a.arg, a.min)
    elif a.cmd == "papeles": papeles()
    elif a.cmd == "rescatar": rescatar(int(a.arg) if a.arg.isdigit() else 0)
    elif a.cmd == "limpiar": limpiar([p for p in a.paths.split(",") if p], a.hard)
    elif a.cmd == "serve": serve(a.arg, a.port)
