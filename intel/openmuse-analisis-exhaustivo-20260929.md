# INFORME DE INTELIGENCIA: OpenMuse — Análisis Exhaustivo del Original y Todos sus Derivados

**Fecha:** 2026-09-29 · **Sesión:** Investigación · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Encargado por:** Monarca (Key) · **Ejecutado por:** Bellion (Gran Comandante)
**Método:** GitHub Search API + Repos API + Forks API + lectura directa de README/CHANGELOG/LICENSE en crudo
**Alcance:** 129 repos hallados bajo "openmuse"; se analizan todos los relevantes con ficha técnica y comparación de capacidades frente al original.

---

## 0. ALERTA DE CONTEXTO CRÍTICO — LEER PRIMERO

### 0.1 Qué es "Muse" (el producto que originó todo)

**Meta lanzó "Muse" el 8 de septiembre de 2026** — su primer agente personal de IA. No es un chatbot: *actúa*. Corre sobre una **"Muse Secure VM"** (computadora cloud dedicada con su propio navegador visible), se conecta a Gmail, Google Calendar, OpenTable, Facebook, Instagram, Peloton y Plaid, y hace tareas largas en segundo plano (enviar correos, comprar, reservar viajes, rellenar formularios, negociar). Lanzado por Alexandr Wang (Chief AI Officer de Meta). Ecosistema asociado: modelo **Muse Spark 1.3** y la herramienta de código de terminal **Muse Code**. Cerrado y propietario.

### 0.2 Qué es "OpenMuse" (el original open source)

**CopilotKit lanzó `CopilotKit/openmuse` el 15 de septiembre de 2026** (una semana después de Muse) como el **clon open source de Meta Muse**, bajo licencia **MIT**, construido con CopilotKit + AG-UI. Autor: Atai Barkai + CopilotKit.

👉 **ESTE es "el original"** al que se refiere el Monarca: es el de mayor tracción (3.436★), el que todo el ecosistema cita, y del que derivan los forks.

### 0.3 HALLAZGO CRÍTICO: existen DOS linajes distintos llamados "OpenMuse"

No hay un solo "OpenMuse". Hay **dos proyectos independientes** que clonan a Meta Muse y comparten el nombre:

| Linaje | Repo raíz | Origen | Lenguaje | Licencia | Relación |
|--------|-----------|--------|----------|----------|----------|
| **LINAJE A — CopilotKit** (EL ORIGINAL) | `CopilotKit/openmuse` | 2026-09-15 | TypeScript | **MIT** | Forkeado por ~445 repos |
| **LINAJE B — Python/Android** | `OpenMuseAgent/OpenMuse` → `nano-muse/nanoMuse` | 2026-09-22 | Python → Swift | MIT → **GPL-3.0** | Reimplementación independiente |

**No son forks entre sí.** Son dos implementaciones paralelas del mismo concepto. Esto es decisivo: cualquier análisis que los mezcle es incorrecto. Este informe los trata por separado.

---

## 1. EL ORIGINAL — Ficha Completa

### `CopilotKit/openmuse`

| Dato | Valor |
|------|-------|
| Estrellas | **3.436★** |
| Forks | 445 |
| Licencia | **MIT** (pura) |
| Lenguaje | TypeScript (monorepo pnpm) |
| Versión | **0.1.0-alpha** (2026-09-15) — única release |
| Creado | 2026-09-15 · Último push: 2026-09-29 |
| Issues abiertos | 50 |
| Web | copilotkit.ai/openmuse |
| Requisitos | Node 24 LTS, pnpm 11.19.0, clave de proyecto CopilotKit Intelligence, clave de modelo (OpenAI/Anthropic/Google) |

**Descripción oficial:** *"Un agente personal con navegador, terminal, archivos y trabajo que sigue avanzando. Compatible con cualquier agent harness."*

#### Arquitectura
```
Cliente (Expo / React Native / Web)
   │ AG-UI + API autenticada
   ▼
API (Hono + runtime CopilotKit)
   ├── Task worker durable
   ├── CopilotKit Intelligence (Threads ricos) [SERVICIO EXTERNO]
   ├── Almacén: PGlite o PostgreSQL
   ├── Worker de navegador (Chromium/Playwright, perfiles persistentes)
   └── Computadora Linux opcional (Docker, volumen /workspace)
```
Módulos: `apps/mobile` (iOS/Android/web), `apps/server` (API + task engine), `apps/worker` (Playwright), `apps/computer` (imagen Linux), `packages/domain`, `packages/integrations`, `packages/backends`.

