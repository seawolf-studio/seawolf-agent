#!/usr/bin/env bash
UA="SeawolfVigia/1.0 (contact seawolfk.studio@gmail.com)"
EP="https://overpass-api.de/api/interpreter"
count() {
  curl -s -A "$UA" --max-time 130 "$EP" --data-urlencode "data=$1" | python3 -c "import sys,json
try:
  d=json.load(sys.stdin); print(d['elements'][0]['tags']['total'])
except Exception: print('err')"
}
A='area["ISO3166-1"="CO"][admin_level=2]->.co;'
echo "=== COLEGIOS por operator:type (OSM Colombia) ==="
for v in private public religious; do
  n=$(count "[out:json][timeout:120];${A}nwr[\"amenity\"=\"school\"][\"operator:type\"=\"$v\"](area.co);out count;")
  echo "  operator:type=$v -> $n"
done
n=$(count "[out:json][timeout:120];${A}nwr[\"amenity\"=\"school\"][!\"operator:type\"](area.co);out count;")
echo "  SIN operator:type -> $n"
echo "=== otras etiquetas utiles (colegios) ==="
for t in isced:level fee religion brand; do
  n=$(count "[out:json][timeout:120];${A}nwr[\"amenity\"=\"school\"][\"$t\"](area.co);out count;")
  echo "  con $t -> $n"
done
echo "=== HOTELES con brand (cadenas) ==="
n=$(count "[out:json][timeout:120];${A}nwr[\"tourism\"=\"hotel\"][\"brand\"](area.co);out count;")
echo "  hotel con brand -> $n"
