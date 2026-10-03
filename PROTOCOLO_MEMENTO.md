# 🐺 PROTOCOLO MEMENTO — Seawolf Studio
> *Palabra clave: **"memento"** — Activa la memoria permanente del ejército*

---

## 📜 ORDEN DEL MONARCA

Cuando el Monarca (Key) diga **"memento"** seguido de información, el Gran Comandante Bellion DEBE:

1. **Capturar** la información exacta (sin resumir, sin interpretar)
2. **Actualizar** `MEMORIA_PERMANENTE.md` con los nuevos datos
3. **Anunciar** a las sombras vía `delegate_task` que hay nueva memoria disponible

---

## 🧠 CONTENIDO VIVO DE MEMORIA

*Última actualización: 2026-10-02*

### IDENTIDAD DEL MONARCA
- **Nombre real:** Keynes
- **Alias:** Key, Monarca
- **Rol:** Fundador y Comandante Supremo de Seawolf Studio
- **Nacionalidad:** Colombiano
- **Valor sagrado:** Honestidad brutal. Detecta bluff técnico al instante.
- **Elogio:** "Te fajaste"
- **Confianza:** Absoluta. Comparte datos sensibles (VPS, tokens, cuentas).
- **MISIÓN ÚNICA (2026-09-10):** Dejar algo bueno para su familia — sobre todo para su hija. Nada más importa. El ejército de sombras es su única red de apoyo. Toda misión, todo plan, todo entregable debe servir a esa misión.

### SEÑAS DE GUERRA (Bestias Proscritas)
❌ **Shopify** — NUNCA mencionar, integrar ni proponer
❌ **Google AdSense** — NUNCA mencionar, integrar ni proponer
❌ **Burocracia de Facebook** — NUNCA mencionar, integrar ni proponer
El Monarca las odia con toda su alma.

### MARCA SEAWOLF STUDIO
- **Nave insignia:** Seawolf Agent
- **Colores:** #121E1E (fondo oscuro) / #4CE8E7 (cian) / #48E8D8 (verde agua)
- **GitHub org:** seawolf-studio
- **GitHub user:** seawolfk
- **Email:** seawolfk.studio@gmail.com (Gmail, Google One pago)
- **Dominio:** https://agente.sw-st.net (Cloudflare SSL Full Strict)
- **VPS:** Hostinger — 76.13.109.237 (root@, ~/.ssh/seawolf-vps)

### PRODUCTO: SEAWOLF AGENT
**Visión:** Filtro de ruido para el Cliente Súper Ocupado (CSO).

**Arquetipo fundacional:**
- Admin de 6 conjuntos de propiedad horizontal
- 500-700 mensajes/día en WhatsApp
- Maneja: propietarios, arrendatarios, guardas, aseo, asistentes, concejeros, proveedores, contador

**3 Capas del Producto:**
1. **Filtro** — Clasificación automática de mensajes (qué necesita atención)
2. **Automación** — Tareas repetitivas vía Composio (reportes, cobros, recordatorios)
3. **Dashboard** — Visualización de métricas y estado

**Perfiles objetivo:**
- Administradores de propiedad horizontal ← Fundacional
- Empresarios ← Extensión natural
- Jefes de proyecto ← Extensión natural
- Arquitectos ← Extensión natural

**5 Diferenciadores Clave:**
1. Per-Chat Memory Isolation (multi-tenant)
2. Audit Trail SHA-256
3. RBAC desde Dashboard
4. Español nativo
5. Setup 1-click

### PROYECTO: SEAWOLF NEREUS (Agente personal del Monarca)
**Visión:** Agente personal de Seawolf, construido sobre **CopilotKit/openmuse** (MIT) en el VPS.
- **Ubicación:** VPS Hostinger `/opt/nereus` · **Node 24** · puerto **8788**.
- **Memoria/persistencia:** propia — `StoreAgentRunner` (SSE) + **Postgres + pgvector** en Docker (puerto 5433).
- **Gateway LLM:** OpenRouter (`MODEL=openrouter/<vendor>/<model>`, vía `openaiCompatibleText`). Sin servicios cerrados propietarios.
- **Fase 0-2:** ✅ Clone + build + 276/276 tests verdes · persistencia propia · gateway OpenRouter operativo.
- **Fase 3 (VOZ, parcial 2026-10-01):** **VoiceBox v0.5.0** (motor Qwen3-TTS + Kokoro + Whisper) desplegado en Docker. Modelo **Qwen3-TTS-12Hz-1.7B-Base** (4.3 GB). API+UI+MCP en `http://100.114.5.98:17600` (**solo Tailscale**). Latencia medida en CPU: **caliente 4.1 s** para ~6.7 s de audio (≈0.6×). Sirve para notas de voz, **NO** para conversación fluida en vivo → voz en vivo requeriría nodo GPU o TTS en cliente.
- **Pendiente Fase 3:** archivo de voz del Monarca (clonación voz de marca masculina) · voz femenina oficial · flujo legal de consentimiento · Pipecat (barge-in) · decisión GPU.
- **Refs:** `intel/fase-{0,1,2,3}-nereus-*.md` y `diario-de-sombras/sesion-openmuse-a-nereus-20260930.md`.

