# 🛡️ Informe TANK — Precios Reales y Piso de Rentabilidad

**Fecha:** 14/10/2026
**Fuente datos:** `products.json` (200 productos) + `config.json` (envío=$10,000 COP)

---

## 🔬 Supuestos Declarados

- **Costo de envío (Dropi):** $10,000 COP (config.json, confirmado)
- **Tasa de devolución baja:** 30% del volumen
- **Tasa de devolución alta:** 40% del volumen
- **Reserva por devolución:** 45% del flete = $4,500/devolución
- **Umbral SANOS:** >=25% margen neto con devolución 40% (peor caso)
- **Ticket máximo creíble:** $75,000 COP
- **Ratio retiro:** precio_min > 3x precio_actual -> RETIRAR/PACK

## 📊 Totales por Veredicto

| Veredicto | Cantidad | % catálogo |
|-----------|----------|------------|
| ✅ SANOS | 97 | 48.5% |
| ⚠️ A_REVISAR | 46 | 23.0% |
| ❌ PÉRDIDA | 56 | 28.0% |
| 🔍 SIN_COSTO | 1 | 0.5% |

**Verificación:** 200 = 200 OK

## 🏆 Top 10 Más Sanos

| # | SKU | Nombre | Precio | M.Bru | M.Net | M.Dev40 |
|---|-----|--------|--------|-------|-------|---------|
|1|`C01`|TEXTOR|$65,000|80.0%|64.6%|61.8%|
|2|`PC01`|Porcelanizador de Pintura x 600ml|$49,900|80.7%|60.7%|57.1%|
|3|`zap sili`|ZAPATOS DE LLUVIA|$49,900|80.0%|59.9%|56.3%|
|4|`70140000`|CINTA IVY 3M|$59,900|75.0%|58.3%|55.3%|
|5|`11080000`|TAPAS DE SILICONAS|$52,900|74.5%|55.6%|52.2%|
|6|`#-44`|Cable Magnético DROPI CUP|$55,000|72.7%|54.5%|51.3%|
|7|`10620000`|ORGANIZADOR DE COPAS|$54,900|72.7%|54.5%|51.2%|
|8|`20460000`|LIMPIADOR DE VIDRIO|$54,900|72.7%|54.5%|51.2%|
|9|`90110013`|GUANTES DE ARTRITIS|$54,900|72.7%|54.5%|51.2%|
|10|`20850000`|SOPORTE DE BAÑO|$59,900|70.8%|54.1%|51.1%|

## 💀 Top 10 Más Dañados

| # | SKU | Nombre | Precio | Costo Dropi | M.Bru | M.Dev40 | Veredicto |
|---|-----|--------|--------|-------------|-------|---------|-----------|
|1|`CO-0028`|CEPILLO DIENTES BAMBÚ BAMBOO ECOLOGICO|$3,600|$1,950|45.8%|-281.9%|PERDIDA|
|2|`2`|SET NARIGUERA TAPAOIDOS|$10,000|$5,000|50.0%|-68.0%|PERDIDA|
|3|`CO-0029`|SET PITILLOS METALICOS CON LIMPIADOR|$10,400|$5,600|46.2%|-67.3%|PERDIDA|
|4|`CO-0030`|JABÓN METÁLICO ANTIOLORES REMOVEDOR OLOR|$11,000|$6,400|41.8%|-65.5%|PERDIDA|
|5|`500621`|LOCIÓN HIDRONUTRITIVA|$12,000|$7,412|38.2%|-60.1%|PERDIDA|
|6|`CO-0016`|ORGANIZADOR ACOMODADOR ZAPATOS|$9,900|$3,900|60.6%|-58.6%|PERDIDA|
|7|`CO-0011`|BOLSA TERMICA FRIO CALOR PVC DOLORES|$10,400|$4,400|57.7%|-55.8%|PERDIDA|
|8|`P05261`|LAZO PARA SALTAR EN SILICONA MANGOS EN P|$16,000|$12,000|25.0%|-48.8%|PERDIDA|
|9|`165`|Lapiz Blanqueador Dental White|$12,000|$6,000|50.0%|-48.3%|PERDIDA|
|10|`SC-82378`|DISCOS DESLIZANTES X2|$12,800|$7,000|45.3%|-46.9%|PERDIDA|

