# EL AGENTE DEL RESTAURANTE — ¿MODELO PEQUEÑO, INCLUSO GRATIS?

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Su pregunta:** *"para un restaurante promedio, ¿podemos usar un modelo pequeño incluso gratuito, cierto?"*
**Antecedentes:** `LA-TRASTIENDA-20261029.md` · `EL-CUADRE-precio-linea-base-plataforma-20261029.md`

---

## 0. VEREDICTO EN TRES LÍNEAS

**Modelo pequeño: SÍ — y para este trabajo no es un compromiso, es la decisión correcta** (el agente no razona: **extrae** un pedido de un chat y lo cruza con un catálogo conocido).
**Gratis: NO — y el motivo NO es el precio.** El motivo es que **la cuota gratuita entrena con tus conversaciones** (rompe el contrato de datos que acabamos de diseñar), tiene **un solo host sin respaldo**, y su **valor real es ~US$6 al mes**. Estaríamos cambiando legalidad y estabilidad por seis dólares.
**Y el dato que cierra la discusión: el modelo cuesta menos del 1% de lo que le cobramos al restaurante.**

---

## 1. LOS NÚMEROS (calculados, no estimados)

**Supuestos de una conversación de pedido (restaurante promedio):** catálogo + reglas en el prompt = **2.500 tokens fijos** (prefijo cacheable) · **8 turnos** · 300 tokens nuevos por turno · **60 tokens de respuesta** por turno.

| Modelo | USD / conversación | COP / conversación | **COP / pedido cerrado*** | % de la tarifa |
|---|---|---|---|---|
| **DeepSeek V4 Flash (DeepInfra)** | 0,00048 | **1,5** | **4,6** | **0,9%** |
| gpt-oss-120b (DeepInfra) | 0,00024 | 0,8 | 2,3 | 0,5% |
| Gemini 2.5 Flash-Lite | 0,00063 | 2,0 | 6,0 | 1,2% |
| Morph DeepSeek V4 Flash (1M ctx) | 0,00082 | 2,6 | 7,7 | 1,5% |
| Llama 3.1 8B (DeepInfra) | 0,00010 | 0,3 | 1,0 | 0,2% |

*\* 3 conversaciones por pedido cerrado · tarifa = **$500 COP por pedido** (TRM 3.164)*

**Escala mensual con el modelo recomendado:**

| Conversaciones/mes | Costo del modelo |
|---|---|
| 300 | **458 COP/mes** (US$0,14) |
| 1.000 | **1.526 COP/mes** (US$0,48) |
| 3.000 | **4.579 COP/mes** (US$1,45) |

**Y la verificación contra la factura real:**
- Un restaurante con **40 pedidos/mes** paga **$20.000**; el modelo nos cuesta **$183** → **0,92%**.
- Uno con **120 pedidos/mes** paga **$59.900**; el modelo nos cuesta **$549** → **0,92%**.

> **El modelo es menos del 1% de la factura en cualquier escenario. "Gratis" nos ahorra US$1,45 al mes en el caso grande.** No hay negocio ahí.

---

## 2. POR QUÉ NO EL NIVEL GRATUITO (tres razones, ninguna es el precio)

### 2.1 Los tiers gratuitos entrenan con las conversaciones — y eso rompe nuestro propio contrato
- **9 de los 19 modelos gratis de OpenRouter** corren en hosts cuya política publicada **dice que pueden entrenar con tus prompts**. Cada host tiene su política; hay que leerla, no suponerla.
- **Google AI Studio entrena fuera de la UE/Reino Unido/EEE** → **Colombia queda dentro de esa excepción**. Un tier gratis que se queda con las conversaciones de nuestros restaurantes.
- **El tier "Experiment" de Mistral también entrena.**
- Y recordemos qué es una conversación de un restaurante: **nombre, teléfono y dirección de un comensal**. Es **dato personal**. En el diseño de La Trastienda ya quedó escrito que **el restaurante es el responsable y nosotros los encargados** → mandar eso a un host que entrena **es incumplir el contrato que le vamos a firmar al cliente.**

### 2.2 Un solo host, sin respaldo, y modelos que desaparecen
Los modelos gratis de OpenRouter **corren en un único host y no tienen respaldo**, y su lista **cambia en cuestión de meses**. Un agente de WhatsApp que un día deja de responder no es un ahorro: **es la peor falla posible del producto** — el restaurante pierde pedidos justo donde le prometimos que no los perdería.

