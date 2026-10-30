# EL CUADRE — PRECIO, LÍNEA BASE MEDIBLE Y LA PLATAFORMA SENCILLA

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Sus 4 respuestas (verbatim, resumidas):**
1. *"Estoy de acuerdo"* → unidad de cobro = **pedido cerrado por el agente**.
2. *"No estoy seguro… pienso que 500 por pedido sea bueno pero no sé qué resistencia tenga el dueño, aconséjame con datos."*
3. *"Hay que decidir 59.900 de techo, lo que más se pueda ganar."*
4. *"De acuerdo, pero hay que poner algo medible al contratar, un antes y después."*
**Además:** *"Para este proyecto no quisiera usar Seawolf Agent, más bien una plataforma sencilla que sea entrar, ver y decidir."*

---

## 0. LO PRIMERO, PORQUE ES LO MÁS IMPORTANTE QUE HE ENCONTRADO HOY

**Buscando la resistencia al $500 encontré que el agente de pedidos por WhatsApp YA ES UN PRODUCTO VENDIDO EN COLOMBIA — y a precios que cambian nuestro tablero.**

| Competidor | Qué es | Precio | Tamaño |
|---|---|---|---|
| **Zavora** (Colombia) | Agente de IA de pedidos por WhatsApp: **texto, nota de voz transcrita y foto de lista escrita a mano**; cruza catálogo e **inventario**; confirma el total; **cobra con link de pago**; **botones de despacho en el panel**; negociación de precio con aprobación del dueño; **escalado a humano desde el panel**; factura en Alegra. **Vende a restaurantes: "pedidos y domicilios por WhatsApp, atendidos solos"** | **desde $350.000/mes + IVA** (14 días gratis, sin tarjeta) · **0% de comisión de Zavora** (el cliente paga la tarifa de MercadoPago) | — |
| **OlaClick** | Chatbot + menú digital + POS + delivery. **Plan GRATIS, sin mensualidad, sin comisiones sobre pedidos** | **$0** | "+40.000 restaurantes" · **1,3 millones de pedidos/mes** · ~50.000 restaurantes activos · respaldo de **Google y Meta** |

> **Esto es honestidad brutal y es lo que le debo: en el eje "agente que toma el pedido por WhatsApp" NO somos pioneros, estamos llegando tarde, y hay un competidor con 40-50 mil restaurantes que lo regala.**
>
> **Y sin embargo — el Radar ya había acertado sin saberlo:** el hueco nunca fue el POS ni el bot de pedidos. **El hueco es EL CUADRE.** Zavora le dice al dueño *qué se pidió*. OlaClick le dice *qué se vendió*. **Ninguno de los dos le dice al dueño cuánta plata le quedó de verdad, ni dónde se le está fugando.** Eso sigue sin tener dueño.
>
> **Consecuencia dura para el taller: NO se construye "otro bot de pedidos". El agente que toma el pedido es el vehículo, no el producto. El producto es el cuadre.**

**Y un dato de Zavora que nos sirve como vara de medir:** en su propia medición con conversaciones reales (agosto 2026), **un agente de IA cerró el 16,3% de las conversaciones en venta contra 11,6% de un bot de reglas sobre el mismo catálogo** — o sea, **el agente de IA vende ~40% más que el menú de "escribe 1 para…"**. Ese es el salto que hay que demostrar en la línea base.

---

## 1. LA RESISTENCIA AL $500 — ACONSEJADO CON DATOS

Se compara todo **por pedido de $25.000** (ticket de referencia), que es la unidad en la que piensa el dueño:

| Ancla real del mercado | Costo por ese pedido | vs nuestro fee |
|---|---|---|
| **Comisión de apps de delivery (Colombia)** | **$5.000 – $7.000** | **10 – 14× más caro** |
| **Domiciliario propio** (mensajero $50-70 mil/día ÷ 10-15 pedidos) | **$3.000 – $5.000** | 6 – 10× |
| **Pasarela de pago** (Wompi 2,65-2,69% + IVA · MercadoPago 3,49% + IVA) | **$672 – $1.620** | **1,3 – 3,2× más caro que nosotros** |
| **Bot de IA de pedidos local** (Zavora $350.000/mes ÷ 50 pedidos) | **~$7.000** | **14×** |
| **OlaClick** | **$0** | ← **aquí está la resistencia real** |
| **Nuestro fee** | **$500** | — |

