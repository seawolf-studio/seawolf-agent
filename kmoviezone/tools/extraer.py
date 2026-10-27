#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRAER — saca los videos de los .rar usando UnRAR (maneja contrasena).
Reemplaza la auto-extraccion de MiPony, que en esta maquina produce 0 bytes
y ADEMAS borra el .rar (perdida total).

Uso:
   python extraer.py "H:\\caida"                      (extrae todo lo que encuentre)
   python extraer.py "H:\\caida" --clave MiClave123
   python extraer.py "H:\\caida" --clave X --borrar    (borra el .rar si extrajo bien)
   python extraer.py --probar "ruta\\archivo.rar"      (solo lista el contenido)
"""
import os, sys, glob, subprocess

UNRAR = r"C:\Program Files\WinRAR\UnRAR.exe"
VIDEO = (".mkv", ".mp4", ".avi", ".mov", ".wmv", ".mpg", ".m4v", ".webm")

def unrar(args, timeout=3600):
    r = subprocess.run([UNRAR] + args, capture_output=True, text=True,
                       timeout=timeout, encoding="utf-8", errors="ignore")
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def probar(rar, clave=None):
    args = ["l"]
    if clave: args.append(f"-p{clave}")
    rc, out = unrar(args, timeout=300)
    print(f"\n--- {os.path.basename(rar)} (rc={rc}) ---")
    for l in out.splitlines()[:25]:
        if l.strip(): print("   ", l[:110])
    return rc, out

def extraer_uno(rar, clave=None, borrar=False):
    carpeta = os.path.dirname(rar)
    args = ["x", "-y", "-o+"]          # extrae, sobrescribe sin preguntar
    if clave: args.append(f"-p{clave}")
    args += [rar, carpeta + os.sep]
    try:
        rc, out = unrar(args)
    except Exception as e:
        print(f"  !! {os.path.basename(rar)}: FALLO {type(e).__name__} {e}")
        return False
    errores = [l for l in out.splitlines() if "ERROR" in l.upper() or "FALLO" in l.upper()]
    if rc == 0 and not errores:
        print(f"  ✔ extraido: {os.path.basename(rar)}")
        if borrar:
            try: os.remove(rar); print("     (y borrado el .rar)")
            except Exception as e: print("     (no pude borrar el .rar:", e, ")")
        return True
    print(f"  ✘ {os.path.basename(rar)} — rc={rc}")
    for l in (errores or out.splitlines())[:6]: print("      ", l[:110])
    if "password" in out.lower() or "contrasena" in out.lower() or rc == 11:
        print("      >>> parece que la CONTRASENA esta mal o falta. Pruebe con --clave")
    return False

def main():
    a = sys.argv[1:]
    clave = None; borrar = False
    if "--clave" in a: i = a.index("--clave"); clave = a[i+1]; del a[i:i+2]
    if "--borrar" in a: borrar = True; a.remove("--borrar")
    if "--probar" in a:
        i = a.index("--probar"); probar(a[i+1], clave); return
    carpeta = a[0] if a else r"H:\caida"
    rars = sorted(glob.glob(os.path.join(carpeta, "*.rar")) + glob.glob(os.path.join(carpeta, "*.part1")))
    rars = [r for r in rars if not r.endswith(".part1")]     # los .part1 son trozos, no el principal
    if not rars:
        print(f"no hay .rar en {carpeta}"); return
    print(f"EXTRAER — {len(rars)} archivo(s) en {carpeta}")
    if clave: print(f"  con contrasena ({len(clave)} caracteres)")
    ok = 0
    for r in rars:
        if extraer_uno(r, clave, borrar): ok += 1
    print(f"\n  RESULTADO: {ok} de {len(rars)} extraidos")
    videos = [f for f in os.listdir(carpeta) if f.lower().endswith(VIDEO)]
    print(f"  videos ahora en la carpeta: {len(videos)}")
    for v in sorted(videos)[-6:]:
        print(f"     {os.path.getsize(os.path.join(carpeta,v))/1e6:>9.1f} MB  {v[:70]}")

if __name__ == "__main__":
    main()
