# MEMENTO — BOTÍN VIDCODER (preparar la colección para el catálogo)

**Fecha:** 2026-10-31 (turno nocturno del Monarca)
**Sesión:** taller de microapps / automatización de VidCoder
**Estado:** T01 COMPLETA 13/13 · herramienta probada y calibrada · **el botín de largo queda para cuando vuelva el Monarca**

---

## 1. Lo que quedó HECHO (no volver a investigarlo)

- **`codificar-carpeta.py` (v4) funciona**: codifica H.265/MKV → **MP4 H.264 1080p con audio español y los subtítulos forzados QUEMADOS** (abajo-centro, amarillo con borde, ~105 px, fuente Arvo), y **reemplaza en sitio** con el original a salvo por volumen separado.
- **T01 (Los Simpson S01, 13 episodios): 13/13 en `.mp4`.** Verificación **independiente** (`verificar-lote.py`): **13 OK · 0 fallas · 0 avisos**, los 13 con audio `spa`. Originales en `J:\_origenes-reemplazados`.
- **La PUERTA protegió la biblioteca las 5 veces que rechazó.** De esos 5 rechazos, **4 eran fallas de la puerta, no de los archivos** — ya corregidas (ver §4).
- Commits: `ef12cf1` (T01 completa + calibración), `422d26a` (tres procesos).
- **El skill del taller ya tiene todas las lecciones**: `seawolf-kmoviezone-streaming/references/vidcoder-y-destinos.md` (§4-sexies Autopilot, §4-septies la PUERTA).

## 2. EL MAPA — dónde se borra y dónde NO

### 🟢 EL BOTÍN: `H:\caida` — **NO SE BORRA NUNCA DE AQUÍ**
Es la fuente. El taller **mueve** el original a `J:`, nunca lo borra. 1.211 videos en total.

| Grupo | Carpetas | Estado |
|---|---|---|
| **HECHO** | `T01` (13 episodios, hoy) · `EX01` (48) · `EX02` (22) | ✅ |
| **MIXTO (a medias)** | `L1G4_D3_L4_JU5T1C14.part1` (65 mkv + 26 mp4) · `T03` (23 mkv + 1 mp4) | ⚠️ la herramienta los completa sola (reanudable) |
| **PENDIENTE (1.096 mkv)** | `T02`, `T04`–`T37`, `EX03`–`EX05`, `game of throns` (73), `JAMES BOND` (26, en la raíz), `W0Lv3r1n3_y_105_Xm3n.part1` (26), `one punch mas S03` (12), `TTHH333SSS44NNNDDMM44NNS02MrX.part01` (12), `TLOU_S1.part1` (9), `TOG1/TOG2.part1`, `0N3_5H0T_4G3NT_C4RT3R`, y las de fuente extraña (`ԌԌ33ΝΝ33ᎡᎡ44ТТ00ᎡᎡᎡᎡ33Χ01/02/03`, `33ᏞᏞРР44ᎠᎠᎡᎡ11Ν003Ꭰ1ТΜгΧ`) | ⏳ |

### 🔴 `E:\wwe` (92 mp4) — **REVISAR ANTES DE DAR POR BUENO**
Son los **cortos de Los Simpson que hizo VidCoder a mano** (`Maggie Simpson In Rogue Not Quite One`, `When Billie Met Lisa`, `Welcome To The Club`, `Yule Log`…). **VidCoder NO quema los forzados** (se descubrió en esta sesión) → **estos NO llevan el subtítulo pegado.** Igual caso: **`EX01` y `EX02`**.
→ **Decidir:** ¿se rehacen con la herramienta, o se quedan así? También **`EX01`: 41 de 48 no traen audio `spa`** (la fuente nunca se dobló; no es falla del proceso).

### 🟡 LO QUE **SÍ** SE PUEDE BORRAR (y solo esto)
| Ruta | Qué es | Cuándo borrar |
|---|---|---|
| `J:\_origenes-reemplazados\*` | **los MKV originales ya reemplazados** (hoy: 4,3 GB de T01) | **solo después de validar** que el mp4 se ve bien → **es el único sitio que se vacía para recuperar espacio** |
| `<carpeta>/_nuevos/_tmp` | temporales (frames, srt) | **siempre**, no hace falta para nada |
| `<carpeta>/_nuevos` | salida intermedia | **solo si la carpeta ya está 100% en mp4** — si queda un mp4 a medias, NO: es la reanudación |

