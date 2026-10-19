#!/usr/bin/env bash
set -e
cd /opt/vigia
echo "=== columna tipo_operador ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -c "ALTER TABLE piezas ADD COLUMN IF NOT EXISTS tipo_operador text;"
echo "=== staging v4 ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -c "CREATE TABLE IF NOT EXISTS stg_v4 (nombre text,categoria text,ciudad text,telefono text,tipo_operador text,marca text,educacion text,lat double precision,lon double precision); TRUNCATE stg_v4;"
echo "=== copy v4 ==="
cat presas_v4.csv | docker exec -i madriguera-postgres psql -U postgres -d madriguera -c "\copy stg_v4 FROM STDIN CSV HEADER"
echo "=== upsert al riel ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -c "INSERT INTO piezas (id,tipo,origen,estado,nombre,sector,ciudad,score,datos,tipo_operador) SELECT 'osm-'||substr(md5(lower(nombre)||coalesce(telefono,'')),1,20),'presa','frio','vigia',nombre,categoria,ciudad,0,jsonb_build_object('tel',telefono,'lat',lat,'lon',lon),tipo_operador FROM stg_v4 ON CONFLICT (id) DO UPDATE SET tipo_operador=EXCLUDED.tipo_operador;"
echo "=== verificar ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -tAc "SELECT 'private='||COUNT(*) FROM piezas WHERE tipo_operador='private';"
docker exec madriguera-postgres psql -U postgres -d madriguera -tAc "SELECT 'total_piezas='||COUNT(*) FROM piezas;"
