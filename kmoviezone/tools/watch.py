# ============================================================
#  SEAWOLF STREAMING - VIGILANTE (actualizacion automatica)
#  Vigila catalogo.csv (o catalogo.xlsx). Al GUARDAR cualquier
#  cambio, regenera datos.json automaticamente.
#
#  USO:   python watch.py
#  corre en segundo plano. Dejelo abierto mientras edita.
#  Para detener: Ctrl + C
#
#  OPCIONAL: si define FTP_DATA abajo, ademas SUBE
#  automaticamente index.html + datos.json a su Hostinger.
# ============================================================

import os
import time
import importlib
import build  # reutiliza el traductor

DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DIR, "catalogo.csv")
XLSX_PATH = os.path.join(DIR, "catalogo.xlsx")

# --- Subida CIFRADA (FTPS). Credenciales en ftp-config.json (fuera del codigo) ---
AUTO_UPLOAD = True
FTP_ARCHIVOS = ["index.html", "datos.json", "logo.png"]  # archivos del sitio


def subir(archivo_local):
    """Sube un archivo por FTPS (cifrado) usando la conexion de subir.py."""
    try:
        from subir import conexion
        ftp = conexion()                      # ya entra a /public_html
        with open(os.path.join(DIR, archivo_local), "rb") as f:
            ftp.storbinary("STOR " + archivo_local, f)
        ftp.quit()
        return True
    except Exception as e:
        print("   [FTP ERROR al subir", archivo_local + "]", e)
        return False


def obtener_marca(archivo):
    """Devuelve la firma (modtime+size) de un archivo, o None si no existe."""
    try:
        st = os.stat(archivo)
        return (st.st_mtime, st.st_size)
    except OSError:
        return None


def main():
    print("=== SEAWOLF VIGILANTE ACTIVO ===")
    print("Vigilando:", os.path.basename(CSV_PATH), "(y", os.path.basename(XLSX_PATH), "si existe)")
    print("Guarde el CSV/Excel y datos.json se regenera al instante.")
    if AUTO_UPLOAD:
        try:
            import json
            _c = json.load(open(os.path.join(DIR, "ftp-config.json"), encoding="utf-8"))
            print(f"Subida CIFRADA (FTPS): ACTIVADA -> {_c['host']}{_c.get('dir','/')}")
        except Exception:
            print("Subida CIFRADA: ACTIVADA (revisa ftp-config.json)")
    else:
        print("Subida FTP: desactivada (sube manual o configura ftp-config.json).")
    print("Para detener: Ctrl+C\n")

    # marca inicial
    marca_csv = obtener_marca(CSV_PATH)
    marca_xlsx = obtener_marca(XLSX_PATH)
    print("Listo. Esperando cambios...")

    while True:
        time.sleep(1.5)  # chequea cada 1.5s

        nueva_csv = obtener_marca(CSV_PATH)
        nueva_xlsx = obtener_marca(XLSX_PATH)

        cambio = (nueva_csv != marca_csv) or (nueva_xlsx != marca_xlsx)
        if cambio:
            # rendimos tempo para que el guardado termine
            time.sleep(0.5)
            print("\n[Cambio detectado] regenerando datos.json...")
            try:
                importlib.reload(build)
                build.build()
                print("[OK] datos.json actualizado.")
                if AUTO_UPLOAD:
                    for f in FTP_ARCHIVOS:
                        if subir(f):
                            print("[OK] subido:", f)
            except Exception as e:
                print("[ERROR al regenerar]", e)
            marca_csv = obtener_marca(CSV_PATH)
            marca_xlsx = obtener_marca(XLSX_PATH)


if __name__ == "__main__":
    main()