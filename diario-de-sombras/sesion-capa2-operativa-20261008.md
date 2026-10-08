# DIARIO DE SESIÓN — SEAWOLF AGENT: CAPA 2 OPERATIVA (C1 + C2)
## El agente que responde, con compuerta de aprobación — probado con un tercero real

**Fecha:** 2026-10-07/08 · **Elaborado por:** Bellion, Gran Comandante
**Para:** el Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Estado al cierre:** Capa 2 (C1+C2) **funcionando en producción**, probada de punta a punta.

---

## 1. LO QUE SE CONSTRUYÓ

### C1 — Motor de respuestas humanas (`/opt/waha/responder.py`, unit `seawolf-responder`)
- **Latencia del modelo = INVISIBLE** (ocurre antes); el aviso "escribiendo…" va **solo los últimos 2-4 s**.
- Primera respuesta no urgente: **15 s a 3 min aleatorio**; 🔥 **rápido** (2-4 s) — la seguridad pesa más que el realismo.
- **Tope de volumen** (20 salientes/hora) + registro de cada saliente en el bus.
- **Modo prueba** (`RESPONDER_TEST_FAST=1`, 4-8 s) para las pruebas con el Monarca.

### C2 — Compuerta de aprobación (deny-by-default)
- El agente **propone** al dueño en **UN SOLO AVISO unificado** (nivel + quién + mensaje + acción sugerida + borrador
  + cómo responder). El filtro **delega** el aviso cuando el motor está vivo (latido `responder_heartbeat`);
  si el motor cae, el filtro alerta solo (resiliencia).
- **Texto libre = ORDEN** (atajos `ok`/`1`/`no`/`silencio Nh` son conveniencia, nunca la única puerta).
- **Decisión por NOTA DE VOZ:** se transcribe (Groq) y se ejecuta; el agente devuelve **eco** de lo entendido.
- **Identidad del dueño** reconocida por LID **o** por número (WhatsApp entrega ambos formatos).
- **Directorio de contactos**: un LID se traduce a nombre humano ("Guarda (prueba)").
- Fallo de entrega **nunca silencioso**: el dueño se entera.

### Capa 1 (filtro) — mejoras de esta sesión
- **Criterio extraído a `criterio.py`** (doctrina de negocio, testeable) + `probar_criterio.py` (regresión 8/8).
- **Reglas nuevas del Monarca:** hurtos/faltantes → **mínimo naranja (se investigan)**; quejas → **nunca verde**;
  objetos en riesgo (maceta/matera) → **mínimo naranja**; persona merodeando → **rojo**.
- **ANÁLISIS DE VIDEO** (`medios.py`): dos canales — **audio** (whisper) + **3 fotogramas** (visión). Antes caía en "[video adjunto]".
- **Determinismo (memoria de veredictos):** huella sha256 del contenido → **mismo contenido, mismo veredicto**
  (y sin re-pagar el análisis). Medido: `cache: miss` → `cache: hit`, 1 entrada.
- **Razonamiento DESACTIVADO** en el clasificador: **13.7 s → 1.8 s** por mensaje y **11× más barato**.
- **Directorio de emergencia** (123/119/125 Colombia) + **regla anti-invención de números**.

---

## 2. PRUEBAS REALES (con un tercero: una amiga del Monarca, "Guarda (prueba)")

| Prueba | Resultado |
|---|---|
| Mensaje informativo (queja de paquete) | clasificado; **no interrumpió** al dueño (disciplina) |
| **Intento de robo** | 🔥 ROJO → aviso → el Monarca aprobó → **ella recibió la respuesta** ("Llama al 123, no confrontes, cierra el portón") |
| Reemplazo por texto libre | *"Mañana se acerca el todero…"* → enviado a ella |
| **Video (19 s)** | analizado: audio *"puede accidentarse cualquier persona"* + fotogramas → NARANJA |
| **Decisión por VOZ** | transcripción **perfecta**: *"El todero será enviado mañana a primera hora para retirar la matera."* → enviada a ella |
| Ciclo completo | **34 s de punta a punta** (incluida la aprobación humana) |

**Auditoría:** cada acción queda en el bus con `approved_by: Key`.

---

## 3. BUGS ENCONTRADOS Y MUERTOS (por orden de aparición)

1. **Borrador vacío** (`finish_reason=length`): el modelo gastaba todo en tokens de razonamiento → `reasoning:{enabled:false}`.
2. **Bucle infinito**: el motor emitía al bus el mismo tipo de evento (`order`) que leía → se reprocesaba solo
   (**74 eventos basura**, riesgo de doble envío) → ahora emite `order_processed`.
3. **Doble aviso** al dueño (alerta + propuesta) → **aviso unificado** con latido y degradación.
4. **Nota de voz del dueño tragada en silencio** (cuerpo vacío) → transcripción + eco de confirmación.
5. **No-determinismo del clasificador:** el **mismo video** dio NARANJA y luego VERDE (el segundo, incorrecto:
   ella habría quedado sin respuesta) → memoria de veredictos por huella + reglas explícitas.
6. **Número inventado** ("Policía 112" en Colombia) → directorio de emergencia + regla anti-invención.
7. Falso positivo de `pgrep` (se contaba a sí mismo) y log duplicado (stdout al mismo archivo) — corregidos.

---

## 4. PENDIENTES

1. **C3 — reglas preaprobadas** ("quejas de mantenimiento → avisar a Don Carlos" sin consultar cada vez).
2. **C4 — onboarding**: directorio de emergencia real del cliente, tono, horas de silencio, formato.
3. **Refinamiento**: descartar transcripciones de video **sin habla** (Whisper alucina con tonos: convirtió un tono puro en *"Gracias por ver el video"*).
4. **Envío de adjuntos por el agente** (reenviar una foto/video al tercero) — hoy solo texto.
5. **Seguridad**: montar solo el bus en el sandbox (no todo `/opt/waha`, que incluye `filtro.env`).
6. **Cuarto de guerra** en Telegram (desde cero, con calma) — las sombras están sueltas de Telegram por orden del Monarca.
7. **Ejército de Sombras**: OPERATIVO (10/10, auditado por Beru) — pendiente el primer "convoca a las sombras".

---

## 5. ESTADO TÉCNICO

- **Servicios VPS:** `seawolf-filtro` (3011), `seawolf-responder` (nuevo), `waha-sink`, `seawolf-webui`, contenedor `waha` (WORKING).
- **Modelo:** `qwen/qwen3.7-flash` (filtro, agente y redacción) con respaldos en el agente; `gemini-2.5-flash` para visión.
- **Bus:** `/opt/waha/bus.db` — eventos de texto, voz, imagen, video, órdenes, aprobaciones y acciones.

> *"El agente piensa callado; cuando ya tiene la respuesta, se comporta como persona — y nunca actúa sin su voz."* 🐺
