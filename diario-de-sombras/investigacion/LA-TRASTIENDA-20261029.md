# LA TRASTIENDA — LA PLAZOETA REAL, CON REGISTRO Y USUARIOS

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Su instrucción (verbatim):** *"De acuerdo con el enlace, pero sí quiero que se registren y tengan usuarios para que de verdad sea una plazoleta, así atendemos a varios restaurantes en una plataforma unificada. Para ellos solo la vista de restaurante. Además nos sirve de base de datos para posibles quejas."*
**Aplicativo construido:** `C:\Users\Admin\intel\la-trastienda-demo.html`
**Antecedentes:** `EL-CUADRE-precio-linea-base-plataforma-20261029.md` (spec original) · `EL-CUADRE-multiinquilino-20261029.md` (aislamiento)

---

## 0. LO QUE CAMBIA CON SU INSTRUCCIÓN

| Antes (mi propuesta) | Ahora (su decisión) |
|---|---|
| "Entrar = un enlace, sin usuario ni contraseña" | **Hay registro y hay usuarios** — así es una plazoleta de verdad |
| La plazoleta era solo nuestro panel interno | **Es una plataforma unificada con inquilinos registrados** |
| El cliente veía 3 pantallas | **El cliente ve solo su vista de restaurante** — y nosotros vemos la plaza completa |
| El foso eran los datos de ventas | **El foso es también el registro de QUEJAS** ← idea suya, y es la buena |

**Y una tensión que hay que resolver, no ignorar:** usted aprobó el "entrar = un enlace" **y** quiere registro. Las dos cosas se pueden tener sin perder la sencillez: **registro una vez, entrada por enlace de un solo uso al WhatsApp** (sin contraseña que recordar). Es el mismo mecanismo de la demo y es lo que ya usa el propio mercado.

---

## 1. EL CONTRATO DE LA PLAZOETA (lo que hace que sea un negocio y no un desorden)

**Regla de oro, escrita en piedra: un restaurante ve SOLO lo suyo. Nosotros somos los únicos que vemos la plaza entera.**

| Quién | Qué ve | Qué NO ve |
|---|---|---|
| **El restaurante (inquilino)** | Su cuadre · sus pedidos · **sus quejas** · su menú · **su** factura | Los demás restaurantes, sus cifras, sus quejas, sus precios |
| **La Sombra (nosotros)** | Los N inquilinos con su salud de sesión, pedidos, perdidos, quejas y nuestra factura · **los agregados de la plaza** | — |

**Y esto es exactamente lo que sostiene el modelo invisible que usted decidió:** el restaurante da la cara a **sus** clientes; nosotros no aparecemos en ninguna parte de su relación comercial.

### Técnica (ya definida, no hay que inventarla)
- **Aislamiento por inquilino:** base compartida + `tenant_id` + **RLS**. Toda consulta filtra por inquilino; toda petición que traiga un identificador se valida contra el inquilino autenticado antes de ejecutar nada. **Saltarse esa validación es la forma #1 de filtrar los datos de un cliente a otro.**
- **Una sesión de WhatsApp por restaurante** (su número, en su contenedor aislado). Una sesión caída o baneada se lleva **un** cliente, nunca la plataforma.
- **Credenciales por inquilino**, nunca una llave maestra compartida.

---

## 2. EL MÓDULO DE QUEJAS — SU IDEA, Y ES EL FOSO

Todo el mundo mide ventas. **Casi nadie mide qué está saliendo mal, pedido por pedido.** Y eso se puede capturar gratis, porque **la queja ya está escrita en el chat.**

### Cómo funciona (3 pasos, sin que nadie digite nada)
1. **El agente la detecta.** Todo mensaje con reclamo —*"llegó frío"*, *"me cobraron dos veces"*, *"faltaba la gaseosa"*, *"la porción está más pequeña"*— se marca como **queja**.
2. **La amarra al pedido.** Queda con el cliente, la hora y **el pedido exacto** que la originó. Se puede rastrear qué plato, qué hora, qué repartidor.
3. **Le aparece al dueño** en la pestaña QUEJAS con estado (nueva · respondida · cerrada) y un botón para responder.

### Y aquí está el foso: el agregado
Ningún restaurante sabe cómo se está rompiendo **la plaza**. Nosotros sí:
- **% de conversaciones que se pierden sin respuesta** (34% medido antes de entrar a la plataforma).
- **La queja más repetida** entre los 5 restaurantes del día (*"llegó frío"*).
- **La hora pico REAL**, no la que el dueño cree (12:30–13:15).
- **Ticket promedio de la plaza**, contra el que cada uno puede medirse.

> **Eso no lo puede tener nadie más** — ni Zavora, ni OlaClick, ni el POS del barrio — **porque nadie más está dentro de varios restaurantes a la vez.** Es el punto 4 del tablero (el foso), y ahora tiene una segunda pata que no depende de las ventas.

