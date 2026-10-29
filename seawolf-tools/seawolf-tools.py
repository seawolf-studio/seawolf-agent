#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SEAWOLF TOOLS — Optimizacion (v4)
Multi-disco + Pesados + MAPA de espacio + Duplicados + MANTENIMIENTO editable +
Papelera reversible + boton REA.

  python seawolf-tools.py drives
  python seawolf-tools.py scan ALL [--top 30]
  python seawolf-tools.py dupes ALL [--min 1]
  python seawolf-tools.py mant [run <id>]         # mantenimiento programado
  python seawolf-tools.py papeles / rescatar N / limpiar --paths "a","b" [--hard]
  python seawolf-tools.py serve ALL [--port 8770]  # APLICATIVO WEB

Seguridad: mueve a la Papelera Seawolf (reversible); --hard borra de verdad.
Codigo propio. Bellion para el Monarca (Key).
"""
import os, sys, re, json, hashlib, argparse, webbrowser, string, shutil, heapq, subprocess, threading
import secrets
import urllib.parse as urlparse
from collections import defaultdict
from datetime import datetime, timedelta

PAPELERA = r"C:\Users\Admin\Seawolf_Papelera"
MANIFEST = os.path.join(PAPELERA, "_manifest.json")
HERE = os.path.dirname(os.path.abspath(__file__))
MANTEN_CFG = os.path.join(HERE, "seawolf-manten.json")
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
            except OSError: pass
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
        rl = root.rstrip("\\").lower()
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d.lower() not in SKIP_DIRS and not d.startswith(".")]
            for fn in fns:
                p = os.path.join(dp, fn)
                try:
                    if os.path.isfile(p):
                        s = os.path.getsize(p)
                        if progress: progress(root, s, p)
                        yield p, s, root
                except OSError: continue

# ---------- MAPA de espacio (top-level por disco) ----------
def top_folder(root, path):
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else "(raiz)"

# ---------- mantenimiento ----------
def mant_cfg():
    if os.path.exists(MANTEN_CFG):
        try: return json.load(open(MANTEN_CFG, encoding="utf-8"))
        except Exception: pass
    cfg = {"tareas": [
        {"id": "temporales", "nombre": "Temporales viejos", "activo": True, "dias": 7,
         "horario": "semanal · lunes 09:00", "desc": "Mueve a Papelera archivos de %TEMP% con +N dias"},
        {"id": "logs_hermes", "nombre": "Logs de Hermes viejos", "activo": True, "dias": 30,
         "horario": "mensual · dia 1, 09:00", "desc": "Logs de ~/.hermes/logs con +N dias"},
        {"id": "papelera", "nombre": "Vaciar Papelera Seawolf", "activo": False, "dias": 30,
         "horario": "mensual · dia 1, 10:00", "desc": "BORRA de verdad lo que lleva +N dias en papelera"}
    ]}
    json.dump(cfg, open(MANTEN_CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return cfg
def mant_save(cfg): json.dump(cfg, open(MANTEN_CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def _old_files(folder, days):
    cut = datetime.now() - timedelta(days=days)
    out = []
    for dp, dns, fns in os.walk(folder):
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                if datetime.fromtimestamp(os.path.getmtime(p)) < cut: out.append(p)
            except OSError: continue
    return out

def mant_run(tid):
    cfg = mant_cfg()
    t = next((x for x in cfg["tareas"] if x["id"] == tid), None)
    if not t: return {"ok": False, "msg": "tarea no existe"}
    dias = int(t.get("dias", 30))
    if tid == "temporales":
        files = _old_files(os.environ.get("TEMP", r"C:\Users\Admin\AppData\Local\Temp"), dias)
        n = len(limpiar(files))
        return {"ok": True, "msg": f"{n} archivos temporales movidos a Papelera"}
    if tid == "logs_hermes":
        lg = r"C:\Users\Admin\.hermes\logs"
        files = _old_files(lg, dias) if os.path.isdir(lg) else []
        n = len(limpiar(files))
        return {"ok": True, "msg": f"{n} logs movidos a Papelera"}
    if tid == "papelera":
        m = _manifest(); cut = datetime.now() - timedelta(days=dias); keep = []; n = 0
        for e in m:
            try:
                old = datetime.fromisoformat(e["fecha"]) < cut
            except Exception:
                old = False
            if old:
                if e.get("accion") == "papelera":
                    p = os.path.join(PAPELERA, e["archivo"])
                    try: os.remove(p); n += 1
                    except OSError: keep.append(e)
                else: n += 1
            else: keep.append(e)
        _save_manifest(keep)
        return {"ok": True, "msg": f"{n} elementos purgados de la Papelera"}
    return {"ok": False, "msg": "tarea desconocida"}

# ---------- REA ----------
def rea_run(path, kind="js"):
    cmd = ["npx", "-y", "rea-agents"]
    cmd += (["analyze-javascript-application", path, "--format", "md"] if kind == "js" else ["analyze", path, "--format", "md"])
    env = dict(os.environ)
    env.setdefault("JAVA_HOME", r"D:\jdk21\jdk-21.0.12.1+1")
    env.setdefault("GHIDRA_INSTALL_DIR", r"D:\ghidra\ghidra_12.1.4_PUBLIC")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=env, shell=True)
        out = (r.stdout or "") + (r.stderr or "")
        ev = ""
        for line in out.splitlines():
            if "ev_" in line and "evidence" not in line.lower():
                ev = line.strip(); break
        for line in out.splitlines():
            if line.strip() == "## evidence_id":
                idx = out.splitlines().index(line) + 2
                ev = out.splitlines()[idx].strip(); break
        return {"ok": True, "evidence": ev or "(sin evidence_id visible)", "tail": out[-1200:]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "msg": "timeout (analisis largo)"}
    except Exception as e:
        return {"ok": False, "msg": str(e)}

# ---------- pesados / duplicados / papelera ----------
def scan(targets, top=30):
    heap = []; per = defaultdict(lambda: [0, 0]); mapa = defaultdict(lambda: defaultdict(int))
    for p, s, root in walk_multi(targets):
        per[root][0] += 1; per[root][1] += s
        mapa[root][top_folder(root, p)] += s
        if len(heap) < top * 4: heapq.heappush(heap, (s, p))
        elif s > heap[0][0]: heapq.heapreplace(heap, (s, p))
    topf = sorted(heap, reverse=True)[:top]
    print("[Scan]")
    for r, v in per.items(): print(f"  {r}  {v[0]} archivos · {human(v[1])}")
    print(f"\n  TOTAL: {sum(v[0] for v in per.values())} archivos · {human(sum(v[1] for v in per.values()))}\n")
    for i, (s, p) in enumerate(topf, 1): print(f"  {i:>3}  {human(s):>9}  {p}")
    return topf

def find_dupes(targets, min_mb=1):
    minsz = int(min_mb * 1024 * 1024); by_size = defaultdict(list)
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
            except OSError: continue
        for _, ps in bh.items():
            if len(ps) > 1: groups.append({"size": s, "files": ps})
    groups.sort(key=lambda g: -g["size"] * (len(g["files"]) - 1)); return groups

def dupes(targets, min_mb=1):
    g = find_dupes(targets, min_mb)
    waste = sum(x["size"] * (len(x["files"]) - 1) for x in g)
    print(f"[Duplicados] {len(g)} grupos · {human(waste)} desperdiciados")
    for i, x in enumerate(g, 1):
        print(f"  Grupo {i} ({len(x['files'])} copias · {human(x['size'])} c/u)")
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
    os.makedirs(PAPELERA, exist_ok=True); m = _manifest(); done = []
    for p in paths:
        if not p or not os.path.isfile(p): continue
        try:
            if hard:
                os.remove(p); m.append({"accion": "borrado", "path": p, "fecha": datetime.now().isoformat(timespec="seconds")}); done.append(p)
            else:
                base = os.path.basename(p); dst = os.path.join(PAPELERA, base)
                if os.path.exists(dst): dst = os.path.join(PAPELERA, f"{datetime.now():%H%M%S}_{base}")
                shutil.move(p, dst)
                m.append({"accion": "papelera", "archivo": os.path.basename(dst), "original": p, "fecha": datetime.now().isoformat(timespec="seconds")}); done.append(p)
        except OSError as e: print(f"  [x] {p}: {e}")
    _save_manifest(m); return done

def papeles():
    m = _manifest()
    if not m: print("[i] Papelera vacia."); return
    for i, e in enumerate(m, 1): print(f"  {i}. [{e['accion']}] {e.get('archivo') or e.get('path')}  ({e['fecha']})")

def rescatar(n):
    m = _manifest()
    if not (1 <= n <= len(m)): print("[!] Numero invalido."); return
    e = m[n - 1]
    if e["accion"] == "borrado": print("[!] Se borro. No hay rescate."); return
    src = os.path.join(PAPELERA, e["archivo"])
    if not os.path.exists(src): print("[!] No esta."); return
    os.makedirs(os.path.dirname(e["original"]), exist_ok=True); shutil.move(src, e["original"]); m.pop(n - 1); _save_manifest(m)
    print(f"[OK] RESCATADO -> {e['original']}")

# ---------------- APLICATIVO WEB ----------------
# ════════════════════════════════════════════════════════════════════════════
#  SALUD DEL EQUIPO — diagnostico y mantenimiento del hierro
#  Regla de oro: NADA se toca sin saber ANTES si el disco es SSD o HDD.
#  Desfragmentar un SSD lo DESGASTA; a un SSD le toca TRIM, a un HDD defrag.
# ════════════════════════════════════════════════════════════════════════════
PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

AVISO_DISCOS = (
 "ZONA DELICADA. Todo lo de aqui toca el disco fisico y el sistema de archivos. "
 "Optimizar NO borra tus archivos, pero NUNCA se interrumpe ni se apaga el equipo mientras corre. "
 "Este modulo NO modifica particiones: un cambio mal hecho ahi puede borrar un disco entero. "
 "Si no estas seguro de algo, NO lo ejecutes."
)

AVISO_TRIM = (
 "TRIM en SSD: es el mantenimiento CORRECTO para un disco solido. Le devuelve el espacio de lo "
 "borrado y lo mantiene rapido. NO lo desgasta. No interrumpas el proceso."
)

AVISO_DEFRAG = (
 "Desfragmentar en HDD: junta los datos repartidos para que el cabezal no salte tanto. Puede tardar "
 "BASTANTE y necesita espacio libre (se pide al menos un 15%). Si el disco esta casi lleno es lento "
 "y poco efectivo: mejor libera espacio primero. No interrumpas el proceso."
)

AVISO_USB = (
 "Disco EXTRAIBLE o de tipo sin confirmar: este modulo NO lo toca. Si se desconecta a mitad de una "
 "operacion el dano puede ser grave. Ademas, en un USB el mantenimiento rara vez aporta."
)

AVISO_VERIFICAR = (
 "Verifica el disco SIN reparar y SIN borrar nada (chkdsk /scan en linea). Es solo lectura, asi que "
 "es seguro. Puede tardar mucho en discos grandes: dejalo terminar. Requiere permisos de administrador."
)


FUNCIONES_SALUD = [
 {"id": "discos", "nombre": "Discos: tipo y salud",
  "desc": "Lista cada disco fisico con su tipo real (SSD, HDD, NVMe o USB), su estado de salud y "
          "su estado operativo. Saber el tipo NO es un lujo: de ahi depende que mantenimiento le toca."},
 {"id": "espacio", "nombre": "Espacio por volumen",
  "desc": "Espacio total, libre y PORCENTAJE libre de cada unidad. Un disco lleno por encima del 90% "
          "trabaja mal y envejece mas rapido. Aqui saltan los avisos antes de que sea un problema."},
 {"id": "particiones", "nombre": "Mapa de particiones (solo lectura)",
  "desc": "Que disco fisico contiene que unidad logica, de que tamano y con que formato. "
          "Es informacion: este modulo NO modifica particiones, porque un cambio mal hecho "
          "puede borrar un disco entero."},
 {"id": "optimizar", "nombre": "Optimizar (TRIM o desfragmentar, automatico)",
  "desc": "Mantenimiento del disco segun su tipo. En SSD ejecuta TRIM (le devuelve el espacio de lo "
          "borrado y lo mantiene rapido). En HDD desfragmenta (junta los datos para que el cabezal "
          "no salte). Si no puede confirmar el tipo de disco, NO toca nada."},
 {"id": "verificar", "nombre": "Verificar disco (solo lectura)",
  "desc": "Revisa la integridad del disco y del sistema de archivos SIN reparar y SIN borrar nada "
          "(chkdsk /scan en modo en linea). Detecta errores antes de que se conviertan en perdida "
          "de datos. Requiere permisos de administrador."},
 {"id": "cpu_ram", "nombre": "CPU y memoria",
  "desc": "Uso actual del procesador y memoria libre. Si la RAM libre baja de forma sostenida, "
          "el equipo empieza a usar el disco como memoria y todo se vuelve lento."},
 {"id": "arranque", "nombre": "Programas de arranque",
  "desc": "Todo lo que arranca solo con Windows. Cada programa aqui alarga el arranque y consume "
          "memoria desde el primer segundo del dia."},
 {"id": "temperatura", "nombre": "Temperatura y desgaste (requiere extra)",
  "desc": "Temperatura real, desgaste y horas de encendido del disco. NO viene en Windows: hace falta "
          "la herramienta libre 'smartmontools'. Sin ella, aqui no te miento mostrando un dato inventado."},
]


def _ps(cmd, timeout=90):
    """Ejecuta PowerShell en segundo plano (sin ventana) y devuelve stdout+stderr."""
    for exe in (PS, "powershell.exe"):
        try:
            r = subprocess.run([exe, "-NoProfile", "-NonInteractive", "-Command", cmd],
                               capture_output=True, text=True, timeout=timeout,
                               creationflags=0x08000000)      # CREATE_NO_WINDOW
            return (r.stdout or "") + (r.stderr or "")
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            return "ERROR: tiempo agotado"
        except Exception as e:
            return f"ERROR: {e}"
    return "ERROR: no encontre PowerShell"


def _ps_json(cmd, timeout=90):
    """Igual que _ps pero parsea JSON (tolerando avisos previos de PowerShell)."""
    txt = (_ps(cmd, timeout) or "").strip()
    if not txt:
        return None
    try:
        return json.loads(txt)
    except Exception:
        pass
    for i, ch in enumerate(txt):
        if ch in "[{":
            try:
                return json.loads(txt[i:])
            except Exception:
                continue
    return None


def _lista(x):
    """PowerShell devuelve un objeto suelto si hay un solo elemento: lo normalizo a lista."""
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def salud_discos():
    """Discos fisicos con su TIPO real y su salud. Es la base de todo lo demas."""
    d = _ps_json('Get-PhysicalDisk | Select-Object DeviceId,FriendlyName,MediaType,BusType,'
                 'HealthStatus,OperationalStatus,@{n="GB";e={[math]::Round($_.Size/1GB)}} | '
                 'ConvertTo-Json -Compress')
    out = []
    for x in _lista(d):
        if not isinstance(x, dict):
            continue
        tipo = str(x.get("MediaType") or "")
        bus = str(x.get("BusType") or "")
        if "SSD" in tipo:
            clase, mant = "SSD", "TRIM"
        elif "HDD" in tipo:
            clase, mant = "HDD", "Desfragmentar"
        elif "USB" in bus:
            clase, mant = "USB", "No tocar (extraible)"
        else:
            clase, mant = "Desconocido", "No tocar (tipo sin confirmar)"
        if clase == "SSD":
            riesgo, motivo = "recomendado", AVISO_TRIM
        elif clase == "HDD":
            riesgo, motivo = "cuidado", AVISO_DEFRAG
        else:
            riesgo, motivo = "prohibido", AVISO_USB
        out.append({"id": x.get("DeviceId"), "modelo": x.get("FriendlyName"), "tipo": clase,
                    "bus": bus, "salud": x.get("HealthStatus"), "estado": x.get("OperationalStatus"),
                    "gb": x.get("GB"), "mantenimiento": mant, "riesgo": riesgo, "motivo": motivo})
    return out


def salud_volumenes():
    """Espacio por unidad + EN QUE DISCO FISICO vive (es lo que decide TRIM o defrag)."""
    mapa = {}
    for m in _lista(_ps_json('Get-Volume | Where-Object {$_.DriveLetter} | ForEach-Object { $v=$_; '
                             '$pd = Get-Partition -DriveLetter $v.DriveLetter -ErrorAction SilentlyContinue | '
                             'Get-Disk | Get-PhysicalDisk -ErrorAction SilentlyContinue; '
                             '[PSCustomObject]@{L=$v.DriveLetter; Tipo=$pd.MediaType; Modelo=$pd.FriendlyName} } | '
                             'ConvertTo-Json -Compress')):
        if isinstance(m, dict):
            mapa[str(m.get("L"))] = (str(m.get("Tipo") or ""), str(m.get("Modelo") or ""))
    v = _ps_json('Get-Volume | Where-Object {$_.DriveLetter} | Select-Object DriveLetter,FileSystem,'
                 'HealthStatus,@{n="TotalGB";e={[math]::Round($_.Size/1GB)}},'
                 '@{n="LibreGB";e={[math]::Round($_.SizeRemaining/1GB)}},'
                 '@{n="LibrePct";e={[math]::Round(100*$_.SizeRemaining/$_.Size)}} | ConvertTo-Json -Compress')
    out = []
    for x in _lista(v):
        if not isinstance(x, dict):
            continue
        pct = x.get("LibrePct") or 0
        aviso = ("CRITICO: casi lleno" if pct <= 5 else
                 "Atencion: poco espacio" if pct <= 10 else
                 "Vigilar" if pct <= 20 else "")
        tipo_fis, modelo_fis = mapa.get(str(x.get("DriveLetter")), ("", ""))
        if "SSD" in tipo_fis:
            mant, riesgo = "TRIM", "recomendado"
        elif "HDD" in tipo_fis:
            mant, riesgo = "Desfragmentar", "cuidado"
        else:
            mant, riesgo = "No tocar (extraible o sin confirmar)", "prohibido"
        out.append({"letra": x.get("DriveLetter"), "fs": x.get("FileSystem"),
                    "salud": x.get("HealthStatus"), "totalGB": x.get("TotalGB"),
                    "libreGB": x.get("LibreGB"), "librePct": pct, "aviso": aviso,
                    "discoTipo": (tipo_fis or "?"), "discoModelo": modelo_fis,
                    "mantenimiento": mant, "riesgo": riesgo})
    out.sort(key=lambda z: z.get("librePct") or 100)
    return out


def salud_particiones():
    """Mapa disco fisico -> unidad logica. SOLO LECTURA (no modifica nada)."""
    p = _ps_json('Get-Partition | Where-Object {$_.DriveLetter} | Select-Object DiskNumber,'
                 'DriveLetter,@{n="GB";e={[math]::Round($_.Size/1GB)}},Type,IsBoot,IsSystem | '
                 'ConvertTo-Json -Compress')
    return [x for x in _lista(p) if isinstance(x, dict)]


def salud_cpu_ram():
    """Uso de CPU y memoria libre."""
    c = _ps_json('$c=Get-CimInstance Win32_Processor; $o=Get-CimInstance Win32_OperatingSystem; '
                 '[PSCustomObject]@{cpu=$c.Name; carga=$c.LoadPercentage; nucleos=$c.NumberOfCores; '
                 'hilos=$c.NumberOfLogicalProcessors; ramTotalGB=[math]::Round($o.TotalVisibleMemorySize/1MB,1); '
                 'ramLibreGB=[math]::Round($o.FreePhysicalMemory/1MB,1)} | ConvertTo-Json -Compress')
    return c if isinstance(c, dict) else {}


def salud_arranque():
    """Programas que arrancan con Windows."""
    a = _ps_json('Get-CimInstance Win32_StartupCommand | Select-Object Name,Location,Command | '
                 'ConvertTo-Json -Compress')
    out = []
    for x in _lista(a):
        if isinstance(x, dict):
            out.append({"nombre": x.get("Name"), "ubicacion": x.get("Location"),
                        "comando": x.get("Command")})
    return out


def salud_tipo_de(letra):
    """Devuelve 'SSD', 'HDD' o '' para una unidad logica (letra sin dos puntos)."""
    t = _ps(f'(Get-Partition -DriveLetter {letra} | Get-Disk | Get-PhysicalDisk).MediaType', 60)
    t = (t or "").strip()
    if "SSD" in t:
        return "SSD"
    if "HDD" in t:
        return "HDD"
    return ""


def salud_optimizar(letra):
    """TRIM en SSD / desfragmentar en HDD. Si no puede confirmar el tipo, NO TOCA NADA."""
    letra = (letra or "").strip().rstrip(":").upper()
    if len(letra) != 1 or not letra.isalpha():
        return {"ok": False, "msg": "Letra de unidad no valida"}
    tipo = salud_tipo_de(letra)
    if tipo == "SSD":
        accion, verbo = "ReTrim", "TRIM (mantenimiento de SSD: NO lo desgasta)"
    elif tipo == "HDD":
        accion, verbo = "Defrag", "Desfragmentado (mantenimiento de disco mecanico)"
    else:
        return {"ok": False, "msg": f"{letra}: no pude confirmar si es SSD o HDD. POR SEGURIDAD no toco nada.",
                "tipo": "?", "aviso": AVISO_USB}
    # ── GUARDIA 1: desfragmentar necesita hueco libre. Un disco casi lleno se queda a medias. ──
    try:
        tot, us, lib = shutil.disk_usage(letra + ":\\")
        pct = 100.0 * lib / tot
    except Exception:
        pct = 100.0
    if tipo == "HDD" and pct < 15:
        return {"ok": False, "tipo": tipo, "bloqueado": True,
                "msg": (f"{letra}: solo {pct:.0f}% libre ({human(lib)}). Desfragmentar un disco casi lleno "
                        f"es lento, poco efectivo y puede quedarse a medias. Libere espacio primero "
                        f"(deje ~15%) y vuelva a intentarlo. NO lo ejecuto."),
                "aviso": AVISO_DEFRAG}
    salida = _ps(f'Optimize-Volume -DriveLetter {letra} -{accion} -Verbose', 1800)
    fallo = any(w in salida.lower() for w in ("denied", "denegado", "error", "no se puede"))
    return {"ok": not fallo, "tipo": tipo, "accion": verbo, "letra": letra,
            "msg": ("Listo. " if not fallo else "Fallo (probablemente faltan permisos de administrador). ")
                   + accion + f" en {letra}:",
            "salida": (salida or "")[-1200:]}


def salud_verificar(letra):
    """chkdsk /scan: revisa SIN reparar y SIN borrar. Solo lectura."""
    letra = (letra or "").strip().rstrip(":").upper()
    if len(letra) != 1 or not letra.isalpha():
        return {"ok": False, "msg": "Letra de unidad no valida"}
    salida = _ps(f'chkdsk {letra}: /scan', 3600)
    texto = (salida or "")
    fallo = any(w in texto.lower() for w in ("denied", "denegado", "administrador", "privilegio"))
    limpio = ("no se encontraron problemas" in texto.lower()) or ("no problems" in texto.lower())
    return {"ok": not fallo, "letra": letra, "limpio": limpio,
            "msg": ("Requiere permisos de administrador." if fallo else
                    ("Sin problemas detectados." if limpio else "Revision terminada: revisa la salida.")),
            "salida": texto[-1500:]}


def salud_todo():
    """Todo el diagnostico de una sola vez + AVISOS automaticos."""
    discos = salud_discos()
    volumenes = salud_volumenes()
    cpu = salud_cpu_ram()
    avisos = []
    for v in volumenes:
        if v.get("aviso"):
            avisos.append(f"{v['letra']}: {v['aviso']} ({v['librePct']}% libre, quedan {v['libreGB']} GB)")
    for d in discos:
        if str(d.get("salud")) != "Healthy":
            avisos.append(f"DISCO {d['modelo']}: salud = {d.get('salud')} (revisar ya)")
        if str(d.get("estado")) not in ("OK", "Online", ""):
            avisos.append(f"DISCO {d['modelo']}: estado = {d.get('estado')}")
    libre = cpu.get("ramLibreGB") or 0
    if libre and libre < 3:
        avisos.append(f"Memoria libre baja: {libre} GB")
    n_ssd = sum(1 for d in discos if d["tipo"] == "SSD")
    n_hdd = sum(1 for d in discos if d["tipo"] == "HDD")
    bloq = [v["letra"] for v in volumenes if v.get("discoTipo", "").startswith("HDD") and (v.get("librePct") or 0) < 15]
    if bloq:
        avisos.append("Desfragmentado BLOQUEADO en " + ", ".join(bloq)
                      + ": menos del 15% libre. Libere espacio primero.")
    return {"discos": discos, "volumenes": volumenes, "cpu": cpu,
            "arranque": salud_arranque(), "particiones": salud_particiones(),
            "avisos": avisos, "resumen": {"ssd": n_ssd, "hdd": n_hdd,
                                          "unidades": len(volumenes), "discos": len(discos)},
            "funciones": FUNCIONES_SALUD,
            "aviso_general": AVISO_DISCOS,
            "avisos_accion": {"optimizar_ssd": AVISO_TRIM, "optimizar_hdd": AVISO_DEFRAG,
                              "prohibido": AVISO_USB, "verificar": AVISO_VERIFICAR}}


# ════════════════════════════════════════════════════════════════════════════
#  CERRADURA — sin la clave no se entra. OBLIGATORIA al publicar en un dominio:
#  este aplicativo MUEVE y BORRA archivos del disco, no puede quedar abierto.
# ════════════════════════════════════════════════════════════════════════════
AUTH_CFG = os.path.join(HERE, "seawolf-tools-auth.json")


def auth_leer():
    """Devuelve (token, activo). Si no hay archivo, crea una clave nueva."""
    try:
        d = json.load(open(AUTH_CFG, encoding="utf-8"))
        return str(d.get("token", "")), bool(d.get("activo", True))
    except Exception:
        pass
    tok = secrets.token_urlsafe(18)
    try:
        json.dump({"token": tok, "activo": True,
                   "creado": datetime.now().isoformat(timespec="seconds")},
                  open(AUTH_CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception:
        pass
    return tok, True


def auth_guardar(token=None, activo=None):
    """Cambia la clave o activa/desactiva la cerradura."""
    tok, act = auth_leer()
    if token is not None: tok = token
    if activo is not None: act = bool(activo)
    json.dump({"token": tok, "activo": act,
               "actualizado": datetime.now().isoformat(timespec="seconds")},
              open(AUTH_CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return tok, act


PAGINA_CLAVE = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Seawolf Tools - clave</title>
<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
background:radial-gradient(1100px 560px at 50% -8%,#122b2b,#0b1414 58%,#070f0f);color:#e6fbfb;
font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.c{border:1px solid #1e3434;border-radius:14px;padding:26px 28px;background:#101d1d;width:370px}
h1{font-size:18px;margin:0 0 4px}b{color:#4CE8E7}.s{color:#7fa8a8;font-size:12.5px;margin-bottom:14px}
input{width:100%;padding:11px 12px;border-radius:9px;border:1px solid #1e3434;background:#0b1414;
color:#e6fbfb;font:inherit;font-size:14px;box-sizing:border-box}
button{margin-top:11px;width:100%;padding:11px;border-radius:9px;border:0;background:#4CE8E7;
color:#04120f;font:inherit;font-weight:700;font-size:14px;cursor:pointer}
.err{color:#ff4d4d;font-size:12.5px;margin-top:9px}</style></head><body>
<form class="c" method="GET" action="/"><h1>SEAWOLF <b>TOOLS</b></h1>
<div class="s">Aplicativo protegido. Escriba su clave de acceso.</div>
<input name="k" type="password" placeholder="Clave de acceso" autofocus autocomplete="off">
<button type="submit">Entrar</button>__ERR__</form></body></html>"""


