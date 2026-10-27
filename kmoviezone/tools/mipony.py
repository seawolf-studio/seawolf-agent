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

def normalizar_url(u):
    """MiPony (build 2023) SOLO resuelve el formato viejo de MediaFire.
    Convierte el moderno /file/<clave>/... al viejo ?<clave>. Verificado 2026-10-26."""
    m = re.search(r"mediafire\.com/file/([^/]+)/", u, re.I)
    if m:
        return "http://www.mediafire.com/?" + m.group(1)
    return u

def detectar_host(url):
    m = re.search(r"https?://(?:www\.)?([a-z0-9.-]+)", url, re.I)
    h = (m.group(1) if m else "").lower()
    for clave, nombre in (("mediafire", "MediaFire"), ("1fichier", "OneFichier"), ("mega", "Megaconz"),
                          ("rapidgator", "Rapidgator"), ("solidfiles", "Solidfiles")):
        if clave in h: return nombre
    return "MediaFire"

def _parse_bloque(lineas):
    """Lee un cajon: cabeceras (titulo/tipo/carpeta/password) + enlaces."""
    titulo = tipo = carpeta = password = None; urls = []
    for l in lineas:
        s = l.strip()
        if not s or s.startswith("#"): continue
        low = s.lower()
        if low.startswith("titulo:"): titulo = s.split(":", 1)[1].strip(); continue
        if low.startswith("tipo:"):   tipo = s.split(":", 1)[1].strip(); continue
        if low.startswith("carpeta:"):carpeta = s.split(":", 1)[1].strip(); continue
        if low.startswith(("password:", "contrasena:", "contraseña:", "clave:", "pass:")):
            password = s.split(":", 1)[1].strip(); continue
        if s.startswith("---"): continue
        m = re.search(r"https?://\S+", s)
        if m: urls.append(m.group(0))
    return titulo, tipo, carpeta, urls, password

def leer_tandas(ruta):
    """Lee el archivo completo y devuelve TODAS las tandas (cajones).
    Cada cajon trae sus cabeceras y sus enlaces; se separan con una linea de
    '===' (3 o mas iguales). Asi se encolan VARIAS subidas en un solo paso."""
    if not os.path.exists(ruta):
        print(f"!! no existe {ruta}"); sys.exit(1)
    bloques = [[]]
    for l in open(ruta, encoding="utf-8", errors="ignore"):
        if re.match(r"^\s*={3,}\s*$", l):
            bloques.append([]); continue
        bloques[-1].append(l)
    tandas = []
    for b in bloques:
        t, ti, c, u, p = _parse_bloque(b)
        if u:
            tandas.append({"titulo": t, "tipo": ti, "carpeta": c or r"D:\my stream",
                           "password": p, "urls": u})
    return tandas

def leer_cola(ruta):
    """Compatibilidad: devuelve la PRIMERA tanda como tupla."""
    td = leer_tandas(ruta)
    if not td: return None, None, None, [], None
    x = td[0]
    return x["titulo"], x["tipo"], x["carpeta"], x["urls"], x["password"]

def encolar(ruta):
    """Encola TODAS las tandas del archivo (una o varias, separadas por '===')."""
    tandas = leer_tandas(ruta)
    if not tandas:
        print("!! no encontre enlaces en el archivo"); return
    if mi_pony_abierto():
        print("### ALTO ### MiPony parece ABIERTO.")
        print("Cierrelo antes de encolar (lo reescribe al salir y perderiamos los cambios).")
        return
    resp = LISTA + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(LISTA, resp)
    print(f"respaldo: {resp}")
    tree = cargar(); root = tree.getroot()
    tasks = root.find("Tasks")
    if tasks is None:
        tasks = ET.SubElement(root, "Tasks")
    print(f"\nENCUELO: {len(tandas)} tanda(s)")
    total = 0
    for n, td in enumerate(tandas, 1):
        print(f"  {n}. {td['titulo'] or '(sin titulo)'} [{td['tipo'] or 'tipo?'}] -> {td['carpeta']}"
              f"  ({len(td['urls'])} enlaces{', con clave' if td['password'] else ''})")
        for u in td["urls"]:
            u = normalizar_url(u)
            t = ET.SubElement(tasks, "Task", {"type": "file"})
            for k, v in (("Url", u), ("State", "Pending"), ("FilePath", td["carpeta"]),
                         ("FileName", ""), ("Size", "0"), ("Type", detectar_host(u)),
                         ("Password", td["password"] or "")):
                ET.SubElement(t, "property", {k: v})
            total += 1
    tree.write(LISTA, encoding="utf-8", xml_declaration=True)
    print(f"\nOK: {total} enlaces encolados en {len(tandas)} tanda(s)")
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
