#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODIFICAR CARPETA  (Seawolf Studio · Bellion)

Codifica una carpeta completa con los MISMOS ajustes del preset "seawolf 1080p"
(x264 veryfast, main, level 4.0, CRF 24 · AAC 192 estéreo · MP4 con capítulos),
pero con las dos cosas que el preset de VidCoder no puede hacer:

  1. AUDIO: toma la pista en ESPAÑOL por IDIOMA (no la primera por número).
     Si el archivo no trae español -> SE SALTA en voz alta. Nunca cae a inglés.
  2. SUBTÍTULOS: quema los FORZADOS. Y aquí está el hallazgo: en esta biblioteca el
     forzado viene como pista APARTE con el nombre "Forced" y la BANDERA en 0, así que
     VidCoder (que filtra por bandera) no quema nada. Aquí se busca por nombre y, si no,
     por bandera. Cero invención: si no hay forzados, se registra y no se quema.

SEGURO POR DISEÑO: nunca toca el original. Escribe en la carpeta de salida.
Reemplazar en sitio es una decisión posterior y aparte.

Uso:
    python codificar-carpeta.py "H:/caida/T01/Season 01" --salida "C:/.../prueba-T01"
    python codificar-carpeta.py "<carpeta>" --salida "<destino>" --solo "S01E01"
