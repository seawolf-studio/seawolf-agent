#!/usr/bin/env bash
for id in nb3d-v3n7 p8a3-absd 86xb-sqr3 c82u-588k ysx6-4ez9 xz9i-gqen; do
  echo "=== $id ==="
  curl -s "https://www.datos.gov.co/resource/$id.json?\$limit=1" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
    if d: print('  cols:', ', '.join(list(d[0].keys())[:25]))
    else: print('  (vacio)')
except Exception as e: print('  err', e)"
done
