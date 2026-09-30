# ANÁLISIS PROFUNDO — `Anil-matcha/open-dots`
## Competidor / posible fuente de piezas para NEREUS

**Fecha:** 2026-09-30 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) — misión en solitario · **Encargado por:** Monarca (Key)
**Método:** skill `github-repo-recon` (modo profundo) · datos vía GitHub API autenticada + árbol de código + lectura de fuente, 2026-09-30.

---

## 1. RESUMEN EJECUTIVO

`open-dots` es un **workspace de agente personal open-source (MIT)**, Python (FastAPI) + Next.js, que se presenta como alternativa a OpenAI Dots, Meta Muse, Grok Bot, Instinct, Manus Cue, Claude Cowork y ChatGPT agent. Tiene piezas de diseño **buenas y robables**, pero **NO es mejor base que OpenMuse para NEREUS** y sus credenciales de tracción están **infladas**.

### Hallazgos críticos (aunque incomoden)
1. ⚠️ **Las 4.856★ y 550 forks NO son de este proyecto.** El repo se creó en 2023, pero su contenido fue **reemplazado por completo el 2026-09-29 17:35 UTC** (commit `cb21263` "Swap project contents with Generative Media Skills repository"). Antes de eso albergaba un proyecto **no relacionado** (skills de generación de media del servicio **MuAPI**). Es decir: **open-dots tiene ~1 día de vida real como código** y heredó la popularidad de otro proyecto. El criterio Seawolf "≥1000★ = tracción real" **NO se cumple aquí de forma legítima.**
2. ⚠️ **Es un embudo SEO/marketing**, no un producto de ingeniería pura: 104 commits con decenas de "Add cross-links to related projects", UTM tracking a `muapi.ai`, badge "MuAPI powered-by", una web con páginas `/alternatives/<competidor>` para 8 rivales y un `Marketplace.jsx`. El `README` empuja a `muapi.ai`.
3. ⚠️ **Su adaptador de modelo por defecto es una trampa de lock-in**: envía un cuerpo **no estándar** (`{"prompt","image_url","system_prompt",...}`) con cabecera `x-api-key` a `{base_url}/{model_id}` — contrato propio (estilo MuAPI), **no OpenAI ni OpenRouter**. El propio README admite: *"no es un adaptador plug-and-play para todo endpoint compatible con OpenAI"*.
4. ⚠️ **NO cierra ninguno de los contras de NEREUS**: sin memoria durable, sin voz, sin OCR, sin multi-tenant, sin app móvil, sin motor de rutinas. SQLite local mono-owner.

### Lo que SÍ vale la pena
- ✅ **`action_gateway.py`**: registro de acciones **deny-by-default** con niveles de riesgo (read/write/external), aprobación obligatoria y **redacción automática de credenciales** en la auditoría. Referencia limpia para nuestro diferenciador de **Audit Trail**.
- ✅ **Búsqueda web sin clave** vía `/search` (perfil gratuito de You.com, MCP) — coste cero.
- ✅ **Secretos cifrados en reposo** (Fernet) + sesiones con cookies HttpOnly revocables.

**Veredicto:** mantener **OpenMuse como base de NEREUS**. Saquear de `open-dots` la idea del **action gateway + redacción de auditoría** y el **search keyless**. No migrar de stack.

---

## 2. METODOLOGÍA

- Metadata y licencia: `GET /repos/Anil-matcha/open-dots` (autenticado) · LICENSE en crudo.
- Estructura: `git/trees/main?recursive=1` (84 blobs).
- Historia/velocidad: `/commits` (últimos 40), `/contributors`, diff del commit de "swap".
- Código: lectura directa en crudo de `provider_service.py`, `action_gateway.py`, `storage_service.py`, `requirements.txt`, `client/package.json`, `client/app/page.js`, `client/app/alternatives/...`.
- Búsqueda de conceptos (memory/voice/pgvector/tenant/ocr/schedul/push…) sobre todo el código.

---