### 2.3 La cuota gratuita completa vale ~US$6 al mes
Correr el mismo modelo en un host que **no entrena ni retiene** cuesta **desde ~US$6 al mes en el techo de la propia cuota gratuita**. Y hay un límite duro: **20 peticiones por minuto y 50 peticiones por DÍA** (1.000 al día solo después de comprar US$10 en créditos).
**Un restaurante con 100 conversaciones al día × 8 turnos = 800 peticiones.** **No cabe.** El nivel gratuito no aguanta ni un restaurante promedio.

> **Esto además coincide con su propia regla vigente:** *gratis solo para el fondo y para LOBO.* Este agente es producto que se le cobra a un cliente: no es fondo.

---

## 3. LA DECISIÓN CORRECTA: SEPARAR EL MODELO DEL HOST

**El último aprendizaje técnico de este informe, y es el que más plata y más riesgo mueve: el modelo y el host son decisiones distintas, y el que decide la política de datos es el HOST, no el modelo.**

| | Modelo | Host | Retención / entrenamiento |
|---|---|---|---|
| ✅ **Recomendado** | DeepSeek V4 Flash | **DeepInfra** | **Retención cero · no entrena** |
| ✅ Alternativa más barata | gpt-oss-120b | DeepInfra | Retención cero · no entrena |
| ❌ **Mismo modelo, otro host** | DeepSeek V4 Flash | **DeepSeek (directo)** | **"Puede entrenar"** |
| ❌ **Alternativa gratis** | Gemini Flash | Google AI Studio (free tier) | **Entrena (fuera de UE/UK/EEE)** |

> **Regla para el taller: nunca se contrata por nombre de modelo — se contrata por nombre de HOST.** El mismo modelo cambia de política según quién lo sirve.
>
> **Costo del recomendado: $0,09 por millón de tokens de entrada y $0,18 por millón de salida** (DeepSeek V4 Flash en DeepInfra, 128K de contexto — sobra: nuestro prefijo son 2.500 tokens).

---

## 4. DÓNDE ESTÁ EL AHORRO DE VERDAD (y no es el modelo)

El modelo ya está en el 1% de la factura: **no hay nada que rascar ahí.** Lo que sí mueve la aguja:

1. **Caché del prefijo** (catálogo + reglas, que son iguales en cada turno): baja los tokens de entrada de **22.400 a 4.400 por conversación — un 80% menos**. Es gratis de implementar y es la única palanca grande.
2. **No reenviar el historial completo** en cada turno; sólo lo nuevo.
3. **Dos niveles:** el **90% de los turnos** (saludo, "¿tienen X?", confirmar) al modelo más barato; **escalar** sólo los difíciles (pedido ambiguo, negociación de precio, queja). Los proveedores lo venden así: *"turnos fáciles barato, turnos difíciles a un modelo superior"*.
4. **La aritmética la hace el CÓDIGO, nunca el modelo.** El modelo **elige platos**; el precio, el total, el descuento y la disponibilidad **se calculan y se validan en código**. Es regla de correctitud **y** de ahorro (un modelo que calcula gasta tokens y se equivoca).

---

## 5. EL PIPELINE COMPLETO DEL AGENTE (no todo es un LLM)

| Entrada | Con qué se resuelve | Costo |
|---|---|---|
| **Texto** | el modelo barato (DeepSeek V4 Flash @ DeepInfra) | **1,5 COP / conversación** |
| **Nota de voz** (lo más común en Colombia) | **faster-whisper LOCAL — ya está instalado** | **0 COP**, y **el audio no sale del equipo** (mejor para el contrato de datos) |
| **Foto de la lista escrita a mano** | necesita un modelo con visión (Zavora ya lo tiene) | ~US$0,0002 por foto · **pero hay que probarlo con fotos reales antes de prometerlo** |
| **Todo local** | **No.** Nuestro propio hallazgo: con **8 GB de VRAM no corre un modelo serio** → texto por API | — |

> **La nota de voz gratis y local** no es un detalle: es la entrada más usada en WhatsApp colombiano, cuesta cero, y mantenerla fuera de terceros **fortalece** el contrato de datos en vez de debilitarlo.

---

## 6. LA RUTA DE FALLO (no cuesta nada y hay que dejarla escrita)

