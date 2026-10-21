# INFORME — AUDITORÍA DE LA CASA: qué tenemos y qué nos falta
## Plugins · MCPs · Conectores · Skills
**Fecha:** 2026-10-21 · Uso Interno — Seawolf Studio · Bellion para el Monarca (Key)

---

## 0. INVENTARIO — lo que YA tenemos hoy

| Recurso | Cantidad | Detalle |
|---|---|---|
| **Skills** | **157** | seawolf (17), productivity (26), creative (16), mlops (8), github (6), research, social-media, smart-home, apple, media, email, note-taking, devops… |
| **Plugins** | **58** | navegador (browser-use/basebase/firecrawl), **imagen** (openai, xai, fal, krea, deepinfra, meta-ai), **plataformas** (telegram, whatsapp ×2, discord, slack, signal, matrix, teams, sms, email, ntfy, line, wecom, weixin, yuanbao…), **búsqueda web** (brave, ddgs, exa, firecrawl, tavily, perplexity, searxng, parallel) |
| **MCPs** | **6** | `cua-driver`, `rea`, `wp-streaming`, `wp-dropshipping`, `wp-respira`, `wp-oktopus` (✗ off) |
| **Sombras** | **10** | beru, igris, tank, kaisel, greed, iron, jima, kamish, titan, tusk |
| **Cron** | 2 | `memento-diario` (06:00) · `Monitor de gasto` (08:00) |
| **Plataformas de mensajería** | 5 | Telegram, Discord, WhatsApp, Slack, Signal |

### ⚠️ Dos cosas que saltaron a la vista
1. **6 carpetas de skills CORRUPTAS** con nombres basura (`software-development" 2>&1 && cp -r C:UsersAdmin…`) — residuo de un comando fallido. **Recomiendo borrarlas.**
2. El plugin **`disk-cleanup` ya está instalado pero DESACTIVADO** — justo lo de hoy. **Activar.**

---

## 1. ACTIVAR YA (instalado y apagado — coste 0)
| Item | Qué hace | Por qué nos sirve |
|---|---|---|
| **`disk-cleanup`** (plugin) | Limpieza de disco | Es literalmente Seawolf Tools por otra vía |
| **`security-guidance`** (plugin) | Guía de seguridad | Blindaje; cierra el frente de secretos/permisos |
| **`chronos`** (plugin) | Tiempo/programación | Refuerza cron y el Panel Kamikaze |
| **`google_meet`** / **`teams_pipeline`** (plugins) | Reuniones Meet/Teams | **CSO**: resumir reuniones de clientes (ya hay skill `teams-meeting-pipeline`) |

---

## 2. LO QUE NOS FALTA — plugins, MCPs y conectores
| Item | Tipo | Qué hace | Por qué nos beneficia |
|---|---|---|---|
| **`agent-mail-gateway`** | Plugin | Buzón de email para agentes | **Frente frío B2B email-first** (la misión raíz) |
| **`gigamail`** | Plugin (Win) | Email masivo/gestionado | Prospección en volumen |
| **`microsoft365`** | Plugin | Outlook/Calendar/Teams/OneDrive | **Seawolf Agent**: el CSO vive en correo y agenda |
| **Google Calendar MCP** (oficial `calendarmcp.googleapis.com`) | MCP | Leer/crear eventos | Agenda del CSO + recordatorios del Kamikaze |
| **`hermes-monitoring-dashboard`** | Plugin | Panel de monitoreo | **Vigilar Seawolf Agent y LOBO 24/7** sin SSH manual |
| **`bot-forge`** | Plugin | Construir bots | Acelera WhatsApp/Telegram de Seawolf Agent |
| **`account-pool` / `account-switcher`** | Plugin | Multi-cuenta / rotar identidad | **Círculo Publicitario** (varias cuentas por red) |
| **`digital-marketing-pro`** | Plugin | Kit de marketing | Círculo Publicitario |
| **`aave-mcp`** | MCP/Plugin | DeFi (Aave) | **Finanzas/inversiones** on-chain |
| **ElevenLabs MCP** | MCP | Voz TTS de alta calidad | **LOBO/NEREUS** (voz por frases) |
| **Postgres/SQLite MCP** | MCP | Consultar bases | Analizar `state.db`, `kanban.db`, finanzas |
| **Stripe / pagos MCP** | MCP | Cobros y suscripciones | **Tiendas Dropi** + cobro de Seawolf Agent |

---

## 3. LO QUE NOS FALTA — skills (por proyecto)

