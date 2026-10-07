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

*Última actualización: 2026-10-07*

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
- **Mascota / producto agente:** **LOBO** — lobo negro estilo peluche 3D (constante de marca en TODOS los proyectos)
- **Temas:** claro + oscuro, con **OSCURO por DEFECTO**
- **Diferencial de marca:** el "sello de unidad social" (constante en todos los proyectos)
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

### PROYECTO: SEAWOLF NEREUS (Agente personal del Monarca → producto de marca **LOBO**)
**Visión:** Agente personal de Seawolf, construido sobre **CopilotKit/openmuse** (MIT) en el VPS. **NEREUS** es la clave interna en el VPS; de cara al público es el producto de marca **LOBO** (mascota lobo negro).
- **Ubicación:** VPS Hostinger `/opt/nereus` · **Node 24** · puerto **8788**.
- **Memoria/persistencia:** propia — `StoreAgentRunner` (SSE) + **Postgres + pgvector** en Docker (puerto 5433).
- **Gateway LLM:** OpenRouter (`MODEL=openrouter/<vendor>/<model>`, vía `openaiCompatibleText`). Sin servicios cerrados propietarios.
- **Fase 0-2:** ✅ Clone + build + 276/276 tests verdes · persistencia propia (Postgres + pgvector) · gateway OpenRouter operativo.
- **Fase 3 (VOZ) — ✅ integrada (10-01→10-02):** **VoiceBox v0.5.0** (Qwen3-TTS + Kokoro + Whisper) en Docker. **Voz de marca masculina CLONADA** (perfil "NEREUS", motor `qwen`, 3 muestras del Monarca; presets ES `em_alex` masc. / `ef_dora` fem.). Clonación **en vivo inviable en CPU** (Qwen 1.7B = OOM >6 GB; 0.6B ≈162 s / 7.2 s audio) → sin GPU solo sirve para notas/lotes. **Streaming por frases** (`voice-gateway.py`, `127.0.0.1:8799`): TTFA **0.75 s** (≈8× menos espera), conversación fluida **sin GPU** con Kokoro (Apache-2.0). Clon = **premium opcional** futuro.
- **Fase 4 (MEMORIA) — ✅ cerrada y persistente (10-02):** **Mem0** (semántica, integrada en el agente, probada: recall score 0,65) + **Graphiti** (temporal, **Neo4j 5.26**, MCP `127.0.0.1:8100`; FalkorDB descartado por incompatibilidad de versión). Todo bajo **systemd** (`nereus-mem0.service`, `nereus-graphiti.service`, `restart: unless-stopped`; puertos solo localhost). Coste IA: gratis/céntimos.
- **Pendiente:** cablear Graphiti en el flujo de NEREUS · conectores · multi-tenant · onboarding · cobro · pruebas integrales · decisión nodo de voz (GPU vs TTS en cliente).
- **Refs:** `intel/fase-{0,1,2,3}-nereus-*.md`, `intel/nereus-{memoria-fase4,memoria-systemd,streaming-por-frases,voz-clonada,graphiti-modelos}-*.md`, `diario-de-sombras/sesion-openmuse-a-nereus-20260930.md`.
- **Systemd NEREUS en VPS:** `nereus-api` · `nereus-mem0` · `nereus-graphiti` · `nereus-voice-gateway` (detenido, migra a PC) · `seawolf-fw` (endurecido de puertos Docker).

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

