# EL CUADRE — COMO PLATAFORMA QUE ALBERGA VARIOS CLIENTES

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Encargo (verbatim):** *"se me ocurrió algo, he visto muchos programas que funcionan muy bien albergando varios clientes, quiero explorar ese enfoque a ver si damos con algo bueno."*
**Antecedente:** `RADAR-restaurantes-manuales.md` (score 36/40) · vertical = restaurantes que hacen todo a mano y solo usan WhatsApp.

---

## 0. VEREDICTO EN TRES LÍNEAS

**Sí se puede, y es el enfoque correcto — pero cambia la unidad del negocio.**
No vendemos *una app por restaurante*: vendemos **un lugar dentro de una plataforma**.
La arquitectura probada para 50–500 clientes es **base de datos compartida con `tenant_id` + Row Level Security**, con **una sesión de WhatsApp aislada por restaurante** (una sesión = un número). El costo marginal por cliente queda en **US$1–3 de infraestructura + US$0,0008 por respuesta en Colombia**.

**Y aparece un dato que el Radar no tenía: en Colombia el canal de WhatsApp de Meta es el más barato de Latinoamérica.** Eso baja el riesgo #2 del Radar de *ALTA* a *manejable*.

---

## 1. QUÉ SIGNIFICA "ALBERGAR VARIOS CLIENTES" — LOS TRES MODELOS, CON NÚMEROS

Existen exactamente tres formas de alojar clientes en un mismo producto. Se eligen por tres criterios: aislamiento que exige el cliente, cuántos clientes se buscan, y capacidad del equipo para operar infraestructura.

| Criterio | **Base compartida (tenant_id + RLS)** | Esquema por inquilino | Base de datos por inquilino |
|---|---|---|---|
| Aislamiento de datos | Lógico, forzado por políticas RLS | Lógico más fuerte | Físico |
| Sobrecosto de desarrollo | **+15 a 20%** | +20 a 25% | +25 a 30% |
| **Costo de hosting por cliente** | **EUR 1–3/mes** | EUR 3–8/mes | EUR 15–60/mes |
| Migraciones de esquema | Una sola | Una por inquilino | Una por base |
| Clientes cómodos | Miles | 50–1.000 | 10–200 |
| Restaurar un cliente solo | Complejo | Posible | Simple |
| Caso típico | SaaS pyme / herramienta B2B amplia | Mid-market con personalizaciones | Salud, banca, enterprise exigente |

**Presupuesto de hosting según número de clientes** (SaaS de gestión estándar: web + API + PostgreSQL + almacenamiento, con respaldos):

| Clientes activos | Infraestructura típica | Costo mensual 2026 | % de un ARPU de EUR 80 |
|---|---|---|---|
| 50 | 2 instancias + PostgreSQL gestionado 4 GB | EUR 150–300 | 3,8–7,5% |
| 100 | 2–3 instancias + PostgreSQL 8 GB con réplica | EUR 250–500 | 3,1–6,3% |
| 250 | balanceador + 3–4 instancias + BD 16 GB + CDN | EUR 500–900 | 2,5–4,5% |
| 500 | Kubernetes gestionado + BD HA 32 GB | EUR 900–1.500 | 2,3–3,8% |
| **Base por inquilino, 100 clientes** | 100 bases gestionadas pequeñas | **EUR 1.500–6.000** | **19–75%** |

> **La última fila es la que mata el margen:** con base de datos por cliente, la infraestructura se come hasta **tres cuartas partes del ingreso**. La base compartida deja el hosting en **2,3–7,5% del ARPU**.

**Decisión recomendada: base compartida + `tenant_id` + RLS, con base dedicada vendida como opción Enterprise si algún cliente grande la pide** (EUR 300–800 extra/mes). El modelo híbrido solo funciona si el código se diseñó para eso desde el principio.

**Consecuencia de ingeniería que no se puede saltar:** en base compartida la garantía de que un cliente no ve al otro se apoya en **tres capas** — filtro en la aplicación, políticas RLS de PostgreSQL, y **pruebas automáticas que intentan acceso cruzado en cada despliegue**. Ese paquete (exportación por cliente, borrado al terminar, registro de tratamiento) son **5 a 10 días de desarrollo** que casi nadie cotiza.

