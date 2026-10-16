#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SEAWOLF TOOLS — Modulo de OPTIMIZACION DE DISCO  (v2, interfaz pulida)
Ranking de archivos mas pesados + duplicados + papelera reversible + aplicativo web.

  python seawolf-tools.py scan  "C:\\ruta" [--top 30]
  python seawolf-tools.py dupes "C:\\ruta" [--min 1]
  python seawolf-tools.py papeles / rescatar N / limpiar --paths "a","b" [--hard]
  python seawolf-tools.py serve ["C:\\ruta"] [--port 8770]   <-- APLICATIVO WEB

Seguridad: mueve a la Papelera Seawolf (reversible) por defecto; --hard borra de
verdad. Nunca actua sin orden explicita. Manifiesto para rescatar.
Codigo propio y limpio. Elaborado por Bellion para el Monarca (Key).
"""
import os, sys, json, hashlib, argparse, webbrowser
from collections import defaultdict
from datetime import datetime

PAPELERA = r"C:\Users\Admin\Seawolf_Papelera"
MANIFEST = os.path.join(PAPELERA, "_manifest.json")
SKIP_DIRS = {"$recycle.bin", "system volume information", "windows", "appdata",
             "node_modules", ".git", "__pycache__", "seawolf_papelera"}

# ---------------- utilidades ----------------
def human(n):
    n = float(n)
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024: return f"{n:.0f}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}PB"

def walk(root, skip=True, progress=None):
    for dp, dns, fns in os.walk(root):
        if skip:
            dns[:] = [d for d in dns if d.lower() not in SKIP_DIRS and not d.startswith(".")]
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                if os.path.isfile(p):
                    s = os.path.getsize(p)
                    if progress: progress()
                    yield p, s
            except OSError:
                continue

def _manifest():
    if os.path.exists(MANIFEST):
        try: return json.load(open(MANIFEST, encoding="utf-8"))
        except Exception: return []
    return []
def _save_manifest(m):
    os.makedirs(PAPELERA, exist_ok=True)
    json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------- funciones ----------------
def scan(root, top=30):
    files = list(walk(root)); files.sort(key=lambda x: -x[1])
    tot = sum(s for _, s in files)
    print(f"[Scan] {root}\n  {len(files)} archivos · {human(tot)} en total\n")
    print(f"  {'#':>3}  {'Tamano':>9}  Archivo")
    for i, (p, s) in enumerate(files[:top], 1):
        print(f"  {i:>3}  {human(s):>9}  {p}")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "optimizer-last-scan.json")
    json.dump({"root": root, "total": tot, "count": len(files),
               "top": [{"path": p, "size": s} for p, s in files[:top]]},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n[i] Reporte: {out}")
    return files

def find_dupes(root, min_mb=1):
    minsz = int(min_mb * 1024 * 1024)
    by_size = defaultdict(list)
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
        for _, ps in by_hash.items():
            if len(ps) > 1: groups.append({"size": s, "files": ps})
    groups.sort(key=lambda g: -g["size"] * (len(g["files"]) - 1))
    return groups

def dupes(root, min_mb=1):
    g = find_dupes(root, min_mb)
    waste = sum(x["size"] * (len(x["files"]) - 1) for x in g)
    print(f"[Duplicados] {root}\n  {len(g)} grupos · {human(waste)} desperdiciados\n")
    for i, x in enumerate(g, 1):
        print(f"  Grupo {i}  ({len(x['files'])} copias · {human(x['size'])} c/u · desperdicia {human(x['size']*(len(x['files'])-1))})")
        for p in x["files"]: print(f"      {p}")
    return g

def limpiar(paths, hard=False):
    import shutil
    os.makedirs(PAPELERA, exist_ok=True)
    m = _manifest(); done = []
    for p in paths:
        if not p or not os.path.isfile(p): continue
        try:
            if hard:
                os.remove(p)
                m.append({"accion": "borrado", "path": p, "fecha": datetime.now().isoformat(timespec="seconds")})
                done.append(p)
            else:
                base = os.path.basename(p); dst = os.path.join(PAPELERA, base)
                if os.path.exists(dst): dst = os.path.join(PAPELERA, f"{datetime.now():%H%M%S}_{base}")
                shutil.move(p, dst)
                m.append({"accion": "papelera", "archivo": os.path.basename(dst), "original": p,
                          "fecha": datetime.now().isoformat(timespec="seconds")})
                done.append(p)
        except OSError as e:
            print(f"  [x] {p}: {e}")
    _save_manifest(m)
    return done

def papeles():
    m = _manifest()
    if not m: print("[i] Papelera vacia."); return
    for i, e in enumerate(m, 1):
        print(f"  {i}. [{e['accion']}] {e.get('archivo') or e.get('path')}  ({e['fecha']})")

def rescatar(n):
    import shutil
    m = _manifest()
    if not (1 <= n <= len(m)): print("[!] Numero invalido."); return
    e = m[n - 1]
    if e["accion"] == "borrado": print("[!] Ese se borro. No hay rescate."); return
    src = os.path.join(PAPELERA, e["archivo"])
    if not os.path.exists(src): print("[!] No esta."); return
    os.makedirs(os.path.dirname(e["original"]), exist_ok=True)
    shutil.move(src, e["original"]); m.pop(n - 1); _save_manifest(m)
    print(f"[OK] RESCATADO -> {e['original']}")

# ---------------- APLICATIVO WEB ----------------
HTML = r"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seawolf Tools · Optimizacion</title>
<style>
:root{--sw:#4CE8E7;--sw2:#48E8D8;--ok:#48E8A0;--bad:#ff4d4d;--warn:#ffb86b;
--bg:#0b1414;--fg:#e6fbfb;--mut:#7fa8a8;--bd:#1e3434;--card:#101d1d}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:radial-gradient(1100px 560px at 50% -8%,#122b2b,#0b1414 58%,#070f0f);
 color:var(--fg);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{width:1180px;max-width:97vw;margin:0 auto;padding:16px 20px 40px}
h1{font-size:21px;margin:0}.b{color:var(--sw);text-shadow:0 0 14px rgba(76,232,231,.4)}
.sub{color:var(--mut);font-size:12.5px;margin:2px 0 14px}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.chip{border:1px solid var(--bd);border-radius:10px;padding:8px 12px;background:var(--card);font-size:12.5px}
.chip b{color:var(--sw);font-size:15px}
.tabs{display:flex;gap:6px;margin:6px 0 14px;flex-wrap:wrap}
.tab{border:1px solid var(--bd);background:transparent;color:var(--mut);padding:7px 13px;border-radius:8px;font:inherit;font-size:12.5px;cursor:pointer}
.tab.on{background:var(--sw);color:#04120f;border-color:var(--sw);font-weight:700}
.tools{display:flex;gap:8px;margin-bottom:10px;align-items:center}
input[type=search]{flex:1;padding:8px 10px;border-radius:8px;border:1px solid var(--bd);background:var(--card);color:var(--fg);font:inherit;font-size:13px}
.spin{width:14px;height:14px;border:2px solid var(--bd);border-top-color:var(--sw);border-radius:50%;display:inline-block;animation:sp .8s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{padding:7px 9px;border-bottom:1px solid var(--bd);text-align:left}
th{color:var(--sw);font-size:11px;text-transform:uppercase;letter-spacing:.4px;cursor:pointer;user-select:none}
tr:hover td{background:rgba(76,232,231,.05)}
.size{color:var(--sw);white-space:nowrap} .path{word-break:break-all;color:var(--mut)}
.ext{display:inline-block;min-width:34px;text-align:center;border:1px solid var(--bd);border-radius:5px;padding:1px 5px;font-size:10.5px;color:var(--sw)}
button{font:inherit;cursor:pointer;border-radius:7px;font-size:12px;padding:5px 10px;border:1px solid var(--bd);background:transparent;color:var(--fg)}
button.sw{background:var(--sw);color:#04120f;border-color:var(--sw);font-weight:600}
button.bad{border-color:var(--bad);color:var(--bad)}
button:hover{transform:translateY(-1px)}
.card{border:1px solid var(--bd);border-radius:11px;padding:12px 13px;background:var(--card);margin-bottom:10px}
.card h3{margin:0 0 6px;font-size:13.5px;color:var(--warn)}
.card .l{font-size:12.5px;display:flex;justify-content:space-between;gap:10px;align-items:center;padding:3px 0;border-bottom:1px dashed var(--bd)}
.toast{position:fixed;right:18px;bottom:18px;background:#04120f;border:1px solid var(--sw);color:var(--sw);
 border-radius:10px;padding:10px 14px;font-size:13px;opacity:0;transform:translateY(10px);transition:.25s;z-index:9}
.toast.on{opacity:1;transform:translateY(0)}
.empty{color:var(--mut);font-size:13px;padding:14px 0}
</style></head><body><div class="wrap">
<h1>SEAWOLF <span class="b">TOOLS</span> · Optimizacion de disco</h1>
<div class="sub">Ranking de pesados · Duplicados · Papelera reversible. Nada se borra sin tu orden.</div>
<div class="chips" id="chips"></div>
<div class="tabs">
<button class="tab on" data-t="heavy">🔥 Pesados</button>
<button class="tab" data-t="dupes">🧬 Duplicados</button>
<button class="tab" data-t="bin">🗑️ Papelera</button>
<button class="tab" id="rescan">↻ Re-escanear</button>
</div>
<div class="tools"><input type="search" id="q" placeholder="Filtrar por nombre o extensión…"><span id="stat" class="sub"></span></div>
<div id="view"></div></div>
<div class="toast" id="toast"></div>
<script>
var S={busy:true,heavy:[],dupes:[],bin:[],tab:'heavy',q:'',sort:'size',desc:true,scanned:0};
function H(t){document.getElementById('toast').textContent=t;var e=document.getElementById('toast');e.classList.add('on');setTimeout(function(){e.classList.remove('on')},1800);}
async function refrescar(){try{var r=await fetch('/api/state');var j=await r.json();Object.assign(S,j);draw();if(S.busy)setTimeout(refrescar,1200);}catch(e){}}
function draw(){
 document.getElementById('chips').innerHTML=
  '<div class="chip">Analizados <b>'+S.scanned+'</b></div>'+
  '<div class="chip">Total <b>'+(S.totalH||'—')+'</b></div>'+
  '<div class="chip">Raiz <b style="font-size:12px">'+(S.root||'')+'</b></div>'+
  '<div class="chip">Desperdicio <b style="color:var(--warn)">'+(S.wasteH||'—')+'</b></div>'+
  '<div class="chip">'+(S.busy?'<span class="spin"></span> analizando…':'✔ listo')+'</div>';
 document.getElementById('stat').textContent=S.tab==='heavy'?(S.heavy.length+' archivos'):(S.tab==='dupes'?(S.dupes.length+' grupos'):(S.bin.length+' en papelera'));
 var v=document.getElementById('view');var q=S.q.toLowerCase();
 if(S.tab==='heavy'){
  var a=S.heavy.filter(function(f){return !q||f.p.toLowerCase().indexOf(q)>=0;});
  a.sort(function(x,y){var k=S.sort;var r=(k==='name')?(x.p.localeCompare(y.p)):(x.size-y.size);return S.desc?-r:r;});
  var h='<table><thead><tr><th data-s="size">Tamaño</th><th data-s="name">Archivo</th><th></th></tr></thead><tbody>';
  a.slice(0,400).forEach(function(f){h+='<tr><td class="size">'+f.h+'</td><td><span class="ext">'+f.ext+'</span> <span class="path">'+f.p+'</span></td><td><button data-p="'+encodeURIComponent(f.p)+'">Mover</button></td></tr>';});
  v.innerHTML=h+'</tbody></table>';
 } else if(S.tab==='dupes'){
  if(!S.dupes.length){v.innerHTML='<div class="empty">Sin duplicados (o aún analizando…).</div>';return;}
  var h='';S.dupes.forEach(function(g,i){
   h+='<div class="card"><h3>Grupo '+(i+1)+' — '+g.files.length+' copias · '+g.h+' c/u · desperdicia '+g.wasteH+'</h3>';
   h+='<div style="margin-bottom:6px"><button class="sw" data-keep="'+i+'">Mover copias (dejar 1)</button></div>';
   g.files.forEach(function(p){h+='<div class="l"><span class="path">'+p+'</span><button data-p="'+encodeURIComponent(p)+'">Mover</button></div>';});
   h+='</div>';});
  v.innerHTML=h;
 } else {
  if(!S.bin.length){v.innerHTML='<div class="empty">Papelera vacía.</div>';return;}
  var h='<table><thead><tr><th>#</th><th>Archivo</th><th>Fecha</th><th></th></tr></thead><tbody>';
  S.bin.forEach(function(e,i){h+='<tr><td>'+(i+1)+'</td><td class="path">'+(e.archivo||e.path)+'</td><td class="path">'+e.fecha+'</td><td>'+(e.accion==='papelera'?'<button data-r="'+(i+1)+'">Rescatar</button>':'—')+'</td></tr>';});
  v.innerHTML=h+'</tbody></table>';
 }
 document.querySelectorAll('button[data-p]').forEach(function(b){b.onclick=async function(){
   if(!confirm('¿Mover a la Papelera Seawolf?\n'+decodeURIComponent(b.dataset.p)))return;
   await fetch('/mover',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({p:decodeURIComponent(b.dataset.p)})});
   b.textContent='✔';H('Movido a la papelera');refrescar();};});
 document.querySelectorAll('button[data-keep]').forEach(function(b){b.onclick=async function(){
   var g=S.dupes[+b.dataset.keep];if(!confirm('Mover '+(g.files.length-1)+' copias y dejar 1?'))return;
   await fetch('/mover-grupo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({files:g.files})});
   H('Copias movidas');refrescar();};});
 document.querySelectorAll('button[data-r]').forEach(function(b){b.onclick=async function(){
   await fetch('/rescatar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({n:+b.dataset.r})});
   H('Rescatado');refrescar();};});
 document.querySelectorAll('th[data-s]').forEach(function(th){th.onclick=function(){var s=th.dataset.s;if(S.sort===s)S.desc=!S.desc;else{S.sort=s;S.desc=true;}draw();};});
}
document.querySelectorAll('.tab[data-t]').forEach(function(t){t.onclick=function(){
 document.querySelectorAll('.tab[data-t]').forEach(function(x){x.classList.remove('on')});t.classList.add('on');S.tab=t.dataset.t;draw();};});
document.getElementById('rescan').onclick=async function(){S.busy=true;S.heavy=[];S.dupes=[];draw();await fetch('/rescan',{method:'POST'});refrescar();};
document.getElementById('q').oninput=function(e){S.q=e.target.value;draw();};
refrescar();
</script></body></html>"""

