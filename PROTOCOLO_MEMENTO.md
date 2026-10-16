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

*Última actualización: 2026-10-16*

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
- **Estado (2026-10-14 — retomada tras ~15 días de abandono):** paquete de despliegue **APTO PARA SUBIR** — `seawolf-tienda-hostinger.zip` + `seawolf-tienda-20261014-0131.zip` (sello `20261014-0131`, SHA-256 `9cdfe811…`), 989 archivos · 14,2 MB · 200 productos (199 con foto real + ID Dropi). Hash ZIP ↔ fuente idéntico en las 2 PHP · cero secretos · `index.html` en raíz. **BERU re-auditó → PASA** (3 bloqueantes cerrados). Pipeline autónomo (`mantenimiento\*.bat`) probado. **El DESPLIEGUE todavía NO se ha hecho** — solo falta que el Monarca suba el ZIP, ponga los 2 secretos en `public_html/api/` y lance la **orden real de prueba** (ya autorizada).
- **Catálogo vivo (2026-10-14):** puente `Dropi Bridge v3` **VIVO** (WordPress de Shopio: PHP 8.2.34 · WP 7.0.7 · WooCommerce 11.2.0), 246 entradas → **199 SKUs únicos** (≈45 duplicados). Fuente de verdad sigue siendo WordPress (no reconstruir).
- **Mejoras inyectadas (2026-10-13, `intel/TIENDA-seawolf-mejoras-desde-destilacion-20261013.md`, 12 mejoras/16 tareas):** lista blanca de **24 departamentos** (bloquea los 9 sin cobertura) · huella propia por teléfono (40-50% del flete) · compuerta de confirmación (mata al cliente fantasma) · seguimiento de los 9 estados → mensajes automáticos · copys GADO + ángulo por ocasión. **La promesa, hecha arquitectura:** autorización del dueño por Telegram (con *rompe-rojo*) → creación en Dropi → post-venta auditada (`approved_by`), reutilizando el patrón **C3** del Seawolf Agent.
- **Precios v4 (2026-10-13, `seawolf-store/mantenimiento/precios-real-20261013-v4.csv`, 200 filas):** 97 SANOS→**MANTENER** (114) · 17 A_REVISAR + 63 **DECISION_MONARCA** (85 esperan la palabra del Monarca) · 11 SUBIR_SUAVE · 10 PACK · 1 RETIRAR_CANDIDATO. **Hallazgo estructural:** `< $20.000 COP` inviable con flete de $10.000; punto dulce **$40.000–$100.000**.
- **Decisión de canal (2026-10-14):** **Telegram para alertas al dueño** (sin riesgo de ban — paracaídas) · **WhatsApp solo para clientes DENTRO de una conversación que el cliente abrió** (WAHA en localhost; requiere endpoint autenticado en el VPS). Mensaje frío/masivo por WAHA = lo que banea. Propuesta ⏳ pendiente de OK: endpoint seguro + `notificador.php` multicanal + regla de ventana por cliente + rotar token de `avisar.sh` (sombras JIMA + KAISEL).
- **Rotación pendiente:** la llave del puente y la clave del procesador deben rotarse (estuvieron en el ZIP viejo y en el historial de git, en texto plano).
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
- **Precios APROBADOS por el Monarca (2026-10-13, commit `54ce192` — ajuste −30% sobre la propuesta, excepto mantenimiento; COP):** N1 **55.000** · N2 **118.000** · Bundle N1+N2 **139.000** · **Smart Shop 620.000** (o 3 cuotas) · mantenimiento **49.000/mes**. Conversión USD registrada con tasa **3.198,10**. Dominio/hosting aparte (a favor del cliente). ✅ **APROBADO** (la propuesta previa 79k/169k/199k/890k quedó superada).
- **Decisiones del Monarca aplicadas (2026-10-13):** **Nivel 2 = Google Sites** (NO WordPress; WordPress/WooCommerce queda solo como referencia del curso, Anexo A) · enlace de registro Dropi: sirve cualquier enlace que otorgue la exoneración (~$5.000 COP/venta) · **burocracia Meta PROSCRITA** (demolida §6: fuera Fan Page/2FA, Business Manager, Pixel, grupos FB, IG profesional; canales permitidos = WhatsApp/estados, TikTok, orgánico) · **Nivel 1 · módulo 5 = [MÉTODO SEAWOLF]** (el curso de referencia no enseña a vender por redes; ese módulo es nuestro).
- **Estado Fase 0 (2026-10-13):** `MANUAL-MAESTRO-tiendas-v5.md` auditado por **BERU → PASA** (9/9 verificaciones) · **6 guiones N1 para Kaelen** listos (`igris/guiones-N1/`, 7 archivos). Todo en `intel/curso-dropshipping-local/`.
- **Reparto:** Fase 0 destilar (tank) + guiones N1 (igris) · Fase 1 afinar tiendas (kaisel+beru) · Fase 2 capa IA Smart Shop/tutor (jima) · Fase 3 diseño (titan) + empaquetado HyperFrames/Kaelen (kaisel) · QA (beru).
- **Doctrina limpia:** manual depurado (fuera Meta/FB/pixel/Shopify).

