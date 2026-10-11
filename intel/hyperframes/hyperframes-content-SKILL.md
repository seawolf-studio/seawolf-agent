---
name: hyperframes-content
description: 'Use when generating video/content with HyperFrames (HTML->MP4).'
---

# HyperFrames Content Generation

## ¿Qué es HyperFrames?

HyperFrames es un framework open-source que convierte HTML, CSS y GSAP en videos MP4 deterministas. Utiliza Chrome headless y FFmpeg para renderizar contenido visual de forma consistente y automatizada.

## Instalación

```bash
npm i -g hyperframes
```

**Requisitos:**
- Node.js >= 22

**Desactivar telemetría:**
```bash
hyperframes telemetry disable
```

## Configuración en Windows

⚠️ **PITFALL CRÍTICO EN WINDOWS:**

El Chrome del sistema puede fallar al arrancar con errores como `SIGKILL` o `ETIMEDOUT`.

✅ **Solución:**
```bash
npx hyperframes browser ensure --force
```

> ⚠️ NO definas `HYPERFRAMES_BROWSER_PATH` si quieres usar el Chrome Headless Shell propio de HyperFrames.
> Verificado: el binario propio es `chrome-headless-shell` v152 descargado a `C:\Users\<user>\.cache\hyperframes\chrome\`.

⚠️ **Render — usa el binario global, NO `npx`:** `npx hyperframes render` puede huérfanar el proceso y cancelar el render (`render_cancelled_parent_exited`). Usa `hyperframes render --workers N` directamente.

## Flujo de trabajo

1. **Iniciar proyecto:**
   ```bash
   hyperframes init <proj> --example blank --resolution portrait --non-interactive
   ```

2. **Estructura de la composición (`index.html`):**
   - Un `div #root` con:
     - `data-composition-id`
     - `data-duration`
     - `data-width`/`data-height`
   - Elementos con `class='clip'` y atributos:
     - `data-start`
     - `data-duration`
     - `data-track-index`
   - Una timeline GSAP en `window.__timelines['main']` (pausada) con `tl.seek(0)`

3. **Renderizar:**
   ```bash
   hyperframes render --workers N
   ```

4. **Validar:**
   ```bash
   hyperframes check
   hyperframes validate
   hyperframes snapshot
   ```

## Capacidades y formatos

HyperFrames puede renderizar a:
- **Formatos:** mp4, webm, mov (alfa), gif, png-sequence, hls
- **Resoluciones:** hasta 4K
- **FPS:** 1-240

Comandos útiles:
- `capture(web->video)` → Captura contenido web
- `tts(voz local Kokoro)` → Texto a voz local
- `transcribe(whisper)` → Transcripción de audio
- `remove-background` → Elimina fondos
- `catalog(blocks/components)` → Catálogo de componentes
- `beats` → Sincronización rítmica
- `preview(studio)` → Vista previa del studio
- `publish` → Publicación de videos

## Prohibiciones

- No usar Shopify, AdSense ni anuncios de Facebook
- Desactivar telemetría
- No almacenar claves en el cliente

## Ejemplo mínimo de `index.html`

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <style>
    #root {
      width: 1080px;
      height: 1920px;
      background: #000;
      position: relative;
    }
    .clip {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-duration="5" data-width="1080" data-height="1920">
    <div class="clip" data-start="0" data-duration="2" data-track-index="0">
      <h1 style="color:white; font-size:48px; margin-top:200px;">¡Hola desde HyperFrames!</h1>
    </div>
  </div>

  <script>
    window.__timelines = {};
    const tl = gsap.timeline({paused: true});
    tl.to('.clip', {
      duration: 1,
      opacity: 1,
    });
    window.__timelines['main'] = tl;
  </script>
</body>
</html>
```