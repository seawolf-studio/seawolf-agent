#!/usr/bin/env bash
set -u
B=http://127.0.0.1:8888
KEY=$(awk -F= '/^ADMIN_API_KEY=/{print $2}' /opt/nereus/mem0/server/.env | tr -d '"')
echo "admin key len: ${#KEY}"

echo "=== schema POST /memories ==="
curl -s -m8 $B/openapi.json | python3 -c "
import sys,json
d=json.load(sys.stdin)
rb=d['paths']['/memories']['post'].get('requestBody',{})
ref=rb.get('content',{}).get('application/json',{}).get('schema',{}).get('\$ref','')
print('ref:', ref)
name=ref.split('/')[-1]
sch=d['components']['schemas'].get(name,{})
print('required:', sch.get('required'))
for k,v in list(sch.get('properties',{}).items())[:15]:
    print('  ', k, '->', json.dumps(v)[:90])
"

echo
echo "=== 1) AÑADIR memoria ==="
ADD=$(curl -s -m120 -X POST "$B/memories" -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"El Monarca prefiere respuestas cortas y odia el relleno corporativo."},{"role":"user","content":"El Monarca trabaja en Colombia y usa espanol latino."}],"user_id":"monarca","metadata":{"source":"prueba-fase4"}}')
echo "$ADD" | head -c 600; echo

echo
echo "=== 2) BUSCAR ==="
SR=$(curl -s -m120 -X POST "$B/search" -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"query":"como prefiere el Monarca las respuestas?","user_id":"monarca"}')
echo "$SR" | head -c 800; echo

echo
echo "=== 3) LISTAR ==="
curl -s -m30 "$B/memories?user_id=monarca" -H "X-API-Key: $KEY" | head -c 500; echo
echo FIN