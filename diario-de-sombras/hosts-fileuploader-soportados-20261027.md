# HOSTS QUE SOPORTA SU FILEUPLOADER — lista extraída de los pantallazos
**Seawolf Studio · 27-oct-2026 · Bellion**
*Fuente: 14 pantallazos del desplegable de FileUploader del Monarca. Extraído por OCR visual (puede haber algún carácter dudoso).*

---

## ⚙️ CÓMO LEER ESTA LISTA

Los sufijos entre corchetes son **modos de acceso** del host, no parte del dominio:

| Sufijo | Significa |
|---|---|
| **[API]** | Acceso por API → **se puede automatizar** y **permite CARGA REMOTA** (el host jala el archivo) |
| **[cookie]** | Entra con la sesión del navegador |
| **[web]** | Entra como navegador normal |
| **[NoSSL]/[webNoSSL]** | Modo sin cifrado (evitar) |
| **[Resumable]** | Subida reanudable (ideal para archivos grandes) |
| **[root]** | Acceso a la raíz de la cuenta |
| **[Europe]/[Asia]/[USEast]/[USWest]** | Espejos regionales |
| **[Client]** | Con cliente propio de la herramienta |

**REGLA: si un host trae `[API]` o `[Resumable]`, es automatizable y prioritario.**

---

## 🎬 HOSTS DE VIDEO (lo que nos interesa) — con estado verificado hoy 27-oct

| Host | Estado | Antigüedad | Nota |
|---|---|---|---|
| **abyss.to** `[API]` | ✅ 200 | — | Conocido en la escena |
| **cloudvideo.tv** | ✅ 200 | 2014 | **Veterano** |
| **media.cm** | ✅ 200 | 2015 | Veterano |
| **vidhide.com** / **earnvids.com** `[API]` | ✅ 200 | 2023 | Activo (mismo operador) |
| **abstream.to** `[API]` | ✅ 200 | — | Activo |
| **luluvdoo.com** `[API]` | ✅ 200 | 2025 | **¡Distinto de LuluStream!** (esa no está) |
| **loadvid.com** `[API+Wait]` | ✅ 200 | — | Activo |
| **maxstream.org** / maxstream.video | ✅ 200 | — | Activo |
| **embedgram.com** | ✅ 200 | — | Activo |
| **liivideo.com** · **loadingvid.com** · **gvid.one** · **1vid.xyz** · **fsvid.lol** `[API]` | (sin probar) | — | Alternativas |
| `bigwarp.io` `[API]` | ❌ 000 | 2024 | **Caído hoy** |
| `highstream.tv` | ❌ 000 | — | **Caído hoy** |
| `lixstream.com` | ❌ 000 | 2025 | **Caído hoy** |
| `easyvidplay.com` | ❌ 000 | 2025 | **Caído hoy** |
| `kez.tv` | ⚠️ 503 | — | Inestable |
| `goodstream.one` `[API]` | ❌ 000 | 2024 | **Caído** |
| **`vidoza.net`** | ❌ **CERRADO** | 2014 | *"not open to visitors"* (27-oct-2026) |

**Ya en uso (confirmados en su herramienta):** `voe.sx`, `streamtape.com`, `vidmoly.to`, ~~`player4me`~~ (muerto).

---

## ☁️ ALMACENAMIENTO EN LA NUBE — **¡incluye su Drive!**

| Host | Nota |
|---|---|
| **Google Drive** · **Google Drive[Client]** · **drive.google.com** | 🎯 **Su destino para Jellyfin** |
| **Google Photos** · **Google shared folder** · **Google TeamDrive** | Carpetas compartidas y TeamDrive |
| **dropbox.com** `[API]` `[root]` | — |
| **box.com** · **adrive.com** · **icedrive** · **cloud.mail.ru** | — |
| **BaiduCloud** · **mail.ru** `[cloud]` `[video]` | — |
| **1fichier.com** `[NoSSL]` `[web]` · **mediafire.com** `[API]` `[Resumable]` `[web]` | **Fuentes de descarga** |
| **4shared.com** `[API]` · **4sync.com** · **mega** (si aparece) | — |

🎯 **`mediafire.com[API]` y `[Resumable]`: por ahí va la automatización del Monarca.**