### El veredicto sobre el $500

1. **En dinero, el $500 no genera resistencia: está por debajo de casi todo lo que el restaurante ya paga.** Es **menos de lo que la pasarela de pago le cobra por la misma venta** (Wompi 2,65% + $700 + IVA ≈ $1.360 en un pedido de $25.000). Pagar $500 por que alguien atienda y cierre el pedido **cuesta menos que el recibo bancario de cobrarlo**.
2. **Es el 3% de lo que ese pedido deja** (contribución ≈ $16.750 = ticket − food cost 33%). **Tres centavos de cada peso de ganancia del pedido.**
3. **Y es 10 a 14 veces más barato que la comisión que ya paga.** El mismo pedido, en Rappi, le deja $5.000–$7.000 menos.
4. **La resistencia NO es el monto. La resistencia es la EXISTENCIA del cobro:** *"¿por qué te pago si OlaClick me lo da gratis?"*. **Ese es el enemigo, no el precio.**

### Cómo se mata esa resistencia (3 instrumentos, ninguno es bajar el precio)

| Instrumento | Por qué funciona |
|---|---|
| **Los primeros 50 pedidos gratis** | El dueño ve **50 facturas en $0** antes de pagar un peso. Aprende la mecánica con el riesgo en cero, y cuando llegue la primera factura ya sabe exactamente qué está pagando. (Zavora usa el mismo truco: "50 pedidos pagados" incluidos en su plan) |
| **La línea base firmada** (punto 3) | Convierte la discusión de *"¿cuánto vale?"* a *"¿cuántos pedidos se te estaban perdiendo?"*. Contra un número medido, no hay regateo |
| **La regla: si un humano tomó el pedido, no se cobra nada** | Convierte el cobro en algo que **él controla**. Si no confía, atiende él y no paga |

### ¿Y si quiere cobrar más? El consejo con datos

**El lever NO es subir el fee unitario; es el TECHO.** Un fee de $500 es un argumento cerrado (está debajo de la pasarela). El techo es donde está el dinero:

| Escenario | Pedidos cerrados/mes | Con techo $59.900 | Si el techo escala |
|---|---|---|---|
| Restaurante pequeño | 40 | $20.000 (paga lo que usa) | $20.000 |
| Mediano | 120 | $59.900 (**tope alcanzado**) | $59.900 |
| Grande | 300 | $59.900 → **el fee real cae a $200/pedido** | **$149.900** (fee real $500/pedido) |

> **Recomendación:** el techo arranca en **$59.900** (su decisión) y **escala por tramos de volumen** para que el fee se mantenga cerca de $500 por pedido. Así el pequeño paga poco y el que cierra 300 no nos sale a mitad de precio. **Eso es "lo que más se pueda ganar" sin tocar la promesa del fee unitario.**

---

## 2. LA PLATAFORMA SENCILLA — NO SEAWOLF AGENT

**Su instrucción:** *"una plataforma sencilla que sea entrar, ver y decidir."*
**Es la instrucción correcta, y hay que aplicarla como prohibición, no como deseo.**

**Seawolf Agent NO se usa en este proyecto.** Por qué (y no es desprecio, es diseño):
- Seawolf Agent es **corporativo, multi-tenant, con RBAC, audit visible, onboarding de un clic e interfaz en español para el Cliente Súper Ocupado**. Es un producto serio para un comprador empresarial.
- **El dueño de un restaurante manual no compra un sistema: quiere entrar, ver tres números y decidir.** Todo lo demás lo ahuyenta.
- **De Seawolf Agent rescatamos los PATRONES, nunca el código ni la pantalla:** aislamiento por inquilino, sesión de WhatsApp aislada, **audit SHA-256** (que es lo que hace auditable la factura) y español nativo.