```
1º  DeepInfra (DeepSeek V4 Flash)      ← primario, retención cero
2º  otro host que NO entrene           ← respaldo
3º  el agente se calla y atiende el humano
    → y ese pedido NO se cobra (la regla ya la tenemos)
```

**Y una advertencia que vale más que el ahorro:** la falla más probable de este agente **no es el precio ni el proveedor — es que el modelo responda mal** (un plato que no existe, un precio inventado, un total errado). Por eso la regla del punto 4 no es opcional: **nada sale al cliente sin validarse en código** (plato del catálogo, precio del catálogo, total cuadrado).

---

## 7. RIESGOS

| Riesgo | Severidad | Nota |
|---|---|---|
| Que el host cambie su política de datos | MEDIA | Se revisa en el alta de cada restaurante; la regla es *contratar por host*, y se puede cambiar de host sin tocar el agente |
| Que un tier gratis se cuele "porque ahorra" | **ALTA** | **Es la trampa de este proyecto.** El ahorro máximo es US$1,45/mes; el daño es incumplir el contrato de datos |
| Que el modelo invente un plato o un precio | **ALTA** | Validación en código antes de enviar (punto 4) |
| La foto de lista a mano | MEDIA | Es lo único que aún **no** puedo prometer: hay que probarlo con fotos reales |
| Latencia y disponibilidad del proveedor | MEDIA | Dos hosts + la ruta de fallo del punto 6 |

---

## 8. LO QUE LE PIDO DECIDIR

1. **¿Aprobamos el motor del agente = DeepSeek V4 Flash en DeepInfra + faster-whisper local para la voz?** *(recomendado)*
2. **¿Regla de taller: "se contrata por HOST, nunca por nombre de modelo"**, y ningún tier gratuito en producto que se le cobra a un cliente? *(recomendado)*
3. **¿Se prueba la foto de lista a mano antes de incluirla en la oferta?** *(Zavora ya la tiene; nosotros no la hemos medido)*

---

## FUENTES

- **Comparativa de tiers gratuitos 2026 (RPM/RPD por proveedor, columna de "Data Training": Google AI Studio entrena fuera de UE/UK/EEE, Mistral Experiment entrena; OpenRouter gratis = 20 RPM y 50 peticiones/día):** https://openrouter.ai/blog/tutorials/free-llm-apis-compared/
- **Cuota gratuita: 9 de 19 modelos pueden entrenar con tus prompts, un solo host sin respaldo, cambian en meses, y el techo vale ~US$6/mes en un host que no entrena:** https://www.truefoundry.com/blog/openrouter-free-models-what-actually-free-and-what-it-costs-you
- **Políticas por host de OpenRouter (DeepSeek ✕ "puede entrenar" · DeepInfra ✓ "retención cero, no entrena" · Google AI Studio retiene 55 días):** https://openrouter.ai/docs/guides/privacy/provider-logging
- **Precios 2026 (DeepSeek V4 Flash en DeepInfra $0,09/$0,18 · gpt-oss-120b $0,037/$0,17 · Llama 3.1 8B $0,02/$0,03 · Gemini 2.5 Flash-Lite $0,10/$0,40; "precio por token no es precio por tarea"):** https://www.morphllm.com/llm-api-pricing
- **Precio de Gemini 2.5 Flash-Lite:** https://pricepertoken.com/pricing-page/model/google-gemini-2.5-flash-lite
- **Transcripción local $0/minuto vs APIs:** https://www.digitalapplied.com/blog/local-speech-to-text-whisper-self-hosted-transcription-2026

---

## DATOS CRUDOS

`C:\Users\Admin\intel\agente-modelo-20261029\` — y el cálculo completo en `calculo-costos.txt` (corrido con TRM 3.164 y verificando el costo contra la factura en dos escenarios).

---

*Salve, Gran Monarca. Modelo pequeño sí; gratis no — y la razón no es el dinero: **es que el tier gratuito se queda con las conversaciones de sus clientes**, que es exactamente lo que acabamos de prometerle al restaurante que no pasaría. El modelo cuesta **$4,6 por pedido** contra una tarifa de **$500**: aquí no se ahorra apretando el modelo, se ahorra **cacheando el catálogo y no dejando que la IA haga cuentas**.*

**— Bellion, Gran Comandante del Ejército de Sombras.**
