#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIPONY — puente con la cola de descargas (sin GUI).
   estado                 -> reporte de la cola (que bajo, que falta, donde)
   pendientes [--archivo] -> exporta los detenidos para reintentar
   encolar <archivo.txt>  -> mete los enlaces a linkList.xml (MIPONY CERRADO!)

ARCHIVO DE CARGA: cola-enlaces.txt  (ver plantilla)
"""
import os, sys, re, shutil, datetime, collections
import xml.etree.ElementTree as ET

APPDATA = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
DATOS = os.path.join(APPDATA, "MiPony")
LISTA = os.path.join(DATOS, "linkList.xml")
BASE = os.path.dirname(os.path.abspath(__file__))
COLA = os.path.join(BASE, "cola-enlaces.txt")

def cargar():
    # Nota: linkList.xml es un archivo LOCAL generado por MiPony (la app del propio
    # Monarca), no entrada externa. No hay superficie XXE aqui; stdlib es suficiente.
    if not os.path.exists(LISTA):
        print(f"!! no encuentro {LISTA}"); sys.exit(1)
    return ET.parse(LISTA)

def props(t):
    d = {}
    for pr in t.findall("property"):
        for k, v in pr.attrib.items(): d[k] = v
    return d

def mi_pony_abierto():
    """Avisa si MiPony parece estar corriendo (escribir con el abierto = perdida)."""
    try:
        import subprocess
        out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=20).stdout.lower()
        return "mipony" in out
    except Exception:
        return None

def estado():
    root = cargar().getroot()
    tareas = [props(t) for t in root.iter("Task")]
    print(f"COLA MiPony — {len(tareas)} tareas\n")
    for k in ("State", "Type"):
        print(f"  {k}:")
        for v, c in collections.Counter(t.get(k, "(vacio)") for t in tareas).most_common(8):
            print(f"     {v}: {c}")
    print("  Carpetas destino:")
    for v, c in collections.Counter(t.get("FilePath", "(vacio)") for t in tareas).most_common(8):
        print(f"     {v}: {c}")
    pend = [t for t in tareas if t.get("State") != "Complete"]
    print(f"\n  PENDIENTES/DETENIDOS: {len(pend)}")
    for t in pend[:8]:
        print(f"     [{t.get('State')}] {(t.get('FileName') or t.get('Url'))[:70]}")

def pendientes(salida=None):
    root = cargar().getroot()
    pend = [props(t) for t in root.iter("Task") if props(t).get("State") != "Complete"]
    salida = salida or os.path.join(BASE, "reintentar.txt")
    with open(salida, "w", encoding="utf-8") as f:
        for t in pend:
            f.write(t.get("Url", "") + "\n")
    print(f"{len(pend)} enlaces detenidos -> {salida}")
    print("Peguelos en MiPony (o vuelvalos a encolar con: mipony.py encolar reintentar.txt)")

def detectar_host(url):
    m = re.search(r"https?://(?:www\.)?([a-z0-9.-]+)", url, re.I)
    h = (m.group(1) if m else "").lower()
    for clave, nombre in (("mediafire", "MediaFire"), ("1fichier", "OneFichier"), ("mega", "Megaconz"),
                          ("rapidgator", "Rapidgator"), ("solidfiles", "Solidfiles")):
        if clave in h: return nombre
    return "MediaFire"

def leer_cola(ruta):
    """Lee cola-enlaces.txt: cabeceras (titulo/tipo/carpeta) + lineas con URLs."""
    titulo = tipo = carpeta = None; urls = []
    if not os.path.exists(ruta):
        print(f"!! no existe {ruta}"); sys.exit(1)
    for l in open(ruta, encoding="utf-8", errors="ignore"):
        s = l.strip()
        if not s or s.startswith("#"): continue
        low = s.lower()
        if low.startswith("titulo:"): titulo = s.split(":", 1)[1].strip(); continue
        if low.startswith("tipo:"):   tipo = s.split(":", 1)[1].strip(); continue
        if low.startswith("carpeta:"):carpeta = s.split(":", 1)[1].strip(); continue
        if s.startswith("---"): continue
        m = re.search(r"https?://\S+", s)
        if m: urls.append(m.group(0))
    return titulo, tipo, carpeta, urls

def encolar(ruta):
    titulo, tipo, carpeta, urls = leer_cola(ruta)
    if not urls:
        print("!! no encontre enlaces en el archivo"); return
    carpeta = carpeta or r"D:\my stream"
    if mi_pony_abierto():
        print("### ALTO ### MiPony parece ABIERTO.")
        print("Cierrelo antes de encolar (lo reescribe al salir y perderiamos los cambios).")
        return
    # respaldo
    resp = LISTA + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(LISTA, resp)
    print(f"respaldo: {resp}")
    tree = cargar(); root = tree.getroot()
    tasks = root.find("Tasks")
    if tasks is None:
        tasks = ET.SubElement(root, "Tasks")
    puestos = 0
    for u in urls:
        t = ET.SubElement(tasks, "Task", {"type": "file"})
        for k, v in (("Url", u), ("State", "Pending"), ("FilePath", carpeta),
                     ("FileName", ""), ("Size", "0"), ("Type", detectar_host(u)), ("Password", "")):
            ET.SubElement(t, "property", {k: v})
        puestos += 1
    tree.write(LISTA, encoding="utf-8", xml_declaration=True)
    print(f"OK: {puestos} enlaces encolados en {carpeta}")
    if titulo: print(f"   tanda: {titulo} ({tipo or 'tipo?'})")
    print("Abra MiPony: los vera en la lista.")

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); print(f"\nArchivo de carga: {COLA}"); return
    if a[0] == "estado": estado(); return
    if a[0] == "pendientes":
        sal = a[a.index("--archivo")+1] if "--archivo" in a else None
        pendientes(sal); return
    if a[0] == "encolar":
        encolar(a[1] if len(a) > 1 else COLA); return
    print("orden desconocida:", a[0], "-> usa: estado | pendientes | encolar <archivo>")

if __name__ == "__main__":
    main()
