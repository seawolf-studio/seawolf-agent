# DIARIO DE SESIÓN — "Búsqueda e Investigación"
## Compactación completa para retomar en sesión nueva

**Sesión:** `20260928_211526_47e1f3` · **Título:** "Busqueda e investigacion"
**Rango:** 2026-09-28 → 2026-10-14 · **Modelo:** deepseek/deepseek-v4.1-flash
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Clasificación:** Uso Interno — Seawolf Studio

---

## 0. CÓMO RETOMAR (leer primero)

Sesión nueva → ordenar: **"lee el diario de la última sesión"** → Bellion lee este archivo y retoma.

**Estado:** investigación y planificación completas. **Sin código escrito aún** para NEREUS (falta autorización de Fase 0).

**Nota de modo:** la skill `caveman` estuvo activa en esta sesión. **No persiste a la sesión nueva** salvo reactivarla (`/caveman` o "modo caveman").

---

## 1. MISIONES DE ESTA SESIÓN (en orden)

1. **Búsqueda e investigación exhaustiva de OpenMuse** (repo original + derivados; qué puede y no puede cada uno vs original). MD + PDF.
2. **Construir NUESTRA versión ("NEREUS")** desde la base de OpenMuse: quitar contras, afianzar pros, y verificar la vía open-source para replicar el resto (memoria, voz, personalización, continuidad). Planes v1 → v2 → v3.
3. **Análisis del repo de generación de video "Agnes"** + alternativas bajo los estándares del Monarca.
4. **Informe de tema:** réplica open-source de los modos de Agnes (Creative / Manuscript / Digital Anchor).
5. **Informe de tema:** repos y estrategias para ahorrar tokens. Activación de `caveman` + medición real.

---

## 2. HALLAZGOS — OPENMUSE (misión 1)

- **Contexto:** Meta lanzó **Muse** el 8-sep-2026 (agente personal, cerrado). **CopilotKit/openmuse** (15-sep-2026, **MIT**, TypeScript, ~3.4k★) es EL clon open source original.
- **DOS linajes distintos** (no son forks entre sí):
  - **A (el original):** `CopilotKit/openmuse` — MIT.
  - **B (paralelo):** `OpenMuseAgent/OpenMuse` → `nano-muse/nanoMuse` — MIT → **GPL-3.0**.
- **Original puede:** chat AG-UI, navegador Chromium con "Take control", computadora Linux opcional, tareas durables, aprobaciones/recibos, Gmail/Calendar, PDF, finanzas CSV, contexto personal, Rich Threads. 154 tests + CI.
- **Original NO puede:** reservas/compras, Drive/Docs, conectores banca/salud/social, push, **voz**, generación de imágenes, OCR/PDF escaneado, multi-usuario, OpenBot en vivo.
- **Requisito crítico:** depende de **CopilotKit Intelligence** (servicio CERRADO, fuera de la licencia MIT) + clave de modelo de pago.
- **Derivados más completos:** zmuse (escritorio Linux gráfico), corgi-publico (Composio + sub-agentes), Agent-Dashboard (modelo local), diggerhq (cloud serverless), nanoMuse (agente completo en el teléfono, GPL).
- **Regla dura:** solo el original cumple **MIT + ≥1000★**. Ningún derivado pasa de 45★.
- **Entregables:** `intel/openmuse-analisis-exhaustivo-20260929.md` (+PDF).

---

## 3. PROYECTO NEREUS — Decisiones (misiones 2, planes v1/v2/v3)

**Codename interno: NEREUS** (⚠️ nunca "Muse/OpenMuse" en el producto — marca de Meta).

### Cons eliminados / pros afianzados
- **Afianzar:** motor de tareas durables, aprobaciones/recibos, worker de navegador, computadora Linux, chat AG-UI, Expo multiplataforma, tests.
- **Eliminar:** dependencia del servicio cerrado, coste por token obligatorio, sin voz, sin memoria real, personalización pobre, sin OCR, conectores escasos, single-owner, sin push, nombre "Muse".

