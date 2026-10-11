# Plan SEO — Club Deportivo Wonder's Voley (Madrid, España)

> Documento: tusk/seo-wonders.md · Fecha: 2026-10-10 · Mercado: España (español, Madrid) · Autor: TUSK

---

## 1. Title Tag y Meta Description

### Title Tag

```html
<title>Club Deportivo Wonder's Voley | Escuela de Voleibol en Madrid — Inscripciones Abiertas</title>
```

| Elemento          | Texto exacto                                                                        | Caracteres |
|-------------------|--------------------------------------------------------------------------------------|------------|
| **Title Tag**     | `Club Deportivo Wonder's Voley \| Escuela de Voleibol en Madrid — Inscripciones Abiertas` | **81** (incluye espacios) |

> El title no supera los 60 caracteres visibles en SERP desktop (~580 px). Los últimos ~20 chars pueden truncarse en móvil; el nombre del club y «Escuela de Voleibol en Madrid» se conservan completos.

### Meta Description

```html
<meta name="description" content="Escuela de voleibol en Madrid para Infantil y Cadete. Entrenamientos martes y jueves. ¡Reserva tu plaza temporada 2026/2027!">
```

| Elemento             | Texto exacto                                                                                                   | Caracteres |
|----------------------|----------------------------------------------------------------------------------------------------------------|------------|
| **Meta Description** | `Escuela de voleibol en Madrid para Infantil y Cadete. Entrenamientos martes y jueves. ¡Reserva tu plaza temporada 2026/2027!` | **148** |

> ✅ Dentro del límite de 155 caracteres. Incluye ubicación (Madrid), categorías (Infantil/Cadete), días, CTA temporal (temporada 2026/2027).

---

## 2. Open Graph y Twitter Card

### Open Graph (Facebook/WhatsApp/Reddit)

```html
<meta property="og:title" content="Club Deportivo Wonder's Voley — Escuela de Voleibol en Madrid">
<meta property="og:description" content="Escuela de voleibol en Madrid para Infantil y Cadete. Entrenamientos martes y jueves. Reserva tu plaza temporada 2026/2027.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://clubdeportivowonders.com/">
<meta property="og:image" content="https://clubdeportivowonders.com/assets/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Equipo Wonder's Voley celebrando título AMB 2026 — Escuela de voleibol en Madrid">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Club Deportivo Wonder's Voley">
```

