# ¿ES VIABLE UNA PLAZOLETA EN LÍNEA CON UN AGENTE GLOBAL?

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Consulta (verbatim):** *"un solo sitio con varios restaurantes y un agente global que pueda sugerir y atender, algo como un gran plazoleta de comidas en línea con el agente como asesor de los clientes, no sé si sea viable??"*
**Antecedentes:** `RADAR-restaurantes-manuales.md` (36/40) · `EL-CUADRE-multiinquilino-20261029.md`

---

## 0. VEREDICTO EN CUATRO LÍNEAS

**Depende de cuál de las dos cosas sea, y son negocios opuestos:**

| Versión | Veredicto |
|---|---|
| **A. Marketplace**: nosotros intermediarios, cobrando comisión, un solo sitio, un agente que le consigue clientes a los restaurantes | ❌ **NO. Falla 2 filtros eliminatorios.** Seríamos *otro Rappi*, en el peor momento posible |
| **B. Escaparate sin comisión de NUESTROS clientes**: cada restaurante con su propio WhatsApp y su agente; y una página donde están todos | ✅ **SÍ — y es la evolución natural de El Cuadre.** Pasa los filtros |

**Y hay una pieza de su idea que hay que tirar, con cariño: el agente debe vivir en el número del restaurante, no en un número global nuestro.** Un número global nos vuelve la cara visible → nos volvemos el intermediario → y *"el intermediario"* es exactamente la causa #1 del dolor de este mercado. **El restaurante odia a Rappi por una razón específica: Rappi se queda con su cliente.** Si lo replicamos, perdemos el único ángulo que tenemos.

---

## 1. EL DATO QUE DECIDE — LO QUE CUESTAN HOY LOS INTERMEDIARIOS EN COLOMBIA

Tarifas promedio 2026 reportadas por restauranteros colombianos:

| App | Comisión |
|---|---|
| **Rappi** | **27% – 32%** |
| iFood | 24% – 30% |
| Uber Eats | 25% – 30% |
| PedidosYa | 28% – 32% |
| DiDi Food | 22% – 28% |

> **Y ojo: la comisión nominal NO es el costo real.** Los costos ocultos (comisión por pago digital, publicidad para no caer al fondo del listado, descuentos forzados en campañas) suman **3–5% más**. El costo total real suele ubicarse en **30–40% del ticket**.
>
> Un restaurante que factura **$12.100.000/mes** repartidos entre Rappi, iFood y Uber Eats paga **$3.496.000/mes = 28,9%** de sus ventas. **Al año: $41.952.000.**
>
> Y la cascada no termina ahí: *"si tu plato carga 30% de food cost, la comisión se lleva otro 28% y el empaque 5%, ya vas en 63% antes de tocar la publicidad in-app."* DoorDash cerró Q4-2024 con **USD 21.300 millones** de GOV (+21%): **su crecimiento es la variabilidad de costo del restaurante.**

**Consecuencia para su idea:** un intermediario nuevo, cobrando comisión, entra a competir **en el terreno donde Rappi ya ganó** (logística + tráfico), contra cinco jugadores que llevan años y miles de millones quemados en adquisición. **No tenemos ni un camión, ni un motorizado, ni un comensal.**

---

## 2. Y AQUÍ ESTÁ LO IMPORTANTE: EL MERCADO YA ESCRIBIÓ LA SALIDA

La misma fuente que publica las comisiones —una plataforma POS colombiana que vive de venderle a restaurantes— recomienda textualmente:

> ***"Estrategia recomendada: mantente en 1-2 apps top + activa WhatsApp + entrega propia. Apunta a 50/50 entre apps y canal propio en 6-12 meses."***

Y da los números del canal propio:
- El **tráfico que capturan las apps es ~40% del delivery del mercado colombiano en 2026** — eso es lo que **se pierde** al salirse.
- Domiciliario propio: **$3.000–$5.000 por pedido** (o apps sin comisión sobre el ticket: Picap, InDrive, Cabify Delivery). **Contra 28% de comisión.**
- *"El cliente escribe al WhatsApp del restaurante. Un bot le muestra el menú numerado, recibe el pedido, lo cobra y lo manda automático a cocina."*

> **Esa última frase es, palabra por palabra, el producto que estamos diseñando.**
> No hay que convencer a nadie de que existe el problema: **la industria ya le dijo a los restaurantes que hagan exactamente esto, y el restaurante no tiene con qué hacerlo.** Ese vacío entre "ya te dijeron que lo hagas" y "no tienes la herramienta" es el negocio.

