# Capacidad: HyperFrames — Generación de contenido por código (Seawolf Studio)

> Archivado por Bellion, 2026-10-11. Verificado en vivo (no promesa de marketing).

## Qué es
`heygen-com/hyperframes` — framework **open-source** que convierte **HTML + CSS + GSAP** en **MP4
deterministas**. Renderiza con **Chrome headless + FFmpeg**. **Licencia Apache-2.0** → absorbible para
uso comercial (con atribución). **Corre 100% local, sin claves, sin nube.**

## Instalación (verificada)
```bash
npm i -g hyperframes                     # Node >= 22
hyperframes telemetry disable            # APAGAR telemetría (privacidad)
npx hyperframes browser ensure --force   # descarga su Chrome Headless Shell propio
```
**PITFALL Windows:** el Chrome del sistema puede fallar al arrancar (SIGKILL/ETIMEDOUT). Solución: su
propio `chrome-headless-shell` v152 (descargado a `~/.cache/hyperframes/chrome/`). NO definir
`HYPERFRAMES_BROWSER_PATH` si quieres el propio.
**PITFALL render:** usar el binario global `hyperframes render` (no `npx`), que puede huérfanar el
proceso (`render_cancelled_parent_exited`).

## Flujo
```bash
hyperframes init <proj> --example blank --resolution portrait --non-interactive
# editar index.html  ->  <div id="root" data-composition-id="main" data-duration=... data-width/height=...>
#                        clips con data-start/data-duration/data-track-index + timeline GSAP en window.__timelines["main"]
hyperframes render --workers N           # -> renders/<proj>_<fecha>.mp4
hyperframes check | validate | snapshot  # validación
```

## Límites y complejidad máxima
- **Salida:** MP4, WebM, MOV (alfa), GIF, secuencia PNG, HLS · hasta **4K** · **fps 1–240**.
- **Entrada:** HTML/CSS/GSAP, video (+alfa), audio, imágenes, **captura de webs**, datos.
- **Nativo:** TTS local (Kokoro), transcripción (whisper), quitar fondo, etalonaje (LUTs), normalizar
  audio (LUFS), cortar a la música (beats).
- **Catálogo:** ~446 bloques/componentes (3D, captions, transiciones, datos/gráficas, mapas, cursores,
  superficies WebGPU/liquid-glass, flowchart, logo-outro…).
- **Complejidad:** *todo lo que un navegador pueda pintar* (3D, WebGPU, shaders, motion paths,
  multi-corte desde una grabación, data-driven personalizado).
- **Límites honestos:** render ≈ **2× tiempo real**; NO es text-to-video (compone, no inventa imágenes);
  pesado en RAM (worker ≈ 256 MB de Chrome); no reemplaza un NLE de metraje pesado.

## Lo construido (evidencia)
- **Sting oficial del estudio:** `renders/seawolf-sting.mp4` (H.264 · 1080×1920 · 10 s · 1,5 MB · render 19,8 s).
- **Composición:** `composition-seawolf-short.html` (HTML+GSAP, logo neón limpio, tagline, pills).
- **Skill del ejército:** `hyperframes-content-SKILL.md` (usar por KAISEL/TITAN/KAMISH).