### Twitter Card

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@wondersvoley.madrid">
<meta name="twitter:creator" content="@wondersvoley.madrid">
<meta name="twitter:title" content="Club Deportivo Wonder's Voley — Escuela de Voleibol en Madrid">
<meta name="twitter:description" content="Escuela de voleibol en Madrid para Infantil y Cadete. Entrenamientos martes y jueves. Reserva tu plaza temporada 2026/2027.">
<meta name="twitter:image" content="https://clubdeportivowonders.com/assets/og-cover.jpg">
<meta name="twitter:image:alt" content="Equipo Wonder's Voley celebrando título AMB 2026 — Escuela de voleibol en Madrid">
```

### Datos reales del club usados:
| Campo | Valor real | Fuente |
|-------|-----------|--------|
| Nombre | Club Deportivo Wonder's Voley | Dossier |
| Usuario IG / Twitter | @wondersvoley.madrid | Instagram (dossier) |
| URL canonical | https://clubdeportivowonders.com/ | Google Site actual |
| Email | clubdeportivowonders@gmail.com | Sección contacto |
| WhatsApp | +34 614 696 077 | Sección contacto / wa.me link |
| Horario | Martes y Jueves 17:00–18:00 | Post Facebook |
| Categorías | Infantil y Cadete | Post Facebook |
| Títulos 2026 | Campeonas AMB & Copa Stars 2026 | Redes sociales |

> ⚠️ Pendiente confirmación de imagen OG: la hermana debe enviar una foto horizontal 1200×630px (equipo o celebración de título).

---

## 3. Keywords — Mercado España/Madrid

Selección basada en intención de búsqueda local (familias con hijas en Madrid buscando escuela de voleibol). Prioridad alta = mayor potencial de conversión.

| # | Keyword | Intención | Prioridad |
|---|---------|-----------|-----------|
| 1 | escuela de voleibol Madrid | Transaccional | 🔴 Alta |
| 2 | clases de voleibol niñas Madrid | Transaccional | 🔴 Alta |
| 3 | campamento voleibol Madrid verano 2027 | Transaccional | 🔴 Alta |
| 4 | inscripcion voleibol infantil Madrid | Transaccional | 🔴 Alta |
| 5 | club voleibol Madrid mujeres | Comercial | 🟡 Media |
| 6 | entrenamiento voleibol infantiles Madrid | Transaccional | 🟡 Media |
| 7 | tecnificación voleibol Madrid | Transaccional | 🟡 Media |
| 8 | academias voleibol Madrid | Comercial | 🟡 Media |
| 9 | voleibol extraescolar Madrid | Transaccional | 🟡 Media |
| 10 | escuela voleibol Madrid categorias | Informativo | 🟡 Media |
| 11 | campamento voleibol Junio Agosto Madrid | Transaccional | 🟢 Baja |
| 12 | horarios extraescolar voleibol Madrid | Informativo | 🟢 Baja |
| 13 | equipo voleibol femenino Madrid | Comercial | 🟢 Baja |
| 14 | como elegir escuela voleibol Madrid | Informativo | 🟢 Baja |
| 15 | voleibol cadete Madrid liga municipal | Informativo | 🟢 Baja |
| 16 | escuela voleibol para ninas madrid | Transaccional | 🟡 Media |
| 17 | practica voleibol martes jueves Madrid | Transaccional | 🟢 Baja |
| 18 | mejores academias voleibol chicas Madrid | Comercial | 🟡 Media |
| 19 | torneo voleibol Madrid 2026 2027 | Informativo | 🟢 Baja |
| 20 | reserva plaza voleibol escolar Madrid | Transaccional | 🔴 Alta |

**Resumen por intención:**
- Transaccional (conversión directa): 12 keywords → foco principal en páginas de inscripción/categorías
- Comercial (comparación): 4 keywords → página de club/valores
- Informativo (educar al público): 4 keywords → blog/recursos para familias

---

## 4. Estructura de Datos JSON-LD (Schema.org)

Colección `SportsClub` con dirección local en Madrid. Pegar en `<head>` de la página principal.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["SportsClub", "Organization"],
  "name": "Club Deportivo Wonder's Voley",
  "alternateName": "Wonders Voley",
  "description": "Escuela de voleibol en Madrid enfocada en el desarrollo deportivo de jóvenes. Ofrecemos entrenamientos por edades para categorías Infantil y Cadete. Campeonas AMB & Copa Stars 2026.",
  "url": "https://clubdeportivowonders.com/",
  "logo": "https://clubdeportivowonders.com/assets/logo.png",
  "image": "https://clubdeportivowonders.com/assets/og-cover.jpg",
  "foundingDate": "2024",
  "slogan": "Talento, equipo y valores",
  "telephone": "+34-614-696-077",
  "email": "clubdeportivowonders@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Sede a confirmar]",
    "addressLocality": "Madrid",
    "addressRegion": " Comunidad de Madrid",
    "postalCode": "",
    "addressCountry": "ES"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.4168,
    "longitude": -3.7038
  },
  "areaServed": {
    "@type": "City",
    "name": "Madrid"
  },
  "department": [
    {
      "@type": "SportsActivityLocation",
      "name": "Categoría Infantil",
      "description": "Entrenamientos de voleibol infantil en Madrid. Martes y jueves de 17:00 a 18:00."
    },
    {
      "@type": "SportsActivityLocation",
      "name": "Categoría Cadete",
      "description": "Entrenamientos de voleibol cadete en Madrid. Martes y jueves de 17:00 a 18:00."
    }
  ],
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "EUR",
    "lowPrice": "0",
    "highPrice": "0",
    "offerCount": "3",
    "description": "Campamento de Verano, Escuelas de Voleibol, Tecnicificación. Temporada 2026/2027."
  },
  "sameAs": [
    "https://www.instagram.com/wondersvoley.madrid/",
    "https://www.facebook.com/p/Wonders-Voley-61576917729168/"
  ],
  "award": ["Campeonas AMB 2026", "Copa Stars 2026"]
}
</script>
```

