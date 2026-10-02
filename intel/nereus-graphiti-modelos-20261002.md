# INFORME — GRAPHITI CABLEADO + AUDITORÍA DE MODELOS (coste)
## Memoria temporal integrada y coste de IA reducido a casi cero

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. GRAPHITI → NEREUS (memoria temporal) — INTEGRADO Y VERIFICADO

| Pieza | Cambio |
|-------|--------|
| `apps/server/src/temporal.ts` | **NUEVO** — cliente MCP (Graphiti): `addEpisode` + `searchFacts`, con sesión y best-effort |
| `engine/conversation.ts` | `remember_fact` → añade episodio temporal |
| `engine/routes.ts` | `POST /memories` → añade episodio temporal |
| `engine/model.ts` | Los **hechos temporales** entran al contexto de tareas (`temporalFacts`) |
| `.env` | `GRAPHITI_MCP_URL` |

**Verificación real:** memoria creada por NEREUS → episodio **presente en el grafo** (grupo `local-user`, con fecha) vía `get_episodes`. `typecheck` + `build` ✅ · servicio `active`.

## 2. AUDITORÍA DE MODELOS (anti-gasto)

### Precios reales (OpenRouter, USD por 1M tokens)
| Modelo | Tools | Entrada | Salida |
|--------|:---:|---:|---:|
| `nvidia/nemotron-3-super-120b-a12b:free` | ✅ | **0** | **0** |
| `qwen/qwen3.8-27b:free` | ✅ | **0** | **0** |
| `deepseek/deepseek-v4-flash` | ✅ | 0,028 | **0,056** |
| `deepseek/deepseek-v4.1-flash` | ✅ | 0,020 | 0,600 |
| `deepseek/deepseek-v4.1-flash:batch` | ✅ | 0,112 | 0,336 |
| `ibm-granite/granite-4.0-h-micro` | ❌ | 0,017 | 0,112 |

### ⚠️ Hallazgo sobre el `:batch`
Los modelos `:batch` son **asíncronos** (procesan por lotes con retraso) → **NO sirven para chat en vivo**; solo para trabajos de fondo. Además, en este caso su **entrada es más cara** que la versión en vivo.

### Cambios aplicados
| Servicio | Antes | Ahora | Coste |
|----------|-------|-------|-------|
| **NEREUS (chat)** | `openai/gpt-4o-mini` | **`nvidia/nemotron-3-super-120b-a12b:free`** | **Gratis** |
| **Mem0 (extracción)** | `openai/gpt-4o-mini` | **`deepseek/deepseek-v4-flash`** | ~0,03/1M |
| **Graphiti (extracción)** | `openai/gpt-4o-mini` | **`deepseek/deepseek-v4-flash`** | ~0,03/1M |
| Embeddings | `text-embedding-3-small` | (igual) | muy bajo |

*Fallback documentado en `.env`: `openrouter/deepseek/deepseek-v4-flash` si el gratis da límite.*

## 3. VERIFICACIÓN TRAS EL CAMBIO
- **Mem0** con modelo barato: alta correcta (`ADD`).
- **NEREUS chat** con modelo **gratis**: respuesta real *"Sí, estoy funcionando con el modelo gratuito."* en **7 s**, **sin errores ni 429**.
- Servicios: `nereus-api` activo, Mem0 y Graphiti arriba.

## 4. ESTADO
- ✅ **Fase 4 completa**: Mem0 (semántica) + Graphiti (temporal) integrados en el agente y probados.
- ✅ Coste de IA del sistema reducido a **gratis / casi gratis**.
- ⏳ systemd para los servicios nuevos (Mem0, Graphiti) — pendiente.
- ⏳ Pruebas integrales.

## 5. VEREDICTO DEL COMANDANTE
NEREUS **recuerda por significado y en el tiempo**, y ya **no sangra créditos**: chat gratis, fondo a céntimos. Blindado el bolsillo del Monarca y avanzada la memoria al completo.

**Fin del informe.**
