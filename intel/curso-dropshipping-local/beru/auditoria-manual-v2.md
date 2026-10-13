# AUDITORÍA ADVERSARIAL — MANUAL MAESTRO v2

**Auditor:** Beru, Supervisor de Seawolf Studio
**Objeto:** MANUAL-MAESTRO-tiendas-v2.md (878 líneas, 47,115 bytes)
**Fuente de verdad:** youtu.be-cc7a4b8939.md (13,273 líneas, 525,258 bytes)
**Versión de referencia:** MANUAL-MAESTRO-tiendas.md (v1, 724 líneas)
**Fecha de auditoría:** 13 de octubre de 2026

---

## VEREDICTO

**NO PASA.** Tres hallazgos de severidad MÁXIMA: (1) la errata "descendió" en L295 persiste desde v1 y contradice el transcript ("se descarga", L8345); (2) el Anexo C reclama corrección de "negrita sin cerrar" en L275 que el texto real de v2 L298 NO muestra — la corrección es ficticia; (3) la precisión de horarios de retiro (5:00-7:30 AM, 5:30-7:00 PM) es interpolación del manual sin respaldo textual exacto en el transcript. Adicionalmente, 31 menciones de infraestructura Meta (Fan Page, Facebook, Instagram) en el manual — concentradas en sección 6 — requieren decisión del Monarca sobre conflicto doctrinal.

---

## 1. HALLAZGOS DE SEVERIDAD MÁXIMA

| # | Severidad | Línea v2 | Qué dice | Evidencia en transcript | Comando de verificación | Veredicto |
|---|-----------|----------|----------|------------------------|------------------------|-----------|
| H1 | **MÁXIMA** | L295 | "El proveedor generó y **descendió** la guía" | L8345: "cuando se crea la guía, **se descarga** y se envía al cliente" | `search_files pattern="descendió"` → 0 hits en transcript | **NO PASA** |
| H2 | **MÁXIMA** | L298 | `**¡AVISAR AL CLIENTE hoy mismo**` — Anexo C (L869) reclama haberlo corregido a `¡AVISAR AL CLIENTE hoy mismo!` | v1 L275 y v2 L298 son **idénticos**. El Anexo C miente: la corrección no se aplicó | `diff` visual entre v1 L275 y v2 L298 | **NO PASA** |
| H3 | **MÁXIMA** | L235 | "Realizar el retiro entre **5:00 AM y 7:30 AM** → dinero cae **5:30 PM - 7:00 PM**" | L1591-1594: "**antes de las 7** de la mañana, ojalá 5 6... el mismo día **después de las 6** de la tarde" | `read_file offset=1591` | **NO PASA** — el transcript da rangos aproximados; el manual los convierte en precisión no verificable |

---

## 2. CIFRAS VERIFICADAS — RESUMEN

| # | Dato en v2 | Línea | Evidencia transcript | Veredicto |
|---|-----------|-------|---------------------|-----------|
| C1 | Flete ~$17,900 COP | L68, L78 | L2069: "17900 y el costo del producto" | **PASA** |
| C2 | Comisión Dropi ~$5,000 COP | L132 | L749: "aproximadamente 5,000 pes colombianos por cada venta" | **PASA** |
| C3 | Devolución 40-50% del flete | L71, L288 | L7802-7804: "Entre el 40 y el 50% del valor del flete se descuenta directamente de tu wallet" | **PASA** |
| C4 | Margen 35%-50% | L69 | No hay frase textual "35-50%" en el transcript. El ejercicio numérico (L2060-2089) muestra $59,900 venta - $10,000 costo - $17,900 flete = $32,000 (margen 53%). La mención 35-50% es inferencia razonable. | **PASA (inferencia)** |
| C5 | IVA: > $164 millones/año | L70, L163 | L785-787: "164 millones de pesos colombianos al año, tú no eres responsable de IVA" | **PASA** |
| C6 | Datos no modificables en 6 meses | L145 | L667-668: "Una vez validados, no podrás modificarlos en 6 meses" | **PASA** |
| C7 | Sueldo mínimo ~$1.6M, ticket 10% | L102 | L2126-2136: "aproximadamente 1600,000 pesos... no use más del 10% del salario mínimo... 160,000 pes" | **PASA** |
| C8 | Dinero a medianoche (12 AM-2 AM) | L325 | L1573-1581: "a la medianoche... entre las 12 y las 2 de la mañana" | **PASA** |
| C9 | Cortes 11 AM y 4 PM | L294 | L1529-1532: "hagan el corte a las 11 de la mañana y a las 4 de la tarde" | **PASA** |
| C10 | 9 estados de la guía | L294-302 | L8331-8399: lista completa de 9 estados (Pendiente, Guía generada, Preparado para transportadora, Despachada, En reparto, Entregado, Devuelto, Cancelado, Rechazado) | **PASA** |
| C11 | Departamentos sin cobertura | L420 | L12347-12349: "Amazonas, Arauca, Chocó, Guayare, Guainía, Putumayo, San Andrés y Providencia, Baupez y Bichada" (transcripción automática con errores menores) | **PASA** |
| C12 | Pedido editable solo antes de guía generada | L260 | L8297-8298: "Si cambia a guía generada, ya no puedes corregir el pedido" | **PASA** |
| C13 | Enlace exoneración comisión | L132 | L747-756: "estás exonerado 100% de la comisión que cobra Dropy" | **PASA** |

