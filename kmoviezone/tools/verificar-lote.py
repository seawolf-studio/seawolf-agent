#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR DEL LOTE  (Seawolf Studio · Bellion)

Para qué: revisar los .mp4 que salen de VidCoder SIN abrirlos uno por uno.
Qué hace: lee cada archivo con ffprobe (solo lectura, no toca nada) y dice
          si trae el audio en español, si el video quedó en H.264/MP4 y cómo
          quedaron los subtítulos.

Uso:
    python verificar-lote.py "H:/caida/EX01"
    python verificar-lote.py "H:/caida" --solo-fallos
    python verificar-lote.py "H:/caida" --csv informe.csv

Regla del lote (la del Monarca): AUDIO EN ESPAÑOL, VIDEO H.264 en MP4,
SUBTÍTULOS en español (quemados o como pista). Lo que no cumpla, se marca.
"""
import argparse, json, os, subprocess, sys

FFPROBE = (r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages"
           r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
           r"\ffmpeg-8.1.2-full_build\bin\ffprobe.exe")
VIDEO = ('.mp4', '.mkv')
MIN_ALTO = 480   # por debajo de esto solo se AVISA: puede ser que la fuente ya viniera asi

def probe(f, intentos=3):
    """Devuelve el JSON de ffprobe del archivo, o None si ffprobe falla.

    Reintenta: mientras VidCoder/HandBrake está escribiendo un archivo, ffprobe
    falla de forma intermitente (a veces sin mensaje). Un archivo recién escrito
    no es un archivo roto."""
    import time
    for i in range(intentos):
        try:
            r = subprocess.run(
                [FFPROBE, '-v', 'error',
                 '-show_entries', 'stream=index,codec_type,codec_name,width,height'
                                  ':stream_tags=language,title:stream_disposition=default',
                 '-show_entries', 'format=format_name,duration,size',
                 '-of', 'json', f],
                capture_output=True, text=True, encoding='utf-8', errors='replace')
            if r.returncode == 0:
                return json.loads(r.stdout)
        except Exception:
            pass
        if i < intentos - 1:
            time.sleep(0.7)
    return None

def leer(f):
    """Extrae lo que importa de un archivo."""
    j = probe(f)
    if not j:
        return None
    d = {'archivo': f, 'vcodec': None, 'ancho': 0, 'alto': 0,
         'audios': [], 'subs': [], 'dur': 0.0, 'peso': 0, 'cont': ''}
    for s in j.get('streams', []):
        t = s.get('codec_type')
        lang = (s.get('tags') or {}).get('language', '?')
        title = (s.get('tags') or {}).get('title', '')
        if t == 'video' and d['vcodec'] is None:
            d['vcodec'] = s.get('codec_name')
            d['ancho'] = s.get('width') or 0
            d['alto'] = s.get('height') or 0
        elif t == 'audio':
            d['audios'].append((lang or 'und') + ('/' + title if title else ''))
        elif t == 'subtitle':
            d['subs'].append((lang or 'und') + ('/' + title if title else ''))
    fm = j.get('format', {})
    d['dur'] = float(fm.get('duration') or 0)
    d['peso'] = int(fm.get('size') or 0)
    d['cont'] = (fm.get('format_name') or '')   # completo: "mov,mp4,m4a,3gp,3g2,mj2" para un mp4
    return d

def idiomas(lista):
    return ', '.join(x.split('/')[0] for x in lista)

def evaluar(d, modo='resultado'):
    """Devuelve (ok, problemas, avisos). ok = sin problemas."""
    if not d:
        return False, ['no se pudo leer (¿lo está escribiendo VidCoder?)'], []
    p, av = [], []
    if not d['audios']:
        p.append('SIN AUDIO')
    elif not any(a.startswith('spa') for a in d['audios']):
        p.append('sin audio en espanol (tiene: ' + idiomas(d['audios']) + ')')

    if modo == 'resultado':
        if 'mp4' not in d['cont']:
            p.append('no es MP4 (es ' + (d['cont'] or '?') + ')')
        if d['vcodec'] != 'h264':
            p.append('video ' + str(d['vcodec']) + ' (debe ser h264)')
        if d['subs'] and not any(s.startswith('spa') for s in d['subs']):
            p.append('subs sin espanol (' + idiomas(d['subs']) + ')')
        if d['dur'] < 5:
            p.append('duracion sospechosa (' + str(round(d['dur'], 1)) + ' s)')

    if d['alto'] and d['alto'] < MIN_ALTO:
        av.append('resolucion baja ' + str(d['ancho']) + 'x' + str(d['alto']) + ' (¿la fuente ya venia asi?)')
    return (len(p) == 0), p, av

def mb(n):
    return round(n / 1048576, 1)

def main():
    ap = argparse.ArgumentParser(description='Verificador del lote de VidCoder (solo lectura)')
    ap.add_argument('raiz', help='carpeta a revisar, ej "H:/caida/EX01"')
    ap.add_argument('--modo', choices=['resultado', 'original'], default='resultado',
                    help='resultado = mp4/h264/espanol (por defecto) · original = la fuente mkv/hevc')
    ap.add_argument('--csv', help='escribir el detalle en un CSV')
    ap.add_argument('--solo-fallos', action='store_true', help='mostrar unicamente los que fallan')
    a = ap.parse_args()

    if not os.path.isdir(a.raiz):
        print('  ERROR: no existe la carpeta ' + a.raiz)
        return 2

    archivos = []
    for base, _, fs in os.walk(a.raiz):
        for f in fs:
            if f.lower().endswith(VIDEO):
                archivos.append(os.path.join(base, f))
    archivos.sort()
    if not archivos:
        print('  No se encontraron videos en ' + a.raiz)
        return 0

    print('  Modo: %s · revisando %d archivos con ffprobe (solo lectura)...' % (a.modo, len(archivos)))
    filas, fallos, con_aviso = [], 0, 0
    for f in archivos:
        d = leer(f)
        ok, probs, av = evaluar(d, a.modo)
        if not ok:
            fallos += 1
        if av:
            con_aviso += 1
        filas.append((d, ok, probs, av))

    print('')
    print('  %-50s %8s %9s %-16s %s' % ('ARCHIVO', 'DUR', 'PESO(MB)', 'AUDIO', 'ESTADO'))
    print('  ' + '-' * 118)
    for d, ok, probs, av in filas:
        if a.solo_fallos and ok:
            continue
        if not d:
            print('  %-50s %8s %9s %-16s %s' % ('(ilegible)', '-', '-', '-', 'FALLA'))
            continue
        nom = os.path.basename(d['archivo'])[:50]
        au = idiomas(d['audios']) or '—'
        if not ok:
            est = 'FALLA: ' + '; '.join(probs)
        elif av:
            est = 'OK · aviso: ' + '; '.join(av)
        else:
            est = 'OK'
        print('  %-50s %8.1f %9.1f %-16s %s' % (nom, d['dur'], mb(d['peso']), au[:16], est))

    print('')
    print('  RESUMEN: %d archivos · %d OK · %d con falla · %d con aviso'
          % (len(filas), len(filas) - fallos, fallos, con_aviso))
    if a.modo == 'resultado' and fallos:
        print('  ("sin audio en espanol" = ese archivo NO se publica hasta revisarlo)')

    if a.csv:
        import csv
        with open(a.csv, 'w', newline='', encoding='utf-8-sig') as fh:
            w = csv.writer(fh, delimiter=';')
            w.writerow(['archivo', 'duracion_s', 'peso_mb', 'video', 'resolucion',
                        'audios', 'subs', 'estado', 'problemas', 'avisos'])
            for d, ok, probs, av in filas:
                if not d:
                    continue
                w.writerow([d['archivo'], round(d['dur'], 1), mb(d['peso']), d['vcodec'],
                            '%dx%d' % (d['ancho'], d['alto']), ' | '.join(d['audios']),
                            ' | '.join(d['subs']) or '(quemados)', 'OK' if ok else 'FALLA',
                            '; '.join(probs), '; '.join(av)])
        print('  CSV escrito en ' + a.csv)
    return 1 if fallos else 0

if __name__ == '__main__':
    sys.exit(main())
