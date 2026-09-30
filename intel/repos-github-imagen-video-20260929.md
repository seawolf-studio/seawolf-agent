# Informe de Inteligencia: Repos GitHub — Generación de Imagen y Video (Web-Deployable)
**Fecha:** 2026-09-29 | **Sesión:** Investigación | **Clasificación:** Uso Interno - Seawolf Studio
**Método:** GitHub Search API (consultas verificadas contra `api.github.com`, no scraping web)
**Descripciones:** extraídas de la descripción oficial + README de cada repositorio (fuente directa, no memoria)

---

## Resumen Ejecutivo

Se ejecutaron **12 consultas directas contra la API de GitHub** con los 4 criterios duros del Monarca. Resultado: **16 repos verificados** que cumplen los 4 filtros simultáneamente (MIT + >1000★ + web-deployable + antigüedad ≥6 meses).

**Hallazgo crítico:** Los repos más famosos de generación de imagen/video **NO califican** por licencia. ComfyUI, Fooocus y A1111 son GPL/AGPL; InvokeAI es Apache-2.0. La regla MIT descarta al 90% de los "obvios" — lo que deja un espacio menos competido y **más seguro para uso comercial**. Eso es una ventaja, no un problema.

---

## Metodología de Filtrado (reutilizable para futuras búsquedas)

Endpoint base usado:
```
https://api.github.com/search/repositories?q=<tema>+license:mit+stars:%3E1000+created:%3C2026-03-01&sort=stars&order=desc&per_page=20
```
Filtros aplicados = tus 4 criterios:
1. **`license:mit`** → solo MIT (innegociable)
2. **`stars:>1000`** → tracción real
3. **`created:<2026-03-01`** → antigüedad mínima ~6 meses (excluye repos recién salidos)
4. **Criterio web-deployable** → verificación manual de lenguaje/topics/README: se exige UI web o servidor (no librería suelta)

Verificación adicional por repo: `GET /repos/{owner}/{repo}` → licencia exacta, fechas, forks, issues, homepage.

---

## 🎬 CATEGORÍA 1 — Generación / Edición de VIDEO

### 1. harry0703/MoneyPrinterTurbo · 126.9k★ · MIT · 2024-03 · Python
**Qué hace:** Herramienta *todo-en-uno* de generación de videos cortos. Le das un **tema o palabra clave** y genera automáticamente: guion del video, búsqueda de material (clips de stock), generación de subtítulos, música de fondo y composición final en **video HD** (formato shorts/reels). Pensada para producir contenido vertical para redes sin edición manual.
**Web-deployable:** Sí — incluye WebUI (Streamlit) + API REST. Corre en Windows/macOS/Linux.
**Despliegue:** El más probado y con más tracción del listado (126k★, 2.5 años, push activo).

### 2. HKUDS/ViMax · 12.5k★ · MIT · 2025-03 · Python
**Qué hace:** Generación de video **agéntica** — un pipeline multi-agente donde distintos agentes AI actúan como **Director, Guionista, Productor y Generador de Video**, todo en uno. Convierte una idea en un video estructurado pasando por las fases de preproducción y producción de forma automatizada.
**Web-deployable:** Sí — app + API.
**Despliegue:** Investigación de HKUDS (Universidad de Hong Kong), 18 meses de antigüedad.

### 3. zhouxiaoka/autoclip · 9.0k★ · MIT · 2025-07 · Python
**Qué hace:** Herramienta de **clipping inteligente con IA**. Importas un video largo, la IA analiza los subtítulos, **identifica los fragmentos destacados** y los recorta automáticamente en clips cortos y colecciones. Ideal para reutilizar contenido largo → shorts.
**Web-deployable:** Sí — app de escritorio con frontend web (Tauri).
**Despliegue:** 14 meses de antigüedad, push activo y en GitHub Trending.

### 4. modelscope/FunClip · 6.4k★ · MIT · 2023-05 · Python
**Qué hace:** Herramienta de corte de video **precisa por texto**. Impulsada por FunASR (reconocimiento de voz), transcribe el video, genera subtítulos y permite **editar/recortar el video seleccionando frases del texto** — incluida edición asistida por LLM.
**Web-deployable:** Sí — **UI local con Gradio** (fácil de levantar como web).
**Despliegue:** 3 años de antigüedad. Proyecto oficial de ModelScope (Alibaba).

