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

*Última actualización: 2026-10-13*

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
- **Capa 2 (C1+C2) OPERATIVA — 2026-10-07/08:** el agente **responde** al cliente con **compuerta de aprobación** (deny-by-default). `responder.py` (unit `seawolf-responder`): latencia del modelo **invisible**, aviso "escribiendo…" solo 2-4 s, primera respuesta 15 s-3 min (🔥 2-4 s), tope 20 salientes/hora. **C2:** aviso unificado al dueño (nivel+quién+mensaje+acción+borrador), **texto libre = ORDEN**, decisión por **nota de voz** (transcrita + eco), identidad por LID/número, directorio de contactos, fallo de entrega nunca silencioso. Probado de punta a punta con un tercero real (34 s ciclo completo), auditable en el bus (`approved_by: Key`).
- **Capas 3 y 4 — ✅ construidas (2026-10-08, ausencia de 72 h del Monarca):** **C3 Reglas preaprobadas** (`reglas.py`, tipos `notificar`/`auto_respuesta`/`rompe_rojo`, prueba 6/6, **`reglas.json` VACÍO** — las dicta el Monarca) · **C4 Onboarding** (`onboarding.py`: mapa de capacidades honesto + 10 preguntas -> `tenant.json` + mini-contrato + recalibración, prueba 8/8) · **Vigilante de salud** (`healthcheck.py`, cron 30 min, avisa solo tras 2 fallos seguidos).
- **Pendiente:** reglas C3 (del Monarca) · primer cliente real con onboarding · envío de **adjuntos** por el agente · bus en directorio propio (no exponer `filtro.env`) · cuarto de guerra Telegram · descartar transcripciones de video sin habla.
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

**Configuración Maestra v2 (2026-10-11, `intel/Ejercito_de_Sombras_Configuracion_v2.md`):** 11 sombras operativas, cada una con SU soul y SU modelo OpenRouter directo + respaldos (sin gateways, sin `:free`). Reporte dual obligatorio (`QUE HICE · ENTREGABLE · HALLAZGO · BLOQUEO · SIGUIENTE`).

| Sombra | Rol (v2) | Contacto |
|:-------|:---------|:---------|
| **Bellion** | Gran Comandante / Orquestador | `deepseek/deepseek-v4.1-flash` → este chat |
| **Beru** | Auditor General / Informes | `deepseek/deepseek-v4-pro` · `hermes -p beru chat -q "..."` |
| **Igris** | **Copywriting** (persuasión/ventas) | `deepseek/deepseek-v4-flash-0731` |
| **Tank** | **Ventas / Cierre** de leads | `qwen/qwen3.7-flash` |
| **Greed** | Ads / Tráfico pago (sin Meta/AdSense) | `bytedance-seed/seed-1.6-flash` |
| **Iron** | Email Marketing | `deepseek/deepseek-v4-flash-0731` |
| **Tusk** | SEO / Tráfico orgánico | `qwen/qwen3.7-flash` |
| **Kamish** | Redes sociales / distribución | `z-ai/glm-5.3-flash` |
| **Kaisel** | Web Dev (front/back) | `qwen/qwen3-coder-30b-a3b-instruct` |
| **Titan** | UX/UI | `qwen/qwen3-vl-32b-instruct` |
| **Jima** | Automatización (n8n/APIs/Workers) | `qwen/qwen3-30b-a3b-instruct-2507` |

> Nota: los roles cambiaron respecto a la v1; **Igris ya NO es infra VPS** (es copy) y **Tank ya NO es búsquedas** (es cierre). Auditoría Beru: 10/10 PASA. Sueltas de Telegram por orden del Monarca.

### CAPACIDAD: HYPERFRAMES (contenido por código: HTML/CSS/GSAP -> MP4)
**Absorbida 2026-10-11** (`intel/hyperframes/CAPACIDAD-hyperframes.md`). `heygen-com/hyperframes` — **Apache-2.0**, 100% local (Chrome headless + FFmpeg), **sin claves ni nube**. Convierte HTML+CSS+GSAP en MP4 deterministas (hasta 4K, fps 1-240; MP4/WebM/MOV-alfa/GIF/HLS). Nativo: TTS Kokoro, whisper, quitar fondo, LUTs, LUFS, cortes por beat. ~446 bloques. Límites honestos: render ≈2× tiempo real, NO es text-to-video, pesado en RAM. **Sting oficial del estudio** ya renderizado (`renders/seawolf-sting.mp4`, 1080×1920, 10 s). Skill del ejército: `hyperframes-content-SKILL.md` (KAISEL/TITAN/KAMISH). Pitfalls Windows: usar su propio `chrome-headless-shell`; render con el binario global, no `npx`.

