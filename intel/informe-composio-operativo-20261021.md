# INFORME — COMPOSIO OPERATIVO (SDK, no MCP)
**Fecha:** 2026-10-21 · Uso Interno — Seawolf Studio · Bellion para el Monarca (Key)

---

## 1. EL MISTERIO DEL 401 — RESUELTO

**Hay DOS tipos de clave y NO son intercambiables** (ya lo teníamos documentado, y se confirmó en vivo):

| Prefijo | Tipo | Header correcto | Para qué sirve |
|---|---|---|---|
| **`ak_`** | **Project API Key** | **`x-api-key`** | **SDK de backend** (`composio` Python) — ejecutar herramientas |
| **`ck_`** | **Consumer API Key** | `x-consumer-api-key` | Solo el **MCP** de `connect.composio.dev/mcp` |

**El Monarca entregó una `ak_`** → al montarla en el MCP (que espera `x-consumer-api-key`) dio **401**.
El error exacto (*"not a valid AuthKit JWT"*) es un caso conocido y reportado por otros usuarios.

**Solución aplicada:** usar la **vía del SDK**, que es la que nuestra doctrina ya tenía verificada.

---

## 2. ESTADO: ✅ OPERATIVO Y PROBADO

| Prueba | Resultado |
|---|---|
| SDK `composio` 0.21.1 instalado | ✅ |
| `Composio(api_key=ak_…)` | ✅ inicializa |
| `sessions.create(user_id="monarca_seawolf")` | ✅ |
| `COMPOSIO_SEARCH_TOOLS` | ✅ ejecuta |
| **`GMAIL_FETCH_EMAILS` (en vivo)** | ✅ **leyó 3 correos reales** |

### Conexiones que YA estaban activas (de una sesión anterior)
- **GMAIL** → `seawolfk.studio@gmail.com` (activa)
- **GOOGLESHEETS** (activa)
- **GOOGLECALENDAR** (activa)

---

## 3. ENTREGABLES
- **`intel/composio.py`** — helper del ejército: `status` · `connections` · `gmail` · `run` · `search`.
- **`COMPOSIO_API_KEY`** guardada en los **11 `.env`** (default + 10 sombras).
- Config: `mcp_servers.composio` **desactivado** (era la vía equivocada con `ak_`).

---

## 4. QUÉ FALTA PARA EXPLOTARLO
1. **Conectar más toolkits** (Gmail/Sheets/Calendar ya están): **NOTION · HUBSPOT · SLACK · DRIVE · LINKEDIN · GOOGLEADS**…
   Se hace con `python composio.py connections NOTION,HUBSPOT` → devuelve enlaces OAuth (**expiran en 10 min**).
2. **Si se quiere el MCP** (en vez del SDK): pedir la **clave `ck_`** en el dashboard → sección **Install** (antes "For You"/"AI Clients") → "Your API Key".
3. **Límite**: plan **Free = 100.000 toolcalls/mes** ($0). No subir a Pro hasta llegar al techo.

---

## 5. FUENTES
- `references/composio-integration.md` (doctrina propia, verificada) · docs.composio.dev · issue ComposioHQ#3485 · prueba en vivo.

**Fin del informe.**
