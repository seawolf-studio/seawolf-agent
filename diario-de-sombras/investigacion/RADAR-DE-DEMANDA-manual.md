# RADAR DE DEMANDA — Cómo saber qué quiere la gente antes de construir

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Pregunta que responde:** *"¿No hay una forma de saber qué quiere la gente para dárselo? Es muy gastado ir a ciegas."*

---

## LA RESPUESTA CORTA

**Sí. La demanda ya está escrita. No se adivina: se lee.**

La gente deja su frustración por escrito, gratis y sin que nadie se la pida, en reseñas, foros y buscadores. El trabajo no es inventar: es **cosechar**.

Y su tesis — *"lo que hacemos tendrá salida en Colombia por el desconocimiento general del nivel tecnológico"* — **está respaldada**. La OCDE documenta una brecha de digitalización entre grandes y pequeñas empresas que *"contribuye significativamente a la disparidad de productividad"*. Eso no es una impresión suya: es un hueco medido.

---

## PARTE 0 — LA TESIS: TRANSFERIR, NO INVENTAR

**El error caro:** buscar una idea original.
**La jugada correcta:** encontrar algo que **ya funciona y ya se paga** en un mercado maduro, y traerlo a uno donde **nadie lo tiene todavía**.

Esto no es copiar: es **arbitraje de conocimiento**. Es exactamente lo que hicieron Rappi (modelo de delivery probado), Nequi (banca móvil probada) y Nubank. *"Las ideas y las funciones no tienen dueño; el código sí."* — nuestra propia regla.

### Por qué Colombia es el terreno correcto