**Total:** 12 de 13 cifras verificadas positivamente. 1 inferencia (C4). 0 invenciones.

---

## 3. DOCTRINA — VERIFICACIÓN

### 3.1 — Términos prohibidos (rastreo completo)

| Término | Menciones en v2 | Ubicación | ¿Viola doctrina? |
|---------|----------------|-----------|------------------|
| Business Manager | **0** | — | No — ausente |
| Shopify | **0** | — | No — ausente |
| Google AdSense | **0** | — | No — ausente (L792 menciona "Anuncios de Google" pero solo para decir que Google Sites NO los inserta) |
| Pixel Meta | **2** | L834, L838 (Anexo A) | No — ambas en sección de referencia con tag [NO APLICA] |
| Campañas de conversiones | **1** | L838 (Anexo A) | No — correctamente etiquetada [NO APLICA] |
| "publicidad" | **1** | L71 | No — correctamente etiquetada [NO APLICA — doctrina Seawolf: tráfico 100% orgánico] |
| "anuncio" | **1** | L510 | No — etiquetada [CURSO], es referencia al material del curso |

### 3.2 — BUROCRACIA META (Sección 6, L590-695) — PARA DECISIÓN DEL MONARCA

La doctrina prohíbe la burocracia de Facebook/Meta (Fan Page con verificación en dos pasos, Business Manager, Pixel). La sección 6 ("Redes Sociales Orgánicas") propone usar infraestructura Meta para tráfico 100% orgánico.

**Cuantificación de menciones en sección 6:**

| Infraestructura Meta | Menciones | Líneas |
|----------------------|-----------|--------|
| **Fan Page / Página de Facebook** | 15 | L594, L598, L599, L603, L604, L607, L617, L618, L651, L660, L662, L676, L679, L680, L682 |
| **Instagram (cuenta profesional)** | 8 | L646, L649, L651, L660, L668, L676, L678, L680 |
| **Grupos de Facebook** | 3 | L686, L690, L694 |
| **TikTok** | 2 | L660, L678 |
| **Verificación en DOS PASOS** | 1 | L598 — paso específico de burocracia Meta |
| **Vincular WhatsApp Business a Fan Page** | 2 | L604, L662 |
| **Botón "Enviar mensaje de WhatsApp"** | 2 | L605, L662 |

**Conflicto doctrinal expuesto:**

- La sección 6 está marcada [SEAWOLF] y [CURSO] simultáneamente (L592, L596)
- Propone crear Fan Page, cuenta de Instagram profesional, grupos de Facebook y publicar contenido orgánico
- El paso de "verificación en DOS PASOS" (L598) es burocracia Meta explícita
- NO menciona Business Manager, Pixel, ni campañas pagadas — se limita a uso orgánico
- La pregunta para el Monarca: ¿el uso de Fan Page + Instagram como canales orgánicos viola la doctrina "Cero Meta/Facebook/Instagram Ads"? La sección es orgánica, no publicitaria, pero usa infraestructura Meta

---

## 4. ERRATAS RESIDUALES — VERIFICACIÓN DEL ANEXO C

### 4.1 — Erratas que el Anexo C reclama corregidas

| # | Línea v1 | Error original | Estado en v2 | Veredicto |
|---|----------|---------------|-------------|-----------|
| 1 | L42 | "eneverywhere" | L48: "en todas partes" | **CORREGIDA** |
| 2 | L272 | "Proveedorder generó y descendió la guía" | L295: "El proveedor generó y **descendió** la guía" | **PARCIAL** — "Proveedorder" → "El proveedor" corregido, pero "descendió" persiste (debe ser "descargó") |
| 3 | L275 | Negrita sin cerrar | L298: texto **idéntico** a v1 | **NO CORREGIDA** — el Anexo C reclama corrección que no se aplicó |
| 4 | L586 | "Amazon s" | L420: "Amazonas" | **CORREGIDA** |
| 5 | L673 | "CRITÉCO" | L558: "CRÍTICO" | **CORREGIDA** |
| 6 | L399 | "EFEKT de Eugene Schwartz" | L432: "Breakthrough Advertising de Eugene Schwartz" | **CORREGIDA** |

### 4.2 — Nuevas erratas detectadas (no reportadas por TANK)