def auth_pagina(error=False):
    return PAGINA_CLAVE.replace("__ERR__", '<div class="err">Clave incorrecta.</div>' if error else "")


# ════════════════════════════════════════════════════════════════════════════
#  RENOMBRADOR SEAWOLF — motor de reglas con vista previa, registro y deshacer
#  Regla de oro: NADA se renombra sin ver antes el resultado y sin poder volver.
# ════════════════════════════════════════════════════════════════════════════
REN_UNDO = os.path.join(HERE, "seawolf-renombrador-undo.json")
REN_HIST = os.path.join(HERE, "seawolf-renombrador-historial.jsonl")
VIDEO_EXT = {".mkv", ".mp4", ".avi", ".mov", ".wmv", ".flv", ".m4v", ".mpg", ".mpeg", ".ts", ".webm"}

# ── Catálogo de reglas. Cada una lleva su DESCRIPCION (para uso de terceros) ──
REGLAS_CATALOGO = [
 {"id": "fecha", "nombre": "Quitar fechas",
  "desc": "Elimina fechas de publicacion que traen los archivos de serie al principio: "
          "(1989-12-17), (2019), [1990-01-14]. Es la regla que resuelve las fechas originales.",
  "ejemplo": "(1989-12-17) The Simpsons - S01E01.mkv  ->  The Simpsons - S01E01.mkv"},
 {"id": "parentesis", "nombre": "Quitar parentesis",
  "desc": "Elimina TODO lo que este entre parentesis, incluidos los parentesis: "
          "(1080p), (RE-EDIT), (Dual Latino), (2020).",
  "ejemplo": "El Padrino (2020) (RE-EDIT).mkv  ->  El Padrino.mkv"},
 {"id": "corchetes", "nombre": "Quitar corchetes",
  "desc": "Elimina TODO lo que este entre corchetes, incluidos los corchetes: "
          "[Erai-raws], [1080p], [MultiSub].",
  "ejemplo": "[Erai-raws] One Punch Man - 01.mkv  ->  One Punch Man - 01.mkv"},
 {"id": "llaves", "nombre": "Quitar llaves",
  "desc": "Elimina TODO lo que este entre llaves { }: {tmdb-12345}, {tvdb-99}.",
  "ejemplo": "Serie (2024) {tvdb-99}.mkv  ->  Serie (2024).mkv"},
 {"id": "borrar", "nombre": "Borrar combinaciones",
  "desc": "Borra de una lista de textos exactos que usted escriba. Separelos con coma. "
          "Util para quitar la firma del uploader, el idioma o la calidad.",
  "ejemplo": "Entrada:  By MrX, DUAL, 1080p    ·    Archivo.mkv By MrX  ->  Archivo.mkv"},
 {"id": "reemplazar", "nombre": "Reemplazar combinaciones",
  "desc": "Cambia un texto por otro. Formato: VIEJO>NUEVO, separados por coma. "
          "Util para cambiar puntos por espacios o guiones bajos por espacios.",
  "ejemplo": "Entrada:  .> , _>     ·    Serie.S01E01.mkv  ->  Serie S01E01.mkv"},
 {"id": "anio_final", "nombre": "Anio al final (peliculas)",
  "desc": "Mueve el anio que esta al principio hacia el final, entre parentesis. "
          "Es el formato canonico de peliculas para Jellyfin y Plex.",
  "ejemplo": "(2019) Parasitos 1080p.mkv  ->  Parasitos 1080p (2019).mkv"},
 {"id": "espacios", "nombre": "Limpiar espacios y bordes",
  "desc": "Junta espacios repetidos y quita guiones, puntos y espacios sueltos que quedan "
          "al principio o al final despues de borrar cosas. Se recomienda dejarla ACTIVA siempre.",
  "ejemplo": "Serie  -  S01E01 -  .mkv  ->  Serie - S01E01.mkv"},
]

