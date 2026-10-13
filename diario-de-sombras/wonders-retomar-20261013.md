# MEMENTO — Retomar «Smart Web Wonder's Voley» cuando Kennya se comunique
**Proyecto:** Smart Web del Club Deportivo Wonder's Voley (Madrid) — negocio de **Kennya**, hermana del Monarca.
**Estado:** ⏸️ PAUSADO por la cliente hasta fin de temporada. **Todo el trabajo está hecho y respaldado** — solo falta su luz verde y sus datos.
**Orquestador:** Bellion · **Estudio:** Seawolf Studio · **Pausa:** 2026-10-10 · **Handoff:** 2026-10-13.

---

## 🚦 Cómo actuar en cuanto Kennya escriba (checklist)
1. **Abrir** `kaisel/wonders-voley-v2.html` (la desplegable) o `wonders-voley-ARCHIVO.html` (la autocontenida).
2. **Reemplazar los huecos `[REEMPLAZAR: …]`** con los datos reales del club (fotos, cuerpo técnico, sede, tarifas, testimonios, año).
3. **Soltar las fotos** en `kaisel/assets/img/`.
4. **Publicar** `index.html` + `assets/` en el **dominio temporal de Hostinger** → aprobación remota de Kennya.
5. **Migrar a Cloudflare** + desplegar el **Worker IA (JIMA)** y pegar su URL en `WONDERS_API_URL`.
6. Decidir: **link de WhatsApp** en contacto y **FormSubmit vs endpoint propio**.

## 📦 Entregables (verificados en disco) — `seawolf-agent/intel/convoca/20261010-wonders-voley/`
| # | Entregable | Ruta |
|---|---|---|
| 1 | Intel del club | `INTEL-club-wonders.md` |
| 2 | Copy coloquial ES/EN (IGRIS) | `igris/copy-wonders.md` |
| 3 | SEO + JSON-LD España (TUSK) | `tusk/seo-wonders.md` |
| 4 | Sistema de diseño + tokens (TITAN) | `titan/design-system.json` |
| 5 | Capa IA — Cloudflare Worker (JIMA) | `jima/worker.js`, `jima/smart-endpoint.md` |
| 6 | Smart Web v1 (single-page) | `kaisel/wonders-voley.html` |
| 7 | **Smart Web v2 (multipágina, 10 vistas, 9 formularios)** | `kaisel/wonders-voley-v2.html` |
| 8 | **Pieza autocontenida (logo embebido, respaldo maestro)** | `kaisel/wonders-voley-ARCHIVO.html` |
| 9 | Auditoría adversarial (PASA 10/10) | `beru/auditoria.md` |
| 10 | PDF de requerimientos a la hermana | `entrega-hermana/SOLICITUD-Wonders.pdf` |
| — | Conclusiones / doctrina Smart Web | `CONCLUSIONES-smart-web-wonders.md` |

## 🔑 Lo esencial para el retorno
- **Desplegable:** `kaisel/wonders-voley-v2.html` **con su carpeta** `kaisel/assets/` (`index.html` + `assets/img/logo.png`). 10 rutas con router, 9 formularios → **`clubdeportivowonders@gmail.com`**.
- **Autocontenida (maestra):** `kaisel/wonders-voley-ARCHIVO.html` — un solo archivo, logo en base64, abre en cualquier navegador. **No perder.**
- **Hash de control (SHA-256):** ARCHIVO `6aef7161…4c7a67` · v2 `209ffc8f…26ec85` · v1 `cb4bfecb…9df3c` (ver `HASHES.txt`).
- **Respaldo:** `Seawolf_Bunker/archivo/wonders-voley/wonders-voley-20261010.tar.gz`.

## ⛔ Bloqueado por la cliente (todo listo para recibirlo)
Logo vectorial · fotos reales · nombres del cuerpo técnico · sede/dirección · tarifas · testimonios · año de fundación · **dominio temporal Hostinger** · decisión de WhatsApp y de método de formulario.

## ☎️ Datos del club (recabados, públicos)
Email `clubdeportivowonders@gmail.com` · WhatsApp `+34 614 696 077` · inscripción vía `app.cluber.es` · lema "Talento, equipo y valores". Colores: **negro predominante, rojo, blanco**.

## ✨ Oportunidad de ampliación (nueva capacidad)
Ya tenemos **Kaelen** (avatar presentador) y HyperFrames → a Wonder's se le puede ofrecer después un **video de bienvenida** o un **Smart Course deportivo**. Guardar como upsell natural.

---
*Memento de retorno generado por Bellion · evidencia o no existe.*