### Decisiones v2 (ordenadas por el Monarca)
| Tema | Decisión |
|------|----------|
| **Gateway de modelo** | **OpenRouter** (pago por uso) — **NO OmniRoute** (falla en rotación) |
| **Memoria** | **Mem0** (principal) + **Graphiti** (temporal/auditoría) |
| **Voz** | **VoiceBox** (TTS/STT/clonación/persona, MIT) + **Pipecat** (turnos + barge-in) |
| **Continuidad multiplataforma** | Servidor autoritativo (Postgres) + SSE/WebSocket + ElectricSQL/PowerSync |

### Decisión v3 — Módulo Avatar
- **Rive** (MIT) como motor del avatar (state machine: idle/escuchando/pensando/hablando) + creador/selector de avatar.
- Alternativa abierta 3D: **VRM + three-vrm + three.js** (MIT).
- Lip-sync ligero por amplitud de audio; fotorrealista (MuseTalk/LivePortrait, MIT) como premium futuro.
- **Entregables:** `intel/plan-nereus-desde-openmuse-20260930.md`, `intel/plan-nereus-v2-20260930.md` (+PDFs).

### Stack final verificado (todo permisivo, cero copyleft)
CopilotKit/openmuse (MIT) · CopilotKit+AG-UI (MIT) · **OpenRouter** · Mem0 (Apache) · Graphiti (Apache) · VoiceBox (MIT) · Pipecat (BSD-2) · Rive (MIT) · Composio (MIT) · Unstructured (Apache) · ElectricSQL/PowerSync (Apache) · pgvector/Qdrant · Playwright (Apache) · Expo (MIT).

**Roadmap:** Fase 0 clone+build *(PENDIENTE)* → 1 persistencia propia → 2 OpenRouter → 3 voz → 4 memoria → 5 conectores → 6 OCR+push → 7 continuidad → 8 avatar → 9 multi-tenant + marca. **Estimación: 4-6 semanas.**

---

## 4. AGNES — Generación de video (misión 3)

- **"Agnes" no es un repo, es una PLATAFORMA:** Agnes AI (Sapiens AI) = pasarela de APIs multimodales **gratis** compatibles OpenAI (texto/imagen/video). **Servicio cerrado**, no open source.
- **Repo de video:** `lcy362/agnes-video-generator` (454★, **MIT**, Python, web self-hosted). Genera video multi-escena desde texto con guion, TTS y subtítulos.
- **NO cumple los estándares del Monarca:** 454★ (<1000) y ~3,5 meses (<6 meses). 2 de 4. **Depende 100% de un servicio gratuito externo.**
- **Alternativa que SÍ cumple:** ⭐ **MoneyPrinterTurbo** (126.9k★, MIT, 2024-03) y Open-Generative-AI, ViMax, LocalAI, autoclip.
- **Entregable:** `intel/agnes-video-generacion-20260930.md` (+PDF).

---

## 5. RÉPLICA DE MODOS AGNES (misión 4)

**Sí, los tres modos son replicables con licencias permisivas:**
- **Creative** (idea→video multi-escena): pipeline — LLM (OpenRouter) → imagen (LocalAI/SD.cpp) → video (**Wan2.2/CogVideo/Open-Sora**, Apache-2.0) → keyframe chaining → TTS (Kokoro/Piper) → subtítulos (faster-whisper) → FFmpeg. **Ya resuelto por MoneyPrinterTurbo.**
- **Manuscript** (artículo→segmentar→video): mismo pipeline + paso de segmentación LLM. Trivial.
- **Digital Anchor** (presentador): fotorrealista con **SadTalker/LivePortrait/MuseTalk/EchoMimic v2**; o estilizado con **Rive/VRM**.
- **Trampas:** **HunyuanVideo** (licencia Tencent no-OSI) y **LTX-Video** (pesos con tope de ingresos) → revisar. **ComfyUI es GPL-3.0**. **Wav2Lip** licencia restrictiva.
- **Coste dominante = GPU**, no el software.
- **Entregable:** `intel/informe-tema-replica-modos-agnes-open-source-20260930.md` (+PDF).

