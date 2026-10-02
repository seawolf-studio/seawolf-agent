# INFORME DE TEMA: Réplica Open-Source de los Modos de Agnes (Creative · Manuscript · Digital Anchor)

**Fecha:** 2026-09-30 · **Clasificación:** Uso Interno — Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Objeto:** Determinar si las tres capacidades diferenciadoras de Agnes Video Generator pueden replicarse con software open-source de licencia permisiva. **Respuesta: SÍ, las tres.**
**Método:** verificación directa contra GitHub Repos API (licencia, estrellas, actividad) el 2026-09-30.

---

## 0. CONTEXTO — Qué se quiere replicar

Agnes Video Generator destaca por tres modos:
1. **Creative Video** — de una idea de texto a un **video multi-escena** con guion, imágenes/keyframes, narración TTS y subtítulos automáticos.
2. **Manuscript Video** — pegar un **artículo/texto largo** → segmentación automática → un video por segmento → narración y subtítulos unificados.
3. **Digital Anchor** — un **presentador digital** (personaje que lee el guion) incrustado en el video.

**Conclusión del informe:** los tres son **pipelines de orquestación** construibles con componentes open-source permisivos. Creative ya está resuelto por repos existentes; Manuscript es una variación trivial; Digital Anchor es el único que añade complejidad real (GPU + modelos de talking-head), pero con ruta abierta y limpia.

---

## 1. MODO CREATIVE — Réplica por componentes

| Etapa | Componente open-source | Licencia | Estado |
|-------|------------------------|----------|--------|
| 1. Idea → guion y desglose de escenas | LLM vía **OpenRouter** | servicio (pago/uso) | ✅ |
| 2. Imagen/keyframe por escena | SD/Flux vía **ComfyUI** *(GPL-3.0)* o **LocalAI** *(MIT)* / **stable-diffusion.cpp** *(MIT)* | mixta | ✅ |
| 3. Imagen→video / texto→video | **Wan2.2** · **CogVideo** · **Open-Sora** · **Mochi** | **Apache-2.0** | ✅ |
| 4. Encadenado de keyframes | Técnica estándar: **último fotograma de un clip → primer fotograma del siguiente** | — | ✅ |
| 5. Narración (TTS) | **Kokoro** (Apache-2.0) · **Piper** (MIT) · **VoiceBox** (MIT) | permisiva | ✅ |
| 6. Subtítulos a nivel de palabra | **faster-whisper** (timestamps) → SRT | MIT | ✅ |
| 7. Composición y “quemado” | **FFmpeg** | LGPL/GPL (herramienta) | ✅ |

**Dato clave:** este modo **ya está resuelto por `harry0703/MoneyPrinterTurbo`** (126.9k★, **MIT**, creado 2024-03, WebUI) — genera video corto con guion, material, TTS, subtítulos y música. **No hay que construirlo desde cero.**

---

## 2. MODO MANUSCRIPT — Réplica

**Es el mismo pipeline Creative con un paso delante.** No requiere tecnología nueva:
1. Un LLM (OpenRouter) **trocea** el artículo en segmentos coherentes.
2. Cada segmento entra al pipeline Creative (imagen/keyframe → video → TTS).
3. Se **unifican** narración y subtítulos y se compone el video final (FFmpeg).

**Veredicto:** trivial. Pura orquestación sobre los mismos componentes del modo Creative.

---

## 3. MODO DIGITAL ANCHOR — Réplica

Dos rutas, ambas abiertas:

### (a) Fotorrealista — foto + audio → presentador con labios sincronizados
| Herramienta | Licencia | ★ (verif.) |
|-------------|----------|-----------|
| **SadTalker** | Apache-2.0 | 14.1k |
| **LivePortrait** | **MIT** | 19.1k |
| **MuseTalk** | **MIT** | 6.6k |
| **EchoMimic v2** | Apache-2.0 | 4.6k |

### (b) Avatar estilizado (2D/3D) — más ligero y multiplataforma
- **Rive** (MIT) — state machine con acciones (idle/hablando).
- **VRM + three-vrm** (MIT) — avatar 3D diseñable.

**Veredicto:** replicable. La ruta fotorrealista exige **GPU** y tiene riesgo de "valle inquietante"; la estilizada es más segura para producto y multiplataforma.

---

## 4. COSTOS Y TRAMPAS (honestidad brutal)

1. **GPU = el costo real.** Agnes es gratis porque el cómputo corre en *su* nube. Nuestra réplica open-source **necesita GPU** para generar video (local o alquilada). Es el ~90% del coste operativo.
2. **Licencias de modelos de video — trampas a evitar:**
   - ✅ **Limpios (Apache-2.0):** Wan2.2, CogVideo, Open-Sora, Mochi, AnimateDiff, EchoMimic v2.
   - ⚠️ **Revisar antes de uso comercial:** **HunyuanVideo** (Licencia Comunitaria Tencent — **no es OSI**) y **LTX-Video** (el código es Apache-2.0, pero los **pesos** tienen licencia propia con tope de ingresos).
   - ⚠️ **ComfyUI es GPL-3.0** (copyleft) — usar **LocalAI / stable-diffusion.cpp (MIT)** si se quiere núcleo permisivo.
3. **Calidad:** los modelos abiertos de video han mejorado mucho pero no igualan aún a los propietarios de gama alta en estabilidad de fotogramas y acciones complejas.
4. **Digital anchor:** los modelos open (SadTalker/LivePortrait/MuseTalk) están por debajo de HeyGen/Synthesia en naturalidad.

---

## 5. STACK RECOMENDADO PARA REPLICAR LOS TRES MODOS

| Capa | Elección (permisiva) |
|------|----------------------|
| Orquestación / guion | OpenRouter (LLM) |
| Imagen/keyframe | LocalAI o stable-diffusion.cpp (MIT) |
| Video (t2v / i2v) | **Wan2.2** (Apache-2.0) |
| Keyframe chaining | Lógica propia (último→primer fotograma) |
| TTS | Kokoro / Piper / VoiceBox |
| Subtítulos | faster-whisper |
| Digital anchor | LivePortrait / MuseTalk (MIT) o Rive (estilizado) |
| Composición | FFmpeg |
| **Atajo probado** | **MoneyPrinterTurbo** (MIT) cubre Creative + base de Manuscript |

---

## 6. CONCLUSIÓN

**Los tres modos de Agnes son replicables íntegramente con licencias permisivas.** Creative y Manuscript son de bajo esfuerzo (y ya existen en un repo MIT con 127k★). Digital Anchor añade la única complejidad real (GPU + talking-head), con ruta open-source limpia. **El coste dominante no es el software, sino la GPU.**

---

## 7. FUENTES

- GitHub Repos API (licencia, estrellas, actividad) — verificación por repo, 2026-09-30.
- README de `lcy362/agnes-video-generator` y catálogo de modelos Agnes (`AgnesAI-Labs/AgnesAI-Models`).
- Informes previos de la sesión: `agnes-video-generacion-20260930.md`, `repos-github-imagen-video-20260929.md`.

**Fin del informe de tema.** Listo para auditoría de Beru y archivo en `diario-de-sombras/`.
