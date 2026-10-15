# INFORME DE TEMA: "El Círculo Publicitario" — Motores Open-Source
## Repos que automatizan publicación en redes (estilo Hootsuite/Metricool)

**Fecha:** 2026-10-14 · **Clasificación:** Uso Interno — Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Objetivo:** Motores open-source para automatizar publicación de contenido en redes sociales, bajo tus estándares.
**Estándares aplicados:** **MIT** (innegociable) · **≥1000★** · deployable como web/servicio · antigüedad ≥6 meses.
**Fuente:** GitHub API + `LICENSE` en crudo — 2026-10-14.

---

## 0. HALLAZGO CLAVE (te lo digo de frente)

**El pool MIT para esta categoría es MUY flaco.** Los grandes de verdad (**Postiz, n8n, Activepieces, Automatisch, Socioboard**) **NO son MIT** (AGPL / fair-code / open-core). Verificado leyendo su `LICENSE` en crudo.

**Solo 3 repos cumplen TODO** (MIT + ≥1000★ + ≥6 meses + deployable), y **4º casi** (falla antigüedad). El claro ganador es **`inovector/mixpost`** — es literalmente un "Buffer/Hootsuite self-hosted" bajo MIT.

---

## 1. FINALISTAS QUE CUMPLEN TUS PARÁMETROS

| Repo | ★ | Lic. | Lenguaje | Inicio | Últ. push | ¿Cumple? |
|------|---|------|----------|--------|-----------|----------|
| **inovector/mixpost** | 3.812 | **MIT** | Vue+Laravel | 2022-07 | 2026-03 | ✅ **TODO** |
| **langchain-ai/social-media-agent** | 2.841 | **MIT** | TypeScript | 2024-11 | 2026-10 | ✅ TODO |
| **Katzca/AutoSocial** | 1.386 | **MIT** | JavaScript | 2026-03 | 2026-06 | ✅ (≈7 meses) |
| LocoreMind/locoagent | 1.065 | MIT | TypeScript | 2026-05 | 2026-06 | ❌ antigüedad ≈5 meses |

### 1.1 ⭐ inovector/mixpost — EL GANADOR
- **3.812★ · MIT puro · Vue + Laravel · self-hosted en tu servidor.**
- **Qué es:** plataforma completa de **gestión de redes sociales** ("Buffer alternative", sin suscripciones ni límites). Es lo más cercano a **Hootsuite/Metricool** que existe en MIT.
- **Capacidades:** calendario de contenido, programación, publicación multi-cuenta, analítica/engagement, colaboración de equipo (tareas, permisos), multi-marca, cuentas sociales centralizadas.
- **Deploy:** app Laravel (PHP) → **se monta como web** en tu VPS. Cumple "deployable".
- **Homepage:** mixpost.app · topics: `buffer-alternative`, `content-calendar`, `cross-platform-posting`, `engagement-analytics`, `smm`.
- **Ojo:** existe **Mixpost Pro** (versión de pago) — pero **el core del repo es MIT**. Verificar qué features quedan tras el muro Pro.
- **Riesgo menor:** último push 2026-03 (~7 meses). Activo pero no frenético.

### 1.2 langchain-ai/social-media-agent — la capa IA
- **2.841★ · MIT · TypeScript · mantenido por LangChain (activo 2026-10).**
- **Qué es:** **agente** que toma una URL y **genera un post** (Twitter/X, LinkedIn) con flujo **human-in-the-loop** (apruebas/editas/rechazas). Soporta **crons** para automatizar.
- **No es** un publicador masivo tipo Hootsuite: es **generación de contenido + publicación asistida**.
- **Dependencias:** Anthropic API + LangSmith + FireCrawl + Arcade (auth a plataformas). Más piezas que mixpost.

