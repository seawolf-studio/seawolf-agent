# ⚔️ ARMAS DE JIMA — EL VIGÍA (descubrimiento de presas)
### Seawolf Studio · arsenal verificado contra el VPS
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)

---

## 0. RECONOCIMIENTO DEL VPS (verificado hoy)

| Pieza | Estado |
|-------|--------|
| Python **3.12.3** | ✅ |
| Node **v22** + `/opt/node24` | ✅ |
| Docker **29.6** | ✅ |
| Claves **OPENROUTER_API_KEY** + **GROQ_API_KEY** | ✅ |
| **La Madriguera** (Postgres, `madriguera-postgres`, puerto 5440) | ✅ montada |
| Chromium / Playwright | ❌ por instalar |
| API key **Google Maps/Places** | ❌ no existe |

---

## 1. LAS TRES RUTAS A GOOGLE MAPS

| Ruta | Descripción | Costo / ToS | Veredicto |
|------|-------------|-------------|-----------|
| **A · Google Places API (New)** | Vía **oficial**. Devuelve nombre, dirección, **teléfono**, web, rating y nº de reseñas | Requiere **API key de Google Cloud + billing** | El arma fuerte (necesita tu key) |
| **B · Scraper de Maps** (navegador headless: Playwright) | Extrae listados navegando Maps | Gratis, **viola ToS**, riesgo de bloqueo/CAPTCHA | Último recurso |
| **C · OpenStreetMap / Overpass API** | Datos abiertos, **gratis y legal** (ODbL) | Sin key, sin riesgo; cobertura variable | **Punto de partida recomendado** |

**Recomendación:** C primero (primera ola gratis y legal) + A en paralelo (profundidad), B solo si no hay key.

---

## 2. ARSENAL POR FUNCIÓN

### Descubrimiento (Vigía)
| Arma | Para qué |
|------|----------|
| **Overpass API (OpenStreetMap)** | barrido de negocios por ciudad/categoría; nombre, dirección, a veces teléfono/web |
| **Google Places API** | Mapas oficial: incluye **teléfono** y reseñas |
| **Playwright + Crawlee (Node)** | scraping de Maps (ruta B) y motor de enriquecimiento |
| **RUES / Cámara de Comercio (datos abiertos)** | empresas formales de Colombia |
| **Páginas Amarillas / directorios sectoriales** | barridos por nicho |

### Enriquecimiento (Acechador)
| Arma | Para qué |
|------|----------|
| Crawler del sitio propio | ¿tiene web? ¿es responsive? ¿velocidad? |
| Detección de tecnología | con qué está hecho |
| Detección de **WhatsApp Business** | señal clave en Colombia |
| Extracción de email/teléfono | desde la página de contacto |
| Scraper de reseñas (Google) | ¿atiende su reputación? |

### Almacenamiento
- **La Madriguera (Postgres)** — toda presa se escribe al riel (esquema PIEZA).

### Cerebro / orquestación
- **OpenRouter** — clasificar y cualificar (scoring).
- **Groq** — transcripción de audio cuando aplique.

---

## 3. LO QUE FALTA MONTAR

1. **Playwright + Chromium** en el VPS (no hay chrome de sistema) → `playwright install --with-deps chromium`.
2. **(Opcional) API key de Google Cloud con Places API + billing** → la habilita el Monarca.
3. Un **contenedor/venv de Jima** con las dependencias del scraper.

---

## 4. PRIMERA OLA (plan de ataque)

1. Instalar Playwright + Chromium (y un venv/contenedor para Jima).
2. **Barrido C (OSM/Overpass)** sobre una ciudad objetivo → 100-200 negocios crudos → La Madriguera.
3. **Enriquecimiento** de los primeros 20 (sitio propio → email + señales de dolor).
4. **Scoring** → semáforo → primeras CALIENTES listas para FOCO TOTAL.
5. (Si el Monarca habilita la key) encender la ruta A para teléfonos/reseñas.

---

## 5. HONESTIDAD

- **Scraping de Maps = viola ToS.** Preferir OSM + Places API.
- **Google Places cuesta** por request → usar con presupuesto y caché de `place_id`.
- **Emails en frío** necesitan dominio calentado (warm-up) ANTES de volumen — eso es fase aparte.

---

*"Primero reconoce el terreno gratis y legal. Después paga por lo que de verdad vale."*
— Bellion, Gran Comandante del Ejército de Sombras