### 5. Anil-matcha/AI-Youtube-Shorts-Generator · 5.2k★ · MIT · 2024-06 · Python
**Qué hace:** Alternativa open source a Opus Clip / Vidyo.ai / Klap. Convierte **videos largos de YouTube en shorts verticales 9:16** usando detección de highlights por LLM, transcripción con Whisper y recorte vertical automático. Sin marcas de agua ni créditos por clip.
**Web-deployable:** Sí — app web.
**Despliegue:** 2 años, enfocado a creadores de contenido.

### 6. buxuku/SmartSub · 5.4k★ · MIT · 2024-05 · TypeScript
**Qué hace:** Suite de escritorio todo-en-uno para **video → subtítulos**: transcripción (Whisper/FunASR local, offline), **traducción de subtítulos**, doblaje con IA y clonación de voz, y *burn-in* (quemado) de subtítulos. Batch + aceleración GPU. Soporta MCP/CLI.
**Web-deployable:** Sí — UI tipo web/desktop multiplataforma (Windows/macOS/Linux).
**Despliegue:** 2 años, muy útil para accesibilidad y localización.

---

## 🖼️ CATEGORÍA 2 — Generación de IMAGEN

### 7. mudler/LocalAI · 49.3k★ · MIT · 2023-03 · Go
**Qué hace:** **Motor de IA local open source**. Ejecuta *cualquier modelo* — LLM, visión, voz, imagen y video — en cualquier hardware, **sin necesidad de GPU**. Expone una **API compatible con OpenAI** y una WebUI propia. Es la alternativa self-hosted a la nube de OpenAI.
**Web-deployable:** Sí — WebUI + API REST (drop-in OpenAI-compatible).
**Despliegue:** 3.5 años, el más maduro. Ideal como backend unificado para el resto de herramientas.

### 8. Anil-matcha/Open-Generative-AI · 29.4k★ · MIT · 2023-05 · JavaScript
**Qué hace:** **Estudio de generación de imagen y video** con 600+ modelos (Flux, Midjourney, Kling, Sora, Veo) repartidos en 14 "studios". Alternativa **sin filtros de contenido** a plataformas cerradas tipo Fal.ai/InVideo. Self-hosted.
**Web-deployable:** Sí — app web (JavaScript), deployable directo.
**Despliegue:** 3 años, push activo. Nota: usa backend "MuAPI" para acceso a modelos.

### 9. leejet/stable-diffusion.cpp · 7.5k★ · MIT · 2023-08 · C++
**Qué hace:** Inferencia de **modelos de difusión en C/C++ puro** — Stable Diffusion, Flux, Wan, Qwen Image, Z-Image — sin depender de Python/PyTorch pesado. Incluye modo **servidor con Web UI**.
**Web-deployable:** Sí — binario + server HTTP con UI.
**Despliegue:** 3 años, activo. Excelente para entornos livianos o embebidos.

### 10. enricoros/big-AGI · 7.1k★ · MIT · 2023-03 · TypeScript
**Qué hace:** **Suite AI completa** (workspace) con personas AI, chat **multi-modelo (Beam)** de primer nivel, **texto-a-imagen**, voz, streaming, ejecución de código e importación de PDF. Deployable on-prem o en la nube.
**Web-deployable:** Sí — app Next.js (web nativa).
**Despliegue:** 3.5 años, muy activo. Enfoque: interfaz unificada para varios proveedores AI.

### 11. mylxsw/aidea · 6.9k★ · MIT · 2023-08 · Dart (Flutter)
**Qué hace:** **App que integra los principales LLM e modelos de generación de imagen** (incl. Stable Diffusion), construida con Flutter, con **código totalmente open source**. Cliente único para chat + generación visual.
**Web-deployable:** Sí — web + móvil (Flutter multiplataforma).
**Despliegue:** 3 años. ⚠️ último push 2026-03 (menos actividad reciente que otros).

### 12. pollinations/pollinations · 5.1k★ · MIT · 2021-04 · TypeScript
**Qué hace:** **Plataforma Gen-AI abierta** ("tu plataforma Gen-AI amistosa"). Ofrece generación de imágenes (y más) vía **API y web sin necesidad de claves de pago** para desarrolladores. Enfocada a accesibilidad y experimentación abierta.
**Web-deployable:** Sí — plataforma/API web.
**Despliegue:** 5+ años, la más antigua del listado. Comunidad grande (457 issues abiertos = mucho uso).

