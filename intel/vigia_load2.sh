#!/usr/bin/env bash
set -e
cd /opt/vigia
echo "=== staging (sin -i) ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -c "CREATE TABLE IF NOT EXISTS stg_osm (nombre text, categoria text, ciudad text, telefono text, lat double precision, lon double precision); TRUNCATE stg_osm;"
echo "=== copy desde CSV ==="
cat presas_final.csv | docker exec -i madriguera-postgres psql -U postgres -d madriguera -c "\copy stg_osm FROM STDIN CSV HEADER"
echo "=== insertar al riel ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -c "INSERT INTO piezas (id,tipo,origen,estado,nombre,sector,ciudad,score,datos) SELECT 'osm-'||substr(md5(lower(nombre)||coalesce(telefono,'')),1,20),'presa','frio','vigia',nombre,categoria,ciudad,0,jsonb_build_object('tel',telefono,'lat',lat,'lon',lon) FROM stg_osm ON CONFLICT (id) DO NOTHING;"
echo "=== verificar ==="
docker exec madriguera-postgres psql -U postgres -d madriguera -tAc "SELECT 'stg='||COUNT(*) FROM stg_osm;"
docker exec madriguera-postgres psql -U postgres -d madriguera -tAc "SELECT 'piezas_total='||COUNT(*) FROM piezas;"
docker exec madriguera-postgres psql -U postgres -d madriguera -tAc "SELECT origen||'='||COUNT(*) FROM piezas GROUP BY origen;"
