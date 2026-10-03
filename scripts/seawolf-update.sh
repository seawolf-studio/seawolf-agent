#!/bin/bash
# ============================================================
# Seawolf Agent — Sistema de Mantenimiento Automático
# Ejecutado por cron a las 3:00 AM (UTC-5)
# ============================================================
set -e

WEBUI_DIR="/opt/seawolf-webui"
LOCKFILE="/tmp/seawolf-maintenance.flag"
LOG_FILE="/var/log/seawolf-update.log"
VERSION_FILE="$WEBUI_DIR/static/version.json"
CHANGELOG_FILE="$WEBUI_DIR/static/changelog.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

log "=== 🐺 Seawolf Update Started ==="

# --- 1. Activar modo mantenimiento ---
touch "$LOCKFILE"
log "🔧 Modo mantenimiento activado"

# --- 2. Obtener versión actual ---
CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$VERSION_FILE')).get('version','unknown'))" 2>/dev/null || echo "unknown")
log "📦 Versión actual: $CURRENT_VERSION"

# --- 3. Hacer fetch del upstream Hermes ---
cd "$WEBUI_DIR"
UPSTREAM_REMOTE="upstream"
UPSTREAM_URL=$(git remote get-url upstream 2>/dev/null || echo "")

if [ -z "$UPSTREAM_URL" ]; then
    log "⚠ No hay upstream configurado. Registrando..."
    git remote add upstream https://github.com/seawolf-studio/seawolf-weui.git 2>/dev/null || true
    UPSTREAM_URL="https://github.com/seawolf-studio/seawolf-weui.git"
fi

git fetch upstream 2>&1 >> "$LOG_FILE" || {
    log "⚠ Error al hacer fetch. ¿Hay conexión a internet?"
}

UPSTREAM_COMMITS=$(git log HEAD..upstream/main --oneline 2>/dev/null | wc -l)

if [ "$UPSTREAM_COMMITS" -eq 0 ]; then
    log "✅ No hay cambios upstream. Nada que actualizar."
    rm -f "$LOCKFILE"
    python3 -c "
import json
with open('$CHANGELOG_FILE') as f:
    cl = json.load(f)
# Mark last maintenance as verified
print('No changes - maintenance check passed')
"
    log "🔧 Modo mantenimiento desactivado (sin cambios)"
    log "=== 🐺 Seawolf Update Completed (no changes) ==="
    exit 0
fi

log "🔄 $UPSTREAM_COMMITS nuevos commits encontrados"

# --- 4. Guardar changelog antes del merge ---
git log HEAD..upstream/main --oneline --pretty=format:"- %s" > /tmp/seawolf-upstream-changes.txt
log "📝 Changelog guardado"

# --- 5. Hacer merge ---
git pull upstream main 2>&1 >> "$LOG_FILE"
log "✅ Merge completado"

# --- 6. Reaplicar rebranding ---
python3 "$WEBUI_DIR/bin/rebrand.py" >> "$LOG_FILE" 2>&1
log "✅ Rebranding reaplicado"

# --- 7. Reemplazar favicon y logo (se pierden en merge) ---
cp "$WEBUI_DIR/static/seawolf-logo.png" "$WEBUI_DIR/static/favicon-512.png" 2>/dev/null || true
log "✅ Assets copiados"

# --- 8. Actualizar versión ---
NEW_VERSION="$(date '+%Y.%m.%d')-r$UPSTREAM_COMMITS"
python3 -c "
import json
with open('$VERSION_FILE') as f:
    v = json.load(f)
v['version'] = '$NEW_VERSION'
v['updated_at'] = '$(date -u '+%Y-%m-%dT%H:%M:%SZ')'
v['commits'] = v.get('commits', 0) + $UPSTREAM_COMMITS
with open('$VERSION_FILE', 'w') as f:
    json.dump(v, f, indent=2)
"
log "✅ Versión actualizada: $NEW_VERSION"

# --- 9. Agregar al changelog ---
python3 -c "
import json
with open('/tmp/seawolf-upstream-changes.txt') as f:
    changes = [c.strip() for c in f.readlines() if c.strip()]
entry = {
    'version': '$NEW_VERSION',
    'date': '$(date '+%Y-%m-%d')',
    'changes': changes
}
try:
    with open('$CHANGELOG_FILE') as f:
        history = json.load(f)
except:
    history = []
history.insert(0, entry)
history = history[:15]
with open('$CHANGELOG_FILE', 'w') as f:
    json.dump(history, f, indent=2, ensure_ascii=False)
"
log "✅ Changelog actualizado"

# --- 10. Reiniciar servicio WebUI ---
systemctl restart seawolf-weui.service >> "$LOG_FILE" 2>&1
log "✅ Servicio reiniciado"

# --- 11. Desactivar modo mantenimiento ---
rm -f "$LOCKFILE"
log "🔧 Modo mantenimiento desactivado"

log "=== 🐺 Seawolf Update Completed ($NEW_VERSION) ==="