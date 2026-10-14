# INFORME DE TEMA: Comparativa DeepSeek V4.1 Flash vs Qwen3.8 Flash
## + Ahorros aplicados · **v2 CORREGIDA**

**Fecha:** 2026-10-14 · **Clasificación:** Uso Interno — Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Fuente:** OpenRouter API (`/api/v1/models` y `/models/{id}/endpoints`) — 2026-10-14.

> ⚠️ **CORRECCIÓN v2:** la v1 traía precios erróneos de DeepSeek ($0.15/$0.60, caché $0.003) y un **"precio pico 2×" que NO existe** para este modelo. El "pico" pertenece a **otro** modelo (`deepseek/deepseek-v4-pro-0813`), no a V4.1 Flash. Error mío, corregido con los datos reales de abajo.

---

## 1. AHORROS APLICADOS (hecho, no recomendación)

| Acción | Estado |
|--------|--------|
| **Skill `caveman`** (recorte de output) | ✅ Activa (full) — recorta ~40–65% del output |
| **Caché de prompt** (`cache_ttl: 5m`) | ✅ Activa y trabajando (32M leídos medidos) |
| **`display.interim_assistant_messages`: true → false** | ✅ Aplicado |
| **`compression.threshold`: 0.5 → 0.4** | ✅ Aplicado (comprime antes) |
| Backup config | ✅ `config.yaml.bak-*` |

Vía: `hermes config set` (el guardrail bloquea editar `config.yaml` directo). Efecto: **próxima sesión.**

---

## 2. COMPARATIVA (datos reales)

### 2.1 Precios (por 1M tokens, USD)
| Concepto | DeepSeek V4.1 Flash | Qwen3.8 Flash | Ganador |
|----------|---------------------|---------------|---------|
| **Input** | **$0.01584** | $0.15 | **DeepSeek (~9,5× más barato)** |
| **Output** | $0.891 | **$0.47** | **Qwen (−47%)** |
| **Cache read** | **$0.0054** | $0.016 | **DeepSeek (~3×)** |
| **Precio pico** | ❌ **NO TIENE** (plano 24/7) | ❌ NO TIENE (plano) | Empate |

### 2.2 Capacidades técnicas
| Capacidad | DeepSeek V4.1 Flash | Qwen3.8 Flash | Ventaja |
|-----------|---------------------|---------------|---------|
| **Contexto** | **1.048.576** | 1.000.000 | ~Empate |
| **Salida máxima** | **393.216** (hasta 943.718 en endpoint OpenInference) | 131.072 | **DeepSeek (3–7×)** |
| **Entrada** | text + image | text + image + **video** | **Qwen** |
| **Razonamiento** | ✅ + **`reasoning_effort`** | ✅ (sin control) | **DeepSeek** |
| **Tools / structured** | ✅ / ✅ | ✅ / ✅ | Empate |
| **Arquitectura** | MoE sparse **CED**; activa 8B input / 16B output | MoE multimodal | — |
| **Quantización** | fp4 (OpenInference) | n/d | — |
| **Params finos** | +logit_bias, min_p, repetition_penalty, reasoning_effort | — | **DeepSeek** |

### 2.3 Costo REAL para TU carga (medido: 3,5M in · 155k out · 32M cache)
| Modelo | Input | Cache-read | Output | **Total** |
|--------|-------|-----------|--------|-----------|
| **DeepSeek V4.1 Flash** | $0.055 | **$0.173** | $0.138 | **≈ $0.37** ✓ (medido $0.3586) |
| **Qwen3.8 Flash** | $0.525 | $0.512 | $0.073 | **≈ $1.11** |

→ Para sesiones largas con caché, **DeepSeek cuesta ~3× menos**. Clave: input y cache-read baratísimos.

---

## 3. VEREDICTO

**Mantener DeepSeek V4.1 Flash.** Es **~9,5× más barato en input** y **~3× en caché** que Qwen. Qwen3.8 Flash solo conviene si necesitas **entrada de video**, o en sesiones muy cortas con salida grande (output −47%).

---

## 4. EXTRA — variantes del mismo proveedor
| Modelo | Input /1M | Output /1M | Cache /1M | Nota |
|--------|-----------|-----------|-----------|------|
| `deepseek/deepseek-v4.1-flash` | $0.01584 | $0.891 | **$0.0054** | **Actual** |
| `deepseek/deepseek-v4-flash-0731` | $0.016 | $0.64 | $0.016 | Output más barato, caché más cara |
| `deepseek/deepseek-v4-pro-0813` | **tiene picos 2×** (L–V 01–04 y 06–10 UTC) | — | — | **Este SÍ tiene picos** (no lo usas) |

---

## 5. FUENTES
- OpenRouter API `/api/v1/models` + `/models/deepseek/deepseek-v4.1-flash/endpoints` — 2026-10-14.
- `state.db` de Hermes (uso real). Config activa.

**Fin del informe de tema (v2 corregida).**
