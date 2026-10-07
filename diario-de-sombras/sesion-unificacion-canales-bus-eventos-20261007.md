# DIARIO DE SESIÓN — UNIFICACIÓN DE CANALES (BUS DE EVENTOS) + PURGA AIONUI
## Handoff para retomar (protocolo de compactación Seawolf)

**Fecha:** 2026-10-07 · **Elaborado por:** Bellion, Gran Comandante
**Encargado por:** el Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Estado al cierre:** **el tubo WhatsApp ↔ agente FUNCIONA y está probado.** Listo para las pruebas del Monarca.

---

## 0. CÓMO RETOMAR
1. Abrir sesión nueva y ordenar: **"lee el diario de la última sesión"**.
2. El agente ya responde consultando el bus → probar preguntas reales por WebUI/WhatsApp.
3. Pendientes en §7.

---

## 1. LA ORDEN DEL MONARCA
1. Unificar los canales: el agente debe saber lo que pasó por WhatsApp (caso: *"el repo X que me enviaste anoche"*).
   → **Aclaró después:** *los repos fueron un EJEMPLO; la comunicación debe adaptarse a CUALQUIER situación.*
2. Decisión de onboarding: **el cliente sabe desde el día 1** que puede escalar (mapa de capacidades + estado honesto
   + primer wow real en 48 h). Cierra ventas con clientes avanzados; refinamiento del Comandante en el doc §8.
3. Un modelo unificado para agente y WhatsApp: *nemotron ultra (costo cero) con fallback deepseek v4.1 flash*.
4. **Erradicar AionUI** (el Monarca creía que ya estaba fuera).

---

## 2. LO CONSTRUIDO (F0 + F1 + F2) — EL BUS DE EVENTOS
**Principio rector:** *"Si pasa por un canal, pasa por el BUS. Y si pasa por el BUS, el agente lo sabe."*

