# INFORME DE INTELIGENCIA: "Agnes" — Repo de Generación de Video y Alternativas

**Fecha:** 2026-09-30 · **Sesión:** Investigación · **Clasificación:** Uso Interno — Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Método:** GitHub Search API + Repos API + lectura directa de README/MODEL_CATALOG/LICENSE
**Parámetros del Monarca aplicados:** ① Licencia **MIT** (innegociable) · ② **≥1000★** · ③ **Deployable como sitio web** · ④ **Antigüedad ≥6 meses**

---

## 0. RESUMEN EJECUTIVO

**"Agnes" NO es un repo, es una PLATAFORMA.** Agnes AI es una pasarela de APIs multimodales (texto/imagen/video) **gratuita y compatible con OpenAI**, operada por Sapiens AI. El repo de generación de video que el Monarca busca es **`lcy362/agnes-video-generator`** — una app self-hosted (MIT) que **consume los modelos gratuitos de Agnes AI**.

**⚠️ Veredicto de cumplimiento:** ese repo **NO cumple tus parámetros** — tiene **454★** (menor a 1000) y **~3,5 meses** de antigüedad (menor a 6 meses). Sí es MIT y sí es web-deployable. Se detalla abajo, junto con **alternativas que SÍ cumplen** las 4 condiciones.

---

## 1. CONTEXTO — QUÉ ES "AGNES AI"

| Dato | Valor |
|------|-------|
| Qué es | Pasarela de IA **multimodal** (texto, imagen, video) vía API única OpenAI-compatible |
| Empresa | Agnes AI / Sapiens AI (fundador: Bruce Yang) |
| Sitios | `agnes-ai.com` (internacional) · `agnes-ai.cn` (China) |
| API base | `https://apihub.agnes-ai.com/v1` |
| Precio | **Gratis** (con límites de rate) |
| Modelos de video | `agnes-video-v2.0` (`POST /v1/videos`): text-to-video, image-to-video, multi-imagen, keyframe animation, generación asíncrona (poll por `video_id`) |
| Modelos de texto | `agnes-1.5-flash` (256K ctx), `agnes-2.0-flash` (256K), `agnes-2.5-flash` (512K) |
| Licencia de la plataforma | **No es open source** — es un servicio cerrado; solo el *cliente* puede ser MIT |
| Límites (referencia) | Texto ~30 RPM; imagen 20-30 RPM; video por RPM; **los valores cambian y no son contractuales** |

**Traducción táctica:** Agnes = un "proveedor de modelos gratis" al estilo OpenRouter, con modelos propios. El cómputo corre **en la nube de Agnes**, no en tu máquina.

---

## 2. EL REPO SOLICITADO — `lcy362/agnes-video-generator`

### 2.1 Ficha técnica
| Dato | Valor |
|------|-------|
| Nombre | Agnes Video Generator |
| Estrellas | **454★** · 146 forks |
| Licencia | **MIT** ✅ |
| Lenguaje | Python |
| Creado | **2026-06-12** (~3,5 meses) ❌ |
| Último push | 2026-09-29 (activo) |
| Web-deployable | ✅ **Sí** — web app self-hosted (homepage `video.lichuanyang.top`); instalación por `start.sh`, **Docker**, `npx free-short-video` o asistida por agente |
| Autor | SandGrid / lcy362 |

### 2.2 Qué hace (características completas)
- **Generación de video multi-escena desde texto**: escribes una idea → el sistema crea guion, escenas, narración y subtítulos, y compone el video final.
- **Modos:** Creative Video (sin narración / con narración TTS), **Manuscript Video** (pegar un artículo largo → auto-segmentar → video por segmento), text-to-video, **image-to-video**, **keyframes animation** (encadenado de keyframes), **digital anchor** (presentador digital).
- **TTS (narración) gratis e integrado** + **subtítulos automáticos** a nivel de palabra (SRT).
- **Resolución:** 9:16 / 16:9 / 1:1. **Sin marca de agua.**
- **Duración:** hasta **20 s por clip**, escenas ilimitadas; **sin límite de uso** (rate ~16 req/min).
- **Sin GPU local** (todo el cómputo en la nube de Agnes).
- **Multi-clave:** `AGNES_API_KEY`, `_2`, `_3`… rotación automática en `429`, escala el límite.
- **Checkpoint resume** (reanudar generación interrumpida).
- **UI web multilingüe**.
- Config por variables de entorno (`.env`). API REST (progreso por **polling**, sin WebSocket).
- **Proyecto hermano:** FreeShortVideoStudio (`lcy362/free-short-video-studio`, 26★, MIT) — versión 100% en navegador.

### 2.3 Requisitos para usarlo
1. **Una API key gratuita de Agnes AI** (obligatoria — sin ella no genera nada).
2. Python (o Docker) y un PC normal.

### 2.4 ✅/❌ Cumplimiento de tus parámetros
| Parámetro | ¿Cumple? |
|-----------|----------|
| Licencia MIT | ✅ Sí |
| ≥1000★ | ❌ **No** (454★) |
| Web-deployable | ✅ Sí |
| Antigüedad ≥6 meses | ❌ **No** (~3,5 meses) |

**Resultado: 2 de 4. NO cumple tus parámetros.**

---

## 3. ECOSISTEMA AGNES (otros repos del entorno)