### CANAL: WHATSAPP (WAHA) — plato fuerte de Seawolf Agent
**Ruta (decisión vigente):** no oficial — Baileys → **WAHA Core** → WAHA Plus. El Monarca rechaza la burocracia de Meta. **Riesgo honesto:** viola ToS de WhatsApp → baneo; mitigación = número dedicado, calentamiento y límites; perfil bajo por diseño (nunca masivo, nunca robótico, destinatario único).
- **Montado, VINCULADO y con Filtro (Capa 1) — 2026-10-06:** contenedor `waha` (`devlikeapro/waha:latest`, **motor GOWS** — obligatorio por el **passkey** de WhatsApp; WEBJS/NOWEB fallan con `Cmd.refreshQR is not a function`; GOWS gratis desde WAHA 2026.6.1; `127.0.0.1:3000`, API key en `/root/.waha.env` chmod 600); **sesión `seawolf` = `WORKING`**, número **+57 300 206 7487** vinculado (perfil "Seawolf Agent"). Receptor `/opt/waha/sink.py` (`waha-sink.service`, log `/opt/waha/messages.log`); webhook `http://172.16.0.1:3010/webhook` (gateway Docker, privado).
- **Filtro (Capa 1) CONSTRUIDO:** `/opt/waha/filtro.py` (unit `seawolf-filtro.service`, puerto **3011**). Criterio del Monarca: 🔥 rojo = perturba seguridad o exige atención inmediata · 🟠 naranja = **mitigable ahora, arreglo después** (la acción empieza por la mitigación) · 🟡 consulta · 🟢 informativo. Voz → transcribe con **Groq `whisper-large-v3-turbo`**; imagen → describe con `google/gemini-2.5-flash` (OpenRouter); clasifica con `google/gemini-2.5-flash` (JSON). Entrega 🟠🔥 a la **Línea 1** del cliente vía WAHA `sendText`. Log en `/opt/waha/filtro.log`.
- **Trampas cazadas:** un contenedor NO alcanza `127.0.0.1` del host → el sink va al gateway Docker `172.16.0.1:3010`; el backlog de webhooks fallidos sigue reintentando → mirar la URL **dentro** del error; `PUT /api/sessions/<name>` **reinicia** la sesión (nuevo QR).
- **MODELO DE 2 LÍNEAS (CONFIRMADO):** **Línea 1** = número **personal** del cliente (ya existe), recibe SOLO lo filtrado, **intocable**. **Línea 2** = línea **dedicada** donde VIVE el agente (eSIM/SIM aparte); el cliente migra ahí sus contactos de trabajo y el agente observa/clasifica/filtra. Aviso **L2 (bot) → L1 (personal)** = notificación natural; no hace falta 3ª línea. Privacidad = arma de venta (el agente solo lee L2).
- **Canal Bellion → Monarca:** helper `/opt/waha/avisar.sh "mensaje"` (L2 → +57 312 533 0127). Probado ✅.
- **Falta:** construir la **Capa 2** (automatización/delegación); ver diseño en `intel/capa2-system-prompt-draft-20261006.md`.
- **Skill:** `seawolf-whatsapp-waha`.

### INFRAESTRUCTURA TÉCNICA
- **Frontend:** WebUI propia (login personalizado, logo lobo, 100% español)
- **Backend:** Hermes Agent (fork MIT → seawolf-agent)
- **Modelo orquestador:** bellion-orchestrator
- **Modelo de visión:** google/gemini-2.5-flash (vía OpenRouter) — `auxiliary.vision.provider=openrouter` en config.yaml
- **Chromium en Windows:** `AGENT_BROWSER_ARGS='--no-sandbox,--disable-dev-shm-usage'` (setx en variable de entorno del sistema)
- **Herramientas:** Composio SDK (Python, API key `ak_` prefijo) — CLI Composio NO funciona en Windows, usar SDK Python o npx
- **Gmail:** seawolfk.studio@gmail.com (OAuth autorizado vía Composio SDK)
- **Canal principal:** **WhatsApp (vía WAHA).** ⚠️ **Telegram APAGADO el 2026-10-04** por bucle de token: vivía en 2 configs (`/opt/data/config.yaml` → `gateway.platforms.telegram` y `/opt/data/profiles/bellion/config.yaml`). Fix = `enabled: false` **+ neutralizar el token** en ambos (solo `enabled:false` NO bastaba; hay configs **por sombra** en `/opt/data/profiles/*/config.yaml`). Se rehará como "sala de guerra" con cada sombra aparte. (Monarca no puede revisar el teléfono → respuestas de audio.)
- **WebUI (rebranding desplegado 2026-10-04):** favicons del lobo (regenerados desde el SVG; antes eran el caduceo de Hermes), titlebar → "Seawolf Agent", **571 cadenas i18n** "Hermes"→"Seawolf" (protegiendo comandos/rutas/claves internas). Repo `seawolf-agent-webui` commit `48d0d161` (push + pull en VPS). En vivo: `https://agente.sw-st.net` → 200, título "Seawolf Agent".
- **Puertos VPS (reconocimiento 2026-10-04):** 8787 = WebUI Seawolf Agent · 8085→9119 = docker `hermes-agent-core` = **Ejército de Sombras (12 gateways s6)** — ⚠️ expuesto en `0.0.0.0`, llevar al tailnet · 8000/9443 = Portainer — ⚠️ público, mover a Tailscale (`https://100.114.5.98:9443`) · **8642 declarado pero fantasma → CERRADO** (limpiado de `config.yaml`/`DEPLOY.md`).
- **Multi-tenant:** Perfiles separados por cliente en Hermes

