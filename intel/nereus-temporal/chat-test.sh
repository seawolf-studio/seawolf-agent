#!/usr/bin/env bash
set -u
B=http://127.0.0.1:8788
TOKEN=$(curl -s -X POST $B/api/session -H "Content-Type: application/json" -d '{}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')
export TH=$(curl -s $B/api/main-thread -H "Authorization: Bearer $TOKEN" | python3 -c 'import sys,json;print(json.load(sys.stdin)["threadId"])')
export RUN=$(python3 -c 'import uuid;print(str(uuid.uuid4()))')
BODY=$(python3 -c 'import json,os;print(json.dumps({"threadId":os.environ["TH"],"runId":os.environ["RUN"],"state":{},"messages":[{"id":"m1","role":"user","content":"Responde en una frase: estas funcionando con el modelo gratuito?"}],"tools":[],"context":[],"forwardedProps":{}}))')
T0=$(date +%s)
curl -s -N -m 90 -X POST "$B/api/copilotkit/agent/default/run" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$BODY" > /opt/nereus/chat-free.txt 2>&1
T1=$(date +%s)
python3 - <<'PY'
import json
txt=[]; types={}
for line in open('/opt/nereus/chat-free.txt',encoding='utf-8',errors='replace'):
    line=line.strip()
    if not line.startswith('data:'): continue
    try: d=json.loads(line[5:].strip())
    except: continue
    types[d.get('type')]=types.get(d.get('type'),0)+1
    if d.get('type')=='TEXT_MESSAGE_CONTENT': txt.append(d.get('delta',''))
print("eventos:", types)
print("TEXTO:", ''.join(txt)[:300])
PY
echo "segundos=$((T1-T0))"
grep -icE "error|429|rate" /opt/nereus/chat-free.txt || true
echo FIN