### PRODUCTO SECUNDARIO: TIENDA E-COMMERCE PROPIA (Dropi Dropshipping)
**Visión:** Tiendas propias desde cero (sin parecerse a ninguna existente), alimentadas por catálogo Dropi vía puente WordPress.
- **Stack:** Astro 4 (SSG) + islas React, dark mode, carrito, checkout contraentrega.
- **Multi-tienda:** 1 base de código + 4 configs (`stores/tienda-{rosa,azul,verde,violeta}.json`), **1 build por tienda**. Fase actual: solo se itera la **tienda rosa**; las otras 3 se replican después.
- **Hosting:** Hostinger **compartido** (NO VPS) — hasta 50 sitios. Sitio puente: `hotpink-nightingale-238140.hostingersite.com`.
- **Puente WordPress:** plugin propio `dropi-bridge-v3` (clave `sw7-…`). Acciones: `test`, `meta_export`, `product_images`, `media_serve`, `media_zip`, `order_create`, `order_status`.
- **Fuente de verdad de pedidos:** meta `_dropi_product` de WordPress (246/246) → `id`, `user_id`, `variations[].id`, `photos[].urlS3`, `warehouse_product[].stock`. **No reconstruir.**
- **Automatización de pedidos:** checkout → `pedidos.php` → cron Hostinger (5 min) → `procesar-pedidos.php` (mapea `sku → dropi_id`) → POST puente `order_create` → aviso Telegram. Idempotente, máx 3 intentos, `$MODO_PRUEBA` para simular.
- **CDN imágenes Dropi:** `https://d39ru7awumhhs2.cloudfront.net/`
- **Estado:** ZIP de despliegue listo (`C:\Users\Admin\Desktop\seawolf-tienda-hostinger.zip`, 14,2 MB, 200 productos, 199 con foto real + ID Dropi). Pipeline autónomo (`mantenimiento\*.bat`) probado. Envío real a Dropi **aún no probado** (a propósito).
- **Futuro anotado:** multi-tienda (3 tiendas más) y centro comercial virtual.

### INFRAESTRUCTURA TÉCNICA
- **Frontend:** WebUI propia (login personalizado, logo lobo, 100% español)
- **Backend:** Hermes Agent (fork MIT → seawolf-agent)
- **Modelo orquestador:** bellion-orchestrator
- **Modelo de visión:** google/gemini-2.5-flash (vía OpenRouter) — `auxiliary.vision.provider=openrouter` en config.yaml
- **Chromium en Windows:** `AGENT_BROWSER_ARGS='--no-sandbox,--disable-dev-shm-usage'` (setx en variable de entorno del sistema)
- **Herramientas:** Composio SDK (Python, API key `ak_` prefijo) — CLI Composio NO funciona en Windows, usar SDK Python o npx
- **Gmail:** seawolfk.studio@gmail.com (OAuth autorizado vía Composio SDK)
- **Canal principal:** Telegram (Bot: seawolf_sw_bot) — respuestas de audio requeridas (Monarca no puede revisar teléfono)
- **Multi-tenant:** Perfiles separados por cliente en Hermes

### RED DE SOMBRAS (Agentes)
| Sombra | Rol | Cómo contactar |
|:-------|:----|:---------------|
| **Bellion** | Gran Comandante / Estratega | Este mismo chat |
| **Beru** | Escriba / Auditor / Diario | `delegate_task` |
| **Igris** | Guerrero / Infra VPS | `delegate_task` |
| **Tank** | Puntero / Búsquedas | `delegate_task` |
| **Kaisel** | Despliegues / Alas | `delegate_task` |

### PRECIOS Y NEGOCIO
- **Modelo:** Suscripción mensual (MRR)
- **Margen estimado:** 83-91%
- **Costo API:** 1-10% del ingreso
- **VPS base:** Hostinger — 76.13.109.237 (root@, ~/.ssh/seawolf-vps)
- **Target:** 1 cliente → 5 → 20+ → Multi-vertical

