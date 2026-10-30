# DATOS CRUDOS — Precio, línea base y plataforma (29-oct-2026)

## Consultas ejecutadas (5)

1. `cuanto se queda Rappi por pedido pesos comision 25000 Colombia ticket`
2. `pasarela de pagos Colombia comision porcentaje Wompi Bold MercadoPago 2026`
3. `chatbot pedidos WhatsApp restaurante precio mensual Colombia costo`
4. `cuanto esta dispuesto a pagar un restaurante por tecnologia porcentaje de ventas encuesta`
5. `restaurant willingness to pay per order technology fee delivery commission absolute`

## Documentos extraídos

| URL | Qué se extrajo |
|---|---|
| **https://zavorai.com/guias/bot-para-tomar-pedidos-por-whatsapp** | **COMPETIDOR DIRECTO COLOMBIANO.** Agente de IA de pedidos por WhatsApp: entiende **texto, nota de voz transcrita y foto de lista escrita a mano**; cruza catálogo (referencias, presentaciones, precios) e **inventario** ("si quedan 3, no vende 10"); confirma el pedido con total; **cobra con link de pago de MercadoPago — 0% de comisión de Zavora, el cliente paga la tarifa de MercadoPago**; **tres botones de despacho en el panel** (alistando, en camino, entregado) con aviso al cliente; **negociación** (el cliente propone precio, el dueño aprueba o contraoferta con un clic); **escalado a humano desde el panel** (el bot se calla y responde el equipo por el mismo número); facturación en Alegra (otra guía). **Planes desde $350.000/mes + IVA**, mensajes incluidos, **14 días gratis sin tarjeta**. **MEDICIÓN PROPIA (conversaciones reales, agosto 2026): el agente de IA cerró 16,3% de las conversaciones en venta vs 11,6% de un bot de reglas sobre el mismo catálogo.** Tiene vertical de restaurantes: *"IA para restaurantes: pedidos y domicilios por WhatsApp, atendidos solos"* (Colombia) |
| **https://olaclick.com/es/chatbot-whatsapp/** | **COMPETIDOR GRATIS.** Chatbot WhatsApp + menú digital + POS + delivery propio. **"Gratis, sin mensualidades"** y **"sin comisiones sobre pedidos"**. **+40.000 restaurantes** (la página dice también ~50.000 activos), **1,3 millones de órdenes mensuales**, respaldo declarado de **Google y Meta**. Configuración en 10 minutos sin técnico; conecta WhatsApp Business por QR. Notificaciones automáticas (pedido recibido/aceptado/en preparación), links de pago, ratings, reactivación de clientes. Cifras de marketing propias: "5x más rápido", "hasta 40% de incremento de pedidos", "99% tasa de respuesta" |
| **https://soft-ia.cloud/blog/pasarela-pagos-whatsapp-wompi-mercadopago/** | Pasarelas Colombia 2026: **Wompi 2,69% + IVA** (tarjeta crédito/débito), Nequi nativo; **MercadoPago 3,49% + IVA**, Daviplata. Ambas $0 de costo mensual, webhooks en tiempo real. **78% de compradores prefieren pagar sin salir del chat**; **38 millones de colombianos activos en WhatsApp**; **48 horas promedio para confirmar un pago manual**. Cada paso extra en el checkout reduce el cierre hasta 22% |
| **https://doneapi.com/blog/pasarelas-pago-colombia-pse-wompi-mercado-pago-comparativa/** | **Wompi: 2,65% + $700 COP + IVA** (tarifa estándar) · **MercadoPago 3,29% + $800 + IVA** (inmediata) / 2,99% + $800 (14 días) · **Bold 2,99% + $900 + IVA** tarjetas / $900 fijos PSE. Mix de métodos de pago en Colombia: **PSE ~45% · Nequi/Daviplata ~25% · tarjetas ~22% · efectivo/recaudo ~8%**. Webhooks con checksum SHA-256 (Wompi) y HMAC-SHA256 (MercadoPago) |
| **https://www.chejefe.com/blog/independencia-de-las-apps/comisiones-rappi-cuanto-queda** | Comisión de Rappi en Colombia: **15% a 35% según negociación** (dato del gremio **Acodres**, 2023, vía La República) |
| **https://sistepos.com/rappi-vs-domiciliario-propio-...** | *"De esos $25.000, la app se quedó con $5.000 o $7.000"* (comisión + publicidad + servicio). Mensajero propio: **$50.000–$70.000/día**; el domiciliario propio se justifica **desde 10-15 pedidos diarios** |
| **https://restaurant.org/.../National-Restaurant-Association-Comments-FTC-Onli...** | Encuesta de delivery de la National Restaurant Association, **830 respuestas, 14-may-2026**: distribución por tramos de comisión (10-14,9%: 11% de los restaurantes · 25-29,9%: 17%…) |
| **https://pubsonline.informs.org/doi/10.1287/mnsc.2023.00435** | *"Como estos restaurantes no internalizan los costos de entrega de la plataforma, están dispuestos a elegir comisiones agresivamente altas para ganar exhibición destacada"* → **la disposición a pagar está atada a visibilidad/clientes NUEVOS, no a herramientas** |
| **https://edwsystem.com/blog/pagina-web-y-sistema-para-restaurantes-pedidos-whatsapp** | Landing con menú y botón de WhatsApp: **$1.260.000 a $3.360.000 COP**, en 1-2 semanas |
| Otras fuentes de precio local del mercado | Guía en Instagram: bot de WhatsApp **desde US$300/mes** (desarrollo a medida) = ~$950.000 COP/mes · **OlaClick**: gratis · **Zavora**: $350.000/mes + IVA |
| https://www.katalystos.com/es-us/restaurant-analytics-guide | Costo primo (food + labor) 55-65% en servicio completo — consistente con el reparto de márgenes usado |

## Cifras de control usadas

- Ticket de referencia: **$25.000** · contribución de un pedido = ticket − food cost 33% ≈ **$16.750**
- Anclas por pedido: comisión apps **$5.000-7.000** · domiciliario propio **$3.000-5.000** · pasarela **$672-1.620** · bot IA local (Zavora ÷ 50 pedidos) **~$7.000** · **OlaClick $0** · **nuestro fee $500**
- Fee propuesto: **$500/pedido**, techo **$59.900/mes** (escalable por tramos), **50 primeros pedidos gratis**, piso $0
- Línea base: **6 métricas** (entrantes · con intención de compra · cerrados · **PERDIDOS** · tiempo a la 1ª respuesta · ticket promedio) medidas en **semana 0 (7 días, modo observador)** y firmadas en **Acta de Línea Base**
- Plataforma: **LA TRASTIENDA** — 3 pantallas (**Hoy · Pedidos · Menú**), **sin Seawolf Agent**, rescatando solo patrones (aislamiento por inquilino, audit SHA-256, español)
