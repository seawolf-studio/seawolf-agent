# PLAN MAESTRO v2 — "SEAWOLF NEREUS"
## Decisiones técnicas críticas: Memoria · Voz · Continuidad multiplataforma

**Fecha:** 2026-09-30 · **Prioridad:** MÁXIMA · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) — misión en solitario · **Encargado por:** Monarca (Key)
**Base:** `CopilotKit/openmuse` (MIT) · Todas las piezas verificadas contra GitHub API el 2026-09-30.

---

## 0. AJUSTES AL ROADMAP (orden del Monarca)

| Antes (v1) | Ahora (v2) | Motivo |
|-----------|-----------|--------|
| OmniRoute como gateway | **OpenRouter** (único gateway, pago por uso) | OmniRoute falla en rotación de modelos; el Monarca prioriza fiabilidad |
| Memoria = "mem0 (?)" | **DECISIÓN TOMADA** (§1) | — |
| Voz genérica | **VoiceBox + capa de diálogo** (§2) | — |
| Continuidad multiplataforma sin definir | **Arquitectura definida** (§3) | — |

---

## 1. DECISIÓN 1 — LA MEJOR MEMORIA PARA NEREUS

### Veredicto: **Mem0 como capa principal + Graphiti como capa temporal**

**Por qué Mem0 es la elección principal:**
- **Apache-2.0, self-hosteable** (66.4k★) — cumple el criterio Seawolf de licencia permisiva y 100% privado.
- **Es la capa de memoria, no un runtime** — se acopla a NUESTRO agente sin reemplazarlo (Letta sí lo reemplazaría: es una plataforma completa).
- **Diseñada para personalización y continuidad** entre sesiones — exactamente lo que un agente personal necesita.
- **Latencia baja y ahorro de tokens** (~6.900 tokens/recuperación vs 25.000+ del contexto completo).
- **Adopción de mercado real:** es la capa de memoria que usa el Agent SDK de AWS.

**Por qué añadir Graphiti (Zep) como capa temporal:**
- **Apache-2.0** (31.3k★) — grafo de conocimiento **temporal**: cada hecho lleva ventana de validez. Los hechos contradichos se **invalidan, no se borran**.
- Crítico para un agente de confianza: que **no actúe sobre un dato obsoleto** ("el Monarca dijo X en marzo, pero Y en septiembre"). Es la memoria "auditable".

### ⚠️ Honestidad brutal (obligatoria): los benchmarks de memoria están disputados
Los números que circulan son **auto-reportados por los vendedores**. Un informe **independiente** midió Mem0 en **49.0 sobre LongMemEval**, contra el **94.4 auto-reportado**. Zep rebajó su propio score de LoCoMo de 84% a 75.14%, y Mem0 lo reprodujo en 58.44%. **Conclusión: no elegimos por el número de marketing, elegimos por arquitectura y encaje.** Y **mediremos con nuestros propios datos** (evals internas) antes de confiar.

### Alternativas evaluadas (descartadas para primaria)
| Opción | Lic. | Por qué NO como primaria |
|--------|------|--------------------------|
| **Letta** (25k★) | Apache-2.0 | Es un **runtime completo**; adoptarlo para memoria = "comprar un SO por su sistema de archivos". Lock-in. |
| **Zep** (servidor) | — | El servidor legacy ya **no se desarrolla**; solo Graphiti (el motor) sigue vivo. |
| **cognee** (31.2k★) | Apache-2.0 | Buen auto-mejora desde correcciones; menos maduro para personalización general. |
| **Supermemory** (31k★) | **MIT** | Candidato sólido y **totalmente local**; guardar como plan B si queremos cero dependencia. |

**Matriz final de memoria:** Mem0 (principal, personalización) + Graphiti (temporal/auditoría). Interfaz propia y **sustituible** (no nos casamos con ninguno).

---

## 2. DECISIÓN 2 — VOZ: ¿SIRVE "VOICEBOX"?

