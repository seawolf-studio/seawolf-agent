#!/usr/bin/env python3
"""RESCATE robusto: copia archivo por archivo, saltando cachés y enlaces rotos.
NO borra nada. Idempotente."""
import os
import shutil

SRC = ("/var/lib/docker/volumes/"
       "582f879afdc054f33faa1c3c986642d68df3c83744bb349d24fa2355170b941d/_data")
DST = "/root/Biblioteca general/Hermes"

SKIP_DIRS = {".cache", ".venv", "venv", "node_modules", "__pycache__", "sandboxes",
             ".npm", ".pnpm-store", ".local/share/uv", "site-packages", ".git"}


def copia_arbol(rel_src, rel_dst):
    s = os.path.join(SRC, rel_src)
    d = os.path.join(DST, rel_dst)
    if not os.path.exists(s):
        print("  (no existe) %s" % rel_src)
        return 0, 0
    if os.path.exists(d):
        shutil.rmtree(d)
    ok = fallos = 0
    for root, dirs, files in os.walk(s):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        rel = os.path.relpath(root, s)
        target = os.path.join(d, rel) if rel != "." else d
        os.makedirs(target, exist_ok=True)
        for f in files:
            src_f = os.path.join(root, f)
            if os.path.islink(src_f):
                continue
            try:
                shutil.copy2(src_f, os.path.join(target, f))
                ok += 1
            except Exception:
                fallos += 1
    print("  %-24s -> %-28s %d archivos (%d saltados)" % (rel_src, rel_dst, ok, fallos))
    return ok, fallos


print("=== EJERCITO DE SOMBRAS (perfiles: SOUL, memorias, skills, config) ===")
copia_arbol("profiles", "ejercito-de-sombras")

print()
print("=== IMAGENES subidas ===")
copia_arbol("images", "imagenes")

print()
print("=== CRON del agente ===")
copia_arbol("cron", "cron")

print()
print("=== PERFILES: que quedo de cada sombra ===")
base = os.path.join(DST, "ejercito-de-sombras")
if os.path.isdir(base):
    for p in sorted(os.listdir(base)):
        d = os.path.join(base, p)
        if not os.path.isdir(d):
            continue
        n = sum(len(fs) for _, _, fs in os.walk(d))
        soul = "SOUL" if os.path.exists(os.path.join(d, "SOUL.md")) else "    "
        mem = "memoria" if os.path.exists(os.path.join(d, "memories", "MEMORY.md")) else "        "
        pr = "config" if os.path.exists(os.path.join(d, "config.yaml")) else "      "
        print("   %-10s %6d archivos  [%s][%s][%s]" % (p, n, soul, mem, pr))

total = sum(os.path.getsize(os.path.join(r, f))
            for r, _, fs in os.walk(DST) for f in fs if os.path.exists(os.path.join(r, f)))
print("\n  TAMANO TOTAL EN 'Biblioteca general/Hermes': %.1f MB" % (total / 1048576.0))
