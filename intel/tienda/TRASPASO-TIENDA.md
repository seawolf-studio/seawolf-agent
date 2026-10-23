# 🏪 TRASPASO — NEGOCIO TIENDA (Zapatillas + Ropa)
### Documento de arranque para la sesión de construcción
**Preparado por:** Bellion (Gran Comandante) · **Para:** Monarca (Key) · **Fecha:** 2026-10-22
**Estado:** captación de catálogo COMPLETA · **falta:** levantar la tienda
**NOMBRE DE LA TIENDA (cerrado):** **SNEAKER HOUSE** · dominio recomendado **`sneakerhouse.co`**
*(nace como CLIENTE FANTASMA de Seawolf Studio: contrató SmartWeb + Círculo Publicitario → doble uso: negocio real + caso vitrina)*

---

## 0. CÓMO USAR ESTE DOCUMENTO
Si estás en una **sesión nueva** y el Monarca dice *"levanta la tienda"*: **este MD es todo el contexto.**
No hay que volver a barrer ni a preguntar lo básico. Lee las secciones 1-6 (contexto y datos) y arranca por la 8 (plan).

---

## 1. EL NEGOCIO (contexto real)
- El Monarca **cerró un acuerdo** con proveedores de calzado: puede comprar a **precio de mayorista** y revender con margen a su favor.
- Los proveedores publican **fotos de producto con el precio** en **grupos de difusión de WhatsApp**; los precios llegan **esporádicos** (no en un lote único).
- **Margen decidido por el Monarca: 40%.**
- La tienda será una **"smart shop"**: se irá armando de a poco, no de golpe.
- **PROSCRITO: Shopify** (bestia proscrita del Studio). La tienda es **código propio**.

## 2. ESTADO ACTUAL — qué YA existe
| Pieza | Estado |
|---|---|
| Catálogo extraído | ✅ **734 productos** (420 con precio) |
| Fotos | ✅ **734 imágenes** en disco |
| Proveedores barridos | ✅ **6 grupos** |
| Puente de WhatsApp (WAHA) | ✅ vinculado y funcionando (VPS) |
| Scripts de la línea de montaje | ✅ probados y en el repo |
| Tienda (web) | ❌ **no existe todavía** |

## 3. DATOS — dónde está todo
**Local (PC del Monarca):**
- `C:\Users\Admin\tienda\CONSOLIDADO.csv` ← **los 734 productos (con precio de venta a 40%)**
- `C:\Users\Admin\tienda\informe-tienda.md` ← informe técnico + arbitraje
- `C:\Users\Admin\tienda\<grupo>\catalogo.csv` · `catalogo.json` · `captions.json` · **`*.jpg` (las fotos)**
- `C:\Users\Admin\tienda\INFORME-BARRIDO-PROVEEDORES.md` / `.pdf`

**Repo (versionado):** `seawolf-agent/intel/tienda/` — commits `42edfbd`, `5aec21a`

**VPS (fuente):** `root@76.13.109.237` · WAHA en `127.0.0.1:3000` (API key en `/root/.waha.env`)

## 4. PROVEEDORES — estado de cada grupo

### ✅ CALIFICADOS (foto + precio en el mismo mensaje)
| Grupo | Productos | Con precio | Rango mayorista | Fuerte en |
|---|---|---|---|---|
| **LOBO_STORE_SHOES #1** | 200 | 193 | $50.000 – $260.000 | Nike(51), Adidas(18), On(14) |
| **BARCELONA MALL 11-12A** | 144 | 135 | $90.000 – $170.000 | Nike(41), Adidas(22), Jordan(21) |
| **Difusión HYPE SNKS** | 122 | 92 | $60.000 – $120.000 | Nike(23), Adidas(16), New Balance(12) |

### ⚠️ NO CALIFICAN (verificado: el precio NO está en la foto ni en el caption)
| Grupo | Productos | Por qué se dejó |
|---|---|---|
| Ropa 👕🩳 y Accesorios 🧢🕶️🧦 | 121 | Precio en **posts de texto aparte** ($60k-$130k) → emparejar sería **adivinar** |
| GRUPO CONTAINER 2 | 100 | Ídem ($28k-$65k sueltos) · grupo MIXTO (ropa niños, perfumes, Timberland) |
| Ultimas Tendencias Zapatillas 👟 | 47 | **No hay precio en ningún lado** (solo tallas: "25 AL 35") |

> **Decisión del Monarca:** *"si se les puede hacer el barrido fácilmente persíguelos, de lo contrario déjalo"* → **se dejaron** (no es fiable). Quedan como **fuente de fotos/producto**; el precio se pide al proveedor.

## 5. 💰 LA JOYA — ARBITRAJE ENTRE PROVEEDORES
**El mismo modelo, hasta $60.000 más barato en un proveedor que en otro:**

| Modelo | Más barato | Precio | Más caro | Precio | Ahorro |
|---|---|---|---|---|---|
| Nike Air Jordan 1 | **HYPE SNKS** | $70.000 | Barcelona | $130.000 | **$60.000** |
| Nike Dunk Low | **LOBO** | $70.000 | Barcelona | $130.000 | **$60.000** |
| Nike Air Force 1 | **LOBO** | $70.000 | Barcelona | $130.000 | **$60.000** |
| New Balance 9060 | **LOBO** | $75.000 | Barcelona | $130.000 | **$55.000** |
| Adidas Samba | **LOBO** | $70.000 | HYPE SNKS | $115.000 | **$45.000** |
| Adidas Superstar | **LOBO** | $70.000 | Barcelona | $115.000 | **$45.000** |
| Nike ZoomX | **LOBO** | $80.000 | Barcelona | $120.000 | **$40.000** |

