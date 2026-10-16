#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SEAWOLF TOOLS — Optimizacion de disco (v3: MULTI-DISCO + UI pulida)
Escanea TODOS los discos o los que elijas. Ranking de pesados + duplicados +
papelera reversible + aplicativo web.

  python seawolf-tools.py drives
  python seawolf-tools.py scan  ALL [--top 30]        # o "C:,D,E:"
  python seawolf-tools.py dupes ALL [--min 1]
  python seawolf-tools.py limpiar --paths "a","b" [--hard] / papeles / rescatar N
  python seawolf-tools.py serve ALL [--port 8770]     # APLICATIVO WEB

Seguridad: mueve a la Papelera Seawolf (reversible); --hard borra de verdad.
Codigo propio. Elaborado por Bellion para el Monarca (Key).
"""
import os, sys, json, hashlib, argparse, webbrowser, string, shutil, heapq
from collections import defaultdict
from datetime import datetime

PAPELERA = r"C:\Users\Admin\Seawolf_Papelera"
MANIFEST = os.path.join(PAPELERA, "_manifest.json")
SKIP_DIRS = {"$recycle.bin", "system volume information", "windows", "winsxs", "appdata",
             "node_modules", ".git", "__pycache__", "seawolf_papelera", "$windows.~bt"}

def human(n):
    n = float(n)
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024: return f"{n:.0f}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}PB"

def list_drives():
    out = []
    for L in string.ascii_uppercase:
        root = f"{L}:\\"
        if os.path.exists(root):
            try:
                t, u, f = shutil.disk_usage(root)
                out.append({"root": root, "total": t, "used": u, "free": f})
            except OSError:
                pass
    return out

def parse_targets(arg):
    raw = (arg or "ALL").strip()
    if raw.upper() in ("ALL", "TODOS", "*", ""):
        return [d["root"] for d in list_drives()]
    roots = []
    for part in raw.split(","):
        p = part.strip()
        if not p: continue
        if len(p) == 1: p = p + ":\\"
        elif p.endswith(":") and not p.endswith(":\\"): p = p + "\\"
        roots.append(p)
    return roots

def walk_multi(roots, progress=None):
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d.lower() not in SKIP_DIRS and not d.startswith(".")]
            for fn in fns:
                p = os.path.join(dp, fn)
                try:
                    if os.path.isfile(p):
                        s = os.path.getsize(p)
                        if progress: progress(root, s)
                        yield p, s, root
                except OSError:
                    continue

def scan(targets, top=30):
    heap = []; per = defaultdict(lambda: [0, 0])
    for p, s, root in walk_multi(targets):
        per[root][0] += 1; per[root][1] += s
        if len(heap) < top * 4: heapq.heappush(heap, (s, p))
        elif s > heap[0][0]: heapq.heapreplace(heap, (s, p))
    topf = sorted(heap, reverse=True)[:top]
    tot = sum(v[1] for v in per.values())
    print(f"[Scan] {len(targets)} disco(s)\n")
    for r, v in per.items(): print(f"  {r}  {v[0]} archivos · {human(v[1])}")
    print(f"\n  TOTAL: {sum(v[0] for v in per.values())} archivos · {human(tot)}\n")
    print(f"  {'#':>3}  {'Tamano':>9}  Archivo")
    for i, (s, p) in enumerate(topf, 1): print(f"  {i:>3}  {human(s):>9}  {p}")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "optimizer-last-scan.json")
    json.dump({"roots": targets, "total": tot, "top": [{"path": p, "size": s} for s, p in topf]},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n[i] Reporte: {out}")
    return topf

def find_dupes(targets, min_mb=1):
    minsz = int(min_mb * 1024 * 1024)
    by_size = defaultdict(list)
    for p, s, _ in walk_multi(targets):
        if s >= minsz: by_size[s].append(p)
    groups = []
    for s, paths in by_size.items():
        if len(paths) < 2: continue
        bh = defaultdict(list)
        for p in paths:
            try:
                h = hashlib.blake2b(digest_size=16)
                with open(p, "rb") as f: h.update(f.read(262144))
                bh[h.hexdigest()].append(p)
            except OSError:
                continue
        for _, ps in bh.items():
            if len(ps) > 1: groups.append({"size": s, "files": ps})
    groups.sort(key=lambda g: -g["size"] * (len(g["files"]) - 1))
    return groups

def dupes(targets, min_mb=1):
    g = find_dupes(targets, min_mb)
    waste = sum(x["size"] * (len(x["files"]) - 1) for x in g)
    print(f"[Duplicados] {len(targets)} disco(s)\n  {len(g)} grupos · {human(waste)} desperdiciados\n")
    for i, x in enumerate(g, 1):
        print(f"  Grupo {i} ({len(x['files'])} copias · {human(x['size'])} c/u · desperdicia {human(x['size']*(len(x['files'])-1))})")
        for p in x["files"]: print(f"      {p}")
    return g

def _manifest():
    if os.path.exists(MANIFEST):
        try: return json.load(open(MANIFEST, encoding="utf-8"))
        except Exception: return []
    return []
def _save_manifest(m):
    os.makedirs(PAPELERA, exist_ok=True)
    json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def limpiar(paths, hard=False):
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
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Seawolf Tools · Optimizacion</title>
<style>
:root{--sw:#4CE8E7;--sw2:#48E8D8;--ok:#48E8A0;--bad:#ff4d4d;--warn:#ffb86b;--bd:#1e3434;--fg:#e6fbfb;--mut:#7fa8a8;--card:#101d1d}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:radial-gradient(1100px 560px at 50% -8%,#122b2b,#0b1414 58%,#070f0f);color:var(--fg);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{width:1220px;max-width:97vw;margin:0 auto;padding:16px 20px 40px}
h1{font-size:21px;margin:0}.b{color:var(--sw);text-shadow:0 0 14px rgba(76,232,231,.4)}
.sub{color:var(--mut);font-size:12.5px;margin:2px 0 14px}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.chip{border:1px solid var(--bd);border-radius:10px;padding:8px 12px;background:var(--card);font-size:12.5px}
.chip b{color:var(--sw);font-size:15px}
.drives{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.drv{border:1px solid var(--bd);border-radius:9px;padding:6px 10px;background:var(--card);font-size:12px;min-width:150px}
.drv .bar{height:6px;border-radius:4px;background:#0a1f1f;margin-top:5px;overflow:hidden}
.drv .bar i{display:block;height:100%;background:linear-gradient(90deg,var(--sw2),var(--sw))}
.tabs{display:flex;gap:6px;margin:6px 0 12px;flex-wrap:wrap}
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
.size{color:var(--sw);white-space:nowrap}.path{word-break:break-all;color:var(--mut)}
.dv{color:var(--sw2)}
.ext{display:inline-block;min-width:34px;text-align:center;border:1px solid var(--bd);border-radius:5px;padding:1px 5px;font-size:10.5px;color:var(--sw)}
button{font:inherit;cursor:pointer;border-radius:7px;font-size:12px;padding:5px 10px;border:1px solid var(--bd);background:transparent;color:var(--fg)}
button.sw{background:var(--sw);color:#04120f;border-color:var(--sw);font-weight:600}
button.bad{border-color:var(--bad);color:var(--bad)}
.card{border:1px solid var(--bd);border-radius:11px;padding:12px 13px;background:var(--card);margin-bottom:10px}
.card h3{margin:0 0 6px;font-size:13.5px;color:var(--warn)}
.card .l{font-size:12.5px;display:flex;justify-content:space-between;gap:10px;align-items:center;padding:3px 0;border-bottom:1px dashed var(--bd)}
.toast{position:fixed;right:18px;bottom:18px;background:#04120f;border:1px solid var(--sw);color:var(--sw);border-radius:10px;padding:10px 14px;font-size:13px;opacity:0;transform:translateY(10px);transition:.25s;z-index:9}
.toast.on{opacity:1;transform:translateY(0)}.empty{color:var(--mut);font-size:13px;padding:14px 0}
</style></head><body><div class="wrap">
<h1>SEAWOLF <span class="b">TOOLS</span> · Optimizacion (multi-disco)</h1>
<div class="sub">Escanea todos los discos o los que elijas · Pesados · Duplicados · Papelera reversible. Nada se borra sin tu orden.</div>
<div class="chips" id="chips"></div><div class="drives" id="drives"></div>
<div class="tabs">
<button class="tab on" data-t="heavy">🔥 Pesados</button>
<button class="tab" data-t="dupes">🧬 Duplicados</button>
<button class="tab" data-t="bin">🗑️ Papelera</button>
<button class="tab" id="rescan">↻ Re-escanear</button></div>
<div class="tools"><input type="search" id="q" placeholder="Filtrar por nombre, extensión o disco…"><span id="stat" class="sub"></span></div>
<div id="view"></div></div><div class="toast" id="toast"></div>
<script>
var S={busy:true,heavy:[],dupes:[],bin:[],drives:[],tab:'heavy',q:'',sort:'size',desc:true,scanned:0};
function H(t){var e=document.getElementById('toast');e.textContent=t;e.classList.add('on');setTimeout(function(){e.classList.remove('on')},1800);}
async function refrescar(){try{var r=await fetch('/api/state');var j=await r.json();Object.assign(S,j);draw();if(S.busy)setTimeout(refrescar,1200);}catch(e){}}
function draw(){
 document.getElementById('chips').innerHTML=
  '<div class="chip">Analizados <b>'+S.scanned+'</b></div>'+
  '<div class="chip">Total <b>'+(S.totalH||'—')+'</b></div>'+
  '<div class="chip">Desperdicio <b style="color:var(--warn)">'+(S.wasteH||'—')+'</b></div>'+
  '<div class="chip">'+(S.busy?'<span class="spin"></span> analizando…':'✔ listo')+'</div>';
 document.getElementById('drives').innerHTML=S.drives.map(function(d){
  var pct=d.total?Math.round(100*d.used/d.total):0;
  return '<div class="drv"><b class="dv">'+d.root+'</b> '+d.scannedS+' de '+d.totalH+' · libre '+d.freeH+'<div class="bar"><i style="width:'+pct+'%"></i></div></div>';}).join('');
 document.getElementById('stat').textContent=S.tab==='heavy'?(S.heavy.length+' archivos'):(S.tab==='dupes'?(S.dupes.length+' grupos'):(S.bin.length+' en papelera'));
 var v=document.getElementById('view'),q=S.q.toLowerCase();
 if(S.tab==='heavy'){
  var a=S.heavy.filter(function(f){return !q||f.p.toLowerCase().indexOf(q)>=0;});
  a.sort(function(x,y){var k=S.sort,r=(k==='name')?x.p.localeCompare(y.p):(x.size-y.size);return S.desc?-r:r;});
  var h='<table><thead><tr><th data-s="size">Tamaño</th><th>Disco</th><th data-s="name">Archivo</th><th></th></tr></thead><tbody>';
  a.slice(0,400).forEach(function(f){h+='<tr><td class="size">'+f.h+'</td><td class="dv">'+f.drv+'</td><td><span class="ext">'+f.ext+'</span> <span class="path">'+f.p+'</span></td><td><button data-p="'+encodeURIComponent(f.p)+'">Mover</button></td></tr>';});
  v.innerHTML=h+'</tbody></table>';
 } else if(S.tab==='dupes'){
  if(!S.dupes.length){v.innerHTML='<div class="empty">Sin duplicados (o aún analizando…).</div>';return;}
  var h='';S.dupes.forEach(function(g,i){h+='<div class="card"><h3>Grupo '+(i+1)+' — '+g.files.length+' copias · '+g.h+' c/u · desperdicia '+g.wasteH+'</h3>';
   h+='<div style="margin-bottom:6px"><button class="sw" data-keep="'+i+'">Mover copias (dejar 1)</button></div>';
   g.files.forEach(function(p){h+='<div class="l"><span class="path">'+p+'</span><button data-p="'+encodeURIComponent(p)+'">Mover</button></div>';});h+='</div>';});
  v.innerHTML=h;
 } else {
  if(!S.bin.length){v.innerHTML='<div class="empty">Papelera vacía.</div>';return;}
  var h='<table><thead><tr><th>#</th><th>Archivo</th><th>Fecha</th><th></th></tr></thead><tbody>';
  S.bin.forEach(function(e,i){h+='<tr><td>'+(i+1)+'</td><td class="path">'+(e.archivo||e.path)+'</td><td class="path">'+e.fecha+'</td><td>'+(e.accion==='papelera'?'<button data-r="'+(i+1)+'">Rescatar</button>':'—')+'</td></tr>';});
  v.innerHTML=h+'</tbody></table>';}
 document.querySelectorAll('button[data-p]').forEach(function(b){b.onclick=async function(){if(!confirm('¿Mover a la Papelera Seawolf?\n'+decodeURIComponent(b.dataset.p)))return;await fetch('/mover',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({p:decodeURIComponent(b.dataset.p)})});b.textContent='✔';H('Movido');refrescar();};});
 document.querySelectorAll('button[data-keep]').forEach(function(b){b.onclick=async function(){var g=S.dupes[+b.dataset.keep];if(!confirm('Mover '+(g.files.length-1)+' copias y dejar 1?'))return;await fetch('/mover-grupo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({files:g.files})});H('Copias movidas');refrescar();};});
 document.querySelectorAll('button[data-r]').forEach(function(b){b.onclick=async function(){await fetch('/rescatar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({n:+b.dataset.r})});H('Rescatado');refrescar();};});
 document.querySelectorAll('th[data-s]').forEach(function(th){th.onclick=function(){var s=th.dataset.s;if(S.sort===s)S.desc=!S.desc;else{S.sort=s;S.desc=true;}draw();};});
}
document.querySelectorAll('.tab[data-t]').forEach(function(t){t.onclick=function(){document.querySelectorAll('.tab[data-t]').forEach(function(x){x.classList.remove('on')});t.classList.add('on');S.tab=t.dataset.t;draw();};});
document.getElementById('rescan').onclick=async function(){S.busy=true;S.heavy=[];S.dupes=[];draw();await fetch('/rescan',{method:'POST'});refrescar();};
document.getElementById('q').oninput=function(e){S.q=e.target.value;draw();};
refrescar();
</script></body></html>"""

