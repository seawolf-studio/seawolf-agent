# ✏️ RENOMBRADOR SEAWOLF — Manual de uso

**Módulo de Seawolf Tools** · Renombrado masivo de archivos con vista previa y deshacer.

---

## ¿Qué es?

Un renombrador de archivos por reglas. Se abre como **pestaña dentro de Seawolf Tools**
(`http://localhost:8770` → pestaña **✏️ Renombrador**).

Su razón de ser: los archivos que llegan de internet traen nombres sucios —
fechas de emisión, calidad, idioma, la firma del uploader, corchetes por todas partes.
Ordenarlos a mano son horas. Esto lo hace en un clic **y siempre le deja ver antes qué va a pasar.**

---

## Las tres garantías (por qué es seguro)

| Garantía | Cómo funciona |
|---|---|
| **1. Vista previa obligatoria** | Siempre le muestra el **ANTES** y el **DESPUÉS** de cada archivo antes de tocar nada. Si no le gusta, no aplica. |
| **2. Deshacer con un botón** | Toda operación queda registrada. El botón **↩ DESHACER** devuelve los nombres originales. |
| **3. Nunca pisa un archivo** | Si el nombre destino ya existe, ese archivo se salta y se reporta como error. No hay pérdidas. |

Además, cada operación se registra en `seawolf-renombrador-historial.jsonl` con un
**sello (hash) de 16 caracteres** — queda constancia de qué se cambió y cuándo.

---

## Cómo se usa (4 pasos)

```
1.  Escriba la carpeta         (ej:  H:\caida  ó  H:/caida)
2.  Marque las reglas          (o pulse un atajo)
3.  Pulse  👁 Ver vista previa → revise el ANTES / DESPUÉS
4.  Pulse  ✔ APLICAR           (y si algo no cuadra:  ↩ DESHACER)
```

---

## LAS REGLAS — qué hace cada una

> Se aplican **en este orden**, no en el orden en que las marque.

### 🗓️ Quitar fechas
Elimina las fechas que traen los archivos al principio, entre paréntesis o corchetes:
`(1989-12-17)`, `(2019)`, `[ 1990-01-14 ]`.
```
(1989-12-17) The Simpsons - S01E01.mkv   →   The Simpsons - S01E01.mkv
JAMES BOND #01 [ 1962 ] DR NO.mkv        →   JAMES BOND #01 DR NO.mkv
```

### ( ) Quitar paréntesis
Elimina **todo** lo que esté entre paréntesis, incluidos los paréntesis.
```
El Padrino (2020) (RE-EDIT).mkv   →   El Padrino.mkv
```

### [ ] Quitar corchetes
Elimina **todo** lo que esté entre corchetes, incluidos los corchetes.
```
[Erai-raws] One Punch Man - 01.mkv   →   One Punch Man - 01.mkv
```

### { } Quitar llaves
Elimina **todo** lo que esté entre llaves. Útil para los identificadores de los scrapers.
```
Serie (2024) {tvdb-99}.mkv   →   Serie (2024).mkv
```

### 🗑️ Borrar combinaciones
Borra de una **lista de textos exactos** que usted escriba. Sepárelos con coma.
Para quitar la firma del uploader, el idioma o la calidad.
```
Entrada:  By MrX, DUAL, 1080p
Pelicula DUAL 1080p By MrX.mkv   →   Pelicula.mkv
```

### 🔁 Reemplazar combinaciones
Cambia un texto por otro. Formato `VIEJO>NUEVO`, separados por coma.
**Para reemplazar por un espacio, deje el lado derecho vacío pero con un espacio: `.> `**
```
Entrada:  .> , _> 
Serie.S01E01.1080p_x264.mkv   →   Serie S01E01 1080p x264.mkv
```

### 📅 Año al final (películas)
Mueve el año que está al principio hacia el final, entre paréntesis.
Es el **formato canónico de películas** para Jellyfin y Plex.
```
(2019) Parasitos 1080p.mkv   →   Parasitos 1080p (2019).mkv
```

### ✨ Limpiar espacios y bordes
Junta espacios repetidos y quita guiones, puntos y espacios sueltos que quedan
al principio o al final **después de borrar cosas**.
*Se activa sola siempre* — sin ella quedan nombres tipo `Serie  -  .mkv`.
```
Serie  -  S01E01 -  .mkv   →   Serie - S01E01.mkv
```

---

## LOS ATAJOS (presets)

Un clic configura las reglas solas y muestra la vista previa al instante.

### 🎯 Jellyfin · Serie
```
Reglas:   Quitar fechas  +  Limpiar espacios
Además:   Renombra las carpetas de temporada
```
Deja los episodios como `Serie - SxxEyy - Título.ext`.

> **¿Por qué en inglés?** Es lo correcto, aunque parezca raro: Jellyfin identifica la serie
> por su **título original** (`The Simpsons`). Traducir el nombre del archivo **debilita** el
> reconocimiento. La sinopsis, la carátula y los nombres de capítulo los trae de TMDb
> **en el idioma que usted configure** — así que lo verá todo en español igual.

