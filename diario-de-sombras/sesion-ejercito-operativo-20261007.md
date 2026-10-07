# DIARIO DE SESIÓN — EJÉRCITO DE SOMBRAS: OPERATIVO
## Segunda misión de alta prioridad — cumplida

**Fecha:** 2026-10-07 · **Elaborado por:** Bellion, Gran Comandante
**Orden del Monarca:** *"deje al resto de sombras completamente operativas… las sombras hiperespecializadas
y letales que siempre he querido… el modelo más idóneo por especialidad con fallback en cada una"*
**Veredicto de Beru (v2):** **EJÉRCITO OPERATIVO** (4/4 criterios, 10/10 en cada uno)

---

## 1. DIAGNÓSTICO QUE ENCONTRÉ (el ejército nunca pudo estar de pie)

1. **OmniRoute caído** (`localhost:20128` sin respuesta). Era el endpoint único de 9 de 10 sombras →
   su caída las tumbaba a todas. *(El Monarca ordenó después olvidarlo por completo.)*
2. **8 de 10 sombras con el MODELO CORRUPTO:** el campo del modelo contenía el **texto del rol**
   (`Beru -Supervision - Report`, `Tank -Ventas`, `Jima -Automatizacion`…). Esas 8 no podían arrancar NUNCA.
3. **Las 10 compartían el bot de Telegram del perfil `default`** (en su `.env`) → el gateway multiplexado
   se niega a levantarlas.

---

## 2. LO HECHO

### 2.1 Souls forjados (10/10)
`SOUL.md` reescrito en cada perfil (2.297–3.741 chars), con: identidad filosa, método propio de la
especialidad, **estándar de entrega exacto** (Igris: metas de 155 chars contadas; Tusk: CSV
`Keyword|LSI_×5|Volume|CPC|Difficulty|Intent`; Titan: JSON que serializa) y **Protocolo del Ejército**
(evidencia o no existe, español, solo tu especialidad, bestias proscritas, no delatar que es IA).
Respaldos: `SOUL.md.bak-20261007-*`.

### 2.2 Configs rearmadas (10/10) — OpenRouter directo, sin OmniRoute, sin Telegram
- `model.default` = **ID real verificado** contra el catálogo vivo.
- `fallback_providers` = **2 respaldos** por sombra (línea ~227 del YAML).
- Fuera el bloque `providers[omni]` (OmniRoute/unorouter).
- Fuera Telegram del `config.yaml` **y del `.env`** (4 variables por sombra).
- `timezone: America/Bogota` (estaba `(GMT-5)`, que no es zona IANA válida → warning en cada arranque).
- Respaldos: `config.yaml.bak-pre-army-*`, `.env.bak-pre-army-*`.

| Sombra | Primario | Respaldo 1 | Respaldo 2 |
|---|---|---|---|
| igris | `deepseek/deepseek-v4-flash-0731` | `qwen/qwen3.7-flash` | `minimax/minimax-m3` |
| tank | `qwen/qwen3.7-flash` | `qwen/qwen3.5-plus-02-15` | `minimax/minimax-m2.7` |
| greed | `bytedance-seed/seed-1.6-flash` | `z-ai/glm-5.3-flash` | `google/gemma-4-31b-it` |
| iron | `deepseek/deepseek-v4-flash-0731` | `qwen/qwen3.7-flash` | `minimax/minimax-m2.7` |
| tusk | `qwen/qwen3.7-flash` | `z-ai/glm-5.3-flash` | `qwen/qwen3.5-plus-02-15` |
| kamish | `z-ai/glm-5.3-flash` | `google/gemma-4-31b-it` | `minimax/minimax-m2.7` |
| kaisel | `qwen/qwen3-coder-30b-a3b-instruct` | `poolside/laguna-s-2.1:free` | `z-ai/glm-5.2` |
| titan | `qwen/qwen3-vl-32b-instruct` | `google/gemma-4-31b-it` | `minimax/minimax-m3` |
| jima | `qwen/qwen3-30b-a3b-instruct-2507` | `deepseek/deepseek-v4-flash-0731` | `minimax/minimax-m3` |
| beru | `deepseek/deepseek-v4-pro` | `z-ai/glm-5.3-flash` | `nvidia/nemotron-3-ultra-550b-a55b:free` |

