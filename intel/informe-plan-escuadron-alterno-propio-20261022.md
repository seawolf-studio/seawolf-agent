# 🐺 PLAN — ESCUADRÓN ALTERNO PROPIO (100% nuestro)
**Arquitecto:** Bellion (Gran Comandante) · **Para:** Monarca · **Fecha:** 2026-10-22
**Condición:** construido **solo sobre lo que ya es nuestro** — sin CopilotKit Intelligence, sin licencias de terceros, sin alquilar el cerebro.

---

## 0. HALLAZGO QUE CAMBIA TODO (verificado hoy, en vivo)

**Hermes YA trae el motor del escuadrón.** No hay que instalar nada nuevo:

> **`hermes kanban`** — *"**Durable SQLite-backed task board shared across Hermes profiles.** Tasks are claimed atomically, can depend on other tasks, and are executed by a named profile in an isolated workspace."*

**Verificado en la máquina del Monarca:**
- Tablero `default` existe y responde ✅
- **Las 10 sombras ya están registradas como ejecutoras** (`on disk: yes`):
  `beru · greed · igris · iron · jima · kaisel · kamish · tank · titan · tusk`
- `kanban create` acepta **exactamente** lo que necesitamos:
  `--assignee` (la sombra) · `--model` + `--provider` (**por tarea**) · `--parent` (dependencias) ·
  `--workspace scratch | worktree | dir:<path>` (**workspace aislado**) · `--skill` (tools forzadas) ·
  `--goal` (bucle hasta cumplir) · `--triage` · `--priority` · `--completion-contract`
- Y trae el resto del ciclo: `dispatch` · **`daemon`** (despachador siempre encendido) · `swarm` (paralelo) ·
  **`request-review`** (compuerta humana) · `notify-subscribe` (avisos) · `attach` (entregables) ·
  `decompose` (partir un objetivo) · `log`/`runs` (auditoría) · `heartbeat` (vivo/no vivo).

**Traducción:** lo que OpenDots/OpenBot alquilan como *"Intelligence"* (hilos durables, memoria, despacho,
compuerta de aprobación, auditoría) **nosotros ya lo tenemos en el motor de Hermes.**

---

## 1. ARQUITECTURA — 8 capas, TODAS nuestras

```
                     MONARCA (Key)
                          │  orden / aprobación (WhatsApp)
                          ▼
   ┌──────────────────────────────────────────────────────┐
   │ 1. CEREBRO — BELLION (orquestador)                   │
   │    recibe → descompone (kanban decompose) → asigna   │
   └───────────────────────────┬──────────────────────────┘
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ 2. MOTOR — HERMES KANBAN (SQLite durable) + daemon   │
   │    reclama atómico · depende · aísla · reintenta     │
   └───────────────────────────┬──────────────────────────┘
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ 3. EJECUTORES — las 10 SOMBRAS (perfiles reales)     │
   └───┬───────────┬───────────┬───────────┬──────────────┘
       ▼           ▼           ▼           ▼
   ┌────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
   │4.MODELO│ │5.MANOS  │ │6.MEMORIA│ │7.GATE    │
   │FreeLLM │ │Composio │ │mem0 +   │ │request-  │
   │API +   │ │+ MCP por│ │Graphiti │ │review +  │
   │OpenRou.│ │sombra   │ │+ Neo4j  │ │WAHA      │
   └────────┘ └─────────┘ └─────────┘ └──────────┘
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ 8. COMPUTADOR POR SOMBRA (patrón OpenBot) + AUDITORÍA │
   └──────────────────────────────────────────────────────┘
```

---

## 2. EL ORGANIGRAMA (roster real, ya forjado)

| Sombra | Rol | Le toca en el escuadrón |
|---|---|---|
| **IGRIS** | Copywriting / Persuasión | Textos, copys, guiones |
| **TANK** | Ventas / Cierre / WhatsApp | Conversación comercial, cierre |
| **GREED** | Ads / Tráfico pagado / CPA | Campañas (sin bestias proscritas) |
| **IRON** | Email marketing / Secuencias | Funnels email-first (**frente frío B2B**) |
| **TUSK** | SEO / Tráfico orgánico | Keywords, contenido orgánico |
| **KAMISH** | Redes sociales / Distribución | Publicación y difusión |
| **KAISEL** | Web dev / WordPress / Dark theme | Webs, tienda, despliegues |
| **TITAN** | UX/UI / Wireframes / Dark theme | Interfaces, diseño |
| **JIMA** | Automatización / n8n / APIs / Webhooks | Cablear todo, integraciones |
| **BERU** | Auditor / Supervisión / Reportes | **Audita** (nadie audita su propio trabajo) |

---

## 3. PLAN DE IMPLEMENTACIÓN (numerado, por fases)

### FASE 0 — Preparación (sin riesgo, 15 min)
1. **Salud de la casa:** correr `hermes update` (hay un aviso pendiente de actualización de fuentes).
2. **Crear el tablero del escuadrón:** `hermes kanban boards` → board **`escuadron`** (separado del `default`).
3. **Confirmar ejecutores:** `hermes kanban assignees` (ya verificado ✅).
4. **Conectar FreeLLMAPI:** guardar la clave con `seawolf-secret.sh` (**sin imprimirla**) y hacer **una llamada de prueba real** al endpoint (no dar por bueno que "debería funcionar").

