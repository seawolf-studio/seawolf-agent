# Informe de Inteligencia: Repos GitHub — Publicación GRATUITA y PROGRAMADA en Redes Sociales
**Fecha:** 2026-09-29 | **Sesión:** Investigación | **Clasificación:** Uso Interno - Seawolf Studio
**Método:** GitHub Search API + Repos API (verificación directa, no scraping)
**Descripciones:** extraídas de la descripción oficial + README de cada repo (fuente directa)

---

## Resumen Ejecutivo

Objetivo: alternativas open source a **Hootsuite/Buffer** — programar y publicar contenido en redes sociales gratis, desde infraestructura propia.

**Criterios aplicados:** ① Licencia **MIT** (innegociable) · ② **≥1000★** · ③ **Deployable como sitio web** · (④ regla de antigüedad OMITIDA por orden del Monarca).

**Hallazgo crítico (honestidad brutal):** esta categoría es la más pobre en MIT de las tres investigadas. **Los referentes del mercado NO califican:**
- **Postiz** (36.5k★) → AGPL-3.0
- **brightbean-studio** (2.4k★) → AGPL-3.0
- **Automatisch** (14k★) → AGPL-3.0
- **n8n** (206k★) → Sustainable Use License (fair-code, no libre)
- **Activepieces** (24.8k★) → open core: MIT + carve-out Enterprise (no MIT puro)
- **Socioboard** (1.5k★) → GPL-3.0

**Conclusión:** el "Hootsuite open source" que cumple MIT puro y ≥1000★ es **escaso pero existe**. La joya es **Mixpost**. El resto son motores de automatización y librerías de API con las que *construyes* tu propio scheduler.

---

## Metodología de Filtrado (reutilizable)

```python
# Catálogo GitHub — búsqueda con filtros duros
"https://api.github.com/search/repositories?q=<tema>+license:mit+stars:>1000&sort=stars&order=desc"
# Verificación individual por repo:
"https://api.github.com/repos/{owner}/{repo}"      # license, stars, fechas
"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/LICENSE"  # licencia real (evita falsos NOASSERTION)
```
⚠️ Lección aprendida: GitHub marca `NOASSERTION` cuando la licencia es mixta/custom. **Siempre leer el archivo LICENSE real** — así se detectó que Activepieces/Automatisch/n8n NO son MIT puro.

---

## ✅ REPOS QUE CUMPLEN (MIT + ≥1000★ + Web-Deployable)

### 🥇 Núcleo — Schedulers / Publicadores (lo que buscas)

#### 1. inovector/mixpost · 3.7k★ · MIT · 2022-07
**Qué hace:** Plataforma completa de **gestión y programación de redes sociales self-hosted**. Programa, publica y gestiona contenido en **10+ redes** (Facebook, Instagram, X/Twitter, LinkedIn, TikTok, Pinterest, YouTube, Mastodon, Threads, Bluesky…) desde un panel propio. Se autocanoniza como *"alternativa a Buffer"*. Sin suscripciones ni límites. (Existe edición Pro de pago; el **repositorio core es MIT puro**.)
**Web-deployable:** ✅ Sí — app web **Laravel (PHP) + Vue**, se despliega en cualquier servidor PHP/MySQL.
**Veredicto:** ⭐ **EL mejor candidato del informe.** Es prácticamente tu Hootsuite privado, con licencia MIT y código auditale.

#### 2. langchain-ai/social-media-agent · 2.8k★ · MIT · 2024-11
**Qué hace:** **Agente AI** (LangGraph) que toma una **URL y genera posts para Twitter/X y LinkedIn** automáticamente. Usa flujo *human-in-the-loop*: maneja la autenticación OAuth con cada red y te deja editar, aceptar o rechazar el post antes de publicar. Programación y curación asistidas por IA.
**Web-deployable:** ✅ Sí — servidor LangGraph (desplegable) + UI.
**Veredicto:** Perfecto si quieres **contenido autogenerado + aprobación humana** antes de publicar.

