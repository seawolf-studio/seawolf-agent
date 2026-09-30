# PLAN MAESTRO — "SEAWOLF NEREUS": Nuestro Agente Personal desde la Base de OpenMuse

**Fecha:** 2026-09-30 · **Prioridad:** MÁXIMA · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Base:** `CopilotKit/openmuse` (MIT) · **Objetivo:** construir NUESTRO agente eliminando los contras del original, afianzando sus pros, y replicando por vía open-source las capacidades ausentes (voz, personalización, memoria, conversación), para luego lanzarlo bajo la marca Seawolf Studio.

> **Nombre provisional:** **NEREUS** (dios marino griego, cambia de forma y es digno de confianza). ⚠️ **NUNCA usar "Muse/OpenMuse"** en el producto final — es marca de Meta (riesgo legal). El nombre definitivo lo decide el Monarca.

---

## PLAN DE ACCIÓN (orden numerada — mandato Bellion)

1. **Fase 0 — Viabilidad real:** `git clone` del original + `pnpm install` + build local en el VPS. Confirmar que arranca sin el servicio cerrado.
2. **Fase 1 — Cirugía del "rehén":** arrancar la dependencia de **CopilotKit Intelligence** y sustituirla por persistencia propia (PostgreSQL + pgvector) para hilos y replay.
3. **Fase 2 — Motor de modelo:** enganchar **OmniRoute** (ya instalado) como gateway único + **Ollama/llama.cpp** para modo 100% local. Fin del coste por token obligatorio.
4. **Fase 3 — Voz:** añadir STT + TTS open-source y orquestación de turnos de voz.
5. **Fase 4 — Personalización y memoria real:** capa de memoria semántica + perfiles de usuario.
6. **Fase 5 — Conectores:** capa **Composio** (ya instalada y con Gmail autorizado) para multiplicar integraciones.
7. **Fase 6 — Huecos documentales:** OCR/PDF escaneado (Unstructured) y notificaciones push.
8. **Fase 7 — Multi-tenant:** auth propia (el original es single-owner).
9. **Fase 8 — Marca y salida:** rebranding Seawolf, español nativo, vertical objetivo (CSO), despliegue.
10. **Verificación continua:** cada fase → reporte MD → auditoría de Beru.

---

## 1. LO QUE TOMAMOS Y LO QUE QUITAMOS DEL ORIGINAL

### 1.1 ✅ PROS A AFIANZAR (lo que el original hace bien y NO tocamos)
| Pro | Por qué conservarlo |
|-----|---------------------|
| Motor de tareas durables (planes, pausa/reanudar/cancelar/reintentar, leases SQL) | Es el corazón de un agente "que sigue trabajando". Difícil de reconstruir. |
| Revisiones y recibos de acción (aprobaciones antes de lo irreversible) | Seguridad y confianza — el diferencial de un agente personal. |
| Worker de navegador (Playwright, perfiles persistentes, "Take control") | Capacidad real de obrar en la web. |
| Computadora Linux opcional (Docker, `/workspace` persistente, recibos) | Ejecuta comandos y maneja archivos en aislamiento. |
| Chat AG-UI con streaming + tarjetas ricas inline | UX conversacional moderna, sin reinventar. |
| Multiplataforma Expo (iOS/Android/web) | Un solo código para los 3 canales. |
| Arquitectura modular (server/worker/computer/packages) | Extensible sin romper el núcleo. |
| 154 tests + CI + verificación de Chromium y Docker reales | Base probada, no un juguete. |