### PROYECTO: «EL CÍRCULO PUBLICITARIO» (línea de montaje de impulso de marca) — 2026-10-14
`intel/plan-circulo-publicitario-20261014.md` (+PDF) + app interactiva `intel/circulo-publicitario-app.html` + informe de motores OSS. Concepto aterrizado a plano construible; uso interno primero, servicio vendible con métricas después.
- **Qué es:** una **línea de montaje** que toma un producto/servicio X y lo empuja a viralizarse en redes por **impulsos repetibles**. No se vende "publicación automática" — se vende **IMPULSO CON MÉTRICAS** (el valor = ángulo creativo + bucle de métricas; la automatización es commodity).
- **Arquitectura — 6 estaciones:** (1) Concepto/ángulo → por **6 ejes** (dolor·deseo·envidia·miedo·curiosidad·estatus·humor·prueba social); (2) Atributos/hooks → **rúbrica 0–5 × 5 criterios** (Hook·Dolor·Diferenciación·Prueba·Encaje); (3) Creativos (copy+imagen+video); (4) Variantes nativas por red (30-40); (5) Publicación multi-cuenta; (6) Medición → **Kill/Scale**. Estaciones 1 y 6 exigen juicio del Monarca; el resto se automatiza.
- **Embudo 100→10** (el corazón): 15-20 ideas por eje → ~100 → rúbrica → **Top 10** → 5 hooks por idea ganadora (se testea el **hook**, no el contenido).
- **Matriz de plataformas:** TikTok, IG Reels, YT Shorts, X, LinkedIn, FB, Pinterest, Threads/Bluesky (formato/hook/cadencia por red). Ganchos "modo Temu" = precio·urgencia·demo visual.
- **Base tecnológica (repos MIT verificados, informe de tema `informe-tema-circulo-publicitario-redes-20261014.md`):** pool MIT **MUY flaco** — los grandes (Postiz AGPL, n8n fair-code, Activepieces/Automatisch open-core, Socioboard GPL) quedan FUERA por licencia. **Ganador: `inovector/mixpost`** (3.812★, MIT puro, Vue+Laravel, self-hosted = "Buffer/Hootsuite self-hosted"; ⚠️ verificar features tras el muro Pro). Complementos: `langchain-ai/social-media-agent` (2.841★, MIT, capa IA URL→post con human-in-the-loop) y `Katzca/AutoSocial` (1.386★, MIT, video corto local). Creativos: MoneyPrinterTurbo (126.9k★), autoclip, LocalAI.
- **Piloto F1:** producto ficticio **USB 1TB + llavero** → 10 creativos + métricas → escalar top 2, matar el resto. Fases F0(aplicativo✅)→F5(productizar como servicio).
- **Riesgos honestos:** baneos por automatizar publicación con navegador (preferir API oficial/mixpost) · contenido genérico sin diversidad de ejes · "impulso agresivo" mal calibrado = spam.

