#!/usr/bin/env bash
cd /opt/vigia
echo "=== descargar xz9i-gqen (establecimientos con telefono) ==="
curl -sL "https://www.datos.gov.co/api/views/xz9i-gqen/rows.csv?accessType=DOWNLOAD" -o est.csv
wc -l est.csv
head -2 est.csv | cut -c1-300
echo "=== descargar ysx6-4ez9 ==="
curl -sL "https://www.datos.gov.co/api/views/ysx6-4ez9/rows.csv?accessType=DOWNLOAD" -o est2.csv
wc -l est2.csv
head -2 est2.csv | cut -c1-300
