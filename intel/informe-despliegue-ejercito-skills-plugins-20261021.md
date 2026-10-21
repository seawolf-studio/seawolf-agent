# INFORME — PUESTA EN MARCHA DEL EJÉRCITO: skills, plugins y conectores por sombra
**Fecha:** 2026-10-21 · Uso Interno — Seawolf Studio · Bellion para el Monarca (Key)

---

## 1. PUNTO 1 — HECHO
| Acción | Resultado |
|---|---|
| Borrar 6 carpetas de skills corruptas (nombres basura) | ✅ 6 eliminadas |
| Activar plugin **`disk-cleanup`** | ✅ activo (default + perfil **jima**) |
| Activar plugin **`security-guidance`** | ✅ activo (default + **beru** + **kaisel**) |

### ⚠️ Hallazgo honesto y rescate
Esas carpetas "basura" **contenían 6 skills REALES del set Superpowers** (`brainstorming`, `executing-plans`, `receiving-code-review`, `subagent-driven-development`, `using-superpowers`, `writing-plans`). Al limpiarlas las eliminé.
**Los originales sobrevivían** en la ubicación legado `C:\Users\Admin\.hermes\skills\` → **restaurados 20 skills**:
- **11 de Superpowers**: brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, subagent-driven-development, using-superpowers, verification-before-completion, using-git-worktrees, writing-plans, writing-skills.
- **9 `seawolf-shadow-*`** (identidad propia de cada sombra).

**Daño neto: cero.** *(Lección anotada: antes de borrar "basura", revisar su CONTENIDO.)*

---

## 2. PUNTO CRÍTICO — ¿ES POSIBLE PONERLO TODO EN MARCHA? **SÍ. Y YA ESTÁ HECHO.**

**Método verificado** (dos vías):
1. `hermes -p <sombra> skills install <id> -y` → instala en el perfil correcto (probado con `official/*`).
2. Copia local de skills ya existentes al `skills/` de cada perfil (idempotente).

**Verificación:** `hermes -p <sombra> skills list` confirma cada skill **enabled** en su perfil.

### Reparto por sombra (lo que se le puso)
| Sombra | Rol | Skills clave asignadas | Plugins |
|---|---|---|---|
| **beru** | Auditor | sdlc-review, verification, code-review (req/recv), TDD, dogfood, DOM-inspect, grounded-citations, tech-eval, **sherlock**, **stocks** | security-guidance |
| **igris** | Copywriting | humanizer, claude-design, baoyu-infographic, docx, document-to-action-items | — |
| **tank** | Ventas/Cierre | open-maps-lead-harvesting, prospeccion-frio, captacion-frios, lobo-cazador, whatsapp-waha, competitor-news | — |
| **greed** | Ads | product-price-monitor, competitor-news, tech-eval, claude-design | — |
| **iron** | Email | rss-feeds, blogwatcher, document-to-action-items, captacion-frios, **agentmail** | — |
| **tusk** | SEO | blogwatcher, rss-feeds, competitor-news, github-repo-recon, youtube-content | — |
| **kamish** | Social | reddit-reading, xurl, youtube-content, gif-search, content-production, hyperframes-content, ascii-video, manim-video, **social-media-content-calendar** | — |
| **kaisel** | WebDev | 6× github, simplify-code, spike, node-inspect, python-debugpy, astro-ecommerce, web-presence, wordpress-mcp, pdf | security-guidance |
| **titan** | UX/UI | claude-design, sketch, design-md, excalidraw, architecture-diagram, interactive-html-apps, aplicativos-interactivos, powerpoint, xlsx, docx, pdf, baoyu-infographic, **excel-author**, **pptx-author** | — |
| **jima** | Automatización | self-hosted-ai-stack-ops, multi-agent-orchestration, maps, github-repo-recon, whatsapp-waha, agent-saas, lobo-nereus, hermes-agent | disk-cleanup |
| **bellion** | Orquestación | **todo** el set de orquestación + Superpowers + 20 restaurados | disk-cleanup, security-guidance |

**+ Núcleo común a todas:** writing-plans, verification-before-completion, systematic-debugging, caveman.

---

## 3. ALTERNATIVA A ELEVENLABS — **Kokoro-82M (gratis)**
| Opción | Licencia | Coste | Veredicto |
|---|---|---|---|
| **Kokoro-82M** | **Apache-2.0** | **$0** (local, corre en CPU) | 🥇 **Elegida** — 54 voces, calidad ~ElevenLabs |
| **Piper** | GPL-3.0 | $0 (local, CPU) | Ya la usamos en **Kaelen** (es_ES) |
| Coqui / Chatterbox | varias | $0 | Alternativas válidas |
| ElevenLabs | propietaria | pago | ❌ descartada por orden |

**Doctrina ya vigente** (referencia interna `voice-layer-deployment`): *"producción preset-first (Kokoro Apache-2.0) con la clonación como premium opcional"*. → **Kokoro es el motor de voz del ejército.** Sin pagar nada.

---

## 4. BLOQUEOS QUE NECESITAN TU MANO
| Necesidad | Por qué | Sin él… |
|---|---|---|
| **`GITHUB_TOKEN`** (o instalar `gh`) | El límite anónimo de GitHub es **60 req/h**; las skills comunitarias (`skills-sh/*`) fallan | No puedo instalar el paquete comunitario (cold-email, social-content, etc.) |
| **Cuenta Composio (free tier)** | **MCP con 1000+ conectores** (Gmail, HubSpot, Google Ads, Notion…) — el gran conector que nos falta | Seguimos sin conectores SaaS unificados |

---

## 5. FUENTES
- `hermes skills install/list`, `hermes plugins enable` (verificado en vivo) · `manage_catalog` · `~/.hermes/skills` (rescate) · docs Kokoro/Apache-2.0.

**Fin del informe.**
