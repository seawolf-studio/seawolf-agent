# PLAN — DIFERENCIACIÓN DE PLANTILLAS SEAWOLF (anti-Shopify)

**Fecha:** 2026-10-23 · **Autor:** Bellion (Gran Comandante) · **Pedido por:** Monarca (Key)
**Estado:** por ejecutar mañana · **Origen:** directriz del Monarca: *"que no se vean similares todas"*

---

## 1. EL PROBLEMA (por qué esto importa)
Si toda web Seawolf sale del mismo molde, pasa **exactamente lo que el Monarca odia de Shopify**: todas
las tiendas se ven iguales → el cliente no siente identidad propia → el Studio se percibe como
**fábrica de clones** y se comoditiza (guerra de precios).

> **Regla:** EL MOTOR es uno. **LA IDENTIDAD es de cada cliente.**

## 2. PRINCIPIO RECTOR — "un motor, N identidades"
La plantilla NO es el diseño: es el **motor**. El diseño se **genera** por cliente desde un archivo de tema.
La variación no se deja al azar ni a la mano: se **parametriza**.

## 3. ARQUITECTURA DE VARIACIÓN (4 capas)
| # | Capa | Qué define | Dónde vive |
|---|------|-----------|-----------|
| 1 | **Tokens de marca** | paleta (2-3 colores), tipografía (display+ui), radios, espaciado, sombras, densidad, tema por defecto | `temas/<cliente>.json` |
| 2 | **Variantes de sección** | ≥3 opciones por sección crítica (ver abajo) | biblioteca de componentes |
| 3 | **Selector de variantes** | qué variante usa cada sección: `hero:"collage", grid:"carrusel", promo:"banda"` | dentro del tema JSON |
| 4 | **Rasgo firma** | UN elemento único por cliente (textura, animación, ilustración) → el "sello" que nadie más tiene | por tema |

### Variantes mínimas a construir (≥3 cada una)
- **Hero:** imagen grande · carrusel de frases · collage/editorial · con video.
- **Cuadrícula de productos:** grid · carrusel horizontal · lista editorial · mosaico.
- **Promos:** banda · tarjetas · banner full-width · cuenta-regresiva.
- **Navegación:** superior · lateral · inferior (mobile-first).
- **Ficha de producto:** galería izquierda · full-bleed · editorial.

## 4. REGLA DE ORO (anti-clon)
Dos clientes distintos **NO** pueden compartir más de una fracción de la estructura visible.
**Checklist anti-Shopify** (marcar antes de entregar):
- [ ] ¿Tiene hero distinto (variante + copy + imagen)?
- [ ] ¿El orden de secciones es distinto?
- [ ] ¿El tono del copy es propio del rubro (no el genérico)?
- [ ] ¿Tiene al menos UN rasgo firma irrepetible?
- [ ] ¿La paleta/tipografía son del cliente (no las de Seawolf por defecto)?

## 5. EJECUCIÓN
1. Separar en la plantilla actual qué es **estructura** (se queda) y qué es **identidad** (se parametriza).
2. Crear `temas/<cliente>.json` + el generador `construir-web.py --tema <cliente>`.
3. Montar la biblioteca de variantes (empezar por hero + grid + promos).
4. Probar con **SNEAKER HOUSE** y un **segundo tema falso** → deben verse **claramente distintos**.
5. Documentar en la skill `seawolf-web-presence` (o crear `seawolf-plantillas-diferenciadas`).

## 6. LO QUE HAY QUE EVITAR (las señales de "clon")
Mismo hero · mismas secciones en el mismo orden · mismas tarjetas · mismo tono de copy · mismos colores.

**Fin del plan.**
