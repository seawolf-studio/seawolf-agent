# CONCLUSIONES — Smart Web «Club Deportivo Wonder's» (misión pausada)

> Extraídas por Bellion al pausar el proyecto (2026-10-10). Sirven para todo el portafolio «Smart Web».

## 1. Elección de modelo OpenRouter para negocios locales

**Hallazgo:** el volumen es tan bajo (≈40 chats/día ≈ 4.800 req/mes) que **el costo del modelo es
irrelevante** frente al riesgo de calidad. Barrido del catálogo vivo (escenario: 1.000 tok in + 200 tok
out por request):

| Modelo | $/1M in | $/1M out | Ctx | USD/mes | Veredicto |
|---|---|---|---|---|---|
| inclusionai/ling-3.0-flash | 0.021 | 0.063 | 262k | 0.16 | fondo; español flojo |
| qwen/qwen3.7-flash | 0.030 | 0.130 | 1M | 0.27 | ala económica |
| **google/gemini-2.5-flash-lite** | 0.100 | 0.400 | 1M | **0.86** | **default idóneo** |
| anthropic/claude-haiku-5.5 | 0.100 | 0.500 | 1M | 0.96 | alternativa prima |
| qwen/qwen3.8-flash | 0.150 | 0.470 | 1M | 1.17 | calidad/precio |
| deepseek/deepseek-v4-flash | 0.030 | 1.280 | 1M | 1.37 | entrada barata, salida carísima |
| google/gemini-2.5-flash | 0.300 | 2.500 | 1M | 3.84 | potencia |

**Regla:** elegir **calidad**, no precio. La tríada por defecto:
- **Núcleo:** `google/gemini-2.5-flash-lite` (~$0.86/mes)
- **Económico:** `qwen/qwen3.7-flash` (~$0.27/mes)
- **Potencia:** `google/gemini-2.5-flash` (~$3.84/mes)

**La palanca real de costo es el CONTEXTO, no el modelo.** Recortar historial (últimos ~12 mensajes),
system-prompt conciso y `max_tokens` acotado ahorran más que cambiar de flash.

**Prohibido en producción:** modelos `:free`/`:batch` y modelos de razonamiento (gastan todo el
presupuesto de tokens en el canal de razonamiento → respuestas vacías). Si se usa uno con razonamiento,
enviar `reasoning.enabled=false`.

## 2. Doctrina de producto «Smart Web» (estándar del estudio)

- Una **sola pieza** (HTML+CSS+JS); multipágina por **router hash** cuando el cliente pide subpáginas.
- **Tema oscuro por defecto** + claro.
- **Un formulario por subpágina** → correo del cliente (sin backend ni claves).
- **IA embebida** con la clave **server-side** (Cloudflare Worker), nunca en el navegador.
- **Contenido visible sin JS** (no depender solo de animaciones).
- Costo objetivo del modelo: **< $2/mes** por cliente a volumen local.

## 3. Lecciones de proceso (para la orquestación)

1. **Verificación propia > auditoría de código fuente.** BERU dio 10/10 leyendo el código, pero el fallo
   real (contenido invisible sin JS) solo apareció **al renderizar**. Siempre renderizar, no solo auditar fuente.
2. **Un modelo coder pequeño (30B) se atasca** con una pieza grande y única. Re-desplegar con un modelo
   fuerte (Sonnet) + instrucción «una sola pasada, sin execute_code» resolvió.
3. **Headless no dispara IntersectionObserver** bajo tiempo virtual → verificar con `--disable-javascript`.
4. **La visión da falsos positivos** en mayúsculas con letter-spacing (reportó typos inexistentes). Confirmar
   con grep contra la fuente antes de «corregir».
5. **Logo del cliente en JPEG con fondo negro → PNG transparente** (ffmpeg `colorkey`); no fiarse del
   `mix-blend-mode` dentro de contextos animados.
6. **La pausa es una victoria de proyecto,** no un fracaso: mejor retomar cuando el cliente respira que
   forzar una entrega que abruma.
