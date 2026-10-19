#!/usr/bin/env bash
echo "=== TAMANO DE LAS BASES ==="
for id in nb3d-v3n7 p8a3-absd c82u-588k xz9i-gqen ysx6-4ez9; do
  c=$(curl -s "https://www.datos.gov.co/resource/$id.json?\$select=count(*)" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0].get('count_1') or d[0].get('count'))" 2>/dev/null)
  echo "  $id -> $c filas"
done
echo "=== MUESTRA p8a3-absd (matriculas vigentes) ==="
curl -s "https://www.datos.gov.co/resource/p8a3-absd.json?\$limit=3" | python3 -c "import sys,json;d=json.load(sys.stdin);[print('  ',r.get('razon_social'),'|',r.get('fec_matricula'),'|',r.get('mun_comercial')) for r in d]" 2>/dev/null
echo "=== MUESTRA nb3d-v3n7 (establecimientos) ==="
curl -s "https://www.datos.gov.co/resource/nb3d-v3n7.json?\$limit=3" | python3 -c "import sys,json;d=json.load(sys.stdin);[print('  ',r.get('razon_social'),'|',r.get('fecha_matricula'),'|',r.get('camara_comercio')) for r in d]" 2>/dev/null
echo "=== PRUEBA DE CRUCE (3 nombres de nuestra presa) ==="
for nm in "Panaderia Pan Fino" "Optica Alemana" "Club Wonder"; do
  enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$nm")
  n=$(curl -s "https://www.datos.gov.co/resource/p8a3-absd.json?\$select=count(*)&\$where=upper(razon_social)%20like%20'%25$(echo $nm | tr '[:lower:]' '[:upper:]')%25'" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0].get('count_1') or d[0].get('count'))" 2>/dev/null)
  echo "  '$nm' -> $n coincidencias en RUES"
done
