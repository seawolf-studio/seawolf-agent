# DIARIO DE SESIÓN — OpenMuse → Proyecto NEREUS
## Handoff para sesión dedicada (protocolo de compactación Seawolf)

**Fecha de sesión:** 2026-09-29 → 2026-09-30 · **Elaborado por:** Bellion (Gran Comandante)
**Encargado por:** Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Propósito:** Congelar TODA la inteligencia y decisiones de esta sesión para retomarla en una sesión nueva y dedicada al proyecto, sin pérdida de contexto.

---

## 0. CÓMO RETOMAR ESTA MISIÓN (leer primero)

1. Abrir una **sesión nueva** y ordenar: **"lee el diario de la última sesión"** → Bellion lee este archivo y retoma.
2. **Estado actual:** planificado y verificado hasta el **plan v3** (avatar). **NO se ha escrito código todavía.** Falta la orden del Monarca para arrancar la **Fase 0** (clone + build del original).
3. **Archivos clave de esta sesión:**
   - `C:\Users\Admin\intel\openmuse-analisis-exhaustivo-20260929.md` (+ PDF) — inteligencia completa de OpenMuse y derivados.
   - `C:\Users\Admin\intel\plan-nereus-desde-openmuse-20260930.md` (+ PDF) — Plan v1 (arquitectura, OSS matrix).
   - `C:\Users\Admin\intel\plan-nereus-v2-20260930.md` (+ PDF) — Plan v2 (memoria, voz, continuidad).
   - Este diario — resumen maestro y decisiones.

---

## 1. LA SOLICITUD ORIGINAL DEL MONARCA

Investigar en GitHub, de forma **profunda y exhaustiva**, todo lo relativo a **OpenMuse**: el repo original y los derivados más completos, con un informe (MD + PDF) centrado en **qué puede y qué no puede hacer cada uno comparado con el original**. Misión marcada como **CRÍTICA** ("hay dinero de por medio"). Después derivó en: **construir NUESTRA versión** desde esa base, quitando contras y afianzando pros, replicando por vía open-source el resto de capacidades (personalización, voz, conversación, avatar), para lanzarla bajo la marca **Seawolf Studio**.

---

## 2. HALLAZGOS CRÍTICOS SOBRE OPENMUSE

### 2.1 Contexto: Meta "Muse"
Meta lanzó **Muse** el **8-sep-2026** (agente personal, Muse Secure VM, Gmail/Calendar/OpenTable/Instagram/Plaid, pagos, llamadas, iOS/Android/web/gafas). Cerrado y propietario.

### 2.2 El original open source
**`CopilotKit/openmuse`** — lanzado **15-sep-2026** (una semana después) por CopilotKit (Atai Barkai) como **clon open source de Meta Muse**. **MIT**, TypeScript, ~3.436★, 445 forks, versión **0.1.0-alpha**.

### 2.3 ⚠️ HALLAZGO CLAVE: existen DOS linajes distintos llamados "OpenMuse"
| Linaje | Repo raíz | Lenguaje | Licencia | Relación |
|--------|-----------|----------|----------|----------|
| **A — EL ORIGINAL** | `CopilotKit/openmuse` | TypeScript | **MIT** | Forkeado por ~445 repos |
| **B — paralelo** | `OpenMuseAgent/OpenMuse` → `nano-muse/nanoMuse` | Python → Swift | MIT → **GPL-3.0** | Reimplementación independiente |

**No son forks entre sí.** Cualquier análisis que los mezcle es incorrecto.

### 2.4 El original — qué PUEDE y qué NO PUEDE
**Puede:** chat AG-UI (iOS/Android/web); navegador Chromium persistente con "Take control"; computadora Linux opcional (Docker, `/workspace`, sin red); tareas durables (planes, pausa/reanudar/cancelar/reintentar, aprobaciones, recibos); Ideas; Goals & Tracking; documentos PDF (relleno de formularios); finanzas CSV; Gmail+Calendar (OAuth); contexto personal (nombre/tono/avatar/memoria); Rich Threads. 154 tests + CI.

**NO puede:** terminal interactiva; apps de escritorio; VM por persona; red controlada; cuotas de disco; **reservas/compras/checkout**; Drive/Docs; **conectores banca/salud/Instagram/WhatsApp**; **push de dispositivo**; **voz**; **generación de imágenes**; **OCR/PDF escaneado**; multi-usuario; OpenBot en vivo.
**Requisitos:** Node 24, pnpm, **clave de CopilotKit Intelligence** (servicio CERRADO, fuera de la licencia MIT) + clave de modelo de pago.

