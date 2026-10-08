#!/bin/bash
# Genera un video de prueba para verificar el canal de video (sin texto: fuente simple).
set -e
OUT=/tmp/prueba_video.mp4
ffmpeg -v error -y -f lavfi -i "color=c=darkgreen:s=640x360:d=6" \
       -f lavfi -i "sine=frequency=300:duration=6" \
       -shortest -pix_fmt yuv420p "$OUT"
ls -la "$OUT"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT"