### 1.2 ❌ CONTRAS A ELIMINAR (los defectos que sí tocamos)
| Contra del original | Por qué es un problema | Solución (ver §2) |
|---------------------|------------------------|-------------------|
| Depende de **CopilotKit Intelligence** (servicio CERRADO, obligatorio) | Rehén arquitectónico; fuera de la licencia MIT; no es 100% self-host | Persistencia propia (Postgres+pgvector) |
| **Coste por token obligatorio** (OpenAI/Anthropic/Google) | Sangra dinero en cada misión | OmniRoute (free pool) + modelos locales |
| **Sin voz** (roadmap "future work") | Muse habla; el original no | STT+TTS open-source (§2.2) |
| **Sin memoria semántica real** (solo "memorias" editables) | No "recuerda por significado" | mem0 / Letta / Zep (§2.3) |
| **Personalización pobre** (nombre/tono/avatar) | Muse se personaliza de verdad | Capa de perfil + memoria (§2.3) |
| **Sin OCR / PDF escaneado** | No maneja documentos reales | Unstructured (§2.4) |
| **Conectores escasos** (solo Gmail/Calendar) | Muse conecta todo | Composio (§2.5) |
| **Single-owner** (clave compartida) | No es un producto multi-cliente | Auth multi-tenant propia (§2.6) |
| **Sin notificaciones push** | No avisa al cerrar la app | Expo Push / Web Push (§2.4) |
| **Alpha de 2 semanas, 50 issues** | Inestable | Hardenizado propio + pinning de versión |
| Nombre "Muse/OpenMuse" | Marca de Meta | Rebranding Seawolf |

---

## 2. MATRIZ DE SUSTITUCIÓN OPEN-SOURCE (VERIFICADA HOY EN GITHUB API)

> Todas las piezas verificadas: estrellas, licencia y actividad al 2026-09-30. **Criterio Seawolf: licencia permisiva (MIT/Apache/BSD/PostgreSQL). Cero AGPL/GPL/Research.**

### 2.1 Reemplazo del servicio cerrado (el contra #1)
| Necesidad | Sustituto | Lic. | Estado real |
|-----------|-----------|------|-------------|
| Persistencia de hilos + replay (CopilotKit Intelligence) | **PostgreSQL + pgvector** (auto-hospedado) | PostgreSQL License | 23.2k★, activo |
| Búsqueda vectorial de memoria | **pgvector** o **Qdrant** | PostgreSQL / **Apache-2.0** | 23.2k★ / 34.9k★ |
| Orquestación del agente / UI | **CopilotKit** + **AG-UI** (se mantienen) | **MIT** | 37.6k★ / 16.1k★ |

### 2.2 Voz (capacidad ausente #1 del original)
| Capa | Sustituto | Lic. | Estado real |
|------|-----------|------|-------------|
| **STT** (oír) | **faster-whisper** (o whisper.cpp para edge) | **MIT** | 25.6k★ / 54k★ |
| **STT alterno** | Moonshine (modelos livianos on-device) | MIT | 11.2k★ |
| **TTS** (hablar) | **Kokoro** (calidad/liviano) | **Apache-2.0** | 9.1k★ |
| **TTS alterno** | **Piper** (rápido, embebible) | **MIT** | 11.3k★ |
| **TTS alterno** | MeloTTS · Chatterbox · F5-TTS | MIT | 7.7k / 26.6k / 15.3k |
| **Orquestación de voz realtime** | **Pipecat** o **LiveKit Agents** | BSD-2 / Apache-2.0 | 16.1k★ / 14.4k★ |
| ❌ Descartado | ~~coqui-ai/TTS~~ (MPL-2.0 + proyecto muerto) y ~~fish-speech~~ (**Research License, NO open source**) | — | — |

### 2.3 Personalización y memoria (capacidad ausente #2)
| Necesidad | Sustituto | Lic. | Estado real |
|-----------|-----------|------|-------------|
| Memoria semántica de largo plazo | **mem0** | **Apache-2.0** | 66.4k★ |
| Memoria "con estado"/agente persistente | **Letta** (ex-MemGPT) | Apache-2.0 | 25.0k★ |
| Memoria conversacional + grafo | **Zep** | Apache-2.0 | 4.9k★ |
| Memoria de agente LangGraph | **LangMem** | MIT | 1.7k★ |
| Perfil/personalización (nombre, tono, avatar, preferencias) | capa propia sobre Postgres + mem0 | — | a construir |