### ⛔ NO TOCAR
- **`H:\caida`** (fuente) — ni borrar ni mover a mano.
- **`J:\` fuera de `_origenes-reemplazados`** — ahí viven también `007` y `Juego de tronos`. Nada más se toca.
- **Ningún `.mkv` de `H:`** hasta que su carpeta esté cerrada y validada.

## 3. DISCOS (medido 2026-10-31)

| Disco | Libre | Nota |
|---|---|---|
| **J: 723 GB** | el destino del respaldo — **holgado, es el que aguanta el largo** |
| H: 443 GB | el botín |
| I: 184 GB · E: 148 GB | |
| **D: 117 GB (88%)** | **el más apretado — evitar** |
| F: 20 GB (83%) | casi lleno |

**Estimación honesta:** ~305–330 s por episodio → los **1.096 mkv ≈ 90 horas de codificación continua** (~4 días). Por eso va **una carpeta a la vez**.

## 4. LAS CUATRO CALIBRACIONES QUE COSTARON LA TARDE (no repetir el error)

1. **Tres procesos** (supervisor / codificador / verificador). El proceso que corre un codificador pesado **queda envenenado** (`rc=3221225794`) y no vuelve ni en 300 s. **La verificación nunca va en el proceso que codificó.**
2. **El supervisor también se agota** → dosificarlo (`--max-archivos`) y **el supervisor del lote largo es el SHELL**, no el script (bucle de corridas con supervisor nuevo).
3. **Dentro de cada corrida: verificar PRIMERO, codificar al final.** Verificar después de codificar hacía que avanzara **una corrida de cada dos**.
4. **La duración se compara contra el VIDEO, no contra el contenedor del MKV** (los subtítulos lo estiran: E02 tenía contenedor 1389,8 s con video real de 1385,4 s), y **el quemado se muestrea en los 3 eventos MÁS LARGOS**, no en el primero (el primero de E13 dio 0,279% con el forzado SI quemado).
5. **"Ya está hecho" se lee del RESPALDO en `J:`, no de `_nuevos`** — al reemplazar, el mp4 sale de `_nuevos`, así que deducirlo de ahí hacía que un episodio terminado **se respaldara a sí mismo**.
6. **Un codificador vivo en la máquina lo empeora todo**: un `VidCoderWorker.exe` **huérfano sigue codificando aunque se cierre la ventana** (el Monarca lo detuvo y el lote despegó).

## 5. LA RECETA DEL LARGO (cuando el Monarca vuelva)

```bash
# 0) VidCoder CERRADO y sin VidCoderWorker vivo
# 1) una carpeta a la vez. N = nº de videos + 3 de margen. EN SEGUNDO PLANO.
cd /c/Users/Admin
for i in $(seq 1 N); do
  python seawolf-agent/kmoviezone/tools/codificar-carpeta.py "H:/caida/<CARPETA>" \
      --reemplazar --max-archivos 1
done
# 2) al cerrar la carpeta, verificación independiente:
python seawolf-agent/kmoviezone/tools/verificar-lote.py "H:/caida/<CARPETA>" --modo resultado
# 3) validado -> recuperar espacio borrando SOLO J:\_origenes-reemplazados\<CARPETA>
```

- **Antes de soltar una carpeta nueva, un solo archivo de prueba** (`--solo "<algo>"`) — así se ejercita el camino destructivo con red debajo.
- **Se reanuda solo**: si se corta, relanzar el bucle y sigue donde quedó.

## 6. HERRAMIENTAS (rutas exactas)

| Archivo | Qué es |
|---|---|
| `seawolf-agent/kmoviezone/tools/codificar-carpeta.py` | el codificador + PUERTA + reemplazo (v4, tres procesos) |
| `seawolf-agent/kmoviezone/tools/verificar-lote.py` | verificador independiente con ffprobe (solo lectura) |
| `seawolf-agent/kmoviezone/tools/fonts/arvo.ttf` | fuente del forzado (OFL) |
| `seawolf-agent/kmoviezone/tools/preset-seawolf-1080p.json` | el preset exportado de VidCoder |
| `J:\_origenes-reemplazados` | los originales reemplazados (la red debajo) |

**ffmpeg/ffprobe:** `C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin`

## 7. LO QUE NO SE HIZO (a propósito)

- **No se tocó ninguna otra carpeta del botín**: T01 era la prueba.
- **No se borró ni un solo archivo en toda la sesión.** Todo se movió; el respaldo siempre va primero.
- **`EX01`/`EX02`/`E:\wwe` no se rehicieron**: quedan los mp4 de VidCoder **sin forzado quemado** hasta que el Monarca decida.
