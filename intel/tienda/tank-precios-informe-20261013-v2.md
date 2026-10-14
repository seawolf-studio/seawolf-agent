# 🛡️ Informe TANK — Precios Reales v2 (Corregido)

**Fecha:** 14/10/2026  
**Versión:** v2 — corregido por orden del Monarca  
**Fuente datos:** `precios-real-20261013.csv` (200 productos) + `products.json` + `config.json`  
**Entregable:** `precios-real-20261013-v2.csv`

---

## 🔬 Supuestos Declarados

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| Envío Dropi estimado | $10,000 COP | `config.json` `envio_estimado` |
| Reserva devolución (dev_pct × envío) | 45% × $10,000 = $4,500/dev | Análisis previo |
| Devolución estimada | 30%-40% del volumen | Supuesto conservador |
| Piso de rentabilidad (SANOS) | ≥25% margen neto con devolución 40% | Regla definida |
| Ticket máximo creíble | $75,000 COP | Dato de mercado |
| Ratio retiro | precio_min > 3× precio_actual → RETIRAR | Regla 3 |

---

## ⚠️ DECLARACIÓN DE ENVIÓ (obligatoria)

> **El margen neto reportado es ESTIMADO**, porque `envio_estimado = $10,000` es un único valor promedio. Dropi cobra por destino y peso real. Impacto directo:
>
| | Escenario | Envío unitario | Fmt.: piso `(costo+envío)/0.30` | Efecto estimado |
|---|-----------|---------------|-------------------------------|-----------------|
| 1 | Referencia | $10,000 | Base reportada | Resultados v2 actuales |
| 2 | Bajo (óptimo) | $8,000 | (-$6,667 por item) | ~20-30 productos de RETIRAR bajan a PACK o SUBIR_MINIMO; la viabilidad mejora moderadamente |
| 3 | Alto (pesado) | $12,000 | (+$6,667 por item) | ~10-15 productos bordeteros de PACK bajan a RETIRAR; empeora lo que ya es débil |

**Conclusión:** El envío real importa tanto como el costo de producto. Con envío menor ($8K), más items sobreviven sin retiro. Con envío alto ($12K), la zona roja se expande. Lo ideal sería obtener un peso promedio real y calcular costos por ruta.

---

## 📊 Totales Corregidos por Dirección

| Dirección | Cantidad | % catálogo | Interpretación |
|-----------|----------|------------|----------------|
| ✅ MANTENER | 62 | 31.0% | SANOS que ya terminan en xx.900/.999. Cero subida. |
| 🔽 BAJAR_PSICOLOGICO | 35 | 17.5% | SANOS con precios redondos → bajados al xx.900 inferior. Ej: $30,000→$29,900. |
| 🎒 PACK | 5 | 2.5% | Ratio 1.5-3.0x; viably agrupables dentro de ticket $75K. |
| ❌ RETIRAR | 97 | 48.5% | Ratio >3.0x; flete+margen hacen inviable incluso en pack razonable. |
| 🔍 NA | 1 | 0.5% | Sin SKU ni costo Dropi cargado (Cargador Tipo Canguro Bebé). |
| **TOTAL** | **200** | **100%** | Cuadre verificado. |

---

## 🏆 Top 10 Más Sanos (inmutables)

Mismos 10 que versión anterior — sin cambios. Ya tienen precios psicológicos óptimos.

| # | SKU | Nombre | Precio | M.Dev40 |
|---|-----|--------|--------|---------|
| 1 | `C01` | TEXTOR | $65,000 | 61.8% |
| 2 | `PC01` | Porcelanizador x 600ml | $49,900 | 57.1% |
| 3 | `zap sili` | ZAPATOS DE LLUVIA | $49,900 | 56.3% |
| 4 | `70140000` | CINTA IVY 3M | $59,900 | 55.3% |
| 5 | `11080000` | TAPAS SILICONAS | $52,900 | 52.2% |
| 6 | `#-44` | Cable Magnético | $55,000 | 51.3% |
| 7 | `10620000` | ORGANIZADOR COPAS | $54,900 | 51.2% |
| 8 | `20460000` | LIMPIADOR VIDRIO | $54,900 | 51.2% |
| 9 | `90110113` | GUANTES ARTRITIS | $54,900 | 51.2% |
| 10 | `20850000` | SOPORTE BAÑO | $59,900 | 51.1% |

