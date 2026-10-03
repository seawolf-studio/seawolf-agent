# DIARIO DE SESIÓN — PROYECTO LOBO (relámpago) Y RELEVO A SEAWOLF AGENT
## Handoff para la sesión de REVISIÓN DEL SISTEMA SEAWOLF AGENT

**Fecha de sesión:** 2026-09-30 → 2026-10-03 · **Elaborado por:** Bellion, Gran Comandante
**Encargado por:** el Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Propósito:** congelar toda la inteligencia y decisiones de esta sesión y **preparar la sesión dedicada a revisar, evaluar, corregir y mejorar SEAWOLF AGENT** (el producto insignia).

---

## 0. CÓMO RETOMAR ESTA MISIÓN (leer primero)

1. Abrir una **sesión nueva** y ordenar: **"lee el diario de la última sesión"** → Bellion lee este archivo y retoma.
2. **Objeto de la próxima sesión (orden del Monarca):** *solo* **revisión del sistema de Seawolf Agent, evaluación, arreglo de errores e implementación de mejoras.**
3. **Regla de criterio (corrección del Monarca, grabada):** **Seawolf Agent y LOBO son DOS servicios y DOS desarrollos distintos.** No son dos caras del mismo servicio. Las lecciones de LOBO entran a Seawolf Agent como **patrones**, nunca como código/backend compartido.
4. **Ubicaciones clave:**
   - **Repo Seawolf Agent:** `C:\Users\Admin\seawolf-agent` (org `seawolf-studio`; WebUI en el subdir `seawolf-webui/`).
   - **Repo LOBO (NEREUS):** VPS `/opt/nereus` (OpenMuse). Fuentes espejo locales en `C:\Users\Admin\nereus-src`.
   - **Informes de esta sesión:** `seawolf-agent/intel/*` (ver §7).
5. **Documentos que guían la próxima sesión:**
   - `intel/seawolf-agent-mejoras-20261003.md` (+PDF) — **criterio corregido**; lista de mejoras.
   - `MANIFIESTO_PRODUCTO_CSO.md` — doctrina del producto insignia.
   - `PROTOCOLO_MEMENTO.md` — memoria permanente del ejército.
   - `seawolf-webui/docs/` (ARCHITECTURE, ROADMAP, CONTRACTS, rfcs/) — arquitectura real de la WebUI.

---

## 1. LA ORDEN DEL MONARCA EN ESTA SESIÓN (arco completo)

1. **Construir el agente personal** a partir de `CopilotKit/openmuse` (Meta Muse open source), marca Seawolf. → **Cristalizó como LOBO** (nombre clave interno: **NEREUS**).
2. **Rebranding** a **LOBO** + acróstico de marca (elegido: **L**ibera tu tiempo · **O**rdena tu día · **B**rinda calma · **O**bra por ti).
3. **Mascota** (lobo negro, estilo peluche 3D), **tema oscuro/claro** (oscuro por defecto), **sello de unidad social**.
4. **Limpieza total** de remanentes de pruebas ("arrancar de cero").
5. **Tres órdenes nuevas (2026-10-03):** (a) cerrar fases de LOBO + informe y manual; (b) mejoras para Seawolf Agent sin dañar Hermes; (c) 3 planes de venta.
6. **Pivote clave:** el Monarca declara **Seawolf Agent = producto insignia** y pide dedicarle el estándar que merece (esta sesión de revisión).
7. **Decisión de mando:** el modelo de Bellion (`deepseek-v4.1-flash`) queda **fijado**; no degradarlo a gratis.

---

## 2. LO CONSTRUIDO EN LOBO (contexto, no objeto de la próxima sesión)

