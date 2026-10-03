# SEAWOLF AGENT — MEJORAS A IMPLEMENTAR (CRITERIO CORREGIDO)
## Dos servicios, dos desarrollos distintos — las lecciones de LOBO se transfieren como PATRONES, no como código

**Fecha:** 2026-10-03 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Reemplaza a:** `seawolf-agent-mejoras-20261003.md` (v1 — criterio erróneo)

---

## 0. PREMISA CORREGIDA (orden del Monarca)

> **LOBO y Seawolf Agent son DOS servicios y DOS desarrollos distintos. No son dos caras del mismo servicio.**

| | **Seawolf Agent** | **LOBO** |
|---|---|---|
| **Naturaleza** | Agente **corporativo** (Cliente Súper Ocupado) | Agente **personal** |
| **Base tecnológica** | **Hermes Agent (Nous Research) + Hermes WebUI** | **CopilotKit/OpenMuse (MIT)** |
| **Stack** | **Python 3.12 + JS vanilla** (sin bundler), WebUI en `~/.hermes/webui` | **TypeScript / React Native (Expo)** + Postgres |
| **Comprador** | Empresas / profesionales CSO (B2B) | Persona natural (prosumer) |
| **Propósito** | **Filtrar ruido + automatizar + dashboard** (WhatsApp-first) | Asistente personal (escuchar, pensar, hablar) |
| **Repo** | `seawolf-studio/seawolf-agent` (subdir `seawolf-webui`) | Proyecto NEREUS (VPS `/opt/nereus`) |
| **Estado** | Agente live (`agente.sw-st.net`), WebUI funcional, Composio Gmail conectado | Fases 0–4 + marca LOBO; limpio y en pruebas |

**Consecuencia:** las lecciones de LOBO entran a Seawolf Agent como **patrones transferibles** (diseño, operación, control de coste), **jamás** como reutilización de su backend. Cada mejora se implementa **en el stack propio de Seawolf Agent (Hermes)**, no en el de LOBO.

---

## 0.1 REGLA DE ORO — NO DAÑAR HERMES

Toda mejora entra como **una de cinco formas**, sin tocar el núcleo de Hermes:

1. **Plugin** · 2. **Servidor MCP** · 3. **Skill** · 4. **Configuración** (`config.yaml`, `.env`) · 5. **Skin/tema/WebUI**.

**Criterio de descarte:** si algo exige **fork del núcleo** → se descarta o se rediseña como extensión. El núcleo (bucle de razonamiento, tools, CLI, gateway de mensajería) **no se toca**, para poder actualizar Hermes sin rompernos.

---

## A. Confianza y cumplimiento — *el foso del comprador corporativo*
1. **Audit Trail SHA-256 encadenado** con exportación para el cliente. → *Plugin + tabla propia; hoy Hermes ya tiene turn-journal, se firma y se expone.*
2. **RBAC real** sobre la WebUI (roles: Creador → Admin → Auxiliar → Operativo, ya demostrado en el Dashboard COP). → *Plugin + skin.*
3. **Aprobaciones explícitas (deny-by-default)** registradas. → *Hermes ya tiene compuertas de aprobación; se extiende, no se reescribe.*
4. **Aislamiento por cliente** (memoria/contexto separado por conversación/tenant). → *Config + plugin de perfiles.*
5. **Cifrado de secretos** y rotación de claves. → *Plugin.*

## B. Coste y modelos
6. **Gateway con presupuesto por cliente** y **fallback** (gratis → barato → premium). → *`config.yaml` + provider OpenRouter (Hermes ya es provider-agnostic).*
7. **Medidor de uso de tokens/coste** por cliente, con alertas. → *Plugin de observabilidad (Hermes ya estima coste por mensaje).*

## C. Memoria
8. **Memoria por cliente** (perfil + hechos + procedimientos) con **inspeccionar / corregir / olvidar**. → *Hermes ya tiene memoria en capas; se añade el scoping por tenant.*
9. **Retención y borrado por política** (cumplimiento). → *Plugin.*

## D. Canal y experiencia
10. **WhatsApp-first** (el canal donde vive el CSO) con **clasificación de ruido**. → *Conector/plugin; es el corazón del MANIFIESTO, no una capa de LOBO.*
11. **Español nativo** en la WebUI (Hermes WebUI ya trae i18n con 15 locales → se **activa/afina el español**). → *Config/i18n.*
12. **Skin Seawolf** con **modo oscuro por defecto** (constante de marca) + **sello de unidad social**. → *Skin (`skins/seawolf.yaml`).*

## E. Operación y producto
13. **Setup 1-click / onboarding** (la WebUI ya trae onboarding guiado → se adapta al cliente). → *Config + docs.*
14. **Observabilidad**: salud, uso, **alertas por Telegram/n8n** (Hermes ya tiene cron y gateway de mensajería). → *Cron + plugin.*
15. **Backups y "reinicio de fábrica" por cliente**. → *Script + plugin.*
16. **Manual del usuario + onboarding guiado**. → *Documentación.*

## F. Integración de negocio (del MANIFIESTO)
17. **Composio** (Gmail/Drive/Sheets y acciones: cobrar, reservar, reportar). → *MCP/SDK (ya conectado con Gmail).*
18. **Dashboard COP en tiempo real** (FastAPI + SQLite + Alpine.js) como **capa de control** del CSO. → *Servicio propio, no toca a Hermes.*
19. **Pasarela de pagos COP** (Wompi/Epayco/Stripe). → *Servicio propio.*
20. **Multi-vertical** (conjuntos → empresarios/arquitectos/jefes) reutilizando el mismo motor. → *Config por plantilla vertical.*

---

## G. Matriz de prioridad (esfuerzo × impacto)

| Prioridad | Mejora | Esfuerzo | Por qué |
|---|---|---|---|
| **1** | RBAC + Audit Trail visibles | Medio | **Es el argumento de venta** corporativo |
| **1** | WhatsApp-first + clasificación | Alto | **El producto es esto** (MANIFIESTO) |
| **1** | Onboarding 1-click + español | Bajo-Medio | El CSO no perdona fricción |
| **2** | Presupuesto/fallback de modelos + alertas | Bajo | Protege el margen |
| **2** | Backups/reset por cliente | Bajo | Operación repetible |
| **3** | Dashboard COP + Composio | Medio-Alto | Valor, tras cobrar |
| **3** | Memoria por cliente | Medio | Diferencial |
| **4** | Pagos COP | Medio | Necesario para escalar |

---

## H. Lo que **NO** se toma de LOBO (para no confundir los desarrollos)
- **NO** se comparte el motor: LOBO corre sobre OpenMuse (TS); Seawolf Agent sobre Hermes (Python).
- **NO** se copia el front: LOBO es React Native; Seawolf Agent es una WebUI Python+JS.
- **NO** se mezclan bases de datos, repos ni despliegues: son **dos productos separados**.

**Qué SÍ se transfiere (y con valor):**
1. **Control de coste con gateway único + modelos gratis/baratos** → patrón replicable en `config.yaml`.
2. **Persistencia propia y soberanía del dato** → principio aplicable al hosting de Seawolf Agent.
3. **Reinicio de fábrica antes de entregar a un cliente** → paso de provisioning por tenant.
4. **Cuidar el acabado de cara al cliente** (marca, español, tema oscuro) → en la skin/WebUI.
5. **Disciplinar el idioma y la marca** (prohibido dejar remanentes de pruebas) → checklist de entrega.