**Sí, pero para la MITAD del problema.** Verificado: `jamiepine/voicebox` — **56.061★, MIT** — "el estudio de voz open source: clona, dicta, crea". Local-first, 23 idiomas, 7 motores TTS (incl. Kokoro, Chatterbox), STT con Whisper.

### ✅ Lo que VoiceBox SÍ cubre
| Capacidad | Detalle |
|-----------|---------|
| **TTS con clonación de voz** | Clona desde segundos de audio; +50 voces preset |
| **Personalidad de voz** (¡clave para ti!) | Permite **atachar una persona libre a cada perfil de voz** — la voz de NEREUS con su carácter |
| **STT / dictado** | Whisper integrado, hotkey global, push-to-talk y toggle |
| **Multilenguaje** | 23 idiomas — español nativo |
| **Integración con agentes vía MCP** | **Una llamada de herramienta (`voicebox.speak`) y tu agente habla con la voz que clonaste** |
| **Privacidad total** | Modelos y datos **nunca salen de la máquina** — alineado con Seawolf |
| **Expresividad** | Tags paralingüísticos (`[laugh]`, `[sigh]`) con Chatterbox Turbo |

### ❌ Lo que VoiceBox NO cubre
**No es un framework de diálogo en tiempo real.** Es un **estudio de voz (I/O)**: hacer TTS/STT. **No gestiona turnos ni barge-in** por sí solo (su lógica es dictado/push-to-talk, no conversación full-duplex). La interrupción ("hablo y se calla") es una **capa de ingeniería aparte**.

### La pieza que falta: interrupción (barge-in) — verificado
| Herramienta | ★ | Lic. | Qué aporta |
|-------------|----|------|-----------|
| **Kyutai Moshi** | 11.2k | **Apache-2.0** | **Full-duplex nativo** — el mejor para interrupciones reales; speech-to-speech en tiempo real (~200 ms) |
| **Pipecat** | 16.1k | BSD-2 | Framework de orquestación de voz: VAD, turn-taking, **barge-in**; conecta cualquier STT+LLM+TTS |
| **LiveKit Agents** | 14.4k | Apache-2.0 | Producción; maneja interrupciones, RTC a escala |
| **Ultravox** | 4.6k | MIT | LLM multimodal rápido para voz en tiempo real |
| **Kyutai DSM** | 3.0k | Apache-2.0 | STT/TTS streaming de Kyutai |

### 🎯 Stack de voz recomendado para NEREUS
```
Micrófono → STT (Whisper, dentro de VoiceBox)
        → Orquestación de turnos + barge-in (Pipecat  —  o LiveKit Agents)
        → LLM (OpenRouter)
        → TTS (VoiceBox: voz clonada + persona)
        → Altavoz
```
**Resumen:** **VoiceBox = la voz (salida/entrada + clonación + persona). Pipecat (o LiveKit) = el cerebro conversacional que permite interrumpir.** Juntos dan fluidez, velocidad y barge-in. Si buscamos la interrupción más natural posible (hablar y que se calle al instante), **Moshi** es la referencia — pero acopla el diálogo a su propio modelo; Pipecat mantiene nuestra lógica y herramientas.

---

## 3. DECISIÓN 3 — CONTINUIDAD MULTIPLATAFORMA (PC ↔ Móvil)

**Requisito:** empezar en PC, salir, y seguir desde el móvil con el progreso intacto.

### Arquitectura: **estado autoritativo en servidor + canal en tiempo real + caché local**
El núcleo ya nos lo da el original: las **tareas durables viven en el servidor** (no en el cliente). El progreso de un agente que "sigue trabajando" es **intrínsecamente server-side**. Solo hay que exponerlo a todos los dispositivos.

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│  PC/Web  │        │  Móvil   │        │  otro    │
└────┬─────┘        └────┬─────┘        └────┬─────┘
     └───────────────┬───┴───────────────────┘
                     │  SSE / WebSocket (canal en vivo)
          ┌──────────▼───────────┐
          │  SERVIDOR (fuente     │  ← hilos, tareas, memoria,
          │  de verdad única)     │    aprobaciones: estado único
          │  PostgreSQL + pgvector│
          └──────────────────────┘