---

## 📦 FILE HOSTS (fuentes y respaldo)
1cloudfile · 1dl.net · 1fichier · 1uploadflix · 4bigbox · 4shared · 5ivenews · abcvideo · abstream · abyss · adrive · akmfls.xyz · alfaflie.net · anafast.org · androidhost.ru · ani-stream · archive.org · ausfile · babup · bdupload.asia · bigimage.cz · bigshare.io · bitporno · bowfile · brfiles · brupload.net · bunkr.cr/la/si/su · bunny.net · burstcloud · buzzheavier · byse.sx · casthq.to · cdnplus.org · centfile · chomikuj.pl · clicknupload · cloubix · clouddrop · cloudfam · cloud-share.in · cloudup · cornfile · cyberdrop.me · cyberfile.me · dosyaupload · douploads · down.fast-down · down.mdiaload · downloadani.me · drakkar.st · drop.download · dropapk · dropgalaxy · dysk.to · easybytez · eclipo · edisk.cz · embedgram · embedrise · filedot.to · filedropper · filefactory · filefox · filegram `[API]` · filehost.net · filejoker · filekeeper `[API]` · fileland.io · filemail · filemirage `[API]` · filenext · filepv `[API]` · fileq `[API]` · filer.net · filerazer · filerice `[API]` · filerio.in · files4down · filesbomb · fileserve `[API]` · filespace · filespayouts `[API]` · filestore.me `[API]` · filestore.to · fileup.cc · file-upload.net/org `[API]` · filezipa `[cookie]` · filezz.cloud · filzz.me `[API]` · film77.xyz · fireload `[cookie]` · firestream.to · flashbang.sh · flashbit `[API]` · flexy.stream · florenfile · flyfile.app · forafile · freedisc.pl · freedl.ink `[API]` · freed.link `[API]` · fromsmash · fs.afam.watch · fuckingfast.co · gamefront · gamovideo · gett.su `[API]` · gettyshare · gigapeta · gigasize · gofile.io `[API]` `[root]` · grabitshare · gupload.xyz · hatfile · hdup1 · hdvid.tv · hd-vk.com · hexload `[AP]` · hidan.co/sh · highload.to · hitfile.net · hostr.co · hostuje · hot4share · hotlink.cc · hxfile.co · hyperfileshare · icerbox · iceyfile `[cookie]` · im.ge · imagebam · imagecurl · imagenetz.de · imagetwist · imgadult · imgbank.cz · imgbox · imgclick · imgcubby `[cookie]` · imgdew · imgdrive · imgflare · imgmaze · imgoutlet · imgrock · imgspice · imgtaxi · imgtown · imgur · imgview · imgway.cz · imgx.pl · imx.to · indishare.org · joupLoad · jpgfree · k2s.cc `[API]` · katfile.cloud/com/online/space/vip `[API]` · kez.tv · koramaup `[Cookie]` · krakenfiles `[API]` · larhu.website `[API]` · liivideo · linkbox.to · lixstream · loadingvid · loadit.io `[cookie]` · loadvid `[API]` · loadx.ws · luluvdoo `[API]` · mail.ru · maxstream.org/video · media.cm · mediafire `[API]` …

*(La lista sigue hacia la N-Z — el Monarca se detuvo al llegar a MediaFire.)*

---

## 🚩 CONCLUSIONES DE OPERADOR

1. **~400 hosts.** El problema nunca fue la cantidad: fue **no saber cuáles soporta**. Ya lo sabemos.
2. **Primero el desplegable, después la investigación.** Regla nueva.
3. **`[API]` o `[Resumable]` = prioritario** (automatizable, reanudable).
4. **Los cafés se pagan con sangre:** `player4me` (1 año, murió) · `vidoza` (11 años, **cerró al público**) · 4 hosts caídos hoy en su propia lista (**bigwarp, highstream, lixstream, easyvidplay**). **Nunca confiar en uno solo.**
5. **Google Drive está dentro** → la segunda vía (Jellyfin) tiene transporte propio.
6. **MediaFire `[API]`/`[Resumable]`** → ahí vive la automatización de entrada.

---
*Documento de referencia operativa — Seawolf Studio.*
