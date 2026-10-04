# DIARIO DE SESIÓN — SANEAMIENTO DEL VPS, REBRANDING Y TUBO DE WHATSAPP
## Handoff para retomar (protocolo de compactación Seawolf)

**Fecha:** 2026-10-04 · **Elaborado por:** Bellion, Gran Comandante
**Encargado por:** el Monarca (Key) · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Estado al cierre:** pausa a petición del Monarca (monta WhatsApp en el número prepago).

---

## 0. CÓMO RETOMAR
1. Abrir sesión nueva y ordenar: **"lee el diario de la última sesión"**.
2. **Primer pendiente operativo:** el Monarca debe escanear el **QR de WAHA** con el número prepago
   (ya tendrá WhatsApp instalado). Generar QR fresco con `/opt/waha/qr.sh` en el VPS y entregarlo.
3. Luego: probar captura real de un mensaje, y arrancar el **Filtro** (corazón del producto).

---

## 1. ÓRDENES DEL DÍA (arco)
1. Reconocer el VPS (puertos): lo que sirve se queda; lo muerto se cierra.
2. Revisar código del agente + repasar el rebranding (conflicto de logos Seawolf vs Hermes).
3. Confirmar el campo completo → arreglos y mejoras.
4. Cerrar **Telegram** del todo (no se usaba; se hará una "sala de guerra" con cada sombra aparte).
5. Cerrar el **8642**.
6. Avanzar el **plato fuerte: WhatsApp**.

---

## 2. RECONOCIMIENTO DEL VPS (puertos)
| Puerto | Proceso | Veredicto |
|:---:|---|---|
| 22 / 80 / 443 / 53 | ssh / nginx / dns | SE QUEDAN |
| **8787** | `seawolf-webui/server.py` = **Seawolf Agent (WebUI)** | SE QUEDA |
| **8085→9119** | docker `hermes-agent-core` = **Ejército de Sombras (12 gateways s6)** | SE QUEDA — ⚠️ **expuesto en 0.0.0.0** |
| 9119 | hermes gateway (host) | activo |
| 8000 / 9443 | docker `portainer` | SE QUEDA — ⚠️ **expuesto al público** |
| 20241 / tailscale 100.114.5.98 | cloudflared / tailnet | SE QUEDAN |
| 5433, 8788, 8081, 8799, 8432, 8888, 7474, 7687, 8100 | LOBO (NEREUS) | SE QUEDAN (localhost) |
| **8642** | **nada escuchaba** — declarado en `config.yaml`/`DEPLOY.md` pero inexistente | **CERRADO** |

Nota: **8642 es el puerto canónico del gateway del agente Hermes en el ecosistema WebUI**, pero en este
VPS nunca corría. Se limpió de la documentación y del config.

---

## 3. TELEGRAM — APAGADO TOTAL
**Causa del bucle:** el token vivía en **2 configs** del contenedor y todos los gateways lo cargaban:
- `/opt/data/config.yaml` → `gateway.platforms.telegram` (token + `enabled: true`)
- `/opt/data/profiles/bellion/config.yaml` → su propio token

**Fix aplicado:** `enabled: false` + **token neutralizado** en ambos. Respaldos: `config.yaml.bak.20261004_170609`.
Reinicio de `hermes-agent-core` y de `hermes-gateway.service` (user scope, root: `XDG_RUNTIME_DIR=/run/user/0 systemctl --user ...`).
**Evidencia:** `docker logs` → **0 "already in use"**; **"No messaging platforms enabled"**. Ejército intacto (18 procesos, 12 gateways).
> Regla: `enabled: false` solo NO bastaba; hubo que quitar el token. Y hay configs **por sombra** en `/opt/data/profiles/*/config.yaml`.

---

## 4. 8642 — CERRADO
- `config.yaml` del repo reescrito (sin el gateway fantasma; describe el sistema real: WebUI 8787, agente Hermes, OpenRouter).
- `DEPLOY.md` corregido (8642→8787, dominio `agente.sw-st.net`, ruta `/opt/seawolf-webui`).

---

