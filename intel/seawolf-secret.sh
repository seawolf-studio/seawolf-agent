#!/usr/bin/env bash
# ============================================================
#  SEAWOLF SECRET — guarda una clave/token/contraseña de forma segura
#  Uso:  bash seawolf-secret.sh NOMBRE "valor"
#  Ej:   bash seawolf-secret.sh COMPOSIO_API_KEY "ck_xxxxx"
#
#  - Escribe NOMBRE=valor en el .env del perfil default Y en los 10 perfiles
#  - NO imprime el valor (solo confirma el nombre y la longitud)
#  - Reemplaza la línea si ya existía (idempotente)
#  - Deja permisos 600
# ============================================================
set -e
NAME="$1"; VALUE="$2"
if [ -z "$NAME" ] || [ -z "$VALUE" ]; then
  echo "Uso: bash seawolf-secret.sh NOMBRE \"valor\""; exit 1
fi
case "$NAME" in *[!A-Z0-9_]*) echo "Nombre invalido (usa MAYUSCULAS y _)"; exit 1;; esac

python - "$NAME" "$VALUE" <<'PY'
import os, re, sys
NAME, VALUE = sys.argv[1], sys.argv[2]
HOME_H = r"C:\Users\Admin\AppData\Local\hermes"
targets = [os.path.join(HOME_H, ".env")]
pd = os.path.join(HOME_H, "profiles")
if os.path.isdir(pd):
    for p in sorted(os.listdir(pd)):
        d = os.path.join(pd, p)
        if os.path.isdir(d):
            targets.append(os.path.join(d, ".env"))
n = 0
for f in targets:
    txt = open(f, encoding="utf-8", errors="ignore").read() if os.path.exists(f) else ""
    if re.search(r"^%s=" % re.escape(NAME), txt, re.M):
        txt = re.sub(r"^%s=.*$" % re.escape(NAME), NAME + "=" + VALUE, txt, flags=re.M)
    else:
        if txt and not txt.endswith("\n"): txt += "\n"
        txt += NAME + "=" + VALUE + "\n"
    open(f, "w", encoding="utf-8").write(txt)
    try: os.chmod(f, 0o600)
    except OSError: pass
    n += 1
print("OK: %s guardada en %d archivos .env (perfil default + perfiles de sombras)" % (NAME, n))
print("Longitud del valor: %d caracteres (el valor NO se imprime)" % len(VALUE))
PY
echo "Listo. Reinicia la app (o el gateway) para que se lea."
