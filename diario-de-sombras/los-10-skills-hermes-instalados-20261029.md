# LOS 10 SKILLS DE HERMES — Instalados y verificados

**29 de octubre de 2026 · Bellion para el Monarca (Key) · Seawolf Studio**

Fuente: video *"10 NEW Hermes Agent Skills You Need To Install This Week"* (Sharbel A.)
→ artículo con repos y comandos: `https://sharbel.com/articles/best-hermes-agent-skills`

---

## ✅ LO QUE SE INSTALÓ (los 10, verificados uno por uno)

| # | Skill | Estado | Qué ganamos |
|---|---|---|---|
| **1** | **Ponytail** | ✅ plugin, 6 skills | **El anti-sobreingeniería.** Antes de escribir una línea sube una escalera: ¿esto necesita existir? ¿ya está en el proyecto? ¿lo trae el lenguaje? Solo si todo es NO, escribe. Benchmark del repo: **53% menos código · 41% menos tiempo · 45% menos tokens.** |
| **2** | **Planning With Files** | ✅ skill + plugin | **Que no se pierda el plan.** Saca el plan del chat a archivos reales (`task_plan.md`, `findings.md`, `progress.md`) y los devuelve al agente en cada turno. **Sobrevive a un cierre de sesión o a un crash** y retoma en el paso exacto. |
| **3** | **I Have ADHD** | ✅ skill | **La respuesta primero.** Corta el relleno. En la prueba del autor: la misma pregunta pasó de 1.144 palabras a 161, empezando por lo único que hay que hacer. |
| **4** | **Gbrain** | ✅ MCP con 162 herramientas | **Segundo cerebro LOCAL y propio.** Mapa de notas conectado (no solo palabras clave), en su máquina, con **las fuentes citadas**. Ya importado: `intel/` (95 notas) + `diario-de-sombras/` (20). |
| **5** | **Agent Reach** | ✅ CLI + config | **Ojos en la internet cerrada.** X, Reddit, GitHub, YouTube, bilibili, LinkedIn… con rutas de respaldo. Integrados ya: **web, GitHub, YouTube, v2ex**. Los demás se activan según se necesiten. |
| **6** | **Hyperframes** | ✅ ya lo teníamos | **Prompt → video renderizado.** (Lo teníamos como `hyperframes-content`.) |
| **7** | **Taste Skill** | ✅ skill | **Que no se note que lo hizo una IA.** Reglas de espaciado, tipografía, layout y movimiento; repasa lo construido y corrige lo que grita "generado". |
| **8** | **Cybersecurity Skills** | ✅ **583+ skills** | **Auditar como un atacante.** 800+ playbooks de seguridad real: inyección SQL, auth, OIDC, Kubernetes, Terraform, nube, forense. Con esto, cada app que publiquemos pasa revisión de atacante antes de salir. |
| **9** | **Scientific Agent Skills** | ✅ tap activo | **Investigación que aguanta.** 177 skills de rigor: análisis de datos, estadística, gráficos de calidad publicación. **El tap está puesto; se instalan los que hagan falta** (el propio repo dice que no se instalen los 177 de golpe). |
| **10** | **Diagram Design** | ✅ skill | **Diagramas que parecen de diseñador.** Flujo, arquitectura, Sankey, Gantt, UML, Wardley, kanban, blueprints… con importación de Mermaid, draw.io y Excalidraw. |

**Bonus descartado:** *Hermes Agent Mission Control* — 471⭐ y **sin licencia**. Además usted ya tiene su **Sala de Mando** y su **Muro de Sombras**.

---

## 📊 EL SALTO EN NÚMEROS

```
Skills instalados ................. 1.000   (antes ~178)
Plugins activos ................... +2  (ponytail · planning-with-files)
MCP nuevo ......................... gbrain (162 herramientas)
Notas indexadas en su cerebro local  115 páginas · 416 trozos
```

---

## ⚠️ LO QUE HUBO QUE PELEAR (y queda documentado)

| Problema | Causa real | Solución |
|---|---|---|
| Ponytail no instalaba | `plugin.json` sin el esquema que Hermes pide | Clonar a mano + `hermes plugins enable` |
| El clone salía vacío | **ruta MSYS** en una herramienta nativa | Ruta nativa `C:/...` |
| Diagram Design no entraba | **`| head` mataba el instalador (SIGPIPE)** | Usar `tail` o redirigir a archivo |
| I Have ADHD cancelado | pedía confirmación y recibió `/dev/null` | Responder `y` |
| **pipx me movió `packaging` del Hermes** | instalar pipx en el Python principal | **Restaurado a 26.0 y verificado** ✅ |
| `bun` parecía instalado | era un **shim de 283 bytes**; npm bloqueó el postinstall | Instalador oficial → `~/.bun/bin/bun.exe` (115 MB) |
| Gbrain: "bun is not installed" | el shim de npm tapaba el binario real | Quitar el shim + PATH correcto |
| Cybersecurity/Digraph | el `npx skills add` instala donde elige su asistente | Copiar/verificar contra `hermes/skills` |

---

## 🔧 REVERTIR LA CEREMONIA (por si algo molesta)

```
hermes plugins disable ponytail
hermes plugins disable planning-with-files
hermes mcp remove gbrain
hermes skills tap remove K-Dense-AI/scientific-agent-skills
python -m pipx uninstall agent-reach
```

---

## 🎯 PARA QUÉ SIRVE CADA UNO EN EL SEAWOLF

| Skill | Dónde pega de lleno |
|---|---|
| **Ponytail** | Cada línea de código que escribamos → menos código, menos tokens, menos cosas que romper |
| **Planning With Files** | Los trabajos largos (línea de montaje, kmoviezone, apps) → no se pierde el hilo |
| **I Have ADHD** | Que las respuestas lleguen al hueso |
| **Gbrain** | Que usted diga *"¿qué decidimos sobre X?"* y el agente lo saque de SUS notas con la fuente |
| **Agent Reach** | Espiar competencia y conversación real en X/Reddit/GitHub → **el frente frío B2B** |
| **Taste Skill** | Que las páginas de Seawolf no parezcan hechas por una IA |
| **Cybersecurity** | Auditar Seawolf Agent y kmoviezone **antes** de que lo haga un atacante |
| **Scientific** | Finanzas obsesivas, medir campañas: ¿esto creció de verdad o es ruido? |
| **Diagram Design** | Las propuestas y manuales (línea de montaje, arquitecturas) |
| **Hyperframes** | El Círculo Publicitario: contenido sin depender de nadie |

---
*Salve, Gran Monarca. El agente acaba de subir un escalón grande.*