def serve(targets, port):
    import http.server, socketserver, threading
    state = {"busy": True, "targets": targets, "scanned": 0, "heavy": [], "dupes": [],
             "total": 0, "waste": 0, "drives": {}}
    def work():
        state["scanned"] = 0; state["drives"] = {r: {"n": 0, "b": 0} for r in targets}
        heap = []
        def prog(root, s):
            state["scanned"] += 1
            d = state["drives"].setdefault(root, {"n": 0, "b": 0}); d["n"] += 1; d["b"] += s
        for p, s, root in walk_multi(targets, progress=prog):
            if len(heap) < 1200: heapq.heappush(heap, (s, p))
            elif s > heap[0][0]: heapq.heapreplace(heap, (s, p))
        state["total"] = sum(v["b"] for v in state["drives"].values())
        state["heavy"] = sorted(heap, reverse=True)
        gs = find_dupes(targets)
        state["waste"] = sum(g["size"] * (len(g["files"]) - 1) for g in gs)
        state["dupes"] = gs
        state["busy"] = False
    def drives_info():
        out = []
        for r, v in state["drives"].items():
            try: t, u, f = shutil.disk_usage(r)
            except OSError: t = u = f = 0
            out.append({"root": r, "scannedS": human(v["b"]), "n": v["n"],
                        "totalH": human(t), "freeH": human(f), "total": t, "used": u})
        return out
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, b, ct): self.send_response(200); self.send_header("Content-Type", ct); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def _json(self, o): self._send(json.dumps(o).encode(), "application/json")
        def do_GET(self):
            if self.path.startswith("/api/state"):
                heavy = [{"p": p, "size": s, "h": human(s), "drv": (p[:2] if len(p) > 1 and p[1] == ":" else ""),
                          "ext": (os.path.splitext(p)[1][1:9] or "—").upper()} for s, p in state["heavy"][:300]]
                dupes = [{"h": human(g["size"]), "wasteH": human(g["size"] * (len(g["files"]) - 1)), "files": g["files"]} for g in state["dupes"][:60]]
                self._json({"busy": state["busy"], "scanned": state["scanned"],
                            "totalH": human(state["total"]) if state["total"] else "—",
                            "wasteH": human(state["waste"]) if state["waste"] else "—",
                            "drives": drives_info(), "heavy": heavy, "dupes": dupes, "bin": _manifest()})
            else:
                self._send(HTML.encode(), "text/html; charset=utf-8")
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0)); d = json.loads(self.rfile.read(n) or b"{}")
            if self.path.startswith("/mover-grupo"): limpiar(d.get("files", [])[1:])
            elif self.path.startswith("/mover"): limpiar([d.get("p", "")])
            elif self.path.startswith("/rescatar"): rescatar(int(d.get("n", 0)))
            elif self.path.startswith("/rescan"):
                state["busy"] = True; state["heavy"] = []; state["dupes"] = []
                threading.Thread(target=work, daemon=True).start()
            self._json({"ok": True})
    threading.Thread(target=work, daemon=True).start()
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), H) as srv:
        srv.allow_reuse_address = True
        print(f"[Seawolf Tools] http://127.0.0.1:{port}  · discos: {', '.join(targets)}  (Ctrl+C salir)")
        try: webbrowser.open(f"http://127.0.0.1:{port}")
        except Exception: pass
        srv.serve_forever()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Seawolf Tools - Optimizacion de disco (multi-disco)")
    ap.add_argument("cmd", choices=["drives", "scan", "dupes", "papeles", "rescatar", "limpiar", "serve"])
    ap.add_argument("arg", nargs="?", default="ALL")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--min", type=float, default=1)
    ap.add_argument("--port", type=int, default=8770)
    ap.add_argument("--paths", default="")
    ap.add_argument("--hard", action="store_true")
    a = ap.parse_args()
    if a.cmd == "drives":
        for d in list_drives(): print(f"  {d['root']}  total {human(d['total'])} · usado {human(d['used'])} · libre {human(d['free'])}")
    elif a.cmd == "scan": scan(parse_targets(a.arg), a.top)
    elif a.cmd == "dupes": dupes(parse_targets(a.arg), a.min)
    elif a.cmd == "papeles": papeles()
    elif a.cmd == "rescatar": rescatar(int(a.arg) if a.arg.isdigit() else 0)
    elif a.cmd == "limpiar": limpiar([p for p in a.paths.split(",") if p], a.hard)
    elif a.cmd == "serve": serve(parse_targets(a.arg), a.port)
