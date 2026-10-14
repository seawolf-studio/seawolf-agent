# TIENDA SEAWOLF — MEJORAS INYECTADAS DESDE LA DESTILACIÓN
**Análisis de Bellion (Gran Comandante) · Monarca: Key · 2026-10-13**
**Base:** `MANUAL-MAESTRO-tiendas-v5.md` (destilación auditada, PASA por BERU) × `C:/Users/Admin/seawolf-store/` (máquina construida 16→28 sep)
**Promesa a vender:** *tiendas automáticas que venden solas, con autorización de sus dueños (intervención humana).*

---

## 0. ESTADO REAL VERIFICADO HOY (no lo que decía el diario — lo que hay)

| Pieza | Estado verificado | Evidencia |
|---|---|---|
| **Puente Dropi Bridge v3** (WordPress) | ✅ **VIVO** — PHP 8.2.34 · WP 7.0.7 · WooCommerce 11.2.0 · token presente (577 chars) · dir escribible | `action=test` respondió OK |
| **Catálogo vivo en Shopio** | **246 productos** (`x-wp-total: 246`) | Store API de WooCommerce |
| **Tienda construida** (`dist/`) | **200 productos** · 199 con `dropi_id` · 200 con foto | `dist/products.json` |
| **Desfase** | ⚠️ La tienda está **46 productos atrás** del catálogo | 246 vs 200 |
| **ZIP de despliegue** | `Desktop/seawolf-tienda-hostinger.zip` (14,9 MB, 989 archivos, sep 27) | verificado |
| **El ZIP NO lleva secretos de notificación** | ✅ Correcto: `notify-config.php` fuera | inspección del ZIP |
| **DESPLIEGUE** | ❌ **NUNCA SE HIZO** — ningún dominio sirve la tienda estática | — |
| **Cron de pedidos** | ❌ No configurado (depende del despliegue) | — |
| **Envío real a Dropi** | ⚠️ `$MODO_PRUEBA = true` — **jamás probado** contra la API | `procesar-pedidos.php:17` |
| **La barrida de productos** | ❌ **NO se hizo**: el catálogo sigue en 246 | x-wp-total |
| **Precios** | 104 sanos · **95 a revisar** | `precios-sugeridos.csv` |
| **Git del proyecto tienda** | ❌ **No tiene repositorio** — vive solo en este disco | `git log` vacío |
| **Contraseña de WordPress** | ⚠️ Viajó por chat el 27-sep → **debe cambiarse** | diario §Pendientes |

> **Lectura honesta:** el proyecto no está "casi listo". Está **listo para desplegar y sin validar el corazón** (la creación real de pedidos). Y hay 14 días de deriva: 46 productos nuevos sin entrar.

---

## 1. FALLA CRÍTICA DE SEGURIDAD (primero, mi Señor)

**La llave del puente viaja en texto plano dentro del ZIP público.**

`dist/api/procesar-pedidos.php` (líneas 12-14) tiene escrito, a la vista:
- `$CLAVE_PROCESO = 'sw-proceso-2026-x9k7'`
- `$BRIDGE = '…&key=sw7-Gh41-…-Rt15&action=order_create'`

Ese archivo se sube a `public_html` (accesible por HTTP como texto si el servidor lo sirviera mal, seguro en backups, visible para cualquiera con acceso al hosting). Y esa llave **crea pedidos reales en Dropi**: quien la tenga, puede generar órdenes a nombre del Monarca.
**Además**, `pedidos.php` acepta `POST` de cualquier origen (`Access-Control-Allow-Origin: *`) sin límite de tasa → un bot puede inflar `pedidos.jsonl`.

**Mejora exigida:** mover **ambas llaves** a `api/seawolf-config.php` (archivo aparte, fuera del ZIP, subido a mano como `notify-config.php`), **rotar la llave del puente**, y añadir límite de tasa por IP + honeypot. (El manual no lo cubre: esto lo aporta la auditoría, no la destilación.)

---

## 2. LAS 12 MEJORAS DESDE LA DESTILACIÓN

> Ninguna es teoría: cada una sale de una sección del manual v5 y de un hueco concreto que verifiqué en el código de la tienda.