def serve(root, port):
    import http.server, socketserver, threading

    state = {"busy": True, "root": root, "scanned": 0, "heavy": [], "dupes": [],
             "total": 0, "waste": 0}

    def work():
        state["scanned"] = 0
        files = list(walk(root, progress=lambda: state.__setitem__("scanned", state["scanned"] + 1)))
        state["total"] = sum(s for _, s in files)
        files.sort(key=lambda x: -x[1])
        state["heavy"] = files  # se recorta al responder
        gs = find_dupes(root)
        state["waste"] = sum(g["size"] * (len(g["files"]) - 1) for g in gs)
        state["dupes"] = gs
        state["busy"] = False

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, body, ctype):
            self.send_response(200); self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        def _json(self, o): self._send(json.dumps(o).encode(), "application/json")
        def do_GET(self):
            if self.path.startswith("/api/state"):
                heavy = [{"p": p, "size": s, "h": human(s), "ext": (os.path.splitext(p)[1][1:9] or "—").upper()}
                         for p, s in state["heavy"][:300]]
                dupes = [{"h": human(g["size"]), "wasteH": human(g["size"] * (len(g["files"]) - 1)), "files": g["files"]}
                         for g in state["dupes"][:60]]
                self._json({"busy": state["busy"], "root": state["root"], "scanned": state["scanned"],
                            "totalH": human(state["total"]) if state["total"] else "—",
                            "wasteH": human(state["waste"]) if state["waste"] else "—",
                            "heavy": heavy, "dupes": dupes, "bin": _manifest()})
            else:
                self._send(HTML.encode(), "text/html; charset=utf-8")
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n) or b"{}")
            if self.path.startswith("/mover"): limpiar([d.get("p", "")])
            elif self.path.startswith("/mover-grupo"):
                fs = d.get("files", [])[1:]  # deja la primera
                limpiar(fs)
            elif self.path.startswith("/rescatar"): rescatar(int(d.get("n", 0)))
            elif self.path.startswith("/rescan"):
                state["busy"] = True; state["heavy"] = []; state["dupes"] = []
                threading.Thread(target=work, daemon=True).start()
            self._json({"ok": True})

    threading.Thread(target=work, daemon=True).start()
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), H) as srv:
        srv.allow_reuse_address = True
        print(f"[Seawolf Tools] Aplicativo en http://127.0.0.1:{port}  (Ctrl+C para salir)")
        try: webbrowser.open(f"http://127.0.0.1:{port}")
        except Exception: pass
        srv.serve_forever()

# ---------------- CLI ----------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Seawolf Tools - Optimizacion de disco")
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
