# IGRIS — SPEC DE COPYS GADO PARA LA TIENDA SEAWOLF (piloto + molde reutilizable)

> Autor: Igris (sombra de copywriting). Aprobado para inyección posterior en `products.json`.
> Alcance: generar copy que vende (GADO) para las 246 publicaciones del catálogo de `tienda-rosa`
> (`C:/Users/Admin/seawolf-store/dist/products.json`), en español colombiano coloquial, sin inventar datos
> y cumpliendo las reglas duras del estudio. El piloto (25 SKU) está en
> `C:/Users/Admin/seawolf-store/mantenimiento/copys-GADO-piloto.json`.

---

## 1. PROMPT REUTILIZABLE (para las 246 restantes, o para automatizar en el pipeline)

Copia este bloque por SKU. No lo edites a mano por producto: expón la misma plantilla y solo cambia los 5 campos de contexto.

```
Eres Igris, redactor de copywriting para e-commerce local en Colombia (tienda Seawolf).
Reglas no negociables: español colombiano coloquial, tuteo, frases cortas, voz activa,
cero relleno y cero jerga. Prohibido: publicidad pagada, Meta/Facebook/Instagram, Business
Manager, Pixel, Shopify, Google AdSense, "método secreto", "gratis de por vida", "hazte rico",
cero precio en el texto y cero promesas de resultado garantizado (sin "te curas",
"funciona al 100%", "adelgazas"). Si la descripción del producto no soporta un beneficio,
escribe literalmente "[FALTA INFO]" y NO inventes nada.

PRODUCTO:
  name:        [name del catálogo]
  description: [description cruda del catálogo, sin HTML]
  price:       [solo para calibrar angulo bajo/alto; NUNCA lo escribas en el copy]
  categorias:  [categorías reales del catálogo]
  ocasion:     [slug(s) de ocasión oficial de la tienda, ver §3]
  NIVEL_DE_CONCIENCIA_ASIGNADO: [A=1, B=2 o C=3 — usa §4]

Genera UN copy GADO (estructura §2) con estos campos exactos:
  - titulo:            rotulo max. 8 palabras.
  - ocasion:           array con el/los slug(s) oficial(es) que habla el idioma del copy.
  - nivel_conciencia:  int 1|2|3.
  - angulo:            el angulo elegido en una linea (una perspectiva de venta).
  - gancho:            primera linea que detiene el scroll.
  - agitacion:         el dolor, con empatia y sin culpar al cliente.
  - demostracion:      como el producto lo resuelve. BENEFICIOS, no caracteristicas.
  - orden:             llamada a la accion concreta (pago contraentrega / envio gratis).
  - whatsapp_prellenado: mensaje corto para el enlace de WhatsApp del producto.
  - pantalla:          rotulo max. 8 palabras para la ficha.
  - fuente_dato:       de donde salio la info (descripcion real) o [FALTA INFO].
```

Consumo programático (Python, para el pipeline):
```python
import json
prod = json.load(open('dist/products.json', encoding='utf-8'))
copys = json.load(open('mantenimiento/copys-GADO-piloto.json', encoding='utf-8'))
# fusionar por sku: prod[k]['copy'] = copys[k]
for p in prod:
    if p['sku'] in copys:
        p['copy'] = copys[p['sku']]
with open('dist/products.json','w',encoding='utf-8') as f:
    json.dump(prod, f, ensure_ascii=False, indent=2)
```

---

## 2. REGLAS DE ESTILO DEL ESTUDIO (no negociables)

- **GADO en orden:** Gancho → Agitación → Demostración → Orden. Nada se relanza por detrás.
- **Primero el dolor, después el producto.** Si no se identifica un dolor con palabras del
  cliente, el copy no existe.
- **Un solo CTA por pieza** (el campo `orden`). Más de uno y no es copy, es texto.
- **Ritmo:** frases cortas. Voz activa. Cero relleno, cero jerga ("soluciones integrales", "líderes del sector").
- **Español colombiano coloquial, tuteo.** Ej: "pedí", "escribinos" → preferir "pide", "escríbenos";
  "llevalo", "pidelo". Natural, de WhatsApp.
- **Titulo y pantalla: máximo 8 palabras.**
- **Cero precio en el copy ni en la imagen:** se captura la intención; el número se negocia
  en el chat. Mal visto mostrar cifra antes de conversar (lección §4.4 del manual).
- **Fuente de datos:** cada afirmación debe salir de la `description` real del catálogo.
  Lo verificable se escribe; lo que no, `[FALTA INFO]`.

### PROHIBICIONES DURAS
| Prohibido | Ejemplo de QUE NO escribir |
|---|---|
| Publicidad pagada / plataformas | "anuncios pagados", "publicidad", "impulsado por…" |
| Meta / Facebook / Instagram / Business Manager / Pixel | cualquier mención |
| Shopify / Google AdSense | cualquier mención |
| Promesas de salud o cura | "te curas", "elimina la enfermedad", "funciona al 100%", "adelgazas" |
| Resultados garantizados | "color garantizado", "resultado asegurado" (sin respaldo del catálogo) |
| Precio en el copy | "solo $20.000", "cuesta poco" con cifra |
| Frases vedadas | "método secreto", "gratis de por vida", "hazte rico" |
| Inventar datos | escribir beneficios no soportados por la descripción |