### 2.5 Derivados más completos (del original)
| Repo | ★ | Lic. | Añade vs original | Pierde |
|------|---|------|-------------------|--------|
| **xuboboo/zmuse** | 2 | MIT | Escritorio Linux gráfico (Xfce), app nativa Windows, UI china | Solo Windows; sin verificar |
| **joaovitor2763/corgi-publico** | 1 | NOASSERTION | Composio (Slack/Notion/Drive), sub-agentes, voz, Web Push, guarda anti-phishing | Licencia NO declarada |
| **norhtecmbarnes-dot/Agent-Dashboard** | 1 | NOASSERTION | Modelo local (llama.cpp), Telegram, app Android | Licencia NO declarada |
| **diggerhq/openmuse** | 44 | (none) | Cloud serverless (OpenComputer), modelo "topic" | **NO es MIT**; tercero |
| **nanoMuse** (linaje B) | 25 | **GPL-3.0** | Agente completo en el teléfono; controla apps sin API (WeChat/Alipay) | Copyleft |

**Regla:** solo el original cumple **MIT + ≥1000★**. Todos los derivados están por debajo de 45★.

---

## 3. DECISIONES TOMADAS (Planes v1 → v3)

### 3.1 Base y cirugía (Plan v1)
- **Base:** `CopilotKit/openmuse` (MIT).
- **Afianzar (pros):** motor de tareas durables, aprobaciones/recibos, worker de navegador, computadora Linux, chat AG-UI, Expo multiplataforma, 154 tests.
- **Eliminar (contras):** dependencia del servicio cerrado CopilotKit Intelligence; coste por token obligatorio; sin voz; sin memoria real; personalización pobre; sin OCR; conectores escasos; single-owner; sin push; nombre "Muse" (marca de Meta).

### 3.2 Decisiones v2 (ordenadas por el Monarca)
| Tema | DECISIÓN | Sustento |
|------|----------|----------|
| **Gateway de modelo** | **OpenRouter** (pago por uso) — **NO OmniRoute** (falla en rotación de modelos) | Fiabilidad |
| **Memoria** | **Mem0** (principal, personalización) + **Graphiti** (capa temporal/auditoría) | Apache-2.0 ambas; Mem0=drop-in, Graphiti=hechos con validez temporal |
| **Voz** | **VoiceBox** (TTS/STT/clonación/persona, MIT) + **Pipecat** (turnos + barge-in) | VoiceBox cubre la voz pero NO la conversación full-duplex |
| **Continuidad multiplataforma** | Servidor autoritativo (Postgres) + SSE/WebSocket + ElectricSQL/PowerSync | Empezar en PC, seguir en móvil con progreso vivo |

### 3.3 Decisión v3 — Módulo Avatar (la capa de personalización de Muse)
| Pieza | Solución | Lic. | ★ |
|-------|----------|------|---|
| Avatar animado con acciones (state machine) | **Rive** (`rive-runtime`, `rive-react-native`) | **MIT** | 1.2k / 784 |
| Diseño/reemplazo (vía rápida) | Rive Editor (gratis; runtime MIT, asset nuestro) | — | — |
| Diseño/reemplazo (vía 100% abierta, 3D) | **Blender → VRM** + **three-vrm** + **three.js** + **react-three-fiber** | MIT | 2.2k / 116k / 32.6k |
| Lip-sync ligero (recomendado) | Animación "speaking" + amplitud de audio de VoiceBox | — | — |
| Lip-sync realista (premium futuro) | **MuseTalk** (MIT) · **LivePortrait** (MIT) · **SadTalker** (Apache-2.0) | permisivas | 6.6k / 19.1k / 14.1k |
| ❌ Evitar | ~~Wav2Lip~~ (licencia restrictiva) | — | — |
| Expresividad en vivo | Kalidokit (MIT) + MediaPipe (Apache-2.0) | permisivas | 5.7k / 37k |

**Recomendación:** **Rive** como motor del avatar (state machine: idle/escuchando/pensando/hablando) + creador/selector de avatar; lip-sync por amplitud. VRM 3D como alternativa abierta. Fotorrealistas como "modo vídeo premium".