### CAPACIDAD: AVATAR KAELEN (robot presentador ESTÁNDAR del estudio) — 2026-10-13
`F:/seawolf/kaelen/` · skill `kaelen-avatar`. Robot con **casco blanco + visera negra**; en la visera viven **ojos LED (estilo EVE)** + **boca-onda** de audio. Pipeline 100% local sobre **HyperFrames**:
- Limpieza (ffmpeg): `delogo` del watermark "Veo" + `chromakey` del verde real **`#08A82E`** con *similarity baja 0.15* + `despill` (⚠️ 0.35 borraba al sujeto).
- **Rastreo del marco LOCAL de la visera:** `CSRT` (ROI por frame) + flujo óptico denso **Farneback + mínimos cuadrados** → `(rx, ry, rot, scale)` por frame. ❌ SIFT/ORB y Lucas-Kanade puntual fallaron (texturas repetidas del casco) — NO reintentar.
- Composición: capa `#vframe` anclada al centro de la visera (`transform-origin` centro) que traslada+rota+escala; `#eyes` y `#mouthLayer` como capas separadas. Boca-onda con forma fija simétrica × amplitud (NO ventana deslizante).
- Voz: **Piper TTS** local (`es_ES-davefx-medium`); envolvente RMS sin librosa (`wave`+numpy, 24 fps; numpy2 rompe scipy).
- Entregables: `kaelen-voz-real.mp4`, `kaelen-verde.mp4`, proyecto HyperFrames en `F:/seawolf/kaelen/kaelen/`.
- **`seawolf-avatar` (SadTalker)** sigue para **avatares humanos**; Kaelen usa la ruta **robot**.

### PRODUCTO: SMART COURSES (nueva línea del estudio — hermana de las Smart Webs) — 2026-10-13
Definición del Monarca: **"un modelo muy pequeño entrenado con el temario del curso"** como tutor → **variante magistral** de la Smart Web.
- **Estructura:** `Información → Video explicativo (Kaelen) → Evaluación → Tutor IA`.
- **Diferencial absoluto:** un curso que **CONVERSA** con el alumno (tutor IA + evaluación, idealmente respuestas abiertas calificadas).
- **PDF: DESCARTADO** como curso y como certificado (el estudio NO es entidad avalada para emitir certificados).
- **Foco vigente:** TODO lo "smart" (Smart Webs + Smart Courses). Pendiente: curso piloto, modelo de cobro, tipo de evaluación.

### EMBUDO «CURSOS DE DROPSHIPPING LOCAL + SMART SHOP» (plan maestro de negocio) — 2026-10-13
`intel/curso-dropshipping-local/` (`PLAN-CURSOS-TIENDAS.md` + `MANUAL-MAESTRO-tiendas.md`, 724 líneas destiladas de un curso de referencia de ~8h20m — "Aprender E-commerce"). Principio: **Dropi es solo el proveedor; el método y la marca son nuestros.**
- **Embudo:** `N1 (imán) → N2 (imán + DOLOR) → N3 (SERVICIO de pago = $$$)`.
- **N1** «Vender por redes sociales» (concepto, sin herramientas difíciles; **sin Meta Ads**) · **N2** «Vender productos de Dropi con Google Sites (manual y trabajoso A PROPÓSITO — crea el dolor)» · **N3 = Smart Shop** (le armamos su tienda: Astro + Dropi API + capa IA → "cuestión de maquillaje", margen alto).
- **Doble carril:** gratis **con anuncios** (Adsterra u otra red rápida) = alcance/captación · pago **sin anuncios** + bonus = ingreso/filtra serios.
- **Precios propuesta (COP, ajustable):** N1 **79.000** · N2 **169.000** · Bundle N1+N2 **199.000** · **Smart Shop 890.000** (o 3 cuotas) · mantenimiento **49.000/mes**. Dominio/hosting aparte (a favor del cliente). ⏳ **Pendiente de aprobación del Monarca** (precios + arrancar Fase 0 con **tank**).
- **Reparto:** Fase 0 destilar (tank) + guiones N1 (igris) · Fase 1 afinar tiendas (kaisel+beru) · Fase 2 capa IA Smart Shop/tutor (jima) · Fase 3 diseño (titan) + empaquetado HyperFrames/Kaelen (kaisel) · QA (beru).
- **Doctrina limpia:** manual depurado (fuera Meta/FB/pixel/Shopify).

