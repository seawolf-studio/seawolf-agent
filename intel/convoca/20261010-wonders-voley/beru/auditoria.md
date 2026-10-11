# AUDITORIA ADVERSARIAL — Smart Web Club Deportivo Wonder's Voley

**Auditor:** Beru, Supervisor del Ejercito de Sombras  
**Artefacto:** `kaisel/wonders-voley.html` (2674 lineas, 106 KB)  
**Fecha:** 2026-10-10  
**Estandar:** Verificacion forense con comando y salida real. Veredicto binario: PASA o NO PASA.

---

## TABLA DE VERIFICACION

| # | Requisito | Ruta / Verificacion | Veredicto | Hallazgo |
|---|-----------|---------------------|-----------|----------|
| 1 | Archivo autocontenido | grep `rel="stylesheet"` + grep `script src=` | **PASA** | 0 CSS externo no-font, 0 script externo. Solo Google Fonts (permitido). |
| 2 | Tema oscuro + toggle + localStorage | grep `data-theme` + grep `localStorage` | **PASA** | `data-theme="dark"` en linea 2. localStorage `wonders_theme` (linea 2385). Toggle funcional (linea 2401). |
| 3 | Paleta Wonder's sin colores prohibidos | grep `#0A0A0C` + conteo de HEX | **PASA** | `#0A0A0C`: 0 matches. Negro `#000000` (7), rojo `#E60000` (2), blanco `#FFFFFF` (24). |
| 4 | Meta description ≤155 chars | python `len()` sobre contenido | **PASA** | **124 caracteres** (limite: 155). |
| 5 | Open Graph + Twitter Card + JSON-LD | parseo JSON-LD con `json.loads()` | **PASA** | OG completo (10 tags). Twitter Card completo (7 tags). JSON-LD valido (SportsClub+Organization). |
| 6 | Sin claves API ni secretos | grep `sk-or-`, `OPENROUTER`, `api_key`, `Bearer` | **PASA** | 0 matches en todos los patrones. `max_tokens: 600` (linea 2598) es parametro de API, no secreto. |
| 7 | prefers-reduced-motion | grep `prefers-reduced-motion` | **PASA** | CSS: linea 217 (`@media`). JS: lineas 2460-2461 (`matchMedia` + early return). |
| 8 | i18n ES/EN completo | conteo `data-i18n` vs `TRANSLATIONS` keys | **PASA** | 119 claves HTML = 119 ES = 119 EN. Cobertura 100% bidireccional. |
| 9 | Responsive con media queries | grep `@media` | **PASA** | 8 media queries: 6x `max-width:768px`, 1x `max-width:375px`, 1x `prefers-reduced-motion`. |
| 10 | Widget chat WONDERS_API_URL sin credenciales | grep `WONDERS_API_URL` + grep credenciales | **PASA** | Constante declarada (linea 2160), valor vacio `''`. Sin credenciales expuestas. Fallback graceful implementado (linea 2573). |

---

## EVIDENCIA POR PUNTO

### 1. Archivo autocontenido

```bash
$ grep -n 'link.*rel="stylesheet"' wonders-voley.html
99:  <link href="https://fonts.googleapis.com/css2?family=...display=swap" rel="stylesheet" />

$ grep -n 'script.*src=' wonders-voley.html
(sin resultado — exit code 1: no matches)
```

CSS externo no-font: 0. Scripts externos: 0. Todo el CSS incrustado en `<style>` (lineas 104-1520). Todo el JS incrustado en `<script>` (lineas 2151-2672).

### 2. Tema oscuro por defecto con toggle y localStorage

```bash
$ grep -n 'data-theme' wonders-voley.html
2:<html lang="es" data-theme="dark">          # <-- default oscuro
120:    [data-theme="dark"] { ... }           # variables oscuras
132:    [data-theme="light"] { ... }          # variables claras
2394:  document.documentElement.setAttribute('data-theme', theme);  # toggle

$ grep -n 'localStorage' wonders-voley.html
2384:let currentLang = localStorage.getItem('wonders_lang') || 'es';
2385:let currentTheme = localStorage.getItem('wonders_theme') || 'dark';  # default='dark'
2397:  localStorage.setItem('wonders_theme', theme);  # persistencia
2410:  localStorage.setItem('wonders_lang', lang);
```