- **Base:** `CopilotKit/openmuse` (MIT) en VPS `/opt/nereus`; puerto **8788**; **Node 24**.
- **Fases cerradas:** 0 (build) · 1 (persistencia propia Postgres+pgvector) · 2 (gateway OpenRouter) · 3 (voz: voice-gateway por frases, VoiceBox) · 4 (memoria: **Mem0** semántica + **Graphiti/Neo4j** temporal).
- **Marca:** rebranding de la app (9 archivos + `app.json`), textos al **español** (100 + 257 traducciones), **contraste** corregido (18 fondos blancos + ternarios), **mascota lobo negro** transparente, **tema oscuro/claro** con toggle.
- **Limpieza:** reinicio de fábrica (script `reset-lobo.sh`) → arranca en cero (identidad **LOBO**, 0 tareas, 0 memoria, chat vacío).
- **Calidad:** suite **276/276** tras corregir mi propio daño (IDs del demo + test de marca).
- **Coste:** chat con modelo **gratis**; fondo con modelo muy económico.

---

## 3. LA CORRECCIÓN DE CRITERIO (lo más importante de esta sesión)

**Mi error (corregido):** había escrito que LOBO y Seawolf Agent eran "**una sola base, dos empaques**". **Falso.**

| | **Seawolf Agent** (insignia) | **LOBO** (personal) |
|---|---|---|
| **Base** | **Hermes Agent + Hermes WebUI** | **CopilotKit/OpenMuse** |
| **Stack** | Python 3.12 + JS vanilla | TypeScript / React Native |
| **Naturaleza** | Corporativo (Cliente Súper Ocupado) | Personal |
| **Propósito** | Filtrar ruido + automatizar + dashboard (WhatsApp-first) | Asistente personal |
| **Repo** | `seawolf-studio/seawolf-agent` | Proyecto NEREUS (VPS `/opt/nereus`) |

**Consecuencia operativa:** toda mejora se implementa en **el stack propio de Seawolf Agent (Hermes)**, extendiendo (plugin / MCP / skill / config / skin) — **nunca** tocando el núcleo de Hermes.

---

## 4. ESTADO REAL DE SEAWOLF AGENT (lo que sabemos hoy)

- **Base:** **Hermes Agent (Nous Research)** + **Hermes WebUI** (Python + JS vanilla, sin bundler).
- **Marca/rebrand:** WebUI con skin Seawolf, **100% español**, logo lobo.
- **Dominio:** `https://agente.sw-st.net` (Cloudflare SSL Full Strict).
- **VPS:** Hostinger `76.13.109.237` (root@).
- **Gateway:** servidor OpenAI-compatible en puerto **8642** (`config.yaml`), modelos GPT-4o / 4o-mini / Claude.
- **Composio:** SDK Python conectado con **Gmail**.
- **Dashboard COP:** base construida (FastAPI + SQLite + Alpine.js); requiere UI estable.
- **Pendiente:** WhatsApp (composer + API), pasarela de pagos COP, mem0/memoria por cliente.
- **Doctrina:** `MANIFIESTO_PRODUCTO_CSO.md` (3 capas: Filtro → Automatización → Dashboard; 5 diferenciadores; precios $50–100/mes).

---

## 5. MEJORAS A IMPLEMENTAR EN SEAWOLF AGENT (resumen — ver doc completo)

**Regla de oro:** extender Hermes (plugin/MCP/skill/config/tema), **nunca** fork del núcleo.

- **Confianza:** Audit Trail SHA-256 encadenado · RBAC (Creador→Admin→Auxiliar→Operativo) · aprobaciones deny-by-default · aislamiento por cliente · cifrado de secretos.
- **Coste:** gateway con presupuesto y fallback · medidor de tokens/coste por cliente.
- **Memoria:** memoria por cliente con inspeccionar/corregir/olvidar · retención/borrado por política.
- **Canal:** **WhatsApp-first** con clasificación de ruido · español nativo · skin con oscuro por defecto + sello social.
- **Operación:** onboarding 1-click · observabilidad + alertas (Telegram/n8n) · backups/reset por cliente · manual.
- **Negocio:** Composio (acciones) · Dashboard COP · pasarela de pagos · multi-vertical.

