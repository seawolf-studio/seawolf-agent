#!/usr/bin/env bash
# Cataloga los grupos restantes y consolida. Incremental y en orden.
cd /c/Users/Admin/intel
LOG=/c/Users/Admin/tienda/_proceso.log
: > "$LOG"
run() {  # slug, categoria
  echo "=== $1 ($2) ===" | tee -a "$LOG"
  python catalogo-grupo.py "C:/Users/Admin/tienda/$1" --margen 0.35 --cat "$2" 2>&1 | tail -6 | tee -a "$LOG"
}
run lobo_shoes zapatillas
run hype_snks zapatillas
run ropa_accesorios ropa
run container2 mixto
run ultimas_tendencias zapatillas
echo "=== CONSOLIDANDO ===" | tee -a "$LOG"
python consolidar-tienda.py 2>&1 | tee -a "$LOG"
echo "PROCESO COMPLETO" | tee -a "$LOG"
