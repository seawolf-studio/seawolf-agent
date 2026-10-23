# PLAN MAESTRO — "EL CÍRCULO PUBLICITARIO"
## Línea de montaje de impulso de marca (concepto → aplicativo)

**Fecha:** 2026-10-14 · **Clasificación:** Uso Interno — Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Estado:** Concepto aterrizado → plano construible. Uso interno primero; servicio vendible con métricas después.

---

## 1. VISIÓN

**El Círculo Publicitario** = una **línea de montaje** que toma un producto/servicio X y lo empuja a viralizarse en redes mediante **impulsos** repetibles.

> No vendemos "publicación automática". Vendemos **IMPULSO CON MÉTRICAS**.

**Principio rector:** la automatización es commodity; el valor está en **(a) el ángulo creativo** y **(b) el bucle de métricas**. El sistema genera 100 ideas → filtra 10 con rúbrica → las ejecuta y publica → **mata perdedoras, escala ganadoras**.

---

## 2. ARQUITECTURA — 6 ESTACIONES

| # | Estación | Entrada | Proceso | Salida | Herramienta | ¿Auto? |
|---|----------|---------|---------|--------|-------------|--------|
| **1** | **Concepto / Ángulo** | Producto X + **datos de demanda (Google Trends)** | Angles por 6 ejes | 100 ideas | LLM (OpenRouter) + `marketingskills` + **`trends-demanda.py`** | Semi (tú apruebas) |
| **2** | **Atributos / Hooks** | 100 ideas | Rúbrica 0–5 × 5 criterios | **Top 10** + hooks | LLM + rúbrica | ✅ |
| **3** | **Creativos** | Top 10 | Copy + imagen + video | 10 piezas | LLM + LocalAI/SD + **MoneyPrinterTurbo** + `autoclip` | ✅ |
| **4** | **Variantes nativas** | 10 piezas | 3–4 formatos por red | 30–40 variantes | LLM + plantillas | ✅ |
| **5** | **Publicación** | Variantes | Calendarización multi-cuenta | Posteado | **mixpost** (centro, API oficial) | ✅ |
| **6** | **Medición → Decisión** | Resultados | Alcance/CTR/conv. | Kill / Scale | analytics + monitor | ✅ (juicio) |

**Regla de oro:** estaciones 1 y 6 exigen **tu juicio**. El resto se automatiza.

---

## 3. EMBUDO 100→10 (el corazón)

### 3.1 Generación por 6 EJES (no "dame 10 ideas")
Se piden 15–20 ideas por eje → diversidad forzada:
**dolor · deseo · envidia · miedo/pérdida · curiosidad · estatus · humor · prueba social.**

### 3.2 Rúbrica de scoring (0–5 cada criterio)
| Criterio | Pregunta |
|----------|----------|
| **Hook** | ¿gana en 1 segundo / 3 palabras? |
| **Dolor** | ¿le duele al público real? |
| **Diferenciación** | ¿ya se vio mil veces? (≈80% muere aquí) |
| **Prueba** | ¿credibilidad / demo? |
| **Encaje** | ¿nativo de ESA red? |

**Suma → ordenar → Top 10.**

### 3.3 Hooks + variantes
5 hooks por idea ganadora → se testea el **hook**, no el contenido. Luego 3–4 variantes nativas por red.

---

## 4. MATRIZ DE PLATAFORMAS

| Red | Comportamiento | Formato | Hook que gana | Cadencia |
|-----|----------------|---------|---------------|----------|
| TikTok | descubrimiento, ocio | 9:16 | 1s, crudo > pulido | 1–3/día |
| IG Reels | estética, aspiración | 9:16 | visual+texto | 3–5/sem |
| YouTube Shorts | ocio+búsqueda | 9:16 | título importa | 3–5/sem |
| X/Twitter | opinión, tiempo real | texto/hilo | 1ª línea | 3–10/día |
| LinkedIn | profesional, valor | texto+doc | insight | 3–5/sem |
| Facebook | comunidad/grupos | video+texto | historia | 3–5/sem |
| Pinterest | intención compra | 2:3 | imagen fuerte | 5+/sem |
| Threads/Bluesky | conversación/nicho | texto | pregunta | diario |

