# INFORME — MEMORIA DE NEREUS (Fase 4)
## Mem0 integrado en el agente + Graphiti desplegado y verificado

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. MEM0 → NEREUS (memoria semántica) — INTEGRADO Y PROBADO

### Código desplegado
| Pieza | Cambio |
|-------|--------|
| `apps/server/src/memory.ts` | **NUEVO** — cliente Mem0 (add/search/forget), best-effort (nunca rompe chat/tareas) |
| `engine/conversation.ts` | `remember_fact` → escribe además en Mem0 |
| `engine/routes.ts` | `POST /memories` → alta en Mem0 (guarda `mem0Ids`); `/forget` → borra en Mem0 |
| `engine/model.ts` | Recuerdo **semántico** en el contexto de tareas (`relevantMemories`) |
| `.env` | `MEM0_URL` + `MEM0_API_KEY` |

### Verificación end-to-end (real)
1. **Crear memoria por NEREUS** → `POST /api/agent/memories` devolvió el registro con `mem0Ids: ["4cf3165d-…"]`.
2. **Recall semántico en Mem0** → la búsqueda *"cómo quiere el Monarca que hable Bellion"* devolvió la memoria con **score 0,65**.
3. `typecheck` + `build:server` ✅ · `nereus-api` reiniciado y `active` · `/api/health` OK.

## 2. GRAPHITI (memoria temporal) — DESPLEGADO Y VERIFICADO

- **Backend:** Neo4j 5.26 (más maduro que FalkorDB).
- **Servidor MCP:** *Graphiti Agent Memory v1.29.1*, en `127.0.0.1:8100` (+ Neo4j en 7474/7687, solo localhost).
- **LLM y embeddings:** **OpenRouter** (vía `OPENAI_API_URL`).
- **Verificación MCP:** handshake OK; **herramientas** disponibles (`add_memory`, `search_nodes`, `search_memory_facts`, `get_episodes`, `build_communities`…); **episodio encolado** correctamente en el grupo `nereus`.

### Pitfall resuelto
FalkorDB falló por **incompatibilidad de versión** con `graphiti-core` (API `db.idx.fulltext.createNodeIndex`). Se **cambió a Neo4j** y quedó estable.

## 3. RECURSOS
- RAM: **4,8 GB disponibles** con Mem0 + Graphiti + Neo4j + NEREUS + Postgres corriendo.
- Todos los servicios nuevos en **localhost** (sin exposición pública).

## 4. ESTADO Y PENDIENTES
- ✅ Mem0 semántico integrado y probado dentro del agente.
- ✅ Graphiti desplegado, conectado a Neo4j y respondiendo por MCP.
- ⏳ **Cablear Graphiti en NEREUS** (capa temporal/auditoría: hechos con ventana de validez).
- ⏳ Exponer Mem0/Graphiti vía NEREUS (no directo) y unificar en la ruta `memories`.
- ⏳ Persistencia (systemd) para los nuevos servicios.

## 5. VEREDICTO DEL COMANDANTE
NEREUS ya **recuerda por significado** (Mem0) y tiene **base para recordar en el tiempo** (Graphiti). La memoria dejó de ser una lista plana. Terreno listo para la capa temporal y para pruebas integrales.

**Fin del informe de memoria.**