#### 3. Katzca/AutoSocial (AutoSocial Studio) · 1.3k★ · MIT · 2026-03
**Qué hace:** **Dashboard local de automatización multi-cuenta** para video corto en **TikTok, Instagram y YouTube**. Combina un panel **Express**, flujos de subida con **Playwright** (automatiza el navegador), **colas por cuenta + schedulers**, descargador con **yt-dlp** y "uniquificador" de video con **FFmpeg** (para evitar detección de contenido duplicado).
**Web-deployable:** ✅ Sí — dashboard web Express; pensado para estación local.
**Veredicto:** Ideal para **volumen de video** (clipping/repost) sin pagar APIs.

#### 4. LocoreMind/locoagent · 1.06k★ · MIT · 2026-05
**Qué hace:** **Agente AI que opera redes sociales con un navegador REAL** (TypeScript/Bun). Publica/interactúa simulando el comportamiento humano en el browser — evita depender de APIs oficiales (que suelen ser de pago o restrictivas).
**Web-deployable:** ✅ Sí — runtime Bun, interfaz web.
**Veredicto:** Enfoque "gratuito": automatiza vía navegador lo que las APIs cobrarían.

### 🔧 Motores para CONSTRUIR tu propio scheduler

#### 5. huginn/huginn · 50k★ · MIT · 2013-03
**Qué hace:** **Motor de agentes de automatización** ("IFTTT/Zapier hackeable en tu servidor"). Los agentes leen la web, vigilan eventos y **ejecutan acciones en tu nombre**, encadenados por un grafo dirigido. Sirve para **monitorizar fuentes y publicar automáticamente** vía APIs/webhooks de redes.
**Web-deployable:** ✅ Sí — app web **Ruby on Rails** (Docker disponible).
**Veredicto:** El motor MIT más estrellado del mundo de la automatización. Construyes lógica de publicación a medida, sin n8n (que no es libre).

### 📚 Librerías de publicación por API (necesitan envoltorio web)

#### 6. tweepy/tweepy · 11.2k★ · MIT · 2009-07
**Qué hace:** La **librería Python estándar para la API de Twitter/X**. Publica tuits, hilos, media y programa envíos.
**Web-deployable:** ⚠️ Es librería — requiere envolverla en tu web/FastAPI.
**Veredicto:** Bloque de construcción sólido y MIT para X.

#### 7. subzeroid/instagrapi · 6.9k★ · MIT · 2020-07
**Qué hace:** **Cliente Python no oficial de Instagram** (API privada móvil). Publica fotos, reels, stories e interactúa sin la API oficial de pago.
**Web-deployable:** ⚠️ Librería — necesita wrapper.
**Veredicto:** Ruta gratuita para Instagram. ⚠️ Usar con cautela (ToS de Instagram).

#### 8. aiogram/aiogram · 5.9k★ · MIT · 2018-02
**Qué hace:** **Framework Python asíncrono para la Telegram Bot API**. Envía/publica contenido a canales y grupos de Telegram, con colas y programación.
**Web-deployable:** ⚠️ Framework — se integra en tu backend.
**Veredicto:** La vía limpia, MIT y gratuita para Telegram.

---

## 🧩 Adyacentes MIT (≥1000★) — útiles, no son schedulers

| Repo | ★ | Qué hace |
|------|---|----------|
| **charlie947/social-media-skills** | 3.7k | Toolkit de 17 *skills* para agentes AI (Codex/Claude): voz de usuario, redacción LinkedIn, Reels, prompts de imagen. Genera, no publica. |
| **ScrapeCreators/social-media-research-skills** | 2.9k | Skills para *investigación* en redes (TikTok/IG/YouTube): análisis de outliers, comentarios, anuncios. |

---

## ⚠️ Lista Negra — Referentes que NO Califican (licencia no-MIT)