**➡️ REGLA OPERATIVA: COMPRAR EN LOBO_STORE_SHOES · VENDER CONTRA EL PRECIO DE BARCELONA.**

## 6. NÚMEROS (margen 40% ya aplicado)
- **420 productos** con precio · mayorista **$50.000 – $260.000** (prom **$106.083**)
- **Venta sugerida (40%):** desde **$70.000** hasta **$364.000**
- Tallas: **36-39** (dama) y **40-44** (caballero) · algunos niñ@s **25-35**

## 6.5 DEMANDA — Google Trends (dato duro, Colombia, 12m)
Índice relativo (ancla `nike`=47.4). **Fuente:** `seawolf-agent/intel/informe-trends-sneakerhouse-20261022.md`
+ módulo `seawolf-agent/intel/trends-demanda.py`.

| Keyword | Índice | Nota |
|---|---|---|
| **jordan** | **20.3** | 🥇 imán (ambiguo con el país) |
| **new balance** | **10.5** | 🥈 imán |
| tenis adidas | 4.3 | 🟢 "tenis" ≫ "zapatillas" (3.6×) |
| tenis nike | 3.4 | 🟢 |
| sneakers | 2.2 | — |
| adidas samba | 2.2 | — |
| zapatillas nike | 1.4 | 🔴 usar "tenis nike" |

**Reglas de copy/SEO para la tienda:**
1. **Usar "TENIS", no "zapatillas"** en títulos, menú y SEO (3.6× más buscado en Colombia).
2. **Priorizar Jordan + New Balance** en home y destacados (imanes reales), luego Nike/Adidas.
3. **Línea femenina** como gancho ("tenis [marca] mujer" domina).
4. Long-tail: *tenis New Balance mujer · tenis Nike Shox · Jordan Retro*.

## 7. ARQUITECTURA PROPUESTA PARA LA TIENDA
- **Base:** Astro headless (skill `multi-brand-headless-ecommerce-astro`) — sitio estático rápido, **sin Shopify**.
- **Marca Seawolf (constante):** modo **OSCURO por defecto** + claro opcional · colores **#121E1E / #4CE8E7 / #48E8D8**.
- **Catálogo:** alimentado desde `CONSOLIDADO.csv` (fuente de verdad) → generar el data layer (JSON/MD por producto).
- **Fotos:** las de `C:\Users\Admin\tienda\<grupo>\*.jpg` (renombrar por SKU al importar).
- **Fase 2:** carrito + pedido por **WhatsApp** (botón "Pedir" → chat) — aprovecha el WAHA que ya está montado.
- **Fase 3:** enganche al **Círculo Publicitario** para empujar los modelos con mejor arbitraje.

## 8. PLAN DE ARRANQUE (para la sesión nueva)
1. **Confirmar marca y nombre de la tienda** con el Monarca.
2. **Definir SKU** y renombrar fotos (marca-modelo-color-talla).
3. **Generar el data layer** desde `CONSOLIDADO.csv` (un JSON por producto + índice).
4. **Montar el sitio Astro** (home + listado + ficha de producto + modo oscuro por defecto).
5. **Filtros** por marca, talla, género, precio.
6. **Botón de pedido por WhatsApp** (WAHA ya operativo).
7. **Desplegar** (VPS del Studio o hosting estático).
8. **Conectar al Círculo** y empezar a empujar.

## 9. ⚠️ PITFALLS YA VIVIDOS (no repetir)
1. **`downloadMedia=false` en WAHA deja `media.url = null`** → hay que pedir `downloadMedia=true`.
2. **Los nombres de grupo se obtienen con `/chats/overview`**, NO con `/groups` (ahí vienen en `null`).
3. **El modelo de visión gasta el budget en `reasoning` y devuelve `content: null`** → enviar siempre `"reasoning": {"enabled": false}`.
4. **Imágenes grandes → error 400 "inner error"** del proveedor → **redimensionar a ≤1024px** antes de mandarlas.
5. **Un `bash` con `"...\$1"` NO expande la variable** → usar barras normales (`C:/ruta/$1`).
6. **Nunca inventar precio**: si no está en el texto ni en la foto, queda **0** y se reporta. *(Es la regla que protege el negocio.)*
7. **Precio y tallas suelen venir en el CAPTION**, no en la imagen → parsear el texto primero, visión después.

## 10. HERRAMIENTAS DE LA LÍNEA DE MONTAJE (en `seawolf-agent/intel/`)
| Script | Qué hace |
|---|---|
| `zap_recon.py` | Reconocimiento de grupos (cuántos productos/precios tiene cada uno) |
| `zap_barrido.py` | Descarga fotos + captions de los grupos (VPS) |
| `traer-barrido.sh` | Trae los lotes del VPS al PC |
| `catalogo-grupo.py` | Cataloga un grupo (caption=precio/tallas + visión=marca/modelo) |
| `consolidar-tienda.py` | Une todos los grupos + arbitraje + informe (`--margen`) |
| `seawolf-secret.sh` | Guarda claves en el `.env` de default y de las 10 sombras |

## 11. CREDENCIALES / ACCESOS
- **WAHA:** VPS `root@76.13.109.237` (clave SSH `~/.ssh/seawolf-vps`, normalizar CRLF) · API key en `/root/.waha.env`
- **Visión:** OpenRouter `deepseek/deepseek-v4-flash-vision-exp` (`OPENROUTER_API_KEY` en el `.env`)
- **WhatsApp vinculado:** número del Monarca **+57 312 533 0127**

---

**Fin del traspaso. La tienda es lo único que falta — y tiene todo lo que necesita para nacer.** 🐺