## 📐 Resumen por Rango de Precio

| Rango | Total | SANOS | A_REVISAR | PÉRDIDA |
|-------|-------|-------|-----------|---------|
|100K-150K|11|9|2|0|
|20K-40K|57|13|15|29|
|40K-60K|57|38|14|5|
|60K-100K|45|33|10|2|
|<20K|23|0|3|20|
|>150K|6|4|2|0|

## ⛔ Los Productos que NO Pueden Ser Rentables (Ticket Ultra-Bajo)

> **Criterio:** costo < $8.000 COP y precio mínimo > ratio de retiro sobre precio actual.
> Con envío fijo de $10,000 COP, estos productos no son viables como unidad individual.

### RETIRAR

| SKU | Nombre | Costo | Precio Actual | Precio Mín. Dev40 | Ratio |
|-----|--------|-------|---------------|-------------------|-------|
|`CO-0028`|CEPILLO DIENTES BAMBÚ BAMBOO ECOLOGICO|$1,950|$3,600|$18,333|5.1x|

### SUBIR DE PRECIO (ticket razonable)

| SKU | Nombre | Costo | Precio Act. | Precio Mín. | Ratio |
|-----|--------|-------|-------------|-------------|-------|
|`CO-0016`|ORGANIZADOR ACOMODADOR ZAPATOS|$3,900|$9,900|$20,933|2.1x|
|`500621`|LOCIÓN HIDRONUTRITIVA|$7,412|$12,000|$25,616|2.1x|
|`165`|Lapiz Blanqueador Dental White|$6,000|$12,000|$23,733|2.0x|
|`2`|SET NARIGUERA TAPAOIDOS|$5,000|$10,000|$22,400|2.2x|
|`CO-0002`|LABIAL LIP VOLUME 3D AUMENTO LABIOS|$6,600|$18,900|$24,533|1.3x|
|`CO-0006`|CARBON ACTIVADO 30G BLANQUEAMIENTO DENTA|$5,200|$15,000|$22,667|1.5x|
|`SC-82378`|DISCOS DESLIZANTES X2|$7,000|$12,800|$25,067|2.0x|
|`CO-0011`|BOLSA TERMICA FRIO CALOR PVC DOLORES|$4,400|$10,400|$21,600|2.1x|
|`CO-0029`|SET PITILLOS METALICOS CON LIMPIADOR|$5,600|$10,400|$23,200|2.2x|
|`CO-0030`|JABÓN METÁLICO ANTIOLORES REMOVEDOR OLOR|$6,400|$11,000|$24,267|2.2x|

## 💡 Recomendaciones Priorizadas

1. **56 productos PERDIDA:** Evaluar retiro progresivo o packs.
2. **1 ultra-bajos (<$8,000)**: No viables individuales — flete come toda rentabilidad.
3. **10 intermedios ($6K-$8K), ratio<=3x:** Subir precio psicológico para alcanzar >=25%.
4. **0 candidatos a PACK:** Agrupar 2-3 unidades diluye flete único.
5. **1 SIN_COSTO:** Sincronizar con Dropi antes de decidir.

## 📏 Comparación con Análisis Previo

> Monarca reportó: 104 SANOS / 95 A_REVISAR.
> Este informe: 97 SANOS / 46 A_REVISAR.
> Diferencias posibles: umbral (35 vs 25%), costos actualizados Dropi, tratamiento dropi_cost=0.
> **Informe independiente:** calculado desde cero con solo products.json y config.json.

---
*Informe generado por TANK · Todo sale de products.json y config.json.*