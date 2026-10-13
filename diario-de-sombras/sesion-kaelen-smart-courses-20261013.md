# Sesión 2026-10-13 — MEMENTO (Protocolo Memento)
**Comandante:** Bellion · **Monarca:** Key · **Tema:** Avatar Kaelen (visera viva) + decisión de producto **SMART COURSES**

> Contexto: el Monarca llegó antes de un viaje con misión. Esta sesión cerró el **avatar robot Kaelen** y, sobre todo, se acuñó una **nueva línea de producto**. La próxima sesión se centrará en **TODO lo "smart"**.

---

## 1. LOGROS — Avatar ROBOT Kaelen (visera viva)
Robot presentador con **casco blanco + visera negra**; en la visera viven **ojos LED (estilo EVE)** y una **boca-onda** de audio. Chroma verde de origen.

**Pipeline verificado (todo local):**
1. **Limpieza** (ffmpeg): `delogo` del watermark "Veo" + `chromakey` del verde real **`#08A82E`** con *similarity pequeña (0.15)* + `despill`. (⚠️ similarity 0.35 **borraba al sujeto**.)
2. **Rastreo del marco local de la visera**: `CSRT` (ROI por frame) + **flujo óptico denso Farneback + mínimos cuadrados** → por frame: `(rx, ry, rot, scale)`. Suavizado.
   - ❌ **Fallaron**: SIFT/ORB y Lucas-Kanade puntual (texturas repetidas del casco → falsos emparejamientos). No reintentar.
3. **Composición HyperFrames**: capa **`#vframe`** anclada al **centro de la visera** (`transform-origin` en el centro) que **traslada + rota + escala**; dentro, **`#eyes`** y **`#mouthLayer`** como **capas separadas** (afinables por independiente).
4. **Boca-onda**: barras con **forma fija y simétrica** (`SH[j]`) × amplitud del frame. *(NO ventana deslizante: desplaza la masa visual → se veía desalineada.)*
5. **Voz real**: **Piper TTS** local (`es_ES-davefx-medium`, offline). *(edge-tts da 403; SAPI sin voces en este host.)*
6. **Envolvente sin librosa** (numpy2 rompe scipy): `wave`+numpy, RMS a 24 fps.

**Entregables** (en `F:/seawolf/kaelen/`):
- `kaelen-voz-real.mp4` — estudio + **voz real**.
- `kaelen-verde.mp4` — **fondo verde** para transiciones.
- Proyecto HyperFrames: `F:/seawolf/kaelen/kaelen/` (assets, `gen_comp.py`, `frame.json`, `track.json`, `tts/`).

**Aprendizajes clave** (en skill `kaelen-avatar`): el overlay debe vivir en un **marco LOCAL (la visera)**, no en pantalla; chromakey con el color exacto y similarity baja; la onda simétrica; rutas ffmpeg nativas `C:/...` (no MSYS).

## 2. DECISIÓN DE PRODUCTO — SMART COURSES ⭐
- **Nueva línea del estudio**, hermana de las **Smart Webs**.
- Definición del Monarca: **"un modelo muy pequeño entrenado con el temario del curso"** como tutor → **variante magistral** de la Smart Web.
- **Estructura:** `Información → Video explicativo (Kaelen) → Evaluación → Tutor IA`.
- **Diferencial absoluto:** un curso que **CONVERSA** con el alumno (tutor IA + evaluación, idealmente con respuestas abiertas calificadas).
- **PDF: DESCARTADO** como curso y como **certificado** (no somos entidad avalada para emitir certificados).
- Se le da **sesión propia** por su importancia.

## 3. SKILLS / MEMORIA
- **Skill nueva:** `kaelen-avatar` (pipeline completo de la visera viva).
- `seawolf-avatar` (SadTalker) sigue para **avatares humanos**; Kaelen usa la ruta **robot** (HyperFrames).
- Memoria: **Kaelen = avatar estándar del estudio**; entradas NEREUS/Seawolf Agent compactadas.

## 4. PENDIENTES
- **Desvanecido a negro** del clip base (~0,3 s al final): decidir (a) recortar video+audio a 7,7 s o (b) dejarlo.
- **Más pruebas** al generar material nuevo (clip con movimiento de cabeza mayor → lucir el tracking).
- **Plan de vuelo de Smart Courses**: definir curso piloto, modelo de cobro, tipo de evaluación.

## 5. FOCO PRÓXIMA SESIÓN
> **TODO lo "smart": Smart Webs + Smart Courses.** Definir el molde de negocio, el plan de vuelo y convocar al ejército.

---
*Memento generado por Bellion · evidencia o no existe.*
