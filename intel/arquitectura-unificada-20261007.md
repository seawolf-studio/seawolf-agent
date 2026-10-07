# ARQUITECTURA UNIFICADA — SEAWOLF AGENT
## Un agente · N canales · UNA sola memoria (bus de eventos)

**Fecha:** 2026-10-07 · **Autor:** Bellion, Gran Comandante
**Encargado por:** el Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Estado:** propuesta para aprobación · **Origen:** sesión de filtro WhatsApp Capa 1 (2026-10-06)

---

## 0. EL CASO QUE DESTAPÓ EL PROBLEMA (palabras del Monarca)

> *"Estoy frente a mi Seawolf Agent y le digo: «oye, me acabo de acordar de un repo de los que me
> enviaste anoche, se llama X — recuérdame cómo lo instalo» — y el agente no sabe, porque no tiene
> la información de los repos que se enviaron al WhatsApp anoche. Hay que conectarlos."*

**Veredicto del Comandante: el Monarca tiene razón. Hoy el agente NO sabría.**
No es un detalle de UX: es que **hay dos cerebros y ningún puente entre ellos.** Mientras existan
dos, Seawolf Agent se puede comprar en pedazos (y el pedazo barato gana). Este documento define la
unificación, y el caso de los repos es su **prueba de aceptación**.

---

## 1. REALIDAD HOY (recon 2026-10-07, con evidencia)

Lo que existe y dónde vive cada cosa (verificado por SSH/comandos, no supuesto):

| Pieza | Dónde vive | Qué guarda | ¿El agente lo ve? |
|---|---|---|---|
| **Filtro WhatsApp (Capa 1)** | VPS `/opt/waha/filtro.py` · `seawolf-filtro.service` · `172.16.0.1:3011` | Clasificación, log `/opt/waha/filtro.log` | ❌ No |
| **Envío de los 100 repos** | VPS `/opt/waha/enviar_repos.py` + cron + `repos_desc.jsonl` (100 líneas) + `repos_idx` (=100) | El texto de cada repo, en un **archivo suelto** | ❌ No |
| **Agente (la cara)** | VPS `/opt/seawolf-webui` · `seawolf-webui.service` (puerto 8787) | Sesiones de chat, WebUI | — |
| **Memoria del agente** | Perfil Hermes: `MEMORY.md` = **2.179 bytes** (límite 2.200) + `USER.md` + `state.db` | Solo hechos permanentes, minúsculo | Parcial |
| **Bus de mensajes WAHA** | `waha-sink.service` · `messages.log` (1,5 MB) | Crudo, sin estructura, sin retrieval | ❌ No |
| **Patrón de memoria avanzada** | VPS `/opt/nereus`: `nereus-mem0.service` (Mem0 + pgvector) y `nereus-graphiti.service` (Graphiti + Neo4j `:7687/:7474`) | Memoria semántica y grafo temporal | ⚠️ Es de **LOBO/NEREUS** |

**Diagnóstico:**
1. El pipeline de repos es un programa **aislado**: escribe a un `.jsonl` y envía por WAHA. Cuando
   termina, **no deja ni un solo rastro en la memoria del agente**. El agente literalmente no sabe
   que *él mismo* envió esos 100 repos.
2. La memoria del agente (2.2 KB inyectados en cada prompt) **nunca** podría contener 100 repos
   (~65 KB de datos). La memoria del prompt no es un almacén; es un recordatorio de identidad.
3. NEREUS ya resolvió este problema en LOBO (Mem0 + Graphiti). **Es un patrón, no código**: se
   reutiliza el diseño (memoria de hechos + memoria semántica + grafo temporal), no la instancia.

---

## 2. PRINCIPIO RECTOR (la frase que ordena todo)

> ### *"Si pasa por un canal, pasa por el BUS. Y si pasa por el BUS, el agente lo sabe."*

Una sola memoria por tenant. Ningún canal habla con archivos sueltos: todo canal **publica eventos**
al bus, y el agente **lee del bus**. El filtro de WhatsApp deja de ser "una app aparte" y pasa a ser
**el adaptador del canal WhatsApp** (su Capa 1).

---

## 3. ARQUITECTURA