### DOCTRINA «SMART WEB» (estándar de sitios del estudio)
De la misión Wonder's Voley (`intel/convoca/20261010-wonders-voley/CONCLUSIONES-smart-web-wonders.md`):
- **Una sola pieza** (HTML+CSS+JS); multipágina por router hash; **un formulario por subpágina** -> correo del cliente (sin backend ni claves).
- **Tema oscuro por defecto** + claro · **contenido visible sin JS** · **IA embebida con la clave server-side** (Cloudflare Worker).
- **Elección de modelo = calidad, no precio** (el volumen local es bajo): núcleo `google/gemini-2.5-flash-lite` (~$0.86/mes), económico `qwen/qwen3.7-flash` (~$0.27/mes), potencia `google/gemini-2.5-flash` (~$3.84/mes). La palanca real es acortar **contexto** (últimos ~12 mensajes). **Prohibido en producción:** `:free`/`:batch` y razonamiento (respuestas vacías; si aplica, `reasoning.enabled=false`).
- **Verificación:** renderizar, no solo auditar código fuente (BERU 10/10 leyendo código pero el fallo real solo apareció al renderizar). Un coder de 30B se atasca con pieza grande -> re-tareas con modelo fuerte, "una sola pasada".

### PROYECTO: SMART WEB — CLUB WONDER'S VOLEY (Madrid) — ⏸️ PAUSADA
Primera «Smart Web» del portafolio; sitio del **Club Deportivo Wonder's Voley** (escuela de voleibol de **Kennya**, hermana del Monarca y futura embajadora del estudio en España). Orquestada con el protocolo «Convoca a las Sombras» (IGRIS copy + TUSK SEO -> TITAN diseño -> KAISEL build -> JIMA capa IA -> BERU auditoría). Entregables: pieza v2 (171 KB, 10 vistas, 9 formularios), archivo autocontenido (882 KB), PDF de requerimientos para la hermana. **PAUSADA a petición de la cliente** hasta fin de temporada. Al retomar: recibir fotos/logo vectorial/tarifas, publicar en dominio temporal Hostinger -> migrar a Cloudflare + Worker IA. **Handoff de retorno listo (2026-10-13, `diario-de-sombras/wonders-retomar-20261013.md`):** checklist de despliegue + datos públicos del club (email `clubdeportivowonders@gmail.com`, WhatsApp `+34 614 696 077`, colores negro/rojo/blanco) + upsell natural (video de bienvenida con Kaelen o Smart Course deportivo). Refs: `intel/convoca/20261010-wonders-voley/`, `diario-de-sombras/sesion-smart-web-wonders-20261010.md`.

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
| 2026-10-06→08 | **Capa 2** (motor de respuestas + compuerta de aprobación + reglas C3 + onboarding C4) — diseño original en `intel/capa2-system-prompt-draft-20261006.md` | ✅ Construida (ver fila 2026-10-07/08) |
| Pendiente | Landing page + pasarela COP | ⏳ Pendiente |
| Pendiente | Traducción paneles restantes | ⏳ Pendiente |
| Pendiente | Pruebas de campo (2 frentes) | ⏳ Pendiente |
| 2026-10-07/08 | **Capas 2, 3 y 4 de Seawolf Agent:** C1 motor de respuestas humanas + C2 compuerta de aprobación (voz, video, determinismo, aviso unificado) probadas con tercero real; C3 reglas preaprobadas + C4 onboarding + vigilante de salud | ✅ Operativas |
| 2026-10-11 | **Ejército de Sombras v2 + HyperFrames + Smart Web Wonder's Voley:** config maestra de 11 sombras (souls+modelos+fallbacks), capacidad HyperFrames absorbida (sting oficial), primera Smart Web (club de Kennya) entregada y **pausada** | ✅ Entregado — Smart Web pausada por la cliente |
| 2026-10-13 | **Avatar Kaelen + línea de producto SMART COURSES + embudo Cursos/Smart Shop:** Kaelen (robot presentador estándar, visera viva, skill `kaelen-avatar`) cerrado; acuñada la línea **Smart Courses** (curso que conversa: tutor IA + evaluación; PDF descartado); plan maestro del embudo N1/N2/N3 (Cursos imán → Smart Shop servicio) + manual maestro de dropshipping local; handoff de retorno de Wonder's Voley | ✅ Entregado — precios del embudo ⏳ pendientes de aprobación |
| Pendiente | Reglas C3 (las dicta el Monarca) · primer cliente real con onboarding · envío de adjuntos por el agente · bus en directorio propio · cuarto de guerra Telegram · landing + pasarela COP · pruebas de campo | ⏳ Pendiente |
| **PRÓXIMO** | Entregar Seawolf Agent al **PRIMER CLIENTE** (desprender a Bellion de lo operativo paulatinamente) | 🔥 Prioridad |

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
| 2026-10-13 | ✅ OK | Fecha revisada. **Información crítica faltante registrada (sesión 2026-10-13):** (1) **AVATAR KAELEN** — sección nueva: robot presentador ESTÁNDAR del estudio (casco blanco + visera negra, ojos LED, boca-onda), pipeline HyperFrames + tracking CSRT/Farneback + Piper TTS, skill `kaelen-avatar`, entregables en `F:/seawolf/kaelen/`; (2) **PRODUCTO SMART COURSES** — sección nueva: nueva línea hermana de las Smart Webs (curso que CONVERSA: Información→Video Kaelen→Evaluación→Tutor IA; PDF descartado como curso/certificado); (3) **EMBUDO CURSOS DROPSHIPPING LOCAL + SMART SHOP** — sección nueva: plan maestro N1/N2/N3, doble carril (gratis con anuncios Adsterra / pago), precios COP (79k/169k/199k/890k + 49k mes), manual maestro destilado (724 líneas), reparto de sombras; (4) **Wonder's Voley** — añadido handoff de retorno 2026-10-13 (checklist + datos del club + upsell Kaelen); (5) Historial actualizado. Integridad estructural OK. |
| 2026-10-12 | ✅ OK | Fecha revisada. **Información crítica faltante registrada (sesiones 2026-10-07→10-11):** (1) **Capa 2 OPERATIVA** (C1 respuestas humanas + C2 compuerta de aprobación) — el protocolo la tenía como "pendiente"; (2) **Capas 3 y 4 construidas** (reglas preaprobadas + onboarding + vigilante de salud); (3) **Ejército de Sombras Config v2** — tabla ROSTER desactualizada reemplazada (11 sombras con modelos reales; Igris=copy, Tank=cierre, nuevas Greed/Iron/Tusk/Kamish/Jima); (4) **HyperFrames** absorbido (HTML->MP4) + sting oficial; (5) **Doctrina Smart Web** (elección de modelo por calidad + palanca de contexto); (6) **Proyecto Smart Web Wonder's Voley** (club de Kennya) entregado y PAUSADO; (7) Historial actualizado. Además **corregida corrupción de la tabla de mantenimiento** (filas con `||` de más). Integridad estructural OK. |
| 2026-10-11 | ✅ OK | Fecha revisada. **Verificación de integridad completa. Sin información crítica faltante.** Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS/LOBO, tienda e-commerce, marca LOBO, WAHA/Capa 1, Capa 2 pendiente) presentes, actualizados y coherentes. Protocolo íntegro. |
| 2026-10-10 | ✅ OK | Fecha revisada. **Verificación de integridad completa. Sin información crítica faltante.** Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS/LOBO, tienda e-commerce, marca LOBO, WAHA/Capa 1, Capa 2 pendiente) presentes, actualizados y coherentes. Protocolo íntegro. |
| 2026-10-09 | ✅ OK | Fecha revisada. **Verificación de integridad completa. Sin información crítica faltante.** Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS/LOBO, tienda e-commerce, marca LOBO, WAHA/Capa 1, Capa 2 pendiente) presentes, actualizados y coherentes. Protocolo íntegro. |
| 2026-10-08 | ✅ OK | Fecha revisada. **Verificación de integridad completa. Sin información crítica faltante.** Todos los datos clave (Monarca, VPS, productos, sombras, precios, infraestructura, Proyecto NEREUS, tienda e-commerce, marca LOBO, WAHA/Capa 1) presentes, actualizados y coherentes. Protocolo íntegro. |
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