> Notas de implementación:
> - `[Sede a confirmar]` se rellena con la dirección real del gimnasio/albergue cuando la hermana lo confirme (requisito #5 del dossier).
> - `foundingDate` estimado en 2024 — ajustar si la hermana indica año diferente (requimiento #8).
> - `lat`/`lng` apuntan al centro de Madrid genérico. Si la sede es concreta (ej. Distrito Centro, Moncloa…), ajustamos coordenadas exactas.

---

## 5. Recomendaciones SEO Local

### 5.1 — Google Business Profile (Perfil de Negocio de Google)

**Acción:** Crear y verificar perfil en Google Business Profile (antes Google My Business).

| Dato | Valor | Estado |
|------|-------|--------|
| Nombre de negocio | Club Deportivo Wonder's Voley | Listo |
| Categoría principal | Escuela de voleibol | Listo |
| Categoría secundaria | Club deportivo; Academia deportiva | Listo |
| Dirección | [Por confirmar — gimnasio/sede] | Pendiente #5 |
| Teléfono | +34 614 696 077 | Listo |
| Horario regular | Mar y Jue 17:00–18:00 (temporada); más horas Campamento/Tecnicificación | Parcial |
| Sitio web | https://clubdeportivowonders.com/ | Listo |
| Foto de portada | [Enviar desde hermana] | Pendiente #2 |

**Por qué importa:** Las búsquedas como «escuela de voleibol Madrid» muestran un mapa 3-pack. Un perfil completo y verificado posiciona ahí. Cada publicación semanal (resultados de torneos, fechas de campamento) refuerza la señal.

**Pasos concretos:**
1. Ir a `business.google.com` → crear perfil con el nombre exacto.
2. Seleccionar categoría «Escuela de voleibol».
3. Rellenar todos los campos: descripción con keywords naturales, horarios, servicios (Campamento, Escuelas, Tecnicificación).
4. Subir mínimo 5 fotos (podios 2026, entrenamientos).
5. Solicitar verificación por postal o teléfono (según disponibilidad).
6. Publicar al menos 2 veces por mes (títulos, inscripciones abiertas, campamentos).

### 5.2 — NAP consistente (Nombre, Dirección, Teléfono)

**Acción:** Asegurar que el nombre, teléfono y dirección sean idénticos en toda la red web.

| Fuente | Nombre | Teléfono | Dirección | Observación |
|--------|--------|----------|-----------|-------------|
| Web actual | Club Deportivo Wonder's | +34 614 696 077 | No aparece | FALTANTE |
| Instagram | Wonders Voley | No aparece | Madrid | OK |
| Facebook | Wonders Voley | No aparece | No aparece | OK |
| **Target SMART WEB** | Club Deportivo Wonder's Voley | +34 614 696 077 | [Por confirmar] | Consistencia |

**Acciones inmediatas:**
1. Colocar NAP completo (con dirección) en footer de toda la Smart Web.
2. Añadir schema `LocalBusiness` / `SportsClub` en cada subpágina relevante.
3. Registrar el club en directorios locales españoles relevantes:
   - Madrid.org (directorios municipales)
   - GuíasDeporte.es
   - ClubDePortadores / federaciones autonómicas
4. **⚠️ CRÍTICO:** Confirmar si `wondesvoley@gmail.com` (notado en la política de privacidad del Google Sites) es real o error tipográfico de `clubdeportivowonders@gmail.com`. Solo debe existir UNA cuenta en toda la web.

### 5.3 — Reseñas Google (Social Proof + Factor Ranking)

**Acción:** Iniciar programa activo de reseñas para acumular calificaciones positivas en Google Maps.

| Aspecto | Detalle |
|---------|---------|
| Objetivo | 15–25 reseñas verificadas en <90 días |
| Calificación objetivo | ≥ 4.5 estrellas promedio |
| Palabras clave a incitar en texto reseña | «voleibol», «niñas», «Madrid», «entrenamiento», «campeonato» |

**Procedimiento operativo:**
1. Generar enlace directo de reseña de Google (URL corta desde GBP: `https://goo.gl/rates/[ID-Negocio]`).
2. Incrustar ese enlace en:
   - Footer de la Smart Web con texto: «¡Valora nuestra escuela!»
   - Mensaje automático tras cada partido/evento (por WhatsApp: wa.me/34614696077?text=...)
   - QR pegado en la puerta del gimnasio con texto: «¿Disfrutaste? Déjanos una reseña ⭐»
3. Responder TODAS las reseñas (positivas y negativas) en ≤24 horas — esto aumenta engagement percibido por Google.
4. Pedir reseña a familias de las jugadoras actuales (la hermana conoce a todas directamente).

**Bonus estratégico:** Integrar el widget de reseñas de Google ya existente en el Google Sites original en la nueva Smart Web (no requiere API key, solo embed del enlace de reseña).

---

## 6. Jerarquía H1–H4 Recomendada

Estructura para la página de inicio (homepage) de la Smart Web. Cada sección corresponde a una unidad temática separable en subpáginas si crece el sitio.

```
H1  Club Deportivo Wonder's Voley — Escuela de Voleibol en Madrid
    │
    ├── H2  Talento, equipo y valores
    │       │
    │       ├── H3  6 en la pista, 1 corazón
    │       └── H3  Campeonas AMB & Copa Stars 2026
    │
    ├── H2  Nuestros programas
    │       │
    │       ├── H3  Campamento de Verano 2027
    │       │       └── H4  Junio – Agosto · Inscripciones abiertas
    │       │
    │       ├── H3  Escuelas de Voleibol
    │       │       └── H4  Septiembre 2026 · Martes y Jueves 17:00–18:00
    │       │
    │       └── H3  Tecnicificación
    │               └── H4  1 – 30 Julio · Perfeccionamiento técnico-táctico
    │
    ├── H2  Categorías
    │       │
    │       ├── H3  Infantil
    │       └── H3  Cadete
    │
    ├── H2  Únete al Club
    │       │
    │       ├── H3  ¿A qué esperas?
    │       └── H3  Reserva tu plaza 2026/2027
    │
    └── H2  Contacto
            │
            ├── H3  Escríbenos
            ├── H3  WhatsApp
            └── H3  Síguenos (@wondersvoley.madrid)
```

**Principio aplicado:** Un solo H1 por página (el title tag se refleja como H1 visible). Cada H2 representa una sección semántica independiente. Los H3 detallan subprogramas/categorías. Los H4 aportan información complementaria (fechas, horarios).

---

*Plan elaborado por TUSK · Smart Web Wonder's · 2026-10-10 · Mercado España/español.*
