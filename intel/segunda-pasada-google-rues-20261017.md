# 🎯 SEGUNDA PASADA — RESEÑAS Y ANTIGÜEDAD (la ruta pesada)
### Seawolf Studio · plan para ejecutar mañana con la API key de Google
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)

---

## 0. LOS 3 FILTROS Y SU FUENTE REAL (verdad dura)

| Filtro pedido | ¿Dónde vive? | ¿Lo tenemos? |
|---------------|--------------|--------------|
| **Sin página web** | OpenStreetMap | ✅ (ya barrido, 2.200+) |
| **>80% reseñas positivas** | **Google Places** (rating + nº reseñas) | ⏳ necesita tu API key |
| **>1 año montado** | **NO está en Google Places** → **RUES** (fecha de matrícula) o Google Maps UI | ⏳ RUES gratis en datos.gov.co |

**Conclusión:** "Google Places" da reseñas pero **no** antigüedad. Se completan con **RUES**.

---

## 1. QUÉ API HABILITAR MAÑANA (paso a paso)

1. **Google Cloud Console** → crear un **proyecto** (ej. "seawolf-vigia").
2. **Habilitar "Places API (New)"** (APIs & Services → Library → buscar "Places API (New)" → Enable).
3. **Activar facturación** (Billing) en el proyecto — Google exige tarjeta para Places.
4. **Crear la API key** (APIs & Services → Credentials → Create credentials → API key).
   - **Restringirla** a "Places API (New)" (para que no la usen en otra cosa si se filtra).
5. **Presupuesto con alerta** (Billing → Budgets → alerta a, p.ej., $50 USD) para no llevarnos sorpresa.

**Lo que me pasas:** la API key → la guardo en el VPS en `madriguera.env`/`vigia.env` (600) y **jamás** viaja dentro de un entregable (doctrina del ejército).

---

## 2. CÓMO LA USAREMOS (por cada presa de OSM)

1. **Text Search** (Places API New) con `"<nombre> <ciudad> Colombia"` → devuelve `place_id`, `rating`, `userRatingCount`, `websiteUri`, `nationalPhoneNumber`.
2. Cotejo: si tiene `websiteUri` → se descarta (buscamos SIN web); si `rating >= 4.0` y `userRatingCount >= 10` → cuenta como ">80% positivas" (proxy honesto del promedio).
3. **Place Details** solo si hace falta más detalle (hasta 5 reseñas).

## 3. ANTIGÜEDAD (>1 año) — vía RUES

- **RUES / Cámara de Comercio** publica **fecha de matrícula** en **datos.gov.co** (API Socrata, gratis).
- Se cruza por **NIT o razón social** → si la matrícula tiene **>1 año**, pasa el filtro.

## 4. COSTO ESTIMADO (honesto)

- Places API (New): **Text Search ~$32 USD / 1.000** consultas; Place Details aparte.
- Con ~2.300 presas → orden de **$40-90 USD** para la primera pasada. Se mide y se cachea `place_id`.

## 5. ENTREGABLES LISTOS (en `/opt/vigia`)

- `vigia_osmp_v3.py` — barrido OSM (corriendo).
- `vigia_google.py` — enriquecimiento por Google Places (listo, esperando la key).
- `presas_CO.csv` — base cruda (sin web + teléfono).

## 6. ORDEN DE MAÑANA

1. Pegas la API key → la cargo en el VPS.
2. Lanzo `vigia_google.py` sobre las presas de OSM.
3. Cruce con RUES para antigüedad.
4. **Resultado:** presas que cumplen los 3 filtros (sin web + >1 año + >80% reseñas) → a La Madriguera → al Centro de Mando.

---

*"El sol no se tapa. Se apunta la sombra y se caza a plena luz."*
— Bellion, Gran Comandante del Ejército de Sombras
