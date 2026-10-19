#!/usr/bin/env bash
set -e
cd /opt/vigia
echo "=== 1. deduplicar ==="
python3 - <<'PY'
import csv
seen=set(); rows=[]
for r in csv.reader(open("presas_CO.csv",encoding="utf-8")):
    if not r or r[0]=="nombre": continue
    if len(r)<6: continue
    k=(r[0].strip().lower(), r[3].strip())
    if k in seen: continue
    seen.add(k); rows.append(r[:6])
with open("presas_final.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["nombre","categoria","ciudad","telefono","lat","lon"]); w.writerows(rows)
print("presas unicas:",len(rows))
PY
echo "=== 2. staging en La Madriguera ==="
docker exec -i madriguera-postgres psql -U postgres -d madriguera -c "CREATE TABLE IF NOT EXISTS stg_osm (nombre text, categoria text, ciudad text, telefono text, lat double precision, lon double precision); TRUNCATE stg_osm;"
echo "=== 3. copy ==="
cat presas_final.csv | docker exec -i madriguera-postgres psql -U postgres -d madriguera -c "\copy stg_osm FROM STDIN CSV HEADER"
echo "=== 4. insertar al riel (piezas) ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -c "INSERT INTO piezas (id,tipo,origen,estado,nombre,sector,ciudad,score,datos) SELECT 'osm-'||substr(md5(lower(nombre)||coalesce(telefono,'')),1,20),'presa','frio','vigia',nombre,categoria,ciudad,0,jsonb_build_object('tel',telefono,'lat',lat,'lon',lon) FROM stg_osm ON CONFLICT (id) DO NOTHING;"
echo "=== 5. verificar ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -tAc "SELECT 'piezas_total='||COUNT(*) FROM piezas; SELECT 'frio='||COUNT(*) FROM piezas WHERE origen='frio'; SELECT 'propio='||COUNT(*) FROM piezas WHERE origen='propio'; SELECT 'no_web_con_tel='||COUNT(*) FROM piezas WHERE datos ? 'tel';"