## 5. REBRANDING (logos + titlebar + i18n) — DESPLEGADO
**Conflicto confirmado con evidencia visual:**
- `favicon.svg` = lobo Seawolf ✅, pero `favicon.ico` / `favicon-32/192/512.png` / `apple-touch-icon.png` = **caduceo de Hermes** ❌
- `index.html` titlebar: logo = **caduceo de Hermes** y título = **"Hermes"** ❌

**Fix:**
- Regenerados TODOS los favicons desde el SVG del lobo (Chrome headless 1024 → PIL 512/192/180/32 + `.ico`).
- Titlebar: logo → lobo; título → **"Seawolf Agent"**.
- **571 cadenas** i18n "Hermes" → "Seawolf" (protegiendo comandos reales `hermes`, rutas `~/.hermes`, claves internas). `node --check` OK.
- **Repos:** `seawolf-agent-webui` commit `48d0d161` (push OK). **VPS:** `git pull` + reinicio `seawolf-webui.service`; HEAD = `48d0d161`; favicons md5 nuevos en producción.
- **Sitio en vivo:** `https://agente.sw-st.net` → 200, título "Seawolf Agent".

---

## 6. WHATSAPP — TUBO MONTADO Y PROBADO (plato fuerte)
**Ruta (decisión vigente): no oficial — Baileys → WAHA Core → WAHA Plus.** (El Monarca rechaza la burocracia de Meta.)
**Riesgo honesto:** viola ToS de WhatsApp → baneo. Mitigación: número dedicado, calentamiento, límites.

**Montado en el VPS:**
| Pieza | Detalle |
|---|---|
| Contenedor `waha` | `devlikeapro/waha:latest` (WEBJS, CORE), `127.0.0.1:3000`, API key en `/root/.waha.env` (600) |
| Sesión | `seawolf`, estado `SCAN_QR_CODE` |
| QR | `GET /api/seawolf/auth/qr?format=image` · helper `/opt/waha/qr.sh` |
| Receptor | `/opt/waha/sink.py` (systemd `waha-sink.service`), log `/opt/waha/messages.log` |
| Webhook | `http://172.16.0.1:3010/webhook` (gateway Docker) — **probado: captura `session.status`** ✅ |

**Trampas cazadas (documentadas en skill `seawolf-whatsapp-waha`):**
1. Un contenedor NO alcanza `127.0.0.1` del host → el sink va al **gateway Docker** (`172.16.0.1:3010`), privado.
2. El backlog de webhooks fallidos sigue reintentando → mirar la **URL dentro** del error, no solo el conteo.
3. `PUT /api/sessions/<name>` **reinicia la sesión** (nuevo QR).

**Falta:** que el Monarca escanee el QR con el prepago → probar captura real → construir el **Filtro**.

---

## 7. PENDIENTES (anotados)
- **Portainer seguro:** recomendar **Tailscale** (`https://100.114.5.98:9443`), cero puertos públicos. Hacerlo con el Monarca presente.
- **`hermes-agent-core` expuesto en `0.0.0.0:8085`** → llevar al tailnet.
- **Jellyfin + 5 TB Google Drive** (rclone mount + Jellyfin Docker, direct-play; solo 54 GB de disco libres).
- **Filtro WhatsApp-first** (clasificador 🟢🟡🟠🔥) → Automatización (Composio) → Dashboard → RBAC + Audit.

---

## 8. DECISIONES VIGENTES
1. Dos productos separados: **Seawolf Agent (insignia)** · **LOBO (personal)**.
2. Telegram: **apagado**; se rehará como "sala de guerra" con cada sombra aparte.
3. WhatsApp: ruta **no oficial** (WAHA/Baileys), número dedicado a futuro.
4. Modelo de Bellion: `deepseek-v4.1-flash` (no degradar).
5. No tocar el núcleo de Hermes (extender: plugin/MCP/skill/config/skin).

---

## 9. INVENTARIO
- **Commits:** `seawolf-agent-webui` → `48d0d161`; `seawolf-agent` → `b02ce6b` (8642 + Memento rev 04-oct).
- **Servicios nuevos:** contenedor `waha`, `waha-sink.service`.
- **Skill nueva:** `seawolf-whatsapp-waha`.

> *"El caño de WhatsApp está listo y probado; solo falta el número."* 🐺