```
                        ┌──────────────────────────────────────────────┐
                        │            SEAWOLF AGENT — NÚCLEO            │
                        │   un tenant = un agente (aislado)            │
                        │                                              │
                        │   (1) MEMORIA DE HECHOS   → identidad/reglas │
                        │   (2) EVENT LOG           → qué pasó y cuándo│
                        │   (3) ÍNDICE SEMÁNTICO    → retrieval natural│
                        └──────────────────▲───────────────┬───────────┘
                                           │ LEE           │ ESCRIBE
                        ┌──────────────────┴───────────────▼───────────┐
                        │              BUS DE EVENTOS                  │
                        │  {tenant, canal, dir, quién, qué, artefactos,│
                        │   ts, id} — append-only, auditable           │
                        └──▲──────▲───────▲──────────▲───────▲─────────┘
                           │      │       │          │       │
                   ┌───────┘  ┌───┘   ┌───┘      ┌───┘   ┌───┘
                   │          │       │          │       │
             ┌─────┴───┐ ┌────┴───┐ ┌─┴──────┐ ┌─┴─────┐ ┌┴────────┐
             │WhatsApp │ │ WebUI  │ │ Correo │ │Calend.│ │ CLI/TUI │
             │ L1/L2   │ │ (chat) │ │ Gmail  │ │       │ │         │
             └─────┬───┘ └────────┘ └────────┘ └───────┘ └─────────┘
                   │
          CAPA 1 FILTRO ──► CAPA 2 ACTÚA ──► CAPA 3 DASHBOARD
          (qué pasa)        (con aprobación)   (lo ve y lo audita)
                  └──── MISMA escalera · MISMO bus · MISMO producto ────┘
```

**Lectura de la arquitectura:**
- **Entrada:** cualquier canal escribe al bus (mensaje recibido, aviso enviado, media transcrita…).
- **Salida:** el agente escribe al bus y los adaptadores entregan al canal que corresponda. **Todo
  saliente se registra** — por eso el agente sabe "yo envié esto".
- **La WebUI y WhatsApp son ventanas del mismo cerebro.** Preguntar en el chat "¿cómo instalo el
  repo X que me mandaste anoche?" es consultar el event log + el índice semántico: el agente
  encuentra el evento y su artefacto, sin importar por qué canal entró.

---

## 4. LAS TRES MEMORIAS (por qué tres y no una)

| # | Memoria | Contenido | Tecnología | Quién escribe |
|---|---|---|---|---|
| 1 | **De hechos** | Identidad del cliente, contactos y roles, reglas, vocabulario, horas de silencio | `MEMORY.md`/`USER.md` del tenant (o tabla `facts`) | Onboarding + correcciones |
| 2 | **Episódica (event log)** | Cada entrada/salida por cualquier canal, con artefactos y timestamp | Tabla append-only (SQLite→PostgreSQL por tenant) | **Todos los canales** |
| 3 | **Semántica** | Embeddings sobre el event log y los artefactos, para recordar por lenguaje natural | `pgvector` (patrón NEREUS/Mem0) + grafo temporal (patrón Graphiti) | Indexador asíncrono |

**Regla:** la memoria de hechos se inyecta en el prompt (es pequeña y permanente). La episódica y la
semántica **se consultan** — el agente las busca cuando las necesita. Así la memoria crece sin
inflar el prompt ni el costo.

---

## 5. CONTRATO DE EVENTO (el mínimo, para no inventar dos esquemas distintos)

```json
{
  "id": "evt_20261007_000123",
  "tenant": "monarca",
  "channel": "whatsapp",            // whatsapp | webui | email | calendar | cli
  "direction": "out",               // in | out
  "actor": "seawolf-agent",         // quién habla (agente, contacto, sistema)
  "peer": "self:L1",                // destinatario/remitente
  "kind": "artifact_delivery",      // message | alert | artifact_delivery | action | audit
  "text": "Repos 96-100 de 100 …",
  "artifacts": [                    // lo que hace recuperable el caso de los repos
    {"type": "repo", "name": "owner/repo", "url": "https://github.com/…",
     "stars": 12000, "license": "MIT", "install": "…"}
  ],
  "layer": 1,                       // 1 filtro | 2 automatización | 3 dashboard
  "approved_by": null,              // si fue acción a tercero, quién aprobó
  "ts": "2026-10-07T03:30:00Z"
}
```

---

## 6. LA PRUEBA DE ACEPTACIÓN (el caso del Monarca, textual)

**Escenario:** los 100 repos se envían por WhatsApp (cron, anoche).

**Pasos:**
1. El pipeline de repos **deja de escribir solo al `.jsonl`** y publica **1 evento por repo**
   (`kind=artifact_delivery`, con `url`, `install` y `texto`) + 20 eventos de lote.
2. El indexador cargue esos eventos al índice semántico del tenant.
3. Al día siguiente, en el **WebUI** (u otro canal), el Monarca escribe:
   *"recuérdame cómo instalo el repo X que me enviaste anoche"*.

**Criterio de aceptación (binario):**
- ✅ El agente **identifica el repo X por nombre** (aunque él no lo recuerde exactamente).
- ✅ Responde con **URL + instrucciones de instalación** sacadas del artefacto.
- ✅ **Cita la fuente interna**: canal (WhatsApp), fecha/hora del envío (evento).
- ✅ La consulta funciona igual si el Monarca pregunta por otro canal o por otro día.