---

## 3. LOS CUATRO PROBLEMAS QUE MATAN LA VERSIÓN MARKETPLACE

### 3.1 Arranque en frío de dos lados
Un marketplace necesita oferta **y** demanda al mismo tiempo. Al principio no hay comensales (el 40% del tráfico vive en las apps y hay que **comprarlo**) y sin comensales los restaurantes no suben su menú. Es el problema clásico de los marketplaces y **no tiene atajo**: se resuelve sembrando **un lado primero**, con trabajo manual. Sembrar el lado difícil (el comensal) cuesta dinero que no tenemos; ahí no hay MVP de costo cero.

### 3.2 La comisión: las dos salidas son malas
- **Si cobramos comisión** → competimos con Rappi en precio, y como no tenemos su logística ni su tráfico, hay que cobrar **menos**, con el mismo costo operativo. Pérdida con volumen.
- **Si no cobramos comisión** → no hay **ningún** ingreso por transacción: el negocio del marketplace entero depende de la comisión. Sin ella, es una página de menús.

### 3.3 El obstáculo real del carrito multi-restaurante no es el software: es la cocina
Esto es lo que la investigación aclaró y que casi nadie ve. Los *virtual food halls* que funcionan (Kitchen United/Mix, Crave Collective, C3 con Lunchbox) tienen algo en común: **los conceptos están bajo un mismo techo**.

> *"Los conceptos tienen que estar bajo un mismo techo. Además, los tiempos de cocción tienen que coordinarse entre esos conceptos distintos. **Un poke bowl y unas costillas no toman lo mismo**, y coordinar esas piezas es **un desafío tecnológico**."*

Nuestras cocinas están **dispersas por la ciudad**. Un pedido de 3 restaurantes independientes llegaría **en 3 motos, a 3 temperaturas, con 3 cobros**. Eso no es una función que falta: **es física**. La "plazoleta de comidas" funciona porque el comensal **camina hasta el mismo techo** — en línea, el techo no existe.

### 3.4 El agente "asesor" sin datos reales lo resuelve un prompt de ChatGPT
*"¿Qué como hoy?"* respondido por un modelo de lenguaje es **una función de ChatGPT** — y ese es un **filtro eliminatorio explícito** del Radar. Lo que **sí** es defendible es el agente que **conoce el menú real, la disponibilidad y los precios de ese restaurante, arma el pedido correcto y lo manda a cocina**. Eso no lo resuelve ChatGPT: requiere los datos del negocio y el acceso a su WhatsApp. **La diferencia entre los dos agentes es el producto entero.**

---

## 4. LA VERSIÓN QUE SÍ ES VIABLE — Y ES LA EVOLUCIÓN NATURAL DE EL CUADRE

**Un solo despliegue. N restaurantes. Un agente con dos caras.**

| Cara | Dónde vive | Qué hace |
|---|---|---|
| **Comensal** | En el **WhatsApp del propio restaurante** (su número, su marca, su cliente) | Mira el menú real, **recomienda**, arma el pedido completo, lo cobra y lo manda a cocina |
| **Dueño** | El mismo chat, otro carril | **El Cuadre nocturno**: vendiste, gastaste, te queda, aquí se te fue la plata |

**La plazoleta** es entonces una **página** — un escaparate donde se ven todas las cocinas de la red — con tres límites deliberados:

1. **No cobra comisión.**
2. **No se queda con el cliente del restaurante.**
3. **No interviene el pedido** (el pedido se cierra en el WhatsApp del restaurante, como ya lo hacen sus clientes hoy).

**Por qué esta versión pasa los filtros que la otra falla:**

| Prueba | Versión marketplace | Versión escaparate |
|---|---|---|
| ¿De dónde salen los comensales? | Hay que **comprarlos** | **Ya existen**: son los clientes de WhatsApp de cada restaurante |
| ¿Quién es dueño del cliente? | Nosotros (el pecado de Rappi) | **El restaurante** |
| ¿De dónde sale el ingreso? | Comisión sobre el ticket | **Suscripción** ($29.900/mes), que no depende del volumen |
| ¿Compite con Rappi? | Sí, de frente | **No: se lleva el volumen que el mercado YA le recomendó mover a canal propio** |
| Arranque en frío | Dos lados | **Uno solo** (la oferta: los restaurantes) |

