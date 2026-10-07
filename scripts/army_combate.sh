#!/bin/bash
# PRUEBA DE COMBATE del Ejercito de Sombras — un perfil por sombra, en su propio contexto.
# Verifica que responde Y que usa herramientas (deja un archivo).
cd /c/Users/Admin/seawolf-agent || exit 1
EF="intel/estado-sombras"
LOG="intel/combate-logs"
mkdir -p "$EF" "$LOG"
PASA=0; TOTAL=0
for s in igris tank greed iron tusk kamish kaisel titan jima beru; do
  TOTAL=$((TOTAL+1))
  rm -f "$EF/$s.txt"
  M="Usa la herramienta terminal para crear el archivo C:/Users/Admin/seawolf-agent/$EF/$s.txt con el contenido exacto 'OPERATIVO $s'. Despues responde SOLO la linea: OPERATIVO: $s - <tu rol en 6 palabras>."
  OUT=$(timeout 280 hermes -p "$s" chat -q "$M" --yolo 2>&1)
  echo "$OUT" > "$LOG/$s.log"
  if [ -f "$EF/$s.txt" ] && echo "$OUT" | grep -qi "OPERATIVO"; then
    SES=$(echo "$OUT" | grep -oE "Session: *[0-9_a-z]+" | head -1)
    echo "  $s  PASA   $SES"
    PASA=$((PASA+1))
  else
    echo "  $s  FALLA  $(echo "$OUT" | tail -2 | tr '\n' ' ' | cut -c1-90)"
  fi
  sleep 1
done
echo
echo "RESUMEN: $PASA/$TOTAL PASAN"
echo "Archivos creados:"; ls -1 "$EF" 2>/dev/null
