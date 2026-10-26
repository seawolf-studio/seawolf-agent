#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUBIR — subida CIFRADA (FTPS/TLS) al hosting. Fuente unica de credenciales.
Lee ftp-config.json (archivo local, fuera de los scripts).

   python subir.py                 -> sube index.html + datos.json + logo.png
   python subir.py <archivo...>    -> sube los archivos indicados
   python subir.py --bajar         -> BAJA el sitio actual a backups-sitio/
   python subir.py --lista         -> lista el contenido remoto
"""
import os, sys, json, datetime
from ftplib import FTP_TLS, FTP

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(BASE, "ftp-config.json")
SITIO = ["index.html", "datos.json", "logo.png"]

def conexion():
    c = json.load(open(CFG, encoding="utf-8"))
    if c.get("tls", True):
        f = FTP_TLS(timeout=45); f.connect(c["host"], int(c.get("port", 21)))
        f.auth(); f.login(c["user"], c["pass"]); f.prot_p()   # cifra datos Y canal
        print("conectado (FTPS — cifrado)")
    else:
        f = FTP(timeout=45); f.connect(c["host"], int(c.get("port", 21)))
        f.login(c["user"], c["pass"])
        print("conectado (FTP plano — SIN cifrar)")
    d = c.get("dir", "/")
    f.cwd(d)
    print("  directorio:", f.pwd())
    return f

def subir(archivos):
    f = conexion(); ok = []
    for a in archivos:
        p = os.path.join(BASE, a)
        if not os.path.exists(p): print("  !! falta local:", a); continue
        with open(p, "rb") as fh:
            f.storbinary("STOR " + a, fh)
        print(f"  subido: {a} ({os.path.getsize(p)} b)")
        ok.append(a)
    f.quit()
    return ok

def bajar():
    f = conexion()
    dest = os.path.join(BASE, "backups-sitio", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(dest, exist_ok=True)
    nombres = f.nlst()
    print("  contenido remoto:", nombres)
    for n in nombres:
        if n in (".", ".."): continue
        base = os.path.basename(n)
        try:
            with open(os.path.join(dest, base), "wb") as fh:
                f.retrbinary("RETR " + base, fh.write)
            print("  bajado:", base, os.path.getsize(os.path.join(dest, base)), "b")
        except Exception as e:
            print("  (saltado)", base, e)
    f.quit()
    print("respaldo del sitio en:", dest)
    return dest

def lista():
    f = conexion()
    ls = []; f.retrlines("LIST", ls.append)
    for l in ls: print("   ", l)
    f.quit()

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: subir(SITIO)
    elif a[0] == "--bajar": bajar()
    elif a[0] == "--lista": lista()
    else: subir(a)