**Ganchos "modo Temu":** precio · urgencia · demostración visual. Funciona por **volumen + iteración**, no por pieza perfecta.

---

## 5. MAPA TECNOLÓGICO (repos MIT, verificados)

| Estación | Herramienta | ★ | Rol |
|----------|-------------|---|-----|
| 1–2 | **coreyhaines31/marketingskills** | 54.768 | Skills de marketing/copy para agentes |
| 1–2 | ericosiu/ai-marketing-skills | 3.634 | Skills de growth/experimentos |
| 1–2 | mikiarlo3/ai-copywriter | 1.212 | Copywriter con método real |
| 1 | **`trends-demanda.py`** (interno) | — | **Demanda real: Google Trends → veredicto (se mueve / no se mueve).** Alimenta el ángulo con datos, no corazonadas |
| 3 | **zhou Xiaoka/autoclip** | 9.414 | Video largo → clips |
| 3 | **MoneyPrinterTurbo** | 126.900 | Video desde texto (TTS+subs) |
| 3 | LocalAI / SD.cpp | — | Imagen |
| 3 | miqdadbadjuber/anti-slop | 6.083 | Reglas anti-genérico (adaptable) |
| 5 | **inovector/mixpost** | 3.812 | **Centro de publicación** |
| 5 | Katzca/AutoSocial | 1.386 | Video corto local (cuidado: ToS) |
| 6 | monitor-gasto + analytics | — | Métricas y control |

*(varios son 2026 → validar antigüedad según la regla antes de adoptar)*

---

## 6. BUCLE DE MÉTRICAS

```
Publicar N variantes  →  medir 48–72h  →  criterio:
  ├─ CTR alto + conversión  →  ESCALAR (más variantes del mismo ángulo)
  └─ CTR bajo               →  MATAR (cambiar ángulo, no formato)
```
**Se mide:** alcance, retención (video), CTR, guardados, comentarios, conversión.
**Decisión semanal:** presupuesto de creativos va a los ángulos ganadores.

---

## 7. PILOTO — USB 1TB + LLAVERO (producto ficticio)

1. **Ángulo raíz:** "chico que cabe en tu llave, pero guarda una biblioteca."
2. **6 ejes → 100 ideas** (LLM + marketingskills).
3. **Rúbrica → Top 10.**
4. **Creativos:** 10 piezas (video corto "antes/después", demo de capacidad, unboxing).
5. **Variantes nativas** por red (9:16 TikTok/Reels, hilo X, doc LinkedIn…).
6. **Publicar vía mixpost** en calendario.
7. **Medir 72h → escalar top 2, matar el resto.**
8. **Resultado:** el sistema queda probado con UN producto antes de venderlo.

---

## 8. FASES

| Fase | Qué | Entregable |
|------|-----|-----------|
| **F0** | Aplicativo/plano + rúbrica | ✅ este plan + app |
| **F1** | Piloto USB-llavero (1 producto) | 10 creativos + métricas |
| **F2** | Automatizar estaciones 1–4 | generador 100→10 funcionando |
| **F3** | Motor de publicación (mixpost) | multi-cuenta en VPS |
| **F4** | Bucle de métricas + dashboard | kill/scale |
| **F5** | Productizar como servicio | oferta "impulso con métricas" |

---

## 9. RIESGOS (honestos)
1. **Baneos:** automatizar publicación con navegador viola ToS → preferir **API oficial (mixpost)**.
2. **Contenido genérico:** sin diversidad de ejes, el output es promedio.
3. **"Impulso agresivo" mal calibrado** = spam reportado. Volumen ≠ calidad.
4. **Vender sin métricas** = no hay servicio. Los números SON el producto.
5. **Licencias:** el pool MIT de publicación es flaco; verificar mixpost Pro.

---

## 10. PRÓXIMO PASO
Aprobar **F1 (piloto USB-llavero)** y montar el aplicativo de control. Después: automatizar el embudo 100→10.

**Fin del plan maestro.**