---

## 2. LA PIEZA QUE **NO** SE COMPARTE: EL WHATSAPP

Aquí está el corazón del asunto, y donde el multi-inquilino se vuelve difícil de verdad.

**Cada restaurante tiene SU número de WhatsApp. Un número = una sesión. Una sesión, jamás compartida entre inquilinos.** Si el número de un restaurante se cae o lo banean, eso **no puede llegarle** al de al lado.

### Cómo se aísla de verdad (no basta un `tenant_id`)

| Buena práctica | Por qué |
|---|---|
| **Un contenedor por sesión** (no por inquilino) | Un inquilino puede tener varias sesiones (ventas, soporte, sedes). Aislar en la frontera de sesión/contenedor hace que la caída de una sesión tenga un radio de daño de exactamente una sesión |
| **Motor ligero, no navegador** | Baileys ≈ **50 MB por sesión**; el modelo con navegador (Puppeteer/WEBJS) cuesta ≈ **10× más RAM por número**. Es lo que vuelve económicamente realista alojar muchos clientes |
| **Escala por servidor** | WAHA: **hasta ~500 sesiones en un servidor con motor NOWEB**; ~50 con motor WEBJS. Nuestro VPS **ya corre WAHA** |
| **Credenciales por inquilino** | Nunca una llave maestra compartida. Una llave por cuenta |
| **Logs y colas por sesión** | Un ticket de soporte sobre un cliente no debe obligar a mirar datos de otro |

### El modelo de datos limpio

```
Tenant 1──* Session 1──* Message
Tenant 1──* WebhookConfig
```

**Toda** fila con alcance de sesión lleva **dos** identificadores: `session_id` (para aislamiento: colas, límites de ritmo, contenedores) y `tenant_id` (para facturación y propiedad). **Una petición que trae un `session_id` SIEMPRE se valida contra el inquilino autenticado antes de ejecutar nada.** Saltarse esa validación es *la* forma más común de terminar filtrando los datos de un cliente a otro.

### Onboarding sin que nosotros toquemos un teléfono

1. Crear la sesión con la llave del inquilino → devuelve un ID antes de que el número esté vinculado.
2. Mostrar el **QR** en la interfaz — el QR **expira y se refresca solo**: la interfaz debe autorefrescarlo, nunca mostrar uno vencido.
3. Esperar/vigilar el estado hasta `connected` y **entonces** encender la función.
4. Manejar la reconexión y la salida: al dar de baja a un inquilino se **borra la sesión por la API** (liberar contenedor y cupo), no basta con desactivar una fila propia.

**Honestidad que debe ir en el contrato y en la interfaz:** una sesión de WhatsApp que se desloguea a veces exige **escanear el QR otra vez**. Prometer reconexión instantánea garantizada = un ticket de soporte que parece una caída de servicio.

---

## 3. LO QUE CUESTA DE VERDAD EL CANAL — EL DATO QUE FALTABA

El Radar marcó como riesgo #2 *"los costos y políticas de Meta"*. Ya hay tarifa oficial y publicada, **en vigor desde el 1 de octubre de 2026, y ahora por mensaje** (ya no por conversación; las respuestas de servicio empezaron a cobrarse).

| País del cliente | Servicio (respuesta libre) | Plantilla de utilidad | Plantilla de marketing |
|---|---|---|---|
| **Colombia** | **USD 0,0008** | USD 0,0008 | USD 0,0125 |
| Brasil | 0,0068 | 0,0068 | 0,0625 |
| México | 0,0085 | 0,0085 | 0,0397 |
| Resto de LatAm (15 mercados) | 0,0113 | 0,0113 | 0,0740 |
| Chile | 0,0200 | 0,0200 | 0,0889 |
| Argentina | 0,0260 | 0,0260 | 0,0618 |
| Perú | 0,0300 | 0,0300 | 0,0703 |
| **Lo que su cliente le escribe a usted** | **Gratis** | | |

