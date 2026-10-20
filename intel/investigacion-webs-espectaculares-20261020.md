# 🔎 INVESTIGACIÓN — WEBS ESPECTACULARES (2026)
### Base para mejorar sw-st.net · compilada por Bellion para el Monarca
**Fecha:** 2026-10-20

---

## 1. PRINCIPIOS (lo que NO cambia con las modas)

1. **Un objetivo por página.** Si un elemento no sirve a la conversión, se corta. ("Anti-diseño" intencional.)
2. **Propuesta de valor en 5 segundos.** El héroe dice qué haces, para quién y qué gana el visitante — sin jerga.
3. **Confianza visible.** Prueba social, testimonios, logos, señales de seguridad, contacto real.
4. **Cero fricción.** Formularios cortos, un CTA claro y repetido, camino obvio al siguiente paso.
5. **Móvil primero** (no "responsive"): diseñado para el pulgar, no una versión encogida.

## 2. ELEMENTOS DE UNA WEB QUE "ESPECTACULA"

- **Héroe con jerarquía brutal:** titular grande, subtítulo, 1-2 CTAs. Tipografía oversized como ancla visual.
- **Motion narrative (storytelling por scroll):** la página se cuenta a medida que bajas (parallax, reveal, escenas).
- **Micro-interacciones con propósito:** hover, botones que reaccionan, contadores que suben, feedback inmediato. "La página se siente viva".
- **Tipografía cinética:** texto que anima al scroll/interacción.
- **Profundidad y 3D:** WebGL/parallax con capas para dar inmersión (con cuidado de no ahogar el rendimiento).
- **Espacio en blanco intencional:** menos ruido, más foco.

## 3. TENDENCIAS 2026 (dónde va la ola)

- **Personalización por IA** y **contenido dinámico** por comportamiento.
- **CSS scroll-driven animations** nativas (más ligeras que JS).
- **Accesibilidad como estándar** (contraste, teclado, lectores, `prefers-reduced-motion`).
- **Sostenibilidad / peso** — páginas rápidas = menos energía y mejor conversión.
- **Retrofuturismo / maximalismo** como estéticas de nicho (no para todas las marcas).

## 4. RENDIMIENTO (Core Web Vitals — requisito, no lujo)

- Anima con **CSS/JS ligero**, nunca bloquees el render; **lazy-load** de imágenes/medios.
- Evita *layout shift*: reserva espacio para lo que carga tarde.
- Degradación elegante en equipos débiles; respeta `prefers-reduced-motion`.

## 5. IA EN LA WEB (nuestro diferencial)

- **Chat proactivo (mejores prácticas):** sale solo **en el momento correcto** (tiempo en página, scroll profundo, intención de salida) con un **saludo útil** ("¿te ayudo a encontrar algo?"). HubSpot: el chat en vivo bien temporizado sube conversión **hasta ~20%**.
- **Perfilado de venta:** el asistente no solo responde — **pregunta** (qué negocio, qué dolor) y **guía** al producto y al siguiente paso.
- **Triggers recomendados:** (a) ~10-15 s en página, (b) scroll >55%, (c) exit-intent (mouse hacia arriba). No saturar: un solo intento.

---

## 6. APLICADO A sw-st.net — auditoría y acciones

| Hallazgo | Acción |
|----------|--------|
| Ya tiene héroe, partículas, terminal, i18n, reveal, modo claro/oscuro | ✅ Conservar (base sólida) |
| **Faltaba capa IA** (el diferencial) | ✅ **Asistente proactivo incrustado** (endpoint real) |
| **Sin salida proactiva** | ✅ Sale solo a los 11 s / scroll >55% / exit-intent y **perfila para la venta** |
| Reveal robusto (`html.js .reveal`) ya correcto | ✅ Sin cambios (no hay riesgo de "página en negro") |
| Faltaban `canonical` y `theme-color` | ✅ Añadidos |
| Prueba social / testimonios visibles | ⏳ **Pendiente** (necesita casos reales — llegan con el piloto) |
| Core Web Vitals medibles | ⏳ Pendiente: medir con Lighthouse y optimizar imágenes/medios |
| Personalización dinámica del héroe | ⏳ Opcional (fase 2) |

---

## 7. LO QUE SIGUE (propuesta)

1. **Medir** la página con Lighthouse (rendimiento, accesibilidad, SEO) y aplicar correcciones.
2. **Prueba social real:** cuando el piloto cierre 1-2 clientes, subir testimonio + caso.
3. **Micro-interacciones extra** donde aporten conversión (no decoración).
4. **A/B del saludo proactivo** (mensaje y timing) para exprimir el ~20% de conversión.

*"La web no es un folleto: es el primer lobo de la manada que recibe al visitante."* — Bellion