### 🎯 Jellyfin · Película
```
Reglas:   Año al final + Quitar paréntesis + Quitar corchetes + Quitar llaves + Limpiar
```
Deja `Título (Año).ext`, quitando calidad, idioma y firma.

### 🎯 Limpiar todo (general)
```
Reglas:   Quitar fechas + paréntesis + corchetes + llaves + Limpiar
```
Primera pasada cuando todavía no sabe qué reglas quiere.

---

## 📁 CARPETAS DE TEMPORADA — y la trampa que resuelve

Este apartado corrige algo que **rompe las bibliotecas de Jellyfin**.

**El problema:** Jellyfin espera que la carpeta se llame `Season 01`.
Si se llama `Temporada 01`, **crea una temporada vacía y otra duplicada**.
Con 1.163 archivos, arreglarlo a mano no es divertido.

```
H:\caida\T01\Temporada 01\   →   H:\caida\T01\Season 01\
```

> *Verificado en la documentación oficial de Jellyfin y en sus incidencias de GitHub
> (issue #15040) y en r/Jellyfin: **"lo arreglé renombrando las carpetas a 'Season *'"**.*

**Botones:** `👁 Ver qué carpetas cambiarían` · `✔ Renombrar a Season NN`

Renombra también `Temporada 1`, `TEMP 01`, `T 01` y `Season 1` → todo queda `Season NN`.
Las renombra de las **más profundas hacia arriba**, para no invalidar las rutas.

---

## API (para quien quiera integrarlo)

El módulo se controla por HTTP. Útil para automatizar o para envolverlo en otra interfaz.

| Método | Ruta | Cuerpo | Devuelve |
|---|---|---|---|
| `POST` | `/ren-preview` | `{carpeta, sel[], valores{}, solo_video}` | Conteo + muestra ANTES/DESPUÉS (**no toca nada**) |
| `POST` | `/ren-aplicar` | igual | `{ok, total_errores, errores[]}` + registro de deshacer |
| `POST` | `/ren-deshacer` | `{}` | `{ok, msg}` — revierte la última operación |
| `POST` | `/ren-carpetas-preview` | `{carpeta}` | Carpetas de temporada que cambiarían |
| `POST` | `/ren-carpetas` | `{carpeta}` | Renombra a `Season NN` |
| `GET` | `/api/state` | — | Incluye `renreglas`, `renpresets`, `renundo` |

`sel` es la lista de identificadores de regla:
`fecha · parentesis · corchetes · llaves · borrar · reemplazar · anio_final · espacios`

`solo_video: true` limita la operación a archivos de video
(`.mkv .mp4 .avi .mov .wmv .flv .m4v .mpg .mpeg .ts .webm`).

---

## Consejos de uso

- **Siempre vista previa antes de aplicar.** Los números no engañan: mire la muestra.
- **De una carpeta a la vez.** Aplicar y revisar el resultado antes de pasar a la siguiente.
- **Si algo sale mal, DESHACER inmediatamente** — el registro es de un solo nivel.
- **Los nombres con acentos y símbolos raros** se conservan tal cual: solo se cambia lo que las reglas tocan.
- **Nunca cambia la extensión** del archivo. `.mkv` sigue siendo `.mkv`, pase lo que pase.

---

## 🌐 EL DOMINIO — acceso desde fuera del PC

La herramienta se publica en:

```
https://herramientas.sw-st.net
```

**Cómo funciona:** el aplicativo corre en el PC (tiene que ver sus discos) y un **túnel de
Cloudflare** lo publica en el dominio. **No hay que abrir puertos en el router** y el PC
queda invisible: solo el túnel sabe llegar.

**Arranque:** doble clic en `C:\Users\Admin\HERRAMIENTAS-SEAWOLF.bat` (y queda en el arranque
de Windows). Levanta dos ventanas minimizadas:

| Ventana | Qué es |
|---|---|
| **Seawolf Tools** | El aplicativo (escanea los discos) |
| **Seawolf Tunel** | El túnel que publica el dominio |

### 🔒 La cerradura

**Sin la clave de acceso no se entra** — ni en local ni por el dominio.

```
Ver la clave     :  python intel\seawolf-tools.py clave
Cambiarla        :  python intel\seawolf-tools.py clave --sub nueva
Entrar (1ª vez)  :  https://herramientas.sw-st.net/?k=<su clave>   ← queda guardada
Apagarla         :  python intel\seawolf-tools.py clave --sub off  (NO recomendado)
```

### ⚠️ Honestidad sobre la seguridad

Este aplicativo **mueve y borra archivos del disco**. Publicado en internet, la única barrera
es esa clave. Dos consecuencias prácticas:

1. **No comparta la clave** ni la deje en capturas de pantalla.
2. Si algún día la herramienta crece o la usan terceros, conviene poner delante
   **Cloudflare Access** (doble factor por correo, gratis hasta 50 usuarios).
   La cerradura actual es sólida, pero es un solo factor: la puerta y la llave.

---

*Renombrador Seawolf · parte de Seawolf Tools · código propio · Seawolf Studio.*
