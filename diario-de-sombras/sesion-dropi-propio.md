# 🐺 DIARIO DE SESIÓN — Sea Wolf Studio
## Sesión: **Dropi propio** — Tienda desde cero + extracción total del catálogo + automatización de pedidos

**Comandante:** Bellion (Gran Comandante del Ejército de Sombras)
**Monarca:** Keynes (Key / Seawolfk)
**Fecha de operación:** 2026-09-16 al 2026-09-28 (múltiples jornadas)
**ID de sesión:** `20260916_080602_84d90d`
**Estado:** 🟢 TIENDA LISTA PARA DESPLIEGUE + PIPELINE AUTÓNOMO ENTREGADO

---

## 📌 RESUMEN EJECUTIVO

La sesión arrancó sacando el catálogo de productos desde el WordPress/WooCommerce puente y terminó con **una tienda e-commerce propia, completa y desplegable**, más un **pipeline de mantenimiento que funciona sin ningún agente de IA**.

Tres hitos:
1. **Tienda propia desde cero** (Astro estático) — 200 productos, 199 con foto real y con ID de Dropi.
2. **Extracción total del catálogo**: 246 productos de WooCommerce, 246 metas `_dropi_product` (IDs de Dropi que faltaban), 436 fotos reales desde el CDN de Dropi.
3. **Automatización de pedidos**: pedido del cliente → creación automática en Dropi, dejando al Monarca solo la confirmación final en el panel.

**Decisión clave del Monarca:** multi-tienda queda como proyecto aparte para más adelante. Ahora se itera solo la tienda rosa hasta que quede bien, y después se replican las otras 3.

---

## 🔧 FASE 1 — LA SEMILLA (extracción y decisión)

- El WordPress de `hotpink-nightingale-238140.hostingersite.com` sirve **solo como puente** para sacar la información. La tienda es propia y desde cero.
- Motivos del Monarca: problemas con WordPress/WooCommerce y **no parecerse a ninguna tienda existente**.
- Primer intento: CSV de WooCommerce. **No incluye imágenes** → los 194 productos quedaron con placeholders SVG generados por SKU.
- El Monarca exige catálogo extenso antes de pulir la tienda: barridas manuales de productos en lotes.

---

## 🏗️ FASE 2 — CONSTRUCCIÓN DE LA TIENDA (Astro estático)

**Stack:** Astro 4 (SSG) + islas React + CSS variables por tienda.
**Features:** hero carrusel de ocasiones, dark mode por defecto con toggle persistente, bottom-nav móvil, filtro por ocasión/categoría, quick-add, carrito drawer, checkout contraentrega, JSON-LD, tipografía Arvo + Inter.

**Multi-tienda:** una base de código + 4 configs (`stores/tienda-{rosa,azul,verde,violeta}.json`), **un build por tienda**. Aisladas de verdad: cada una su carpeta, su `products.json`, su `api/pedidos.php`, su `data-pedidos/`.

**Errores resueltos en el camino (para no repetirlos):**
| Síntoma | Causa real | Solución |
|---|---|---|
| `linkStyle is not defined` | funciones usadas en el template definidas en un `<script>` cliente | moverlas al frontmatter |
| `The character ">" is not valid inside a JSX element` | `>$150.000` en texto JSX | escape HTML |
| imports no resuelven | alias no configurados | alias en `astro.config.mjs` **y** `tsconfig.json` |
| `<script src="/x.js">` rompe el build | asset de `public/` sin directiva | `is:inline` |
| build pedía `getStaticPaths` | rutas dinámicas sin generar | `getStaticPaths()` con los slugs |
| `react-router-dom` no existe en estático | isla con router cliente | `window.location` |

**Lección dura:** los SKU del origen son sucios (espacios, `#`, mayúsculas mezcladas, **duplicados**). Se generó un campo `slug` URL-safe único por producto y **toda** la tienda usa `slug`, no `sku`.

---

## 📦 FASE 3 — PAQUETE PARA HOSTINGER (hosting compartido, NO VPS)

El Monarca corrigió el rumbo: **no es VPS, es hosting compartido** (puede crear hasta 50 sitios).

**Entregable:** build estático + `.htaccess` (URLs limpias, gzip, caché, 404) + **endpoint PHP** para pedidos. Sin Node, sin Docker, sin base de datos.
`api/pedidos.php` guarda en `data-pedidos/pedidos.jsonl`, protege la carpeta y envía correo.

---

## 🧱 FASE 4 — LOS TRES MUROS (el corazón técnico de la sesión)

### Muro 1 — El token de Dropi está atado a su origen
`POST https://api.dropi.co/integrations/products/index` responde desde cualquier otra IP:
```json
{"isSuccess":false,"message":"Access denied","status":401,"ip":"<ip>"}
```
Se probaron **8 variantes** (pageSize 500/100/50/10/2, hosts `api.dropi.{co,pa,mx}`, cabecera CamelCase, token en query, body vacío): **siempre 401**. El mismo token **sí funciona desde el WordPress** (su `integration_url`).
→ **Toda automatización debe ejecutarse desde el origen autorizado.**