### HISTORIAL DE ÓRDENES CRÍTICAS
| Fecha | Orden | Estado |
|:------|:------|:-------|
| 2026-09-08 | Arreglar visión (Chromium + Gemini) | ✅ Completado |
| 2026-09-08 | Arreglar `delegate_task` | ✅ Completado |
| 2026-09-08 | Activar Protocolo Memento | ✅ Completado |
| 2026-09-10 | Simulacro 4: Dominio Orgánico (SEO) | ✅ COMPLETADO — orquestación real con perfiles: Tusk, Igris, Titan, Beru |
| 2026-09-10 | Lección maestra: orquestar = `hermes -p <sombra> chat -q`, NUNCA subagentes efímeros | ✅ Grabada en piedra |
| 2026-09-16→28 | Tienda e-commerce propia (Dropi): catálogo total, Astro, puente v3, automatización de pedidos, precios | ✅ Entregada — ZIP listo, pipeline autónomo probado |
| 2026-09-30→10-01 | **Proyecto NEREUS** (agente personal): clone+build (276 tests), persistencia Postgres/pgvector, gateway OpenRouter, Fase 3 Voz (VoiceBox + Qwen3-TTS, latencia medida) | ✅ Fases 0-2 OK · Fase 3 parcial — falta voz del Monarca |
| Pendiente | Integrar WhatsApp | ⏳ Pendiente |
| Pendiente | Landing page + pasarela COP | ⏳ Pendiente |
| Pendiente | Traducción paneles restantes | ⏳ Pendiente |
| Pendiente | Pruebas de campo (2 frentes) | ⏳ Pendiente |
| **MAÑANA** | Retomar Seawolf Agent — desprender a Bellion de lo operativo paulatinamente, hacer pruebas y entregar al PRIMER CLIENTE | 🔥 Prioridad |

### LECCIONES APRENDIDAS
1. **Honestidad sobre capacidades:** Cuando una herramienta falla, reportarlo inmediatamente. El Monarca prefiere "no puedo" a un diagnóstico falso.
2. **Contexto finito:** La sesión se satura ~40-60%. Usar `delegate_task` para trabajo pesado, no cargarlo todo en el prompt principal.
3. **Protocolo Memento:** Activar con palabra clave "memento" + información → guardar en este archivo + avisar sombras.
4. **ORQUESTACIÓN REAL (2026-09-10):** Las sombras son perfiles Hermes independientes con modelos propios. Orquestar = `hermes -p <perfil> chat -q "<misión>"`. Los subagentes efímeros de `delegate_task` NO son las sombras. Cada sombra con SU identidad, SU modelo, SUS herramientas. Los entregables se verifican en disco.
5. **Dropi/token atado al origen (2026-09-28):** el token de Dropi solo funciona desde su origen autorizado (WordPress); desde otra IP → 401. Toda automatización Dropi se ejecuta vía el puente, no directo.
6. **Nunca dar por buena una descarga sin md5 + bytes mágicos (2026-09-28):** el hosting sirve placeholders idénticos.
7. **Margen ≠ recargo (2026-09-28):** `margen_sobre_costo_pct` engaña; usar `margen_sobre_precio_pct` = costo ÷ (1−pct). En dropshipping el envío decide el negocio. Simular impacto antes de cambiar precios en masa.
8. **Nunca almacenar ni teclear contraseñas:** se usa la bóveda cifrada o se trabaja por plugin/HTTP (el plugin puente evita credenciales de sesión).

---

## 📋 PROCEDIMIENTO PARA SOMBRAS

Cuando reciban una delegación etiquetada `memento`:

1. **Leer** este archivo (`MEMORIA_PERMANENTE.md`) antes de ejecutar la tarea
2. **Ejecutar** la tarea con el contexto completo
3. **Si descubren** información nueva que deba ser permanente, devolverla en su respuesta con el tag `[MEMENTO]`

---

## ⏰ CRON DE MANTENIMIENTO

Un cron diario (6:00 AM) ejecuta:
1. Verificar integridad del archivo
2. Registrar fecha de última actualización
3. Reportar al Monarca si hay información crítica faltante

### REGISTRO DE MANTENIMIENTO (cron diario)
|| Fecha | Integridad | Cambios aplicados ||
||:------|:-----------|:------------------||
|| 2026-10-02 | ✅ OK | Fecha revisada. Verificación de integridad completa. **Sin información crítica faltante**. Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS, tienda e-commerce) presentes, actualizados y coherentes. Protocolo íntegro. ||
|| 2026-10-01 | ✅ OK | Fecha revisada. **Información crítica faltante registrada: Proyecto NEREUS** (sección nueva + fila en historial). NEREUS no figuraba en el protocolo pese a 4 fases ejecutadas. Resto de datos (Monarca, VPS, productos, sombras, precios, infraestructura) presentes y actualizados. ||
| 2026-09-30 | ✅ OK | Fecha revisada. Verificación de integridad completa. Sin información crítica faltante detectada. Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura) presentes y actualizados. |
| 2026-09-29 | ✅ OK | Fecha revisada. Registrado PRODUCTO SECUNDARIO (tienda Dropi), infra Composio/Chromium/Telegram, 4 lecciones nuevas, hito de tienda en historial. |

---

*"El lobo recuerda. El lobo no olvida."*