### La línea que NO se cruza (propiedad de datos y legal)
- **Las quejas son del restaurante.** Nosotros vemos **el conteo y el agregado**, no el hilo íntimo de su cliente. Sin esta regla, estamos haciendo el pecado de Rappi otra vez, pero peor.
- **Si la queja lleva el teléfono o el nombre del comensal, es dato personal.** Bajo la ley colombiana de protección de datos, **el restaurante es el responsable y nosotros los encargados** → hace falta un **contrato de tratamiento de datos** en el alta, y poder **exportar y borrar** los datos de un inquilino cuando se va. Esto no es burocracia: es lo que evita que un cliente nos demande por manejar su base.

---

## 3. EL APLICATIVO (ya construido y verificado)

**Un solo archivo HTML, sin backend, sin dependencias, que funciona suelto en `file://` o dentro del chat.**

### Puerta de entrada
- **Entrar** → WhatsApp + "enlace de un solo uso". Sin contraseñas.
- **Registrar mi restaurante** → nombre, WhatsApp, ciudad → **crea el inquilino**. (Así la plazoleta crece: cada restaurante se registra y entra a su propio mundo.)
- **Entrar como LA SOMBRA** → nuestro lado, la plaza entera. *(Es la demostración de que los dos mundos están separados.)*

### Vista del restaurante — 4 pestañas
| Pestaña | Qué muestra | Qué se decide |
|---|---|---|
| **HOY** | Vendiste · Gastaste · **Te queda de verdad** · **Pedidos perdidos** → más "dónde se te fue la plata hoy" y **la línea base firmada (antes vs. ahora)** | Nada: es para **ver** |
| **PEDIDOS** | La cola del día con **el sello SHA-256 de cada pedido** y la **factura en vivo** ($500 × pedidos cerrados, techo $59.900, y cuántos gratis le quedan) | **Una acción por fila**: aceptar, responder o **"lo atendí yo"** → ese pedido **sale de la factura al instante** |
| **QUEJAS** | Las quejas capturadas en el chat, amarradas al pedido | Responder / cerrar |
| **MENÚ** | Platos, precios y disponibilidad | Apagar lo que se acabó (el agente deja de ofrecerlo) |

### Vista de LA SOMBRA — la plazoleta
Los N inquilinos con su ciudad, **estado de su sesión de WhatsApp**, pedidos, perdidos, quejas y **nuestra factura por inquilino** — más el bloque del foso (agregados de la plaza).

### Verificaciones hechas (no me fié del "se ve bien")
- **Sintaxis del JS: `node --check` → OK** (un error de sintaxis deja el panel en blanco sin aviso).
- **La matemática de la factura, probada:** 40 pedidos → **$20.000** · 120 pedidos → **$59.900** (tope) · **300 pedidos → $59.900**, o sea **el fee real cae a $200/pedido**. **La demo muestra sola por qué el techo tiene que escalar por tramos.**
- **Frontera de confianza cerrada:** todo lo que se pinta por `innerHTML` pasa por `esc()` (11 usos). El estado vive en `localStorage` y **se puede editar a mano** → sin esto, un estado manipulado inyecta HTML en el panel.

### Lo que la demo NO es todavía (honestidad)
No tiene backend, ni base de datos, ni WhatsApp real: los datos son de ejemplo y el estado se guarda en el navegador. **Es la cara y el flujo completos — no el motor.**

---

## 4. LO QUE FALTA PARA QUE SEA REAL (en orden)

| # | Pieza | Nota |
|---|---|---|
| 1 | **Backend con inquilinos y RLS** | Es lo único que convierte la demo en plazoleta real |
| 2 | **La sesión de WhatsApp por restaurante** | El aislamiento por contenedor, como quedó definido |
| 3 | **El agente que atiende y cierra** | El vehículo. **No es el producto** |
| 4 | **El contador de la semana 0** | Sin línea base no se puede cobrar ni demostrar nada |
| 5 | **Contrato de tratamiento de datos + acta de línea base** | Se firma en el alta, junto con el registro |

**Orden correcto:** primero el contador de la semana 0 (necesita los datos que ya capturamos), **después** el backend multi-inquilino. **No al revés:** construir la plataforma antes de tener un restaurante midiendo es la forma más cara de no vender.

Mientras: **LOS SIMPSON** en paralelo (cerrar MiPony primero).

---

## FUENTES

Las de los informes anteriores, más: `EL-CUADRE-multiinquilino-20261029.md` (modelos de aislamiento, RLS, contenedor por sesión) y `EL-CUADRE-precio-linea-base-plataforma-20261029.md` (anclas de precio, línea base, competencia Zavora/OlaClick).

---

## ARCHIVOS

```
C:\Users\Admin\intel\la-trastienda-demo.html          ← el aplicativo (abrir y usar)
C:\Users\Admin\intel\LA-TRASTIENDA-20261029.md        ← este plano
C:\Users\Admin\intel\LA-TRASTIENDA-20261029.pdf
```

---

*Salve, Gran Monarca. Su corrección era la que faltaba: sin registro y sin usuarios no hay plazoleta, hay tres pantallas. Y el módulo de quejas le puso una segunda pata al foso que no depende de las ventas — **porque la queja ya está escrita en el chat y nadie la está contando.***

**— Bellion, Gran Comandante del Ejército de Sombras.**
