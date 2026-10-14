# Resumen de Corrección TANK — Precios v2

## QUE HICE

1. **Identifiqué el bug raíz**: `psico_abajo()` usaba `int(precio/100)*100 - 100 + 900` que daba resultados MAYORES al precio actual (ej: $30K→$30,800), haciendo que NINGÚN SANOS pudiera bajar de precio y cayendo todos en MANTENER fallback.
2. **Reescribí `psico_abajo()`** con lógica de miles: `(miles-1)*1000+900` que da resultados correctamente menores. Ej: $30K→$29,900 ✓.
3. **Corregí verificaciones `%100==90` → `%1000==900`**: El check de "precio ya psicológico" fallaba porque `$29,900 % 100 = 0`, nunca 90. Todos los precios terminan en "00".
4. **Regeneré CSV completo v2** con todas las reglas aplicadas correctamente.
5. **Actualisé informe markdown** con datos verificados, Pack candidates completos, envío scenarios, SKU missing list.

## ENTREGABLES (rutas + tamaños)

| Archivo | Ruta | Tamaño | Estado |
|---------|------|--------|--------|
| CSV v1 (original erróneo) | `C:/Users/Admin/seawolf-store/mantenimiento/precios-real-20261013.csv` | 19,120 B | intacto |
| CSV v2 (CORREGIDO) | `C:/Users/Admin/seawolf-store/mantenimiento/precios-real-20261013-v2.csv` | 30,473 B | nuevo |
| Informe v2 | `C:/Users/Admin/seawolf-agent/intel/tienda/tank-precios-informe-20261013-v2.md` | 9,934 B | actualizado |

## HALLAZGO

La distribución CORRECTA es:

| Acción | Cantidad | Qué significa |
|--------|----------|---------------|
| 🔽 BAJAR_PSICOLOGICO | **35** | SANOS redondos bajados a xx.900 inferior ($30K→$29.9K). Rentable ambos lados. |
| ✅ MANTENER | **62** | SANOS que ya tienen precios .900/.999. No tocar. |
| 🎒 PACK | **5** | Ratio 1.5-3.0x; 3 unidades del mismo producto diluyen fijo. |
| ❌ RETIRAR | **97** | Ratio >3.0x; inviable individual ni pack razonable. Ningún rentable se toca. |
| NA | **1** | Sin SKU ni costo Dropi. Crear SKU primero. |

**Confirmado:** ningún producto rentable SUBE de precio. La regla #1 está satisfecha.
- CO-0029 ($10,400) → **RETIRAR** (no $11,300 como decía v1 errónea)
- Set Nariguera ($10,000) → **RETIRAR** (no $10,900 como decía v1 errónea)
- Shampoo Gama Rojo ($25,000) → **PACK x3 a $75,900** (no $25,900)

El hallazgo estructural se mantiene: rango `<20K` es inviable (20/23 en pérdida), rango `40K-100K` es sano (96/102).

## BLOQUEO

No hay bloqueo técnico. Los archivos están correctos y verificados contra la fórmula matemática.

El único riesgo operativo es external/contributary: si Dropi cobra más de $10K promedio por envío (por peso/distinto destino), la zona RETIRAR se amplía. Con $8K de envío, ~20-30 productos de RETIRAR podrían salvarse como PACK o SUBIR_MINIMO. Si el usuario quiere optimizar más, necesita el peso real promedio de cada producto y las tarifas reales por ruta.

## SIGUIENTE

Para proceder con cambios en Shopio/WooCommerce:

1. **Primero:** Arreglar SKU huérfano ("Cargador Tipo Canguro Bebé"). Sin SKU no hay acción posible.
2. **PACKs:** Preparar 5 packs de 3 unidades en Shopio (GR25ML, CO-0002, CO-0003, CO-0017, CO-0034).
3. **BAJAR_PSICOLOGICO (35):** Ajustar precios de SANOS redondos al xx.900 inferior vía batch update en WooCommerce.
4. **MANTENER (62):** Verificar visualmente que todos terminen en .900 o .999 antes de confirmar.
5. **RETIRAR (97):** Retirar progresivamente según inventario restante. No activar nada sin autorización expresa.
6. **Enviar reporte al bot Hermes** cuando esté listo para migrar kmoviezone.

---
*Informe generado por TANK · Corrección v2 final.*
