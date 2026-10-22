# INFORME FINAL — Paquete comunitario instalado por sombra
**Fecha:** 2026-10-21 · Uso Interno — Seawolf Studio · Bellion para el Monarca (Key)

---

## Resultado: 21 skills comunitarias instaladas (de 30 intentadas)

**Método:** `hermes -p <sombra> skills install <id> -y` — **verificado** con `hermes -p <s> skills list` (fuente `skills.sh`).

| Sombra | Skills comunitarias activas | N |
|---|---|---|
| **kamish** | bulkpublish-social-scheduling · schedule-social-post · short-form-converter · shorts-creator · social · twitter-automation · vertical-video | **7** |
| **tusk** | content-strategy · seo-ai-optimizer · seo-keyword-research · youtube-title-tag-optimizer | **4** |
| **igris** | content-creation · copywriting · draft-content | **3** |
| **tank** | business-dev · customer-referrals · sales-email-sequences | **3** |
| **iron** | email-sequence · outbound-prospecting | **2** |
| **greed** | prospecting | **1** |
| **beru** | invoice-organizer | **1** |
| kaisel / titan / jima | (recibieron **oficiales + locales**, no comunitarias) | 0 |

**+ oficiales:** sherlock (beru) · stocks (beru) · agentmail (iron) · social-media-content-calendar (kamish) · excel-author + pptx-author (titan).

---

## Tres rondas y sus causas (sin adornos)
| Ronda | OK | Fallos | Causa REAL |
|---|---|---|---|
| **1** | 5 | 18 | **El token solo estaba en `.env` de `default`** — cada sombra lee **su propio** `profiles/<s>/.env` → GitHub la veía anónima (60/h) |
| **2** | 8 | 9 | Token ya propagado a los 10 perfiles; los fallos restantes eran **entradas obsoletas** del índice (el autor borró los archivos upstream) |
| **3** | 8 | 3 | Busqué **alternativas vivas** para los obsoletos → instaladas |

### Descartadas (irrecuperables — el autor borró el origen)
`social-media-publishing` · `publish-social` · `sales-nav-search-builder` · `osint-researcher` · `seo-article-writing` · `bookkeeping`.
**Sustitutas que sí entraron:** `bulkpublish-social-scheduling`, `schedule-social-post`, `cold-email-copy`, `seo-ai-optimizer`, `content-strategy`.

---

## Lección grabada en la skill del ejército
> **`GITHUB_TOKEN` debe vivir en el `.env` de CADA perfil**, no solo en el de `default`.
> Síntoma engañoso: `GitHub API rate limit exhausted (unauthenticated)` **aunque el default tenga token válido**.

---

## Estado del token
- Guardado con permisos `600` en el `.env` del `default` **y de los 10 perfiles**.
- Verificado en vivo: login `seawolfk`, límite **5.000/h** (4.796 restantes).
- ⚠️ **Viajó por el chat** → recomendada rotación al cerrar el trabajo (crear nuevo → cambiar → borrar el viejo).

---

## Pendiente
- **API key de Composio** (usuario `monarca_seawolf`) → el MCP de 1000+ conectores. Sin ella no se puede configurar.

**Fin del informe.**