### 13. mcmonkeyprojects/SwarmUI · 4.6k★ · MIT · 2024-06 · C#
**Qué hace:** **Interfaz web modular para Stable Diffusion** (ex-StableSwarmUI). Énfasis en hacer accesibles *powertools* de SD con **alto rendimiento y extensibilidad**. Es la alternativa con licencia MIT a A1111/ComfyUI (que son GPL).
**Web-deployable:** Sí — **es una Web UI** de propósito (frontend JS + backend C#).
**Despliegue:** 2 años, push activo. ⭐ El hueco MIT del ecosistema SD.

### 14. idootop/MagicMirror · 2.9k★ · MIT · 2024-11 · TypeScript
**Qué hace:** **Face swap instantáneo con IA** ("一键 AI 换脸" = cambio de cara en un clic). Interfaz web para intercambiar rostros en imágenes de forma rápida.
**Web-deployable:** Sí — app web.
**Despliegue:** ~22 meses. Nota: uso de face swap tiene consideraciones éticas/legales según jurisdicción.

### 15. nadermx/backgroundremover · 8.1k★ · MIT · 2021-05 · Python
**Qué hace:** **Elimina el fondo de imágenes y videos con IA** mediante una interfaz de línea de comandos simple. Gratis y open source; también hay servicio web (backgroundremoverai.com).
**Web-deployable:** Sí — CLI + API (integrable en web).
**Despliegue:** 5+ años, muy estable. Útil como paso de post-proceso en pipelines de imagen/video.

---

## 🎥 CATEGORÍA 3 — Híbrido (imagen + video, canvas/workflow)

### 16. HBAI-Ltd/Toonflow-app · 16.2k★ · MIT · 2026-01 · TypeScript
**Qué hace:** **Plataforma creativa AI open source** que combina **canvas infinito + agentes AI + workflows visuales**. Soporta generación de imagen, generación de video, storyboard inteligente y creación de cortos/短剧. Despliegue **local**, conexión libre de modelos, app de escritorio multiplataforma y extensible vía MCP/plugins. Enfoque tipo "LibTV/TapNow".
**Web-deployable:** Sí — app web/canvas (TypeScript), desktop multiplataforma.
**Despliegue:** ⚠️ Solo **8 meses** de antigüedad (borde inferior del criterio). Aún así, 16.2k★ y 0 issues abiertos = muy pulido para su edad. **Vigilar bugs.**

---

## Tabla Resumen — Los 16 y sus 4 Criterios

| # | Repo | ★ | Lic. | Creado | Leng. | Web-ready | Función (1 línea) |
|---|------|---|------|--------|-------|-----------|-------------------|
| 1 | MoneyPrinterTurbo | 126.9k | MIT | 2024-03 | Python | ✅ WebUI | Texto → video corto HD automático |
| 2 | LocalAI | 49.3k | MIT | 2023-03 | Go | ✅ WebUI+API | Motor AI local (imagen/video/LLM/audio) |
| 3 | Open-Generative-AI | 29.4k | MIT | 2023-05 | JS | ✅ Web app | Estudio imagen+video, 600+ modelos |
| 4 | Toonflow-app | 16.2k | MIT | 2026-01 | TS | ✅ Web canvas | Canvas infinito + agentes imagen/video |
| 5 | ViMax | 12.5k | MIT | 2025-03 | Python | ✅ App/API | Video agéntico (director+guionista) |
| 6 | backgroundremover | 8.1k | MIT | 2021-05 | Python | ✅ CLI+API | Quita fondo de imagen/video con IA |
| 7 | autoclip | 9.0k | MIT | 2025-07 | Python | ✅ Web app | Clipping + highlights automáticos |
| 8 | stable-diffusion.cpp | 7.5k | MIT | 2023-08 | C++ | ✅ Server+UI | Difusión en C++ puro (SD/Flux/Wan) |
| 9 | big-AGI | 7.1k | MIT | 2023-03 | TS | ✅ Next.js | Suite AI con text-to-image multi-modelo |
| 10 | aidea | 6.9k | MIT | 2023-08 | Dart | ✅ Web+móvil | App LLM + generación de imagen |
| 11 | FunClip | 6.4k | MIT | 2023-05 | Python | ✅ Gradio UI | Corte de video por texto (ASR) |
| 12 | SmartSub | 5.4k | MIT | 2024-05 | TS | ✅ Web UI | Subtítulos + traducción + doblaje |
| 13 | AI-Youtube-Shorts-Gen | 5.2k | MIT | 2024-06 | Python | ✅ Web app | YouTube largo → shorts 9:16 |
| 14 | pollinations | 5.1k | MIT | 2021-04 | TS | ✅ Plataforma/API | Plataforma Gen-AI abierta |
| 15 | SwarmUI | 4.6k | MIT | 2024-06 | C# | ✅ Web UI | ⭐ Web UI de Stable Diffusion (MIT) |
| 16 | MagicMirror | 2.9k | MIT | 2024-11 | TS | ✅ Web | Face swap instantáneo |

---

## ⚠️ Lista Negra — Famosos que NO Califican (por licencia o antigüedad)

| Repo | Motivo de exclusión |
|------|---------------------|
| **ComfyUI** (comfyanonymous/ComfyUI) | Licencia **GPL-3.0** — incompatible con regla MIT |
| **AUTOMATIC1111/stable-diffusion-webui** | Licencia **AGPL-3.0** |
| **lllyasviel/Fooocus** | Licencia **GPL-3.0** |
| **invoke-ai/InvokeAI** | Licencia **Apache-2.0** (no MIT) |
| **Sora / Runway / Pika** | Cerrados (no open source) |
| **ZeroLu/awesome-nanobanana-pro**, **ZeroLu/awesome-seedance** | Creados 2025-10 a 2026-02 → borde/recientes; además son *listas*, no software |

> **Nota estratégica:** los tres gigantes del sector (ComfyUI, A1111, Fooocus) quedan fuera por licencia copyleft. Si en el futuro el Monarca necesitara usarlos, implicaría obligaciones de distribución de código. Los MIT de esta lista son **comercialmente más limpios**.

---

## Recomendación Táctica

**Para arrancar HOY (mejor relación madurez/estrellas/MIT/web):**

1. **MoneyPrinterTurbo** (126k★) — el más probado para *video*: texto → video corto, WebUI lista para self-host. 2.5 años, push activo.
2. **LocalAI** (49k★) — para *imagen + video + más*: un motor local con WebUI y API compatible OpenAI. 3.5 años.
3. **SwarmUI** (4.6k★) — si el objetivo específico es **UI web de Stable Diffusion con licencia MIT** (el hueco que dejan A1111/ComfyUI al ser GPL).
4. **Open-Generative-AI** (29k★) — para *imagen + video* en una sola app web JS, deployable directo.

**Criterio de selección por caso de uso:**
| Necesito… | Repo recomendado |
|-----------|------------------|
| Video corto desde texto (Reels/TikTok auto) | MoneyPrinterTurbo |
| Motor local todo-en-uno con API | LocalAI |
| UI web SD con licencia MIT | SwarmUI |
| Clipping/highlights automáticos | autoclip / AI-Youtube-Shorts-Generator |
| App web JS de imagen+video | Open-Generative-AI |
| Inferencia SD en C++ (sin Python pesado) | stable-diffusion.cpp |
| Subtítulos/doblaje/traducción de video | SmartSub / FunClip |
| Quitar fondo (imagen/video) | backgroundremover |

---

## Siguientes Pasos Sugeridos

1. **Clonar y verificar** los 2-3 finalistas en un entorno aislado (Docker cuando exista).
2. **Auditar licencia real** en el `LICENSE` del repo (no solo el badge de la API) antes de uso comercial.
3. **Definir caso de uso Seawolf** para elegir entre "video automático" vs "imagen SD" — el stack cambia según el objetivo.

---

## Apéndice — Fuente de Datos

- **GitHub Search API** (12 consultas: image generation, text-to-image, video generation, text-to-video, stable diffusion webui, ai image, ai video, comfyui, generative ai, face swap, upscale image, image generator) — acceso 2026-09-29
- **GitHub Repos API** (verificación individual de licencia/stars/fechas/topics/descripción para 16 finalistas) — acceso 2026-09-29
- **README oficial** de cada repo (descripciones de función) — acceso 2026-09-29
- Filtro obligatorio: `license:mit stars:>1000 created:<2026-03-01`

**Fin del informe.** Listo para auditoría de Beru y archivo en `diario-de-sombras/`.