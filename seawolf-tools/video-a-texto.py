#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VIDEO A TEXTO — Seawolf Studio
==============================
Convierte un video de TikTok (o YouTube, Instagram, X, Facebook, lo que sea que
entienda yt-dlp) en TEXTO para poder analizarlo.

Como funciona:
  1. yt-dlp   descarga el video (y los subtitulos si el sitio los tuviera)
  2. ffmpeg   le saca el audio
  3. whisper  transcribe el audio AQUI MISMO (local, gratis, sin enviar nada a nadie)

Uso:
  python video-a-texto.py "https://www.tiktok.com/@usuario/video/1234567890"
  python video-a-texto.py "<url>" --modelo small   # mas preciso (mas lento)
  python video-a-texto.py "<url>" --idioma es      # forzar idioma
  python video-a-texto.py "<url>" --solo-subtitulos  # sin transcribir (si el sitio los trae)

Salidas (en la carpeta de trabajo):
  <nombre>.txt        transcripcion limpia
  <nombre>.srt        subtitulos con tiempos (por si se quieren usar)
  <nombre>.info.json  metadatos del video (titulo, autor, duracion, vistas)

Nota de legalidad: esto sirve para ANALIZAR contenido. No reemplaza ni distribuye
la obra, y no salta ninguna proteccion.
"""
import os, sys, json, argparse, subprocess, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(HERE, "transcripciones")


def log(t):
    print(f"  {t}", flush=True)


def bajar(url, destino, solo_subs=False):
    """Descarga el video (o solo los subtitulos) con yt-dlp."""
    base = os.path.join(destino, "video")
    args = [sys.executable, "-m", "yt_dlp",
            "--no-warnings", "--no-playlist",
            "-o", base + ".%(ext)s"]
    if solo_subs:
        args += ["--skip-download", "--write-auto-subs", "--write-subs",
                 "--sub-langs", "es.*,en.*", "--convert-subs", "srt"]
    else:
        args += ["--write-auto-subs", "--write-subs", "--sub-langs", "es.*,en.*",
                 "--convert-subs", "srt"]
    args += [url]
    r = subprocess.run(args, capture_output=True, text=True, timeout=1800)
    return r.stdout + r.stderr


def audio_de(video, destino):
    """Extrae el audio a wav mono 16k (lo que whisper quiere)."""
    wav = os.path.join(destino, "audio.wav")
    r = subprocess.run(["ffmpeg", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", wav],
                       capture_output=True, text=True, timeout=1800)
    return wav if os.path.exists(wav) else ""


def transcribir(wav, modelo="base", idioma=None):
    """Transcribe con faster-whisper (LOCAL). Devuelve (texto, segmentos)."""
    from faster_whisper import WhisperModel
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, info = m.transcribe(wav, language=idioma, beam_size=5, vad_filter=True)
    trozos, lineas = [], []
    t0 = 0.0
    for s in segs:
        trozos.append(s.text.strip())
        lineas.append((s.start, s.end, s.text.strip()))
        t0 = s.end
    return " ".join(trozos).strip(), lineas, getattr(info, "language", "")


def srt(lineas):
    def hms(t):
        h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
    out = []
    for i, (a, b, txt) in enumerate(lineas, 1):
        out.append(f"{i}\n{hms(a)} --> {hms(b)}\n{txt}\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Video (TikTok/YouTube/...) -> texto")
    ap.add_argument("url")
    ap.add_argument("--modelo", default="base", help="tiny/base/small/medium/large-v3 (mas = mejor y mas lento)")
    ap.add_argument("--idioma", default=None, help="es, en... (si no, lo detecta)")
    ap.add_argument("--solo-subtitulos", action="store_true", help="no transcribir; usar los subtitulos del sitio")
    ap.add_argument("--salida", default=SALIDA)
    a = ap.parse_args()

    os.makedirs(a.salida, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="v2t_")
    try:
        log(f"1/3  Descargando…  {a.url}")
        sal = bajar(a.url, tmp, a.solo_subtitulos)
        videos = [os.path.join(tmp, f) for f in os.listdir(tmp)
                  if os.path.splitext(f)[1].lower() in (".mp4", ".mkv", ".webm", ".mov", ".m4a", ".mp3")]
        subs = [os.path.join(tmp, f) for f in os.listdir(tmp)
                if f.lower().endswith((".srt", ".vtt"))]
        if not videos and not subs:
            log("No se pudo descargar nada. Salida de yt-dlp:")
            print(sal[-1500:])
            return 2

        # 2) metadatos
        meta = {}
        try:
            r = subprocess.run([sys.executable, "-m", "yt_dlp", "--dump-json", "--no-warnings",
                                "--no-playlist", a.url], capture_output=True, text=True, timeout=300)
            i = r.stdout.find("{")
            if i >= 0:
                meta = json.loads(r.stdout[i:].splitlines()[0])
        except Exception:
            meta = {}

        # 3) texto
        texto, lineas = "", []
        if subs:
            log("2/3  El sitio traia subtitulos: los uso (mas rapido que transcribir)")
            with open(subs[0], encoding="utf-8", errors="ignore") as fh:
                texto = fh.read()
            lineas = []
        else:
            if not videos:
                log("No hay video que transcribir y no habia subtitulos.")
                return 3
            log("2/3  Sacando el audio…")
            wav = audio_de(videos[0], tmp)
            if not wav:
                log("ffmpeg no pudo sacar el audio.")
                return 4
            log(f"3/3  Transcribiendo (whisper {a.modelo}, LOCAL, gratis)… puede tardar")
            texto, lineas, idi = transcribir(wav, a.modelo, a.idioma)
            if idi:
                meta["_idioma_detectado"] = idi

        titulo = (meta.get("title") or meta.get("description") or "video")[:60]
        seguro = "".join(c if c.isalnum() or c in "-_ " else "_" for c in titulo).strip().replace(" ", "_")[:50]
        seguro = seguro or "video"

        with open(os.path.join(a.salida, seguro + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(f"FUENTE: {a.url}\nAUTOR: {meta.get('uploader') or meta.get('channel') or '?'}\n"
                     f"TITULO: {meta.get('title') or '?'}\nDURACION: {meta.get('duration') or '?'} s\n"
                     f"{'-'*70}\n\n{texto}\n")
        if lineas:
            with open(os.path.join(a.salida, seguro + ".srt"), "w", encoding="utf-8") as fh:
                fh.write(srt(lineas))
        if meta:
            with open(os.path.join(a.salida, seguro + ".info.json"), "w", encoding="utf-8") as fh:
                json.dump({k: meta.get(k) for k in ("title", "uploader", "channel", "duration",
                                                    "view_count", "like_count", "comment_count",
                                                    "upload_date", "description", "webpage_url",
                                                    "_idioma_detectado") if meta.get(k) is not None},
                          fh, ensure_ascii=False, indent=1)

        print()
        log(f"LISTO -> {os.path.join(a.salida, seguro)}.txt")
        print()
        print("-" * 70)
        print(texto[:2500] + ("…" if len(texto) > 2500 else ""))
        print("-" * 70)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