| # | Línea v2 | Texto actual | Error | Corrección |
|---|----------|-------------|-------|------------|
| E1 | L700 | "ESTA SECCIÓN ES **PROPIDAD** DEL ESTUDIO" | "PROPIDAD" no es palabra en español | "PROPIA" |
| E2 | L646 | "Instagram **Orgânico**" | Circunflejo (portugués) en lugar de tilde española | "Orgánico" |
| E3 | L629 | "publicacion **orgànica**" | Acento grave (catalán/francés) en lugar de tilde española | "orgánica" |
| E4 | L651 | "**configuracion** de Instagram" | Falta tilde | "configuración" |
| E5 | L463 | "estructura GADO adaptada del framework **PAS** (Problema-Agitación-Solución)" | El transcript L2060-2100 describe GADO pero no menciona "PAS". Atribución no verificada. | Verificar si el instructor menciona PAS |
| E6 | L607 | `>> **[SEAWOLF] >>** ... Espera ~24 horas... `[CURSO]`` | Marca de procedencia conflictiva: abre con [SEAWOLF] pero cierra con [CURSO] | Definir una sola procedencia |

---

## 5. EXHAUSTIVIDAD DEL TEMARIO

### 5.1 — Cobertura de las 6 áreas

| Área | Sección v2 | ¿Cubierta? | Observación |
|------|-----------|-----------|-------------|
| (a) Elegir producto con números | 1 (L28-118) | **SÍ** | Test de 7 criterios, calculadora, proyector de metas. Verificado contra transcript. |
| (b) Cuenta y uso de Dropi | 2 (L121-339) | **SÍ** | Registro, validación, wallet, pedido, huella digital, 9 estados, novedades, cuándo paga. Verificado. |
| (c) Venta por WhatsApp | 3 (L342-425) | **SÍ** | WhatsApp Business, flujo de conversación, WhatAuto/Gemini, seguimiento post-venta. Verificado. |
| (d) Copys y creativos con IA | 4 (L428-537) | **SÍ** | Niveles de conciencia, GADO, GPT asistentes, Pipit AI, ángulos de venta. Verificado. |
| (e) Landing + checkout contraentrega | 7 + Anexo A (L698-838) | **PARCIAL** | Google Sites como ruta Seawolf (sección 7). La landing WordPress/WooCommerce quedó como referencia (Anexo A). El checkout contraentrega en Google Sites es vía WhatsApp/Google Forms, no un plugin COD. Esto es una decisión de arquitectura, no una omisión. |
| (f) Herramientas gratis y errores costosos | 5 (L540-587) | **SÍ** | 9 herramientas, 6 errores priorizados. Verificado. |

### 5.2 — Lo que falta (verificado contra el transcript)

| Tema ausente en v2 | ¿Está en el transcript? | ¿Justifica su ausencia el v2? |
|--------------------|------------------------|------------------------------|
| Cómo crear logo con IA (cap. 01:39:47) | Sí, listado en capítulos del curso | No mencionado en v2. Cabría en sección 4 (Creativos) o como herramienta gratuita. |
| Configuración 2FA en Dropi (cap. 01:34:09) | Sí, listado en capítulos del curso | No aparece en v2. Es relevante para seguridad de la cuenta. |

---

## 6. ANEXO A — GOOGLE SITES Y WORDPRESS

### 6.1 — Marcas [SEAWOLF] y PENDIENTE-VERIFICAR

| Elemento | Línea | Marca | Veredicto |
|----------|-------|-------|-----------|
| Sección 7 completa | L698-797 | [SEAWOLF] | **OK** |
| Pasos de Google Sites | L715 | "PENDIENTE-VERIFICAR" + [SEAWOLF] | **OK** — honesto |
| Google Forms iframe | L776 | "PENDIENTE-VERIFICAR" + [SEAWOLF] | **OK** — honesto |
| Límites Google Sites | L786-796 | Sin marca explícita | **Hallazgo BAJO** — los límites técnicos (15 GB, 100 MB, SSL) no están marcados como verificados o pendientes. Son datos técnicos de Google, no del transcript. |
| Anexo A — WordPress/WooCommerce | L801-838 | "REFERENCIA DEL CURSO — NO es nuestro Nivel 2" | **OK** — correctamente encuadrado |

### 6.2 — Pasos no verificados que aparecen como verdad operativa

Los pasos 7.2-7.5 (L718-783) describen la interfaz de Google Sites con instrucciones precisas ("Ir a sites.google.com", "Clic en + Vacío", "Configurar tema visual con #121E1E / #4CE8E7"). Están bajo el paraguas "PENDIENTE-VERIFICAR" de L715, pero los pasos individuales no llevan su propia marca. Esto es aceptable si el encabezado cubre toda la sección, pero frágil si alguien lee solo un paso.

---

