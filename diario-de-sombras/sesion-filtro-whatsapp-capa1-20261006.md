# DIARIO DE SESIÓN — SEAWOLF AGENT: FILTRO WHATSAPP (CAPA 1) + DISEÑO CAPA 2
## Handoff para retomar (protocolo de compactación Seawolf)

**Fecha:** 2026-10-06 · **Elaborado por:** Bellion, Gran Comandante
**Encargado por:** el Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Estado al cierre:** pausa nocturna; el Monarca verá los informes y al volver retomamos la **Capa 2**.

---

## 0. CÓMO RETOMAR
1. Abrir sesión nueva y ordenar: **"lee el diario de la última sesión"**.
2. **Primer pendiente:** el Monarca querrá empezar la **Capa 2** del agente (automatización/delegación).
   El diseño ya está en `intel/capa2-system-prompt-draft-20261006.md`.
3. **Chequear que el cron de repos terminó** (ver §6) — debía enviar 100 repos hasta la mañana.

---

## 1. LO HECHO HOY (arco)
1. **Cierre de Telegram** y del puerto fantasma **8642**.
2. **Rebranding** del Seawolf Agent (logos + titlebar + i18n) y deploy.
3. **Tubo de WhatsApp** con **WAHA** (motor GOWS) — vinculación exitosa.
4. **Filtro (Capa 1)**: clasificación con criterio de negocio + **voz e imagen**.
5. **Modelo de 2 líneas** confirmado y probado (entrega con notificación).
6. **Canal directo** Bellion→WhatsApp del Monarca.
7. **Pipeline de 100 repos** de contenido con IA, enviados cada 30 min.
8. **Diseño de la Capa 2** (system prompt + onboarding + reglas de humanidad).

---

## 2. WHATSAPP — WAHA (el corazón del producto)
- **Contenedor `waha`**: `devlikeapro/waha:latest`, motor **GOWS** (obligatorio por el **passkey**), `127.0.0.1:3000`,
  API key en `/root/.waha.env`.
- **Sesión `seawolf`**: número **+57 300 206 7487** vinculado (`WORKING`), perfil **"Seawolf Agent"**.
- **Passkey**: WhatsApp exige passkey al vincular; WEBJS/NOWEB NO pueden (log `Cmd.refreshQR is not a function`);
  **GOWS sí** (gratis desde WAHA 2026.6.1). Detalle en la skill `seawolf-whatsapp-waha`.
- **Filtro**: `/opt/waha/filtro.py` (unit `seawolf-filtro.service`, puerto 3011).
  - **Criterio (del Monarca):** 🔥 rojo = perturba la seguridad o exige atención inmediata; 🟠 naranja = **mitigable ahora, arreglo después** (la acción empieza por la mitigación); 🟡 consulta; 🟢 informativo.
  - **Voz** → transcribe con **Groq `whisper-large-v3-turbo`**.
  - **Imagen** → describe con **`google/gemini-2.5-flash`** (OpenRouter).
  - **Clasifica** con `google/gemini-2.5-flash` (JSON).
  - **Entrega** 🟠🔥 a la **Línea 1** del cliente vía WAHA `sendText`. Log en `/opt/waha/filtro.log`.

---

## 3. MODELO DE NEGOCIO (2 líneas — CONFIRMADO)
- **Línea 1** = número **personal** del cliente (ya existe). Recibe SOLO lo filtrado. **Intocable.**
- **Línea 2** = línea **dedicada** donde VIVE el agente (eSIM/SIM aparte). El cliente migra ahí a sus contactos de trabajo; el agente observa/clasifica/filtra.
- El aviso va **L2 (bot) → L1 (personal, otro número)** ⇒ **notificación natural**. No hace falta 3ª línea.
- **Privacidad (arma de venta):** el agente solo lee L2; la L1 personal nunca se toca.
- **eSIM:** funciona igual (WAHA solo necesita el número con cuenta de WhatsApp). Preferir línea estable (no prepago que se recicle).
- **Riesgo Meta (opinión del Monarca + Bellion):** bajo perfil por diseño — nunca masivo, nunca robótico, un solo destinatario ⇒ poco sospechoso. Ojo: sigue siendo cliente no oficial (ToS); mantener disciplina (poco volumen, variado, sin difusión).

---

## 4. CANAL BELLION → MONARCA
- Helper **`/opt/waha/avisar.sh "mensaje"`** (L2 → +57 312 533 0127).
- Probado: el Monarca recibe notificación desde "Seawolf Agent".

---

## 5. DISEÑO CAPA 2 (sin construir)
Documento: `intel/capa2-system-prompt-draft-20261006.md`.
- **System prompt**: humano competente y discreto, **no hablador**, claro/conciso/concreto, sin relleno, frases variadas.
- **Humanidad (mecánica)**: no responder al instante (2–5 s), pausas entre mensajes (2–6 s), "escribiendo…", marcar leído, volumen bajo.
- **Onboarding (§4)**: el agente acuerda identidad y comportamiento con el cliente en las primeras interacciones (nombre, tono, vocabulario, criterio de urgencia, contactos, horario, silencio, formato).
- **Reglas útiles (§5)**: horas de silencio, contactos prioritarios, aprender por corrección, no repetir, consolidar, nunca prometer, registro (Audit Trail).
- **Pendiente**: motor de respuestas con cola/pausas/presencia, compuerta de aprobación, reglas preaprobadas, onboarding configurable, límites + auditoría.

---

## 6. PIPELINE DE 100 REPOS (corriendo)
- **Metodología**: GitHub Search API (40 consultas `license:mit stars:>1000`) → 405 candidatos → curación con IA → **100 finales** (creación de contenido con IA).
- **Archivos VPS**: `repos100_final.json`, `generar.py` (descripciones largas con gemini), `enviar_repos.py`, `cron_repos.sh`.
- **Cron**: `*/30 * * * *` → envía **5 repos por mensaje** al WhatsApp del Monarca (≈20 mensajes hasta la mañana). Índice en `/opt/waha/repos_idx`.
- **Informe**: `intel/creacion-contenido-ia-100repos-20261006.md`.
- **Verificar al volver**: que `wc -l /opt/waha/repos_desc.jsonl` = 100 y que el índice llegó a 100 (aviso de cierre enviado).

---

## 7. INVENTARIO TÉCNICO
- **Servicios nuevos (VPS)**: contenedor `waha`, `waha-sink.service`, `seawolf-filtro.service`, cron `cron_repos.sh`.
- **Helper**: `/opt/waha/avisar.sh`.
- **Skills**: `seawolf-whatsapp-waha` (creada/actualizada con GOWS, 2 líneas, filtro, avisar.sh).
- **Commits (repo seawolf-agent)**: ver git log.
- **Cambios previos de la sesión (2026-10-04)**: Telegram off, 8642, rebranding (commit ya empujado).

---

## 8. DECISIONES VIGENTES
1. **Capa 1 primero, luego Capa 2** (el Monarca: A es la puerta de entrada y de mayor adopción).
2. **Modelo de 2 líneas** (L1 personal del cliente; L2 dedicada con el agente).
3. Criterio de filtro con **lógica de negocio** (mitigable → naranja; seguridad/inmediato → rojo).
4. Capa 2: **no hablador, humano, con aprobación** para acciones a terceros.

> *"Seawolf Agent: observa mucho, habla poco, y solo a quien debe."* 🐺