### La plataforma: **LA TRASTIENDA**

*(nombre propuesto — es literalmente lo que usted decidió: operar desde las sombras. La trastienda es el cuarto de atrás del negocio: el público ve el frente, el dueño ve todo desde atrás.)*

**Tres pantallas. Eso es todo.**

| Pantalla | Qué muestra | Qué se decide ahí |
|---|---|---|
| **1 · HOY** | Vendiste · Gastaste · **Te queda de verdad** · **Pedidos que se te perdieron** | Nada: es para **ver** (el cuadre de El Cuadre) |
| **2 · PEDIDOS** | Los pedidos que el agente cerró, con hora y monto | **Una acción por fila** — aceptar · responder · marcar que se cayó (**y si lo atiende él, se marca aquí: ese no se cobra**) |
| **3 · MENÚ** | Los platos y precios que el agente puede vender | Corregir un precio · apagar un plato que se acabó |

**Reglas de diseño duras (para que sea "entrar, ver y decidir" de verdad):**
1. **Entrar = un enlace.** Sin instalación, sin usuario y contraseña, sin capacitación. Entra desde el celular.
2. **Cada pantalla cabe en un teléfono, sin hacer scroll para lo importante.**
3. **Ningún menú lateral, ninguna configuración por defecto, ningún reporte.** Si algo no cambia una decisión, no va.
4. **El antes y el después vive en la pantalla 1** (punto 3): el dueño ve su línea base contra su presente, todos los días, sin pedirlo.
5. **Todo lo demás es invisible** — la plazoleta interna (nuestro panel de operador, para nosotros), la infraestructura, los otros restaurantes. **Eso nunca lo ve el cliente, y así debe quedarse.**

---

## 3. LO MEDIBLE AL CONTRATAR: LA LÍNEA BASE CON ACTA

Su objeción es la correcta y es la que yo mismo levanté: **sin línea base no hay antes/después**. La solución no es pedirle sus libros — es **medirla nosotros, en su propio WhatsApp, con la misma vara que después**. Y que quede firmada.

### Semana 0 — el diagnóstico (gratis, 7 días, modo observador)

El agente entra al WhatsApp del restaurante **solo a contar, sin responder** (o respondiendo con aviso al dueño). Se miden **6 números**:

| # | Métrica | Definición exacta (la que va al contrato) |
|---|---|---|
| 1 | **Mensajes entrantes** | Todos los que llegan al WhatsApp del negocio |
| 2 | **Mensajes con intención de compra** | Los que piden algo, con o sin precio, con o sin dirección |
| 3 | **Pedidos cerrados** | El pedido terminó confirmado con monto y forma de pago |
| 4 | **Pedidos PERDIDOS** | Intención de compra **sin respuesta en 10 minutos**, o sin confirmación al final del día ← **el número que justifica todo** |
| 5 | **Tiempo hasta la primera respuesta** | Mediana (no promedio: el promedio esconde los abandonos) |
| 6 | **Ticket promedio** | Monto total de pedidos cerrados ÷ pedidos cerrados |

### El Acta de Línea Base (se firma al final de la semana 0)

Un documento de **una página** que fija:
1. **Los 6 números del "antes"**, medidos y con fecha.
2. **La definición de "pedido cerrado"** (lo que se cobra) y **de "pedido perdido"** (lo que se persigue).
3. **Las exclusiones de facturación:** duplicados, pruebas internas, pedidos de cortesía, pedidos que cierra el dueño sin pasar por el agente.
4. **Si un humano tomó el pedido, no se cobra.**
5. **El fee, el techo, la cadencia de facturación y cómo se audita cada pedido** (hora, chat, monto, sello).