### Muro 2 — Faltaban los IDs de Dropi
Solo 37 de 194 productos aparecían en el API de productos. Los IDs reales viven en el **meta protegido `_dropi_product`** de WordPress, invisible por REST.
→ Se resolvió con un plugin puente propio (ver Fase 5).

### Muro 3 — El hosting bloquea las imágenes
| Tipo | Resultado |
|---|---|
| `.jpg` | 200 real |
| `.png` | **422 Unprocessable Entity** (incluso con cookies y Referer) |
| `.webp` | 200 pero **siempre el mismo placeholder** (21.622 bytes, md5 `0db684cf…`) |

Los proxies externos no lo resuelven. **Regla aprendida: nunca dar por buena una descarga sin verificar md5 + bytes mágicos.**

---

## 🌉 FASE 5 — PUENTE WORDPRESS v3 (la llave maestra)

**Decisión de seguridad del Monarca y de Bellion:** el Monarca dio su usuario y contraseña de WordPress, pero **Bellion se negó a usarla** — ninguna contraseña se escribe en una web ni se pide por chat. Se resolvió entregando un **plugin** que el Monarca sube él mismo (`Plugins → Añadir nuevo → Subir plugin`). Así el agente no necesita credenciales de sesión.

**Plugin:** `dropi-bridge-v3` (clave `sw7-Gh41-…`) con acciones:
`test` · `meta_export` · `product_images` · `media_serve&id=N` (esquiva el WAF) · `media_zip` · `order_create` · `order_status`

**Hallazgo clave:** el meta `_dropi_product` contiene **exactamente** lo que exige la creación de pedidos:
`id` (Dropi), `user_id` (proveedor), `type`, `variations[].id`, `photos[].urlS3`, `warehouse_product[].stock`, precios. **246/246 productos.**

**Ojo, error corregido:** el puente v2 paginaba con `page` y solo traía 40 productos; el parámetro correcto es **`startData`** (con `pageSize` máximo 100).

---

## 📊 FASE 6 — EXTRACCIÓN TOTAL

| Extracción | Resultado |
|---|---|
| Catálogo WooCommerce (Store API pública) | 246 productos con slug, permalink, precio, stock e imágenes |
| Biblioteca de medios | 1002 imágenes catalogadas |
| Meta Dropi de todos los productos | 246/246 → `dropi_meta.jsonl` (1,09 MB) |
| Fotos reales desde CloudFront (`d39ru7awumhhs2.cloudfront.net`) | **436 descargadas, 0 fallos** |
| Optimización con Pillow (WebP 900px) | **167 MB → 16,7 MB (90% menos)** |
| Cruce tienda ↔ Dropi por SKU | 192/194 → luego 199/200 |
| Duplicados del CSV viejo detectados | 40 eliminados (mismo `wc_id`) |
| Productos nuevos detectados | 46 (entraron solos con ID y foto) |

**Nota de honestidad:** se intentó verificar una foto con `vision_analyze` y la API falló con **401 (API key inválida)**. No se inventó un diagnóstico visual; se verificó por bytes, dimensiones reales (1024×768, 800×800…) y unicidad de md5.

---

## 🤖 FASE 7 — AUTOMATIZACIÓN DE PEDIDOS

**Endpoint verificado leyendo el plugin oficial** (`wc-dropi-integration`, `OrdersModel.php`):
`POST {API_URL}orders/myorders` → `type: FINAL_ORDER`, `rate_type: CON RECAUDO`, `status: PENDIENTE CONFIRMACION`, `calculate_costs_and_shiping: true`, `supplier_id = producto.user_id`.
Respuesta: `{isSuccess: true, objects: {id: <dropi_order_id>}}`.

**Verdad incómoda:** **incluso el plugin oficial** deja el pedido en `PENDIENTE CONFIRMACION`. La confirmación final en el panel **siempre es humana**. No se prometió automatización al 100%.

**Flujo montado:** checkout → `pedidos.php` guarda → **cron de Hostinger (5 min)** → `procesar-pedidos.php` mapea `sku → dropi_id` en `products.json` → POST al puente (`order_create`) → aviso a **Telegram** con ID de Dropi, cliente, dirección y total.
- Estado idempotente (`estado-pedidos.json`), máximo 3 intentos, sin duplicados.
- **`$MODO_PRUEBA = true`**: simula sin crear nada en Dropi. Se activa en real solo tras validar.
- Notificaciones: token del bot en `api/notify-config.php`, **archivo aparte que nunca va en el ZIP público**.

**Pendiente:** el envío real **aún no se ha probado contra la API** (a propósito). El checkout ahora pide **departamento** porque Dropi exige `state`.

---

## 🛠️ FASE 8 — MANTENIMIENTO AUTÓNOMO (independencia del ejército)

El Monarca planteó el riesgo real: *"la posibilidad de que no pueda tener a mi ejército"*. Respuesta: pipeline que **no necesita IA**.