### 2.4 Huecos documentales y notificaciones
| Necesidad | Sustituto | Lic. | Estado real |
|-----------|-----------|------|-------------|
| OCR / PDF escaneado / parseo de documentos | **Unstructured** | Apache-2.0 | 15.5k★ |
| Notificaciones push (móvil/web) | **Expo Push** + Web Push | MIT | (Expo 52.5k★) |

### 2.5 Conectores (el contra más caro de cubrir)
| Necesidad | Sustituto | Lic. | Estado real |
|-----------|-----------|------|-------------|
| Multiplicar integraciones (Slack/Notion/Drive/Gmail/Calendar…) | **Composio** | **MIT** | 30.4k★ |
| ⚡ Ventaja Seawolf | **Composio YA está instalado en la máquina del Monarca + Gmail ya autorizado por OAuth** | — | listo para usar |

### 2.6 Motor de modelo y despliegue
| Necesidad | Sustituto | Lic. | Estado real |
|-----------|-----------|------|-------------|
| Gateway multi-proveedor con fallback | **OmniRoute** (ya instalado, local) | MIT | en uso |
| Modelos 100% locales | **Ollama** / **llama.cpp** | MIT | 182k★ / 130k★ |
| Automatización de navegador | **Playwright** (ya usado por el original) | Apache-2.0 | 96.9k★ |
| App multiplataforma | **Expo** (ya usado) | MIT | 52.5k★ |

---

## 3. ARQUITECTURA PROPUESTA — "SEAWOLF NEREUS"

```
┌─────────────────────────────────────────────────────────────────┐
│  CANALES:  Web  ·  iOS  ·  Android        (Expo — MIT, se conserva)│
│            + VOZ (Pipecat/LiveKit)  + PUSH (Expo Push)            │
└───────────────┬───────────────────────────────────────────────────┘
                │  AG-UI (MIT) + API autenticada
┌───────────────▼───────────────────────────────────────────────────┐
│  API (Hono) + runtime CopilotKit (MIT)                            │
│   ├── Motor de tareas durables (se conserva del original)         │
│   ├── Revisiones / aprobaciones / recibos (se conserva)           │
│   ├── ► PERSISTENCIA PROPIA: PostgreSQL + pgvector  ← reemplaza   │
│   │     al servicio cerrado CopilotKit Intelligence               │
│   ├── ► MEMORIA: mem0 (Apache-2.0)                                 │
│   ├── ► CONECTORES: Composio (MIT) — ya instalado                 │
│   │     Gmail · Calendar · Slack · Notion · Drive …               │
│   └── ► MODELO: OmniRoute (gateway+fallback) / Ollama (local)     │
├───────────────┬───────────────────────────────────────────────────┤
│  Worker navegador (Playwright — Apache-2.0)                       │
│  Computadora Linux opcional (Docker, /workspace)                  │
│  ► VOZ: faster-whisper (STT) + Kokoro/Piper (TTS)                 │
│  ► DOCS: Unstructured (OCR/PDF)                                   │
└───────────────────────────────────────────────────────────────────┘
```

**Ganancia neta vs el original:** +voz, +memoria real, +personalización, +conectores, +OCR, −coste por token obligatorio, −dependencia de servicio cerrado. **Todo con licencias permisivas.**

---

## 4. PARIDAD vs META MUSE (expectativa realista)