Productos de belleza/salud (tintes, copa menstrual, parches, blanqueadores, fajas, EMS):
nunca citar dolencias ni curas. Hablar de "apoyo", "favorece", "cuida", "rutina diaria".
Quedan fuera los dientes de curar, los alivios garantizados y los milagros estéticos.

---

## 2.5 REGLA ORTOGRÁFICA OBLIGATORIA (no negociable)

Todo copy que salga de este spec (piloto y los 246 restantes) cumple:

(a) **Ortografía completa:** cada texto sale con sus tildes (`más`, `día`, `fácil`,
    `información`…) y con los signos de apertura y cierre (`¿…?`, `¡…!`). Un copy sin
    tildes se lee pobre y resta credibilidad; se corrige antes de publicar, nunca después.

(b) **Normalización obligatoria antes de inyectar:** antes de fusionar el copy en
    `dist/products.json` se corre
    `python mantenimiento/normalizar_copys.py <json-de-copys> --dry-run`
    y su reporte DEBE quedar en **`SOSPECHOSAS SIN RESOLVER = 0`** y los **`AMBIGUOS`
    revisados a mano** (confirmar `esta/estas` por contexto antes de publicar). El
    renglón `CORREGIDAS: n` por sí solo NO basta (ronda 5 cerró ese agujero: el chequeo
    de `SOSPECHOSAS` es **independiente del diccionario** y marca palabras sin tilde
    que el diccionario ni conoce — p. ej. `pagina`—, así que un "listo para inyectar"
    con `SOSPECHOSAS > 0` es imposible: el script lo bloquea y devuelve exit 1). El
    modo real del script corrige en sitio y deja respaldo `.bak`.

(c) **Qué NO se normaliza** (identificadores): la clave `sku` del producto y los slugs del
    array `ocasion` (`san-valentin`, `dia-madre`, `regreso-clases`, `black-friday`) se
    quedan EXACTAMENTE como están. El script ya los respeta; la regla es que ningún paso
    de la cadena los toque.

El diccionario del normalizador es palabra-completa (límites de palabra): nunca corrige
dentro de otra palabra ("masaje", "oscuras") y nunca toca homógrafos ambiguos de forma
ciega ("pago" sustantivo vs "pagó" verbo, "esta" determinante vs "está" verbo) — esos
quedan listados para revisión humana, no se reemplazan a ciegas.

---

## 3. CONEXIÓN AL PIPELINE DE MANTENIMIENTO

Estado actual (verificado 2026-10-13):
- `products.json` usa `name`, `description`, `short_description`, `price`, `categories`, `tags`, `slug`.
- La ficha `src/pages/producto/[sku].astro`.render() muestra `product.description` (bloque) y
  `product.short_description` (destacados). El botón WhatsApp usa `wa.me/573000000000?text=...encodeURIComponent(product.name)`.
- El filtro por ocasión en `catalogo.astro` usa `p.tags?.includes(occParam)` — **y ningún
  producto tiene `tags`**. Las ocasiones (navidad, san-valentín, día-madre, black-friday,
  regreso-clases, verano, aniversario) existen en `src/data/occasions.json` y en el hero,
  pero NO filtran nada hoy: volver una ocasión = 0 productos.
  → **BLOQUEANTE de la tienda** mientras `tags` siga vacío. Arreglo obligatorio al inyectar
  el copy: poblar `tags` de cada producto con los slugs de `copy.ocasion` (punto 4 abajo).

### Qué hay que tocar para inyectar el copy

0. **Normalización ortográfica (regla §2.5):** correr
   `mantenimiento/normalizar_copys.py` sobre el JSON de copys hasta que el reporte dé
   **`SOSPECHOSAS SIN RESOLVER = 0`** y **`AMBIGUOS` revisados a mano** ANTES de
   fusionar (el `CORREGIDAS: n` solo no basta — ver §2.5b). Sin eso, no se inyecta.

1. **Nuevo campo `copy` (objeto) en cada producto** de `products.json` (ver consumidor en §1).
   No se sobreescribe `description` ni `short_description` (el proveedor te reescribe esos
   campos en cada sync; el `copy` es tuyo y sobrevive).

2. **Ficha `src/pages/producto/[sku].astro`:** si `product.copy` existe, renderizarlo como
   la descripción principal en lugar de `product.description`:
   - `gancho` como primera línea (negrita/lead de la ficha).
   - `agitacion` + `demostracion` como cuerpo (2-3 párrafos cortos).
   - `orden` como CTA debajo del bloque (además del botón "Añadir al carrito").
   - `pantalla` como fallback del `<title>` si es más corto que `name`.
   - El enlace WhatsApp: reemplazar `encodeURIComponent(product.name)` por
     `encodeURIComponent(copy.whatsapp_prellenado)`.
   - Guarda `name` intacto: es el identificador del proveedor; el `copy.titulo` es solo
     para la tarjeta/título si se desea.