| Repo | ★ | Licencia | Motivo |
|------|---|----------|--------|
| **gitroomhq/postiz-app** | 36.5k | **AGPL-3.0** | El "Hootsuite open source" más famoso. Copyleft: obliga a liberar tu código si lo ofreces como servicio. |
| **n8n-io/n8n** | 206k | **Sustainable Use** | Fair-code, no libre. |
| **activepieces/activepieces** | 24.8k | **MIT + Enterprise** | Open core: `packages/ee` es propietario. No MIT puro. |
| **automatisch/automatisch** | 14k | **AGPL-3.0** | — |
| **brightbeanxyz/brightbean-studio** | 2.4k | **AGPL-3.0** | — |
| **muesli/beehive** | 6.5k | **AGPL-3.0** | — |
| **Socioboard-5.0** | 1.5k | **GPL-3.0** | — |

> **Nota estratégica:** el ecosistema de schedulers sociales vive mayoritariamente en **AGPL-3.0**. Eso protege al autor original pero obliga a *ti* a liberar código si montas un servicio. Si el plan es un producto SaaS cerrado de Seawolf, **AGPL es una trampa legal**. Los MIT de este informe evitan ese riesgo.

---

## 🎯 Cerca del corte — MIT correcto pero <1000★ (por si el Monarca flexibiliza)

| Repo | ★ | Qué hace |
|------|---|----------|
| **Anil-matcha/Free-AI-Social-Media-Scheduler** | 529 | Self-host Next.js, foco YouTube/TikTok, generación AI integrada. MIT. |
| **deepakness/cogsend** | 159 | Scheduler self-hosted en Cloudflare Workers (SvelteKit). MIT. |
| **Matthew-Selvam/Open-Dispatch** | 14 | Una API → 7 plataformas (X, IG, Telegram, Bluesky, LinkedIn, Threads, YouTube). MIT. |
| **AstaBlackClove/posthive** | 16 | Scheduler agéntico con MCP. **AGPL-3.0** (ni así califica). |

---

## Recomendación Táctica

| Si necesito… | Repo recomendado |
|--------------|------------------|
| **Un Hootsuite/Buffer privado, MIT, web** | ⭐ **Mixpost** |
| **Motor de automatización propio (self-host)** | **Huginn** |
| **Contenido AI → aprobación → publicar** | **langchain-ai/social-media-agent** |
| **Volumen de video TikTok/IG/YouTube en local** | **AutoSocial** |
| **Publicar vía navegador (sin APIs de pago)** | **locoagent** |
| **Publicar en X / Instagram / Telegram por API** | **tweepy / instagrapi / aiogram** (MIT) |

**Ruta recomendada para Seawolf Studio:**
1. **Base:** desplegar **Mixpost** en el VPS (Hostinger) → scheduler multi-red gratuito, MIT, propio.
2. **Automatización:** añadir **Huginn** para flujos de monitorización + disparo de publicaciones.
3. **IA de contenido:** integrar **social-media-agent** si se quiere generación + aprobación humana.
4. **Bloqueo legal:** Ninguno de los recomendados arrastra AGPL → producto SaaS cerrado viable.

---

## Siguientes Pasos Sugeridos

1. **Probar Mixpost** en el VPS (Docker/Composer) y conectar 2-3 redes de prueba.
2. **Auditar el LICENSE real** de Mixpost en el repo (confirmar que el core es MIT puro y qué cubre Pro).
3. **Decidir alcance:** ¿scheduler multi-red (Mixpost) o solo X/IG/Telegram vía librerías?

---

## Apéndice — Fuente de Datos

- **GitHub Search API** (consultas: social media scheduler/management/automation, crosspost, buffer/hootsuite alternative, scheduler, autopost, publish, etc.) — acceso 2026-09-29
- **GitHub Repos API** (verificación de stars/licencia/fechas para ~25 repos) — acceso 2026-09-29
- **Verificación de licencia real** vía archivo `LICENSE` en crudo (detectó open-core y carve-outs) — acceso 2026-09-29
- Filtro obligatorio: `license:mit stars:>1000` (sin filtro de fecha, por orden del Monarca)

**Fin del informe.** Listo para auditoría de Beru y archivo en `diario-de-sombras/`.