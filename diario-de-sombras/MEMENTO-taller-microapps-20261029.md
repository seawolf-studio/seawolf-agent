# MEMENTO — HANDOFF PARA LA SESIÓN "TALLER MICROAPPS"

**De:** Bellion, Gran Comandante · **Para:** El Monarca (Key) y la sombra que abra el taller
**Sesión cerrada:** 29 de octubre de 2026
**Sesión destino:** **`taller microapps`**
**Estado del repo:** limpio · último commit `085758c` · empujado a `origin/master` ✅

---

## ⚡ CÓMO RETOMAR

```bash
hermes --resume 20260928_211526_47e1f3 -p beru
# o abrir la sesión nueva con nombre clave: taller microapps
```

**El Monarca anunció:** *"se me acaba de ocurrir algo, pero lo voy a pasar a otra sesión con nombre clave taller microapps."*
→ **La idea nueva NO está registrada.** Esa es la primera cosa que hay que preguntarle al abrir el taller.

---

## 1️⃣ LO QUE SE INSTALÓ HOY (los 10 skills de Hermes)

**Total del equipo: 1.000 skills** (antes ~178 → **+822**)

| # | Skill | Estado | Ganancia |
|---|---|---|---|
| 1 | **Ponytail** | ✅ plugin activo (6 skills) | Anti-sobreingeniería: −53% código, −45% tokens |
| 2 | **Planning With Files** | ✅ skill + plugin | El plan sobrevive a crash o cierre de sesión |
| 3 | **I Have ADHD** | ✅ skill | La respuesta primero, sin relleno |
| 4 | **Gbrain** | ✅ MCP (162 herramientas) | Segundo cerebro local: **115 notas indexadas** |
| 5 | **Agent Reach** | ✅ CLI + config | Ojos en X, Reddit, GitHub, YouTube |
| 6 | **Hyperframes** | ✅ ya lo teníamos | Prompt → video |
| 7 | **Taste Skill** | ✅ | Que no se note que lo hizo una IA |
| 8 | **Cybersecurity Pack** | ✅ 583+ skills | Auditar como atacante |
| 9 | **Scientific (tap)** | ✅ tap activo | Estadística y gráficos de publicación |
| 10 | **Diagram Design** | ✅ | Diagramas con ojo de diseñador |

**Descartado:** *Mission Control* (471⭐, sin licencia — y ya tenemos Sala de Mando).

**Bun 1.4.4 instalado** (requisito de Gbrain) · **pipx** instalado (requisito de Agent Reach).
**Pitfall grave cazado:** `pip install pipx` subió `packaging` y **rompía Hermes** → restaurado a 26.0 y verificado.
**Lecciones grabadas** en el skill `hermes-agent` → `references/instalar-skills-de-terceros.md`.

---

## 2️⃣ CAMBIO PERMANENTE DE COMPORTAMIENTO

**ADHD mode quedó como estilo de salida POR DEFECTO**, ordenado por el Monarca. Grabado en **memoria permanente** (se inyecta en cada sesión):

> *"Salida POR DEFECTO: ADHD mode — la acción primero en la 1ª línea, pasos numerados, reafirmar estado cada turno, sin preámbulos/recaps/despedidas, tiempos concretos, victorias visibles, máx 5 ítems por lista."*

**Se apaga** diciendo *"stop adhd mode"* o *"normal mode"*.

---

## 3️⃣ ENTREGABLES DE INVESTIGACIÓN (3 informes, con PDF, citados)

| Informe | Qué contiene | Commit |
|---|---|---|
| `intel/informe-remoto-y-microapps-2026.md` | Trabajo remoto + microapps: 24 fuentes, 96 búsquedas, 14 documentos primarios | `2bbff27` |
| `intel/RADAR-DE-DEMANDA-manual.md` | **El método** para saber qué construir antes de gastar | `13592e9` |
| `intel/RADAR-restaurantes-manuales.md` | **El Radar aplicado**: restaurantes manuales Colombia | `085758c` |