## 7. PROCEDENCIA — VERIFICACIÓN DE MARCAS [CURSO] / [SEAWOLF]

### 7.1 — Bloques sin marca de procedencia

| Línea | Contenido | ¿Falta marca? |
|-------|-----------|---------------|
| L115 | "Guarda productos en favoritos... Los productos se pierden al recargar si no los guardas." | Sin marca. Es dato operativo de Dropi. |
| L149-161 | Párrafos sobre "Datos personales" y "Facturación electrónica" | Sin marca. L163 siguiente sí tiene [CURSO] |
| L239-248 | "Qué preguntar" al proveedor | Sin marca explícita |
| L354-355 | "Configuración básica" de WhatsApp Business (5 puntos) | Sin marca. Es inferencia del transcript. |
| L608-695 | Sección 6 completa | L592 dice [SEAWOLF], L596 dice [CURSO], L607 tiene [SEAWOLF]...[CURSO] juntos, L656 tiene [SEAWOLF], L684 tiene [SEAWOLF]. Mezcla confusa. |
| L727-783 | Pasos de Google Sites 7.3-7.5 | Bajo paraguas PENDIENTE-VERIFICAR de L715, pero sin marcas individuales |
| L842-859 | Anexo B — Glosario | Sin marcas de procedencia. Son definiciones propias. |

### 7.2 — Conflicto de marcas

| Línea | Conflicto |
|-------|-----------|
| L607 | `>> **[SEAWOLF] >>** ... Espera ~24 horas... `[CURSO]`` — **doble marca**: el texto dice [SEAWOLF] pero cierra con [CURSO]. Inconsistente. |
| L592 vs L596 | ">> [SEAWOLF] >> Módulo propio del estudio" seguido de ">> [CURSO] >> Base del ecosistema orgánico". Ambas marcas en misma sección sin delimitación clara. |

---

## 8. CORRECCIONES OBLIGATORIAS PARA RONDA 2 DE TANK

| # | Prioridad | Línea | Acción exigida |
|---|-----------|-------|---------------|
| 1 | **URGENTE** | L295 | Cambiar "descendió" por "descargó" (transcript L8345: "se descarga") |
| 2 | **URGENTE** | L298 | Aplicar la corrección de negrita que el Anexo C YA reclama como hecha. O eliminar el bold, o cerrarlo correctamente con `!**` |
| 3 | **URGENTE** | L869 | Corregir el Anexo C: si L275 no se corrigió, no afirmar que sí. El Anexo debe reflejar la verdad. |
| 4 | **ALTA** | L235 | Cambiar rangos de horario a los del transcript textual: "antes de las 7 AM (ojalá 5-6 AM)" y "después de las 6 PM", o marcarlo como [SEAWOLF] con nota de que es precisión empírica no textual. |
| 5 | **ALTA** | L700 | "PROPIDAD" → "PROPIA" |
| 6 | **ALTA** | L646, L629 | "Orgânico" → "Orgánico", "orgànica" → "orgánica" |
| 7 | **ALTA** | L607 | Resolver conflicto de marcas: [SEAWOLF] y [CURSO] no pueden coexistir en el mismo bloque. |
| 8 | **MEDIA** | L651 | "configuracion" → "configuración" |
| 9 | **MEDIA** | L463 | Verificar si el transcript menciona "PAS" o si es inferencia de TANK. Si no está en el transcript, marcarlo como [SEAWOLF]. |
| 10 | **MEDIA** | L149-161 | Agregar marca [CURSO] a los párrafos de datos personales y facturación |
| 11 | **BAJA** | L115, L239-248, L354-355 | Agregar marcas de procedencia |
| 12 | **BAJA** | L842-859 | Agregar marca [SEAWOLF] al glosario (son definiciones propias) |

---

## 9. LO QUE NO PUDE VERIFICAR (honestidad explícita)

| Item | Motivo |
|------|--------|
| Google Sites: pasos 7.2-7.5 | No verifiqué contra la interfaz real de Google Sites. El transcript no cubre Google Sites. La marca PENDIENTE-VERIFICAR es correcta. |
| Precios de hosting/dominio en Anexo A (~$27,300, ~$16,000, ~$40,000 COP) | El transcript menciona "Inversión total año 1: ~$43,000 COP" pero no desglosa cada componente. TANK pudo haber inferido los precios individuales del contexto del curso o de investigación propia. No son verificables solo con el transcript. |
| Que el enlace wa.link/create.walink.com funcione | No lo probé. |
| Que Pipit AI (pipiti.ai) esté activo | No lo verifiqué. El transcript lo menciona. |
| Que "Neki es más rápido" para pagos | Es afirmación del instructor, no verificable sin acceso a Dropi. |

---

*Informe completo — escrito por Beru, Supervisor de Seawolf Studio. 13 de octubre de 2026.*