**Cuatro reglas que cambian la factura:**
- **Las primeras 1.000 respuestas de servicio de cada mes son gratis**, por número de negocio. No se acumulan y no aplican a plantillas.
- **El país del cliente fija el precio**: si el restaurante está en Colombia, aplica la tarifa de Colombia.
- Las respuestas con texto libre dentro de la ventana de 24 h se cobran a tarifa de servicio; una **plantilla** dentro de la ventana se cobra desde la primera.
- **Que el cliente escriba primero**: un mensaje de marketing que usted inicia cuesta hasta **15× más** por mensaje según el país.

**El mismo trabajo (9.000 respuestas de servicio al mes, con las 1.000 gratis):**

| País | Costo mensual |
|---|---|
| **Colombia** | **USD 6,40** |
| México | USD 68,00 |
| Resto de LatAm | USD 90,40 |
| Perú | USD 240,00 |

> **El mismo volumen cuesta 37,5 veces más en Perú que en Colombia.**
> **Conclusión: en Colombia el canal es el más barato de Latinoamérica — prácticamente gratis.** El riesgo real no es el costo: es la **política** (y contra eso, lo que protege es el aislamiento por sesión).

---

## 4. UNIT ECONOMICS DE LA PLATAFORMA

Con el precio propuesto en el Radar y la TRM de referencia (USD 1 = **3.164 COP**):

| Concepto | Valor |
|---|---|
| Precio El Cuadre | **$29.900 COP/mes = US$9,45** |
| Infraestructura por cliente | **US$1–3/mes** |
| WhatsApp por cliente (hasta ~9.000 respuestas) | **US$0,0064–0,64/mes** |
| **Costo marginal total por cliente** | **< US$3,5/mes** |
| **Margen bruto** | **> 60%**, incluso alimentando 3 sesiones |

**Y aquí el hallazgo incómodo.** Las plataformas multi-inquilino de restaurantes ya se venden así en el mundo — con bandas de precio explícitas por mercado. Para **Colombia (banda C)** la referencia de venta al público es:

| Banda | Por local/mes | Mercados |
|---|---|---|
| A · Alto ingreso | US$129 → US$89 por volumen | EE.UU., Canadá, UE-15, Australia, Japón |
| B · Europa media y Cono Sur | US$71 → US$49 | Polonia, Portugal, Grecia, Chile, Uruguay |
| **C · Emergentes grandes** | **US$45 → US$31** | India, Brasil, México, **Colombia**, Argentina, Perú |
| D · ARPU bajo | US$32 → US$22 | Filipinas, Indonesia, Vietnam, Egipto, Kenia |

> **US$45 por local/mes ≈ $142.000 COP. Nuestro $29.900 es 1/5 del piso de la banda.**
> O es una **cuña deliberada** para entrar (defendible: ganar datos y volumen primero), o **estamos dejando plata sobre la mesa** con el mismo trabajo. Esta decisión no la tomo yo: es suya, y conviene tomarla **antes** de que el primer cliente vea un precio.

---

## 5. LA ARQUITECTURA CONCRETA DE EL CUADRE COMO PLATAFORMA

**Dos caras, un solo despliegue:**

| Cara | Quién entra | Qué ve |
|---|---|---|
| **Panel del operador** | Nosotros | Todos los inquilinos: salud de cada sesión de WhatsApp, uso por mes, cupos, quién está por cortarse, alta/baja de clientes |
| **Panel del dueño** | El restaurante | SU día: ventas, gastos, compras, **la utilidad real**, y dónde se le fue la plata |
| **El mensaje nocturno** | El dueño, por WhatsApp | *"Hoy vendiste $X. Gastaste $Y. Te quedan $Z de verdad. Aquí se te fue plata: [3 puntos]"* |

**Todo lo demás ya está construido** y es lo que hace que este enfoque nos favorezca:

