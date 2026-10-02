# INFORME — LIMPIEZA DEL VPS + MEM0 OPERATIVO (Fase 4.1)
## Espacio y RAM liberados; memoria semántica funcionando

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. LIMPIEZA EJECUTADA (orden del Monarca)

| Acción | Resultado |
|--------|-----------|
| **Puerto 8787 verificado** | Era **`seawolf-webui.service`** (WebUI de Seawolf Agent) → **INTACTO** |
| **n8n** | Fuera (contenedor + imagen 2,51 GB); **volumen de datos conservado** |
| **VoiceBox** | Fuera (contenedor + imagen 12,6 GB + caché de modelos); **volumen del perfil NEREUS conservado** para migrar al PC |
| **Gateway de voz** | Detenido/deshabilitado (dependía de VoiceBox) |
| **Caché de build Docker** | Purgada (~11,8 GB) |
| **Imagen mem0-dashboard** | Eliminada (no se usa) |

### Recursos: antes → ahora
| | Antes | Ahora |
|---|-------|-------|
| Disco libre | 42 GB | **64 GB** (+22 GB) |
| RAM disponible | ~1,8 GB | **6,4 GB** (+4,6 GB) |
| Imágenes Docker | 22,66 GB | **7,28 GB** |

## 2. SEGURIDAD — PUERTOS CERRADOS
Reglas en la cadena **`DOCKER-USER`** (solo loopback + tailnet + redes docker; el resto **DROP**):
- **8000** y **9443** (Portainer) · **8085** (Hermes)
- Persistidas con `seawolf-fw.service` (systemd, `RemainAfterExit`) → sobreviven reinicios.
- Verificado: los servicios siguen respondiendo en **localhost**.

⚠️ **Pendiente de su decisión:** el **8787 (seawolf-webui)** sigue escuchando en `0.0.0.0`. Es un proceso del host (no Docker), así que no lo cubre `DOCKER-USER`. ¿Lo cerramos también?

## 3. MEM0 OPERATIVO (memoria semántica)
- **Desplegado**: `mem0-dev-mem0-1` (127.0.0.1:8888) + `mem0-dev-postgres-1` (pgvector, healthy).
- **Parche propio**: el servidor Mem0 no aceptaba `base_url`; se parchó para usar **OpenRouter** (LLM + embeddings).
- **Prueba end-to-end (superada)**:
  - **Añadir** → extrajo 2 memorias reales (el LLM las normalizó).
  - **Buscar** semántico → devolvió ambas con *score* (0,68 y 0,49).
  - **Listar** → correcto.
- Autenticación por `X-API-Key` (ADMIN_API_KEY).

## 4. ESTADO Y PENDIENTES
- ✅ Limpieza y seguridad aplicadas.
- ✅ Mem0 (memoria semántica) probado con OpenRouter.
- ⏳ **Integrar Mem0 en NEREUS** (ruta `memories` + `remember_fact` → semántico; prompts recuperan solo lo relevante).
- ⏳ **Graphiti** (capa temporal/auditoría) — Fase 4b.
- ⏳ **VoiceBox → PC** (migrar el perfil NEREUS conservado).
- ⏳ Decidir sobre **8787** y sobre **Portainer** (¿se queda?).

## 5. VEREDICTO DEL COMANDANTE
VPS **aligerado y asegurado** (64 GB y 6,4 GB libres), y la **memoria semántica ya funciona** con nuestro gateway. Queda integración en el agente y el nivel temporal. Terreno listo para pruebas completas.

**Fin del informe.**