#### ✅ LO QUE SÍ PUEDE HACER (verificado en repo)
1. **Chat nativo CopilotKit** (streaming de eventos AG-UI) en iOS, Android y web.
2. **Navegador del agente:** Chromium persistente, lectura de páginas públicas, snapshots, **consola de toma de control** ("Take control"), descarga de PDFs.
3. **Computadora Linux opcional** (contenedor Docker no-root): comandos acotados de bash/Python/Node/git, recibos de salida/exit guardados, `/workspace` persistente, edición de texto, import/export de PDF. **SIN red** (el acceso web va por el worker de navegador). Límite de 30s por comando.
4. **Tareas durables:** planes, progreso, solicitudes de input, pausa/reanudar/cancelar/reintentar, aprobaciones y recibos. Recuperación por leases SQL.
5. **Ideas:** sugerencias con evidencia-fuente; editar/aceptar/descartar.
6. **Goals & Tracking:** metas e hitos, chequeos recurrentes de páginas (cambios, texto, umbral de precio USD), alertas deduplicadas con backoff.
7. **Documentos:** adjunto de correo → PDF → valores de formulario → copia rellenada → respuesta revisada → recibo.
8. **Finanzas:** importar CSV de transacciones → resumen de gasto con categorías.
9. **Gmail y Calendar:** adaptadores OAuth de Google, hilos completos, borradores/adjuntos, CRUD de eventos con revisión. (Requiere credenciales live.)
10. **Contexto personal:** nombre, tono, avatar y memorias editables/olvidables.
11. **Rich Threads:** persistencia CopilotKit Intelligence (hilos, side chats, renombrar, archivar, replay). **Requiere clave de proyecto** (servicio externo, NO incluido en la licencia MIT).

#### ❌ LO QUE NO PUEDE HACER (roadmap / no implementado — declarado por el propio proyecto)
- Terminal **interactiva**, aplicaciones de escritorio, orquestación de VM por persona, acceso de red controlado, cuotas de disco en el workspace.
- **Reservas, compras, checkout o atención al cliente autónomos** (el checkout autónomo es "future work").
- **Google Drive/Docs**, conectores de **banca (Plaid), salud, Instagram, WhatsApp** o APIs de partners.
- **Notificaciones push de dispositivo** (APNs/FCM), **voz** (entrada/respuesta), **generación de imágenes**.
- **OCR / PDF escaneados** y tipos de formulario adicionales; edición de recurrencia de calendario.
- Planificación adaptativa de largo plazo y registro gestionado de herramientas generadas.
- **Multi-usuario** (es single-owner con clave de acceso compartida, NO multi-tenant).
- Integración **OpenBot en vivo** (adaptador existe pero deshabilitado).
- Requiere un servicio externo (CopilotKit Intelligence) → no es 100% autónomo con solo el repo.

---

## 2. MAPA COMPLETO — Clasificación de los 129 repos

| Grupo | Cantidad | Descripción |
|-------|----------|-------------|
| **A. El original** | 1 | CopilotKit/openmuse |
| **B. Derivados del original (Linaje A)** | ~14 relevantes | Forks/modificaciones del repo de CopilotKit |
| **C. Linaje B (nanoMuse)** | 2 | OpenMuseAgent/OpenMuse + nano-muse/nanoMuse |
| **D. Wrappers de despliegue** | 4 | Empaquetan el original para Render/Railway/Spine sin cambiar features |
| **E. Ecosistema "Muse" (no OpenMuse)** | ~5 | UIs para Muse Code, muselab, comparativas |
| **F. Colisiones de nombre (NO relacionadas)** | ~60 | EEG Muse headband, Musenet (música), Open Museum, OpenMusE (Open Music Europe) |
| **G. Forks vacíos** | ~40 | Rebrands sin cambios (0-2★) |

---

## 3. DERIVADOS DEL ORIGINAL (LINaje A) — Capacidades vs Original

### 3.0 Tabla Comparativa Maestra

