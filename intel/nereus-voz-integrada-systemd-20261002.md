# INFORME — VOZ INTEGRADA EN NEREUS + SYSTEMD
## El agente ya habla por su propia pasarela, y sobrevive reinicios

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. QUÉ SE IMPLEMENTÓ

### 1.1 Ruta de voz dentro del agente
**`POST /api/voice/speak`** en el servidor NEREUS — protegida por la sesión del owner (mismo middleware `/api/*`):
- Recibe `{text, profileId?, engine?}`.
- Proxea a la pasarela de voz (por `VOICE_GATEWAY_URL`, por defecto `http://127.0.0.1:8799`).
- Devuelve el **flujo por frases** (audio de la primera frase en ~0.75 s).
- Nuevo campo de config `voiceGatewayUrl`; el `/api/health` ahora reporta `voiceConfigured`.

### 1.2 Servicios persistentes (systemd)
| Unidad | Función | Estado |
|--------|---------|--------|
| `nereus-voice-gateway.service` | Pasarela TTS por frases | ✅ enabled + active |
| `nereus-api.service` | Servidor NEREUS | ✅ enabled + active |
| `voicebox` (Docker) | Motor TTS/STT | ✅ `restart unless-stopped` (ya existía) |

`Restart=always` + arranque automático → **aguanta reinicios y caídas**.

## 2. VERIFICACIÓN END-TO-END (evidencia)
| Prueba | Resultado |
|--------|-----------|
| `/api/health` | ✅ `voiceConfigured: true` |
| `POST /api/voice/speak` con sesión | ✅ **288 KB de audio, 3 frases** |
| Validez del framing | ✅ las 3 frases son WAV válidos (`RIFF=True`), **sin bytes sobrantes** |
| Sin autorización | ✅ **401** (ruta protegida) |
| systemd | ✅ ambas unidades `enabled` y `active` |
| typecheck + lint + build | ✅ limpios |

## 3. CÓMO QUEDA EL FLUJO
```
Cliente (móvil/PC)
   │  POST /api/voice/speak  (con sesión)
   ▼
NEREUS API (8788, systemd)
   │  proxy
   ▼
Voice gateway (8799, systemd)  →  trocea por frases
   │  POST /speak
   ▼
VoiceBox (17600, Docker)  →  Kokoro ES, sin clonación
```
- **Primer audio en ~0.75 s**; el resto fluye por detrás.
- **Todo server-side y persistente** → apto para el cliente que "quiere que su agente le hable ya".

## 4. ESTADO DEL PROYECTO
- ✅ Fase 0 — build.
- ✅ Fase 1 — persistencia propia (sin servicio cerrado).
- ✅ Fase 2 — gateway OpenRouter.
- ✅ Fase 3 — **voz**: motor montado, clon privativo, y **conversacional ligero integrado + persistente**.
- ⏳ Nodo de voz dedicado para la venta (GPU o CPU multinúcleo) — decisión pendiente del Monarca.
- ⏳ Clonación premium (mi voz / la del Monarca) cuando la infra lo permita.
- ⏳ Reporte para auditoría de **Beru**.

## 5. VEREDICTO DEL COMANDANTE
**NEREUS ya escucha (STT), piensa (OpenRouter) y habla (pasarela por frases), todo bajo servicio persistente.** El pilar de voz del producto está **en pie y probado**. Queda el dimensionamiento de infraestructura para la venta, con los números ya medidos.

**Fin del informe de integración de voz.**
