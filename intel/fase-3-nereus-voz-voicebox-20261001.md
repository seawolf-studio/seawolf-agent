# INFORME DE EJECUCIÓN — FASE 3 (parcial) "SEAWOLF NEREUS"
## Voz: VoiceBox desplegado y operativo + medición de latencia

**Fecha:** 2026-10-01 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Objetivo:** montar el programa de voz (VoiceBox) para clonar la voz por defecto y medir latencia real en CPU antes de gastar en GPU.
**Resultado:** ✅ **VoiceBox desplegado y generando voz.** Latencia medida. Pendiente: tu archivo de voz para completar la clonación de la voz de marca.

---

## 1. DECISIÓN DEL MONARCA (cerrada)
- **Dos voces de marca, español latino:** una **masculina** (sintetizada por el Monarca de una voz de **dominio público** con Audacity — pendiente de subir) y una **femenina**.
- **Clonación de voz del usuario** disponible, con **advertencias** explícitas (solo voz propia / con derechos).

---

## 2. LO QUE SE DESPLEGÓ

| Pieza | Estado |
|-------|--------|
| **VoiceBox v0.5.0** (motor **Qwen3-TTS** + Kokoro + Whisper) | ✅ En Docker, `restart unless-stopped` |
| Imagen construida | ✅ **12.6 GB** (build CPU) |
| Modelo **Qwen3-TTS-12Hz-1.7B-Base** | ✅ Descargado (**4.3 GB** en caché HF) |
| API + UI + **servidor MCP** (`/mcp`) | ✅ `/health` 200 |
| Persistencia (perfiles, generaciones) | ✅ Volumen `voicebox-data` |
| **Acceso seguro** | ✅ `http://100.114.5.98:17600` (solo red **Tailscale**) |

**Despliegue aislado:** contenedor `voicebox`, volúmenes y red propios; **sin tocar** los servicios previos del VPS.

---

## 3. CIRUGÍA DE PERMISOS (dos fallos reales corregidos)
1. **`/app/data/generations` no escribible** → el bind-mount `./output` no existía. Creado y corregido → `/health/filesystem` verde.
2. **`PermissionError` al descargar el modelo** → el servidor corre como **uid 999** (`voicebox`), no como root; la caché era root-only. Corregido (`chmod`) → **modelo descargado**.

Sin estas dos correcciones, la clonación habría sido imposible.

---

## 4. VERIFICACIÓN REAL — LATENCIA MEDIDA (CPU)

| Prueba | Resultado |
|--------|-----------|
| TTS end-to-end (Kokoro, ES) | ✅ WAV generado |
| **Latencia en frío** (con carga de modelo) | **15.9 s** para 6.05 s de audio |
| **Latencia en caliente** (la que importa) | **4.1 s** para ~6.7 s de audio ≈ **0.6× tiempo real** |
| Aislamiento | ✅ Otros servicios del VPS intactos |

**Lectura honesta:** en 2 vCPU, una frase tarda ~4 s y produce ~6.7 s de voz → **sirve para notas de voz y turnos pausados, NO para conversación fluida en vivo** (barge-in instantáneo). Confirma la decisión de **medir antes de gastar**: para voz en vivo hará falta **nodo GPU (opción B)** o **TTS en el cliente (opción C)**.

---

## 5. VOCES DISPONIBLES EN ESPAÑOL (para tu decisión)
Adjunto **muestras generadas** (mismo texto) para que elijas de oído:
- **Masculina ES — "Alex"** (`em_alex`) — muestra: `nereus-voz-masculina-alex-ES.wav`
- **Femenina ES — "Dora"** (`ef_dora`) — muestra: `nereus-voz-femenina-dora-ES.wav`

> Nota: **"Santa"** (`em_santa`) falló en la prueba (error transitorio del motor). Se reintentará si interesa.

---

## 6. FLUJO DE CLONACIÓN (listo para tu archivo)
```
POST /profiles                       → crear perfil "NEREUS"
POST /profiles/{id}/samples          → subir TU audio de referencia
POST /generate  {profile_id, text}   → voz clonada
```
Tipos de voz aceptados: `cloned | preset | designed`. Idiomas: incluye **es**.
⚠️ La voz **diseñada** (sin muestra) **falló**: el modelo base exige **embedding de referencia** → **tu archivo es imprescindible** para la voz de marca.

---

## 7. CÓMO SUBIR TU VOZ (cuando llegues)
1. Conéctate a Tailscale (tu PC debe estar en el tailnet del VPS).
2. Abre **`http://100.114.5.98:17600`**.
3. **Profiles → New** → nombre "NEREUS" → sube el clip de tu voz sintetizada → **Generate** para probar.

*(Alternativa sin Tailscale: túnel SSH `-L 17600:127.0.0.1:17600`.)*

---

## 8. LÍMITES Y PENDIENTES
- ⏳ **Voz de marca masculina:** falta tu archivo (dominio público → Audacity).
- ⏳ **Voz femenina oficial:** elegir entre preset (Dora) o clonar una referencia con derechos.
- ⏳ **Advertencias de clonación:** flujo legal/consentimiento por diseñar.
- ⏳ **Pipecat (barge-in):** capa de diálogo en tiempo real — pendiente.
- ⏳ **GPU:** decidir tras esta medición.
- ⏳ Clonación/efectos y comprobación de MCP para integrar con NEREUS.

---

## 9. VEREDICTO DEL COMANDANTE
La voz de NEREUS **ya tiene dónde vivir y ya habla**. El programa está montado, el modelo cargado y la latencia medida con datos, no con promesas. **Falta tu voz** para sellar la marca.

**Fin del informe parcial de Fase 3.**
