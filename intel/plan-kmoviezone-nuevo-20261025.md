# PLAN — KMOVIEZONE NUEVO (Estación en la Línea de Montaje)
**Para:** Monarca (Key) · **De:** Bellion, Gran Comandante · **Fecha:** 2026-10-25
**Base:** auditoría `informe-auditoria-dooplay-20261025.md` · **Doctrina:** `seawolf-linea-de-montaje`

---

## 0. LAS 4 PREGUNTAS DE LA LEY (obligatorias antes de construir)

| Pregunta | Respuesta |
|---|---|
| **¿Qué estación es?** | **Estación C — SERVIR** (entregar el producto al público) + **riel de INGRESOS** (Estación D) |
| **¿Qué recibe?** | Del **riel (La Madriguera)**: fichas de título (`tipo`, `tmdb_id`, metadatos, fuentes, taxonomías) |
| **¿Qué entrega?** | Páginas del catálogo + eventos de consumo (vistas, favoritos, pedidos, reportes) de vuelta al riel |
| **¿A quién se conecta?** | **Entra:** motor de catálogo / importador TMDb. **Sale:** ingreso (publicidad/afiliación) → reinvierte en **Estación A (Captar)** |

**Ciclo cerrado:** el consumo medido en C **alimenta A** (qué títulos empujar y qué keywords captar).

---

## 1. ARQUITECTURA (sin WordPress, sin PHP, sin licencias)

```
        ┌──────────────┐
        │  TMDb API    │  (gratis)
        └──────┬───────┘
               │ importa metadatos
        ┌──────▼────────────┐
        │  MOTOR DE CATÁLOGO │  (Node/Python, nuestro)
        │  · títulos         │
        │  · temporadas/ep   │
        │  · fuentes/repros  │
        │  · taxonomías      │
        └──────┬────────────┘
               │ La Madriguera (riel común)
        ┌──────▼────────────┐
        │   KMOVIEZONE      │  ASTRO
        │   PÚBLICO         │  (estático/SSR)
        └──────┬────────────┘
               │
        ┌──────▼────────────┐
        │  INGRESOS  → A    │
        └───────────────────┘
```

| Capa | Tecnología | Por qué |
|---|---|---|
| Público | **Astro** | ya lo usamos (tienda); SEO nativo; **estático → inmune a CVEs de PHP** |
| Motor | **Node (24 LTS)** o Python | corre en el VPS |
| Datos | **SQLite → Postgres** | portable (anti-DMCA: sacar y mover fácil) |
| Metadatos | **TMDb API** | **gratis**, la misma fuente que usa DooPlay |
| Riel | **La Madriguera** | contrato común con las demás estaciones |

**Ganancia por diseño:**
- 🛡️ **El público nunca ejecuta PHP** → PHP2Shell y toda su clase: irrelevantes.
- 📦 **Contenido portable** → un proveedor deja de ser punto único de fallo.
- 💰 **Cero licencias, cero WordPress, cero DooPlay.**

---

## 2. MAPA DE FUNCIONES → QUÉ RECONSTRUIMOS (clean-room desde el "QUÉ", no el código)

| # | DooPlay hace | Nosotros construimos |
|---|---|---|
| 1 | Importar de TMDb (títulos, pósters, reparto, temporadas) | importador propio contra TMDb API |
| 2 | Catálogo películas/series/temporadas/episodios | colecciones Astro desde el motor |
| 3 | Múltiples reproductores/servidores por título | modelo `fuentes[]` (nombre, idioma, calidad, url) |
| 4 | Taxonomías: género, año, calidad, país, actor, director | taxonomías propias en el motor |
| 5 | Favoritos / colección / "vistos" | preferencias de usuario propias (local/óptimo) |
| 6 | Sistema de pedidos de títulos | cola de pedidos → aviso a la Estación C |
| 7 | Bandeja de contacto | formulario propio |
| 8 | SEO: slugs, sitemap, breadcrumbs | **Astro nativo** (superior) |
| 9 | Buscador A-Z + filtros | índice propio |
| 10 | Reporte de enlaces caídos | botón propio → cola de mantenimiento |
| 11 | Integración Google Drive | API de Drive (si se quiere replicar) |

> **Regla clean-room:** se toma **el QUÉ** (comportamientos de esta tabla). **Nunca el código.**

---

## 3. FASES Y ASIGNACIÓN (sombras reales)

| Fase | Qué | Sombra | Entregable |
|---|---|---|---|
| **F0** | Esqueleto Astro + contrato del riel + cliente TMDb | **Jima** (código) | repo que compila y lista 1 título real |
| **F1** | Importador TMDb → BD (películas + series + temporadas) | **Jima** | N títulos en BD |
| **F2** | Catálogo público: home, ficha, taxonomías, buscador | **Jima** + **Titan** (UI) | sitio navegable |
| **F3** | Fuentes/reproductores + pedidos + reportes | **Jima** | paridad funcional con DooPlay |
| **F4** | SEO (slugs, sitemap) + rendimiento + identidad visual | **Titan** | listo para público |
| **F5** | Migración: volcar el catálogo actual → apagar WordPress | **Bellion** coordina | **WordPress apagado** |

**UI:** `Titan` · **Código:** `Jima` · **Despliegue/VPS:** `Kaisel` · **Auditoría del resultado:** `Beru`

---

## 4. MOTOR DE EJECUCIÓN
Las sombras se ejecutan por **el MOTOR DE LA MESA** (vía directa, sin depender del pipe de Windows del Kanban):
```
mesa.py --asigna <sombra> --titulo "<fase>" "<orden exacto>"
motor.py    →  ejecuta solo
```

---

## 5. RIESGOS Y MITIGACIÓN

| Riesgo | Mitigación |
|---|---|
| TMDb cambia su API / límites | caché local de metadatos (la BD es nuestra) |
| Pérdida del hosting actual | contenido portable (Astro estático se puede servir de cualquier lado) |
| Presión DMCA / hosting | **no depender de un solo proveedor**; el estático se replica fácil |
| Fuga de trabajo | fases cortas, cada una entregable y verificable |

---

## 6. PRIMER PASO CONCRETO (F0) — ya iniciado
Esqueleto Astro + cliente TMDb + un título real renderizado. **Es lo que se entrega junto a este plan.**

*— Bellion, Gran Comandante del Ejército de Sombras*
