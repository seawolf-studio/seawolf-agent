#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CASTOR DEL PANEL DE MANDO v2 — saqueo aleatorio por CARPETAS.
El sistema (no tú) elige. Configuras las CARPETAS de riesgo; el castigo saca
1 archivo AL AZAR de ahí. Dos modos:
   trastero (def.) -> mueve al Trastero (reversible, con dias_bloqueo)
   borrar          -> BORRADO PERMANENTE (irreversible, sin red)

Comandos:
  python castigo-panel.py               -> SIMULACRO
  python castigo-panel.py --ejecutar    -> ejecuta el castigo
  python castigo-panel.py --zonas       -> muestra carpetas y cuántos archivos tienen
  python castigo-panel.py --listar      -> qué hay en el Trastero
  python castigo-panel.py --rescatar N  -> devuelve el archivo N (solo si pasó el bloqueo)
  python castigo-panel.py --modo borrar -> cambia de modo

CONFIG: castigo-config.json (junto a este script).
BLINDAJE: jamas toca nada fuera de las carpetas configuradas.
Elaborado por Bellion para el Monarca.
"""
import os, sys, random, shutil, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "castigo-config.json")
TRASTERO = r"C:\Users\Admin\Seawolf_Trastero"
MANIFEST = os.path.join(TRASTERO, "_trastero.json")

DEF = {"zonas": [], "modo": "trastero", "dias_bloqueo": 7}

def cfg():
    if os.path.exists(CONFIG):
        try:
            c = json.load(open(CONFIG, encoding="utf-8"))
            for k, v in DEF.items(): c.setdefault(k, v)
            return c
        except Exception: return dict(DEF)
    json.dump(DEF, open(CONFIG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return dict(DEF)
def save_cfg(c): json.dump(c, open(CONFIG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def files_in(zona):
    out = []
    if not os.path.isdir(zona): return out
    for root, dirs, fs in os.walk(zona):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
        for n in fs:
            if n.startswith((".", "_")) or n.lower() in ("desktop.ini", "thumbs.db"): continue
            out.append(os.path.join(root, n))
    return out

def gather(c):
    zones = [z for z in c["zonas"] if os.path.isdir(z)]
    pool = []
    for z in zones:
        for f in files_in(z):
            if os.path.abspath(f).lower().startswith(os.path.abspath(z).lower()+os.sep.lower()):
                pool.append(f)
    return zones, pool

def manifest():
    if os.path.exists(MANIFEST):
        try: return json.load(open(MANIFEST, encoding="utf-8"))
        except Exception: return []
    return []
def save_manifest(m): json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def ejecutar(real):
    c = cfg(); os.makedirs(TRASTERO, exist_ok=True)
    zones, pool = gather(c)
    if not c["zonas"]:
        print("[!] No hay CARPETAS configuradas. Edita castigo-config.json:")
        print('    {"zonas": ["C:\\\\Users\\\\Admin\\\\Downloads"], "modo": "trastero", "dias_bloqueo": 7}')
        return
    if not zones:
        print("[!] Ninguna carpeta configurada existe. Revisa castigo-config.json."); return
    if not pool:
        print("[!] Las carpetas estan vacias. Nada que saquear."); return
    pick = random.choice(pool)
    modo = c["modo"]
    if not real:
        print(f"[i] SIMULACRO ({modo}): se tomaria -> {pick}")
        print(f"    ({len(pool)} archivos en {len(zones)} carpeta(s))")
        return
    if modo == "borrar":
        os.remove(pick)
        print(f"[X] BORRADO PERMANENTE -> {pick}  (sin vuelta atras)")
        m = manifest(); m.append({"accion":"borrado","archivo":os.path.basename(pick),"original":pick,"fecha":datetime.datetime.now().isoformat(timespec="seconds")}); save_manifest(m)
    else:
        base = os.path.basename(pick); dst = os.path.join(TRASTERO, base)
        if os.path.exists(dst):
            b, e = os.path.splitext(base); dst = os.path.join(TRASTERO, f"{b}_{datetime.datetime.now():%Y%m%d_%H%M%S}{e}")
        shutil.move(pick, dst)
        hasta = (datetime.datetime.now()+datetime.timedelta(days=int(c["dias_bloqueo"]))).isoformat(timespec="seconds")
        m = manifest(); m.append({"accion":"trastero","archivo":os.path.basename(dst),"original":pick,"fecha":datetime.datetime.now().isoformat(timespec="seconds"),"liberar_hasta":hasta}); save_manifest(m)
        print(f"[X] CASTIGO -> {os.path.basename(dst)}  (en Trastero)")
        print(f"    Bloqueado {c['dias_bloqueo']} dias. Rescate: python castigo-panel.py --rescatar {len(m)}")

def listar():
    m = manifest()
    if not m: print("[i] Trastero vacio."); return
    print(f"[Trastero] {len(m)} registro(s):")
    for i, e in enumerate(m, 1):
        extra = "" if e.get("accion")=="borrado" else f"  (libera {e.get('liberar_hasta','?')})"
        print(f"  {i}. [{e.get('accion','?')}] {e['archivo']}{extra}")

def rescatar(n, forzar=False):
    m = manifest()
    if not (1 <= n <= len(m)): print("[!] Numero invalido."); return
    e = m[n-1]
    if e.get("accion")=="borrado": print("[!] Ese fue BORRADO permanente. No hay rescate."); return
    if not forzar and e.get("liberar_hasta"):
        try:
            if datetime.datetime.now() < datetime.datetime.fromisoformat(e["liberar_hasta"]):
                print(f"[!] TRABA anti-trampa: bloqueado hasta {e['liberar_hasta']}."); return
        except Exception: pass
    src = os.path.join(TRASTERO, e["archivo"]); dst = e["original"]
    if not os.path.exists(src): print("[!] No esta en el Trastero."); return
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.move(src, dst); m.pop(n-1); save_manifest(m)
    print(f"[OK] RESCATADO -> {dst}")

if __name__ == "__main__":
    a = sys.argv[1:]
    c = cfg()
    if "--zonas" in a:
        for z in c["zonas"]:
            print(f"  {z}  ->  {len(files_in(z))} archivos" + ("" if os.path.isdir(z) else "  [NO EXISTE]"))
        if not c["zonas"]: print("  (sin carpetas configuradas)")
        print(f"  modo actual: {c['modo']} · bloqueo: {c['dias_bloqueo']} dias")
    elif "--modo" in a:
        c["modo"] = a[a.index("--modo")+1]; save_cfg(c); print(f"[i] modo = {c['modo']}")
    elif "--ejecutar" in a: ejecutar(True)
    elif "--listar" in a: listar()
    elif "--rescatar" in a:
        try: rescatar(int(a[a.index("--rescatar")+1]), "--forzar" in a)
        except Exception: print("Uso: --rescatar N [--forzar]")
    else:
        ejecutar(False); print("\n[i] Simulacro. Ejecutar de verdad: --ejecutar")