Toggle funcional via `toggleTheme()` (linea 2401). Boton con aria-label "Cambiar tema" (linea 1547).

### 3. Paleta Wonder's sin colores prohibidos

```bash
$ grep -n '#0A0A0C\|#0a0a0c' wonders-voley.html
(sin resultado — exit code 1)

# Conteo de colores Wonder's:
#000000 / #000 (negro): 7 matches (backgrounds, hero, footer)
#E60000 (rojo): 2 matches (--accent-red, gradientes)
#FFFFFF / #fff (blanco): 24 matches (texto, fondos, bordes)
```

Paleta declarada en `:root` (lineas 106-117): `--primary-black: #000000`, `--accent-red: #E60000`, `--neutral-white: #FFFFFF`. Adicionalmente `--seawolf-*` presente pero no obligatorio para este requisito.

### 4. Meta description — conteo exacto de caracteres

```python
desc = 'Escuela de voleibol en Madrid para Infantil y Cadete. Entrenamientos martes y jueves. ¡Reserva tu plaza temporada 2026/2027!'
len(desc) == 124  # PASA (limite: 155)
```

### 5. Open Graph, Twitter Card y JSON-LD

**Open Graph** (lineas 16-25): `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:image:width`, `og:image:height`, `og:image:alt`, `og:locale`, `og:site_name` — 10 tags.

**Twitter Card** (lineas 28-34): `twitter:card=summary_large_image`, `twitter:site`, `twitter:creator`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt` — 7 tags.

**JSON-LD** (lineas 37-94): Valido. `json.loads()` exitoso.
```json
{
  "@context": "https://schema.org",
  "@type": ["SportsClub", "Organization"],
  "name": "Club Deportivo Wonder's Voley",
  ...
  "award": ["Campeonas AMB 2026", "Copa Stars 2026"]
}
```

### 6. Sin claves ni secretos

```bash
$ grep -ni 'sk-or-\|OPENROUTER_API_KEY\|api_key\|Bearer' wonders-voley.html
(sin resultado — exit code 1)

$ grep -ni 'secret\|token\|password\|passwd' wonders-voley.html
2598:        max_tokens: 600,     # <-- parametro de API (modelo), NO secreto
```

El unico hit (`max_tokens`) es un parametro de configuracion de modelo LLM, no una credencial. WONDERS_API_URL esta vacio (`''`), sin valor hardcodeado.

### 7. prefers-reduced-motion

```
CSS (linea 217):
  @media (prefers-reduced-motion: reduce) {
    .reveal { opacity: 1; transform: none; transition: none; }
    * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }

JS (lineas 2460-2461):
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
```

CSS desactiva todas las animaciones y transiciones. JS aborta el IntersectionObserver (scroll reveal) si el usuario prefiere movimiento reducido.

### 8. i18n ES/EN

```python
# Conteo exacto:
html_keys = 119  # data-i18n unicos en el HTML
es_keys = 119    # claves en TRANSLATIONS.es
en_keys = 119    # claves en TRANSLATIONS.en