---

## 4. STACK FINAL VERIFICADO (todo permisivo, cero copyleft, cero servicio cerrado obligatorio)

| Capa | Componente | Lic. | ★ |
|------|-----------|------|---|
| Base del agente | CopilotKit/openmuse | MIT | 3.4k |
| UI/streaming | CopilotKit + AG-UI | MIT | 37.6k / 16.1k |
| Gateway modelo | **OpenRouter** | servicio (pago/uso) | — |
| Memoria principal | **Mem0** | Apache-2.0 | 66.4k |
| Memoria temporal | **Graphiti** | Apache-2.0 | 31.3k |
| Voz TTS/STT/persona | **VoiceBox** | MIT | 56.1k |
| Voz diálogo/barge-in | **Pipecat** (o LiveKit Agents) | BSD-2 | 16.1k |
| Full-duplex (opción) | Kyutai Moshi | Apache-2.0 | 11.2k |
| Avatar | **Rive** (o VRM/three-vrm) | MIT | 1.2k / 2.2k |
| Conectores | Compose (Composio) — ya instalado + Gmail OAuth | MIT | 30.4k |
| Docs/OCR | Unstructured | Apache-2.0 | 15.5k |
| Sync multiplataforma | ElectricSQL / PowerSync | Apache-2.0 | 10.4k / 0.7k |
| Vector DB | pgvector / Qdrant | PostgreSQL / Apache-2.0 | 23.2k / 34.9k |
| Navegador | Playwright | Apache-2.0 | 96.9k |
| Móvil/Web | Expo | MIT | 52.5k |

**Descartados por licencia:** fish-speech (Research License), coqui TTS (MPL-2.0, muerto), Wav2Lip (restrictiva), Triplit (AGPL), nanoMuse/openmuseai (GPL/AGPL), n8n (fair-code), Automatisch/Beehive/Socioboard (AGPL/GPL).

---

## 5. ROADMAP

| Fase | Entregable |
|------|-----------|
| **0** | Clone + build local del original en el VPS *(PENDIENTE DE AUTORIZACIÓN)* |
| 1 | Persistencia propia (Postgres + pgvector) — adiós servicio cerrado |
| 2 | Modelo: **OpenRouter** |
| 3 | Voz: **VoiceBox + Pipecat** (barge-in) |
| 4 | Memoria: **Mem0 + Graphiti** |
| 5 | Conectores: **Composio** |
| 6 | OCR (**Unstructured**) + Push |
| 7 | Continuidad multiplataforma (SSE + ElectricSQL/PowerSync) |
| 8 | **Módulo Avatar (Rive)** |
| 9 | Multi-tenant + marca Seawolf + despliegue |

**Estimación honesta:** 4-6 semanas de ingeniería real. No es un fin de semana.

---

## 6. ESTADO Y PENDIENTES

- ✅ Inteligencia OpenMuse exhaustiva (129 repos), derivados y análisis can/cannot.
- ✅ Plan v1 (arquitectura + matriz OSS verificada).
- ✅ Plan v2 (memoria, voz, continuidad — decisiones cerradas por el Monarca).
- ✅ Plan v3 (módulo avatar — Rive/VRM).
- ✅ 4 informes de inteligencia auditados por **Beru** y subidos a `github.com/seawolf-studio/seawolf-agent` (commit de auditoría `8fae4ae`, corrección de hash `85fe2db`).
- ⏳ **PENDIENTE: autorización del Monarca para arrancar la Fase 0** (clone + build).
- ⏳ Pendiente: forjar skill `github-repo-recon` (protocolo de búsqueda MIT+estrellas+web+PDF).
- ⏳ Pendiente: blindar auto-arranque de OmniRoute (nota al margen: se cayó y tumbó a 9/10 sombras; el Monarca dijo que ya sabe el problema).

---

## 7. INSTRUCCIÓN DE RETOMO

> "Bellion, lee el diario de la última sesión (sesion-openmuse-a-nereus-20260930.md) y retoma el proyecto NEREUS."

Al retomar: verificar el estado de la Fase 0 y continuar desde ahí. La cancha es del Comandante; la señal de salida es del Monarca.

---

**Fin del diario de sesión.** Archivo listo para commit en `diario-de-sombras/`.
