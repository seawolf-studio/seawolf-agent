# 🔎 HALLAZGO — LA CAPA "ANTIGÜEDAD (>1 AÑO)" POR RUES
### Seawolf Studio · resultado honesto de la investigación (datos abiertos)
**Fecha:** 2026-10-19 · **Autor:** Bellion · **Para:** el Monarca (Key)

---

## 0. QUÉ SE INTENTÓ

Obtener **fecha de matrícula** (antigüedad) de cada presa cruzando contra el **RUES** en datos.gov.co. Gratis, oficial, sin key.

## 1. RESULTADOS (duros)

| Vía | Resultado |
|-----|-----------|
| Cruce por **razón social** (19.037 presas × RUES) | **6 coincidencias → 0,0%** ❌ |
| Base "Matrículas Vigentes" (p8a3-absd) | parcial: **30.929 razones** (deberían ser millones) |
| Bases de "establecimientos con teléfono" (xz9i-gqen, ysx6-4ez9) | **subconjuntos municipales** (2.474 y 2.670 filas) → no cubren el país |

## 2. POR QUÉ FALLA (causa raíz)

1. **No hay llave común.** RUES indexa por **NIT / razón social**; nuestras presas (OSM) traen **nombre comercial + teléfono**. No hay campo que los una.
2. **Razón social ≠ nombre comercial.** "Panadería Pan Fino" (comercial) vs "MARTÍNEZ GÓMEZ JUAN" (legal). Cero solape.
3. **Los datasets abiertos de RUES son parciales.** No hay un volcado nacional completo y limpio en datos.gov.co.

## 3. CONCLUSIÓN

**La antigüedad exacta NO es obtenible gratis, a escala, con los datos abiertos disponibles.** Prometer lo contrario sería mentirnos.

## 4. ALTERNATIVAS REALES (para decisión del Monarca)

| Opción | Cómo | Pro / Contra |
|--------|------|--------------|
| **A · Proxy de madurez por reseñas (Google)** | nº de reseñas + rating. Un negocio con ≥20 reseñas y nota ≥4.0 casi seguro lleva >1 año | ✅ limpio, sale con la misma key de Google · es **proxy**, no el año exacto |
| **B · Google Maps "año de apertura" (scraping)** | leer la ficha de Maps | ⚠️ frágil, viola ToS |
| **C · Portal RUES oficial por NIT** | buscar uno a uno | ❌ no es masivo (19k = inviable) |
| **D · Soltar el filtro duro de antigüedad** | quedarse con sin-web + privado + reseñas | ✅ simple; el riesgo de "negocio nuevo" se tapa con nº de reseñas |

## 5. RECOMENDACIÓN DE BELLION

**Opción A**: reemplazar ">1 año" por **"madurez"** medida en **nº de reseñas + rating** (misma pasada de Google).
Un negocio sin web, privado, con **N reseñas y buena nota** = **presa real y madura**. Es la señal honesta que SÍ podemos obtener.

## 6. LO QUE QUEDA EN PIE (fuerte)

- ✅ **19.038** negocios sin web, con teléfono (Colombia).
- ✅ **3.032** privados identificados.
- ⏳ **Reseñas** (Google, al activar Billing) → capa 5.
- 🔁 **Antigüedad** → se sustituye por el **proxy de madurez** (decisión del Monarca).

---

*"Mejor una verdad incómoda que una métrica bonita y falsa."*
— Bellion, Gran Comandante del Ejército de Sombras