```

**Componentes verificados para la capa de sync:**
| Necesidad | Opción | Lic. | Nota |
|-----------|--------|------|------|
| Canal en tiempo real (progreso en vivo) | **SSE / WebSocket propio** o **Supabase Realtime** | Apache-2.0 | El original ya usa SSE/AG-UI |
| Estado local-first (seguir offline) | **ElectricSQL** (10.4k★) o **PowerSync** | Apache-2.0 | Sincroniza Postgres ↔ cliente |
| Estado colaborativo/CRDT (si hiciera falta) | **Automerge** (6.6k★) / **Yjs** | MIT | Para edición concurrente |
| ❌ Descartado | ~~Triplit~~ | **AGPL-3.0** | Copyleft — fuera |

**Decisión:** **servidor autoritativo (Postgres) + SSE/WebSocket para vivo + ElectricSQL/PowerSync para caché offline.** Así: abres en PC → el trabajo corre en el servidor → abres el móvil → **la misma sesión, el mismo progreso, en vivo**. Sin lógica de sync frágil.

---

## 4. ROADMAP v2 (actualizado)

| Fase | Entregable | Cambios v2 |
|------|-----------|-----------|
| 0 | Clone + build local del original | igual |
| 1 | Persistencia propia (adiós servicio cerrado) | Postgres + pgvector |
| 2 | **Modelo: OpenRouter** (reemplaza OmniRoute) | **CAMBIO** |
| 3 | **Voz: VoiceBox (TTS/STT/persona) + Pipecat (barge-in)** | **DEFINIDO** |
| 4 | **Memoria: Mem0 + Graphiti** | **DEFINIDO** |
| 5 | Conectores Composio (ya instalado + Gmail OAuth) | igual |
| 6 | OCR (Unstructured) + Push | igual |
| 7 | **Continuidad multiplataforma (SSE + ElectricSQL/PowerSync)** | **DEFINIDO** |
| 8 | Multi-tenant + marca Seawolf + despliegue | igual |

**Estimación:** 4-6 semanas de ingeniería. Con 3 decisiones cerradas hoy, el camino se acorta y se desriesga.

---

## 5. COMPONENTES FINALES (todo verificado, licencia permisiva)

| Capa | Componente | Lic. | ★ |
|------|-----------|------|---|
| Base del agente | CopilotKit/openmuse | MIT | 3.4k |
| UI/streaming | CopilotKit + AG-UI | MIT | 37.6k |
| Gateway de modelo | **OpenRouter** | (servicio) | — |
| Memoria principal | **Mem0** | Apache-2.0 | 66.4k |
| Memoria temporal | **Graphiti** | Apache-2.0 | 31.3k |
| Voz — TTS/STT/persona | **VoiceBox** | MIT | 56.1k |
| Voz — diálogo/barge-in | **Pipecat** (o LiveKit Agents) | BSD-2 | 16.1k |
| Full-duplex (opción) | Kyutai Moshi | Apache-2.0 | 11.2k |
| Conectores | Composio | MIT | 30.4k |
| Docs/OCR | Unstructured | Apache-2.0 | 15.5k |
| Sync multiplataforma | ElectricSQL / PowerSync | Apache-2.0 | 10.4k / 0.7k |
| Vector DB | pgvector / Qdrant | PostgreSQL / Apache-2.0 | 23.2k / 34.9k |
| Navegador | Playwright | Apache-2.0 | 96.9k |
| Móvil/Web | Expo | MIT | 52.5k |

**Cero copyleft. Cero servicio cerrado obligatorio. Todo auto-hospedable.**

---

## 6. SIGUIENTE PASO

Plan v2 con las 3 decisiones críticas cerradas. **Autoriza la Fase 0** (clone + build local del original en el VPS) para convertir el plan en código ejecutable — la cancha es mía, pero la orden de arranque es tuya.

**Fin del informe v2.** Listo para auditoría de Beru.