"""
import argparse, json, os, re, subprocess, sys, time

BIN = (r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages"
       r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
       r"\ffmpeg-8.1.2-full_build\bin")
FFMPEG = os.path.join(BIN, 'ffmpeg.exe')
FFPROBE = os.path.join(BIN, 'ffprobe.exe')
EXT = ('.mkv', '.mp4', '.m4v', '.avi')
MAX_ANCHO, MAX_ALTO = 1920, 1080
PATRON_FORZADO = re.compile(r'forzad|forced', re.I)

def probe(f):
    r = subprocess.run([FFPROBE, '-v', 'error', '-show_entries',
        'stream=index,codec_type,codec_name,width,height'
        ':stream_tags=language,title:stream_disposition=forced,default',
        '-show_entries', 'format=duration,size', '-of', 'json', f],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)

def elegir(j):
    """Del JSON de ffprobe saca: indice de video, indice de audio en espanol, indice de subs forzados."""
    vid = aud = sub = None
    subs_es = []
    for s in j.get('streams', []):
        t = s.get('codec_type')
        tag = (s.get('tags') or {})
        lang = (tag.get('language') or '').lower()
        disp = s.get('disposition') or {}
        if t == 'video' and vid is None:
            vid = s['index']
        elif t == 'audio' and aud is None and lang.startswith('spa'):
            aud = s['index']
        elif t == 'subtitle' and lang.startswith('spa'):
            subs_es.append((s['index'], tag.get('title') or '', int(disp.get('forced') or 0)))
    # 1) por NOMBRE ("Forced") — el caso real de esta biblioteca
    for i, titulo, _ in subs_es:
        if PATRON_FORZADO.search(titulo):
            sub = i
            break
    # 2) por BANDERA (comportamiento estandar)
    if sub is None:
        for i, _, forzado in subs_es:
            if forzado:
                sub = i
                break
    return vid, aud, sub, subs_es

def codificar(src, dst, vid, aud, sub, tmp):
    """Devuelve (ok, mensaje). Escribe a dst.partial y renombra al terminar."""
    parcial = dst + '.partial.mp4'
    vf = []
    if sub is not None:                       # extraer los subtitulos y quemarlos
        asf = os.path.join(tmp, 'subs.srt')
        # SRT y no ASS: el ASS que trae esta biblioteca NO lo renderiza libass (verificado
        # con un ASS a mano que si quema). El SRT conserva los mismos eventos y quema bien.
        r = subprocess.run([FFMPEG, '-y', '-v', 'error', '-i', src,
                            '-map', '0:%d' % sub, '-c:s', 'srt', asf],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        if r.returncode != 0 or not os.path.exists(asf) or os.path.getsize(asf) == 0:
            return False, 'no se pudo extraer la pista de subtitulos %d' % sub
        # El SRT hereda la etiqueta <font face="sans-serif" size="71"> del ASS. libass la
        # interpreta sobre un lienzo de 288 lineas, la escala ~3,75x y el texto sale GIGANTE
        # tapando el video (medido: 994 px de alto en vez de 105). Se quita la etiqueta.
        with open(asf, encoding='utf-8-sig', errors='replace') as fh:
            texto = re.sub(r'</?font[^>]*>', '', fh.read())
        with open(asf, 'w', encoding='utf-8') as fh:
            fh.write(texto)
        vf.append('subtitles=subs.srt')       # sin ruta: se ejecuta con cwd=tmp (evita el escape de C:\)
    # escalar SOLO si supera 1080p (DownscaleOnly del preset)
    vf.append("scale=w='min(%d,iw)':h='min(%d,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2"
              % (MAX_ANCHO, MAX_ALTO))
    cmd = [FFMPEG, '-y', '-v', 'warning', '-stats', '-i', src,
           '-map', '0:%d' % vid, '-map', '0:%d' % aud, '-map_chapters', '0',
           '-c:v', 'libx264', '-preset', 'veryfast', '-profile:v', 'main',
           '-level', '4.0', '-crf', '24', '-pix_fmt', 'yuv420p',
           '-vf', ','.join(vf),
           '-c:a', 'aac', '-b:a', '192k', '-ac', '2',
           '-movflags', '+faststart', parcial]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        if os.path.exists(parcial):
            os.remove(parcial)
        cola = (r.stderr or '').strip().splitlines()[-2:]
        return False, 'ffmpeg fallo: ' + ' | '.join(cola)
    os.replace(parcial, dst)
    return True, 'ok en %.0fs' % (time.time() - t0)

def main():
    ap = argparse.ArgumentParser(description='Codifica una carpeta con los ajustes del preset seawolf 1080p')
    ap.add_argument('origen', help='carpeta con los archivos fuente (recursivo)')
    ap.add_argument('--salida', required=True, help='carpeta de salida (NUNCA se toca el original)')
    ap.add_argument('--solo', help='procesar unicamente los que contengan este texto')
    ap.add_argument('--log', help='archivo de registro (por defecto <salida>/codificacion.log)')
    a = ap.parse_args()

    if not os.path.isdir(a.origen):
        print('  ERROR: no existe ' + a.origen); return 2
    os.makedirs(a.salida, exist_ok=True)
    tmp = os.path.join(a.salida, '_tmp'); os.makedirs(tmp, exist_ok=True)
    LOG = a.log or os.path.join(a.salida, 'codificacion.log')

    fuentes = []
    for base, _, fs in os.walk(a.origen):
        for f in fs:
            if f.lower().endswith(EXT):
                fuentes.append(os.path.join(base, f))
    if a.solo:
        fuentes = [f for f in fuentes if a.solo.lower() in os.path.basename(f).lower()]
    fuentes.sort()
    if not fuentes:
        print('  No hay archivos que procesar.'); return 0

    print('  %d archivo(s) · salida: %s' % (len(fuentes), a.salida))
    print('  %-46s %-9s %-6s %-9s %s' % ('ARCHIVO', 'ESPANOL', 'FORZADO', 'PESO', 'ESTADO'))
    print('  ' + '-' * 116)
    lineas, ok_n, sal_n, err_n = [], 0, 0, 0
    for f in fuentes:
        nom = os.path.basename(f)
        j = probe(f)
        if not j:
            print('  %-46s %-9s %-6s %-9s %s' % (nom[:46], '?', '?', '?', 'ILEGIBLE'))
            lineas.append([nom, '?', 'ilegible']); err_n += 1; continue
        vid, aud, sub, subs_es = elegir(j)
        peso = '%.1f MB' % (int(j['format'].get('size') or 0) / 1048576)
        if aud is None:
            print('  %-46s %-9s %-6s %-9s %s' % (nom[:46], 'NO', '-', peso, 'SALTADO: sin audio en espanol'))
            lineas.append([nom, 'no', 'sin audio en espanol - no se codifica']); sal_n += 1; continue
        dst = os.path.join(a.salida, os.path.splitext(nom)[0] + '.mp4')
        if os.path.exists(dst):
            print('  %-46s %-9s %-6s %-9s %s' % (nom[:46], 'si', '-', peso, 'YA EXISTE (se salta)'))
            lineas.append([nom, 'si', 'ya existia']); continue
        marca_sub = 'si(idx %d)' % sub if sub is not None else 'NO SE QUEMA'
        ok, msg = codificar(f, dst, vid, aud, sub, tmp)
        if ok:
            ok_n += 1
            print('  %-46s %-9s %-6s %-9s %s' % (nom[:46], 'si', marca_sub, peso, msg))
            lineas.append([nom, 'si', 'forzados ' + marca_sub + ' · ' + msg])
        else:
            err_n += 1
            print('  %-46s %-9s %-6s %-9s %s' % (nom[:46], 'si', marca_sub, peso, 'FALLA: ' + msg))
            lineas.append([nom, 'si', 'FALLA: ' + msg])
    try:
        os.rmdir(tmp)
    except OSError:
        pass
    print('')
    print('  RESUMEN: %d codificados · %d saltados · %d con error' % (ok_n, sal_n, err_n))
    with open(LOG, 'w', encoding='utf-8-sig') as fh:
        fh.write('\n'.join('\t'.join(x) for x in lineas) + '\n')
    print('  Registro: ' + LOG)
    return 1 if err_n else 0

if __name__ == '__main__':
    sys.exit(main())