| Activo | Estado | Por qué es decisivo aquí |
|---|---|---|
| **WAHA + Seawolf Agent** | **En producción** (VPS `76.13.109.237`, sesión `seawolf` WORKING) | Ya corremos WhatsApp multi-sesión de verdad. Ningún competidor del radar lo tiene listo |
| Multi-tenant por chat + **Audit SHA-256** + **RBAC** | Construido | Cada restaurante es un inquilino con rastro auditable: es la respuesta al requisito de aislamiento |
| El filtro de ruido (CSO) | Construido | **Un dueño de restaurante ES el Cliente Súper Ocupado** |
| Español nativo · un clic | Construido | El informal no compra software en inglés ni con instalación |
| Cerradura + dominio propio | `herramientas.sw-st.net` | Canal de demo y venta ya listo |

---

## 6. CÓMO SE VENDE EL ENFOQUE DE "ALBERGAR VARIOS CLIENTES"

Usted intuyó un modelo que tiene nombre y precedente: **programa de socios con marca blanca** (*white-label*).

**La división es nítida y está probada:** el socio es dueño de **la marca que ve el restaurante, el precio que cobra, la factura, y la relación con el cliente**; el dueño de la plataforma es dueño del **producto, la infraestructura, el aislamiento por inquilino y el soporte de tercer nivel** — y **queda invisible**. Existe un socio que ya corre **100+ apps de restaurante de su propia marca** sobre una sola plataforma.

**Dos formas de cobrar (y se pueden combinar):**
1. **Directo:** nosotros cobramos al restaurante y listo.
2. **Por socios:** cobramos al socio **por local vivo** al mes, o un **porcentaje del precio que él cobra** — acordado contra su mercado, nunca contra una lista en dólares.

**La exclusividad se gana, no se regala** (precedente real): ≥10 locales vivos → 12 meses de exclusividad territorial; se mantiene con **+3 locales netos por trimestre y churn ≤10%**; se pierde tras un periodo de gracia de 90 días. Y la protección de prospectos por registro (**90 días, ampliable 30**) es lo que evita que el socio trabaje para que nosotros vendamos en su contra.

**Dónde está el apalancamiento en Colombia:** los gremios (Acodrés, Asobares) y las agencias/POS locales **ya venden a restaurantes**. El enfoque de albergar varios clientes convierte a cada agencia en un canal, sin contratar un solo vendedor.

---

## 7. RIESGOS HONESTOS

| Riesgo | Severidad | Qué hacer |
|---|---|---|
| **El informal paga poco** (capacidad de pago 3/5 del Radar) | **ALTA** | El multi-inquilino **baja el piso de rentabilidad** (costo marginal < US$3,5), pero **el churn sigue siendo el enemigo real** |
| **Aislamiento mal hecho = un incidente de plataforma**, no de un cliente | **ALTA** | Contenedor por sesión + RLS + **pruebas de acceso cruzado en cada despliegue** |
| **Política de Meta**: uso no oficial (WAHA) vs API oficial | **ALTA** | Decidir por cliente; el aislamiento por sesión contiene el daño de un baneo |
| **Sobrecosto de desarrollo del multi-inquilino** | MEDIA | +15–20% con base compartida. Se paga con creces: evita EUR 82.000/año de infraestructura frente a base por cliente |
| Migrar después | MEDIA | Mover un cliente grande de base compartida a dedicada: **2–4 semanas** si el código se diseñó para eso. Al revés (fusionar bases) cuesta **2–3× más** |
| **No medimos el uso por inquilino** | MEDIA | **Cupos y límites aplicados en el momento de la petición**, no medidos después |
| Canales de soporte | MEDIA | Un documento de soporte para *"sesión desconectada"*, *"cupo excedido"* y *"webhook que no dispara"* **antes** de vender, y poder apagarle la función a un inquilino **sin desplegar** |

---

## 8. LAS DECISIONES QUE LE PIDO

1. **Modelo de aislamiento:** ¿base compartida + `tenant_id` + RLS, con base dedicada vendida como opción Enterprise? *(recomendado — es el que usan 8 de cada 10 SaaS B2B de este tamaño)*
2. **Canal:** ¿vendemos directo, por socios con marca blanca, o los dos?
3. **Precio:** ¿mantenemos $29.900 como cuña de entrada, o subimos al piso de la banda colombiana (**$142.000**)? Nótese que la banda es el precio de un producto más amplio; aun así, `$29.900` es el 21% de ese piso.
4. **WhatsApp:** ¿WAHA (ya corre, costo ≈ 0, riesgo de política) o API oficial de Meta (US$0,0008/respuesta en Colombia, costos de plantilla, política limpia) **por inquilino**?