# Diferencia ES-EN: conjunto vacio
# Diferencia EN-ES: conjunto vacio
# Claves huerfanas (HTML sin traduccion): 0
# Claves huerfanas (traduccion sin uso en HTML): 0
```

Cobertura 100% bidireccional. El objeto TRANSLATIONS contiene bloques `es` (lineas 2167-2285) y `en` (lineas 2287-2378) con las mismas 119 claves cada uno. La funcion `setLang()` (linea 2408) itera sobre `[data-i18n]` y aplica `textContent`.

### 9. Responsive con media queries

```bash
$ grep -n '@media' wonders-voley.html
217:    @media (prefers-reduced-motion: reduce) { ... }
395:    @media (max-width: 768px) { ... }    # navbar -> burger
669:    @media (max-width: 768px) { ... }    # quienes-grid -> 1 col
863:    @media (max-width: 768px) { ... }    # cat-grid -> 1 col
1202:   @media (max-width: 768px) { ... }    # contacto-grid -> 1 col
1283:   @media (max-width: 768px) { ... }    # footer-grid -> 1 col
1512:   @media (max-width: 375px) { ... }    # micro-phone
1517:   @media (max-width: 768px) { ... }    # inscripcion-steps
```

8 media queries en total. Breakpoints: 375px (telefonos pequenos) y 768px (tablets/moviles). Comportamiento: grid de 2 columnas colapsa a 1 columna, navbar links se ocultan y aparece burger, hero actions se apilan vertical.

### 10. Widget chat — WONDERS_API_URL

```bash
$ grep -n 'WONDERS_API_URL' wonders-voley.html
2160:const WONDERS_API_URL = '';  // placeholder, URL del Worker pendiente
2573:  if (!WONDERS_API_URL) { ... }   // fallback graceful
2591:    const res = await fetch(WONDERS_API_URL, { ... });

$ grep -nci 'bearer\|token\|key\|secret' wonders-voley.html
# Solo "max_tokens: 600" (parametro de modelo, no secreto)
```

WONDERS_API_URL declarado como constante en el ambito global (linea 2160). Valor actual: string vacio. El codigo implementa fallback graceful: si no hay URL, envia mensaje con datos de contacto alternativos (WhatsApp/email). La llamada fetch no incluye headers de autenticacion, solo `Content-Type: application/json`. El modelo `qwen/qwen3.8-flash` esta en otra constante (`CHAT_MODEL`, linea 2161), tambien sin exponer secretos.

---

## RESUMEN DE HALLAZGOS

### Falsos cumplimientos detectados
**Ninguno.** Todas las verificaciones pasan con evidencia real.

### Observaciones (no bloqueantes)

1. **WONDERS_API_URL vacio**: El Worker de Cloudflare no esta desplegado aun. El fallback es correcto, pero el chat IA no funcionara hasta que se configure la URL. Esto es intencional segun el comentario en linea 2158.

2. **Open Graph / Twitter Card: URLs no verificables en vivo**: Las URLs de imagenes (`og:image`, `twitter:image`) apuntan a `https://clubdeportivowonders.com/assets/og-cover.jpg`. El archivo probablemente no existe aun (dominio y assets pendientes de despliegue). Esto no es un fallo del HTML en si, pero debe verificarse en produccion.

3. **JSON-LD `streetAddress`**: Contiene placeholder `[Sede a confirmar]`. Valido estructuralmente pero semantico debil hasta que se reemplace.

4. **Placeholders en equipo y testimonios**: Varios `[PENDIENTE: nombre]`, `[REEMPLAZAR: foto...]`. Marcados correctamente con comentarios. No afectan funcionalidad.

5. **`tel:` con digitos enmascarados** (linea 2008): `tel:+346****6077`. El enlace no funcionara como llamada telephonica. El numero completo si esta visible en el texto del channel-value (linea 2012).

---

## VEREDICTO GLOBAL

**PASA — 10/10 puntos verificados con evidencia real.**

El archivo `wonders-voley.html` es un single-page autocontenido, con tema oscuro por defecto y toggle funcional, paleta Wonder's correcta, SEO completo (meta description 124 chars, Open Graph, Twitter Card, JSON-LD valido), sin secretos expuestos, animaciones respetuosas con prefers-reduced-motion, i18n ES/EN con cobertura 100%, responsive con 8 media queries, y widget de chat con WONDERS_API_URL como constante sin credenciales.

---

*Auditoria forense ejecutada por Beru, Supervisor del Ejercito de Sombras. Ningun veredicto emitido sin comando y salida real que lo respalde.*