| Repo | ★ | Lic. | Qué es |
|------|---|------|--------|
| `AgnesAI-Labs/AgnesAI-Models` | 5.184 | **sin licencia** ❌ | Gateway/catálogo oficial (no es app de video) |
| `Yacey/agnes-ai-generation-skill` | 420 | MIT | Skill de agente para APIs Agnes (texto/imagen/video) |
| `kangarooking/agnes-free-model-skills` | 198 | MIT | Skills Codex para modelos gratis de Agnes |
| `NicholasCone/agnes-ai-video-suite` | 128 | sin licencia | Suite de video (text to multi-scene) |
| `16nic/comfyui-agnes-ai` | 88 | MIT | Nodos ComfyUI para Agnes |
| `LGQLIFE/agnes-ai-studio` | 55 | MIT | Web UI texto→imagen/video |
| `LingyunStudio/AgnesStudio` | 51 | MIT | Genera imagen/video con Agnes |
| `1038lab/ComfyUI-Agnes-AI` | 39 | **GPL-3.0** ❌ | Nodos ComfyUI |
| `easyeye163/vimax-agnes` | 33 | MIT | ViMax potenciado por Agnes |
| `lcy362/free-short-video-studio` | 26 | MIT | Video en navegador, sin instalar |

**Ninguno de la familia Agnes cumple tus 4 parámetros** (o están por debajo de 1000★, o no tienen licencia MIT declarada).

---

## 4. ALTERNATIVAS QUE SÍ CUMPLEN TUS PARÁMETROS (MIT + ≥1000★ + web + ≥6 meses)

Verificadas contra GitHub API. Estas son **de verdad** MIT puras, con tracción y web-deployables.

| Repo | ★ | Lic. | Creado | Leng. | Web | Para qué |
|------|---|------|--------|-------|-----|----------|
| **harry0703/MoneyPrinterTurbo** | **126.9k** | MIT | 2024-03 | Python | ✅ WebUI | **Texto → video corto HD** (la mejor alternativa directa a Agnes). Guion+material+subtítulos+música. |
| **Anil-matcha/Open-Generative-AI** | 29.4k | MIT | 2023-05 | JS | ✅ Web app | Estudio **imagen+video**, 600+ modelos, self-hosted |
| **HKUDS/ViMax** | 12.5k | MIT | 2025-03 | Python | ✅ App/API | **Video agéntico** (director+guionista+productor) |
| **mudler/LocalAI** | 49.3k | MIT | 2023-03 | Go | ✅ WebUI+API | Motor local (imagen/video/LLM), API OpenAI-compatible |
| **zhouxiaoka/autoclip** | 9.0k | MIT | 2025-07 | Python | ✅ Web app | Clipping + highlights automáticos |
| **leejet/stable-diffusion.cpp** | 7.5k | MIT | 2023-08 | C++ | ✅ Server+UI | Difusión en C++ (SD, **Flux, Wan, Qwen**, vídeo) |
| **modelscope/FunClip** | 6.4k | MIT | 2023-05 | Python | ✅ Gradio | Corte de video por texto (ASR) |
| **Anil-matcha/AI-Youtube-Shorts-Generator** | 5.2k | MIT | 2024-06 | Python | ✅ Web app | YouTube largo → shorts 9:16 |

**Mejor alternativa directa a Agnes (para generar video desde texto):** ⭐ **MoneyPrinterTurbo** (126.9k★, MIT) — misma promesa, 280× más tracción y 2,5 años de madurez.

---

## 5. RECOMENDACIÓN TÁCTICA

1. **Si el objetivo es "generar video desde texto, gratis, self-hosted":** usar **MoneyPrinterTurbo** — cumple tus 4 parámetros y es el más maduro del mercado.
2. **Agnes Video Generator:** solo como **referencia de UX** (modos Creative/Manuscript, digital anchor, keyframes) — no como base de producto: 454★, 3,5 meses, y **depende 100% de un servicio gratuito externo**.
3. **Nunca** basar un producto en Agnes sin contrato: la plataforma es cerrada, sus límites "cambian y no son contractuales", y su viabilidad depende de que sigan regalando cómputo.

---

## 6. RIESGOS

| Riesgo | Detalle |
|--------|---------|
| **Dependencia externa** | Agnes es un servicio **gratuito y cerrado**; si cambia el precio o cierra, el repo cliente queda inútil |
| **Licencia** | El gateway oficial **no declara licencia** → no apto para uso comercial limpio |
| **Madurez** | El repo de video tiene 3,5 meses y 454★ → sin verificación independiente |
| **Calidad del modelo** | El propio README admite: *"el modelo de video de Agnes no es perfecto aún; fotogramas inestables, acciones complejas se deforman"* |
| **Monetización del sitio** | Pide desactivar el ad-blocker y clicar anuncios → modelo de supervivencia frágil |
| **Rate limits** | Valores "de referencia", no contractuales; con 1 sola key el límite es bajo |

---

## 7. FUENTES

- GitHub Search/Repos API — consultas "agnes", "agnes video", "agnes ai" (2026-09-30)
- `lcy362/agnes-video-generator` README + metadata (2026-09-30)
- `AgnesAI-Labs/AgnesAI-Models` README + `MODEL_CATALOG.md` (2026-09-30)
- sitios oficiales: agnes-ai.com, wiki.agnes-ai.com, news.ycombinator.com

**Fin del informe.** Listo para auditoría de Beru y archivo en `diario-de-sombras/`.