| Capacidad de Meta Muse | OpenMuse original | **NEREUS (nuestro)** |
|------------------------|-------------------|----------------------|
| VM con navegador visible | ✅ | ✅ |
| Corre tras cerrar la app (tareas de fondo) | ✅ | ✅ |
| Aprueba antes de lo irreversible | ✅ | ✅ |
| Gmail + Calendar | ✅ | ✅ (+ Composio) |
| Slack/Notion/Drive | ❌ | ✅ (Composio) |
| Voz (hablar/oir) | ❌ | ✅ (OSS) |
| Memoria semántica real | ❌ | ✅ (mem0) |
| OCR/PDF escaneado | ❌ | ✅ (Unstructured) |
| Push al móvil | ❌ | ✅ |
| Multi-tenant (producto) | ❌ | ✅ (a construir) |
| **Auto-hospedado / privado** | ⚠️ (depende servicio externo) | ✅ **100%** |
| **Español nativo** | ❌ | ✅ |
| Plaid / banca | ❌ | ❌ (fuera de MVP) |
| Pagos / checkout | ❌ | ❌ (fuera — riesgo legal) |
| Llamadas telefónicas | ❌ | ❌ (fuera) |
| Instagram/Facebook | ❌ | ❌ (proscrito por el Monarca) |
| Gafas / hardware | ❌ | ❌ (fuera) |

**Conclusión honesta:** no superamos a Muse en *alcance de consumo* (pagos, telefonía, hardware, distribución). **Sí lo superamos en auto-hospedaje, privacidad, idioma, voz, memoria y conectores.** Ese es el carril.

---

## 5. ROADMAP POR FASES

| Fase | Entregable | Esfuerzo estimado |
|------|-----------|-------------------|
| 0 | Clone + build local + verificación de arranque | 1 día |
| 1 | Persistencia propia (adiós servicio cerrado) | 3-5 días |
| 2 | OmniRoute + Ollama (fin del coste obligatorio) | 1-2 días |
| 3 | Voz STT+TTS + turnos de voz | 5-8 días |
| 4 | mem0 + perfiles de personalización | 3-5 días |
| 5 | Composio (conectores) | 3-5 días |
| 6 | Unstructured (OCR) + Push | 3-4 días |
| 7 | Multi-tenant (auth propia) | 5-8 días |
| 8 | Rebranding + español + despliegue vertical | 5-10 días |

**Estimación total (MVP usable):** 4-6 semanas de trabajo de ingeniería real. **No es un fin de semana** — es honesto decirlo.

---

## 6. RIESGOS Y REGLAS INAQUEBRANTABLES

| Riesgo | Mitigación |
|--------|-----------|
| **Legal / marca "Muse"** | Rebranding Seawolf; cero referencias a Meta Muse en el producto |
| **Licencias copyleft** | Solo MIT/Apache/BSD/PostgreSQL. Vetar AGPL/GPL/Research en cada dependencia |
| **Upstream alpha (2 semanas, alto churn)** | Pinnear commit; tratar el fork como base congelada + cherry-picks |
| **Coste de modelos** | OmniRoute free pool + Ollama local; premium solo para crítico |
| **Esfuerzo subestimado** | Roadmap por fases con verificación; nada se declara "listo" sin prueba real |
| **Dependencia de Composio/terceros** | Interfaz de conectores abstraída; Composio es sustituible |

**Reglas de oro:** (1) nada se entrega sin ejecutarlo de verdad; (2) cada fase pasa por auditoría de Beru; (3) cero copyleft en producción.

---

## 7. SALIDA AL MUNDO — MARCA SEAWOLF STUDIO

- **Nombre:** a definir por el Monarca (codename interno: NEREUS). Evitar "Muse".
- **Identidad:** paleta Seawolf (#121E1E / #4CE8E7 / #48E8D8).
- **Posicionamiento:** *"Tu agente personal. Tu servidor. Tus datos. En tu idioma."* — el wedge anti-lock-in, español-nativo y privado que Meta nunca hará.
- **Vertical de entrada:** el arquetipo CSO del Monarca (cliente súper ocupado; agente sobre SU Gmail/Calendar/datos).
- **Modelo:** self-hosted / suscripción (a definir con el resultado del MVP).

---

## 8. VERIFICACIÓN Y SIGUIENTE PASO

- Toda la matriz OSS de §2 fue **verificada contra la GitHub API el 2026-09-30** (estrellas, licencia, actividad).
- **Pendiente de aprobación del Monarca:** ejecutar la **Fase 0** (clone + build) para convertir este plan en código ejecutable.

**Este plan queda listo para auditoría de Beru.**

**Fin del informe.**
