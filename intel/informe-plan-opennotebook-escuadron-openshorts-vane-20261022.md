# 🏗️ PLAN DE IMPLEMENTACIÓN — OpenNotebook · Escuadrón Alterno (OpenDots) · OpenShorts · Vane
**Arquitecto:** Bellion (Gran Comandante) · **Para:** Monarca · **Fecha:** 2026-10-22
**Núcleo común:** **FreeLLMAPI** (API que ya tiene el Monarca) → todo cuelga de ahí.
**Verificado en vivo:** licencias, requisitos, puertos y estado real del VPS `76.13.109.237`.

---

## 0. VEREDICTO RÁPIDO

| Pieza | ¿Entra? | Dónde | Por qué |
|---|---|---|---|
| **OpenNotebook** | ✅ SÍ | VPS | MIT, Docker, 4 GB RAM, usa FreeLLMAPI como proveedor |
| **Vane** | ✅ SÍ | VPS | MIT, Docker, ligero |
| **OpenShorts** | ⚠️ SÍ, pero **NO en el VPS** | **PC** | Pide **8 GB+ RAM** y CPU 5-8 min/video; el VPS tiene 2 vCPU / 6 GB libres |
| **OpenDots** (escuadrón alterno) | ❌ **NO como base** | — | Su cerebro (**CopilotKit Intelligence**) **no es abierto**: hosted o licencia. El camino gratis es una **evaluación de 30 días**, en macOS, pidiendo **4 CPU / 12 GiB / 40 GB** — *"not a production installation"*. **Alpha.** |

**Lo que sí rescatamos de OpenDots:** sus **ideas** y una pieza concreta — **OpenBot** (MIT) — para darle a cada sombra **su propio computador**. El escuadrón alterno se construye sobre **lo que ya es nuestro** (Hermes + Composio + MCP + FreeLLMAPI).

---

## 1. NÚCLEO: FreeLLMAPI (la pieza que lo une todo)
- **Qué es:** 34 proveedores gratis (635 endpoints) tras **un solo endpoint OpenAI-compatible `/v1`**, con router y failover.
- **Rol en el plan:** es el **motor de IA** de OpenNotebook, Vane y (si se quiere) las sombras de fondo.
- **Lo que hay que tener a mano del Monarca:** `base_url` + `api_key` de FreeLLMAPI.
- ⚠️ **Requiere modelos de 2 tipos:** **chat** (para responder) y **embeddings** (para buscar). FreeLLMAPI cubre ambos.
- ⚠️ **Honestidad:** son cupos de terceros → ideal para trabajo de fondo; **no** para el modelo de Bellion.

---

## 2. OpenNotebook — IMPLEMENTACIÓN PASO A PASO

**Qué ganamos:** cuaderno tipo NotebookLM **privado y nuestro**, con las fuentes del Studio (`intel/`, informes, catálogos) y consulta por chat + **podcast**.

### Requisitos verificados
- Docker + Compose v2 ✅ (el VPS tiene Docker 29.6.0 / Compose v5.2.0)
- **RAM: 4 GB mínimo** (8 recomendado *solo si* se usan modelos locales → nosotros usamos FreeLLMAPI, así que **no hace falta**)
- Disco: imágenes + documentos (tenemos 55 GB libres)

