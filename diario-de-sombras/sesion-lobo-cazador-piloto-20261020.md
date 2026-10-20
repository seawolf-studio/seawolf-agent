# 🐺 DIARIO DE LAS SOMBRAS — Sesión: PILOTO LOBO CAZADOR + ASISTENTE SMARTWEB + SW-ST.NET V2
**Fecha:** 2026-10-20 (madrugada) · **Comandante:** Bellion · **Monarca:** Key

---

## 1. LOBO CAZADOR — CACERÍA A ESCALA (Google Maps / Playwright)
- **Decisión del Monarca:** opción **B** (scraper Maps gratis). Regla de filtrado final: **≥80% positivas = `rating ≥ 4.0`** + **ranking por nº de reseñas** + **sin web** + **no cerrado**. Quien no cumpla, se descarta ("no nos juntamos con perdedores").
- **Estado:** scraper `vigia_maps_v4.py` corriendo sobre las **19.037 presas** (resumible). Muestra: ~**564 prometedoras** sobre ~2.100 procesadas.
- **Límite honesto:** la vista limitada de Maps **NO expone el nº de reseñas** (verificado hasta en HTML y JSON-LD) → **el ranking por reseñas queda pendiente** (vías: API de tercero, o rankear por rating mientras).

## 2. PILOTO — 10 SMARTWEBS PERSONALIZADAS
- **Tarifa APROBADA:** **COP 250.000/mes**. **Trial APROBADO:** **7 días**. Entrega: **ZIP del bloque HTML**. Dominios temporales: aleatorios.
- **Generador:** `gen_piloto_v3.py` → 10 SmartWebs (una por sector), cada una con **asistente IA con NOMBRE propio**: Roma (Floristería Roma) · Tinta (Litografía) · Nido (El Nido) · JJ (Bicicletas J.J) · Turbo (AutoSport) · Estilo (Outfit Store) · Herby (Herby PC) · Tecno (Tecnodrywall) · Ultra (Ultrapan) · Visión (OptiSalud del Valle).
- **Desplegadas VIVAS** en el VPS con **token aleatorio** por demo: `https://agente.sw-st.net/d/<token>.html`.

## 3. ESTÁNDAR DE FÁBRICA SMARTWEB (NO NEGOCIABLE) — grabado en skill `seawolf-web-presence`
Toda SmartWeb para cliente nace con: 🌗 **modo claro/oscuro (oscuro por defecto)** · ✍️ **tipografía Arvo** · 🤖 **asistente IA** (modelo en backend) · 📎 **pie con firma + "SmartWeb powered by Seawolf Studio" + © derechos reservados + QR**.

## 4. BACKEND DEL ASISTENTE (VPS) — VIVO
- **Endpoint:** `https://agente.sw-st.net/asistente` · servicio systemd `asistente.service` · `/opt/asistente/app.py` (solo stdlib).
- **Modelos:** primario **`nvidia/nemotron-3.5-lightning:free`** → fallback **`deepseek/deepseek-v4.1-flash`**(economico).
- **Hallazgo clave:** ambos son de **razonamiento** → devolvían `content: null`. Fix: **`reasoning: {enabled: false}`** → respuestas limpias. Probado end-to-end (Ultrapan y OptiSalud respondieron especializado). Rate-limit por IP + CORS `*`.
- **Key:** leída de `/root/.hermes/.env` → volcada a `/root/asistente.env` (chmod 600).

## 5. SW-ST.NET V2 — MEJORADA Y CON CEREBRO
- **Investigación** exhaustiva de webs espectaculares (principios, elementos, tendencias 2026, Core Web Vitals, chat proactivo) → `intel/investigacion-webs-espectaculares-20261020.md`.
- **`sw-st.net-v2.html`** (original intacto): asistente incrustado que **perfila para la venta** y **SALE SOLO** (11 s / scroll >55% / exit-intent) con saludo + chips de perfilado. Añadidos `canonical`, `theme-color`, `robots`. Reveal ya era robusto (`html.js .reveal`).
- **Bloqueado:** publicar en el dominio real `sw-st.net` — **no resuelve** (ni local ni VPS) y **no hay credenciales de Cloudflare** en el VPS. **Sitio VIVO de prueba:** `https://agente.sw-st.net/sitio/`.

## 6. COMMITS
`3cc7cc7` (backend asistente) · `201e91a` (sw-st.net-v2 + investigación) · `d91048b` (estándar de fábrica v2) · `73294a9` (generador piloto) · repo `seawolf-agent` branch master, HEAD==origin.

## 7. PENDIENTES (para la próxima jornada)
1. **Publicar** la v2 en `sw-st.net` (requiere acceso Cloudflare del Monarca o subida manual).
2. **Dominios aleatorios reales** para los demos (requiere wildcard DNS `*` — hoy van por token en path).
3. **Ranking por nº de reseñas** (fuente pendiente).
4. **Disparar el primer contacto** del piloto (email-first, 7 días, 250.000/mes).
5. **Lighthouse** sobre la v2 + prueba social real cuando cierre el 1er cliente.

---
*"El lobo recuerda. El lobo no olvida."* — Bellion, Gran Comandante.