---

## 6. AHORRO DE TOKENS (misión 5) + DATOS REALES

### Repos verificados (MIT)
**LLMLingua** (compresión de prompt 2×–20×), **GPTCache** (caché semántica), **DSPy**, **semantic-router**, **Portkey Gateway** (deployable), **tiktoken**, **PromptWizard**, **cascadeflow**. · Descartado: **litellm** (open-core, no MIT puro).

### Ahorro inmediato
- **Skills `caveman`** (YA instaladas): `caveman`, `caveman-stats`, `caveman-compress`, `caveman-commit`, `caveman-review`. → **activadas en esta sesión (nivel full)**.
- **Caché de prompt de OpenRouter** (ya trabajando).
- **Protocolo de compactación de sesión** (esta acción).

### Medición REAL de esta sesión (de `state.db` de Hermes — el hook oficial `caveman-stats` lee logs de Claude Code, NO de Hermes)
| Métrica | Valor |
|---|---|
| Mensajes | 324 |
| Tool calls / llamadas API | 150 / 150 |
| Input tokens | 3.506.000 |
| Output tokens | 155.062 |
| Cache-read tokens | 32.008.736 |
| Razonamiento | 68.154 |
| **Costo estimado** | **$0.359** |

**Lectura:** la caché trabaja (32M leídos de caché) → coste bajo para 324 mensajes. El volumen alto es **input por contexto grande reenviado cada turno**. Palanca mayor = **compactar sesiones largas**; caveman ataca el **output**.

**Entregable:** `intel/informe-tema-ahorro-tokens-20260930.md` (+PDF).

---

## 7. ÍNDICE DE ENTREGABLES (todos versionados en `github.com/seawolf-studio/seawolf-agent`, rama `master`)

**En `intel/`:**
| Archivo | Tema |
|---|---|
| `openmuse-analisis-exhaustivo-20260929.md/.pdf` | OpenMuse: original, linajes, derivados |
| `plan-nereus-desde-openmuse-20260930.md/.pdf` | Plan v1 (arquitectura + OSS) |
| `plan-nereus-v2-20260930.md/.pdf` | Plan v2 (memoria, voz, continuidad) |
| `agnes-video-generacion-20260930.md/.pdf` | Agnes + alternativas |
| `informe-tema-replica-modos-agnes-open-source-20260930.md/.pdf` | Réplica Creative/Manuscript/Digital Anchor |
| `informe-tema-ahorro-tokens-20260930.md/.pdf` | Ahorro de tokens |

**En `diario-de-sombras/`:**
| Archivo | Tema |
|---|---|
| `sesion-openmuse-a-nereus-20260930.md` | Handoff previo del proyecto NEREUS |
| `informe-auditoria-beru-20260930.md` | Auditoría de Beru (4 informes intel) |
| **este archivo** | Diario completo de la sesión |

**Commits relevantes:** `8fae4ae` (auditoría Beru) · `85fe2db` (fix hash) · `e309563` (handoff + planes v1/v2) · `b2ae35f` (Agnes) · `83525e6` (ahorro de tokens).

---

## 8. ESTADO Y PENDIENTES

- ✅ Misiones 1-5 completadas y versionadas.
- ⏳ **PENDIENTE (crítico):** autorización del Monarca para la **Fase 0** de NEREUS (clone + build local del original en el VPS).
- ⏳ Pendiente: forjar skill `github-repo-recon` (protocolo MIT+estrellas+web+PDF).
- ⏳ Pendiente: blindar auto-arranque del router de sombras (se cayó y tumbó a 9/10; el Monarca dijo que ya sabe el problema).
- ⏳ Pendiente: servir el PDF del informe de tema de tokens a Beru para auditoría.

---

## 9. INSTRUCCIÓN DE RETOMO

> "Bellion, lee el diario de la última sesión y retoma."

Al retomar: reactivar `caveman` si se quiere, verificar estado de Fase 0 de NEREUS, y continuar desde ahí.

---

**Fin del diario de sesión.**
