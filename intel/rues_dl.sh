#!/usr/bin/env bash
cd /opt/vigia
(setsid bash -c 'curl -sL "https://www.datos.gov.co/api/views/p8a3-absd/rows.csv?accessType=DOWNLOAD" -o rues_mat.csv' >/dev/null 2>&1 &)
sleep 30
echo "=== tras 30s ==="
ls -la rues_mat.csv 2>/dev/null
wc -l rues_mat.csv 2>/dev/null
echo "=== primeras lineas ==="
head -2 rues_mat.csv 2>/dev/null