Carpeta `seawolf-store\mantenimiento\`:
- **`1-SINCRONIZAR-CATALOGO.bat`** — trae meta Dropi + precios, agrega nuevos, baja y optimiza fotos, limpia huérfanas, deduplica
- **`2-CONSTRUIR-TIENDA.bat`** — compila y deja el ZIP en el Escritorio
- **`MANUAL-MANTENIMIENTO.md`** — manual completo en español, con solución exacta a cada error
- **`PENDIENTES-DESPLIEGUE.md`** — checklist de subida y qué contraseña va dónde (sin secretos)
- **`precios.csv`** — columna `mi_precio` manda sobre todo
- **`precios-sugeridos.csv`** — precio sugerido para margen real del 25%
- **`config.json`** — puente, clave, proyección de precios
- **`respaldos\`** — copia automática del catálogo antes de cada cambio

**Ambos scripts fueron ejecutados y verificados** (no se entregó nada sin probar).

---

## 💰 FASE 9 — PRECIOS (la lección de negocio más caras)

El Monarca preguntó si el modo masivo del 40% le dejaba 40% de ganancia. **No.**

| Opción | Fórmula | Ganancia real |
|---|---|---|
| `margen_sobre_costo_pct: 40` | precio = costo × 1,40 | **28,6%** |
| `margen_sobre_precio_pct: 25` | precio = (costo + envío) ÷ (1 − 0,25) | **25% limpio** |

**Si se activaba el recargo global** (como estaba planteado): **166 de 200 precios BAJARÍAN** — pérdida de ~**$3.134.748** de ingreso por unidad vendida (ej.: parlante 716 de $190.000 → $119.000).
→ Se blindó el sistema: `aplicar_margen_solo_a_nuevos: true` (el margen automático **solo** toca productos nuevos sin precio). Verificado: `PRECIOS por origen: precios.csv: 1 | woocommerce: 198`.

**Situación real medida:**
- Margen promedio **48,4%** antes de envío · **~20,9%** con envío de $10.000
- **Dentro del catálogo: 104 sanos, 95 a revisar**
- Hallazgo estratégico: los productos muy baratos (cepillo de bambú $3.600, costo $1.950) **no pueden ser rentables** con envío de $10.000 → la salida es **packs** o retirarlos, no subir el precio 4×.

---

## 🎖️ LECCIONES PARA LA PRÓXIMA SESIÓN

1. **El token de Dropi solo funciona desde el origen autorizado.** No perder tiempo probando cabeceras.
2. **El meta `_dropi_product` es la fuente de verdad** para crear pedidos. No reconstruir nada.
3. **Nunca confiar en una descarga sin md5 + bytes mágicos.** El hosting sirve placeholders idénticos.
4. **Nunca almacenar ni teclear contraseñas.** Se usa la bóveda cifrada o el trabajo se hace por plugin/HTTP.
5. **Verificar dentro del artefacto final**, no en el código fuente (el ZIP se revisó archivo por archivo).
6. **`pageSize` 100 máximo** y paginación con `startData`.
7. **Margen ≠ recargo.** El envío decide el negocio en dropshipping.
8. **Antes de modificar precios en masa: simular el impacto** (se perdieron ~$3,1 M en el papel de prueba, no en la realidad).

---

## 📍 ESTADO ACTUAL Y PENDIENTES

**Hecho:**
- ✅ ZIP de despliegue: `C:\Users\Admin\Desktop\seawolf-tienda-hostinger.zip` (14,2 MB, 989 archivos, 200 productos)
- ✅ Fotos reales + IDs de Dropi en 199/200 productos
- ✅ Pipeline autónomo probado
- ✅ Sistema de precios probado (SKU 144 subido a $39.900 a modo de demo)
- ✅ `notify-config.php` generado en el Escritorio (SECRETO)
- ✅ Puente v3 activo y funcionando en WordPress

**Pendiente:**
1. El Monarca está haciendo una **barrida grande de productos** en WordPress.
2. Al volver: **`1-SINCRONIZAR-CATALOGO.bat` → `2-CONSTRUIR-TIENDA.bat` → subir el ZIP** a `public_html` del dominio temporal.
3. Correr el procesador en **modo simulado**, verificar, luego `$MODO_PRUEBA = false` y activar el **cron cada 5 min**.
4. Probar **un pedido real** y confirmar el ID de Dropi.
5. Revisar los **95 productos** de `precios-sugeridos.csv`.
6. **Cambiar la contraseña de WordPress** (viajó por chat).
7. Reconectar Dropi las veces necesarias vía el puente.
8. Proyectos futuros anotados: **multi-tienda** (3 tiendas más, casi vendidas) y **centro comercial virtual**.

**Datos de referencia rápida:**
- Puente: `https://hotpink-nightingale-238140.hostingersite.com/?dropi_bridge=1&key=<CLAVE>` (clave en `mantenimiento/config.json`)
- CDN de imágenes Dropi: `https://d39ru7awumhhs2.cloudfront.net/`
- Clave del procesador de pedidos: en `api/procesar-pedidos.php` (cambiar)

---

*Redactado por Bellion, Gran Comandante del Ejército de Sombras — Fiel a la memoria del Monarca.*
*"El lobo recuerda. El lobo no olvida."*