## 3. FICHA DEL REPO

| Campo | Valor |
|-------|-------|
| Repo | `Anil-matcha/open-dots` |
| Licencia | **MIT** (verificada en crudo; `Copyright (c) 2026 Anil-matcha`) |
| Stars / Forks | **4.856 / 550** ⚠️ *(heredados del proyecto anterior — ver §1.1)* |
| Lenguaje | **Python 69.8%** · JavaScript 29.7% |
| Stack | **FastAPI** (API) + **Next.js 15 / React 19** (cliente) + Docker/Playwright opcional |
| Estado declarado | **"Prototype / active development"** — sin releases publicadas |
| Creado | 2023-05-25 (repo) · **contenido actual desde 2026-09-29** (~1 día) |
| Último push | 2026-09-30 (activo) |
| Issues abiertos | 1 |
| Contribuidores | **5** (Anil-matcha 95 commits; resto marginal: masskx 6, 3 anónimos) |
| Tamaño del código | ~**8.100 LOC Python** + ~**4.100 LOC JS/JSX** (84 archivos) |
| Tests | 15 archivos de test (pytest) — sin cifra pública de cobertura |
| Homepage | *(vacía)* |

---

## 4. QUÉ PUEDE Y QUÉ NO (según código y README)

### ✅ Puede
- Chat con streaming (SSE), Markdown, adjuntar imágenes.
- **Personas/asesores** ("bots") con instrucciones, modelo y avatar separados.
- **Action gateway gobernado**: acciones deny-by-default, aprobaciones para acciones de riesgo, **eventos de auditoría**.
- **Conectores vía Composio** (OAuth; acciones estrechas: p. ej. lookup/creación de issues de GitHub).
- **Búsqueda web `/search`** (You.com, sin clave).
- **Runtime de computadora opcional** (Docker/Playwright o remoto), rootfilesystem de solo lectura, capabilities dropped.
- **Estado en SQLite** + **credenciales cifradas en reposo** (Fernet).
- Autenticación de owner con cookies de sesión revocables.

### ❌ NO puede (limitaciones admitidas + verificadas en código)
- **Mono-owner local**: sin usuarios, roles ni multi-tenant (`tenant`: 0 archivos; `LOCAL_USER_ID` fijo).
- **SQLite local**: sin almacenamiento multi-instancia ni backup; sin Postgres.
- **Sin memoria durable / semántica**: `embedding`: 0 · `pgvector`: 0. Solo guarda historial de conversación local.
- **Sin voz** (solo dictado del navegador) · **sin OCR** · **sin push**.
- **Sin app móvil ni de escritorio** (solo web).
- **Sin motor de rutinas/tareas programadas**.
- **Inferencia**: solo API "prediction" propia + **Responses API**; **Chat Completions NO implementado** (lo que corta OpenRouter y muchos proveedores por la vía estándar).
- Runtime de computadora **no es sandbox endurecido** para web hostil.

---

## 5. `open-dots` vs `OpenMuse` (base de NEREUS)

| Dimensión | OpenMuse (NEREUS) | Open Dots |
|-----------|-------------------|-----------|
| Lenguaje | **TypeScript** (Expo + Hono, monorepo) | **Python** (FastAPI) + Next.js |
| Licencia | MIT | MIT |
| Tracción | 3.4k★ / 445 forks (orgánica) | 4.8k★ / 550 forks **(heredada, no orgánica)** |
| Edad del código | ~2 semanas (2026-09-15) | **~1 día (2026-09-29)** |
| Tests | **276 (todos verdes)** | 15 archivos pytest (sin cifra) |
| Persistencia | PGlite / **PostgreSQL** | **SQLite** solo |
| Gateway de modelo | CopilotKit Intelligence *(cerrado)* + proveedor | configurable; default = **contrato propio MuAPI** |
| Compat. OpenRouter | vía proveedor OpenAI | **Responses ✅ / default ❌** |
| Aprobaciones + auditoría | ✅ revisiones + recibos | ✅ gateway + **redacción de credenciales** |
| Navegador + computadora | ✅ Playwright + Linux Docker | ✅ opcional (no endurecido) |
| Conectores | Gmail/Calendar OAuth | **Composio** (estrecho) |
| Memoria | memorias editables | **NINGUNA durable** |
| Voz | ✗ | ✗ |
| Móvil/Escritorio | ✅ **Expo (iOS/Android/Web)** | ✗ web solo |
| Multi-tenant | single-owner | single local owner |
| Búsqueda web | roadmap | ✅ **You.com keyless** |
| Madurez de ingeniería | CI + docs VERIFICATION | prototipo, marketing-first |

