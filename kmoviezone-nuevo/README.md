# kmoviezone-nuevo

Reconstrucción **clean-room** del sitio, sin WordPress y sin PHP.
**Estación C (Servir)** de la Línea de Montaje Seawolf. Riel: **La Madriguera**.

## Por qué
El sitio anterior corría **WordPress + DooPlay (nulled) sobre PHP/Apache**.
Riesgos: la clase entera de CVEs de PHP (p. ej. PHP2Shell CVE-2026-109618/109619, CVSS 9.2),
código de procedencia dudosa y sin actualizaciones. El público, en cambio, solo necesita ver catálogo.

## Cómo
```
TMDb (gratis) → motor propio → Astro (público, ESTÁTICO)
```
**Estático = el público nunca ejecuta PHP** → inmune a esa clase de fallos.

## Arranque
```bash
npm install
cp .env.example .env      # y pon tu TMDB_API_KEY (https://www.themoviedb.org/settings/api)
npm run dev               # http://localhost:4321
npm run build             # genera dist/
```
Sin `TMDB_API_KEY` el sitio **compila igual** y muestra la **muestra local** (`src/data/fixture.json`).

## Estructura
| Ruta | Qué |
|---|---|
| `src/lib/riel.js` | **contrato del riel** (La Madriguera) |
| `src/lib/tmdb.js` | cliente TMDb (clave en `.env`) |
| `src/layouts/Base.astro` | layout + identidad (oscuro por defecto) |
| `src/pages/index.astro` | catálogo |
| `src/pages/titulo/[id].astro` | ficha de título |

## Fases (ver `intel/plan-kmoviezone-nuevo-20261025.md`)
F0 esqueleto ✅ · F1 importador · F2 catálogo · F3 fuentes/pedidos · F4 SEO · F5 migración y apagado de WordPress.

## Regla
**Clean-room**: se reconstruye *el qué* (comportamientos). **Nunca se copia el código de DooPlay.**
