#!/usr/bin/env bash
set -u
mkdir -p /opt/vigia
cd /opt/vigia
echo "=== TAMANO DEL TERRENO (Overpass, Colombia, conteo) ==="
for k in shop amenity office craft healthcare leisure; do
  c=$(curl -s --max-time 160 https://overpass-api.de/api/interpreter \
      --data-urlencode "data=[out:json][timeout:150];area[\"ISO3166-1\"=\"CO\"][admin_level=2]->.co;nwr[\"name\"][\"$k\"](area.co);out count;" \
      | python3 -c "import sys,json
try:
  d=json.load(sys.stdin); t=d['elements'][0].get('tags',{}); print(t.get('total','?'))
except Exception:
  print('err')")
  echo "$k -> $c"
done
echo "=== CON SIN WEB (shop, ejemplo) ==="
curl -s --max-time 160 https://overpass-api.de/api/interpreter \
  --data-urlencode "data=[out:json][timeout:150];area[\"ISO3166-1\"=\"CO\"][admin_level=2]->.co;nwr[\"name\"][\"shop\"][!website][!\"contact:website\"](area.co);out count;" \
  | python3 -c "import sys,json
try:
  d=json.load(sys.stdin); t=d['elements'][0].get('tags',{}); print('shop sin web ->', t.get('total','?'))
except Exception:
  print('err')"
echo "=== PYTHON / DEPS ==="
python3 -m venv --help >/dev/null 2>&1 && echo "venv ok" || echo "no venv"
python3 -c "import requests" 2>/dev/null && echo "requests ok" || echo "requests missing"
echo "=== OK ==="
