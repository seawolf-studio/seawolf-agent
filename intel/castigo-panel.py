#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CASTOR DEL PANEL DE MANDO — castigo por ausencias (3).
Mueve 1 archivo ALEATORIO de tu ZONA DE SACRIFICIO al TRASTERO.
NO borra: mueve. Es recuperable con --rescatar.

  python castigo-panel.py              -> SIMULACRO (muestra que moveria, no toca nada)
  python castigo-panel.py --ejecutar   -> ejecuta el castigo (mueve 1 archivo)
  python castigo-panel.py --listar     -> lista lo que hay en el Trastero
  python castigo-panel.py --rescatar 3 -> devuelve el archivo #3 del Trastero

BLINDAJE: solo opera dentro de estas 2 carpetas. Jamas toca nada fuera de ellas.
Elaborado por Bellion para el Monarca.
"""
import os, sys, random, shutil, json, datetime

SACRIFICIO = r"C:\Users\Admin\Seawolf_Sacrificio"
TRASTERO   = r"C:\Users\Admin\Seawolf_Trastero"
MANIFEST   = os.path.join(TRASTERO, "_trastero.json")

def ensure_dirs():
    os.makedirs(SACRIFICIO, exist_ok=True)
    os.makedirs(TRASTERO, exist_ok=True)

def candidates():
    """Archivos (no carpetas) en la Zona de Sacrificio, excluyendo ocultos/sistema."""
    out = []
    for n in os.listdir(SACRIFICIO):
        p = os.path.join(SACRIFICIO, n)
        if os.path.isfile(p) and not n.startswith((".","_")):
            out.append(p)
    return out

def load_manifest():
    if os.path.exists(MANIFEST):
        try: return json.load(open(MANIFEST, encoding="utf-8"))
        except Exception: return []
    return []
def save_manifest(m):
    json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def ejecutar(real=True):
    ensure_dirs()
    cs = candidates()
    if not cs:
        print(f"[!] La Zona de Sacrificio esta VACIA: {SACRIFICIO}")
        print("    Llenala con cosas que aceptas perder (descargas, juegos, archivos sueltos).")
        print("    Nada critico. Solo la comodidad, no tus activos.")
        return
    pick = random.choice(cs)
    dst  = os.path.join(TRASTERO, os.path.basename(pick))
    if real:
        if os.path.exists(dst):
            base, ext = os.path.splitext(os.path.basename(pick))
            dst = os.path.join(TRASTERO, f"{base}_{datetime.datetime.now():%Y%m%d_%H%M%S}{ext}")
        shutil.move(pick, dst)
        m = load_manifest()
        m.append({"archivo": os.path.basename(dst), "original": pick, "fecha": datetime.datetime.now().isoformat(timespec="seconds")})
        save_manifest(m)
        print(f"[X] CASTIGO EJECUTADO -> {os.path.basename(dst)}")
        print(f"    Movido al Trastero. Recuperable: python castigo-panel.py --rescatar {len(m)}")
    else:
        print(f"[i] SIMULACRO: se moveria -> {os.path.basename(pick)}")
        print(f"    ({len(cs)} archivos en tu Zona de Sacrificio)")

def listar():
    m = load_manifest()
    if not m: print("[i] Trastero vacio."); return
    print(f"[Trastero] {len(m)} archivo(s):")
    for i, e in enumerate(m, 1):
        print(f"  {i}. {e['archivo']}   ({e['fecha']})")

def rescatar(n):
    m = load_manifest()
    if not (1 <= n <= len(m)): print("[!] Numero invalido."); return
    e = m[n-1]; src = os.path.join(TRASTERO, e["archivo"])
    dst = e["original"]
    if not os.path.exists(src): print("[!] No esta en el Trastero."); return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    m.pop(n-1); save_manifest(m)
    print(f"[✔] RESCATADO -> {dst}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--ejecutar" in a: ejecutar(True)
    elif "--listar" in a: listar()
    elif "--rescatar" in a:
        try: rescatar(int(a[a.index("--rescatar")+1]))
        except Exception: print("Uso: --rescatar N")
    else:
        ejecutar(False)
        print("\n[i] Modo simulacro. Para ejecutar de verdad: --ejecutar")
