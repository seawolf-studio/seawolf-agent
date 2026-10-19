#!/usr/bin/env bash
q() { python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1"; }
for term in "RUES" "matricula mercantil" "registro mercantil" "camara de comercio empresas" "establecimientos de comercio"; do
  echo "=== $term ==="
  curl -s "https://api.us.socrata.com/api/catalog/v1?q=$(q "$term")&domains=www.datos.gov.co&limit=6" \
    | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
    for r in d.get('results',[]):
        res=r['resource']; print(' ', res['id'],'|', (res.get('name') or '')[:70])
    if not d.get('results'): print('  (sin resultados)')
except Exception as e: print('  err', e)"
done
