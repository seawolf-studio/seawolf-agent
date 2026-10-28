# LÍNEA DE MONTAJE KMOOVIEZONE v2 — diagrama definitivo
**Seawolf Studio · 27 de octubre de 2026 · Bellion (Gran Comandante)**

---

## 1. El diagrama

```
╔══════════════════════════════════════════════════════════════════════╗
║   KMOOVIEZONE — LÍNEA DE MONTAJE v2      Seawolf Studio · 27-oct-26  ║
╚══════════════════════════════════════════════════════════════════════╝

  [1] ENLACES ─────────────────────────────────────────────── SUYO
       │   MediaFire (a mano)
       │   ↓  se pegan en  cola-enlaces.txt  (multi-cajón, con "===")
       ▼
  [2] MIPONY ──────────────────────────────────────────────── SUYO
       │   descarga + extrae   (.rar  →  VIDEO)
       │   ⚠  MiPony CERRADO antes de encolar
       │   ↓  H:\caida\
       ▼
  [3] ReNamer  ★★ LA PIEZA QUE FALTABA ───────────────────── SUYO
       │   NOMBRE CANÓNICO EN MASA
       │   • Película  →  Título (Año).mkv
       │   • Serie     →  Título SxxExx.mkv
       │   ↓  el MISMO nombre sirve a la web Y a Jellyfin
       ▼
  [4] VIDCODER ───────────────────────────────────────────── SUYO
       │   preset "seawolf 1080p"
       │   → mp4 maestro: 1080p · audio latino · subtítulos forzados
       │   ↓  E:\wwe\
       ▼
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
  ┌─────────┐      ┌───────────┐      ┌──────────────────┐
  │ [5A]    │      │ [5A]      │      │ [5B]             │
  │ SERVIDORES (4) │ ...       │      │ DRIVE  ( I: )    │
  │         │      │           │      │                  │
  │streamtape│      │ vidmoly  │      │ → JELLYFIN       │
  │  voe     │      │ mixdrop  │      │   (premium)      │
  └────┬────┘      └───────────┘      └──────────────────┘
       │              ↑                      ↑
       │        EN PARALELO, no en serie       │
       │        (1 transferencia c/u)         │
       ▼                                      ▼
  [6] COSECHADOR ─────────────────────────────────────────── MÍO
       │   lee el log de FileUploader  →  fila del catálogo
       │   • Serie      → 1 fila con capítulos
       │   • Película   → 1 fila POR película
       ▼
  [7] PUBLICAR ───────────────────────────────────────────── MÍO
       │   build.py  →  datos.json  →  subir.py (FTPS cifrado)
       ▼
  [8] VERIFICAR ──────────────────────────────────────────── MÍO
       │   curl al sitio VIVO  (nunca fiarse del FTP)
       ▼
     ✅ kmoviezone.stream actualizado
```

---

## 2. Nombre canónico (ReNamer) — sirve a los DOS destinos

| Tipo | Formato | Ejemplo |
|---|---|---|
| **Película** | `Título (Año).ext` | `Ballerina (2025).mkv` |
| **Serie / Anime** | `Título SxxExx.ext` | `One Punch Man S03E01.mkv` |
| **Jellyfin perfecto** | `Título (Año)\Season NN\Título SxxExx.ext` | carpeta por serie y temporada |

**Por qué este formato y no otro:**
- **Jellyfin** exige `(Año)` y `SxxExx` para traer carátula, sinopsis y reparto. Sin eso, **no reconoce el archivo**.
- **El Cosechador** ya reconoce `SxxExx` (probado con 7 casos distintos).
- **Los nombres actuales del Drive no sirven a Jellyfin**: `Free Guy Latino.mp4`, `hablame.mp4` → no matchean.
- ⚠ **Cuidado con el separador:** el preset de VidCoder convierte `_` en espacio y aplica Mayúscula Por Palabra.
  El `SxxExx` y el `(Año)` sobreviven; los **nombres raros de los uploaders, no** → por eso ReNamer va ANTES.

**Orden correcto: extraer → ReNamer → VidCoder → subir.** El renombre primero, para que el mp4 nazca con su nombre bueno.

---

## 3. Las 3 claves del diseño

| Clave | Razón |
|---|---|
| **★ ReNamer ANTES de VidCoder** | El mp4 maestro hereda el nombre canónico (VidCoder lo respeta) |
| **⇉ Drive en PARALELO, nunca en medio** | En serie = sube a Google, baja, y vuelve a subir al host = **3 transferencias** y el doble de conexión. En paralelo = **1 por destino** |
| **⑱ Un solo nombre para dos negocios** | El mismo mp4: web pública (kmoviezone) **y** servicio premium (Jellyfin) |

---

## 4. Reparto de trabajo

| Paso | Quién | Herramienta |
|---|---|---|
| 1. Conseguir enlaces | **Monarca** | a mano → `cola-enlaces.txt` |
| 2. Descargar + extraer | **Monarca** | MiPony |
| 3. **Renombrar canónico** | **Monarca** | **ReNamer** |
| 4. Transcodificar | **Monarca** | VidCoder (preset *seawolf 1080p*) |
| 5A. Subir a servidores | **Monarca** | FileUploader (4 hosts) |
| 5B. Copiar al Drive | **Monarca** | Google Drive para Escritorio (`I:`) |
| 6. Cosechar | **Bellion** | `cosechar.py` |
| 7. Publicar | **Bellion** | `build.py` + `subir.py` |
| 8. Verificar | **Bellion** | `curl` al sitio vivo |

---

## 5. Estado de cada pieza (27-oct-2026)

| Pieza | Estado |
|---|---|
| `cola-enlaces.txt` multi-cajón | ✅ operativo |
| `mipony.py` (encolar/estado/pendientes) | ✅ operativo |
| `extraer.py` (UnRAR propio) | ✅ operativo |
| Nombre canónico ReNamer | ⏳ **por definir reglas** |
| VidCoder (preset seawolf 1080p) | ✅ existe · ⏳ falta automatizar (carpeta vigilada) |
| Servidores | ✅ streamtape · voe · vidmoly · ⏳ mixdrop |
| Drive | ✅ montado en `I:` · ⏳ falta la copia en paralelo |
| `cosechar.py` (series) | ✅ **con filtro por título, 4 hosts, `--actualizar`** |
| Cosechador de **películas** | ⏳ **por construir** |
| `build.py` / `subir.py` / `.htaccess` | ✅ operativos y verificados |

---

## 6. Lecciones que quedaron grabadas hoy

1. **Un host de 1 año de vida no es un host** (player4me: murió).
2. **Un host viejo también cierra** (vidoza: 11 años, *"not open to visitors"*).
3. **Los hosts de video RECODIFICAN** (voe sirve 720p/151 MB de un 1080p de 1478 MB).
4. **La subida-remota desde MediaFire no funciona** (403) y choca con el muro del `.rar`.
5. **El log de FileUploader acumula TODA la historia** → el título DEBE filtrar.
6. **Primero el desplegable, después la investigación** (compatibilidad antes que antigüedad).
7. **Drive montado como disco = fuente** (`I:`); como servidor, no.
8. **Sacar un host muerto toca 3 archivos** (cosechar · build · index).
9. **Verificar siempre en el sitio VIVO**, nunca solo en el FTP.

---
*Documento operativo — Seawolf Studio.*