| # | Lo que enseña la destilación | Qué falta HOY en la tienda | Mejora concreta | Impacto |
|---|---|---|---|---|
| **1** | **9 departamentos SIN cobertura** (Amazonas, Arauca, Chocó, Guainía, Guaviare, Putumayo, San Andrés, Vaupés, Vichada) | 🔴 **Verificado: ninguno de los 9 aparece en el checkout** — la tienda los acepta y esos pedidos se pierden | Excluirlos del `<select>` de departamento + validación en `pedidos.php` (doble candado) | Evita pérdidas del 100% del flete en esos pedidos |
| **2** | **Huella digital: cliente rojo = pago anticipado o NO se vende** (3 entregas de 10 → declinar) | No existe ninguna validación de riesgo: el mismo teléfono puede pedir 20 veces | **"Huella propia"**: índice de historial por teléfono en `data-pedidos` (entregado/devuelto). Reglas: 1ª compra con tope de monto · naranja = confirmar antes · rojo = pago anticipado | Es el **error #1 más caro** del manual: 40-50% del flete por devolución |
| **3** | **No despachar sin confirmar** (cliente fantasma = flete perdido) | El pipeline crea el pedido en Dropi **solo** — la confirmación es un link suelto en `pedido.astro` | **Compuerta de confirmación**: el pedido queda capturado pero **no se crea en Dropi** hasta que el cliente confirme por WhatsApp (o el dueño apruebe) | Mata al fantasma antes de pagar el flete |
| **4** | **Los 9 estados de la guía + rutina diaria de novedades ("avisar al cliente en reparto")** | El pipeline **crea y olvida**: no consulta estados, no avisa a nadie | **Seguimiento de estados**: el cron consulta `order_status` por el puente y **dispara mensajes al cliente** según estado (guía generada → número; en reparto → "llega hoy") | Es la mitad del trabajo diario del dueño, automatizada |
| **5** | **Reserva por devolución: 40-50% del flete** (no publicidad) | El precio se calcula sin reserva de devolución | Campo `tasa_devolucion_estimada` en `config.json` → **margen real por producto** y **piso de rentabilidad** que **oculta** lo que no da | Sube el margen verdadero; ordena los **95 productos a revisar** |
| **6** | **Precio psicológico: "si vale 60.000, di 59.900"** | Precios planos: 25.000, 11.000… | Redondeo a `xx.900` + regla de precio mínimo por producto | Conversión (efecto conocido, y es gratis) |
| **7** | **Copys GADO + niveles de consciencia + ángulos por ocasión** | 🔴 El copy es **el crudo del feed**: *"Shampoo Potencializador para Cabellos Rojos Natural hecho co…"* — truncado y sin ángulo | **IGRIS** genera para cada producto: título de 8 palabras + GADO + ángulo de ocasión (la tienda **ya tiene** filtro por ocasión: falta el copy que lo acompañe) | Ahí está la diferenciación: la tienda deja de ser "otra tienda de Dropi" |
| **8** | **Del post al chat: enlace de WhatsApp con mensaje prellenado** | Solo hay botón en `pedido.astro`; no en catálogo/ficha | Botón flotante de WhatsApp con **producto prellenado** en toda la tienda | Recupera al que no quiere llenar formulario |
| **9** | **Seguimiento 1h / 1d / 3d** ("muchas ventas se cierran en el 2º o 3er toque") | No existe recuperación de carrito ni de pedido a medias | Capturar teléfono en el **primer paso** del checkout + secuencia de 3 toques | Ingreso que hoy se cae al piso |
| **10** | **"El cliente que no responde no te ignora, te olvida"** | No hay página de seguimiento del pedido | Página `/seguimiento` con el número de pedido → estados reales de Dropi | Menos llamadas al dueño |
| **11** | **Exclusión de departamentos también en campañas/atribución** | La tienda no mide nada | Registro mínimo de origen (UTM) por pedido → saber qué producto/ocasión vende | Decide **qué producto escalar** |
| **12** | **Aviso en el estado "En reparto" HOY** | Sin notificaciones al cliente | Plantillas de mensaje por estado, listas para WhatsApp Business | Sube la tasa de entrega (menos rechazos) |

---

## 3. LA PROMESA, HECHA ARQUITECTURA: «MOTOR DE REGLAS DEL DUEÑO»

La destilación (huella, cobertura, confirmación, novedades) + lo que ya probamos en el Seawolf Agent (**C3: reglas preaprobadas**, 6/6) dan el molde exacto:

