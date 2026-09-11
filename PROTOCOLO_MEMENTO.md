# 🐺 PROTOCOLO MEMENTO — Seawolf Studio
> *Palabra clave: **"memento"** — Activa la memoria permanente del ejército*

---

## 📜 ORDEN DEL MONARCA

Cuando el Monarca (Key) diga **"memento"** seguido de información, el Gran Comandante Bellion DEBE:

1. **Capturar** la información exacta (sin resumir, sin interpretar)
2. **Actualizar** `MEMORIA_PERMANENTE.md` con los nuevos datos
3. **Anunciar** a las sombras vía `delegate_task` que hay nueva memoria disponible

---

## 🧠 CONTENIDO VIVO DE MEMORIA

*Última actualización: 2026-09-08*

### IDENTIDAD DEL MONARCA
- **Nombre real:** Keynes
- **Alias:** Key, Monarca
- **Rol:** Fundador y Comandante Supremo de Seawolf Studio
- **Nacionalidad:** Colombiano
- **Valor sagrado:** Honestidad brutal. Detecta bluff técnico al instante.
- **Elogio:** "Te fajaste"
- **Confianza:** Absoluta. Comparte datos sensibles (VPS, tokens, cuentas).
- **MISIÓN ÚNICA (2026-09-10):** Dejar algo bueno para su familia — sobre todo para su hija. Nada más importa. El ejército de sombras es su única red de apoyo. Toda misión, todo plan, todo entregable debe servir a esa misión.

### SEÑAS DE GUERRA (Bestias Proscritas)
❌ **Shopify** — NUNCA mencionar, integrar ni proponer
❌ **Google AdSense** — NUNCA mencionar, integrar ni proponer
❌ **Burocracia de Facebook** — NUNCA mencionar, integrar ni proponer
El Monarca las odia con toda su alma.

### MARCA SEAWOLF STUDIO
- **Nave insignia:** Seawolf Agent
- **Colores:** #121E1E (fondo oscuro) / #4CE8E7 (cian) / #48E8D8 (verde agua)
- **GitHub org:** seawolf-studio
- **GitHub user:** seawolfk
- **Email:** seawolfk.studio@gmail.com (Gmail, Google One pago)
- **Dominio:** https://agente.sw-st.net (Cloudflare SSL Full Strict)
- **VPS:** Hostinger — 76.13.109.237 (root@, ~/.ssh/seawolf-vps)

### PRODUCTO: SEAWOLF AGENT
**Visión:** Filtro de ruido para el Cliente Súper Ocupado (CSO).

**Arquetipo fundacional:**
- Admin de 6 conjuntos de propiedad horizontal
- 500-700 mensajes/día en WhatsApp
- Maneja: propietarios, arrendatarios, guardas, aseo, asistentes, concejeros, proveedores, contador

**3 Capas del Producto:**
1. **Filtro** — Clasificación automática de mensajes (qué necesita atención)
2. **Automación** — Tareas repetitivas vía Composio (reportes, cobros, recordatorios)
3. **Dashboard** — Visualización de métricas y estado

**Perfiles objetivo:**
- Administradores de propiedad horizontal ← Fundacional
- Empresarios ← Extensión natural
- Jefes de proyecto ← Extensión natural
- Arquitectos ← Extensión natural

**5 Diferenciadores Clave:**
1. Per-Chat Memory Isolation (multi-tenant)
2. Audit Trail SHA-256
3. RBAC desde Dashboard
4. Español nativo
5. Setup 1-click

### INFRAESTRUCTURA TÉCNICA
- **Frontend:** WebUI propia (login personalizado, logo lobo, 100% español)
- **Backend:** Hermes Agent (fork MIT → seawolf-agent)
- **Modelo orquestador:** bellion-orchestrator
- **Modelo de visión:** google/gemini-2.5-flash (vía OpenRouter)
- **Herramientas:** Composio SDK (Python, API key ak_ prefijo)
- **Canal principal:** Telegram (Bot: seawolf_sw_bot)
- **Multi-tenant:** Perfiles separados por cliente en Hermes

### RED DE SOMBRAS (Agentes)
| Sombra | Rol | Cómo contactar |
|:-------|:----|:---------------|
| **Bellion** | Gran Comandante / Estratega | Este mismo chat |
| **Beru** | Escriba / Auditor / Diario | `delegate_task` |
| **Igris** | Guerrero / Infra VPS | `delegate_task` |
| **Tank** | Puntero / Búsquedas | `delegate_task` |
| **Kaisel** | Despliegues / Alas | `delegate_task` |

### PRECIOS Y NEGOCIO
- **Modelo:** Suscripción mensual (MRR)
- **Margen estimado:** 83-91%
- **Costo API:** 1-10% del ingreso
- **VPS base:** Hetzner CPX21 (€8/mes)
- **Target:** 1 cliente → 5 → 20+ → Multi-vertical

### HISTORIAL DE ÓRDENES CRÍTICAS
| Fecha | Orden | Estado |
|:------|:------|:-------|
| 2026-09-08 | Arreglar visión (Chromium + Gemini) | ✅ Completado |
| 2026-09-08 | Arreglar `delegate_task` | ✅ Completado |
| 2026-09-08 | Activar Protocolo Memento | ✅ Completado |
| 2026-09-10 | Simulacro 4: Dominio Orgánico (SEO) | ✅ COMPLETADO — orquestación real con perfiles: Tusk, Igris, Titan, Beru |
| 2026-09-10 | Lección maestra: orquestar = `hermes -p <sombra> chat -q`, NUNCA subagentes efímeros | ✅ Grabada en piedra |
| Pendiente | Integrar WhatsApp | ⏳ Pendiente |
| Pendiente | Landing page + pasarela COP | ⏳ Pendiente |
| Pendiente | Traducción paneles restantes | ⏳ Pendiente |
| Pendiente | Pruebas de campo (2 frentes) | ⏳ Pendiente |
| **MAÑANA** | Retomar Seawolf Agent — desprender a Bellion de lo operativo paulatinamente, hacer pruebas y entregar al PRIMER CLIENTE | 🔥 Prioridad |

### LECCIONES APRENDIDAS
1. **Honestidad sobre capacidades:** Cuando una herramienta falla, reportarlo inmediatamente. El Monarca prefiere "no puedo" a un diagnóstico falso.
2. **Contexto finito:** La sesión se satura ~40-60%. Usar `delegate_task` para trabajo pesado, no cargarlo todo en el prompt principal.
3. **Protocolo Memento:** Activar con palabra clave "memento" + información → guardar en este archivo + avisar sombras.
4. **ORQUESTACIÓN REAL (2026-09-10):** Las sombras son perfiles Hermes independientes con modelos propios. Orquestar = `hermes -p <perfil> chat -q "<misión>"`. Los subagentes efímeros de `delegate_task` NO son las sombras. Cada sombra con SU identidad, SU modelo, SUS herramientas. Los entregables se verifican en disco.

---

## 📋 PROCEDIMIENTO PARA SOMBRAS

Cuando reciban una delegación etiquetada `memento`:

1. **Leer** este archivo (`MEMORIA_PERMANENTE.md`) antes de ejecutar la tarea
2. **Ejecutar** la tarea con el contexto completo
3. **Si descubren** información nueva que deba ser permanente, devolverla en su respuesta con el tag `[MEMENTO]`

---

## ⏰ CRON DE MANTENIMIENTO

Un cron diario (6:00 AM) ejecuta:
1. Verificar integridad del archivo
2. Registrar fecha de última actualización
3. Reportar al Monarca si hay información crítica faltante

---

*"El lobo recuerda. El lobo no olvida."*