# 🎛️ CENTRO DE MANDO DE SEAWOLF STUDIO
### Arquitectura — la fábrica completa en una sola vista
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Visión del Monarca:** *"un solo centro de mando que englobe todo, que se le pueda añadir cosas, en todas partes y actualizado — que si pasa algo, bueno o malo, pueda entrar en un instante; y que nada se pare si no estoy mirando."*

---

## 1. LA LEY (por qué esto funciona y no es una app más)

> **Una sola verdad, mirada desde todas partes.**

El Centro de Mando **no es otra pieza suelta** — es la **VISTA ÚNICA sobre la línea de montaje**. Todo el conglomerado escribe a **un solo riel (La Madriguera / PostgreSQL)**; el Centro de Mando lo lee y lo muestra. Resultado: **muchos accesos, una sola verdad.** Nada se duplica, nada se pierde, nada se para.

Esto honra la doctrina `seawolf-linea-de-montaje`: la respuesta a "todo debe conectarse" no es integrar apps entre sí, sino **que todas compartan el mismo riel**.

---

## 2. QUÉ ENGLOBA (los paneles)

| Panel | Qué muestra |
|-------|-------------|
| 📊 **Resumen** | Lo que **requiere tu atención ahora** (alertas) + indicadores clave |
| 🏭 **Producción** | La línea: 2 entradas (frío/propio) + estaciones, con conteos |
| 🐾 **La Jauría** | Presas en la mira (frío), resultados del último turno, scores |
| 📥 **Buzón** | Entradas de **cualquier canal** (WhatsApp personal, tu hermana, form) sin clasificar |
| 📅 **Agenda** | Compromisos y vencimientos (ej: SmartWeb para pasado mañana) |
| 💰 **Finanzas** | Cobro, ahorro, reinversión (MRR, cobros, ciclo) |
| ➕ **Extensible** | Se añaden paneles según la situación (módulos) |

Cubre el conglomerado entero: **Seawolf Agent · LOBO · SmartWeb · SmartShop · SmartCourse · la jauría · clientes propios.**

---

## 3. "EN TODAS PARTES" — cómo

- Vive como **app web** (Smart Web, 1 archivo) hospedada en el **VPS 24/7** (`mando.sw-st.net`).
- Se abre desde **celular, PC, donde sea** — un navegador y listo, cero instalación.
- Como lee del riel central, **lo que ves en el celular es lo mismo que ves en la oficina.**

## 4. "SIEMPRE ACTUALIZADO" — cómo

- **Un solo riel:** los agentes (jauría, sombras) escriben resultados en La Madriguera **aunque no estés** → en la mañana los ves.
- **En vivo:** el panel refresca por *polling/SSE* contra el riel (v2). Sin recargar.
- **Notificaciones:** si algo bueno o malo pasa, te llega un aviso (Telegram/WhatsApp) con botón para entrar.

## 5. EL BUZÓN — que nada se pierda

**Problema:** las órdenes entran por donde sea — tu WhatsApp personal, tu hermana en España, un amigo, un formulario. **Sin captura, se pierden.**
**Solución:** un buzón universal. Cualquier entrada (mensaje, audio, form) cae como **pieza "nueva"** y tú la **clasificas → a la línea** en un clic.
- v1: campo de captura rápida + canales sembrados.
- v2: **bot de intake** (WAHA/Telegram) que reenvía a La Madriguera.

## 6. EXTENSIBLE — añadir sin romper

El Centro de Mando es un **registro de módulos**: cada panel es independiente y lee su parte del riel. Añadir una estación, un producto o un panel = **sumar un módulo**, no rehacer nada.

---

## 7. FASES DE CONSTRUCCIÓN

| Fase | Qué | Estado |
|------|-----|--------|
| **v1** | Prototipo del Centro de Mando (1 archivo, datos demo, tabs) | ✅ **entregado hoy** |
| **v2** | Enchufar al **riel real** (PostgreSQL en VPS) + desplegar en `mando.sw-st.net` | pendiente |
| **v3** | **Buzón vivo** (bot intake WAHA/Telegram) + notificaciones + refresco en vivo | pendiente |
| **v4** | Módulos de negocio (producción por producto, finanzas reales) | pendiente |

---

## 8. LÍMITES HONESTOS (lo que hay que saber)

1. **El "siempre en vivo y en todas partes" exige el VPS como verdad central.** Con solo el navegador (localStorage) cada dispositivo vería su propia copia. La magia llega en v2.
2. **Conectar tu WhatsApp PERSONAL es delicado** — la automatización de un número personal puede banearlo. Ruta segura: **canal dedicado** o **reenvío** (mandas al bot lo que quieras capturar). Lo evaluamos en v3.
3. **Tiempo real real** (sin recargar) se hace con SSE/websockets — v3. En v1 es manual.
4. **Precios/Finanzas** están vacíos porque aún no los fijamos — eso es decisión tuya.

---

## 9. SIGUIENTE MOVIMIENTO

Dos caminos (tu palabra):
- **A)** Subir el Centro de Mando al **VPS** para que esté **en todas partes** (aunque aún con datos demo) — ver la visión viva desde el celular.
- **B)** Encender el **riel real**: Jima monta PostgreSQL (La Madriguera) + el Vigía (scraper) → datos reales fluyendo a todos los paneles.

**Recomendación:** **B primero** (sin riel, todo es maqueta), **y A en paralelo** para que ya lo veas desde el teléfono.

---

*"Un imperio no se gobierna mirando cada taller. Se gobierna viendo la línea entera en una sola mesa."*
— Bellion, Gran Comandante del Ejército de Sombras