### OPTIMIZACIÓN DE GASTO (TOKENS / API) — 2026-10-14
`intel/informe-tema-plan-anti-picos-20261014.md`, `intel/informe-tema-comparativa-deepseek-v4.1-vs-qwen3.8-flash-20261014.md`, `intel/monitor-gasto-tokens.py`. Encargado por el Monarca (reducir sangría de API).
- **Ahorros APLICADOS (via `hermes config set`, efecto próxima sesión):** skill **`caveman`** activa (output −40–65%) · **caché de prompt** activa · `display.interim_assistant_messages: true→false` · `compression.threshold: 0.5→0.4` · backup `config.yaml.bak-*`.
- **Precios REALES DeepSeek V4.1 Flash** (por 1M USD): input **$0.01584** · output **$0.891** · cache-read **$0.0054**. **Precio PLANO 24/7 — SIN horas pico** (el "pico 2×" era de otro modelo, `deepseek-v4-pro-0813`). ⚠️ Lección: nunca editar `config.yaml` a mano (guardrail lo bloquea) → `hermes config set`.
- **Veredicto comparativa:** mantener DeepSeek V4.1 Flash (~9,5× más barato en input y ~3× en caché que Qwen3.8 Flash; Qwen solo gana en output −47% y en entrada de video).
- **Diagnóstico real:** gasto acumulado **$12,76** en 64 sesiones → **dos tercios = output/razonamiento + cache-read**, ambos crecen con **sesiones maratónicas** (el gasto NO es constante: días normales $0,00–0,04 vs días con sesión gigante $1,25–2,44). Los "picos" reales son **sesiones largas**, no horarios.
- **Plan anti-picos (6 palancas por impacto):** (1) **cerrar sesión al pasar ~100 msgs o ~$0,50 → diario → sesión nueva** (el mayor; corta 70-80% del reenvío de contexto); (2) bajar `reasoning_effort` en rutina (razonamiento = 35% del gasto; sugerido `low`/`minimal` por defecto); (3) `caveman`; (4) `compression 0.4`; (5) modelo según tarea (rutina→`deepseek-v4-flash-0731` o gratis); (6) monitor de alerta temprana.
- **Monitor entregado:** `python "C:\Users\Admin\intel\monitor-gasto-tokens.py"` (lee `state.db`, reporta gasto de hoy/7 días, top 5 sesiones, alerta si día >$2,00 o sesión >$0,50). Programable 1×/día.

### DOCTRINA «SMART WEB» (estándar de sitios del estudio)
De la misión Wonder's Voley (`intel/convoca/20261010-wonders-voley/CONCLUSIONES-smart-web-wonders.md`):
- **Una sola pieza** (HTML+CSS+JS); multipágina por router hash; **un formulario por subpágina** -> correo del cliente (sin backend ni claves).
- **Tema oscuro por defecto** + claro · **contenido visible sin JS** · **IA embebida con la clave server-side** (Cloudflare Worker).
- **Elección de modelo = calidad, no precio** (el volumen local es bajo): núcleo `google/gemini-2.5-flash-lite` (~$0.86/mes), económico `qwen/qwen3.7-flash` (~$0.27/mes), potencia `google/gemini-2.5-flash` (~$3.84/mes). La palanca real es acortar **contexto** (últimos ~12 mensajes). **Prohibido en producción:** `:free`/`:batch` y razonamiento (respuestas vacías; si aplica, `reasoning.enabled=false`).
- **Verificación:** renderizar, no solo auditar código fuente (BERU 10/10 leyendo código pero el fallo real solo apareció al renderizar). Un coder de 30B se atasca con pieza grande -> re-tareas con modelo fuerte, "una sola pasada".

### PROYECTO: SMART WEB — CLUB WONDER'S VOLEY (Madrid) — ⏸️ PAUSADA
Primera «Smart Web» del portafolio; sitio del **Club Deportivo Wonder's Voley** (escuela de voleibol de **Kennya**, hermana del Monarca y futura embajadora del estudio en España). Orquestada con el protocolo «Convoca a las Sombras» (IGRIS copy + TUSK SEO -> TITAN diseño -> KAISEL build -> JIMA capa IA -> BERU auditoría). Entregables: pieza v2 (171 KB, 10 vistas, 9 formularios), archivo autocontenido (882 KB), PDF de requerimientos para la hermana. **PAUSADA a petición de la cliente** hasta fin de temporada. Al retomar: recibir fotos/logo vectorial/tarifas, publicar en dominio temporal Hostinger -> migrar a Cloudflare + Worker IA. **Handoff de retorno listo (2026-10-13, `diario-de-sombras/wonders-retomar-20261013.md`):** checklist de despliegue + datos públicos del club (email `clubdeportivowonders@gmail.com`, WhatsApp `+34 614 696 077`, colores negro/rojo/blanco) + upsell natural (video de bienvenida con Kaelen o Smart Course deportivo). Refs: `intel/convoca/20261010-wonders-voley/`, `diario-de-sombras/sesion-smart-web-wonders-20261010.md`.

