#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTACCESS-CACHE — pone cabeceras anti-cache para datos.json e index.html en el
servidor (Hostinger/Apache), sin pisar lo que ya exista.

Seguro por diseno:
  1. descarga el .htaccess actual (si existe) y lo respalda
  2. ANEXA nuestro bloque (no reemplaza)
  3. sube el resultado
  4. pide verificar la web (esa comprobacion se hace aparte, con curl)

Uso:  python htaccess-cache.py  [--revertir]
"""
import os, sys, re, datetime
from subir import conexion, BASE

BLOQUE = """
# ==== kmoviezone: sin cache para el contenido dinamico (2026-10-25) ====
# Anadido por Bellion. Los titulos nuevos deben verse al instante.
<IfModule mod_headers.c>
  <FilesMatch "\\.(html|json)$">
    Header set Cache-Control "no-cache, no-store, must-revalidate"
    Header set Pragma "no-cache"
    Header set Expires "0"
  </FilesMatch>
</IfModule>
# ==== fin kmoviezone ====
"""
MARCA = "kmoviezone: sin cache para el contenido dinamico"

def main():
    revertir = "--revertir" in sys.argv
    ftp = conexion()          # FTPS cifrado + /public_html, lee ftp-config.json

    actual = ""
    try:
        lineas = []
        ftp.retrlines("RETR .htaccess", lineas.append)
        actual = "\n".join(lineas) + "\n"
        print(f"  .htaccess existente: {len(actual)} bytes")
    except Exception as e:
        print(f"  .htaccess NO existe (o no se pudo leer): {e}")

    # respaldo local
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    datos_dir = os.path.join(BASE, "htaccess-backups")
    os.makedirs(datos_dir, exist_ok=True)
    if actual:
        with open(os.path.join(datos_dir, f"htaccess-{ts}.bak"), "w", encoding="utf-8") as f:
            f.write(actual)
        print(f"  respaldo: htaccess-backups/htaccess-{ts}.bak")

    if revertir:
        nuevo = actual
    else:
        if MARCA in actual:
            print("  ya tenia nuestro bloque -> reemplazando por la version actual")
            nuevo = re.sub(r"\n# ==== kmoviezone.*?# ==== fin kmoviezone ====\n", "\n", actual, flags=re.S)
        else:
            nuevo = actual
        nuevo = (nuevo.rstrip() + "\n" + BLOQUE)

    if not nuevo.strip():
        print("!! el resultado quedaria vacio: aborto por seguridad"); ftp.quit(); return

    with open(os.path.join(BASE, ".htaccess.nuevo"), "w", encoding="utf-8", newline="\n") as f:
        f.write(nuevo)
    with open(os.path.join(BASE, ".htaccess.nuevo"), "rb") as f:
        ftp.storbinary("STOR .htaccess", f)
    print(f"  subido: {len(nuevo)} bytes")
    ftp.quit()
    print("\nLISTO. AHORA verifica que la web siga viva (curl a la raiz).")
    print("Si diera error 500:  python htaccess-cache.py --revertir  y volver a subir el respaldo.")

if __name__ == "__main__":
    main()