# INFORME DE EJECUCIÓN — FASE 2 "SEAWOLF NEREUS"
## Gateway de modelo: OpenRouter como vía única

**Fecha:** 2026-10-01 · **Prioridad:** MÁXIMA · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) — misión en solitario · **Encargado por:** Monarca (Key)
**Objetivo:** enganchar **OpenRouter** como gateway de modelo único, eliminando el coste por token obligatorio atado a proveedores concretos y la resolución dispersa de proveedores.
**Resultado:** ✅ **FASE 2 COMPLETADA.** NEREUS genera respuestas con **modelo real vía OpenRouter**; el gateway cubre **agente de chat y task worker**; suite en **276/276 verdes**.

---

## 1. RECONOCIMIENTO — DÓNDE SE RESOLVÍA EL MODELO

- Punto **único** de resolución: `apps/server/src/engine/tanstack-agent.ts` → función `adapter(spec)`, que traduce `"proveedor/modelo"` a un adaptador del SDK. Solo soportaba `openai`, `anthropic` y `google`.
- Tanto el **agente de chat** (`conversation.ts`) como el **task worker** (`engine/model.ts:296`) llaman al **mismo** `tanstackAgent(...)` → `adapter(...)`. **Una sola puerta que cambiar.**
- Formato previo: `MODEL=<proveedor>/<modelo>` con `OPENAI_BASE_URL`, `ANTHROPIC_BASE_URL`, `GOOGLE_GENERATIVE_AI_BASE_URL`.

---

## 2. LO QUE SE CONSTRUYÓ

### 2.1 Proveedor `openrouter` de primera clase
En `engine/tanstack-agent.ts`, usando el adaptador **`openaiCompatibleText`** (subruta `@tanstack/ai-openai/compatible`, hecha para endpoints compatibles con OpenAI):

- **Formato de spec:** `openrouter/<vendor>/<model>` — p. ej. `openrouter/anthropic/claude-sonnet-4.5` (el id de OpenRouter conserva su prefijo de vendor).
- **Base URL:** `OPENROUTER_BASE_URL` o por defecto `https://openrouter.ai/api/v1`.
- **Clave:** `OPENROUTER_API_KEY`.
- **Protocolo:** `chat-completions` (el que habla OpenRouter).
- **Cabeceras de identificación:** `HTTP-Referer` y `X-Title` (atribución en OpenRouter) configurables.
- **Reintentos:** hereda `MODEL_MAX_RETRIES`.

### 2.2 Configuración
- `agent.ts` → `agentConfigured()` ahora reconoce `OPENROUTER_API_KEY` como clave válida.
- `.env` de NEREUS: `AGENT_BACKEND=model`, `MODEL=openrouter/openai/gpt-4o-mini`, `OPENROUTER_API_KEY=<clave del Monarca>`, `OPENROUTER_REFERER`, `OPENROUTER_TITLE`. (La clave se reutiliza del propio `/root/.hermes/.env` del VPS; **no se expone** en informes ni logs.)

---

## 3. VERIFICACIÓN REAL

| Prueba | Resultado |
|--------|-----------|
| `pnpm typecheck` + `lint` + `build:server` | ✅ limpios |
| **Suite completa** | ✅ **276/276 · 0 fallos** |
| Validez de la clave OpenRouter (`/api/v1/models`) | ✅ 462 modelos disponibles |
| **Run con modelo REAL vía OpenRouter** (gpt-4o-mini) | ✅ stream `RUN_STARTED`→`TEXT_MESSAGE_CONTENT`(15)→`RUN_FINISHED`, **sin `RUN_ERROR`** |
| **Tool-calling vía OpenRouter** | ✅ el modelo invocó herramientas (`write_computer_file`, `start_computer`) y recibió resultados |
| **Persistencia tras el run** | ✅ fila en Postgres: **206 eventos · 5 mensajes** |
| Fuente de la clave | ✅ reutilizada del VPS, **no expuesta** |

**Nota de honestidad:** una primera prueba con un **modelo gratuito** (`qwen3.8-27b:free`) devolvió `400 Provider returned error` (límite del plan gratuito). El gateway funcionó (transmitió respuesta real en español), pero **el proveedor gratis era inestable**. Se fijó por defecto un modelo **pago barato** (`openai/gpt-4o-mini`) que corrió **limpio**. Saldo OpenRouter del Monarca: **~$19.33 disponibles**.

---

## 4. ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| `apps/server/src/engine/tanstack-agent.ts` | caso `openrouter` vía `openaiCompatibleText` + import |
| `apps/server/src/agent.ts` | `agentConfigured` acepta `OPENROUTER_API_KEY` |

---

## 5. LÍMITES HONESTOS

1. **Modelo por defecto:** `openrouter/openai/gpt-4o-mini` (pago, baratísimo). Cambiarlo es **una línea** en `.env` (`MODEL=openrouter/...`). Los modelos `:free` existen pero son inestables.
2. **Computadora Docker** no habilitada → si el modelo intenta usarla, recibe "Computer is not configured" (comportamiento esperado, no fallo del gateway).
3. **Voz y avatar** aún no existen (Fases 3 y 8 del roadmap).
4. El proceso se levanta a mano en pruebas (systemd pendiente).

---

## 6. ESTADO Y PENDIENTES

- ✅ **Fase 0** — clone + build (276 tests).
- ✅ **Fase 1** — persistencia propia; servicio cerrado arrancado.
- ✅ **Fase 2** — **gateway OpenRouter** operativo con modelo real.
- ⏳ **Fase 3** — Voz: **VoiceBox (TTS/STT/persona) + Pipecat (barge-in)**.
- ⏳ Endurecer operación (systemd) + rotación de credenciales.
- ⏳ Reporte para auditoría de **Beru**.

---

## 7. VEREDICTO DEL COMANDANTE

NEREUS **piensa**. Ya no hay que pelear con proveedores dispersos ni con la clave cerrada: **una sola puerta (OpenRouter)** sirve al chat y a las tareas. El camino queda allanado para la voz. Cadencia sostenida: **tres fases en dos jornadas**.

> **Recomendación:** autorizar **Fase 3 — Voz (VoiceBox + Pipecat)**.

**Fin del informe de Fase 2.** Listo para auditoría de Beru.