**Si falla cualquiera de los cuatro → la unificación NO está hecha.** Este test se corre antes de
dar por cerrada la fase, y queda registrado como evidencia.

---

## 7. FASES DE IMPLEMENTACIÓN (sombras asignadas)

| Fase | Trabajo | Sombra | Entregable / evidencia |
|---|---|---|---|
| **F0** | Definir el contrato de evento y el almacén (tabla append-only + nombres por tenant) | **Igris** | Esquema + migración mínima |
| **F1** | **Adaptador WhatsApp**: `filtro.py` y `enviar_repos.py` publican al bus (no a archivos sueltos) | **Igris** | 100 eventos visibles en el log del bus |
| **F2** | **Índice semántico + herramienta de retrieval** expuesta al agente (patrón NEREUS: pgvector) | **Igris** + **Jima** | El agente responde el caso X (§6) |
| **F3** | **Outbound universal**: todo saliente (avisos, respuestas, correos) se registra en el bus | **Tank** | Un saliente aparece como evento |
| **F4** | **Multi-tenant + Audit Trail**: namespace por tenant; cada evento es auditable | **Tank** + **Beru** | Aislamiento probado con 2 tenants |
| **F5** | **Onboarding**: mapa completo de capacidades + **estado honesto** (activo/en desarrollo/disponible en X) desde el día 1, y **primer wow real en 48 h** | **Igris** + **Greed** | Draft v2 + mapa de capacidades + guion de arranque |
| **F6** | **Copy de venta** reescrito: el filtro es un bullet del agente, no un producto | **Greed** | 1-pager v2 + planes v2 |
| **F7** | **Auditoría** del conjunto y Audit Trail de ejemplo como pieza de confianza | **Beru** | Reporte + ejemplo |

**Secuencia recomendada:** F0 → F1 → F2 (esto ya responde el caso del Monarca y es el hito que
prueba que hay UN solo cerebro) → luego F3–F7.

---

## 8. DECISIONES ABIERTAS (requieren al Monarca)

1. **Transparencia de la escalera — DECIDIDO (2026-10-07, Monarca): el cliente lo sabe desde el
   día 1.** Razón del Monarca: *"el efecto wow que sea desde el principio; eso cerrará ventas de
   clientes más experimentados, con conocimiento de tecnología, automatizaciones o IA — dirán «ya
   tienen esto implementado, qué bueno» y no se irán a otras alternativas buscando eso que ya
   tenemos pero no vieron desde el primer momento."*
   **Refinamiento del Comandante (mapa ≠ desbloqueo):** transparencia total de **capacidades**,
   activación **progresiva**. El arranque se compone de tres movimientos:
   - **(a) El mapa completo, el día 1** — el cliente ve TODO lo que el agente puede llegar a hacer
     (Capa 1 filtro → Capa 2 acciones → Capa 3 dashboard), para que no busque afuera lo que ya hay.
   - **(b) El estado honesto** — junto a cada capacidad, su estado real: **activo hoy** / **en
     desarrollo** / **disponible en X**. Un cliente experto **prueba en el día 1**: prometer lo que
     aún no existe es lo único que destruye su confianza (y es peor que no anunciarlo).
   - **(c) El primer wow REAL en 48 h** — su propio WhatsApp filtrado con sus mensajes reales. El
     mapa cierra la venta; el wow entregado la sostiene. Un mapa sin primera entrega es una promesa.
   **Regla de retención del cliente avanzado:** hitos visibles y periódicos (roadmap visible) — un
   cliente técnico no se va por falta de funciones, se va cuando cree que estamos detenidos.
2. **Almacén:** ¿SQLite por tenant (simple, ya probado) o PostgreSQL central (escala, como NEREUS)?
3. **Grafo temporal:** ¿se suma Graphiti-patrón ya en F2, o se pospone a F4 (multi-tenant)?
4. **Retención/privacidad:** cuánto tiempo se guarda el event log y qué se borra a pedido del cliente
   (arma de venta: "usted controla su memoria").

---

## 9. RIESGOS

| Riesgo | Mitigación |
|---|---|
| El bus se vuelve un vertedero (costo de embeddings) | Indexar asíncrono y por lotes; hechos pequeños en prompt, resto on-demand |
| Dos fuentes de verdad otra vez (archivo + bus) | **Regla dura:** los canales escriben SOLO al bus; el archivo pasa a ser caché desechable |
| Costo por cliente sube | Embeddings baratos; probar el margen con el test de los 100 repos |
| El agente "recuerda" datos del cliente en otro tenant | Namespace por tenant desde F0, **no** retrofit en F4 |
| Ruido: el agente cita cosas irrelevantes | Retrieval con umbral + citar evento (canal/fecha) para que el Monarca pueda auditar |

---

> *"Un número, un agente, toda tu operación. La puerta es WhatsApp; la casa es Seawolf Agent."* 🐺
