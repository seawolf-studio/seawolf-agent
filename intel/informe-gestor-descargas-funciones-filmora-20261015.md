# INFORME — Gestor de Descargas, Funciones Deseadas y Filmora vs Alternativas
## + Novedades de SEAWOLF TOOLS v4

**Fecha:** 2026-10-15 (cierre del día) · Uso Interno — Seawolf Studio · Bellion para el Monarca (Key)

---

## 0. SEAWOLF TOOLS v4 — lo que se agregó hoy ✅ (probado)

| Función pedida | Estado |
|----------------|--------|
| **🗺️ Mapa de espacios** | ✅ pestaña nueva: agrupa el peso por carpeta raíz de cada disco, en bloques proporcionales |
| **🛠️ Mantenimiento programado EDITABLE** | ✅ pestaña nueva: activar/desactivar, editar **días** y **horario**, y **"Ejecutar"** ahora. Tareas: Temporales viejos · Logs de Hermes · Vaciar Papelera |
| **🔎 Botón REA** | ✅ pestaña nueva: ruta + [App JS/Electron] o [Binario] → corre REA y devuelve la **Evidence sellada** |

*(Además: multi-disco, pesados, duplicados, papelera reversible — ya estaban.)*
Config del mantenimiento: `intel/seawolf-manten.json`. Lanzador: `SeawolfTool.bat`.

---

## 1. GESTOR DE DESCARGAS — qué hacen MiPony y JDownloader (y nuestro plan)

### 1.1 JDownloader (el "todoterreno")
- **Link Grabber:** pegas N enlaces → detecta el hoster, los archivos y sus tamaños.
- **Cola con prioridades**, pausa/reanudar, **límite de ancho de banda**.
- **Reconnect:** cambia la IP para saltar límites de espera.
- **Auto-extracción** de RAR/ZIP + **lista de contraseñas**.
- **Programador** (descargar/parar a ciertas horas), **monitor del portapapeles**.
- **Multi-conexión por archivo**, reanudación, **plugins para cientos de hosters**, integración con el navegador (Click'n'Load).

### 1.2 MiPony (el "multi-nube")
- **Todas tus nubes en una ventana** (Drive, OneDrive, Dropbox, Mega…).
- **Transferencia entre nubes gratis e ilimitada**; de enlace → nube.
- **Explorador de dos paneles**, **renombrado masivo**, **crear enlaces para compartir**, pausar/reanudar, **extraer RAR** antes de subir.

### 1.3 Nuestro plan para Seawolf Tools (Gestor de Descargas)
1. **Link Grabber** (pegar N enlaces → cola con tamaño detectado).
2. **Cola con prioridades**, pausa/reanuda, **límite de banda**.
3. **Motor multi-conexión** (aria2 es open-source; o multipart propio).
4. **Auto-organización por tipo** al terminar (Video/Audio/Docs/Instaladores/Comprimidos) → encaja con el **Gestor de Descargas** del Top 10.
5. **Programador** (descargar en horario) — se integra con el Mantenimiento.
6. **Auto-extracción** y **post-proceso** (mover/comprimir).
7. **Integración con el optimizador** (lo descargado entra al escaneo).

---

## 2. FUNCIONES QUE LOS USUARIOS PIDEN (investigación, cualquier programa)

**En editores de video** (reseñas G2/Capterra + YouTube de Filmora):
facilidad/sin curva · plantillas y efectos listos · **subtítulos automáticos** · IA (texto→video, quitar fondo, mejorar) · **velocidad/rendimiento** · **sin suscripción** · interfaz limpia + atajos · **estabilidad** (que no crashee) · biblioteca integrada · export multi-plataforma · modo oscuro.

**En utilidades/optimizadores de PC** (foros, alternativas, reseñas):
**velocidad de escaneo** · **seguridad** (que NO rompa el sistema) · **sin publicidad** · **portable** (sin instalar) · **un clic** · **informes** · **programación** · **papelera reversible** · duplicados **por hash** (no por nombre) · **alertas de disco**.

→ **Regla que saco:** la gente perdona funciones; **no perdona que la herramienta los dañe o los bombardee con ads.** Nuestro diferencial: **seguro + reversible + sin ruido.**

---

## 3. FILMORA — funciones y quién lo iguala/supera

### 3.1 Qué hace Filmora 16
Línea de tiempo multitrack · **análisis IA de video** · edición basada en texto · **subtítulos automáticos** · corrección de color · limpieza de audio · grabación de pantalla · **IA generativa** (texto→video, imagen→video, AI Extend) · **máscara y recorte inteligente** · **motion tracking** · **2,9M+ recursos** stock · plantillas · **planificador social** · embellecer rostro · mejorar video.

### 3.2 Alternativas open-source (verificadas hoy)
| Repo | ★ | Licencia | Rol |
|------|---|----------|-----|
| **OpenCut-app/OpenCut** | 94.772 | **MIT** ✅ | **la alternativa open-source a CapCut** — nuestro caballo |
| **harry0703/MoneyPrinterTurbo** | 131.703 | **MIT** ✅ | video corto desde texto con IA (ya nuestro) |
| **Zulko/moviepy** | 14.989 | **MIT** ✅ | edición de video con Python (motor) |
| **WyattBlue/auto-editor** | 5.529 | Unlicense ✅ | "edición sin esfuerzo" (quita silencios, etc.) |
| mifi/lossless-cut | 44.606 | GPL-2.0 | corte sin recodificar (swiss army) |
| mltframework/shotcut | 15.432 | GPL-3.0 | editor completo |
| olive-editor/olive | 9.135 | GPL-3.0 | editor no lineal |
| OpenShot/openshot-qt | 6.633 | GPL | editor clásico |
| KDE/kdenlive | 5.871 | GPL-3.0 | editor potente |
| obsproject/obs-studio | 77.594 | GPL-2.0 | grabación/streaming |

**Veredicto:** para **nuestro producto** (cero copyleft) → **OpenCut (MIT) + MoviePy (MIT) + MoneyPrinterTurbo (MIT)**. Los GPL (Shotcut/Kdenlive/Olive/OpenShot/OBS) sirven como **herramientas internas** o referencia, **no embebidos**.

**Complemento gratis para el día a día:** `mifi/lossless-cut` (cortar sin recodificar) y `auto-editor` — ambos **gratis** y muy útiles, aunque GPL/Unlicense.

---

## 4. FUENTES
- GitHub API (todas las fichas verificadas) — 2026-10-15.
- filmora.wondershare.com (features) · jdownloader.org · mipony.net · alternative.me · reseñas G2/Capterra.

**Fin del informe — cierre del día.**