3. **Tarjeta de producto** (`components/ProductGrid.astro`): opcionalmente mostrar
   `copy.pantalla` como título de la tarjeta (no toca el SEO del `<h1>` de la ficha si
   el `name` se mantiene en `alt`/`title` del enlace).

4. **Ocasiones en el catálogo (desbloquea el filtro muerto):** para que `?occ=navidad`
   realmente filtre, hay que poblar `tags` de cada producto con el/los slug(s) de ocasión
   de su `copy.ocasion` en el MISMO paso de inyección (punto 1). Es el arreglo del
   **BLOQUEANTE**: `tags` vacío hoy = toda ocasión devuelve 0 productos.
   `copy.ocasion` es la fuente de la verdad del idioma de ocasión; el tag lo vuelve operativo.

---

## 4. CRITERIOS PARA ELEGIR NIVEL DE CONCIENCIA Y ÁNGULO

### 4.1 Nivel de conciencia (del manual §4.1 — Schwartz; práctico: A/B/C)
Usa estas 5 preguntas:
1. ¿El comprador ya sabe que la *categoría* existe y la busca activamente? (ej: audífonos bluetooth) → 2.
2. ¿Es un producto que la persona *desconoce que existe* hasta que lo ve? (ej: estimulador EMS, cactus que canta, organizador zapatos) → 1.
3. ¿Es una compra de impulso barata donde decide en segundos, ya convencido del problema? (ej: ganchos a $19.900, cepillo $3.600) → 3.
4. ¿Es ticket alto donde comparan marca/foto antes de confiar? → 2 (diferenciar tu oferta: envío gratis, contraentrega).
5. Primera misión de un producto: empezar en 1 o 2; atacar a 3 recién cuando hay datos de que el público caliente existe (regla del manual: empezar por A, más audiencia).

En el piloto: 8 en nivel 1 (novelty o desconocido), 17 en nivel 2. Cero en nivel 3 por doctrina.

### 4.2 Ángulo según ocasión y tipo de producto
Un mismo producto tiene varios ángulos (manual §4.5). Regla: **un ángulo por copy**. Elegir así:

| Ocasión oficial (slug) | El idioma que habla el copy | Angulo sugerido |
|---|---|---|
| `navidad` | regalo que sorprende, "lo van a recordar" | regalo con historia / el que nadie más tiene |
| `san-valentin` | detalle para consentir(se) | regalo romántico / auto-mimo |
| `dia-madre` | cuidar y agradecer | ritual de cuidado personal |
| `black-friday` | precio justo, "aprovechá ahora" (sin cifra) | ahorro oportuno |
| `regreso-clases` | organización y practicidad | listo antes del primer día |
| `verano` | salidas y frescura | batería extra / cuidar la piel invisible |
| `aniversario` | celebrar el momento | regalo simbólico y elegante |

Regla de negocio: si el producto sin ocasión natural (abrillantador de llantas, copa menstrual,
bandas de gimnasia), poner `"ocasion": []` — el copy habla del dolor cotidiano, no de la fecha.

Para **pack** (ticket muy bajo, < ~15.000 COP): el ángulo es "llevá varios" — resolver el dolor
en cantidad sin citar precio ("a este precio llevátelo sin riesgo", "cambia el tuyo con varios").
Para **ticket alto** (> ~150.000 COP): cerrar con "envío gratis" (el umbral de la tienda) y
reforzar que se paga contraentrega — baja el riesgo percibido, no se negocia la cifra.

---

## 5. COBERTURA DEL PILOTO (verificada)

- 25 SKU, todos existentes en `dist/products.json` (comprobado contra el catálogo).
- Categorías reales cubiertas por inferencia de producto: Belleza, Salud, Cocina, Tecnología,
  Hogar, Bienestar, Vehículos, Natural Home, Aseo, Bisutería, Moda, Deportes, Bebé, Juguetería, Mascotas (15).
  — Caveat: la mayoría de los productos del catálogo están SIN `categories` en la data; el tag de
    categoría literal solo coincide en 12 de las 13 registradas. "Deportes" quedó cubierto por
    inferencia (bandas y maletín de mancuernas) pero no por tag real en el catálogo.
- 3 ticket bajo (pack): CO-0016, CO-0028, CO-0029.
- 3 ticket alto: 716, PO002, 0006.
- Ocasiones usadas: solo slugs oficiales; las 7 representadas (navidad, san-valentín, día-madre,
  black-friday, regreso-clases, verano, aniversario).
- Un producto con información insuficiente (TILAPIA, descripción basura "1111…") marcado
  `[FALTA INFO]` en `demostracion` y `fuente_dato` — no inventé.