---

## 9. EL PRIMER PASO CONCRETO — COSTO CERO, ESTA SEMANA

El primer entregable del taller sigue siendo **el DEMO en un solo archivo HTML** — pero ahora mostrando **las dos caras** del enfoque que usted intuyó:

```
LADO DUEÑO   → escribe su día (ventas, gastos, compras, merma)
             → recibe EL CUADRE + el mensaje de WhatsApp con sus fugas
LADO PLATAFORMA → una tira con VARIOS restaurantes a la vez
             → la prueba visual de "albergar varios clientes" sin backend
```

**Qué prueba:** que el dueño *quiere* y *lee* el mensaje (hipótesis 1) **y** que el producto se ve como plataforma, no como app suelta (hipótesis 2). Sin backend, sin llaves, sin servidor.

**El Revenue Test sigue intacto y sigue siendo lo que decide:** 3 restaurantes, 30 días, reporte nocturno **a mano**, y al día 30 se les pide el dinero. *3 pagan → se construye la plataforma. 0 pagan → se descarta habiendo gastado US$0 en infraestructura.*

**Mientras eso corre:** usted avanza con LOS SIMPSON en paralelo (`01-LOS-SIMPSON-236GB.txt`, cerrar MiPony primero).

---

## FUENTES

- **WhatsApp Business API — tarifas oficiales LatAm (vigentes 1-oct-2026, por mensaje):** https://contactship.ai/en/blog/whatsapp-business-api-pricing-latin-america-2026
- **Precios WhatsApp Business por país (calculadora, 2026):** https://chatdaddy.tech/es/blog/whatsapp-business-api-pricing-calculator
- **Arquitectura multi-inquilino de WhatsApp para SaaS (aislamiento por sesión/contenedor, modelo de datos, onboarding por QR):** https://simplewa.com/blogs/whatsapp-api-for-saas-platforms
- **Sistema multi-inquilino escalable de WhatsApp API para SaaS (número, llave y enrutamiento por cliente):** https://rapiwa.com/blog/multi-tenant-whatsapp-api-saas-architecture
- **WAHA — escalado: 50 sesiones (WEBJS) o 500 sesiones (NOWEB) por servidor:** https://dev.to/waha/waha-scaling-how-to-handle-500-whatsapp-sessions-3fie · https://github.com/devlikeapro/waha-docs/blob/bf2cb5e1/content/blog/waha-scaling/index.md
- **Aislamiento multi-inquilino en MCP/agentes (patrones pool/bridge/silo):** https://wati.io/en/blog/mcp-multi-tenant-data-isolation
- **Arquitectura y costo de hosting multi-inquilino 2026 (3 modelos, EUR/cliente, sobrecosto 15–30%, caso 300 clientes):** https://kolonell.com/en/blog/multi-tenant-saas-architecture-hosting-cost-2026
- **Plataformas backend SaaS y VPS 2026 (patrón de claves multi-inquilino):** https://techplained.com/top-backend-platforms-saas
- **Programa de socios marca blanca de plataforma de restaurantes (bandas de precio por mercado, exclusividad ganada, división de responsabilidades, caso de 100+ apps de una sola plataforma):** https://supaorder.com/partners
- **Referencia de precios POS Colombia (piso del mercado: $46.000–$139.900 COP/mes):** https://scrampi.com/mejor-pos-restaurantes-colombia · https://menuthere.com/alternatives/toteat
- **TRM de referencia usada:** USD 1 = **3.164 COP** (open.er-api.com, consultada 29-oct-2026 20:04).

---

## DATOS CRUDOS

`C:\Users\Admin\intel\multiinquilino-20261029\` — consultas y fuentes extraídas.

---

*Salve, Gran Monarca. Su intuición tiene nombre propio en la industria (marca blanca multi-inquilino), está probada, y el costo por cliente —lo que siempre mata estos negocios— es el punto más fuerte que tiene el proyecto.*

**— Bellion, Gran Comandante del Ejército de Sombras.**