**Conclusión:** stacks distintos e incompatibles. Adoptar `open-dots` sería **empezar de cero en Python**, perdiendo los 276 tests, el móvil Expo y la base TS ya cimentada en el VPS. No tiene sentido estratégico.

---

## 6. QUÉ SAQUEAR (valor real para NEREUS)

| Pieza de `open-dots` | Valor | Uso propuesto en NEREUS |
|----------------------|-------|-------------------------|
| **Action gateway** (registro deny-by-default, riesgo read/write/external, handoff de aprobación) | Alto | Patrón de referencia para el **Audit Trail + RBAC** (diferenciadores Seawolf) |
| **Redacción automática de credenciales** en la auditoría (`redact_sensitive`) | Alto | Endurecer nuestros recibos/auditoría: nunca registrar tokens |
| **Búsqueda web keyless** (You.com MCP, `/search`) | Medio | Añadir búsqueda web sin coste a NEREUS |
| **Cifrado de secretos en reposo** (Fernet) + sesiones revocables | Medio | Endurecer manejo de credenciales de proveedor |

⚠️ **Anti-patrón a NO copiar:** el adaptador "prediction" con `x-api-key` y cuerpo propio = **lock-in de proveedor**. Confirma que nuestra decisión de **OpenRouter como gateway** (Fase 2) es la correcta.

---

## 7. RECOMENDACIÓN TÁCTICA

1. **NO adoptar `open-dots` como base.** Mantener **OpenMuse → NEREUS** (TypeScript, 276 tests, móvil Expo ya desplegado en el VPS).
2. **Incorporar a NEREUS** el patrón de **action gateway con redacción de auditoría** y el **search keyless** — encaja con nuestros diferenciadores (Audit Trail, español, filtro CSO).
3. **Vigilar** el repo como competidor de nicho (mismo espacio "alt a OpenAI Dots/Meta Muse"), pero tratar sus métricas de estrellas y su copy con **escepticismo**: es una vitrina SEO para MuAPI, no tracción de producto.

> **Honestidad brutal:** si hubiéramos filtrado por "MIT + ≥1000★" sin leer la historia, habríamos dado por bueno un repo de 4.8k estrellas que en realidad tiene 1 día de vida y cuyo principal activo es un embudo de marketing. Lección para el protocolo: **las estrellas se heredan al reciclar un repositorio — verificar el diff de "swap" y la fecha del primer commit del contenido, no la fecha del repo.**

---

## 8. APÉNDICE — FUENTES Y CONSULTAS

- `GET https://api.github.com/repos/Anil-matcha/open-dots` (2026-09-30)
- `GET .../git/trees/main?recursive=1` · `.../commits?per_page=40` · `.../contributors`
- Diff commit `cb21263d` (swap) — 177 archivos; eliminado contenido `muapi-*` (`core/`, `.opencode/skills/`).
- Crudo: `LICENSE`, `server/requirements.txt`, `client/package.json`, `server/app/services/provider_service.py`, `server/app/services/action_gateway.py`, `server/app/services/storage_service.py`, `client/app/page.js`, `client/app/alternatives/[competitor]/page.js`.
- OpenRouter Responses API (compatibilidad confirmada): `https://openrouter.ai/docs/api_reference/responses/overview`.

**Fin del informe.** Listo para auditoría de Beru.