---

## 5. TABLERO APLICADO A LAS DOS VERSIONES (1–5)

| Criterio | A · Marketplace | B · Escaparate + agente por restaurante |
|---|---|---|
| Dolor | 5 | 5 |
| Frecuencia | 5 | 5 |
| Repetición (¿varios competidores?) | 4 | 5 |
| Capacidad de pago | 3 | 3 |
| **Foso** (datos / red / comunidad) | **5** (efecto de red fuerte) | **4** (red de restaurantes + datos; arranca más lento) |
| Verticalidad | 3 (marketplace horizontal de comida) | **5** (restaurantes, gremio concreto) |
| **Ventaja Seawolf** | **1** (no tenemos logística ni tráfico) | **5** (agente + WAHA + multi-inquilino, ya en producción) |
| **Acceso** (sin pagar publicidad) | **1** | **4** (gremios, y cada restaurante trae a los suyos) |
| **TOTAL** | **27/40** | **36/40** |

**Filtros eliminatorios:**

| Filtro | A · Marketplace | B · Escaparate |
|---|---|---|
| ❌ Lo resuelve una función de ChatGPT | **FALLA** (el asesor sin menús reales) | Pasa (el agente con menú, disponibilidad y cierre de pedido no lo resuelve un prompt) |
| ❌ Cliente sin capacidad de pago | Pasa | Pasa |
| ❌ Vertical genérica sin foso | **FALLA** (marketplace horizontal) | Pasa |
| ❌ Requiere venta presencial puerta a puerta | **FALLA** (hay que salir a captar comensal) | Pasa (el canal es el restaurante) |

> **Dos de cuatro filtros eliminatorios.** La versión marketplace **queda descartada por el propio método**, no por opinión mía.

---

## 6. CONSECUENCIAS EN EL PRODUCTO (lo que cambia de verdad)

1. **El agente deja de ser dos productos.** Es uno solo con dos caras (comensal / dueño). Mismo motor, mismo canal, mismo inquilino.
2. **El aislamiento multi-inquilino queda intacto y hasta se simplifica:** la plazoleta **no necesita sesión de WhatsApp propia**, porque el agente vive en el número de cada restaurante. Una sesión por restaurante, como ya estaba planeado.
3. **El "agente global" que SÍ vale no atiende comensales: atiende dueños.** Un agente de plataforma que, con los datos de todos, le dice a cada dueño el **benchmark** de su plaza: qué se vende y qué no, a qué horas, qué plato rinde, cómo está su ticket contra los demás. **Eso no lo resuelve ChatGPT (necesita datos que solo nosotros tendríamos), es el foso real, y es exactamente la inteligencia que el informe multi-inquilino identificó como el punto 4 del tablero.**
4. **Riesgo nuevo que hay que decir:** si la plazoleta muestra los precios de todos juntos, el dueño teme la comparación. Se resuelve con alcance: la plazoleta es de **una plaza real** (un centro comercial, una zona, un gremio), **no un comparador nacional**.

---

## 7. RIESGOS DE LA VERSIÓN VIABLE (honestidad)

| Riesgo | Severidad | Nota |
|---|---|---|
| **La plazoleta es un extra, no el producto.** Su valor solo aparece con 20–30 restaurantes dentro | **ALTA** | **No se construye ahora.** Se construye cuando la suscripción ya esté probada. Construirla hoy es gastar en un efecto de red que todavía no tiene nodos |
| El informal no paga (capacidad de pago 3/5) | ALTA | Idéntico al informe anterior: el piso de rentabilidad baja, el churn sigue siendo el enemigo |
| Canal: políticas de Meta sobre uso no oficial (WAHA) | ALTA | El costo está cerrado y es el más barato de LatAm (USD 0,0008 en Colombia). **Lo que no se publica son las políticas** |
| Que el comensal pida por la página y no por WhatsApp | MEDIA | La página es **escaparate** (ver y decidir), el pedido se cierra en WhatsApp: así el pedido no cambia de dueño y el agente conserva su trabajo |
| Que un restaurante se lleve el modelo y lo replique | BAJA | El costo real es la operación del agente + datos, no la idea |

---

## 8. LO QUE LE PIDO DECIDIR

