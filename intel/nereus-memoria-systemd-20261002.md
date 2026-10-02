# INFORME — MEM0 Y GRAPHITI BAJO SYSTEMD (cierre de infraestructura)
## Los servicios de memoria aguantan reinicios

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. LO QUE SE HIZO
- **Unidades systemd** (tipo `oneshot`, `RemainAfterExit`, `enabled`):
  - `nereus-mem0.service` → levanta `mem0` + `postgres` (pgvector).
  - `nereus-graphiti.service` → levanta `graphiti-mcp` + `neo4j`.
- **Política `restart: unless-stopped`** añadida a los contenedores vía override (Docker los revive si mueren).
- **Puertos solo en localhost** (8888/8432 Mem0, 8100/7474/7687 Graphiti).

## 2. VERIFICACIÓN
| Comprobación | Resultado |
|--------------|-----------|
| `systemctl is-enabled` | ✅ `mem0` y `graphiti` |
| `systemctl is-active` | ✅ `active`/`active` |
| Contenedores | ✅ mem0 (200), postgres healthy, graphiti-mcp healthy, neo4j healthy |
| Salud HTTP | ✅ `mem0=200`, `graphiti=200` |

## 3. INVENTARIO SYSTEMD DE NEREUS
| Unidad | Rol |
|--------|-----|
| `nereus-api.service` | Servidor NEREUS |
| `nereus-mem0.service` | Memoria semántica (Mem0 + pgvector) |
| `nereus-graphiti.service` | Memoria temporal (Graphiti + Neo4j) |
| `nereus-voice-gateway.service` | (detenido) voz — pendiente migrar a PC |
| `seawolf-fw.service` | Endurecido de puertos Docker |
| `voicebox` (Docker) | (retirado) |

## 4. ESTADO
- ✅ Fase 4 (memoria) **cerrada y persistente**: Mem0 + Graphiti integrados, probados y bajo systemd.
- ✅ Coste de IA: gratis / céntimos.
- ⏳ VoiceBox → PC (perfil NEREUS conservado).
- ⏳ Pruebas integrales del sistema completo.

## 5. VEREDICTO DEL COMANDANTE
La memoria de NEREUS **vive, recuerda y sobrevive reinicios**. Infraestructura cerrada y ordenada. Terreno listo para las **pruebas integrales** que el Monarca anunció.

**Fin del informe.**