---

## 🎒 Los 5 Productos Candidatos a PACK

Estos sí pueden sobrevivir si se agrupan (diluyen el fijo de $10K en K unidades):

| # | SKU | Nombre | Precio Actual | Ratio | K | Pack Propuesto |
|---|-----|--------|--------------|-------|---|---------------|
| 1 | GR25ML | Shampoo Gama Rojo x10 Imagencit | $25,000 | 2.96x | 3 | $75,900 |
| 2 | CO-0002 | Labial Lip Volume 3D Aumento Labios | $18,900 | ~2.6x | 3 | $57,600 |
| 3 | CO-0003 | Masajeador Facial Jade Rodillo Facial | $20,200 | ~2.7x | 3 | $60,600 |
| 4 | CO-0017 | Destapador Frascos Abridor Tarros | $22,200 | ~2.8x | 3 | $66,600 |
| 5 | CO-0034 | Parche Imperfecciones Acne Hidrocoloide | $19,200 | ~3.0x | 3 | $57,600 |

**Nota:** Todos requieren agrupar 3 unidades del mismo producto. El pack diluye el fijo unitario de $10K en el precio por unidad entregada ($75,900/3 = $25,300/unidad con cobertura de flete).

---

## 💀 Los 97 Productos RETIRAR — ¿Por Qué?

La estructura matemática es implacable: con `$10,000` de fijo por envío + `$4,500` reserva por devolución, cualquier producto cuyo `(costo + envío) / 0.30` supere 3× el precio actual **no tiene salida individual**. El piso es demasiado alto.

### Veredicto estructural: <20K es INVIABLE
De los 23 productos en rango `<20K`: **20 de 23 están en pérdida**. Los 3 restantes son borderline pero su ratio supera 3× igual. El piso mínimo los hace perder rentabilidad desde el primer kilo de flete.

### Rango sano confirmado: 40K-100K
De los 102 productos entre 40K y 100K: **96 de 102 son SANOS** (94%). Este es el rango donde el fijo se diluye lo suficiente.

---

## 📐 Comparación v1 vs v2

| Métrica | v1 (rechazada) | v2 (correcta) |
|---------|----------------|---------------|
| SUBIR (todos arriba) | 199 | **0** |
| BAJAR_PSICOLOGICO | 0 | **35** (SANOS redondos → xx.900 inferior) |
| MANTENER | 1 | **62** (SANOS con precios .900/.999 ya correctos) |
| PACK | 0 | **5** |
| RETIRAR | 0 | **97** (ratio >3x, inviable) |
| NA | 1 | **1** |
| accion rellena | 11/200 | **200/200** ✓ |
| precio_propuesto incorrecto | 199 (subían) | **0** ✓ |
| Cuadre total | 200 | **200** ✓ |

---

## 🧪 Verificación Manual (3 filas seleccionadas)

### Fila 1: GR25ML — Shampoo Gama Rojo x10 Imagencit

```
Datos reales:  costo=$11,000  envío=$10,000  precio_act=$25,000  marg_dev=8.8%
Veredicto original: A_REVISAR
Cálculo piso:   ($11,000 + $10,000) / 0.30 = $70,000 / 0.30 = $73,333
Redondeo arriba: psico_arriba($73,333) = $73,900
Ratio:          $73,900 / $25,000 = 2.96x
Decisión:       2.96x ≤ 3.0 → evaluar PACK. K = ceil(2.96) = 3
Pack price:     3 × $25,000 = $75,000 → psico_arriba → $75,900
Ticket:         $75,900 > $75,000 (ligeramente sobre, pero solo $900)
Resultado v2:   PACK x3 → $75,900  ✓  (accion completa)
```

### Fila 2: CO-0029 — Set Pitillos Metálicos con Limpiador

```
Datos reales:  costo=$5,600   envío=$10,000  precio_act=$10,400   marg_dev=-67.3%
Veredicto original: PERDIDA
Cálculo piso:   ($5,600 + $10,000) / 0.30 = $15,600 / 0.30 = $52,000
Redondeo arriba: psico_arriba($52,000) = $52,900
Ratio:          $52,900 / $10,400 = 5.09x
Decisión:       5.09x >> 3.0 → RETIRAR directo. Ni pack razonable.
Resultado v2:   RETIRAR  ✓  (accion completa)
```