### PRODUCTO: SEAWOLF TOOLS (recopilatorio de herramientas propias) — 2026-10-15
**Nombre clave:** SEAWOLF TOOLS — suite de utilidades propias del Monarca (reimplementa software pagado que usaba). Código propio en `intel/seawolf-tools.py`; lanzador `SeawolfTool.bat`.
- **v4 (probado):** **Optimizador multi-disco** (ranking de pesados + duplicados por hash + Papelera Seawolf reversible; `--hard` = borrado real) · **Mapa de espacios** (peso por carpeta raíz de cada disco) · **Mantenimiento programado EDITABLE** (`seawolf-manten.json`: temporales viejos · logs de Hermes · vaciar papelera; activar/días/horario) · **Botón REA** (analiza app JS/Electron o binario → Evidence sellada). Aplicativo web local: `python seawolf-tools.py serve ALL`.
- **Seguridad (diferencial):** mueve (reversible) por defecto; nunca toca nada sin orden; papelera con manifiesto para rescatar.
- **Top 10 funciones objetivo** (`intel/informe-rea-estreno-webui-top10-20261015.md`): 1 optimizador (✅) · 2 limpieza de temporales/cachés · 3 mapa de espacio · 4 mantenimiento programado · 5 arranque/rendimiento · 6 gestor de descargas · 7 detector de "olvidados" · 8 botón REA · 9 auditoría de privacidad/telemetría · 10 panel de discos con alertas.
- **Frentes futuros:** **Gestor de Descargas** (plan tipo JDownloader/MiPony: link grabber + cola + aria2 + auto-organización por tipo; `intel/informe-gestor-descargas-funciones-filmora-20261015.md`) y **Editor de video propio** sobre base **OpenCut** (MIT, 94.772★) — NO clonar Filmora.
- **Regla de oro del catálogo:** la gente perdona funciones; **no perdona que la herramienta los dañe o los bombardee con ads**. Diferencial Seawolf = **seguro + reversible + sin ruido**.

### CAPACIDAD: REA (ingeniería inversa como estudio interno) + LÍNEA LEGAL — 2026-10-15
**`morluto/rea`** (270.701★, **MIT**, TypeScript) = MCP que conecta agentes a herramientas de RE (Ghidra/Hopper/IDA) para entender **cómo funciona una función**, de la conducta de la app al binario. ⚠️ Hype por delante de la evidencia ("real, pero inflado").
- **Instalado:** `rea-agents` v6.5.0 (MIT) registrado en Hermes (`config.yaml`, backup `config.yaml.rea.backup`) + skill `reverse-engineer-anything` en `~/.agents/skills/`; **Ghidra 12.1.4 + JDK21** en `D:` (REA doctor healthy). Uso: `npx -y rea-agents@6.5.0 mcp` o `rea analyze <app>`.
- **Estrenado:** análisis de nuestra `seawolf-webui` (app JS/Electron) → **Evidence sellada** (`ev_f13c39df…`, sha256 raíz `6ddb1d13…`) = trazable/auditable.
- **Para qué sirve:** entender features · interoperabilidad · seguridad · aprendizaje. **NO** es máquina de copiar software pagado.
- **LA LÍNEA LEGAL (regla Seawolf):** *"Mira el original, entiende la función, escribe TU código."* ✅ Reimplementación **clean-room** (así se hizo NEREUS) · ❌ clonar/distribuir app de pago · ❌ **cracks/DRM** = delito y **hunde a Seawolf**. Prueba viva del modelo limpio: familia `storytold/*craft` (wordcraft/deckcraft/soundcraft/figcraft, Apache-2.0).
- **Voz NEREUS — veredicto de licencia (2026-10-15):** **VoiceBox (MIT)** ✅ para el producto; **VoiceStudio (AGPL-3.0)** ❌ descartado para el producto (copyleft; solo herramienta interna aislada).

### PROYECTO: kmoviezone (plataforma de streaming estática) — ACTIVO
**Foco activo del Monarca** (ficha "ACTIVO" en el Panel de Mando). Plataforma de streaming **estática** (películas/series/anime/comics) con **enlaces de terceros** (Streamtape, Voe, Player4Me); la web NO aloja video — genera **fichas automáticas** (imagen/sinopsis/reparto/trailer/capítulos) vía **API de TMDB**.
- **Arquitectura propia (NO WordPress):** un `index.html` único + backend Python (`build.py`) que convierte `catalogo.csv` (fuente de verdad, se edita a mano) en `datos.json`; vigilante `watch.py` regenera y sube por FTP al guardar.
- **Carpeta:** `C:\Users\Admin\streaming_web\` (index.html, build.py, watch.py, catalogo.csv, datos.json, logo.png, MANUAL.txt, INICIAR_VIGILANTE.bat, SUBIR_WEB.bat, backups/).
- **Dominio:** `https://kmoviezone.stream` (operativo). **Modelo:** tier gratis con anuncios + tier miembro de pago sin anuncios.
- **Credenciales (FTP/TMDB):** viven en el **expediente** `seawolf-store/backups/EXPEDIENTE_KMVZONE_20260829.md` — NO duplicar aquí.
- **Skill:** `seawolf-static-streaming-platform`.