### 2.3 Prueba de combate (10/10 PASA)
Una misión real por sombra en SU propio perfil (`hermes -p <sombra> chat -q …`): cada una **respondió
y usó herramientas** (dejó `intel/estado-sombras/<sombra>.txt` con `OPERATIVO <sombra>`).
Evidencia: `intel/combate-logs/*.log` + `intel/estado-sombras/*.txt`.

### 2.4 Auditoría de Beru — y el hallazgo de la auditoría
- **v1: NO PASA (2 falsos negativos).** Reportó “fallback_providers no existe” (estaba en la línea 227 de
  230) y “credenciales Telegram activas en los 10” (era el **comentario** `# TELEGRAM INTEGRATION`).
- **Lección reforzada en su SOUL:** un comentario no es configuración; leer el archivo COMPLETO;
  cada veredicto lleva comando + salida; si no se puede probar → “NO VERIFICADO”, no “NO PASA”.
- **v2: EJÉRCITO OPERATIVO** (4/4 criterios, 10/10). Reporte: `intel/auditoria-ejercito-20261007-v2.md`.

---

## 3. INTELIGENCIA CRÍTICA: LA CAPA GRATIS DE OPENROUTER NO ES CONFIABLE

Screening real de los **15 únicos `:free` con `tools=True`** del catálogo:

| Modelo :free | Resultado real |
|---|---|
| `poolside/laguna-s-2.1:free` | ✅ contenido + tool call (el único plenamente apto) |
| `apodex/…`, `nvidia/nemotron-3-super-120b:free`, `inclusionai/ling-3.0-flash-sante:free`, `cohere/north-mini-code:free` | ⚠️ llaman la herramienta pero **sin texto** |
| `dots-studio/dots-3-note-preview:free` | ❌ **vacío** |
| `thinkingmachines/inkling:free`, `inkling-small:free` | ❌ **HTTP 403** |
| `google/gemma-4-31b-it:free`, `gemma-4-26b-a4b-it:free` | ❌ **HTTP 429 en la primera llamada** |

Además, **4 IDs de la doctrina ya no existen** (`z-ai/glm-5.2:free`, `minimax/minimax-m3:free`).
**Conclusión (con el "no me importa cuánto me cueste" del Monarca):** primario = modelo **barato y
confiable** de pago por token (≈$0.018–0.30/1M); el `:free` entra **solo donde se verificó apto**.
Costo estimado de la flota: **≈$1–3/mes** con los primarios actuales.

---

## 4. GOTCHAS DUROS DE HOY
1. **Los secretos de mensajería de un perfil viven en `profiles/<s>/.env`, NO en su `config.yaml`.**
   Purgar solo el YAML deja la credencial y la advertencia.
2. **`(GMT-5)` no es zona IANA válida** → `timezone: America/Bogota`.
3. **Lanzar 10 `hermes -p` en bucle desde un script Python de Windows revienta con `rc=0xC0000142`**
   (STATUS_DLL_INIT_FAILED) a partir del segundo. Lanzarlas **de a una desde bash** funciona; y nunca
   editar los `.env`/configs **mientras** corre una prueba (esa colisión tumbó 9 de 10 en el primer intento).
4. **`yaml` no está en el python local:** usar `uv run --with pyyaml python script.py`.
5. **Un auditor también se equivoca:** un falso NO PASA cuesta igual que un falso PASA.

---

## 5. ESTADO Y PENDIENTES
- **Ejército: OPERATIVO** (10/10). Sombras **sueltas de Telegram** (el cuarto de guerra se armará desde cero, con calma).
- **Modelo:** cada sombra con primario OpenRouter + 2 respaldos.
- **Pruebas del Seawolf Agent PAUSADAS** por orden del Monarca hasta que el ejército esté de pie → **ya lo está**;
  el bus (101 eventos) sigue intacto y esperando.
- **Pendiente:** cuarto de guerra en Telegram desde cero; `timezone (GMT-5)` del perfil global (default/Bellion)
  por corregir; decidir si se sube el bus a su propio directorio (no exponer `filtro.env` al sandbox).

> *"Seawolf Studio acelera por 10x cuando el ejército camina solo."* 🐺