### 🎯 CAPTACIÓN / FRENTE FRÍO (misión raíz #1)
| Skill | Qué hace | Por qué |
|---|---|---|
| `sales-skills/.../cold-email` | Correos fríos que abren | El canal email-first |
| `sales-skills/.../email-sequence` | Secuencias de seguimiento | Sin seguimiento no hay cierre |
| `skills-sh/.../outbound-prospecting` | Prospección saliente completa | Estructura el frente frío |
| `sales-skills/sales/sales-development-rep` | Rol SDR automatizado | Sombras que prospectan solas |
| `skills-sh/.../copywriting` | Copy persuasivo | La pluma del Círculo |
| `skills-sh/.../customer-referrals` | Referidos | Crecimiento barato |

### 📣 CÍRCULO PUBLICITARIO (contenido y publicación)
| Skill | Qué hace | Por qué |
|---|---|---|
| `official/creative/social-media-content-calendar` (oficial) | Calendario de contenido | La línea de montaje del Círculo |
| `skills-sh/.../social-content` · `.../social` | Contenido por red | Adapta el mensaje a cada red |
| `skills-sh/.../social-media-publishing` · `publish-social` | Publicar programado | La automatización del Círculo |
| `skills-sh/.../twitter-automation` | Automatizar X | Palanca directa de viralización |
| `skills-sh/.../vertical-video` · `shorts-creator` · `short-form-converter` | Video vertical/corto | El formato que hoy mueve todo |
| `skills-sh/.../ai-video-generation` · `ffmpeg-skill` | Generar/procesar video | Motor del Círculo |
| `skills-sh/.../seo-content` · `seo-keyword-research` | SEO | Tráfico gratis y duradero |

### 🛒 TIENDAS (Dropi/e-commerce)
| Skill | Qué hace | Por qué |
|---|---|---|
| `skills-sh/.../ecommerce-product-scraping` | Extraer productos | Precios/competencia |
| `skills-sh/.../apify-ecommerce-monitor` | Monitorear tiendas | Detectar ganadores |
| `skills-sh/.../dropshipping-mentor-nick` · `ecommerce-seller` | Playbook dropshipping | Método, no improvisación |
| `skills-sh/afadtc/.../afa` | DTC (venta directa) | Modelo de negocio afín |

### 💰 FINANZAS OBSESIVAS (misión raíz #3)
| Skill | Qué hace | Por qué |
|---|---|---|
| `official/finance/stocks` · `dcf-model` · `3-statement-model` | Valuación/mercados | **Inversiones**, el sueño de libertad |
| `official/finance/excel-author` · `pptx-author` | Excel/PowerPoint de nivel | Entregables a clientes e inversores |
| `bookkeeping-basics` · `receipt-processing` · `invoice-organizer` · `invoice-expense-extractor` | Contabilidad, facturas, recibos | Manejo obsesivo del dinero |

### 🕵️ INTELIGENCIA / OSINT
| Skill | Qué hace | Por qué |
|---|---|---|
| `official/security/sherlock` (oficial) | Buscar usuarios en redes | Recon de objetivos/clientes |
| `skills-sh/.../osint-researcher` | Investigación OSINT | Due diligence y prospección |

### 📚 ARCHIVO / BIBLIOTECA
| Skill | Qué hace | Por qué |
|---|---|---|
| `obsidian` · `second-brain-librarian` | Segundo cerebro / notas | Tu biblioteca y tu memoria |
| `llm-wiki` | Wiki con LLM | Organizar el conocimiento acumulado |

### ⚙️ DEVOPS (VPS / LOBO)
| Skill | Qué hace | Por qué |
|---|---|---|
| `skills-sh/.../devops-deploy` | Despliegue | LOBO/NEREUS en el VPS |
| `skills-sh/.../linux-agent-skills` | Administración Linux | Los servidores |

---

## 4. RECOMENDACIÓN DE ORDEN (por impacto/misión raíz)
1. **Activar** `disk-cleanup` + `security-guidance` + limpiar las 6 carpetas corruptas.
2. **Captación**: cold-email + email-sequence + outbound-prospecting + Gmail/Calendar MCP. *(misión raíz #1)*
3. **Círculo Publicitario**: social-media-content-calendar + vertical-video + social-media-publishing.
4. **Finanzas**: stocks + excel-author + bookkeeping.
5. **Infra**: hermes-monitoring-dashboard + devops-deploy.

---

## 5. FUENTES
- `manage_catalog` de Hermes (búsquedas en vivo) · `hermes plugins/mcp/cron list` · config.yaml · Google Calendar MCP docs (calendarmcp.googleapis.com) · nspady/google-calendar-mcp (MIT).

**Fin del informe.**