PRESETS = {
 "jellyfin_serie": {
   "nombre": "Jellyfin · Serie",
   "desc": "Deja los episodios como 'Serie - SxxEyy - Titulo.ext' (ingles, que es lo correcto: "
           "Jellyfin reconoce la serie por su titulo original y muestra los textos en el idioma "
           "que usted configure). Ademas renombra las carpetas 'Temporada NN' a 'Season NN', "
           "que es lo que Jellyfin espera: con 'Temporada NN' crea temporadas duplicadas o vacias.",
   "reglas": ["fecha", "espacios"], "carpetas": True},
 "jellyfin_pelicula": {
   "nombre": "Jellyfin · Pelicula",
   "desc": "Deja las peliculas como 'Titulo (Anio).ext', quitando la calidad, el idioma y la firma "
           "del uploader. Formato canonico de Jellyfin y Plex.",
   "reglas": ["anio_final", "parentesis", "corchetes", "llaves", "espacios"], "carpetas": False},
 "limpiar_todo": {
   "nombre": "Limpiar todo (general)",
   "desc": "Quita fechas, parentesis, corchetes y llaves de cualquier archivo. Util como primera "
           "pasada cuando todavia no sabe que reglas quiere.",
   "reglas": ["fecha", "parentesis", "corchetes", "llaves", "espacios"], "carpetas": False},
}


def _ren_lista(v):
    """Convierte 'a, b, c' en ['a','b','c'] limpio."""
    return [x.strip() for x in str(v or "").split(",") if x.strip()]


def _ren_regla(n, r):
    """Aplica UNA regla a un nombre (sin extension)."""
    t = r.get("id"); v = r.get("valor", "")
    if t == "fecha":
        n = re.sub(r"[\(\[]\s*\d{4}([-/.]\d{1,2}){0,2}\s*[\)\]]", " ", n)
    elif t == "parentesis":
        n = re.sub(r"\([^)]*\)", " ", n)
    elif t == "corchetes":
        n = re.sub(r"\[[^\]]*\]", " ", n)
    elif t == "llaves":
        n = re.sub(r"\{[^}]*\}", " ", n)
    elif t == "borrar":
        for w in _ren_lista(v):
            n = n.replace(w, " ")
    elif t == "reemplazar":
        for par in str(v or "").split(","):          # NO se recorta el lado derecho,
            if ">" in par:                            # asi  ".> "  (con espacio) = reemplazar por espacio
                a, b = par.split(">", 1)
                a = a.strip(); b = b.rstrip("\r\n")
                if a:
                    n = n.replace(a, b)
    elif t == "anio_final":
        m = re.match(r"^[\(\[]\s*(\d{4})\s*[\)\]]\s*", n)
        if m:
            n = n[m.end():].strip()
            n = f"{n} ({m.group(1)})"
    elif t == "espacios":
        n = re.sub(r"\s*-\s*(?=-)", "", n)
        n = re.sub(r"\s{2,}", " ", n)
    return n


def _ren_nuevo_nombre(archivo, reglas):
    """Aplica todas las reglas al nombre SIN tocar la extension. Devuelve el nombre nuevo."""
    base, ext = os.path.splitext(archivo)
    n = base
    for r in reglas:
        n = _ren_regla(n, r)
    n = re.sub(r"\s{2,}", " ", n)
    n = re.sub(r"^[\s\-_.]+", "", n)
    n = re.sub(r"[\s\-_.]+$", "", n)
    n = n.strip()
    if not n:
        return archivo          # nunca dejar un archivo sin nombre
    return n + ext