### 1.3 Katzca/AutoSocial — video corto local
- **1.386★ · MIT · JavaScript · 2026-03 (≈7 meses ✅).**
- **Qué es:** dashboard **local** multi-cuenta para **video corto** (TikTok, Instagram, YouTube). Colas por cuenta, **Playwright** para subir, schedulers (cron/hora), descarga con yt-dlp, "uniquifier" de video con FFmpeg.
- **Enfoque:** estación de trabajo local (sin auth, no SaaS). Ideal para **distribución de clips/video**.

### 1.4 LocoreMind/locoagent — ❌ por antigüedad
- **1.065★ · MIT · TS · 2026-05 (≈5 meses → NO cumple ≥6 meses).** Agente IA que opera redes con **navegador real** (fork del Claude Code CLI). Interesante como referencia; **descartado por tiempo** salvo que ordenes omitir la regla.

---

## 2. CASI-CUMPLEN (MIT pero <1000★) — por si flexibilizas estrellas
| Repo | ★ | Lic. | Qué hace |
|------|---|------|----------|
| wanghaisheng/easy-uploader | 385 | MIT | **Subida masiva programada** de video a redes (headless, equipo). Python, 2021. |
| getindiekit/indiekit | 392 | MIT | Servidor Node que **publica a tu web personal y comparte** en redes (IndieWeb/Micropub). |

---

## 3. PANORAMA NO-MIT (los grandes — honestidad)
*Por si algún día flexibilizas la licencia. **Hoy quedan fuera por tu regla innegociable.***

| Repo | ★ | Licencia REAL (leída en crudo) | Veredicto |
|------|---|-------------------------------|-----------|
| gitroomhq/postiz-app | 37.198 | **AGPL-3.0** | El líder OSS de la categoría. ❌ |
| n8n-io/n8n | 207.401 | **Fair-code (sustainable use) + `ee/`** | Automatización general. ❌ |
| activepieces/activepieces | 25.057 | **MIT core + `packages/ee/` (enterprise)** | Open-core. ❌ |
| automatisch/automatisch | 13.995 | **AGPL-3.0 + `.ee.`** | "n8n del social". ❌ |
| Socioboard-developers/Socioboard-5.0 | 1.517 | **GPL-3.0** | Histórico. ❌ |

→ **Motivo:** copyleft (AGPL/GPL) u open-core. Ninguno pasa tu filtro MIT.

---

## 4. RECOMENDACIÓN PARA "EL CÍRCULO PUBLICITARIO"

**Base principal: `inovector/mixpost` (MIT).** Es el único motor completo tipo Hootsuite/Metricool bajo MIT puro: calendario, programación, multi-cuenta, analítica y equipo, self-hosted en tu VPS.

**Complementos (combinables):**
- **`langchain-ai/social-media-agent`** → capa de **IA para generar el contenido** (URL → post) con aprobación humana.
- **`Katzca/AutoSocial`** → si el Círculo incluye **video corto** (TikTok/IG/YouTube) con colas locales.

**Arquitectura sugerida (borrador):**
```
[Generación IA]  social-media-agent  ─┐
[Video corto]    AutoSocial           ─┼─►  [Motor/Centro] mixpost  ─►  Redes
[Analítica]      (mixpost analytics)  ─┘
```

**Caveat honesto:** ninguna combinación MIT iguala de fábrica a Postiz (AGPL) en amplitud de plataformas. **mixpost es la mejor apuesta MIT**, pero hay que verificar cuántas features quedan en su edición Pro.

---

## 5. PREGUNTA PARA TI
¿"El Círculo Publicitario" es un **producto** (para vender) o una **herramienta interna** (para tus marcas)? Cambia la elección:
- **Producto comercial** → mixpost (self-host, sin límites) como núcleo.
- **Interno** → mixpost + social-media-agent basta.

---

## 6. FUENTES
- GitHub API `/search/repositories` + `/repos/{owner}/{repo}` (stars, licencia, fechas, topics) — 2026-10-14.
- Archivos `LICENSE` en crudo (verificación real de licencia) — 2026-10-14.
- READMEs oficiales de cada repo candidato.

**Fin del informe de tema.**