### SISTEMA PERSONAL: «PANEL DE MANDO» + CASTIGO + KAMIKAZE (anti-abandono) — 2026-10-14/15
Herramienta personal del Monarca para que **ningún proyecto quede a la mitad** (`intel/plan-panel-mando-20261014.md`, `panel-mando-app-v3.html`, addendum `20261014`). Convierte "finalidad + miedo" en mecánica.
- **3 reglas sagradas:** **máx 3 proyectos ACTIVO** (el resto a la Bóveda) · la **finalidad** (por qué, ligada a la MISIÓN RAÍZ) siempre a la vista · la **pérdida debe doler** (real y pactada, no simbólica).
- **Mecánica:** tareas con pts → % por proyecto → **% TOTAL ponderado** (solo activos) · **sueldo semanal** (cumples = ganas / no cumples = pierdes algo pactado) · **XP/Nivel/Racha/Logros**.
- **12 proyectos (v3) — los 3 ACTIVOS:** **Tiendas (Dropi propio)** · **Seawolf Agent** · **kmoviezone**. **9 en Bóveda:** Círculo Publicitario · Clientes en frío · NEREUS/LOBO · Smart Courses · Web Presence Seawolf · WhatsApp Bridge (WAHA) · Kaelen Avatar · HyperFrames Content · WordPress MCPs.
- **`castigo-panel.py`** (blindado): configuras **CARPETAS** (no archivos), el sistema saca **1 archivo AL AZAR** → no se puede trampear. Modos: `trastero` (reversible) / `borrar` (irreversible, exige `--backup-ok`). Config personal `castigo-config.json` **fuera del repo**. Comandos: `--zonas`, simulacro, `--ejecutar`, `--rescatar N`.
- **Panel KAMIKAZE** (`intel/panel-kamikaze.html`): "smart web" con coach sarcástico/retador + métricas de ánimo (XP/tareas/días/mejor racha + sparkline 14d), animaciones; modo IA OpenRouter opcional.

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
| 2026-10-13 | **Avatar Kaelen + línea de producto SMART COURSES + embudo Cursos/Smart Shop:** Kaelen (robot presentador estándar, visera viva, skill `kaelen-avatar`) cerrado; acuñada la línea **Smart Courses** (curso que conversa: tutor IA + evaluación; PDF descartado); plan maestro del embudo N1/N2/N3 (Cursos imán → Smart Shop servicio) + manual maestro de dropshipping local; handoff de retorno de Wonder's Voley | ✅ Entregado — precios ⏳ pendientes |
| 2026-10-13 | **Cierre Fase 0 Cursos + precios aprobados:** `MANUAL-MAESTRO-tiendas-v5` (auditado BERU → PASA, 9/9) + 6 guiones N1 (IGRIS) + Nivel 2 = Google Sites + precios APROBADOS (−30%): N1 55k/N2 118k/Bundle 139k/Smart Shop 620k/Mant. 49k mes | ✅ Entregado |
| 2026-10-13/14 | **Tienda Dropi: retoma y despliegue:** paquete **APTO PARA SUBIR** (sello `20261014-0131`, BERU PASA), 12 mejoras desde la destilación (lista blanca 24 deptos, huella propia, compuerta de confirmación, seguimiento 9 estados, copys GADO), precios v4 (85 esperan palabra del Monarca), decisión de canal Telegram (dueño)/WhatsApp (clientes en ventana) | ✅ Paquete listo — ⏳ falta que el Monarca suba el ZIP |
| Pendiente | Reglas C3 (las dicta el Monarca) · primer cliente real con onboarding · envío de adjuntos por el agente · bus en directorio propio · cuarto de guerra Telegram · landing + pasarela COP · pruebas de campo | ⏳ Pendiente |
| 2026-10-14 | **«El Círculo Publicitario» + optimización de gasto API:** plan maestro de la línea de montaje de impulso de marca (6 estaciones, embudo 100→10) + app interactiva + informe de motores OSS (ganador `mixpost` MIT); informes de tokens (comparativa DeepSeek vs Qwen, plan anti-picos) + ahorros aplicados (caveman, caché, compression 0.4) + monitor `monitor-gasto-tokens.py` | ✅ Entregado — F1 (piloto) pendiente de OK |
| 2026-10-15 | **SEAWOLF TOOLS v4 + REA + Panel de Mando/KAMIKAZE:** suite de utilidades propias (optimizador multi-disco + mapa de espacios + mantenimiento editable + botón REA; lanzador `SeawolfTool.bat`) · **REA** (`morluto/rea`, MIT) instalado (Ghidra 12.1.4 + JDK21) y estrenado sobre `seawolf-webui` (Evidence sellada) + **línea legal clean-room** · **Panel de Mando v3** (3 focos: Tiendas/Seawolf Agent/kmoviezone) + `castigo-panel` blindado · **Panel KAMIKAZE** · informe Gestor de Descargas + Filmora vs OSS (OpenCut MIT) | ✅ Entregado — kmoviezone registrado como foco ACTIVO |
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
| 2026-10-16 | ✅ OK | Fecha revisada (2026-10-15 → 2026-10-16). **Información crítica faltante registrada (trabajo del 2026-10-15, posterior a la revisión de las 06:01):** (1) **SEAWOLF TOOLS** — sección nueva: suite de utilidades propias (optimizador multi-disco, mapa de espacios, mantenimiento programado editable, botón REA), Top 10 de funciones, frentes de gestor de descargas y editor de video (OpenCut MIT); (2) **REA** — sección nueva: herramienta de RE como estudio interno (MIT, instalado + estrenado con Evidence) + **línea legal clean-room** (cracks/clonar pago = NO) + veredicto de voz (VoiceBox MIT sí / VoiceStudio AGPL no); (3) **kmoviezone** — sección nueva: plataforma de streaming estática, foco ACTIVO del Monarca (dominio kmoviezone.stream, arquitectura HTML+Python+TMDB); (4) **PANEL DE MANDO + CASTIGO + KAMIKAZE** — sección nueva: dashboard gamificado anti-abandono (3 activos de 12 proyectos) + castigo de carpetas al azar; (5) Historial actualizado. Integridad estructural OK (291→324 líneas, todas las secciones presentes). |
| 2026-10-15 | ✅ OK | Fecha revisada (última actualización 2026-10-14 → 2026-10-15). **Información crítica faltante registrada (trabajo del 2026-10-14 posterior a la última revisión, 06:01):** (1) **PROYECTO «EL CÍRCULO PUBLICITARIO»** — sección nueva: línea de montaje de impulso de marca ("IMPULSO CON MÉTRICAS"), 6 estaciones, embudo 100→10, matriz de plataformas, base `mixpost` (MIT) + `social-media-agent` + `AutoSocial`, piloto USB-llavero, riesgos; app interactiva + informe de motores OSS; (2) **OPTIMIZACIÓN DE GASTO (TOKENS/API)** — sección nueva: ahorros aplicados (caveman, caché, compression 0.4, interim off), precios reales DeepSeek (plano 24/7, sin picos), comparativa vs Qwen, diagnóstico ($12,76/64 sesiones, el gasto = sesiones maratónicas), plan anti-picos (6 palancas), monitor `monitor-gasto-tokens.py`; (3) Historial actualizado. Integridad estructural OK (270→291 líneas, todas las secciones presentes). |
| 2026-10-14 | ✅ OK | Fecha revisada. **Información crítica faltante registrada (sesiones 2026-10-13/14):** (1) **TIENDA Dropi** — sección actualizada: retomada tras ~15 días de abandono, paquete **APTO PARA SUBIR** (sello `20261014-0131`, SHA-256 `9cdfe811…`, 989 archivos, BERU re-auditó → PASA), catálogo vivo (246→199 SKUs), 12 mejoras de la destilación, precios v4 (85 esperan palabra del Monarca), rotación de llaves pendiente; (2) **precios del EMBUDO Cursos/Smart Shop APROBADOS** (−30%, commit `54ce192`): N1 55k/N2 118k/Bundle 139k/Smart Shop 620k/Mant. 49k mes + conversión USD tasa 3.198,10; (3) **decisiones del Monarca 2026-10-13**: Nivel 2 = Google Sites, burocracia Meta demolida, módulo 5 = Método Seawolf; (4) **Estado Fase 0**: Manual v5 PASA + 6 guiones N1 (IGRIS); (5) **decisión de canal de notificaciones** (Telegram dueño / WhatsApp clientes en ventana); (6) Historial actualizado. Integridad estructural OK (4 secciones, 259→266 líneas). |
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