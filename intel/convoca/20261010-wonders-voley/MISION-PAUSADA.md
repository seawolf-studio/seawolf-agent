# MISIÓN PAUSADA — Smart Web «Club Deportivo Wonder's Voley»

**Estado:** ⏸️ PAUSADA por decisión de la cliente (Kennya) — retomar **a fin de temporada**.
**Motivo (textual del Monarca):** a Kennya le abrumó recibir una Smart Web en cuestión de días.
**Fecha de pausa:** 2026-10-10 · **Orquestador:** Bellion (Gran Comandante) · **Estudio:** Seawolf Studio.

---

## Qué quedó entregado (todo verificado en disco)

| # | Entregable | Sombra | Ruta |
|---|-----------|--------|------|
| 1 | Dossier de intel del club | Bellion | `INTEL-club-wonders.md` |
| 2 | Copy coloquial ES/EN | IGRIS | `igris/copy-wonders.md` |
| 3 | SEO + JSON-LD (España) | TUSK | `tusk/seo-wonders.md` |
| 4 | Sistema de diseño + tokens de tema | TITAN | `titan/design-system.json` |
| 5 | Capa IA (Cloudflare Worker + spec) | JIMA | `jima/worker.js`, `jima/smart-endpoint.md` |
| 6 | **Smart Web v1 (single-page)** | KAISEL | `kaisel/wonders-voley.html` |
| 7 | **Smart Web v2 (multipágina)** | KAISEL | `kaisel/wonders-voley-v2.html` |
| 8 | **Pieza autocontenida (logo embebido)** | Bellion | `kaisel/wonders-voley-ARCHIVO.html` |
| 9 | Auditoría adversarial (PASA 10/10) | BERU | `beru/auditoria.md` |
| 10 | PDF de requerimientos para la hermana | Bellion | `entrega-hermana/SOLICITUD-Wonders.pdf` |

## Las dos piezas clave para el retorno
- **`kaisel/wonders-voley-v2.html`** → la **desplegable**. Viaja CON su carpeta `kaisel/assets/`
  (`index.html` + `assets/img/logo.png`). 10 vistas con router, 9 formularios → `clubdeportivowonders@gmail.com`.
- **`kaisel/wonders-voley-ARCHIVO.html`** → la **autocontenida**. Logo embebido (base64). Un solo archivo,
  sin dependencias. Abre en cualquier navegador tal cual. **Respaldo maestro.**

## Cómo retomar (para cuando el Monarca diga «retomamos»)
1. Abrir `kaisel/wonders-voley-v2.html` (o la ARCHIVO) y refrescar con los datos de Kennya.
2. Soltar las fotos reales en `assets/img/` (los huecos están marcados con `[REEMPLAZAR: ./assets/img/...]`).
3. Publicar `index.html` + `assets/` en el **dominio temporal de Hostinger** → aprobación remota de Kennya.
4. Migrar a dominio propio en **Cloudflare** + desplegar el **Worker IA** (JIMA) y pegar su URL en `WONDERS_API_URL`.

## Pendientes del cliente (bloqueados por Kennya — todo listo para recibirlo)
Logo vectorial · fotos reales · nombres del cuerpo técnico · sede/dirección · tarifas · testimonios ·
año de fundación · dominio temporal · decisión WhatsApp (link) y FormSubmit vs endpoint propio.

## Notas técnicas para no perder nada
- **Formularios:** endpoint `https://formsubmit.co/ajax/clubdeportivowonders@gmail.com` (sin claves).
  El primer envío exige activación por correo (1 clic en la cuenta del club). Degrada a `mailto:`.
- **Blindaje:** contenido visible sin JavaScript (scoping `html.js` + `<noscript>` + red de seguridad).
- **Tema:** oscuro por defecto + claro. Paleta Wonder's negro/rojo/blanco (`#000000`/`#E60000`/`#FFFFFF`).
- **Prohibiciones respetadas:** sin Shopify, sin AdSense, sin burocracia Facebook/Meta.
- **Backups:** `kaisel/*.bak-pre-hardening`, `*.bak-pre-logo`, `*.bak-pre-png`.

## Integridad
Ver `HASHES.txt` (SHA-256 de las piezas clave, calculado al archivar).