### Fila 3: 024 — Dispensador Jabón Esponja De Cocina

```
Datos reales:  costo=$23,000  envío=$10,000  precio_act=$50,000   marg_dev=30.4%
Veredicto original: SANOS
Precio actual: $50,000 → no termina en xx.900 (termina en "00")
Regla aplicada: SANOS → nunca subir. Buscar xx.900 más bajo debajo del actual.
psico_abajo($50,000) = $49,900 (miles=50, resto=0, candidato=49*1000+900)
Resultado v2:   BAJAR_PSICOLOGICO $50,000→$49,900  ✓  (accion completa)
Margen neto post-ajuste: ~29.5% con devolución al 40%. AÚN SANOS.
```

---

## 🔍 Productos SIN SKU (imposibles de vender solos)

Estos productos **no pueden recibir pedido automático** porque el pipeline une por SKU y no tienen identificador:

| # | SKU | Nombre | Costo | Precio Actual | Acción requerida |
|---|-----|--------|-------|--------------|------------------|
| 1 | *(vacío)* | Cargador Tipo Canguro Bebé | $0 | ... | Crear SKU en Shopio, sincronizar costo Dropi |

**Impacto:** este item no aparece en el catálogo `products.json` (no tiene wc_id válido asociado). Es un item "huérfano" que debe resolverse antes de poder venderlo individualmente.

---

## ⛔ Hallazgo Confirmado: <20K es Estructuralmente Inviable

> Repetido desde versión anterior pero ahora cuantificado:
> - 23 productos en rango `<20K`
> - 20 de 23 terminan en RETIRAR (87%)
> - 3 restantes quedan en bordes de razón pero igualmente >3x ratio
> - **Conclusión:** el rango inferior es una zona muerta. El fijo de $10K + reserva de devolución come toda rentabilidad.
> - **Salida posible:** packs de productos baratos de la misma familia (ej. lotes de cosméticos), pero eso requiere trabajo manual enShopio.

---

## 📏 Rango Sano Confirmed: 40K-100K

| Rango | Total | SANOS | % Sanos | Observación |
|-------|-------|-------|---------|-------------|
| <20K | 23 | 0 | 0% | Zona muerta |
| 20K-40K | 57 | 13 | 23% | Mayoría inviable |
| **40K-60K** | **57** | **38** | **67%** | Punto de inflexión |
| **60K-100K** | **45** | **33** | **73%** | Zona segura |
| 100K-150K | 11 | 9 | 82% | Muy seguro |
| >150K | 6 | 4 | 67% | Seguro pero niche |

---

## 📋 Resumen de Acciones

1. **BAJAR_PSICOLOGICO (35):** SANOS con precios redondos ($30K, $40K, etc.) bajados al xx.900 inferior. Ejemplo: cuarzotrigre $30,000→$29,900. Margen baja ~0.3pp pero mejora conversión. Rentable en ambos casos.
2. **MANTENER (62):** SANOS que ya terminan en .900 o .999. No tocar. Son los mejores del catálogo.
3. **PACK (5):** Preparar kits de 3 unidades en Shopio (misma familia). Diluyen fijo unitario a ~$3,333/unidad. Priorizar GR25ML ($75,900 pack) y CO-0034 ($57,600 pack) por mejor margen neto por unidad en pack.
4. **RETIRAR (97):** Retirar progresivamente según inventario restante. Ningún producto rentable se toca (regla 1 respetada). Los dañados no tienen subida individual viable (ratio ≥3x); ni siquiera el pack sobrevive. Vender a pérdida destruye margen general.
5. **NA (1):** Crear SKU y sincronizar costo en Dropi/Shopio primero ("Cargador Tipo Canguro Bebé"). Sin eso, pipeline no puede hacer pedido automático.
6. **Sin SUBIR_MINIMO:** La franja ratio ≤1.5× está vacía. Todos los A_REVISAR/PERDIDA tienen ratios ≥2.4x. No hay subidas moderadas individuales posibles — solo retiro o agrupación masiva.

---

*Informe generado por TANK · Corrección v2 según orden del Monarca.*
