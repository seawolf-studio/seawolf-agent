#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COSECHADOR DE ENLACES — lee el log de FileUploader y arma la fila del catalogo.
No usa GUI: el log ya trae los 3 enlaces por archivo.

Uso:
   python cosechar.py "Solo Leveling" --tipo anime
   python cosechar.py "Solo Leveling" --tipo anime --csv     (agrega a catalogo.csv)
   python cosechar.py --log otra_ruta.log --titulo X
"""
import os, re, csv, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.expanduser("~"), "Downloads", "FileUploader.log")

# orden fijo de proveedores (doctrina del Monarca)
ORDEN = [("streamtape", "streamtape.com"), ("voe", "voe.sx"), ("player4me", "player4me.com[APi]")]
ALIAS = {"streamtape.com": "streamtape", "streamtape.to": "streamtape",
         "voe.sx": "voe", "voe2.sx": "voe",
         "player4me.com[APi]": "player4me", "player4me.com": "player4me"}

def leer_log(ruta):
    """Devuelve {archivo: {proveedor: url}} tomando el ULTIMO enlace valido de cada uno."""
    datos = collections.defaultdict(dict)
    if not os.path.exists(ruta):
        print(f"!! no encuentro el log: {ruta}"); return datos
    for l in open(ruta, encoding="utf-8", errors="ignore"):
        parts = l.rstrip("\r\n").split("|")
        if len(parts) < 5: continue
        _, host, url, _, archivo = parts[0], parts[1], parts[2], parts[3], parts[4]
        prov = ALIAS.get(host.strip(), host.strip())
        if not archivo.strip(): continue
        if "File is in your account" in url or not url.startswith("http"):
            datos[archivo.strip()].setdefault(prov, None)   # marca ausencia
            continue
        datos[archivo.strip()][prov] = url.strip()
    return datos

def num_cap(archivo):
    """Saca el numero de capitulo del nombre del archivo."""
    n = os.path.splitext(archivo)[0]
    # 'LDSH_T1_1080p-(Identi-Jesus4247) (10)'  -> 10
    m = re.search(r'\((\d+)\)\s*$', n)
    if m: return int(m.group(1))
    # '01 - The Return - Joining Forces'  -> 1
    m = re.match(r'^(\d{1,3})\s*[-_ ]', n)
    if m: return int(m.group(1))
    # 'Solo Leveling 06'  -> 6
    m = re.search(r'(\d{1,3})\s*$', n)
    if m: return int(m.group(1))
    return None

def nombre_cap(archivo):
    n = os.path.splitext(archivo)[0]
    m = re.match(r'^\d{1,3}\s*[-_ ]\s*(.+)$', n)
    return m.group(1).strip() if m else n

def construir(titulo, tipo, datos):
    """Devuelve (fila_csv, reporte)."""
    caps = []
    problemas = []
    for archivo, provs in datos.items():
        c = num_cap(archivo)
        if c is None:
            problemas.append(f"sin numero de capitulo: {archivo}"); continue
        caps.append((c, archivo, provs))
    caps.sort(key=lambda x: x[0])
    bloques = []
    for c, archivo, provs in caps:
        partes = []
        for clave, _ in ORDEN:
            u = provs.get(clave)
            if u: partes.append(u)
            else: problemas.append(f"cap {c}: falta {clave} ({archivo})")
        bloques.append("|".join(partes))
    enlaces = ";".join(bloques)
    fila = [titulo, tipo, enlaces]
    rep = [f"{len(caps)} capitulos", f"{len(enlaces)} chars de enlaces",
           f"capitulos: {[c for c,_,_ in caps]}"]
    return fila, rep, problemas

def main():
    a = sys.argv[1:]
    titulo = None; tipo = "anime"; log = LOG; escribir = False; solo_lista = False; filtro = ""
    if "--log" in a: i = a.index("--log"); log = a[i+1]; del a[i:i+2]
    if "--filtro" in a: i = a.index("--filtro"); filtro = a[i+1]; del a[i:i+2]
    if "--tipo" in a: i = a.index("--tipo"); tipo = a[i+1]; del a[i:i+2]
    if "--csv" in a: escribir = True; a.remove("--csv")
    if "--lista" in a: solo_lista = True; a.remove("--lista")
    if "--titulo" in a: i = a.index("--titulo"); titulo = a[i+1]; del a[i:i+2]
    if a and not titulo: titulo = a[0]
    if not titulo and not solo_lista: print('Uso: python cosechar.py "Titulo" --tipo anime [--csv]'); return
    if solo_lista and not titulo: titulo = "(lista)"

    datos = leer_log(log)
    if filtro:
        f = filtro.lower()
        datos = {k: v for k, v in datos.items() if f in k.lower()}
    print(f"LOG: {log}")
    print(f"Archivos con enlaces: {len(datos)}\n")
    if solo_lista:
        for arch, provs in sorted(datos.items()):
            print(f"  {arch}")
            for clave, _ in ORDEN:
                print(f"      {clave:<11} {provs.get(clave) or '(falta)'}")
        return

    fila, rep, problemas = construir(titulo, tipo, datos)
    print("=== COSECHA ===")
    for r in rep: print("  " + r)
    if problemas:
        print(f"\n=== AVISOS ({len(problemas)}) ===")
        for p in problemas[:15]: print("  ! " + p)
        if len(problemas) > 15: print(f"  ... y {len(problemas)-15} mas")
    print(f"\n=== FILA para catalogo.csv ===")
    print(f"{fila[0]},{fila[1]},{fila[2][:400]}{'...' if len(fila[2])>400 else ''}")

    if escribir:
        ruta = os.path.join(BASE, "catalogo.csv")
        existe = os.path.exists(ruta)
        with open(ruta, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            if not existe: w.writerow(["titulo", "tipo", "enlaces"])
            w.writerow(fila)
        print(f"\n✔ agregado a {ruta}")

if __name__ == "__main__":
    main()