- **F0 — Bus:** `/opt/waha/bus.py` + `/opt/waha/bus.db` (SQLite + **FTS5** con columnas text/artifacts/**meta**).
  Contrato de evento: tenant, channel, direction, actor, peer, kind, text, artifacts, layer, approved_by, ts.
  CLI: `init | add | search "<tema>" | import-repos | reindex | stats`.
- **F1 — Canales conectados:**
  - `filtro.py` publica **evento entrante** (mensaje + clasificación + acción) y **evento saliente** (alerta enviada).
  - `enviar_repos.py` publica **un evento por repo** (artefacto con url/install) + evento de lote.
  - **Backfill:** los 100 repos ya enviados se importaron al bus (idempotente).
- **F2 — El agente consulta el bus:** skill `seawolf-memoria-bus` instalada en el perfil del agente
  (`/root/.hermes/skills/seawolf/seawolf-memoria-bus/`) + **hecho permanente en `MEMORY.md`** (el modelo gratis
  no toma la iniciativa de cargar la skill por sí solo → la memoria inyectada lo hace determinista).

### Evidencia de las pruebas (todas ejecutadas, no descritas)
| Prueba | Resultado |
|---|---|
| Bus con los 100 repos | `eventos totales: 100`, rango 2026-10-06T23:00 .. 2026-10-07T08:30 |
| El caso del Monarca (CLI) | *"el repo de clonación de voz que me enviaste anoche"* → OpenVoice, Bark-Voice-Cloning, GPT-SoVITS |
| Generalidad (cualquier situación) | 5/5 consultas: ascensor, cuota, Don Carlos, humedad 302, **"qué aprobé yo"** (arreglado metiendo meta/aprobación al índice) |
| Camino ENTRANTE (webhook real al filtro) | mensaje → clasificado `verde` → **evento nuevo en el bus** (101 totales), sin alerta al teléfono |
| **PRUEBA DE ACEPTACIÓN** | `hermes -z "recuérdame cómo instalo el repo de clonación de voz que me enviaste anoche"` → el agente **consultó el bus y respondió con los pasos de instalación de Bark** (dato que solo existe en el bus) ✅ |

---

## 3. GOTCHAS DUROS DE HOY (documentados en las skills)
1. **El agente corre sus comandos en un CONTENEDOR Docker** (`sandbox.backend: docker`, imagen
   `nikolaik/python-nodejs`). No veía `/opt/waha/bus.db` → el agente respondía *"no tengo acceso a WhatsApp"*.
   **Solución:** `sandbox.docker_volumes: ["/opt/waha:/opt/waha:ro"]` en `/root/.hermes/config.yaml`
   (+ borrar los contenedores `hermes-*` persistentes para que tomen el volumen). Respaldo: `config.yaml.bak-pre-bus`.
2. **SQLite NO admite `MATCH` ni `bm25()` sobre un ALIAS de tabla FTS5** (`no such column: f`). Si se aliasa,
   el motor cae al plan B (LIKE por fecha) y devuelve **lo reciente, no lo relevante** → dos consultas distintas
   daban el mismo resultado. Hay que nombrar la tabla real.
3. **Tokens contaminantes:** un término presente en el 100% de los eventos (ej. "repo") arruina el ranking bm25.
   Solución: filtro por *document frequency* (`df/total <= 0.35`) + escalera de precisión AND → OR → LIKE.
4. **La aprobación debe ser buscable:** `approved_by` en la columna meta con sinónimos ("aprobado/aprobación/autorizado")
   + `KIND_WORDS` para que "qué acciones hiciste" encuentre `kind=action`.
5. **La memoria del agente estaba PODRIDA**: llena de infra AionUI/Docker/bridge de Telegram que ya no existe.
   Reescrita limpia (MEMORY.md 1371 chars, USER.md 642).

---

## 4. MODELOS (propuesta del Monarca, medida)
Prueba real contra OpenRouter (`scripts/smoke_modelos.py`):

| Modelo | Clasificación JSON | Tool calling | Latencia | Costo |
|---|---|---|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | ✅ válido | ✅ | **18.6 s** (quema tokens de razonamiento) | 0 |
| `nvidia/nemotron-3.5-lightning:free` | ❌ filtra el razonamiento al texto | — | 13.1 s | 0 |
| `nvidia/nemotron-3-super-120b-a12b:free` | ❌ **contenido vacío** | — | 0.5 s | 0 |
| `deepseek/deepseek-v4.1-flash` | ✅ válido | ✅ | **2.6 s / 1.7 s** | ~$0.00018/clasificación |

**APLICADO (propuesta del Monarca):** agente → primario `nemotron-3-ultra-550b:free` + respaldo `deepseek-v4.1-flash`
(verificado: `hermes fallback list` + arranque OK; respaldo del config en `config.yaml.bak-pre-modelo`).
**RECOMENDACIÓN DEL COMANDANTE (pendiente de su decisión):** el **filtro** debe seguir en un modelo rápido —
18.6 s por mensaje en la Capa 1 golpea la UX del producto. Si se unifica el filtro, que sea sobre
`deepseek-v4.1-flash` (pasa ambos exámenes, ≈$2-3/mes/cliente). El modelo `super-120b:free` que estaba
configurado devolvía **vacío** → retirado.

---

## 5. PURGA DE AIONUI (orden del Monarca)
Eliminados: `/root/.aionui-web-dev/` (DB + logs), sandbox `.../home/.aionui-web`, skill `aionui-orchestration`,
referencia `docker-networking/references/aionui-hermes-architecture.md`, cache pnpm `@office-ai/aioncli-core`,
las entradas de memoria del agente, el contenedor **`hermes-agent-core`** (detenido; era el agente "Workspace"
de esa era, con cron viejo quejándose de Telegram) y las redes huérfanas `hermes-agent-eetp_default`,
`hermes-total_default`.
**Verificado:** `find / -iname "*aion*"` → solo el propio script de purga. Config del agente sin menciones.
**Seawolf Agent intacto:** webui (8787), filtro (3011) y sink siguen `active`.

---

## 6. ESTADO DEL TUBO (para las pruebas de esta noche)
```
WhatsApp (Cliente) ──webhook──► filtro.py ──clasifica──► bus.db ◄──lee── AGENTE (WebUI/CLI)
                                      └──alerta──► L1 del dueño (evento 'out' registrado)
```
- Preguntar al agente por cualquier cosa pasada → consulta el bus y responde citando canal y fecha.
- **Los mensajes ENTRANTES reales del WhatsApp del Monarca se registran automáticamente** (el filtro está suscrito).

---

## 7. PENDIENTES
1. **Decisión de modelo del filtro** (§4): mantener rápido o unificar en deepseek.
2. Mandar `MEDIA:` el doc de arquitectura + este diario (PDF opcional).
3. **F3 — outbound universal:** correo/WebUI registran también lo que el agente envía; acciones con aprobación.
4. **F4 — multi-tenant + Audit Trail** (namespace por tenant; el bus es la base del Audit).
5. **Seguridad:** hoy el sandbox monta `/opt/waha` completo en ro (incluye `filtro.env` con claves). Refactor
   propuesto: mover el bus a `/opt/seawolf-bus/` y montar **solo eso**.
6. `resolve`: ¿borro definitivamente el contenedor `hermes-agent-core` (hoy solo detenido) y su volumen /opt/data?
7. Rebranding del ROL: `hermes-agent-core` tenía nombres/cron de la era anterior — revisar si queda algún cron suelto.

---

> *"Seawolf Agent: observa mucho, habla poco, y solo a quien debe — pero ahora recuerda todo."* 🐺