def ren_plan(carpeta, reglas, solo_video=False, limite=6000):
    """Calcula el plan COMPLETO (viejo -> nuevo) sin tocar un solo archivo."""
    if not carpeta or not os.path.isdir(carpeta):
        return [], 0, False, "La carpeta no existe"
    plan, total = [], 0
    truncado = False
    for dirpath, dirnames, filenames in os.walk(carpeta):
        dirnames[:] = [d for d in dirnames if d.lower() not in SKIP_DIRS]
        for f in filenames:
            total += 1
            if solo_video and os.path.splitext(f)[1].lower() not in VIDEO_EXT:
                continue
            nuevo = _ren_nuevo_nombre(f, reglas)
            if nuevo != f:
                plan.append([os.path.join(dirpath, f), os.path.join(dirpath, nuevo)])
                if len(plan) >= limite:
                    truncado = True
                    return plan, total, truncado, ""
    return plan, total, truncado, ""


def ren_preview(carpeta, reglas, solo_video=False):
    """Vista previa: que cambiaria, SIN cambiar nada. Devuelve las primeras 300 filas."""
    plan, total, truncado, err = ren_plan(carpeta, reglas, solo_video)
    return {"ok": not err, "msg": err, "total": total, "cambian": len(plan), "truncado": truncado,
            "muestra": [{"antes": os.path.basename(a), "despues": os.path.basename(b),
                         "dir": os.path.dirname(a)} for a, b in plan[:300]]}


def ren_aplicar(carpeta, reglas, solo_video=False):
    """Aplica el plan y deja registro con DESHACER. Nunca pisa un archivo existente."""
    plan, total, truncado, err = ren_plan(carpeta, reglas, solo_video)
    if err:
        return {"ok": 0, "msg": err}
    hechos, errores = [], []
    for viejo, nuevo in plan:
        try:
            if os.path.exists(nuevo):
                errores.append([os.path.basename(viejo), "ya existe el destino"]); continue
            os.rename(viejo, nuevo)
            hechos.append([viejo, nuevo])
        except Exception as e:
            errores.append([os.path.basename(viejo), str(e)[:90]])
    if hechos:
        sello = hashlib.sha256(json.dumps(hechos, ensure_ascii=False).encode()).hexdigest()[:16]
        op = {"fecha": datetime.now().isoformat(timespec="seconds"), "carpeta": carpeta,
              "tipo": "archivos", "n": len(hechos), "sello": sello, "pares": hechos}
        json.dump(op, open(REN_UNDO, "w", encoding="utf-8"), ensure_ascii=False)
        with open(REN_HIST, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({k: v for k, v in op.items() if k != "pares"},
                                ensure_ascii=False) + "\n")
    return {"ok": len(hechos), "total": total, "errores": errores[:15],
            "total_errores": len(errores), "truncado": truncado}


def ren_aplicar_lote(carpetas, reglas, solo_video=False):
    """Aplica las reglas a VARIAS carpetas y deja UN SOLO registro de deshacer con todo.

    Pensado para lotes: 'las 42 carpetas de esta serie'. Si fallara algo, el DESHACER
    devuelve TODO el lote de una vez, no solo la ultima carpeta."""
    pares, errores, revisados = [], [], 0
    for c in (carpetas or []):
        plan, total, _trunc, err = ren_plan(c, reglas, solo_video)
        revisados += total
        if err:
            errores.append([str(c), err]); continue
        for viejo, nuevo in plan:
            try:
                if os.path.exists(nuevo):
                    errores.append([os.path.basename(viejo), "ya existe el destino"]); continue
                os.rename(viejo, nuevo)
                pares.append([viejo, nuevo])
            except Exception as e:
                errores.append([os.path.basename(viejo), str(e)[:90]])
    if pares:
        sello = hashlib.sha256(json.dumps(pares, ensure_ascii=False).encode()).hexdigest()[:16]
        op = {"fecha": datetime.now().isoformat(timespec="seconds"),
              "carpeta": f"LOTE de {len(carpetas)} carpetas", "tipo": "archivos",
              "n": len(pares), "sello": sello, "pares": pares}
        json.dump(op, open(REN_UNDO, "w", encoding="utf-8"), ensure_ascii=False)
        with open(REN_HIST, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({k: v for k, v in op.items() if k != "pares"},
                                ensure_ascii=False) + "\n")
    return {"ok": len(pares), "revisados": revisados, "carpetas": len(carpetas or []),
            "errores": errores[:15], "total_errores": len(errores)}


def ren_carpetas_preview(carpeta):
    """Busca carpetas tipo 'Temporada 01' / 'Temporada 1' y propone 'Season 01'."""
    if not carpeta or not os.path.isdir(carpeta):
        return {"ok": False, "msg": "La carpeta no existe", "muestra": [], "cambian": 0}
    plan = []
    for dirpath, dirnames, _ in os.walk(carpeta):
        for d in dirnames:
            m = re.match(r"^(?:temporada|season|temp)\s*0*(\d{1,3})$", d.strip(), re.I)
            if m:
                nuevo = f"Season {int(m.group(1)):02d}"
                if nuevo != d:
                    plan.append([os.path.join(dirpath, d), os.path.join(dirpath, nuevo)])
    plan.sort(key=lambda p: -p[0].count(os.sep))      # las mas profundas primero
    return {"ok": True, "msg": "", "cambian": len(plan),
            "muestra": [{"antes": os.path.basename(a), "despues": os.path.basename(b),
                         "dir": os.path.dirname(a)} for a, b in plan[:100]]}


def ren_carpetas(carpeta):
    """Renombra de verdad las carpetas de temporada (profundas primero)."""
    pv = ren_carpetas_preview(carpeta)
    if not pv.get("ok") or not pv["cambian"]:
        return {"ok": 0, "msg": pv.get("msg") or "No hay carpetas de temporada que renombrar"}
    plan, hechos, errores = [], [], []
    for dirpath, dirnames, _ in os.walk(carpeta):     # recalcular completo (no solo la muestra)
        for d in dirnames:
            m = re.match(r"^(?:temporada|season|temp)\s*0*(\d{1,3})$", d.strip(), re.I)
            if m:
                nuevo = f"Season {int(m.group(1)):02d}"
                if nuevo != d:
                    plan.append([os.path.join(dirpath, d), os.path.join(dirpath, nuevo)])
    plan.sort(key=lambda p: -p[0].count(os.sep))
    for viejo, nuevo in plan:
        try:
            if os.path.exists(nuevo):
                errores.append([os.path.basename(viejo), "ya existe"]); continue
            os.rename(viejo, nuevo); hechos.append([viejo, nuevo])
        except Exception as e:
            errores.append([os.path.basename(viejo), str(e)[:90]])
    if hechos:
        sello = hashlib.sha256(json.dumps(hechos, ensure_ascii=False).encode()).hexdigest()[:16]
        op = {"fecha": datetime.now().isoformat(timespec="seconds"), "carpeta": carpeta,
              "tipo": "carpetas", "n": len(hechos), "sello": sello, "pares": hechos}
        json.dump(op, open(REN_UNDO, "w", encoding="utf-8"), ensure_ascii=False)
        with open(REN_HIST, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({k: v for k, v in op.items() if k != "pares"},
                                ensure_ascii=False) + "\n")
    return {"ok": len(hechos), "errores": errores[:15], "total_errores": len(errores)}


def ren_estado():
    """La ultima operacion, para el aviso de DESHACER."""
    if os.path.exists(REN_UNDO):
        try:
            d = json.load(open(REN_UNDO, encoding="utf-8"))
            return {k: d[k] for k in ("fecha", "carpeta", "tipo", "n", "sello") if k in d}
        except Exception:
            return None
    return None


def ren_deshacer():
    """Revierte la ultima operacion registrada. Un solo nivel, a proposito."""
    if not os.path.exists(REN_UNDO):
        return {"ok": 0, "msg": "No hay operacion reciente que deshacer"}
    try:
        d = json.load(open(REN_UNDO, encoding="utf-8"))
    except Exception:
        return {"ok": 0, "msg": "El registro esta danado"}
    ok, err = 0, []
    for viejo, nuevo in reversed(d.get("pares", [])):
        try:
            if os.path.exists(nuevo) and not os.path.exists(viejo):
                os.rename(nuevo, viejo); ok += 1
            else:
                err.append(os.path.basename(nuevo))
        except Exception as e:
            err.append(str(e)[:60])
    os.remove(REN_UNDO)
    with open(REN_HIST, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"fecha": datetime.now().isoformat(timespec="seconds"),
                             "deshecho": True, "n": ok}, ensure_ascii=False) + "\n")
    return {"ok": ok, "errores": err[:10], "msg": f"Deshechos {ok} de {d.get('n', 0)}"}


def ren_reglas_de(sel):
    """Traduce la seleccion del usuario en la lista de reglas ordenada."""
    orden = [r["id"] for r in REGLAS_CATALOGO]
    vals = {r["id"]: r.get("valor", "") for r in REGLAS_CATALOGO}
    out = []
    for r in (sel or []):
        rid = r.get("id") if isinstance(r, dict) else r
        val = r.get("valor", "") if isinstance(r, dict) else vals.get(rid, "")
        if rid in orden:
            out.append({"id": rid, "valor": val})
    out.sort(key=lambda r: orden.index(r["id"]))
    if not any(r["id"] == "espacios" for r in out):
        out.append({"id": "espacios", "valor": ""})
    return out


def _ren_reglas_req(d):
    """Combina la seleccion de reglas (sel) con los textos que escribio el usuario (valores)."""
    reglas = ren_reglas_de(d.get("sel") or [])
    vals = d.get("valores") or {}
    for r in reglas:
        v = str(vals.get(r["id"], "") or "")
        if v.strip():
            r["valor"] = v
    return reglas


