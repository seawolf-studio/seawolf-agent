#!/usr/bin/env bash
# Trae los tarballs del barrido del VPS y los descomprime por grupo en el PC.
set -e
K="$HOME/.ssh-clean/seawolf-vps"
DEST="/c/Users/Admin/tienda"
mkdir -p "$DEST"
SLUGS="barcelona lobo_shoes hype_snks ropa_accesorios container2 ultimas_tendencias"
for s in $SLUGS; do
  if ssh -i "$K" -o BatchMode=yes -o ConnectTimeout=20 -o StrictHostKeyChecking=no root@76.13.109.237 "test -f /tmp/barrido_$s.tgz" 2>/dev/null; then
    ssh -i "$K" -o BatchMode=yes -o StrictHostKeyChecking=no root@76.13.109.237 "base64 -w0 /tmp/barrido_$s.tgz" > "$DEST/_$s.b64" 2>/dev/null
    base64 -d "$DEST/_$s.b64" > "$DEST/_$s.tgz" 2>/dev/null && rm -f "$DEST/_$s.b64"
    tar xzf "$DEST/_$s.tgz" -C "$DEST" && rm -f "$DEST/_$s.tgz"
    n=$(ls "$DEST/$s"/*.jpg 2>/dev/null | wc -l)
    echo "  $s: $n imágenes"
  else
    echo "  $s: (no hay tar en el VPS)"
  fi
done
echo "DESCARGA COMPLETA -> $DEST"