### Pasos
1. **Crear la carpeta** en el VPS: `/opt/opennotebook` y bajar el `docker-compose.yml` oficial (`lfnovo/open-notebook`).
2. **`.env`** con:
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY` = cadena secreta propia (**obligatoria**: cifra las claves en la BD).
   - `SURREAL_USER` / `SURREAL_PASSWORD` = propios (por defecto vienen `root:root` → **hay que cambiarlos**).
   - Guardar en `chmod 600`, **sin imprimir valores** (regla del Studio).
3. **⚠️ CORREGIR PUERTOS (crítico):** el compose trae SurrealDB en `127.0.0.1:8000` → **ese puerto YA está ocupado** (Portainer). Remapear:
   - SurrealDB → `127.0.0.1:8010:8000` (solo local)
   - Web UI → **8502** (libre ✅)
   - REST API → **5055** (libre ✅)
4. **Levantar:** `docker compose up -d` y verificar con `curl` a `127.0.0.1:5055` (no solo ver el contenedor arriba).
5. **Conectar el proveedor en la UI** (se configura en la interfaz, no en archivos):
   - Chat → **OpenAI-compatible** → `base_url` = FreeLLMAPI, `api_key` = la del Monarca.
   - Embeddings → igual (FreeLLMAPI).
6. **Cargar conocimiento:** los informes del repo `seawolf-agent/intel/` como fuentes.
7. **Exponerlo:** por el **Cloudflare Tunnel que YA corre** en el VPS (como NEREUS) → acceso desde cualquier dispositivo, sin abrir puertos.
8. **Respaldo:** los datos viven en volúmenes Docker → incluir en el respaldo del VPS.

**Tiempo estimado:** 30-45 min. **Riesgo:** bajo. **Aislado:** sí (si falla, se borra la carpeta y listo).

---

## 3. ESCUADRÓN ALTERNO — EXAMEN DE OPENDOTS (y lo que haremos en su lugar)

### Qué es OpenDots (real)
- **MIT · 5.918 ⭐ · Alpha.** "Always-on AI coworkers that move between text, calls, and Slack. Persistent AI agents, **each with its own computer**."
- **Conceptos:** **Dots** = agentes con nombre, rol, instrucciones y **herramientas permitidas** · **Spaces** = carpetas de trabajo · **Dot computer** = cada agente con su navegador, archivos y terminal propios · **Review before saving** = tarjeta de aprobación humana · **Connections** = **MCP servers** y **Composio**.

### El problema (lo que hay que decir sin adornos)
1. **El cerebro no es libre.** Las conversaciones **exigen CopilotKit Intelligence**: nube (tus datos allá), **licencia de pago**, o una **evaluación local de 30 días** (Docker Desktop **en macOS**, **4 CPU / 12 GiB / 40 GB**, plan Developer gratis) — y el propio README dice: **"This is not a production installation."**
2. **No cabe en nuestro VPS** (2 vCPU / 8 GB contra los 4 CPU / 12 GiB que pide hasta la evaluación).
3. **Alpha**, y "un template, no un producto".
4. Nada de esto es culpa del código (que es MIT y bonito): es que el **motor de conversación está fuera del código abierto**.

### La decisión: **copiar la arquitectura, no la dependencia**
Nuestro **escuadrón alterno** se construye sobre lo que **ya funciona y es nuestro**:

| Concepto de OpenDots | Nuestra pieza equivalente (ya existe) |
|---|---|
| **Dot** (agente con rol e instrucciones) | **Sombra** = perfil Hermes (`hermes -p <sombra> chat -q`) |
| **Tools permitidas por Dot** | **Skills + MCP por sombra** (ya asignamos 51 skills a las sombras) |
| **Connections (MCP + Composio)** | **Composio ya conectado** (Gmail/Sheets/Calendar) + nuestros MCP |
| **Dot computer** | **OpenBot** (MIT) o sandbox propio por sombra |
| **Review before saving** | **Compuerta de aprobación C2** del `seawolf-responder` |
| **Space** | El repo/carpeta del proyecto (`seawolf-agent`, `intel/`) |

**Único componente de CopilotKit que SÍ vale la pena estudiar:** **OpenBot** (6.983 ⭐, **MIT**, alpha) — "cada compañero con su computador: navegador real con sus logins, sus archivos, y solo las herramientas que le autorices; cada acción decidida antes y registrada después". **Eso sí es implementable en nuestra infra.**

**Por qué así:** la marca se construye sobre código propio; el escuadrón no puede depender de una licencia de tercero para *pensar*.

---

## 4. OpenShorts — INCORPORACIÓN (el Círculo Publicitario)
- **MIT · 7.015 ⭐ · Docker Compose** (3 servicios: backend, frontend, **renderer/Rémotion**).
- **Requisito duro: 8 GB+ RAM** + descarga de modelos + **CPU 5-8 min por video de 8 min**.
- **Dónde va: en el PC del Monarca** (el VPS no lo aguanta). Trabajo por lotes; no necesita 24/7.
- **Puertos a remapear si algún día va a un servidor:** backend `8000` (**ocupado por Portainer**) → `8040`; frontend `5175` → `5185`; renderer `3100` → `3110`.
- **Claves:** el **Clip Generator funciona con Whisper local** (transcripción en el propio equipo) — **sin APIs de pago**. Solo la función "AI Shorts (actores IA)" pide fal.ai/ElevenLabs.
- **🎁 LA JOYA:** expone un endpoint **`/mcp`** → **nuestras sombras pueden manejarlo como una herramienta MCP**. Es decir: el Círculo Publicitario se pilota desde el ejército.
- **Plan:** clonar → `docker compose up` → probar con un video largo real → medir tiempos en el PC → recién entonces evaluar si merece un VPS con GPU.

---

## 5. Vane — INCORPORACIÓN (motor de investigación)
- **MIT · 37.666 ⭐ · imagen Docker oficial** (`itzcrazykns1337/vane`).
- **Qué hace:** buscador con **respuestas citadas**, modos **Speed / Balanced / Quality**, fuentes **web / foros / académicas**, y **widgets**. Todo en hardware propio.
- **Dónde va: en el VPS** (ligero).
- **Puerto:** asignar uno libre (p. ej. **3040** — verificado libre) y exponer por el **Cloudflare Tunnel**.
- **Conectar a FreeLLMAPI** → investigación del `intel/` **a costo cero**.
- **Uso:** es la herramienta que reemplaza a Perplexity Pro para las investigaciones como la de este mismo informe.

---

## 6. MAPA DE RECURSOS (VPS real, medido hoy)

**VPS `76.13.109.237`:** 2 vCPU · 7,8 GB RAM (**6,0 libres**) · 96 GB disco (**55 libres**) · **load 0,07** (ocioso) · Docker ✅

**Ya corre ahí (no tocar):** WAHA · NEREUS (api/voice/web, postgres) · Seawolf Agent (filtro, responder, webui) · mem0 + Graphiti + Neo4j · Portainer · Cloudflare Tunnel.

| Servicio nuevo | RAM | Puerto | Destino |
|---|---|---|---|
| OpenNotebook | ~1,5 GB | 8502 / 5055 / 8010 | ✅ VPS |
| Vane | ~1 GB | 3040 | ✅ VPS |
| **Suma** | **~2,5 GB** de 6 libres | ✅ | ✅ cabe con margen |
| OpenShorts | **8 GB+** | 8040/5185/3110 | ⚠️ **PC** (no VPS) |
| OpenDots | 12 GB+ | — | ❌ descartado |

**Puertos YA ocupados (para no chocar):** 22, 53, 80, 443, 3000, 3011, 5433, 5440, 7474, 7687, **8000**, 8081, 8100, 8432, 8787-8799, 8888, 9443.

---

## 7. RIESGOS Y TRAMPAS (verificados)
1. **Puerto 8000 ocupado** por Portainer → OpenShorts y SurrealDB **deben remapearse** o no arrancan.
2. **OpenNotebook exige `OPEN_NOTEBOOK_ENCRYPTION_KEY`** y trae `root:root` por defecto en la BD → cambiarlo **antes** de exponer.
3. **Falta el modelo de embeddings** al conectar el proveedor → sin él la búsqueda no funciona aunque el chat sí.
4. **OpenShorts pide 8 GB** — lanzarlo en el VPS lo tiraría junto con WAHA/NEREUS. **Va al PC.**
5. **OpenDots: el gratis es una evaluación de 30 días** y no es producción → no montar nada encima.
6. **FreeLLMAPI = cupos de terceros** → respaldo y no usarlo para lo crítico.
7. **Regla de secretos:** claves en `.env` con `chmod 600`, **nunca impresas** ni en git.

---

## 8. PLAN DE EJECUCIÓN PROPUESTO (numerado)

1. **OpenNotebook en el VPS** — compose corregido (puertos 8502/5055/8010) + `.env` cifrado → arriba y verificado por `curl`.
2. **Conectar OpenNotebook a FreeLLMAPI** (chat **y** embeddings) y cargar `intel/` como fuentes.
3. **Vane en el VPS** (puerto 3040) + FreeLLMAPI → investigación a costo cero.
4. **Exponer ambos por el Cloudflare Tunnel** ya existente (acceso remoto, sin abrir puertos).
5. **OpenShorts en el PC** — probar el Clip Generator con un video largo real y medir tiempos.
6. **Conectar OpenShorts por MCP al ejército** → el Círculo Publicitario pilotado por las sombras.
7. **Escuadrón alterno (versión propia):** evaluar **OpenBot** como "computador por sombra" sobre nuestra infra — **sin** CopilotKit Intelligence.
8. **Registrar todo** en la línea de montaje (`seawolf-linea-de-montaje`) y en el Centro de Mando.

**Cada paso se entrega verificado** (no "parece que quedó": se prueba y se muestra la salida). 🐺