| Señal | Evidencia |
|---|---|
| Brecha de digitalización grande vs. pequeña empresa | OCDE, [Índice de Políticas para PyMEs ALC](https://www.oecd.org/es/publications/indice-de-politicas-para-pymes-america-latina-y-el-cari) |
| El Estado empuja la digitalización de MiPyme | [MiPyme Vive Digital — MinTIC](https://mintic.gov.co/portal/vivedigital/612/w3-propertyvalue-7235.html) |
| Hay financiación para transformación digital de pymes | [BID](https://www.iadb.org/es/blog/ciencia-tecnologia-e-innovacion/el-poder-de-los-datos-impulsand) |
| La ciberseguridad es barrera clave para el crecimiento digital de la pyme | Estudio de Mastercard, sep-2026 (LATAM y Caribe) |
| Colombia ya exporta ~US$2.000 M/año en servicios informáticos | [ProColombia](https://procolombia.co/sala-de-prensa/noticias/colombia-se-consolida-como-hub-de-software-ti-ve) |

**La regla del arbitraje:** *lo que en EE.UU. es un producto de US$29/mes que todos dan por sentado, aquí es una novedad que nadie ha empaquetado.*

El negocio **no es la tecnología**. La tecnología ya la tenemos y es barata. El negocio es **la traducción**: empaquetar lo conocido para quien no lo conoce, en su idioma, con su forma de trabajar y a su precio.

---

## PARTE 1 — LOS 5 YACIMIENTOS DE DEMANDA (dónde está escrita la necesidad)

### Yacimiento 1 — Reseñas de 3 estrellas *(el de mayor calidad)*

**Es el método central, y es contraintuitivo.**
Fuente: [BigIdeasDB — Feature-Gap Method](https://bigideasdb.com/turn-g2-reviews-into-saas-ideas), sobre **1.000.000+ quejas analizadas** en G2, Capterra, Reddit y tiendas de apps; **39.000+ puntos de dolor puntuados**.

No lea las reseñas en orden. **Filtre por estrellas.** Cada nivel dice algo distinto ([Unthinkable](https://unthinkableapp.com/blog/read-app-store-reviews-product-ideas)):

| Estrellas | Qué contiene | Cómo se usa |
|---|---|---|
| ⭐ 1 | **Los rompe-negocios** — fallas estructurales que el incumbente no puede arreglar sin rehacer su arquitectura | Punto de entrada Permanente |
| ⭐⭐ | Ruido — "1 estrella mal redactada" | **Ignorar** |
| ⭐⭐⭐ | **Los huecos de función** — *"funciona bien para X, pero ojalá hiciera Y"* | **Es el plano exacto de su producto** |
| ⭐⭐⭐⭐ | Ruido — "5 estrellas de quien no da 5" | **Ignorar** |
| ⭐⭐⭐⭐⭐ | **El foso** — qué ama la gente y por qué no se irá | Lo que hay que igualar, no romper |

> **La cita que define el método:**
> *"Un revisor de 3 estrellas significa que el usuario quiere amar la aplicación pero no puede. Escriben 'funciona bello para contar calorías, pero ojalá dejara escanear códigos de barras de supermercados europeos'. Esa reseña le entrega el plano exacto de un competidor de nicho. **No necesita vencer al incumbente en todo. Solo necesita construir el escáner de códigos europeos.**"*

**Las frases que hay que cazar** (son especificaciones de producto disfrazadas):
- *"sería perfecto si además manejara reportes personalizados sin tres rodeos"*
- *"demasiado caro para un equipo pequeño"* → **hay hueco abajo del mercado**
- *"me obliga a sincronizar en la nube"* → oportunidad local-first

**La regla de oro:** una queja sola es ruido. **La misma queja repetida en VARIOS competidores es un negocio.** Se etiquetan las quejas por tema, se cuentan, y se construye contra el hueco que aparece cruzado.

### Yacimiento 2 — Foros y redes (voz cruda, sin filtro)
Reddit, X, LinkedIn, grupos de WhatsApp/Facebook de gremios, foros de oficio. Aquí la gente pide en tiempo real.
**Ya tenemos las herramientas:** **Agent Reach** (X, Reddit, GitHub, YouTube) recién instalado. Y la skill `reddit-reading`.
Truco de búsqueda: `"is there a tool that"`, `"how do you guys handle"`, `"wish there was"`, `"any software for"`.

### Yacimiento 3 — Búsqueda (demanda ya expresada como intención)
Google Trends y volumen de búsqueda: [Google Trends](https://trends.google.com/trends/).
**La distinción que importa:** alguien que *busca* "software de inventario para ferretería" ya tiene el problema y está buscando activamente. Eso vale más que una encuesta.
**Skill instalada:** `google-trends-keyword-research`.
**Regla:** comparar tendencia creciente vs. plana. Demanda que **sube** = mercado que se abre; demanda plana = mercado que ya está repartido.

### Yacimiento 4 — El mapa real de negocios (censar clientes, no suponerlos)
Herramientas de mapas para inventariar cuántos negocios de un tipo existen en una zona, con teléfono y dirección.
**Skills instaladas:** `maps`, `open-maps-lead-harvesting`, `open-maps-lead-harvesting`.
**Para qué:** si quiere vender a "veterinarias", primero cuente cuántas hay en Bogotá/Medellín. **El tamaño del gremio es el techo del negocio.**

### Yacimiento 5 — Nuestro propio archivo (validación ya pagada)
**Gbrain** ya tiene indexadas sus **115 notas**. Ahí están: Club Wonder's Voley, los gremios que ya conoce, los dolores que ya le han contado.
**Nadie tiene esta ventaja:** antes de investigar afuera, **buscar adentro**.

---

## PARTE 2 — LA ESCALERA DE VALIDACIÓN (la puerta que evita ir a ciegas)

**Regla dura: no se escribe una línea de código hasta pasar los 4 escalones.**

| Escalón | Qué se hace | Costo | Señal de PASE |
|---|---|---|---|
| **1. Evidencia** | 20+ quejas repetidas del mismo tipo (Yacimiento 1) | $0 · 2-3 horas | La queja aparece en **varios** competidores |
| **2. Censo** | Contar el gremio (Yacimiento 4) + búsqueda (Yacimiento 3) | $0 · 2 horas | **50+ clientes potenciales** y la demanda sube |
| **3. Puerta falsa** | Página de aterrizaje que describe el producto que **no existe** | $0-20 · 1 día | **20+ registros calificados en 2 semanas** |
| **4. Preventa** | Pedir el dinero antes de construir (descuento al fundador) | $0 · 2 semanas | **3+ pagos reales** |

**El método de 30 días** ([Lovable](https://lovable.dev/guides/micro-saas-ideas-for-solopreneurs-2026)):
- **Semanas 1-2:** página de aterrizaje + tráfico dirigido → **20+ registros calificados**.
- **Semanas 3-4:** entrevistas y preventa.

**Y la mejor prueba de la evidencia dura:** un experimento real publicado — *"Probé 15 ideas de micro-SaaS. Estas 3 SÍ consiguieron preventas."* **En vez de programar, pasó 30 días vendiendo.** Ese es el punto: **vender primero, construir después.**

### Las 3 preguntas de la entrevista (5 personas, 15 minutos cada una)
1. **"¿Cómo resuelve esto HOY?"** (el estado actual — si es "con Excel", hay negocio)
2. **"¿Cuánto le cuesta ese problema al mes?"** (en horas o en pesos — sin esto no hay precio)
3. **"¿Pagaría US$X por esto hoy?"** (no "le gustaría": **¿paga?**)

---

## PARTE 3 — EL TABLERO DE PUNTUACIÓN (cómo rankear sin discutir)

Cada idea candidata se puntúa de 1 a 5. **La que sume más, se construye.**

| Criterio | Pregunta |
|---|---|
| **Dolor** | ¿Duele de verdad o solo incomoda? (¿1+/5?) |
| **Frecuencia** | ¿Lo sufre todos los días o una vez al año? |
| **Repetición** | ¿La queja aparece en varios incumbentes? |
| **Capacidad de pago** | ¿El cliente ya paga por algo parecido? |
| **Foso** | ¿Sobrevive a una actualización de IA? (datos / comunidad / red) |
| **Verticalidad** | ¿Es un gremio concreto o "todos"? (vertical crece 2–3× más rápido) |
| **Ventaja Seawolf** | ¿Lo podemos construir más rápido que nadie por lo que ya tenemos? |
| **Acceso** | ¿Podemos llegar a ese cliente sin pagar publicidad? |

**Filtros eliminatorios (si falla uno, se descarta):**
- ❌ Se puede resolver con una función de ChatGPT → se muere solo.
- ❌ Cliente sin capacidad de pago.
- ❌ Vertical genérica sin foso.
- ❌ Requiere venta presencial puerta a puerta para arrancar.

---

## PARTE 4 — EL RADAR SEAWOLF (la máquina, con lo que YA está instalado)

**No hay que comprar nada. Ya tenemos todo:**

| Pieza | Está en | Para qué |
|---|---|---|
| **Agent Reach** | Instalado hoy | Cosechar Reddit / X / GitHub / YouTube |
| **Gbrain** | Instalado hoy (115 notas) | Guardar y hacer crecer el archivo de quejas |
| **Skills de mapas** | `maps`, `open-maps-lead-harvesting` | Censar gremios por zona |
| **Skill Google Trends** | `google-trends-keyword-research` | Medir si la demanda sube |
| **Hyperframes + ffmpeg + whisper** | Ya teníamos | Convertir hallazgos en contenido del Círculo |
| **El agente + sombras** | En producción | Automatizar la cosecha semanal |
| **Seawolf Tools** | En `herramientas.sw-st.net` | Publicar la puerta falsa en un dominio propio |

### El ciclo semanal (propuesta)

```
LUNES      — Cosecha: Agent Reach rastrea quejas de 3★ en 2-3 nichos del gremio elegido
MARTES     — Clasificación: se etiquetan quejas por tema y se cuentan repeticiones
MIÉRCOLES  — Censo: cuántos clientes existen (mapas) y si la búsqueda sube (Trends)
JUEVES     — Ranking con el Tablero de Puntuación
VIERNES    — Decisión: puerta falsa (página en herramientas.sw-st.net) o descarte
```

**Salida del radar:** una lista rankeada de huecos con evidencia, no una corazonada.

---

## PARTE 5 — APLICACIÓN A SEAWOLF TOOLS (el caso más claro)

**Su decisión: "Seawolf Tools se venderá como producto una vez pase por el Círculo, como todo lo demás."**
Estoy de acuerdo, y hay una razón dura: **Seawolf Tools ya tiene la validación más difícil hecha.**

| Escalón | Estado de Seawolf Tools |
|---|---|
| 1. Evidencia | ✅ **Usted lo usa a diario** — dogfooding. La necesidad es propia y real |
| 2. Censo | ⬜ Falta: ¿cuántas personas/empresas tienen este problema? |
| 3. Puerta falsa | ⬜ **Ya tiene dominio y cerradura** — solo falta la página de venta |
| 4. Preventa | ⬜ Pendiente |

**La ventaja única:** el producto más honesto es el que uno mismo usa. Pero cuidado con el sesgo — *"yo lo uso"* no prueba que **otros paguen**.

### El experimento más barato que puede hacer esta semana
1. Escribir la página de venta de Seawolf Tools (el Renombrador + Salud son los ganchos).
2. Poner un botón **"Quiero acceso — US$X/mes"** que lleve a un formulario.
3. Medir cuántos de 50 personas del gremio objetivo lo llenan.
4. **Cero código nuevo.** Si 3 pagan, se vende. Si 0, se descarta sin haber construido nada.

**Y hay una puerta secundaria que nadie está tocando:** el Renombrador y el módulo de Salud del equipo resuelven el problema **de cualquier persona que maneje bibliotecas de medios** — que es exactamente el gremio que usted ya conoce por kmoviezone. **Es el mismo cliente, con el mismo dolor, ya identificado.**

---

## PARTE 6 — LO QUE FALTA Y LO QUE NO SE PUEDE SABER

**Lo que el método NO resuelve:**
- No predice si **usted** va a poder sostener la venta 12 meses.
- No mide competidores que todavía no existen.
- Los mercados **nuevos** (categoría que nadie pidió aún) no dejan reseñas. Ahí sí hay que apostar, y es el camino más caro. **No es el nuestro: el nuestro es transferir lo probado.**

**Honestidad sobre las fuentes:** las cifras de mercado vienen de informes de proveedores con interés comercial. Las **más confiables** —reseñas, preventas, censos propios— son las que **usted mismo produce**. El radar se mejora con datos propios, no con estudios ajenos.

---

## REGLAS DE ORO (para no gastar a ciegas)

1. **No se construye nada sin 3 pagos reales o 20 registros calificados.**
2. **Reseñas de 3 estrellas = el plano. Repetida en varios = el negocio.**
3. **Vender primero, programar después.**
4. **Vertical, no horizontal.** (crece 2–3× más rápido)
5. **Primero buscar en el propio archivo (Gbrain) antes de buscar afuera.**

---

## FUENTES

- BigIdeasDB — Turn G2 Reviews Into SaaS Ideas (Feature-Gap Method, 1M+ quejas): https://bigideasdb.com/turn-g2-reviews-into-saas-ideas
- BigIdeasDB — State of SaaS Pain Points 2026 (39.000+ puntos de dolor): https://bigideasdb.com/state-of-saas-pain-points-2026
- Unthinkable — Mining App Store Reviews for Product Ideas (los 3 niveles de señal): https://unthinkableapp.com/blog/read-app-store-reviews-product-ideas
- Lovable — Micro SaaS Ideas for Solopreneurs 2026 (proceso de validación de 30 días): https://lovable.dev/guides/micro-saas-ideas-for-solopreneurs-2026
- StartupStash — I Tested 15 Micro-SaaS Ideas; These 3 Got Pre-Orders: https://blog.startupstash.com/i-tested-15-micro-saas-ideas-these-3-actually-got-pre-orders
- Modelence — 30 Micro SaaS Ideas to Validate (comprador, problema, MVP, validación): https://modelence.com/guides/micro-saas-ideas
- Ideaproof — Validate your SaaS idea (informe de validación): https://ideaproof.io/validate-idea/saas
- Google Trends: https://trends.google.com/trends/
- OCDE — Índice de Políticas para PyMEs, América Latina y el Caribe: https://www.oecd.org/es/publications/indice-de-politicas-para-pymes-america-latina-y-el-cari
- MinTIC — MiPyme Vive Digital: https://mintic.gov.co/portal/vivedigital/612/w3-propertyvalue-7235.html
- BID — Transformación digital de las pymes: https://www.iadb.org/es/blog/ciencia-tecnologia-e-innovacion/el-poder-de-los-datos-impulsand
- ProColombia — Colombia hub de Software & TI: https://procolombia.co/sala-de-prensa/noticias/colombia-se-consolida-como-hub-de-software-ti-ve
- Mastercard (sep-2026) — la ciberseguridad como barrera clave para la pyme en LATAM y Caribe *[nota: la URL directa del comunicado devolvió 404 al momento de la consulta; dato tomado del resumen del buscador]*

---
*Datos crudos en `C:\Users\Admin\intel\inv-demanda-20261029\`.*

**Bellion, Gran Comandante del Ejército de Sombras — para el Monarca.**