> **Por qué esto es lo que hace que el negocio funcione:** el "antes y después" **no sale de la contabilidad del dueño** (que no cuadra — es el hallazgo de las 11.389 reseñas); **sale de la misma medición nuestra, dos veces**. Es el mismo instrumento antes y después → comparable, verificable, indiscutible. **Y esa acta es, textualmente, lo que la industria llama "codificar el resultado en contrato: el contrato ES el sistema".**

### El "después" no se promete: se ve
Los mismos 6 números viven en la **pantalla 1 de La Trastienda**, lado a lado con la línea base. **El dueño nunca tiene que pedir un reporte para saber si le estamos sirviendo — lo tiene abierto en el celular.** Y si los pedidos perdidos no bajan, él mismo lo va a ver antes que nosotros.

### La garantía del punto 4 (acordada)
**30 días gratis** (el Revenue Test) → y luego: **"si en 90 días tu venta no subió, no pagas"**. Es una promesa con fecha, no un medidor.

---

## 4. LO QUE QUEDA DECIDIDO

| Punto | Decisión |
|---|---|
| **Unidad de cobro** | ✅ **El pedido que el agente cerró y cobró** (con exclusiones y regla "si un humano lo tomó, no se cobra") |
| **Fee unitario** | **$500 por pedido** — y su defensa con datos: debajo de lo que ya paga a la pasarela por cobrar ese mismo pedido, 10-14× debajo de la comisión de apps, y 3% de lo que el pedido deja |
| **Techo** | ✅ **$59.900/mes**, **escalable por tramos de volumen** para no regalar el margen del que cierra 300 pedidos |
| **Entrada** | **50 primeros pedidos gratis** (mata la objeción sin bajar el precio) |
| **Garantía** | ✅ **"Si en 90 días no te subió la venta, no pagas"** |
| **Antes/después** | ✅ **Semana 0 de diagnóstico + Acta de Línea Base firmada** con los 6 números |
| **Plataforma** | **LA TRASTIENDA** — 3 pantallas (Hoy · Pedidos · Menú), **sin Seawolf Agent**, rescatando solo sus patrones (aislamiento, audit SHA-256, español) |
| **Lo que NO se construye** | **Otro bot de pedidos.** El agente es el vehículo; el producto es **el cuadre** |

---

## 5. RIESGOS (incluidos los nuevos, que son los serios)

| Riesgo | Severidad | Nota |
|---|---|---|
| **OlaClick: mismo producto, GRATIS, 40-50 mil restaurantes y respaldo de Google/Meta** | **MUY ALTA** | Es el riesgo #1 del proyecto. **Contra "gratis" no se compite con precio: se compite con el cuadre y con el cobro por resultado** (OlaClick no cobra por pedido porque no asume el resultado) |
| **Zavora: agente de IA de pedidos a $350.000/mes, con audio, foto, inventario y negociación** | **ALTA** | Ya cubre el vehículo entero. **Nuestro terreno es el dinero, no el pedido** |
| Que el taller derive a construir un bot de pedidos | **ALTA** | Es la trampa natural de este proyecto. **Prohibido: el producto es el cuadre** |
| Disputa de factura | ALTA | El Acta + el sello por pedido son la defensa |
| Márgenes del cliente (~5%) | ALTA | El precio se comunica **en pedidos**, nunca en porcentaje |
| Políticas de Meta (WAHA no oficial) | ALTA | Costo cerrado y el más bajo de LatAm; las **políticas** siguen siendo el riesgo abierto |
| Que el restaurante use OlaClick para pedir y a nosotros solo para el cuadre | MEDIA | Legítimo: **si el cuadre vale, se paga solo.** Y nuestro agente sigue siendo el que cierra |

---

## 6. EL PASO SIGUIENTE

**El DEMO en un solo archivo HTML sigue siendo el primer entregable del taller** — y con esto ya tiene forma exacta:

```
CARA DEL DUEÑO (lo que ve el restaurante)
   HOY      → el cuadre + los pedidos perdidos contra la línea base
   PEDIDOS  → aceptar / responder / marcar que se cayó
   MENÚ     → precios y platos disponibles

CARA DE LA SOMBRA (lo que vemos solo nosotros)
   la plazoleta interna: varios restaurantes, salud de cada sesión, pedidos cerrados
```

