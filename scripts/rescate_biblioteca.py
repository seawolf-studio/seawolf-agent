#!/usr/bin/env python3
"""RESCATE: saca de un volumen Docker lo valioso y lo deja en 'Biblioteca general/Hermes'.
NO borra nada: solo copia."""
import os
import shutil

SRC = ("/var/lib/docker/volumes/"
       "582f879afdc054f33faa1c3c986642d68df3c83744bb349d24fa2355170b941d/_data")
DST = "/root/Biblioteca general/Hermes"

os.makedirs(DST, exist_ok=True)


def copiar(rel_src, rel_dst, ignore=None):
    s = os.path.join(SRC, rel_src)
    d = os.path.join(DST, rel_dst)
    if not os.path.exists(s):
        print("  (no existe) %s" % rel_src)
        return 0
    os.makedirs(os.path.dirname(d) or d, exist_ok=True)
    if os.path.isdir(s):
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(s, d, ignore=ignore, symlinks=False)
        n = sum(len(f) for _, _, f in os.walk(d))
        print("  dir  %-46s -> %s  (%d archivos)" % (rel_src, rel_dst, n))
        return n
    shutil.copy2(s, d)
    print("  file %-46s -> %s" % (rel_src, rel_dst))
    return 1


print("=== 1) DOCUMENTOS (raiz, sin cache) ===")
DEST_DOCS = os.path.join(DST, "documentos")
os.makedirs(DEST_DOCS, exist_ok=True)
top = [f for f in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, f))
       and f.lower().endswith((".md", ".txt", ".pdf", ".docx", ".csv"))]
for f in sorted(top):
    shutil.copy2(os.path.join(SRC, f), os.path.join(DEST_DOCS, f))
    print("  file %s" % f)

print()
print("=== 2) shopio-rescate (docs sueltos) ===")
copiar("shopio-rescate", "documentos/shopio-rescate")

print()
print("=== 3) MEMORIA del agente de ese contenedor ===")
copiar("memories", "memoria-del-agente")

print()
print("=== 4) EL EJERCITO DE SOMBRAS (perfiles + sus memorias) ===")
copiar("profiles", "ejercito-de-sombras",
       ignore=shutil.ignore_patterns("cache", "__pycache__", "*.pyc", "node_modules"))

print()
print("=== 5) IMAGENES subidas (uploads del Monarca) ===")
copiar("images", "imagenes")

print()
print("=== 6) CRON del agente (que hacia) ===")
copiar("cron/jobs.json", "cron/jobs.json")

print()
print("=== RESULTADO: 'Biblioteca general/Hermes' ===")
for root, dirs, files in os.walk(DST):
    lvl = root.replace(DST, "").count(os.sep)
    if lvl <= 2:
        print("  " * lvl + os.path.basename(root) + "/  (%d archivos)" % len(files))

total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(DST) for f in fs)
print("\n  TAMANO TOTAL RESCATADO: %.1f MB" % (total / 1048576.0))