| Repo | ★ | Lic. | Leng. | Puede MÁS que el original | ≠ Pierde / NO puede |
|------|---|------|-------|---------------------------|---------------------|
| **CopilotKit/openmuse** (ORIGINAL) | 3.436 | MIT | TS | — (baseline) | — |
| **xuboboo/zmuse** | 2 | MIT | TS | Escritorio Linux gráfico (Xfce+Firefox) en la app; app nativa Windows (tray, auto-sanado); UI 100% china; presets de proveedores chinos | Solo Windows (docs); sin iOS/Android; 2★ sin verificar |
| **joaovitor2763/corgi-publico** | 1 | NOASSERTION | TS | Composio (Gmail/Calendar/**Slack/Notion/Drive**…); **Apify**; voz; fotos; chats paralelos; **sub-agentes**; Radar; memoria con fuentes; guarda anti-phishing "Jev"; **Web Push**; pt-BR | Licencia NO declarada (riesgo legal); 1★ |
| **norhtecmbarnes-dot/Agent-Dashboard** | 1 | NOASSERTION | JS | **Modelo local (llama.cpp gpt-oss-120b)** sin nube; control por **Telegram**; app Android; libro de 384 págs; model-agnostic | Licencia NO declarada; calidad no verificada |
| **romangalaxys10-spec/openmuse-macos** | 0 | MIT | TS | App **nativa macOS (AppKit)**; gateway "Agnes AI"; modo offline | 0★; sin probar; 2026-09-28 |
| **jerelvelarde/openmuse** | 1 | MIT | TS | Fork directo; app React Native; base "Meta Muse/OpenBot" | Prácticamente idéntico; 1★ |
| **jerelvelarde/heycapybara** | 2 | (none) | TS | Companion macOS; **record-to-skill** (graba acciones→skills); AG-UI; Codex | No es el agente completo; sin licencia |
| **diggerhq/openmuse** | 44 | (none) | TS | Corre agentes en **OpenComputer Serverless Agents** (cloud a demanda); modelo de **"topic"** con notas editables; app TanStack Start | **NO es MIT** (sin licencia); requiere cuenta tercero OpenComputer + túnel HTTPS; sin app móvil nativa; sin terminal Linux local documentado |
| **SiliconLabAI/OpenMuse** | 7 | MIT | TS | UI estilo Muse + **servidor de webhook callback** async | **NO usa el runtime CopilotKit**; depende 100% de **Manus API v2** (externo, de pago); sin navegador/terminal propios |
| **AXT224/openmuse** | 0 | MIT | TS | Rebrand minimal del original | Sin valor añadido |
| **0sparsh2/OpenMuse** | 3 | (none) | Python | Reimplementación en **Python**; corre en **NVIDIA NIM** (Nemotron); voz; app de teléfono; Gmail+Calendar | Sin licencia; temprano |
| **openmuseai/openmuse** | 1 | **AGPL-3.0** | Dart/Flutter | Host de escritorio clean-room + **SDK de plugins** + broker de plataforma (Helix/DSH/Native View); enforcement de permisos | **AGPL-3.0 → NO es MIT**; es un host de escritorio, no el agente móvil/web |
| **tuxevil/openmuse** | 0 | (none) | Python | Runtime portable self-hostable, model-agnostic; control plane durable single-user | Pre-alpha; sin licencia; 0★ |
| **SubjectAlphaChisato/OpenMuse** | 1 | Apache-2.0 | Python | FastAPI+PostgreSQL, 6 servicios aislados, React, **269 tests**, 10 skills (Gmail/Calendar/Drive/Notion/GitHub) | **Apache, no MIT**; no es derivado (reimplementación) |
| **Devin-AXIS/OpenMuse** | 0 | Apache-2.0 | TS | Mobile-first; **DeepSeek Harness (DSH)**; **E2B microVM** por cloud run; auth por OTP telefónico | **Apache, no MIT**; depende de E2B (tercero) |
| **ibchouti9/openmuse** | 1 | MIT | TS | UI (PWA) que habla con el binario real **`muse` (Muse Code de Meta)** vía protocolo MSP | Requiere **Muse Code de Meta** instalado → no self-contained; solo UI |
| **onlinegill/beli** | 0 | (none) | — | Fork de OpenMuse llamado "Beli" | Sin cambios relevantes |

### 3.1 Fichas detalladas de los "más completos"

**(a) xuboboo/zmuse — el derivado con MÁS capacidades de UI/desktop**
Añade al original: **escritorio Linux gráfico real (Xfce + Firefox, entorno chino, con internet)** operado dentro de la app; **app nativa de Windows** (bandeja del sistema, auto-recuperación de subprocesos en 3s, cierre elegante sin corromper datos); UI y docs en chino; presets listos para **中转** chinos (AgentRouter, OpenRouter, self-host). Base idéntica (mismo stack CopilotKit, misma clave Intelligence). **No puede:** iOS/Android (documentado Windows 10/11), y su tracción es mínima (2★) → sin verificación independiente.

**(b) joaovitor2763/corgi-publico — el derivado con MÁS integraciones**
Añade: **Composio** (Gmail, Calendar, Slack, Notion, Drive y "muchos más"), cada uno con permiso propio (aprobar / solo leer / off); **Apify** con clave propia; **voz, fotos y archivos**; **conversaciones paralelas**; **"Ajudantes"** (mini-agentes con misión propia: Radar de Slack, Preparador de reuniones, Concorrentes) — capacidad de **sub-agentes que el original NO tiene**; **Radar** de alertas; **memoria con origen de cada hecho** + revisión horaria + reflexión nocturna; guarda de seguridad **"Jev"** contra phishing e inyección de instrucciones; **Web Push** para aprobaciones/preguntas/resultados. pt-BR nativo. **No puede:** licencia NO declarada (derivado, sin SPDX) → riesgo legal para uso comercial; 1★.

**(c) norhtecmbarnes-dot/Agent-Dashboard — el derivado 100% local**
Añade: **modelo local por defecto (llama.cpp con gpt-oss-120b)** — sin coste de nube, a diferencia del original que exige OpenAI/Anthropic/Google; **control desde Telegram**; app Android; model-agnostic (Ollama/LM Studio/vLLM/Anthropic/Google con una línea en `.env`); incluye libro gratuito "Building Your AI Dashboard" (384 páginas). **No puede:** licencia NO declarada; calidad no verificada independientemente.

**(d) diggerhq/openmuse — arquitectura distinta (cloud serverless)**
En lugar de correr local, apunta los agentes a **OpenComputer Serverless Agents**, que aprovisionan computadoras y guardan conversaciones/notas en tu proyecto OpenComputer. Introduce el modelo de **"topic"**: cada trabajo largo tiene su conversación propia, notas editables y computadora cloud; el trabajo sigue aunque cierres el navegador. **No puede:** **NO es MIT** (sin licencia declarada → incumple el criterio del Monarca); exige cuenta OpenComputer (tercero) y un túnel HTTPS; sin app móvil nativa ni adaptadores Gmail/Calendar documentados.

**(e) SiliconLabAI/OpenMuse — NO es el mismo motor**
Es una **UI estilo Muse** (Vite+React+TanStack) con un **servidor proxy a Manus API v2** y callback de webhooks async. **No puede:** no usa el runtime CopilotKit/AG-UI; sin navegador propio, sin terminal, sin Gmail/Calendar; todo depende de Manus (servicio externo de pago). Es una interfaz, no un agente completo.

**(f) openmuseai/openmuse — concepto distinto (host de escritorio)**
"Clean-room OpenMuse desktop Host, plugin SDK, platform broker y plugins first-party" — arquitectura Flutter + Helix + DSH + Native View, con envelopes RPC, negociación de versión, enforcement de capacidades/permisos y workbench de 3 paneles. **No puede:** **AGPL-3.0** (no MIT); no incluye producto web; es un host local con SDK, no el agente móvil/web.

---

## 4. LINAJE B — OpenMuse (Python/Android) → nanoMuse

⚠️ **Implementación INDEPENDIENTE, no derivada de CopilotKit.** También clona el concepto de Meta Muse.

### 4.1 `OpenMuseAgent/OpenMuse` (archivo 0.1.0–0.6.0) — 4★ · MIT · Python
Paquete Python (`pip install openmuse`), app web incluida y app Android. ~18.000 líneas de Python tipado + 11.000 TS + 800 Kotlin; ~240 tests. **Puede:** investigar, escribir páginas/documentos, correr shell y Python, enviar correo, leer calendario y contactos, navegar; **Sentinel** decide allow/ask/deny por llamada y en Linux cada comando corre en su propio sandbox **bubblewrap**; aprobaciones con alcance (una vez / esta tarea / siempre) revocables; metas de semanas con la app cerrada; check-ins programados; arranque por llegada de correo/evento/webhook; feed de posts; memoria semántica editable/olvidable; formato **Agent Skills**; cualquier servidor **MCP**; **cualquier modelo OpenAI-compatible** (DeepSeek, OpenAI, OpenRouter, Ollama, vLLM). **No puede:** es un linaje aparte (no comparte la UI nativa CopilotKit ni los Rich Threads); repositorio archivado.

### 4.2 `nano-muse/nanoMuse` — 25★ · **GPL-3.0** · Swift (sucesor)
El proyecto **más completo de todo el ecosistema OpenMuse** en alcance de dispositivo. La app **Android corre el agente COMPLETO en el teléfono**: sistema de archivos Linux root, shell, navegador, MCP, skills y tareas programadas **dentro del APK**, con modelo propio. Tiene **"manos" para apps que nunca tuvieron API** — opera la **pantalla del propio teléfono** con tu permiso (微信/微信, Alipay, 12306…) — y alcanza tu computadora (lo dices al teléfono, se hace allí). App de escritorio y versión web incluidas; iOS y gafas "próximamente". Modelo gratis con asignación inicial vía relay abierto, o trae tu propia clave; estudio de avatar. Versión 0.1.24. **No puede:** iOS y gafas aún no; **GPL-3.0 → NO es MIT** (incumple el criterio innegociable del Monarca si busca MIT).

---

## 5. WRAPPERS DE DESPLIEGUE (no añaden features, facilitan el deploy)

| Repo | ★ | Lic. | Qué hace |
|------|---|------|----------|
| **render-examples/openmuse** | 0 | MIT | Blueprint de Render; construye desde `CopilotKit/openmuse` `main` sin cambios |
| **will-bogusz/railway-openmuse** | 0 | MIT | Imágenes de contenedor (API+web, browser worker) desde commit fijado; plantilla Railway |
| **lNamelessl/openmuse-railway-template** | 0 | NOASSERTION | Plantilla Railway 1-clic, commit fijado + parche same-origin |
| **savvautops/openmuse-spine** | 0 | (none) | Despliegue en "Spine" + exposición por Tailscale (iPhone Safari) |

Ninguno modifica capacidades; solo empaquetan el original. Útiles para acelerar puesta en marcha, pero **no son "más completos"** funcionalmente.

---

## 6. ECOSISTEMA "MUSE" (relacionado conceptualmente, NO es OpenMuse)

| Repo | ★ | Qué es |
|------|---|--------|
| **ibchouti9/openmuse** | 1 | UI web/PWA para **Muse Code** (el `muse` binario real de Meta) sobre protocolo MSP |
| **Auth-Xero/OpenMuselab** | 0 | Versión self-hostable de **muselab.app** |
| **inematds/openmuse-vs-muse** | 0 | Documento comparativo Meta Muse × OpenMuse (PT/EN/ES), con validación de afirmaciones |
| **kapelame/openmuse-studio** | 0 | Workspace de **música** con IA (título homónimo, tema distinto) |

---

## 7. COLISIONES DE NOMBRE (NO relacionadas — descartadas)

Estos repos comparten "OpenMuse/OpenMuseum" pero **no tienen nada que ver** con el agente:
- **DominiqueMakowski/OpenMuse** (93★) — graba/stream señales del headband **Muse S Athena** (EEG).
- **hidude562/OpenMusenet2** (69★) y **json2007or8/OpenMusenet3** — implementaciones de **MusicNet** (música).
- **PN-promo6/openmuseum-*** (decenas) — proyectos de clase ("Open Museum", Angular).
- **dataobservatory-eu/openmuse.*** y **openmusiceurope/*** — **OpenMusE = Open Music Europe** (proyecto de investigación musical).
- **GetIT-Sunday/Openmuse** — "Smeargle", convierte papers a artículos (música/papers).
- **unirsm/openMuseum**, **Gravity-Turtles/OpenMuseum**, **ZaQChojecki/OpenMuseum** — museos/galerías.

---

## 8. ANÁLISIS ESTRATÉGICO Y RECOMENDACIÓN

### 8.1 Hallazgos duros
1. **El original (CopilotKit/openmuse) es, con enorme diferencia, el más completo y maduro de su linaje.** Ningún fork lo supera en capacidades nucleares de agente; los forks añaden capas horizontales (escritorio, conectores, modelo local, deploy).
2. **Solo el original cumple "MIT + ≥1000★".** TODOS los derivados están por debajo de 45★. Si el criterio MIT+1000★ es innegociable, **solo el original califica**.
3. **El original NO es 100% autónomo:** exige una clave de **CopilotKit Intelligence** (servicio externo, fuera de la licencia MIT) para los Rich Threads, y una clave de modelo de pago.
4. **Alternativas con más alcance de dispositivo existen pero rompen MIT:** `nanoMuse` (GPL-3.0, agente completo en el teléfono) y `openmuseai/openmuse` (AGPL-3.0, host de escritorio).
5. **Varios derivados "interesantes" NO tienen licencia declarada** (`diggerhq`, `corgi-publico`, `Agent-Dashboard`, `0sparsh2`) → **riesgo legal** para uso comercial.
6. El proyecto es **alpha desde hace ~2 semanas** (0.1.0). Todos: original y derivados, son **muy jóvenes**. Riesgo de bugs alto.

### 8.2 Recomendación táctica (para Seawolf Studio)
- **Si el objetivo es un agente personal propio sobre base MIT:** partir del **original CopilotKit/openmuse** — es el único MIT + maduro + con tracción, y es la base que el ecosistema mantiene.
- **Si se necesita escritorio gráfico/Windows y mercado hispano/chino:** el original no lo da → estudiar fork `zmuse` (MIT) como referencia de código, no como base (2★, sin verificar).
- **Si se quiere 100% local sin nube:** el original exige proveedor de modelo; `Agent-Dashboard` muestra cómo enchufar llama.cpp, pero sin licencia → replicar la idea sobre el original.
- **EVITAR como base:** `diggerhq` (no MIT + tercero), `SiliconLabAI` (depende de Manus), `openmuseai` (AGPL), `nanoMuse` (GPL) — salvo que se acepte su licencia.
- **Advertencia legal inquebrantable:** AGPL/GPL obligan a liberar código si se ofrece como servicio. Mantener el criterio MIT del Monarca protege el SaaS cerrado.

### 8.3 Riesgos
| Riesgo | Detalle |
|--------|---------|
| Madurez | Alpha de 2 semanas; sin releases estables; 50 issues abiertos en el original |
| Dependencia externa | Rich Threads requiere CopilotKit Intelligence (fuera de MIT) |
| Legal | Varios derivados sin licencia; AGPL/GPL en otros |
| Calidad de forks | Derivados con 0-2★ sin verificación; muchos son rebrands vacíos (0★) |
| Obsolescencia | Meta Muse evoluciona; los clones quedan atrás rápido |

---

## 9. APÉNDICE — Metodología y Fuentes

**Consultas ejecutadas (GitHub API):**
- `search/repositories?q=openmuse|open-muse|open_muse|muse` → 129 repos
- `repos/{owner}/{repo}` individual para 24 repos (licencia, estrellas, fechas, topics)
- `repos/CopilotKit/openmuse/forks?sort=stargazers` → 100 forks top
- `git/trees/main?recursive=1` del original (216 archivos)
- Lectura en crudo de README, CHANGELOG, LICENSE, FEATURES.md, ROADMAP.md, VERIFICATION.md, package.json
- Verificación de licencia real vía `raw.githubusercontent.com/.../LICENSE` (detecta open-core y NOASSERTION)

**Fuentes externas (contexto Muse):** CNBC, NYT, Reuters, Eigent, eesel.ai, coursiv.io, CopilotKit.ai/openmuse, X/@ataiiam, AGTP Insights.

**Comandos de reproducción:**
```bash
# Ver el original
git clone https://github.com/CopilotKit/openmuse.git
cd openmuse && pnpm install --frozen-lockfile && cp .env.example .env
npx copilotkit@latest login && npx copilotkit@latest project select
pnpm dev && pnpm dev:web
```

**Fin del informe.** Listo para auditoría de Beru y archivo en `diario-de-sombras/`. Documento PDF adjunto generado en paralelo.