### FASE 1 — Encender el motor (30 min)
5. **Definir el flujo del tablero:** `triage → todo → ready → running → review → done` (+`blocked`).
6. **Avisos al Monarca:** `hermes kanban notify-subscribe` apuntando al **WhatsApp del Monarca** vía WAHA → recibirá el aviso cuando algo pida su palabra.
7. **Compuerta de aprobación:** dejar `request-review` como **único** camino para cerrar algo sensible (nada se da por bueno sin pasar por ahí).
8. **Encender el despachador:** `hermes kanban daemon` como **servicio persistente** (systemd/`persist_on_release`) — a partir de aquí el escuadrón vive aunque cerremos la sesión.

### FASE 2 — Cablear las capas que ya existen (1 h)
9. **Memoria:** apuntar las sombras a **mem0 (8888) + Graphiti (8100) + Neo4j (7474/7687)** — *verificados vivos en el VPS*. Cada sombra con su memoria.
10. **Manos por sombra:** allowlist de **Composio** (Gmail/Sheets/Calendar ✅) y **MCP** — cada sombra con **solo** las herramientas de su rol (Tank no necesita Gmail; Iron sí).
11. **Modelo por tarea:** regla de dos capas —
    - **FreeLLMAPI** para trabajo de fondo y mecánico (barridos, catálogos, resúmenes).
    - **OpenRouter** para lo crítico de producción.
    - Se aplica **por tarea** con `--model` / `--provider` (ya soportado).
    - Bellion mantiene su modelo fijado por el Monarca (**no se degrada**).

### FASE 3 — El computador por sombra (patrón OpenBot, hecho por nosotros) (2-3 h)
12. **Workspace aislado por tarea:** `--workspace dir:<ruta>` → cada misión corre en su propia carpeta, sin pisar a las demás.
13. **Sandbox por sombra:** una carpeta + **navegador con perfil propio** + límites de escritura, para que una sombra no pueda tocar lo que no le toca.
14. **Registro por acción:** cada tarea guarda **quién hizo qué, con qué modelo, en qué carpeta y con qué resultado** (`kanban log` / `runs`).

### FASE 4 — La cara (2-3 h)
15. **Panel del escuadrón** en el Centro de Mando: qué sombra está corriendo, qué entregó, qué está bloqueado, qué espera aprobación.
16. **Aprobación desde el teléfono:** la tarjeta de `request-review` viaja por **WhatsApp** — el Monarca aprueba/rechaza sin abrir el PC.

### FASE 5 — Prueba de fuego (la que decide)
17. **Una misión real de punta a punta** — propongo **la tienda de zapatillas** (ya tiene insumo: 734 fotos, catálogo a 40%) o **el Círculo Publicitario**.
    Flujo a probar: Bellion descompone → asigna a 3-4 sombras en paralelo → Jima cablea → **Beru audita** → `request-review` → aviso al WhatsApp → aprobación del Monarca.
18. **Medir y ajustar:** tokens gastados, tareas completadas, atascos, y **documentarlo** en la línea de montaje.

---

## 4. CÓMO CUMPLE NUESTRAS CONDICIONES

| Condición del Monarca | Cómo se cumple |
|---|---|
| **Código propio** | El motor es Hermes (nuestro). No se instala CopilotKit ni nada licenciado. |
| **Cero dependencia del "cerebro" ajeno** | La orquestación es el Kanban local (SQLite nuestro). |
| **Cero copyleft en producción** | No entra AGPL al producto. |
| **Costo controlado** | FreeLLMAPI para el fondo; OpenRouter solo donde importa. Modelo por tarea. |
| **Modo oscuro por defecto + marca** | Aplica al panel del escuadrón (`#121E1E / #4CE8E7 / #48E8D8`). |
| **Nada nace suelto** | Cada pieza se registra en la línea de montaje y el Centro de Mando. |
| **Privacidad** | Memoria y datos en **nuestro** VPS, no en una nube de terceros. |
| **Evidencia o no existe** | Cada entrega queda con archivo + auditoría de Beru + `log`/`runs`. |

---

## 5. RIESGOS Y TRAMPAS (anticipados)

1. **El `daemon` es un proceso vivo:** si no se ancla bien (systemd / `persist_on_release`), el escuadrón se apaga al cerrar la sesión. Hay que montarlo persistente y **verificarlo** con una tarea que corra sin nadie mirando.
2. **Sombras en paralelo:** el pitfall ya conocido — **una por proceso en background**, nunca en bucle desde un script de Windows (`0xC0000142`).
3. **Nadie audita su propio trabajo:** el flujo siempre es *escribir → Beru audita → re-auditar*. Un `PASA` de Beru sin evidencia citada no vale.
4. **FreeLLMAPI son cupos de terceros:** puede caer. Por eso hay **fallback a OpenRouter** y no se usa para lo crítico.
5. **Un one-shot largo en primer plano se pierde:** siempre `background=true` + verificar el **artefacto en disco** (el exit code no prueba nada).
6. **Los secretos jamás se imprimen** — entran por `seawolf-secret.sh` y viven en `.env` (`chmod 600`).

---

## 6. LO QUE NECESITO DEL MONARCA
1. **La `base_url` + `api_key` de FreeLLMAPI** (por `seawolf-secret.sh`, sin imprimirla).
2. **Su visto bueno** para encender el `daemon` (es lo único que corre "siempre encendido").
3. **Qué misión** quiere para la prueba de fuego: **la tienda** o **el Círculo Publicitario**.

**Con eso, el escuadrón queda de pie — sin alquilar el cerebro a nadie.** 🐺
