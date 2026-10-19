# 🎚️ SISTEMA DE FILTROS v2 — SEGMENTAR, NO DESCARTAR
### Seawolf Studio · corrección del Monarca aplicada
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)

---

## 0. LA CORRECCIÓN (del Monarca)

> *"No necesariamente debemos descartarlos; por ejemplo, un colegio PRIVADO podría ser un cliente. Esto me demuestra que debemos aplicar más filtros."*

**Verdad adoptada:** descartar por categoría es perezoso. **Un colegio privado, una clínica privada, un club privado = leads legítimos.** La respuesta no es borrar: es **etiquetar y puntuar**.

---

## 1. LAS CAPAS DE FILTRO (en vez de una lista negra)

| Capa | Qué separa | Fuente |
|------|-----------|--------|
| **1 · Sin web** | la joya base | OpenStreetMap ✅ |
| **2 · Tipo de entidad** | **privado vs público** | OSM `operator:type` + **RUES** (persona natural/jurídica) + nombre |
| **3 · Sector** | comercial / institucional / mixto | OSM `amenity/shop/...` (clasificar, NO descartar) |
| **4 · Antigüedad** | **>1 año montado** | **RUES** (fecha de matrícula) |
| **5 · Reseñas** | **>80% positivas** | **Google Places** (rating + nº) |

**Puntaje final** = combinación → semáforo **CALIENTE / TIBIA / FRÍA**.

---

## 2. EVIDENCIA (probe OSM Colombia, hoy)

| Colegios | Cantidad |
|----------|---------:|
| `operator:type = private` | **3.570** |
| `operator:type = public` | 20.489 |
| sin etiqueta | 10.796 |

**Lectura:** OSM ya nos da **3.570 colegios privados** sin web (leads directos). Pero **10.796 quedaron sin etiqueta** → hay que **enriquecer** (RUES/Google) para clasificarlos. La etiqueta de privacidad no siempre viene en OSM.

---

## 3. REGLA DE ORO DEL SCORING

> Un **colegio privado** sin web + **>1 año** + **buenas reseñas** = **LEAD CALIENTE**, no descarte.

El sector NO define el descarte. Lo define la **privacidad + antigüedad + reputación + (sin web)**.

---

## 4. QUÉ MONTA HOY (gratis, sin key)

- **Vigía v4** — re-barrido que captura las **etiquetas de segmentación** (`operator:type`, `brand`, `isced:level`) para separar privado/público **sin adivinar**. → `/opt/vigia/presas_v4.csv`.

## 5. QUÉ MONTA MAÑANA (con tu API key de Google)

- **Reseñas** (Google Places) → capa 5.
- **Antigüedad** (RUES, datos.gov.co) → capa 4.

---

*"No quemes el bosque para quitar la maleza. Etiqueta cada árbol y corta el que no sirve."*
— Bellion, Gran Comandante del Ejército de Sombras
