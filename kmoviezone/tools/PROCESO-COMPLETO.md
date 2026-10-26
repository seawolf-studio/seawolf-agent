# 📋 PROCESO COMPLETO — kmoviezone (de la fuente al catálogo publicado)
**Para:** Monarca · **De:** Bellion, Gran Comandante · **Fecha:** 2026-10-25
**Carpeta de trabajo:** `C:\Users\Admin\streaming_web\`

> **Léalo una vez completo antes de empezar.** Cada fase dice qué hacer **y cómo verificar** que salió bien.

---

## 🗺️ EL MAPA (7 fases)
```
1. CONSEGUIR    los enlaces          (usted)
2. ENCOLAR      en MiPony            (usted + ENCOLAR.bat)
3. DESCARGAR    MiPony → D:\my stream (MiPony)
4. SUBIR        FileUploader → 3 hosts (usted)
5. COSECHAR     log → fila del catálogo (cosechar.py)
6. PUBLICAR     catálogo → web        (watch.py / BAT)
7. VERIFICAR    que se vea bien        (usted)
```

---
# FASE 1 — CONSEGUIR LOS ENLACES *(manual)*

1. Busque el contenido en sus fuentes habituales (mayoría **MediaFire**).
2. **Regla de oro:** fíjese en el **nombre exacto** del archivo. El Cosechador saca el número de capítulo del nombre, así que un nombre torcido = capítulo mal numerado.
3. Reúna **los enlaces de una sola tanda** (una serie o una película) antes de pasar a la fase 2.

✅ **Verificación:** tiene una lista de enlaces de **un solo título**.

---

# FASE 2 — ENCOLAR EN MIPONY *(usted + 1 doble clic)*

1. Abra `cola-enlaces.txt`.
2. Rellene **las 3 líneas** (respete los dos puntos):
   ```
   titulo: Solo Leveling
   tipo: anime
   carpeta: D:\my stream
   ```
   *(tipo admite: `pelicula`, `serie`, `anime`, `comics`)*
3. Pegue los enlaces **debajo de la línea `---`**, **uno por línea**.
4. **Guarde** el archivo (Ctrl+S).
5. **CIERRE MiPony.** *(obligatorio: lo reescribe al salir y perdemos los enlaces)*
6. Doble clic en **`ENCOLAR.bat`**.

✅ **Verificación:** el .bat imprime `OK: N enlaces encolados`. Luego **abra MiPony** y confirme que aparecen en la lista.

> ⚠️ **Si el .bat dice `*** MIPONY ESTA ABIERTO ***`** → ciérrelo y repita el paso 6. No insista con MiPony abierto.

---

# FASE 3 — DESCARGAR *(MiPony)*

1. En MiPony, **arranque la descarga** (botón de inicio).
2. Déjelo trabajar. Los archivos caen en la carpeta que puso (`D:\my stream`).
3. Cuando termine (o si quiere saber cómo va), en la carpeta del proyecto:
   ```
   python mipony.py estado
   ```
   Le dice cuántos **Complete**, cuántos **Stopped** y dónde quedaron.
4. **Si quedaron detenidos:**
   ```
   python mipony.py pendientes
   ```
   → escribe `reintentar.txt` con los enlaces caídos. **Re-encólalos** con el mismo `ENCOLAR.bat` (Fase 2, pasos 5 y 6).

✅ **Verificación:** los archivos están **en el disco** (`Complete`).

> 💡 **Dato real:** en su cola hay **633 detenidos** (p. ej. Black Mirror S01–S05). Son descargas a medias, no pérdidas: se reintentan con este mismo método.

---

# FASE 4 — SUBIR A LOS 3 HOSTS *(usted, FileUploader)*

1. Abra **FileUploader** (`Escritorio` → `FileUploader.exe`).
2. Agregue **los archivos de esta tanda** (arrastrar la carpeta o seleccionar).
3. Deje que suba a los **3 hosts**: **streamtape · voe · player4me**.
4. **Ojo con esto (no es culpa suya):**
   - **`429 Too Many Requests`** en player4me → el host lo está frenando. **Reintente con pausa.** Es la causa #1 de enlaces faltantes.
   - **`File is in your account`** → el archivo ya estaba subido; el host **no da enlace nuevo**. Sáquelo manualmente o sáltelo.

✅ **Verificación:** el log creció. Compruébelo así:
```
cosechar.py --lista | findstr /i "player4me"
```
o simplemente siga a la fase 5 — el Cosechador le dirá qué falta.

---

# FASE 5 — COSECHAR LOS ENLACES *(automático)*

**Paso 1 — VER (no escribe nada):**
```
python cosechar.py "Solo Leveling" --tipo anime --filtro "Solo Leveling"
```
Le muestra: **cuántos capítulos**, la **lista de capítulos** y **qué servidor falta** en cada uno.

**Paso 2 — AGREGAR (escribe en `catalogo.csv`):**
```
python cosechar.py "Solo Leveling" --tipo anime --filtro "Solo Leveling" --csv
```

> **`--filtro` es obligatorio en la práctica:** el log **mezcla todas las tandas** que haya subido. El filtro es una palabra que solo aparezca en los archivos de **esta** tanda.

✅ **Verificación:** revise la última línea de `catalogo.csv` — debe tener `titulo,tipo` y la cadena de enlaces con `;` y `|`.

---

# FASE 6 — PUBLICAR *(automático)*

**Opción A (recomendada) — el vigilante ya está corriendo:**
Si `INICIAR_VIGILANTE.bat` está abierto, **detecta el cambio solo** y regenera + sube.

**Opción B (manual):**
```
REGENERAR_DATOS.bat     (regenera datos.json desde catalogo.csv)
SUBIR_WEB.bat           (sube index.html + datos.json + logo.png)
```

✅ **Verificación:** `datos.json` contiene el título nuevo.

---

# FASE 7 — VERIFICAR EN LA WEB

1. Abra **kmoviezone.stream** y **fuerce recarga** (`Ctrl + F5` — el navegador cachea).
2. Busque el título nuevo.
3. **Abra su ficha** y pruebe los **3 servidores**.
4. Si un servidor dice **"· falta"** → ese enlace no llegó (fase 4, el 429). Reintente la subida de ese archivo y repita desde la fase 4.

✅ **Verificación final:** el título se ve, con sus capítulos, y **los 3 botones** funcionan.

---

# 🚫 REGLAS QUE NUNCA SE ROMPEN

| Nunca | Por qué |
|---|---|
| **Escribir en la cola con MiPony abierto** | MiPony reescribe `linkList.xml` al salir → se pierde todo |
| **Usar otro formato raro de nombre de archivo** | El Cosechador no saca el número de capítulo |
| **Subir dos tandas mezcladas sin `--filtro`** | La fila del catálogo saldría con capítulos cruzados |
| **Editar `index.html` a mano** | Lo regenera `build.py`; se pierde el cambio |
| **Olvidar el `Ctrl + F5`** | Verá la versión vieja y creerá que falló |

---

# 🔧 DICCIONARIO DE ERRORES

| Síntoma | Causa | Solución |
|---|---|---|
| `*** MIPONY ESTA ABIERTO ***` | MiPony corriendo | Ciérrelo y repita `ENCOLAR.bat` |
| `429 Too Many Requests` | Límite del host | Reintentar con pausa (no cambiar nada) |
| `File is in your account` | Ya estaba subido | Sacar el enlace a mano o saltar |
| Faltan capítulos en la cosecha | Nombre sin número legible | Renombre con `NN - Título` y re-subir |
| Un capítulo sin un servidor | Subida fallida | Reintentar ese archivo en FileUploader |
| La web no muestra el título nuevo | Falta publicar o caché | `SUBIR_WEB.bat` + `Ctrl + F5` |
| `cosechar` mezcla series | Falta `--filtro` | Añada `--filtro "<palabra de la tanda>"` |

---

# ✅ TARJETA RÁPIDA (para pegar en la pared)

```
1. Pegar enlaces en  cola-enlaces.txt  (titulo/tipo/carpeta)
2. CERRAR MiPony  ->  ENCOLAR.bat
3. Abrir MiPony  ->  descargar
4. FileUploader  ->  subir a los 3
5. cosechar.py "Titulo" --tipo X --filtro "X"          (ver)
   cosechar.py "Titulo" --tipo X --filtro "X" --csv    (agregar)
6. Vigilante sube solo   (o REGENERAR_DATOS.bat + SUBIR_WEB.bat)
7. kmoviezone.stream  +  Ctrl+F5  ->  probar los 3 botones
```

*— Bellion, Gran Comandante del Ejército de Sombras*