**Todos** en `C:\Users\Admin\intel\` (MD + PDF) **y** respaldados en `diario-de-sombras/investigacion/` con sus datos crudos.

---

## 4️⃣ EL HALLAZGO CENTRAL DE LA SESIÓN: **"EL CUADRE"**

### La idea
> **El hueco no es un POS. Es EL CUADRE.**
> Los ~115.000 restaurantes informales de Colombia **jamás van a adoptar un POS** — exige cambiar cómo trabajan.
> Viven en WhatsApp (94% de adultos lo usa a diario) y no se van a mover.
> **La microapp no reemplaza WhatsApp: lo instrumenta.** Le devuelve al dueño, cada noche, por el mismo WhatsApp:
> *"esto vendiste, esto gastaste, esto te queda de verdad — y aquí estás perdiendo plata."*

### La evidencia que lo sostiene
| Dato | Fuente |
|---|---|
| **11.389 reseñas de Capterra**: lo más citado NO son funciones, es que **no pueden conciliar** lo vendido con lo que llegó al banco | DeliverGuard 2026 |
| **73% de los restaurantes que cierran en año 1 tenían ventas POSITIVAS** — los mató no entender utilidad vs. caja | Masterestaurant |
| Costos operativos Bogotá: **87% → 109% de los ingresos** (2025→2026) | Presik / DANE |
| El conteo manual **solo detecta 20-30%** de la pérdida real de alimentos | SATE Institute |
| **96,7% de los restaurantes no tiene sitio web** | AtlasForgeX (9.679 censados) |

### El producto
**3 capas de Seawolf Agent (ya construido):** Filtro → Automación → Dashboard.
**Precio: $29.900 COP/mes** (~US$7,5) — **por debajo del piso del POS** ($46.000). No compite: es una capa que nadie tiene.

### El MVP (costo: **$0 de desarrollo**)
```
1. Reclutar 3 restaurantes manuales de la red del Monarca (gratis, 30 días a cambio de datos)
2. Producir el reporte nocturno A MANO con el agente — sin programar nada
3. Al día 30 pedir los $29.900. 3 pagan → se construye. 0 pagan → se descarta
```
**Puntuación del Radar: 36/40.** ✅ Se construye la puerta falsa.

---

## 5️⃣ PENDIENTES QUE ENTRAN AL TALLER

### 🔴 Lo que bloquea avanzar
1. **La idea nueva del Monarca** — dijo que se le ocurrió algo y no lo contó. **PREGUNTAR PRIMERO.**
2. **Nombrar 1 restaurante real** de su red para el piloto (el primero de los 3).
3. **Medir el costo real de la API de WhatsApp de Meta** — es el riesgo #2 del informe y **define el precio**. Sin esto no se puede fijar el margen.

### 🟡 Decisiones abiertas del informe de microapps
4. ¿Cuál **gremio vertical** alternativo si restaurantes no arranca?
5. ¿Qué **2-3 personas del escuadrón** tienen inglés/perfil para el Camino A (remoto en dólares)?
6. ¿Cuántos **meses de colchón** hay antes de necesitar ingresos?
7. ¿**Seawolf Tools** se vende como producto propio o se usa de escaparate de capacidad?

### 🟢 Pendientes de otras sesiones (no urgentes)
- **SMART de los SATA/USB**: requiere que el Monarca ejecute `LEER-SMART-ADMIN.bat` (UAC)
- **Botín de 568 GB** sin descargar (arrancar por `01-LOS-SIMPSON-236GB.txt`, cerrar MiPony primero)
- **One Piece** quedó sin enlaces al caer player4me
- **`hermes update` incompleto** (staging falla con `0xC0000142`)
- **Auto-despacho del Kanban roto** (el worker muere a los ~61 s)
- **rclone** sin configurar
- **`cloudflared.exe `** (con espacio final, creado 08:52) sin firmas — **nunca ejecutado**; el Monarca no ha confirmado si lo puso él

---

## 6️⃣ REGLAS VIGENTES QUE APLICAN AL TALLER

1. **Nada se construye sin 3 pagos reales o 20 registros calificados.** *(la puerta que evita ir a ciegas)*
2. **Reseñas de 3 estrellas = el plano. Repetida en varios competidores = el negocio.**
3. **Vender primero, programar después.**
4. **Vertical, no horizontal** (crece 2-3× más rápido).
5. **Buscar primero en el propio archivo (Gbrain, 115 notas) antes de buscar afuera.**
6. **La acción primero en la 1ª línea. Máx 5 ítems por lista.** *(ADHD mode)*
7. **Secretos solo en `.env`/archivos locales. Nunca en el repo, informes ni git.**
8. **Nunca `| head` en `npx skills add`** (SIGPIPE mata el instalador).
9. **MiPony cerrado antes de tocar `linkList.xml`.**
10. **Prohibido: Shopify, AdSense, burocracia de Facebook.**

---

## 7️⃣ MAPA DE ARCHIVOS DE ESTA SESIÓN

```
C:\Users\Admin\intel\
├── informe-remoto-y-microapps-2026.md / .pdf
├── RADAR-DE-DEMANDA-manual.md / .pdf
├── RADAR-restaurantes-manuales.md / .pdf
├── los-10-skills-hermes-instalados-20261029.md
├── inv-remoto-microapps-20261029/     (raw + 14 fuentes)
├── inv-demanda-20261029/              (raw + fuentes)
└── radar-restaurantes-20261029/       (raw + 5 fuentes)

C:\Users\Admin\seawolf-agent\diario-de-sombras\
├── investigacion/  (los 3 informes + PDFs + datos crudos)
├── los-10-skills-hermes-instalados-20261029.md
└── MEMENTO-taller-microapps-20261029.md  ← este archivo
```

**Herramientas clave vivas:** Seawolf Tools (`herramientas.sw-st.net`, cerradura activa) · WAHA + Seawolf Agent (VPS `76.13.109.237`, sesión WhatsApp `seawolf` WORKING) · Gbrain (115 notas) · Agent Reach.

---

## 8️⃣ LA FRASE PARA ABRIR EL TALLER

> *"Monarca, el Radar ya tiene un veredicto: El Cuadre, 36/40, MVP de costo cero. Pero usted dijo que se le ocurrió algo. ¿Lo escucho primero?"*

---

*Salve, Gran Monarca. El ejército queda en formación y el taller, encendido.*
**— Bellion, Gran Comandante del Ejército de Sombras.**