**Un solo archivo. Tres pantallas. Entrar, ver y decidir.**

Mientras: **LOS SIMPSON** en paralelo (cerrar MiPony primero).

---

## FUENTES

- **Competidor directo — agente IA de pedidos por WhatsApp (precios desde $350.000/mes + IVA, 0% comisión, texto/audio/foto, inventario, negociación, escalado, panel; medición propia: agente IA cierra 16,3% vs 11,6% de bot de reglas):** https://zavorai.com/guias/bot-para-tomar-pedidos-por-whatsapp · https://zavorai.com/ia-para/restaurantes
- **Competidor directo — gratis (chatbot + menú digital + POS; +40.000 restaurantes, 1,3 M pedidos/mes, respaldo Google y Meta):** https://olaclick.com/es/chatbot-whatsapp/
- **Comisiones de pasarelas en Colombia (Wompi 2,69% + IVA tarjeta; 2,65% + $700 + IVA tarifa estándar · MercadoPago 3,49% + IVA · Bold 2,99% + $900 + IVA; mix de métodos: PSE 45%, Nequi/Daviplata 25%, tarjetas 22%):** https://soft-ia.cloud/blog/pasarela-pagos-whatsapp-wompi-mercadopago/ · https://doneapi.com/blog/pasarelas-pago-colombia-pse-wompi-mercado-pago-comparativa/
- **Comisión de apps Colombia (Rappi 27-32%, real todo incluido 30-40%; "de esos $25.000 la app se quedó con $5.000 o $7.000"):** https://poscolombia.com/herramientas/simulador-comisiones-delivery · https://sistepos.com/rappi-vs-domiciliario-propio-que-es-mas-rentable-para-tu-restaurante-en-2026/
- **Comisión de Rappi en Colombia: 15% a 35% según negociación (gremio Acodres):** https://www.chejefe.com/blog/independencia-de-las-apps/comisiones-rappi-cuanto-queda
- **Márgenes del restaurante (ganancia antes de impuestos ~5%) y fórmula de ganancia mensual:** https://www.chejefe.com/blog/finanzas/cuanto-gana-un-restaurante
- **Cobro por resultado: definir, excluir, medir, atribuir, precio unitario, guardarraíles, codificar en contrato ("el contrato es el sistema"); precedente Intercom USD 0,99 por ticket resuelto:** https://www.thesaascfo.com/how-to-build-outcome-based-pricing/ · https://www.solvimon.com/glossary/outcome-based-pricing
- **Disposición a pagar del restaurante atada a visibilidad/clientes nuevos (comisiones altas aceptadas a cambio de exhibición destacada; encuesta de la National Restaurant Association, 830 respuestas, mayo 2026):** https://pubsonline.informs.org/doi/10.1287/mnsc.2023.00435 · https://restaurant.org/getmedia/f925bcf1-9195-401d-9a1f-341e0e1e5b31/National-Restaurant-Association-Comments-FTC-Onli
- **Ofertas locales de página/bot para restaurantes (landing + menú + botón WhatsApp: $1.260.000–$3.360.000 COP; desarrollo a medida desde US$300/mes):** https://edwsystem.com/blog/pagina-web-y-sistema-para-restaurantes-pedidos-whatsapp

---

## DATOS CRUDOS

`C:\Users\Admin\intel\precio-linea-base-20261029\`

---

*Salve, Gran Monarca. Le traigo una advertencia y una confirmación. La advertencia: **el bot de pedidos ya está hecho y regalado — si el taller se va por ahí, perdemos.** La confirmación: **lo que el Radar vio desde el principio sigue intacto y sin dueño — nadie le está diciendo al dueño cuánta plata le queda.** Cobrar $500 por pedido no va a generar resistencia: cobrar *cualquier cosa* sí, y se vence mostrándole los pedidos que hoy se le pierden.*

**— Bellion, Gran Comandante del Ejército de Sombras.**