HTML = r"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seawolf Tools</title>
<style>
:root{--sw:#4CE8E7;--sw2:#48E8D8;--ok:#48E8A0;--bad:#ff4d4d;--warn:#ffb86b;--bd:#1e3434;--fg:#e6fbfb;--mut:#7fa8a8;--card:#101d1d}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(1100px 560px at 50% -8%,#122b2b,#0b1414 58%,#070f0f);color:var(--fg);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{width:1240px;max-width:97vw;margin:0 auto;padding:16px 20px 40px}
h1{font-size:21px;margin:0}.b{color:var(--sw);text-shadow:0 0 14px rgba(76,232,231,.4)}.sub{color:var(--mut);font-size:12.5px;margin:2px 0 12px}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}.chip{border:1px solid var(--bd);border-radius:10px;padding:8px 12px;background:var(--card);font-size:12.5px}.chip b{color:var(--sw);font-size:15px}
.drives{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}.drv{border:1px solid var(--bd);border-radius:9px;padding:6px 10px;background:var(--card);font-size:12px;min-width:150px}
.drv .bar{height:6px;border-radius:4px;background:#0a1f1f;margin-top:5px;overflow:hidden}.drv .bar i{display:block;height:100%;background:linear-gradient(90deg,var(--sw2),var(--sw))}
.tabs{display:flex;gap:6px;margin:6px 0 12px;flex-wrap:wrap}.tab{border:1px solid var(--bd);background:transparent;color:var(--mut);padding:7px 13px;border-radius:8px;font:inherit;font-size:12.5px;cursor:pointer}
.tab.on{background:var(--sw);color:#04120f;border-color:var(--sw);font-weight:700}
.tools{display:flex;gap:8px;margin-bottom:10px;align-items:center}input[type=search],input[type=text]{flex:1;padding:8px 10px;border-radius:8px;border:1px solid var(--bd);background:var(--card);color:var(--fg);font:inherit;font-size:13px}
.spin{width:14px;height:14px;border:2px solid var(--bd);border-top-color:var(--sw);border-radius:50%;display:inline-block;animation:sp .8s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}
table{border-collapse:collapse;width:100%;font-size:12.5px}th,td{padding:7px 9px;border-bottom:1px solid var(--bd);text-align:left}th{color:var(--sw);font-size:11px;text-transform:uppercase;cursor:pointer}
tr:hover td{background:rgba(76,232,231,.05)}.size{color:var(--sw);white-space:nowrap}.path{word-break:break-all;color:var(--mut)}.dv{color:var(--sw2)}
button{font:inherit;cursor:pointer;border-radius:7px;font-size:12px;padding:5px 10px;border:1px solid var(--bd);background:transparent;color:var(--fg)}button.sw{background:var(--sw);color:#04120f;border-color:var(--sw);font-weight:600}button.bad{border-color:var(--bad);color:var(--bad)}button:hover{transform:translateY(-1px)}
.card{border:1px solid var(--bd);border-radius:11px;padding:12px 13px;background:var(--card);margin-bottom:10px}
.tree{display:flex;flex-wrap:wrap;gap:6px}.tf{border:1px solid var(--bd);border-radius:8px;padding:8px 10px;background:#0d1a1a;font-size:12px;min-width:120px}
.tf b{display:block;color:var(--sw);font-size:14px}.tf .n{color:var(--mut);font-size:11px;word-break:break-all}
.toast{position:fixed;right:18px;bottom:18px;background:#04120f;border:1px solid var(--sw);color:var(--sw);border-radius:10px;padding:10px 14px;font-size:13px;opacity:0;transform:translateY(10px);transition:.25s;z-index:9}.toast.on{opacity:1;transform:translateY(0)}
.empty{color:var(--mut);font-size:13px;padding:14px 0}
.warn{border:1px solid var(--warn);background:rgba(255,184,107,.08);border-radius:10px;padding:10px 12px;font-size:12.5px;margin:9px 0;color:#ffd9ad;line-height:1.5}
.danger{border:2px solid var(--bad);background:rgba(255,77,77,.10);border-radius:10px;padding:11px 13px;font-size:12.5px;margin:10px 0;color:#ffc9c9;line-height:1.55}
.danger b{color:var(--bad)}
.good{border:1px solid var(--ok);background:rgba(72,232,160,.08);border-radius:10px;padding:10px 12px;font-size:12.5px;margin:9px 0;color:#b6f5d6;line-height:1.5}
.pill{display:inline-block;border-radius:20px;padding:2px 9px;font-size:11px;border:1px solid var(--bd);white-space:nowrap}
.pill.g{color:var(--ok);border-color:var(--ok)}.pill.y{color:var(--warn);border-color:var(--warn)}
.pill.r{color:var(--bad);border-color:var(--bad)}.pill.n{color:var(--mut)}
.saludgrid{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.dsk{border:1px solid var(--bd);border-radius:10px;padding:9px 11px;background:#0d1a1a;min-width:250px;flex:1}
.dsk b{color:var(--sw);display:block;font-size:13px}
.dsk .m{color:var(--mut);font-size:11px;margin:2px 0 6px}
button:disabled{opacity:.4;cursor:not-allowed}
</style></head><body><div class="wrap">
<h1>SEAWOLF <span class="b">TOOLS</span></h1><div class="sub">Pesados · Mapa · Duplicados · Mantenimiento · REA · ✏️ Renombrador · 🩺 Salud · Papelera. Nada se borra ni se cambia sin tu orden. <b style="color:var(--warn)">Los módulos de disco son zona delicada: lean las advertencias antes de ejecutar.</b></div>
<div class="chips" id="chips"></div><div class="drives" id="drives"></div>
<div class="tabs">
<button class="tab on" data-t="heavy">🔥 Pesados</button><button class="tab" data-t="map">🗺️ Mapa</button>
<button class="tab" data-t="dupes">🧬 Duplicados</button><button class="tab" data-t="mant">🛠️ Mantenimiento</button>
<button class="tab" data-t="rea">🔎 REA</button><button class="tab" data-t="ren">✏️ Renombrador</button>
<button class="tab" data-t="salud">🩺 Salud</button>
<button class="tab" data-t="bin">🗑️ Papelera</button>
<button class="tab" id="rescan">↻ Re-escanear</button></div>
<div class="tools"><input type="search" id="q" placeholder="Filtrar por nombre, extensión o disco…"><span id="selinfo" class="sub"></span><button class="sw" id="b-trash">♻️ Mover marcados</button><button class="bad" id="b-hard">💀 Borrar marcados</button><span id="stat" class="sub"></span></div>
<div id="view"></div></div><div class="toast" id="toast"></div>
<script>
var S={busy:true,heavy:[],dupes:[],bin:[],drives:[],map:[],manten:[],rea:null,tab:'heavy',q:'',sort:'size',desc:true,scanned:0,sel:{},renreglas:[],renpresets:{},rensel:['fecha'],renvals:{},rencar:'',renprev:null,renundo:null,rencv:null,salud:null,saludBusy:false,saludMsg:null};
function H(t){var e=document.getElementById('toast');e.textContent=t;e.classList.add('on');setTimeout(function(){e.classList.remove('on')},1900);}
function humanaB(n){if(n<1024)return n+' B';var u=['KB','MB','GB','TB'],i=-1;do{n/=1024;i++}while(n>=1024&&i<3);return n.toFixed(1)+' '+u[i];}
/* esc(): neutraliza caracteres peligrosos antes de pintar NOMBRES DE ARCHIVO en el HTML.
   Un archivo llamado "<script>..." no debe ejecutarse en el navegador del usuario. */
function esc(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function selInfo(){var n=0,by=0;for(var k in S.sel){n++;var f=S.heavy.find(function(x){return x.p===k;});if(f)by+=f.size;}var e=document.getElementById('selinfo');if(e)e.innerHTML=n?('<b style="color:var(--sw)">'+n+'</b> marcados · <b style="color:var(--sw)">'+humanaB(by)+'</b>'):'';}
async function enviarSel(hard){var ps=Object.keys(S.sel);if(!ps.length){H('Nada marcado');return;}
 if(hard&&!confirm('BORRADO PERMANENTE de '+ps.length+' archivos. Sin vuelta atrás. ¿Confirmas?'))return;
 if(!hard&&!confirm('Mover '+ps.length+' archivos a la Papelera Seawolf?'))return;
 H(hard?'Borrando…':'Moviendo…');
 await fetch('/mover-muchos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({paths:ps,hard:hard})});
 S.sel={};H('Hecho');refrescar();}
async function refrescar(){try{var r=await fetch('/api/state');var j=await r.json();Object.assign(S,j);draw();if(S.busy)setTimeout(refrescar,1500);}catch(e){}}
function draw(){
 document.getElementById('chips').innerHTML='<div class="chip">Analizados <b>'+S.scanned+'</b></div><div class="chip">Total <b>'+(S.totalH||'—')+'</b></div><div class="chip">Desperdicio <b style="color:var(--warn)">'+(S.wasteH||'—')+'</b></div><div class="chip">'+(S.busy?'<span class="spin"></span> analizando…':'✔ listo')+'</div>';
 document.getElementById('drives').innerHTML=(S.drives||[]).map(function(d){var p=d.total?Math.round(100*d.used/d.total):0;return '<div class="drv"><b class="dv">'+d.root+'</b> '+d.scannedS+' de '+d.totalH+' · libre '+d.freeH+'<div class="bar"><i style="width:'+p+'%"></i></div></div>';}).join('');
 document.getElementById('stat').textContent=S.tab+(S.tab==='heavy'?' → '+S.heavy.length+' archivos':'');
 var v=document.getElementById('view'),q=S.q.toLowerCase();
 if(S.tab==='heavy'){var a=S.heavy.filter(function(f){return !q||f.p.toLowerCase().indexOf(q)>=0;});
  a.sort(function(x,y){var k=S.sort,r=(k==='name')?x.p.localeCompare(y.p):(x.size-y.size);return S.desc?-r:r;});
  var h='<table><thead><tr><th style="width:30px"><input type="checkbox" id="ck-all" title="Marcar visibles"></th><th data-s="size">Tamaño</th><th>Disco</th><th data-s="name">Archivo</th></tr></thead><tbody>';
  a.slice(0,400).forEach(function(f){h+='<tr><td><input type="checkbox" class="ck" data-p="'+encodeURIComponent(f.p)+'"'+(S.sel[f.p]?' checked':'')+'></td><td class="size">'+f.h+'</td><td class="dv">'+f.drv+'</td><td class="path">'+f.p+'</td></tr>';});
  h+='</tbody></table>';
  v.innerHTML=h;selInfo();
 } else if(S.tab==='map'){
  if(!S.map.length){v.innerHTML='<div class="empty">Sin datos (o aún analizando…).</div>';return;}
  var h='';S.map.forEach(function(d){h+='<div class="card"><h3 style="margin:0 0 8px;color:var(--sw2)">'+d.root+' — '+d.totalH+'</h3><div class="tree">';
   d.folders.forEach(function(f){h+='<div class="tf" style="flex-grow:'+Math.max(1,Math.round(f.pct))+'"><b>'+f.h+'</b><span class="n">'+f.n+' ('+f.pct+'%)</span></div>';});
   h+='</div></div>';});v.innerHTML=h;
 } else if(S.tab==='dupes'){
  if(!S.dupes.length){v.innerHTML='<div class="empty">Sin duplicados.</div>';return;}
  var h='';S.dupes.forEach(function(g,i){h+='<div class="card"><h3>Grupo '+(i+1)+' — '+g.files.length+' copias · '+g.h+' c/u · desperdicia '+g.wasteH+'</h3><div style="margin-bottom:6px"><button class="sw" data-keep="'+i+'">Mover copias (dejar 1)</button></div>';
   g.files.forEach(function(p){h+='<div style="font-size:12.5px;display:flex;justify-content:space-between;gap:10px;padding:3px 0;border-bottom:1px dashed var(--bd)"><span class="path">'+p+'</span><button data-p="'+encodeURIComponent(p)+'">Mover</button></div>';});h+='</div>';});v.innerHTML=h;
 } else if(S.tab==='mant'){
  var h='<div class="card"><h3>🛠️ Mantenimiento programado (editable)</h3><div class="sub">Activa/desactiva, edita días y horario. "Ejecutar" corre la tarea ahora.</div>';
  S.manten.forEach(function(t){h+='<div style="border-top:1px dashed var(--bd);padding:8px 0"><b>'+(t.activo?'🟢':'⚪')+' '+t.nombre+'</b><div class="sub">'+t.desc+'</div>'+
   '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px"><button data-toggle="'+t.id+'">'+(t.activo?'Desactivar':'Activar')+'</button>'+
   '<button data-dias="'+t.id+'">Días: '+t.dias+'</button><button data-hor="'+t.id+'">'+t.horario+'</button><button class="sw" data-run="'+t.id+'">Ejecutar</button></div></div>';});
  v.innerHTML=h+'</div>';
 } else if(S.tab==='ren'){
  var rg=S.renreglas||[],ps=S.renpresets||{},sel=S.rensel||[];
  var VAL={borrar:'Textos a borrar, separados por coma.  Ej: By MrX, DUAL, 1080p',
           reemplazar:'VIEJO>NUEVO separados por coma.  Ej: .> , _>   (el lado derecho vacio con un espacio = poner un espacio)'};
  var h='<div class="card"><h3>✏️ Renombrador Seawolf</h3><div class="sub">Renombra archivos en masa. SIEMPRE le muestra el ANTES y el DESPUES antes de tocar nada, y toda operacion se puede DESHACER con un boton. Nunca pisa un archivo que ya exista.</div>'
   +'<div class="tools"><input type="text" id="rencar" placeholder="Carpeta a trabajar   (ej: H:\\caida)" value="'+(S.rencar||'')+'"><button class="sw" data-ren="prev">👁 Ver vista previa</button></div>';
  h+='<div style="margin:14px 0 6px"><b>Atajos</b> <span class="sub">— un clic configura las reglas solas:</span></div><div style="display:flex;gap:6px;flex-wrap:wrap">';
  for(var k in ps){h+='<button data-renpreset="'+k+'">🎯 '+ps[k].nombre+'</button>';}
  h+='</div>';
  if(S.renpresets_hint)h+='<div class="sub" style="margin-top:6px">'+S.renpresets_hint+'</div>';
  h+='<div style="margin:16px 0 4px"><b>Reglas</b> <span class="sub">— marque las que quiera. Cada una explica que hace:</span></div>';
  rg.forEach(function(r){
   h+='<div style="border-top:1px dashed var(--bd);padding:9px 0"><label style="display:flex;gap:9px;align-items:flex-start;cursor:pointer">'
    +'<input type="checkbox" class="renck" data-id="'+r.id+'"'+(sel.indexOf(r.id)>=0?' checked':'')+' style="margin-top:3px">'
    +'<span><b>'+r.nombre+'</b><div class="sub" style="margin:3px 0 0">'+r.desc+'</div>'
    +'<div style="font-size:11.5px;color:var(--sw2);margin-top:3px">Ejemplo:  '+r.ejemplo+'</div></span></label>';
   if(VAL[r.id]){h+='<input type="text" class="renval" data-id="'+r.id+'" placeholder="'+VAL[r.id]+'" value="'+((S.renvals||{})[r.id]||'')+'" style="margin:7px 0 0 23px;width:calc(100% - 23px)">';}
   h+='</div>';
  });
  h+='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;align-items:center">'
   +'<button class="sw" data-ren="aplicar">✔ APLICAR a los archivos</button>'
   +'<button class="bad" data-ren="deshacer">↩ DESHACER la ultima operacion</button>'
   +(S.renundo?('<span class="sub">Ultima: <b>'+S.renundo.n+'</b> '+S.renundo.tipo+' · '+S.renundo.fecha+' · sello '+S.renundo.sello+'</span>'):'<span class="sub">Sin operaciones recientes que deshacer</span>')
   +'</div>';
  h+='<div style="border-top:1px solid var(--bd);margin-top:16px;padding-top:12px"><b>📁 Carpetas de temporada</b>'
   +'<div class="sub">Cambia "Temporada 01" por "Season 01". Jellyfin espera "Season NN": con "Temporada NN" crea temporadas duplicadas o vacias.</div>'
   +'<div style="display:flex;gap:8px;margin-top:9px;flex-wrap:wrap"><button data-ren="cvprev">👁 Ver qué carpetas cambiarían</button><button class="sw" data-ren="cvap">✔ Renombrar a Season NN</button></div>';
  if(S.rencv&&S.rencv.muestra&&S.rencv.muestra.length){
   h+='<div class="sub" style="margin-top:8px"><b>'+S.rencv.cambian+'</b> carpetas:</div><table><thead><tr><th>ANTES</th><th>DESPUES</th><th>UBICACION</th></tr></thead><tbody>';
   S.rencv.muestra.slice(0,40).forEach(function(m){h+='<tr><td>'+esc(m.antes)+'</td><td class="size">'+esc(m.despues)+'</td><td class="path">'+esc(m.dir)+'</td></tr>';});
   h+='</tbody></table>';
  }
  h+='</div>';
  if(S.renprev){
   if(!S.renprev.ok){h+='<div class="card" style="border-color:var(--bad)">'+(S.renprev.msg||'Error')+'</div>';}
   else{
    h+='<div style="border-top:1px solid var(--bd);margin-top:16px;padding-top:12px"><b>👁 Vista previa</b> <span class="sub">— <b style="color:var(--sw)">'+S.renprev.cambian+'</b> de '+S.renprev.total+' archivos cambiarian'+(S.renprev.truncado?' (lista recortada)':'')+'</span>';
    if(S.renprev.muestra&&S.renprev.muestra.length){
     h+='<table><thead><tr><th>ANTES</th><th>DESPUES</th></tr></thead><tbody>';
     S.renprev.muestra.slice(0,150).forEach(function(m){h+='<tr><td class="path">'+esc(m.antes)+'</td><td class="size">'+esc(m.despues)+'</td></tr>';});
     h+='</tbody></table>';
    }
    if(S.renprev.cambian)h+='<div style="margin-top:10px"><button class="sw" data-ren="aplicar">✔ APLICAR estos '+S.renprev.cambian+' cambios</button></div>';
    h+='</div>';
   }
  }
  v.innerHTML=h+'</div>';
 } else if(S.tab==='salud'){
  var h='<div class="card"><h3>🩺 Salud del equipo</h3>'
   +'<div class="sub">Analiza el hierro: discos, espacio, memoria y arranque. <b style="color:var(--ok)">Analizar es SOLO LECTURA</b>: no cambia ni borra nada.</div>'
   +'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><button class="sw" data-salud="analizar">'
   +(S.saludBusy?'<span class="spin"></span> analizando…':'🔍 Analizar el equipo')+'</button></div></div>';
  if(S.saludMsg){h+='<div class="'+(S.saludMsg.ok?'good':'warn')+'">'+esc(S.saludMsg.texto)+'</div>';}
  if(!S.salud){v.innerHTML=h+'<div class="warn">Pulse <b>Analizar el equipo</b>. La primera lectura tarda unos segundos porque consulta el hardware de verdad.</div>';return;}
  var Z=S.salud, esc2=esc;
  h+='<div class="danger">🚨 <b>ZONA DELICADA</b><br>'+esc2(Z.aviso_general||'')+'</div>';
  if(Z.avisos&&Z.avisos.length){
   h+='<div class="card"><h3>⚠️ Avisos ('+Z.avisos.length+')</h3>';
   Z.avisos.forEach(function(a){h+='<div class="warn">• '+esc2(a)+'</div>';});
   h+='</div>';
  } else {h+='<div class="good">✔ Sin avisos: discos sanos y espacio suficiente.</div>';}
  h+='<div class="card"><h3>💽 Discos ('+Z.resumen.discos+') — '+Z.resumen.ssd+' SSD · '+Z.resumen.hdd+' HDD</h3>'
   +'<div class="sub">El TIPO de disco decide el mantenimiento. Nunca al revés.</div><div class="saludgrid">';
  (Z.discos||[]).forEach(function(d){
   var cl=d.riesgo==='recomendado'?'g':(d.riesgo==='cuidado'?'y':'r');
   h+='<div class="dsk"><b>'+esc2(d.modelo)+'</b><div class="m">'+d.gb+' GB · '+esc2(d.bus)+' · salud '+esc2(d.salud)+' · '+esc2(d.estado)+'</div>'
    +'<span class="pill '+cl+'">'+esc2(d.tipo)+'</span> <span class="pill '+(d.riesgo==='prohibido'?'r':'n')+'">'+esc2(d.mantenimiento)+'</span>'
    +'<div class="sub" style="margin-top:7px">'+esc2(d.motivo)+'</div></div>';
  });
  h+='</div></div>';
  h+='<div class="card"><h3>📦 Unidades y espacio</h3><div class="sub">Ordenadas de más a menos apretadas. Aquí saltan los avisos antes de que sea un problema.</div>'
   +'<table><thead><tr><th>Unidad</th><th>Disco</th><th>Total</th><th>Libre</th><th>%</th><th>Le toca</th><th></th></tr></thead><tbody>';
  (Z.volumenes||[]).forEach(function(u){
   var cl2=u.riesgo==='recomendado'?'g':(u.riesgo==='cuidado'?'y':'r');
   var puede=(u.riesgo!=='prohibido');
   h+='<tr><td><b class="dv">'+esc2(u.letra)+':</b>'+(u.aviso?(' <span class="pill '+(u.librePct<=10?'r':'y')+'">'+esc2(u.aviso)+'</span>'):'')+'</td>'
    +'<td>'+esc2(u.discoTipo)+' <span class="path">'+esc2((u.discoModelo||'').substring(0,18))+'</span></td>'
    +'<td class="size">'+u.totalGB+' GB</td><td class="size">'+u.libreGB+' GB</td><td class="size">'+u.librePct+'%</td>'
    +'<td><span class="pill '+cl2+'">'+esc2(u.mantenimiento)+'</span></td>'
    +'<td style="white-space:nowrap">'
    +'<button data-optim="'+esc2(u.letra)+'"'+(puede?'':' disabled title="Prohibido: disco extraíble o sin confirmar"')+'>⚡ Optimizar</button> '
    +'<button data-verif="'+esc2(u.letra)+'">🔍 Verificar</button></td></tr>';
  });
  h+='</tbody></table>'
   +'<div class="warn">⚡ <b>Optimizar</b>: en SSD hace TRIM · en HDD desfragmenta. <b>🔍 Verificar</b>: solo lectura (chkdsk /scan), no repara ni borra. Ambas pueden tardar y <b>NUNCA se interrumpen</b>. Necesitan permisos de administrador.</div>';
  if(Z.avisos_accion){
   h+='<div class="sub">Antes de ejecutar, lea: <b>'+esc2(Z.avisos_accion.optimizar_ssd)+'</b></div>';
   h+='<div class="warn" style="border-color:var(--bd)">'+esc2(Z.avisos_accion.optimizar_hdd)+'</div>';
  }
  h+='</div>';
  var c=Z.cpu||{};
  h+='<div class="card"><h3>🧠 Procesador y memoria</h3><div class="saludgrid">'
   +'<div class="dsk"><b>'+esc2(c.cpu||'—')+'</b><div class="m">'+c.nucleos+' núcleos · '+c.hilos+' hilos</div><span class="pill '+(c.carga>85?'r':(c.carga>60?'y':'g'))+'">carga '+c.carga+'%</span></div>'
   +'<div class="dsk"><b>Memoria RAM</b><div class="m">'+c.ramLibreGB+' GB libres de '+c.ramTotalGB+' GB</div><span class="pill '+(c.ramLibreGB<3?'r':(c.ramLibreGB<8?'y':'g'))+'">'+Math.round(100*c.ramLibreGB/Math.max(1,c.ramTotalGB))+'% libre</span></div>'
   +'</div></div>';
  h+='<div class="card"><h3>🗺️ Mapa de particiones <span class="pill n">SOLO LECTURA</span></h3>'
   +'<div class="warn">Este módulo <b>NO modifica particiones</b>. Cambiar particiones puede borrar un disco entero: para eso, una herramienta dedicada y con respaldo hecho.</div>'
   +'<table><thead><tr><th>Disco físico</th><th>Unidad</th><th>Tamaño</th><th>Tipo</th><th>Sistema</th></tr></thead><tbody>';
  (Z.particiones||[]).forEach(function(p){
   h+='<tr><td>#'+esc2(p.DiskNumber)+'</td><td><b class="dv">'+esc2(p.DriveLetter)+':</b></td><td class="size">'+p.GB+' GB</td>'
    +'<td>'+esc2(p.Type)+'</td><td>'+(p.IsBoot?'<span class="pill y">arranque</span> ':'')+(p.IsSystem?'<span class="pill n">sistema</span>':'')+'</td></tr>';
  });
  h+='</tbody></table></div>';
  h+='<div class="card"><h3>🚀 Arranque de Windows ('+(Z.arranque||[]).length+')</h3><div class="sub">Todo lo que arranca solo. Cada uno alarga el arranque y come memoria.</div>'
   +'<table><thead><tr><th>Programa</th><th>Ubicación</th></tr></thead><tbody>';
  (Z.arranque||[]).forEach(function(a){
   h+='<tr><td>'+esc2(a.nombre)+'</td><td class="path">'+esc2((a.ubicacion||'').substring(0,52))+'</td></tr>';
  });
  h+='</tbody></table><div class="warn">Para <b>desactivar</b> algo del arranque: Administrador de tareas (Ctrl+Shift+Esc) → pestaña <b>Inicio</b>. Aquí solo se muestra: no lo apagamos por usted.</div></div>';
  h+='<div class="card"><h3>📖 Qué hace cada función</h3>';
  (Z.funciones||[]).forEach(function(f){h+='<div style="border-top:1px dashed var(--bd);padding:8px 0"><b>'+esc2(f.nombre)+'</b><div class="sub" style="margin-top:3px">'+esc2(f.desc)+'</div></div>';});
  h+='</div>';
  v.innerHTML=h;
 } else if(S.tab==='rea'){
  v.innerHTML='<div class="card"><h3>🔎 Analizar con REA</h3><div class="sub">Ruta de una app/carpeta o archivo. REA devuelve Evidence sellada (hash).</div>'+
   '<div class="tools"><input type="text" id="reapath" placeholder="C:\\ruta\\app" style="flex:1"><button class="sw" data-rea="js">App JS/Electron</button><button data-rea="bin">Binario</button></div>'+
   '<div id="reares">'+(S.rea?('<b>Estado:</b> '+S.rea.status+'<br>'+(S.rea.evidence?('Evidence: <span class="path">'+S.rea.evidence+'</span>'):(S.rea.msg||''))):'Sin análisis en esta sesión.')+'</div></div>';
 } else {
  if(!S.bin.length){v.innerHTML='<div class="empty">Papelera vacía.</div>';return;}
  var h='<table><thead><tr><th>#</th><th>Archivo</th><th>Fecha</th><th></th></tr></thead><tbody>';
  S.bin.forEach(function(e,i){h+='<tr><td>'+(i+1)+'</td><td class="path">'+(e.archivo||e.path)+'</td><td class="path">'+e.fecha+'</td><td>'+(e.accion==='papelera'?'<button data-r="'+(i+1)+'">Rescatar</button>':'—')+'</td></tr>';});
  v.innerHTML=h+'</tbody></table>';}
 document.querySelectorAll('button[data-p]').forEach(function(b){b.onclick=async function(){if(!confirm('¿Mover a la Papelera Seawolf?'))return;await fetch('/mover',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({p:decodeURIComponent(b.dataset.p)})});b.textContent='✔';H('Movido');refrescar();};});
 document.querySelectorAll('input.ck').forEach(function(c){c.onchange=function(){var p=decodeURIComponent(c.dataset.p);if(c.checked)S.sel[p]=1;else delete S.sel[p];selInfo();};});
 var cka=document.getElementById('ck-all');if(cka)cka.onchange=function(){document.querySelectorAll('input.ck').forEach(function(c){c.checked=cka.checked;var p=decodeURIComponent(c.dataset.p);if(cka.checked)S.sel[p]=1;else delete S.sel[p];});selInfo();};
 var btr=document.getElementById('b-trash');if(btr)btr.onclick=function(){enviarSel(false);};
 var bhd=document.getElementById('b-hard');if(bhd)bhd.onclick=function(){enviarSel(true);};
 document.querySelectorAll('button[data-keep]').forEach(function(b){b.onclick=async function(){var g=S.dupes[+b.dataset.keep];if(!confirm('Mover '+(g.files.length-1)+' copias y dejar 1?'))return;await fetch('/mover-grupo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({files:g.files})});H('Copias movidas');refrescar();};});
 document.querySelectorAll('button[data-r]').forEach(function(b){b.onclick=async function(){await fetch('/rescatar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({n:+b.dataset.r})});H('Rescatado');refrescar();};});
 document.querySelectorAll('button[data-toggle]').forEach(function(b){b.onclick=async function(){await fetch('/manten',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:b.dataset.toggle,toggle:true})});H('Cambiado');refrescar();};});
 document.querySelectorAll('button[data-dias]').forEach(function(b){b.onclick=async function(){var d=prompt('Días:',30);if(d)await fetch('/manten',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:b.dataset.dias,dias:+d})});refrescar();};});
 document.querySelectorAll('button[data-hor]').forEach(function(b){b.onclick=async function(){var h=prompt('Horario:',b.textContent);if(h)await fetch('/manten',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:b.dataset.hor,horario:h})});refrescar();};});
 document.querySelectorAll('button[data-run]').forEach(function(b){b.onclick=async function(){H('Ejecutando…');var r=await fetch('/manten-run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:b.dataset.run})});var j=await r.json();H(j.msg||'Hecho');refrescar();};});
 document.querySelectorAll('button[data-rea]').forEach(function(b){b.onclick=async function(){var p=document.getElementById('reapath').value;if(!p)return;H('Analizando con REA…');await fetch('/rea',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:p,kind:b.dataset.rea})});refrescar();};});
 // ─────────────── SALUD DEL EQUIPO ───────────────
 // NOTA DE SEGURIDAD: todo dato de hardware que se pinta con innerHTML pasa antes por esc(),
 // porque proviene de PowerShell (nombres de disco/modelo). No se interpola texto sin escapar.
 document.querySelectorAll('button[data-salud]').forEach(function(b){b.onclick=async function(){
  if(b.dataset.salud!=='analizar')return;
  S.saludBusy=true;S.saludMsg=null;draw();
  var j=await fetch('/salud',{method:'POST'}).then(function(r){return r.json();});
  S.salud=j;S.saludBusy=false;draw();H('Análisis listo');
 };});
 document.querySelectorAll('button[data-optim]').forEach(function(b){b.onclick=async function(){
  var L=b.dataset.optim;
  var aviso='⚠️  OPTIMIZAR LA UNIDAD '+L+':\n\n'
   +'· Si es SSD  ->  hace TRIM  (es lo correcto para SSD, NO lo desgasta)\n'
   +'· Si es HDD  ->  DESFRAGMENTA  (puede TARDAR mucho rato)\n\n'
   +'NUNCA interrumpa el proceso ni apague el equipo mientras corre.\n'
   +'Si el disco estuviera casi lleno, el modulo lo bloquea por seguridad.\n\n'
   +'¿Confirma que quiere optimizar '+L+': ?';
  if(!confirm(aviso))return;
  S.saludMsg={ok:true,texto:'Optimizando '+L+': …  no cierre esta ventana ni apague el equipo.'};draw();
  H('Optimizando '+L+': … puede tardar');
  var j=await fetch('/salud-optimizar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({letra:L})}).then(function(r){return r.json();});
  S.saludMsg={ok:!!j.ok,texto:(j.msg||'')+(j.aviso?('\n\n'+j.aviso):'')+(j.salida?('\n\n'+j.salida):'')};
  draw();H(j.ok?'Listo':'Revisa el aviso');
 };});
 document.querySelectorAll('button[data-verif]').forEach(function(b){b.onclick=async function(){
  var L=b.dataset.verif;
  var aviso='🔍  VERIFICAR LA UNIDAD '+L+':\n\n'
   +'Es SOLO LECTURA: revisa el disco SIN reparar y SIN borrar nada.\n'
   +'En discos grandes puede TARDAR BASTANTE: déjalo terminar.\n'
   +'Requiere permisos de administrador.\n\n'
   +'¿Empezar la verificación de '+L+': ?';
  if(!confirm(aviso))return;
  S.saludMsg={ok:true,texto:'Verificando '+L+': …  puede tardar bastante. No cierre esta ventana.'};draw();
  H('Verificando '+L+': …');
  var j=await fetch('/salud-verificar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({letra:L})}).then(function(r){return r.json();});
  S.saludMsg={ok:!!j.ok,texto:(j.msg||'')+(j.salida?('\n\n'+j.salida):'')};draw();H(j.msg||'Hecho');
 };});
 // ─────────────── fin salud ───────────────
 function renSel(){var o=[];document.querySelectorAll('.renck').forEach(function(c){if(c.checked)o.push(c.dataset.id);});return o;}
 function renVals(){var v={};document.querySelectorAll('.renval').forEach(function(i){v[i.dataset.id]=i.value;});return v;}
 function renCar(){var e=document.getElementById('rencar');return e?e.value.trim():S.rencar;}
 document.querySelectorAll('.renck').forEach(function(c){c.onchange=function(){S.rensel=renSel();S.renvals=renVals();S.rencar=renCar();S.renprev=null;draw();};});
 document.querySelectorAll('.renval').forEach(function(i){i.oninput=function(){S.renvals=renVals();};});
 var _rc=document.getElementById('rencar');if(_rc)_rc.oninput=function(){S.rencar=_rc.value.trim();};
 document.querySelectorAll('button[data-renpreset]').forEach(function(b){b.onclick=async function(){
  var p=(S.renpresets||{})[b.dataset.renpreset];if(!p)return;
  S.rensel=p.reglas.slice();S.renvals=renVals();S.rencar=renCar();S.renpresets_hint=p.desc;S.renprev=null;S.rencv=null;draw();
  H('Atajo: '+p.nombre);
  if(S.rencar){var j=await fetch('/ren-preview',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({carpeta:S.rencar,sel:S.rensel,valores:S.renvals,solo_video:true})}).then(function(r){return r.json();});S.renprev=j;draw();}
 };});
 document.querySelectorAll('button[data-ren]').forEach(function(b){b.onclick=async function(){
  var acc=b.dataset.ren,car=renCar();
  if(acc==='prev'||acc==='aplicar'){
   if(!car){H('Escriba la carpeta');return;}
   S.rencar=car;S.rensel=renSel();S.renvals=renVals();
   var body=JSON.stringify({carpeta:car,sel:S.rensel,valores:S.renvals,solo_video:true});
   var H2={'Content-Type':'application/json'};
   if(acc==='prev'){H('Calculando…');var j=await fetch('/ren-preview',{method:'POST',headers:H2,body:body}).then(function(r){return r.json();});S.renprev=j;draw();H(j.cambian+' cambios');}
   else{
    if(!S.renprev||!S.renprev.cambian){H('Primero vea la vista previa');return;}
    if(!confirm('Se van a RENOMBRAR '+S.renprev.cambian+' archivos en '+car+'. Despues podra deshacerlo. ¿Confirma?'))return;
    H('Renombrando…');var j=await fetch('/ren-aplicar',{method:'POST',headers:H2,body:body}).then(function(r){return r.json();});
    S.renprev=null;H('Renombrados: '+j.ok+(j.total_errores?(' · errores: '+j.total_errores):''));refrescar();
   }
  } else if(acc==='deshacer'){
   if(!confirm('¿Deshacer la ultima operacion y devolver los nombres originales?'))return;
   H('Deshaciendo…');var j=await fetch('/ren-deshacer',{method:'POST'}).then(function(r){return r.json();});H(j.msg||'Hecho');S.renprev=null;refrescar();
  } else if(acc==='cvprev'||acc==='cvap'){
   if(!car){H('Escriba la carpeta');return;}
   S.rencar=car;var H2={'Content-Type':'application/json'};
   if(acc==='cvprev'){var j=await fetch('/ren-carpetas-preview',{method:'POST',headers:H2,body:JSON.stringify({carpeta:car})}).then(function(r){return r.json();});S.rencv=j;draw();H(j.cambian+' carpetas');}
   else{
    if(!S.rencv||!S.rencv.cambian){H('Primero vea que carpetas cambiarian');return;}
    if(!confirm('Renombrar '+S.rencv.cambian+' carpetas de "Temporada NN" a "Season NN"?'))return;
    H('Renombrando carpetas…');var j=await fetch('/ren-carpetas',{method:'POST',headers:H2,body:JSON.stringify({carpeta:car})}).then(function(r){return r.json();});S.rencv=null;H('Carpetas renombradas: '+j.ok);refrescar();
   }
  }
 };});
 // ─────────────── fin renombrador ───────────────
 document.querySelectorAll('th[data-s]').forEach(function(th){th.onclick=function(){var s=th.dataset.s;if(S.sort===s)S.desc=!S.desc;else{S.sort=s;S.desc=true;}draw();};});
}
document.querySelectorAll('.tab[data-t]').forEach(function(t){t.onclick=function(){document.querySelectorAll('.tab[data-t]').forEach(function(x){x.classList.remove('on')});t.classList.add('on');S.tab=t.dataset.t;draw();};});
document.getElementById('rescan').onclick=async function(){S.busy=true;S.heavy=[];S.dupes=[];S.map=[];draw();await fetch('/rescan',{method:'POST'});refrescar();};
document.getElementById('q').oninput=function(e){S.q=e.target.value;draw();};
setInterval(function(){if(!S.busy&&S.tab==='mant')refrescar();},60000);
refrescar();
</script></body></html>"""

def serve(targets, port, abrir=True):
    import http.server, socketserver
    state = {"busy": True, "targets": targets, "scanned": 0, "heavy": [], "dupes": [],
             "total": 0, "waste": 0, "drives": {}, "map": [], "rea": None}
    def work():
        state["scanned"] = 0; state["drives"] = {r: {"n": 0, "b": 0} for r in targets}
        mapa = defaultdict(lambda: defaultdict(int)); heap = []
        def prog(root, s, p):
            state["scanned"] += 1
            d = state["drives"].setdefault(root, {"n": 0, "b": 0}); d["n"] += 1; d["b"] += s
            mapa[root][top_folder(root, p)] += s
        for p, s, root in walk_multi(targets, progress=prog):
            if len(heap) < 1200: heapq.heappush(heap, (s, p))
            elif s > heap[0][0]: heapq.heapreplace(heap, (s, p))
        state["total"] = sum(v["b"] for v in state["drives"].values())
        state["heavy"] = sorted(heap, reverse=True)
        m = []
        for r, folders in mapa.items():
            tot = sum(folders.values()) or 1
            fl = sorted(folders.items(), key=lambda x: -x[1])[:20]
            m.append({"root": r, "totalH": human(tot), "folders": [{"n": k, "h": human(v), "pct": round(100 * v / tot)} for k, v in fl]})
        state["map"] = m
        gs = find_dupes(targets)
        state["waste"] = sum(g["size"] * (len(g["files"]) - 1) for g in gs); state["dupes"] = gs
        state["busy"] = False
    def drives_info():
        out = []
        for r, v in state["drives"].items():
            try: t, u, f = shutil.disk_usage(r)
            except OSError: t = u = f = 0
            out.append({"root": r, "scannedS": human(v["b"]), "n": v["n"], "totalH": human(t), "freeH": human(f), "total": t, "used": u})
        return out
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, b, ct): self.send_response(200); self.send_header("Content-Type", ct); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def _json(self, o): self._send(json.dumps(o).encode(), "application/json")
        def _clave_ok(self):
            tok, act = auth_leer()
            if not act or not tok: return True                      # cerradura desactivada
            if ("swt=" + tok) in (self.headers.get("Cookie") or ""): return True
            q = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            return q.get("k", [""])[0] == tok
        def _pedir_clave(self):
            q = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            b = auth_pagina(error=bool(q.get("k"))).encode()
            self.send_response(401); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            tok, act = auth_leer()
            if act and tok and ("swt=" + tok) not in (self.headers.get("Cookie") or ""):
                q = urlparse.parse_qs(urlparse.urlparse(self.path).query)
                if q.get("k", [""])[0] == tok:      # clave correcta: dejo cookie y limpio la URL
                    self.send_response(302)
                    self.send_header("Set-Cookie", "swt=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=31536000" % tok)
                    self.send_header("Location", "/"); self.end_headers(); return
            if not self._clave_ok():
                self._pedir_clave(); return
            if self.path.startswith("/api/state"):
                heavy = [{"p": p, "size": s, "h": human(s), "drv": (p[:2] if len(p) > 1 and p[1] == ":" else "")} for s, p in state["heavy"][:300]]
                dupes = [{"h": human(g["size"]), "wasteH": human(g["size"] * (len(g["files"]) - 1)), "files": g["files"]} for g in state["dupes"][:60]]
                self._json({"busy": state["busy"], "scanned": state["scanned"], "totalH": human(state["total"]) if state["total"] else "—",
                            "wasteH": human(state["waste"]) if state["waste"] else "—", "drives": drives_info(), "map": state["map"],
                            "heavy": heavy, "dupes": dupes, "bin": _manifest(), "manten": mant_cfg()["tareas"], "rea": state["rea"],
                            "renreglas": REGLAS_CATALOGO, "renpresets": PRESETS, "renundo": ren_estado()})
            else:
                self._send(HTML.encode(), "text/html; charset=utf-8")
        def do_POST(self):
            if not self._clave_ok():
                b = json.dumps({"ok": False, "msg": "No autorizado"}).encode()
                self.send_response(401); self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
            n = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(n) or b"{}"
            try: d = json.loads(raw)
            except Exception:
                d = {}
                try:
                    # Repara rutas de Windows con barras invertidas sin escapar ("H:\caida" -> "H:/caida")
                    # y vuelve a parsear COMPLETO (asi no se pierden 'sel' ni 'valores').
                    txt = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', "/", raw.decode("utf-8", "ignore"))
                    d = json.loads(txt)
                except Exception:
                    d = {}
            if self.path.startswith("/mover-muchos"): limpiar(d.get("paths", []), bool(d.get("hard")))
            elif self.path.startswith("/mover-grupo"): limpiar(d.get("files", [])[1:])
            elif self.path.startswith("/mover"): limpiar([d.get("p", "")])
            elif self.path.startswith("/rescatar"): rescatar(int(d.get("n", 0)))
            elif self.path.startswith("/manten-run"):
                tid = d.get("id"); threading.Thread(target=lambda: state.__setitem__("rea", None), daemon=True).start()
                res = mant_run(tid); self._json(res); return
            elif self.path.startswith("/manten"):
                cfg = mant_cfg(); t = next((x for x in cfg["tareas"] if x["id"] == d.get("id")), None)
                if t:
                    if d.get("toggle"): t["activo"] = not t["activo"]
                    if d.get("dias"): t["dias"] = d["dias"]
                    if d.get("horario"): t["horario"] = d["horario"]
                    mant_save(cfg)
            elif self.path.startswith("/rea"):
                state["rea"] = {"status": "analizando…", "msg": "REA corriendo"}
                path = d.get("path", ""); kind = d.get("kind", "js")
                def go():
                    state["rea"] = rea_run(path, kind); state["rea"]["status"] = "listo" if state["rea"].get("ok") else "error"
                threading.Thread(target=go, daemon=True).start()
            elif self.path.startswith("/salud-optimizar"):
                self._json(salud_optimizar(d.get("letra", ""))); return
            elif self.path.startswith("/salud-verificar"):
                self._json(salud_verificar(d.get("letra", ""))); return
            elif self.path.startswith("/salud"):
                self._json(salud_todo()); return
            elif self.path.startswith("/ren-preview"):
                self._json(ren_preview(d.get("carpeta", ""), _ren_reglas_req(d), bool(d.get("solo_video", True)))); return
            elif self.path.startswith("/ren-aplicar"):
                self._json(ren_aplicar(d.get("carpeta", ""), _ren_reglas_req(d), bool(d.get("solo_video", True)))); return
            elif self.path.startswith("/ren-deshacer"):
                self._json(ren_deshacer()); return
            elif self.path.startswith("/ren-carpetas-preview"):
                self._json(ren_carpetas_preview(d.get("carpeta", ""))); return
            elif self.path.startswith("/ren-carpetas"):
                self._json(ren_carpetas(d.get("carpeta", ""))); return
            elif self.path.startswith("/rescan"):
                state["busy"] = True; state["heavy"] = []; state["dupes"] = []; state["map"] = []
                threading.Thread(target=work, daemon=True).start()
            self._json({"ok": True})
    threading.Thread(target=work, daemon=True).start()
    tok, act = auth_leer()
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), H) as srv:
        srv.allow_reuse_address = True
        print(f"[Seawolf Tools] http://127.0.0.1:{port}  · discos: {', '.join(targets)}")
        if act and tok:
            print("[Cerradura]  ACTIVA")
            print(f"[Cerradura]  Clave de acceso ......... {tok}")
            print(f"[Cerradura]  Entrada directa ......... http://127.0.0.1:{port}/?k={tok}")
            print("[Cerradura]  (guardela. Sin ella no se entra desde el dominio.)")
        else:
            print("[Cerradura]  DESACTIVADA (solo uso local)")
        if abrir:
            try: webbrowser.open(f"http://127.0.0.1:{port}/?k={tok}" if (act and tok) else f"http://127.0.0.1:{port}")
            except Exception: pass
        srv.serve_forever()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Seawolf Tools - Optimizacion")
    ap.add_argument("cmd", choices=["drives", "scan", "dupes", "mant", "papeles", "rescatar", "limpiar", "serve", "clave", "salud"])
    ap.add_argument("arg", nargs="?", default="ALL")
    ap.add_argument("--sub", default="")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--min", type=float, default=1)
    ap.add_argument("--port", type=int, default=8770)
    ap.add_argument("--paths", default="")
    ap.add_argument("--hard", action="store_true")
    ap.add_argument("--no-open", action="store_true", help="no abrir el navegador al arrancar")
    a = ap.parse_args()
    if a.cmd == "drives":
        for d in list_drives(): print(f"  {d['root']}  total {human(d['total'])} · usado {human(d['used'])} · libre {human(d['free'])}")
    elif a.cmd == "scan": scan(parse_targets(a.arg), a.top)
    elif a.cmd == "dupes": dupes(parse_targets(a.arg), a.min)
    elif a.cmd == "mant":
        if a.sub == "run": print(mant_run(a.arg))
        else:
            for t in mant_cfg()["tareas"]: print(f"  [{('X' if t['activo'] else ' ')}] {t['id']:<10} {t['nombre']}  ({t['horario']}, +{t['dias']}d)")
    elif a.cmd == "papeles": papeles()
    elif a.cmd == "rescatar": rescatar(int(a.arg) if a.arg.isdigit() else 0)
    elif a.cmd == "limpiar": limpiar([p for p in a.paths.split(",") if p], a.hard)
    elif a.cmd == "clave":
        if a.sub in ("nueva", "reset"):
            tok, act = auth_guardar(token=secrets.token_urlsafe(18))
            print(f"  clave NUEVA: {tok}")
        elif a.sub in ("on", "activar"):
            tok, act = auth_guardar(activo=True); print(f"  cerradura ACTIVADA · clave: {tok}")
        elif a.sub in ("off", "desactivar"):
            auth_guardar(activo=False); print("  cerradura DESACTIVADA (ojo: cualquiera entra)")
        else:
            tok, act = auth_leer()
            print(f"  cerradura : {'ACTIVA' if act else 'DESACTIVADA'}")
            print(f"  clave     : {tok}")
            print(f"  entrada   : http://127.0.0.1:{a.port}/?k={tok}")
    elif a.cmd == "salud":
        t = salud_todo()
        print("=" * 68)
        print(f"  SALUD DEL EQUIPO — {t['resumen']['discos']} discos "
              f"({t['resumen']['ssd']} SSD · {t['resumen']['hdd']} HDD)")
        print("=" * 68)
        for d in t["discos"]:
            print(f"  [{d['id']}] {str(d['modelo'])[:30]:<32} {d['tipo']:<12} {str(d['salud']):<9} -> {d['mantenimiento']}")
        print("\n  UNIDADES (de mas a menos apretadas):")
        for v in t["volumenes"]:
            print(f"   {v['letra']}:  {v['libreGB']:>5}/{v['totalGB']:>5} GB  ({v['librePct']}% libre)"
                  + ("   << " + v["aviso"] if v["aviso"] else ""))
        print("\n  AVISOS:")
        for x in (t["avisos"] or ["ninguno"]): print("   -", x)
        print("\n  " + AVISO_DISCOS)
    elif a.cmd == "serve": serve(parse_targets(a.arg), a.port, abrir=not a.no_open)
