#!/usr/bin/env python3
"""
MEDIOS — Seawolf Agent
======================
Analisis de adjuntos para la Capa 1:
- audio    -> transcripcion (Groq whisper)
- imagen   -> descripcion (vision)
- video    -> DOS CANALES: audio (transcripcion) + fotogramas (vision)

Antes de esto, un video caia en "[video adjunto]" y el filtro clasificaba a ciegas.
Acotado por diseno: duracion maxima, numero de fotogramas y tiempos; si algo falla,
devuelve un texto degradado pero NUNCA tumba el filtro.

Prueba: python3 medios.py video /ruta/video.mp4
        python3 medios.py audio /ruta/nota.ogg
        python3 medios.py imagen /ruta/foto.jpg
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

ORK = os.environ.get("OPENROUTER_API_KEY", "")
GROQ = os.environ.get("GROQ_API_KEY", "")
VMODEL = os.environ.get("VISION_MODEL", "google/gemini-2.5-flash")
STT = os.environ.get("STT_MODEL", "whisper-large-v3-turbo")
VIDEO_MAX_SEG = int(os.environ.get("VIDEO_MAX_SEG", "90"))
VIDEO_FRAMES = int(os.environ.get("VIDEO_FRAMES", "3"))


def _post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def transcribe(path):
    """Audio -> texto (Groq whisper)."""
    r = subprocess.run(["curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions",
                        "-H", "Authorization: Bearer " + GROQ, "-F", "file=@" + path,
                        "-F", "model=" + STT, "-F", "language=es", "-F", "response_format=json"],
                       capture_output=True, timeout=180)
    try:
        return json.loads(r.stdout).get("text", "").strip()
    except Exception:
        return ""


def describe_image(path, mt="image/jpeg"):
    """Imagen -> una frase objetiva (vision)."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    d = _post_json("https://openrouter.ai/api/v1/chat/completions",
                   {"model": VMODEL, "max_tokens": 140, "reasoning": {"enabled": False},
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": "Describe en UNA frase que muestra esta imagen "
                                                 "(contexto: conjunto residencial en Colombia). Objetivo y breve."},
                        {"type": "image_url", "image_url": {"url": "data:" + mt + ";base64," + b64}}]}]},
                   {"Authorization": "Bearer " + ORK})
    return (d["choices"][0]["message"].get("content") or "").strip()


def _duracion(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, timeout=60)
        return float((r.stdout or "0").strip() or 0)
    except Exception:
        return 0.0


def describe_video(path):
    """Video -> texto con DOS canales: lo que se dice (audio) y lo que se ve (fotogramas)."""
    dur = _duracion(path)
    partes = []
    if dur:
        partes.append("duracion %.0fs" % dur)

    # ---- canal 1: AUDIO (lo que se dice) ----
    try:
        aud = tempfile.NamedTemporaryFile(delete=False, suffix=".ogg").name
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vn", "-ac", "1",
                        "-ar", "16000", "-t", str(VIDEO_MAX_SEG), aud],
                       capture_output=True, timeout=180)
        if os.path.getsize(aud) > 1200:                      # si trae audio de verdad
            t = transcribe(aud)
            partes.append("audio: " + (t[:700] if t else "(sin voz inteligible)"))
        else:
            partes.append("audio: (sin voz)")
        os.unlink(aud)
    except Exception as e:
        partes.append("audio: (error %s)" % str(e)[:40])

    # ---- canal 2: FOTOGRAMAS (lo que se ve) ----
    try:
        n = max(1, VIDEO_FRAMES)
        total = min(dur, VIDEO_MAX_SEG) if dur else 10.0
        descripciones = []
        for i in range(n):
            t = (total * (i + 0.5)) / n
            frame = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.1f" % t, "-i", path,
                            "-frames:v", "1", "-vf", "scale=640:-1", frame],
                           capture_output=True, timeout=120)
            if os.path.exists(frame) and os.path.getsize(frame) > 500:
                d = describe_image(frame)
                if d:
                    descripciones.append("%ds: %s" % (int(t), d))
            os.unlink(frame)
        partes.append("imagenes: " + (" | ".join(descripciones) if descripciones else "(no se pudo leer)"))
    except Exception as e:
        partes.append("imagenes: (error %s)" % str(e)[:40])

    return "[video] " + " ; ".join(partes)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    p = sys.argv[2] if len(sys.argv) > 2 else ""
    if cmd == "video":
        print(describe_video(p))
    elif cmd == "audio":
        print(transcribe(p))
    elif cmd == "imagen":
        print(describe_image(p))
    else:
        print(__doc__)