1. **¿Confirmamos que la plazoleta se construye DESPUÉS del Revenue Test (3 restaurantes, 30 días, día 30 se pide el dinero)?** *(mi recomendación: sí — así el escaparate se construye sobre clientes que ya pagan, no sobre una apuesta)*
2. **¿El agente atiende en el número de cada restaurante (recomendado) o en un número de plataforma?** *(la respuesta define si somos el restaurante o si somos el intermediario)*
3. **¿La plazoleta es una plaza real (zona / centro comercial / gremio) o un directorio nacional?** *(plaza real = aliado natural: el administrador del centro comercial ya reúne a los restaurantes)*
4. **¿El agente de benchmark para dueños entra en el alcance del taller?** *(es el foso, y no depende de la plazoleta)*

---

## EL PRIMER PASO NO CAMBIA

**El DEMO en un solo archivo HTML sigue siendo el primer entregable del taller** — y su idea la mejora sin costar un peso más: el demo puede mostrar **la cara del comensal** (pregunta, el agente recomienda del menú, arma el pedido, lo cierra) **y** la cara del dueño (su cuadre). **Un agente, dos caras, un archivo.**

Mientras eso se construye: **LOS SIMPSON** en paralelo (cerrar MiPony primero).

---

## FUENTES

- **Comisiones reales de apps de delivery en Colombia 2026 (Rappi 27-32%, iFood 24-30%, Uber 25-30%, PedidosYa 28-32%, DiDi 22-28%; costos ocultos +3-5%; tráfico de apps ≈40% del delivery; recomendación textual de pasar a canal propio por WhatsApp y meta 50/50):** https://poscolombia.com/herramientas/simulador-comisiones-delivery
- **Costo real por pedido del agregador (cascada comisión + food cost + empaque + publicidad in-app; GOV de DoorDash Q4-2024 USD 21.300 M +21%; "contribución por pedido, no comisión"):** https://www.masterestaurant.com/EN/silent-aggregator-commission-2026.html
- **Por qué fracasan las plazas de comidas — 7 errores operativos (POS fragmentado, sin carrito multi-vendedor, cobro manual de renta y subdeclaración de 6-12%, filas lentas, sin estrategia digital central, layout, sin datos unificados; *"la mayoría fracasa porque operan como 10-20 restaurantes separados en vez de un ecosistema conectado"*):** https://tabski.com/2025/11/14/why-food-halls-fail-the-7-most-common-operational-mistakes-and-how-to-avoid-them/
- **Virtual food hall / orden multi-concepto en una sola transacción (requiere conceptos bajo un mismo techo y coordinación de tiempos de cocción — "un poke bowl y unas costillas no toman lo mismo"; Kitchen United Mix instalado en centros comerciales Westfield):** https://thespoon.tech/the-next-big-tech-for-the-virtual-food-hall/ · https://www.forbes.com/sites/garyocchiogrosso/2019/09/03/an-innovation-in-urban-dining-a-closer-look-at-the-virtual-food-hall/
- **Comisión de Rappi y DiDi en Colombia 2026 (porcentaje más IVA sobre cada venta):** https://www.chejefe.com/blog/independencia-de-las-apps/comision-rappi-didi-colombia-2026
- **Comisiones de agregadores por país y modalidad (25-30% en Colombia):** https://www.chejefe.com/blog/independencia-de-las-apps/comisiones-rappi-cuanto-queda
- **Costo real del delivery de terceros (comisión 15-30%, costo total 35-48%):** https://www.unplugdining.com/blog/the-true-cost-of-doordash-and-uber-eats-commissions-in-2026
- **Arranque en frío de marketplaces (sembrar un lado primero; no hay atajo):** https://www.sharetribe.com/marketplace-glossary/chicken-and-egg-problem/ · https://www.growthmentor.com/blog/chicken-and-egg-problem
- **Comercio agéntico en restaurantes 2026 (valor transaccional global proyectado USD 3,5 billones — **cifra de proveedor interesado, tratar como la menos confiable**):** https://www.orderout.co/blog/agentic-commerce-restaurants/

---

## DATOS CRUDOS

`C:\Users\Admin\intel\plazoleta-20261029\`

---

*Salve, Gran Monarca. Su instinto apuntó a algo real —un solo sitio con varias cocinas— pero el sitio no puede ser el intermediario: **el intermediario es el enemigo del cliente al que le vamos a vender**. La versión que sí aguanta es la otra cara de la misma moneda: un agente con dos caras, cada restaurante dueño de su cliente, y el escaparate compartido como premio cuando ya haya vecinos.*

**— Bellion, Gran Comandante del Ejército de Sombras.**