### RED DE SOMBRAS (Agentes)
**Cómo orquestar (REGLA DE ORO, 2026-09-10):** las sombras son **perfiles Hermes REALES con modelos propios**. Se invocan con `hermes -p <perfil> chat -q "<misión>"`. `delegate_task` NO son las sombras — son subagentes efímeros de trabajo auxiliar.

| Sombra | Rol | Cómo contactar |
|:-------|:----|:---------------|
| **Bellion** | Gran Comandante / Estratega | Este mismo chat (modelo fijado: `deepseek-v4.1-flash`) |
| **Beru** | Escriba / Auditor / Diario | `hermes -p beru chat -q "..."` |
| **Igris** | Guerrero / Infra VPS | `hermes -p igris chat -q "..."` |
| **Tank** | Puntero / Búsquedas | `hermes -p tank chat -q "..."` |
| **Kaisel** | Despliegues / Alas | `hermes -p kaisel chat -q "..."` |

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
| 2026-09-30→10-02 | **Proyecto NEREUS** (agente personal → marca LOBO): clone+build (276 tests), persistencia Postgres/pgvector, gateway OpenRouter, Fase 3 Voz (VoiceBox + clon de voz + streaming por frases TTFA 0,75 s), Fase 4 Memoria (Mem0 + Graphiti/Neo4j bajo systemd) | ✅ Fases 0-4 OK — pendiente conectar Graphiti al flujo, pruebas integrales y decisión nodo de voz |
| 2026-10-04 | **Saneamiento VPS + Rebranding + Tubo de WhatsApp:** reconocimiento de puertos, Telegram apagado, 8642 cerrado, rebranding WebUI (favicons lobo + i18n) desplegado, WAHA montado y probado (`session.status` capturado) | ✅ Tubo listo |
| 2026-10-06 | **Filtro WhatsApp (Capa 1) + modelo de negocio 2 líneas:** WAHA migrado a motor **GOWS** (passkey), sesión `seawolf` vinculada (`WORKING`, +57 300 206 7487), **Filtro Capa 1** construido (🔥🟠🟡🟢 + voz Groq + imagen Gemini), canal Bellion→Monarca (`avisar.sh`), pipeline de 100 repos IA, **diseño de la Capa 2** | ✅ Capa 1 operativa — **Capa 2 pendiente de construir** |
| Pendiente | Construir **Capa 2** (automatización/delegación: motor de respuestas con cola/pausas/presencia, compuerta de aprobación, onboarding configurable, límites + auditoría) — diseño en `intel/capa2-system-prompt-draft-20261006.md` | ⏳ Pendiente |
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
| Fecha | Integridad | Cambios aplicados |
|:------|:-----------|:------------------|
| 2026-10-07 | ✅ OK | Fecha revisada. **Información crítica faltante registrada (sesión 2026-10-06: Filtro WhatsApp Capa 1):** (1) **Canal WhatsApp/WAHA** actualizado — migrado a motor **GOWS** (passkey obligatorio; WEBJS/NOWEB fallan), sesión `seawolf` **`WORKING`** con número **+57 300 206 7487** (ya no "falta escanear el QR"); (2) **Filtro (Capa 1) CONSTRUIDO** (`/opt/waha/filtro.py`, `seawolf-filtro.service`, puerto 3011) con criterio del Monarca 🔥🟠🟡🟢, voz vía Groq `whisper-large-v3-turbo`, imagen y clasificación con `gemini-2.5-flash`, entrega a Línea 1; (3) **Modelo de negocio de 2 líneas** documentado (L1 personal intocable / L2 dedicada con el agente); (4) **Canal Bellion→Monarca** (`/opt/waha/avisar.sh`); (5) **Capa 2** — diseño en `intel/capa2-system-prompt-draft-20261006.md` registrado como pendiente; (6) Historial actualizado (fila 2026-10-06 + pendiente Capa 2). Integridad estructural OK. |
| 2026-10-05 | ✅ OK | Fecha revisada. **Información crítica faltante registrada:** (1) **NEREUS Fase 3 completada** (voz clonada + streaming por frases TTFA 0,75 s) y **Fase 4** (Mem0 + Graphiti/Neo4j bajo systemd) — la sección estaba congelada en "Fase 3 parcial"; (2) **Canal WhatsApp (WAHA)** — sección nueva: tubo montado y probado, ruta no oficial, trampas y pendiente del QR; (3) **Telegram apagado** (corregido el "Canal principal" obsoleto); (4) **Rebranding WebUI desplegado** (favicons lobo, i18n, commit 48d0d161); (5) **Puertos VPS** y cierre del 8642 fantasma; (6) Historial actualizado. Además **corregida corrupción de la tabla de mantenimiento** (filas con `||` de más). |
| 2026-10-04 | ✅ OK | Fecha revisada. **Verificación de integridad completa. Sin información crítica faltante.** Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS, tienda e-commerce, marca LOBO) presentes, actualizados y coherentes. Protocolo íntegro. |
| 2026-10-03 | ✅ OK | Fecha revisada. **Información crítica faltante registrada:** (1) **Marca LOBO** — mascota/producto agente (lobo negro peluche 3D), temas claro+oscuro con oscuro por defecto, sello de unidad social añadidos a MARCA; (2) **NEREUS ↔ LOBO** — enlace de marca documentado (NEREUS = clave interna del producto LOBO); (3) **Modelo de Bellion fijado** (`deepseek-v4.1-flash`); (4) **Corregida la Red de Sombras** — decía `delegate_task`, contradiciendo la regla de oro #4; ahora indica `hermes -p <perfil> chat -q`. Integridad estructural completa (174→181 líneas, todas las secciones presentes). |
| 2026-10-02 | ✅ OK | Fecha revisada. Verificación de integridad completa. **Sin información crítica faltante**. Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS, tienda e-commerce) presentes, actualizados y coherentes. Protocolo íntegro. |
| 2026-10-01 | ✅ OK | Fecha revisada. **Información crítica faltante registrada: Proyecto NEREUS** (sección nueva + fila en historial). NEREUS no figuraba en el protocolo pese a 4 fases ejecutadas. Resto de datos (Monarca, VPS, productos, sombras, precios, infraestructura) presentes y actualizados. |
| 2026-09-30 | ✅ OK | Fecha revisada. Verificación de integridad completa. Sin información crítica faltante detectada. Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura) presentes y actualizados. |
| 2026-09-29 | ✅ OK | Fecha revisada. Registrado PRODUCTO SECUNDARIO (tienda Dropi), infra Composio/Chromium/Telegram, 4 lecciones nuevas, hito de tienda en historial. |

---

*"El lobo recuerda. El lobo no olvida."*