```
PEDIDO ENTRA
   │
   ├─ 1. COBERTURA      → depto sin cobertura ⇒ RECHAZO EDUCADO (automático)
   ├─ 2. HUELLA PROPIA  → verde/naranja/rojo según historial del teléfono
   ├─ 3. MONTO Y STOCK  → ¿hay stock real en Dropi? ¿supera el tope de 1ª compra?
   │
   ├─ verde  ⇒ prepara y pide AUTORIZACIÓN al dueño
   ├─ naranja ⇒ CONFIRMACIÓN del cliente por WhatsApp antes de seguir
   └─ rojo   ⇒ pago anticipado o declinar (regla escrita, jamás improvisada)
   │
   ▼
AUTORIZACIÓN DEL DUEÑO (Telegram, 2 botones: APROBAR / RECHAZAR)
   ├─ toca APROBAR   ⇒ se crea el pedido en Dropi (PENDIENTE CONFIRMACION)
   ├─ no responde N s ⇒ acción segura por defecto (rompe-rojo)
   └─ RECHAZA        ⇒ se avisa al cliente con dignidad
   ▼
POST-VENTA AUTOMÁTICO (los 9 estados → mensajes al cliente)
   ▼
AUDITORÍA: cada acción con `approved_by: dueño | regla:<id>` y su hash
```

**Todo lo automático es reversible y auditable; nada toca el dinero sin su voz o sin una regla que usted escribió.** Eso es exactamente lo que vende la promesa: *"vende sola, pero no hace nada raro sin tu permiso"*.

---

## 4. PRIORIDADES Y REPARTO (sombras)

### P0 — sin esto, nada más importa
| # | Tarea | Sombra |
|---|---|---|
| 1 | **Rotar llave del puente + sacar claves del ZIP** (`seawolf-config.php` aparte) | **JIMA** (con visto bueno de BERU) |
| 2 | **Bloquear los 9 departamentos** en checkout + `pedidos.php` | **KAISEL** |
| 3 | **Verificación de stock real** antes de crear pedido (el catálogo ya trae `dropi_stock`) | **KAISEL** + **JIMA** |
| 4 | **Poner el proyecto bajo git** (hoy no tiene repositorio) | **KAISEL** |

### P1 — el corazón de la promesa
| # | Tarea | Sombra |
|---|---|---|
| 5 | **Motor de reglas** (cobertura → huella propia → monto/stock → verde/naranja/rojo) | **JIMA** |
| 6 | **Autorización por Telegram** (aprobar/rechazar + rompe-rojo + auditoría) | **JIMA** |
| 7 | **Seguimiento de los 9 estados** → mensajes al cliente (en reparto, guía, etc.) | **JIMA** + **IGRIS** (plantillas) |
| 8 | **Compuerta de confirmación** (no crear en Dropi sin confirmar) | **JIMA** |
| 9 | **Reserva de devolución + piso de rentabilidad** → limpiar los 95 productos | **TANK** (números) + **KAISEL** |

### P2 — lo que la hace vendible y diferente
| # | Tarea | Sombra |
|---|---|---|
| 10 | **Copys GADO + ángulos por ocasión** para todo el catálogo | **IGRIS** |
| 11 | **Precio psicológico + redondeo** | **KAISEL** |
| 12 | **WhatsApp flotante con mensaje prellenado** | **KAISEL** |
| 13 | **Recuperación de carrito** (captura temprana del teléfono + 3 toques) | **IGRIS** + **JIMA** |
| 14 | **Página /seguimiento** + UTMs por pedido | **KAISEL** |
| 15 | **Sincronizar los 46 productos** que faltan + reconstruir el ZIP | **KAISEL** |
| 16 | **Auditoría de todo el despliegue** | **BERU** |

### Lo que SOLO puede hacer el Monarca (no es delegable)
- Elegir el **dominio/espacio** donde vive la tienda (debe ser **distinto** de Shopio, que aloja el puente).
- Subir el ZIP y su `seawolf-config.php` (o autorizar la bóveda para que lo haga yo sin ver la contraseña).
- **Autorizar el primer pedido REAL** contra Dropi (gasta flete real; propongo el producto más barato, 1 unidad, enviado a su propia dirección).
- **Cambiar la contraseña de WordPress** (viajó por chat).

---

## 5. LA DECISIÓN ESTRATÉGICA (una sola pregunta, mi Señor)

Todo lo demás lo puedo ordenar ya. Lo que necesito de su boca:

> **¿La tienda se despliega como dominio temporal de Hostinger (prueba, sin costo) o compramos dominio propio desde el arranque?**
> Y con eso: **¿autoriza una orden REAL de prueba** (1 unidad del producto más barato, a su dirección) para cerrar el único tramo nunca probado del pipeline?

---

*Análisis de Bellion · evidencia o no existe · nada de esto se toca sin su voz.*
