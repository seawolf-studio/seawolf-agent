# INFORME DE EJECUCIÓN — FASE 3 "SEAWOLF NEREUS" (voz)
## Clonación de la voz de marca + medición de rendimiento

**Fecha:** 2026-10-01 → 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Resultado:** ✅ **Voz de marca masculina CLONADA** en VoiceBox y generando audio real. ⚠️ Confirmado con datos que **la clonación es inviable en vivo en el VPS CPU** (necesita GPU).

---

## 1. LO QUE SE HIZO
1. **Muestras del Monarca** (`VOZ 1.m4a`, `VOZ 4.m4a`) recibidas, convertidas a WAV mono 24 kHz.
2. **Normalización** de volumen (`loudnorm -16 LUFS`): la muestra 2 salía demasiado baja y el motor la rechazaba ("too quiet or silent").
3. **Transcripción** de cada muestra con el Whisper interno de VoiceBox (campo multipart `file`).
4. **Perfil clonado "NEREUS"** creado (`voice_type=cloned`, motor `qwen`), con **3 muestras** adjuntas.

## 2. APRENDIZAJES TÉCNICOS (pitfalls reales)
- **Motor de clonación = `qwen`**, no `qwen3-tts` (ese id solo vale para presets). El backend restringe: `CLONING_ENGINES = {qwen, luxtts, chatterbox, chatterbox_turbo, tada}`.
- **La API de muestras exige `file` + `reference_text`** (multipart). Sin transcripción, se usa un texto de relleno.
- **El motor rechaza audio bajo** → hay que normalizar antes de subir.

## 3. RENDIMIENTO MEDIDO (lo crítico)
| Motor | Uso | Latencia real (2 vCPU) | Veredicto |
|-------|-----|------------------------|-----------|
| **Kokoro** (preset) | Voz genérica ES | **~4 s** / 6.7 s audio | ✅ Usable (notas) |
| **Qwen3-TTS 1.7B** (clonado) | Tu voz | **OOM kill** (>6 GB) | ❌ No cabe |
| **Qwen3-TTS 0.6B** (clonado) | Tu voz | **~162 s** / 7.2 s audio | ❌ Inviable en vivo |

- OOM confirmado por `oom-killer` del kernel (anon-rss 6.1 GB).
- Con 0.6B el pico de memoria baja a **4.6/6 GB** y la clonación **funciona**, pero la síntesis en CPU es ~22× tiempo real.

## 4. CONCLUSIÓN
- **Voz de marca masculina: REGISTRADA** (clonada de muestra del Monarca, de origen de dominio público).
- **Presets ES (Kokoro):** `em_alex` (masc.), `ef_dora` (fem.) → operativos en CPU.
- **Clonación en vivo en el VPS actual: NO viable.** Para conversación fluida con la voz clonada se requiere **nodo GPU** (opción B) o **TTS en cliente** (opción C).
- La clonación sigue siendo válida para **generación por lotes / notas de voz** (no interactivo).

## 5. PENDIENTES
- ⏳ Decisión del Monarca: **GPU dedicada** vs. **TTS en cliente** vs. seguir con **Pipecat** en CPU.
- ⏳ **Voz femenina oficial** (preset Kokoro o clonar referencia con derechos).
- ⏳ **Advertencias de clonación** de usuario (legal/consentimiento).
- ⏳ **Pipecat (barge-in)** e integración MCP con NEREUS.
- ⏳ Ajustar el límite de memoria del contenedor según la decisión.

## 6. VEREDICTO DEL COMANDANTE
**Tu voz ya vive en NEREUS.** El clon es real y reproducible. El muro ya no es de software — es de **hierro**: sin GPU, la voz clonada habla en cámara lenta. Decisión con números, no con corazonadas.

**Fin del informe de Fase 3 (voz).**