**Prioridad #1:** RBAC + Audit visibles · WhatsApp-first + clasificación · onboarding 1-click + español.

---

## 6. DECISIONES DE MANDO (vigentes)

1. **Dos productos separados** (Seawolf Agent insignia · LOBO personal). No mezclar.
2. **Modelo de Bellion fijado:** `deepseek-v4.1-flash` (gratis/baratos solo para fondo y LOBO).
3. **No tocar el núcleo de Hermes** (extender, no fork).
4. **Reinicio de fábrica antes de entregar** a un cliente (patrón heredado de LOBO).
5. **Beastias proscritas:** Shopify, AdSense, burocracia de Facebook — nunca.
6. **Constantes de marca:** LOBO (mascota lobo negro) · modos claro/oscuro con **oscuro por defecto** · sello de unidad social · colores `#121E1E`/`#4CE8E7`/`#48E8D8`.

---

## 7. INVENTARIO DE ACTIVOS DE ESTA SESIÓN

**Repos y commits (repo `seawolf-agent`, branch master):**
- `c710bb2` informe+manual LOBO, mejoras Seawolf Agent, 3 planes de venta.
- `1865afe` criterio corregido (dos desarrollos distintos).
- (LOBO en VPS `/opt/nereus`: commits `92e9fd9` → `774d70c`.)

**Informes (MD + PDF) en `intel/`:**
- `lobo-informe-final-y-manual-20261003` — informe final + manual de uso de LOBO.
- `seawolf-agent-mejoras-20261003` — mejoras (criterio corregido).
- `seawolf-agent-3-planes-venta-20261003` — 3 planes de venta.
- `plan-nereus-*`, `fase-{0,1,2,3}-nereus-*`, `nereus-*` — ingeniería de LOBO.

**Scripts LOBO (VPS `/opt/nereus`):** `reset-lobo.sh` (reinicio de fábrica), `deploy2.sh`, `chat-test.sh`, `rebrand.py`, `theme-i18n.py`, etc.

**Servicios LOBO (systemd):** `nereus-api`, `nereus-web`, `nereus-mem0`, `nereus-graphiti`, `seawolf-fw`.

---

## 8. AGENDA PROPUESTA PARA LA PRÓXIMA SESIÓN (revisión de Seawolf Agent)

1. **Reconocimiento del sistema real:** leer `seawolf-webui/{README,ARCHITECTURE,ROADMAP,CONTRACTS}.md`, `docs/rfcs/`, `config.yaml`, `DEPLOY.md`; inventariar servicios, puertos y estado en el VPS.
2. **Evaluación:** comparar estado real vs MANIFIESTO (Filtro/Automatización/Dashboard) y vs los 5 diferenciadores.
3. **Errores:** reproducir y corregir fallos (arranque, onboarding, streaming, aprobaciones, multi-perfil).
4. **Mejoras:** implementar por prioridad #1 (RBAC+Audit visibles, WhatsApp-first, onboarding 1-click, español) **sin tocar el núcleo de Hermes**.
5. **Verificación:** pruebas del repo (`./scripts/test.sh`) + prueba end-to-end real en `agente.sw-st.net`.
6. **Cierre:** nuevo informe + actualización de `PROTOCOLO_MEMENTO.md`.

---

## 9. PREGUNTAS ABIERTAS / RIESGOS

- **Hosting:** ¿cada cliente en su VPS o **multi-tenant** central? (decisión del MANIFIESTO pendiente).
- **WhatsApp:** canal oficial (Meta) vs puente no oficial (riesgo ToS) — el Monarca aborrece la burocracia de Meta.
- **Pagos:** pasarela COP por definir (Wompi/Epayco/Stripe).
- **Marca:** ¿la WebUI de Seawolf Agent también adopta el **lobo** de LOBO o mantiene identidad propia? (definir para no confundir los productos).

> *"Una versión débil de Bellion hizo a Seawolf Agent — el producto insignia. Ahora la estrella recibe el trato digno que merece."*
> — el Monarca, 2026-10-03
