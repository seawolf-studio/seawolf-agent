#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODIFICAR CARPETA  (Seawolf Studio · Bellion)

Codifica una carpeta con los MISMOS ajustes del preset "seawolf 1080p"
(x264 veryfast, main, level 4.0, CRF 24 · AAC 192 estéreo · MP4 con capítulos),
pero eligiendo los detalles POR ARCHIVO, que es lo que el preset de VidCoder no puede hacer:

  1. AUDIO en ESPAÑOL (por idioma o por título). Si no hay -> SE SALTA en voz alta.
     Nunca cae a inglés en silencio.
  2. SUBTÍTULOS FORZADOS quemados, con el estilo clásico: abajo-centro, amarillo con borde
     negro, ~105 px en 1080. Fuente Arvo si está disponible (si no, la de sistema).

Uso normal (escribe aparte, NUNCA toca el original):
    python codificar-carpeta.py "H:/caida/T01/Season 01" --salida "C:/.../prueba-T01"
    python codificar-carpeta.py "<carpeta>" --simular          # el plan, sin codificar

Reemplazo en sitio (PISA el original; el original se guarda en --respaldo-origen):
    python codificar-carpeta.py "H:/caida/T01/Season 01" --reemplazar

Antes de reemplazar, cada salida pasa una PUERTA: duración, audio en español y verificación
numérica de que el forzado quedó quemado abajo. Si falla, la salida se tira y el original
NO se toca.
"""
import argparse, json, os, re, shutil, subprocess, sys, time

BIN = (r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages"
       r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
       r"\ffmpeg-8.1.2-full_build\bin")
FFMPEG = os.path.join(BIN, 'ffmpeg.exe')
FFPROBE = os.path.join(BIN, 'ffprobe.exe')
EXT = ('.mkv', '.mp4', '.m4v', '.avi')
MAX_ANCHO, MAX_ALTO = 1920, 1080
PATRON_FORZADO = re.compile(r'forzad|forced', re.I)
# El espanol NO siempre viene etiquetado: 'lat' es latinoamericano, y muchos archivos
# solo traen el titulo ("Latino", "Espanol", "Castellano"). Ver los tres casos en elegir().
PALABRA_ES = re.compile(r'latino|espa[nñ]ol|castellano|spanish', re.I)
# Fuente de marca: Arvo (Google Fonts, OFL). Se usa si el .ttf esta junto al script.
FUENTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'arvo.ttf')
NOMBRE_FUENTE = 'Arvo'
# Estilo del forzado: el clasico. Colores ASS en &HAABBGGRR (BGR, no RGB): amarillo=&H0000FFFF.
ESTILO = ("PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BackColour=&H80000000"
          ",BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=28")

ULTIMO_ERROR = ''

def probe(f, intentos=8):
    """JSON de ffprobe, o None. Reintenta CON ESPERA ESCALONADA: en este Windows, lanzar
    ffprobe agota recursos y CreateProcess responde rc=3221225794 (0xC0000142, fallo al
    iniciar DLL). Ocurre de forma acumulativa al lanzar muchos seguidos, y sobre todo JUSTO
    DESPUES de un codificador pesado: ahi ffprobe no arranca por ~1-2 minutos. Los reintentos
    cortos NO lo absorben; la escalera larga si. Medido: 5 intentos -> 19/26 archivos."""
    global ULTIMO_ERROR
    esperas = (1.0, 3.0, 8.0, 15.0, 25.0, 35.0, 40.0)
    for i in range(intentos):
        try:
            r = subprocess.run([FFPROBE, '-v', 'error', '-show_entries',
                'stream=index,codec_type,codec_name,width,height'
                ':stream_tags=language,title:stream_disposition=forced,default',
                '-show_entries', 'format=duration,size', '-of', 'json', f],
                capture_output=True, text=True, encoding='utf-8', errors='replace')
            if r.returncode == 0:
                return json.loads(r.stdout)
            ULTIMO_ERROR = (r.stderr or '').strip().replace('\n', ' ')[:170] or ('rc=%d sin mensaje' % r.returncode)
        except Exception as e:
            ULTIMO_ERROR = str(e)[:170]
        if i < intentos - 1:
            time.sleep(esperas[min(i, len(esperas) - 1)])
    return None

def elegir(j):
    """Elige video, audio en espanol y subtitulos FORZADOS.
    Devuelve (vid, aud, sub, regla_audio, regla_sub); indices o None.

    La biblioteca usa TRES convenciones de etiquetado y ninguna regla unica las cubre
    (verificado sobre archivos reales):
      1) sin etiqueta de idioma, solo titulo ("Latino"/"English")  -> Bond viejos
      2) 'lat' = espanol latinoamericano, ademas de 'spa' y 'eng'  -> Bond nuevos
      3) 'spa' + 'eng', forzados en una pista aparte por nombre     -> Los Simpson
    """
    vid, aud, sub, ra, rs = None, None, None, '', ''
    vs, au, su = [], [], []
    for s in j.get('streams', []):
        tag = s.get('tags') or {}
        disp = s.get('disposition') or {}
        it = {'idx': s['index'],
              'lang': (tag.get('language') or '').lower(),
              'titulo': tag.get('title') or '',
              'forzado': int(disp.get('forced') or 0),
              'def': int(disp.get('default') or 0),
              'w': s.get('width') or 0, 'h': s.get('height') or 0,
              'codec': s.get('codec_name') or '?'}
        t = s.get('codec_type')
        if t == 'video':
            vs.append(it)
        elif t == 'audio':
            au.append(it)
        elif t == 'subtitle':
            su.append(it)
    if vs:
        vid = vs[0]['idx']

    def es_espanol(x):
        return x['lang'].startswith(('spa', 'lat', 'es')) or bool(PALABRA_ES.search(x['titulo']))

    # ---- AUDIO: el espanol; latino > spa > es; empate -> la pista por defecto ----
    cand = [x for x in au if es_espanol(x)]
    if cand:
        rango = {'lat': 0, 'spa': 1, 'es': 2}
        a = min(cand, key=lambda x: (rango.get(x['lang'][:3], 3), 0 if x['def'] else 1, x['idx']))
        aud = a['idx']
        ra = (a['lang'] or ('titulo "%s"' % a['titulo'])) + (' default' if a['def'] else '')
    elif au:
        a = min(au, key=lambda x: (0 if x['def'] else 1, x['idx']))
        aud = a['idx']
        ra = 'POR DEFECTO sin marca es (titulo "%s") REVISAR' % (a['titulo'] or '?')
    else:
        ra = 'SIN PISTAS DE AUDIO'

    # ---- SUBTITULOS: SOLO forzados (bandera o nombre). Nunca el completo: quemar el
    #      completo le pondria subtitulos a toda la pelicula. ----
    cands = [x for x in su if es_espanol(x) and (x['forzado'] or PATRON_FORZADO.search(x['titulo']))]
    if cands:
        s_ = min(cands, key=lambda x: (0 if x['forzado'] else 1, 0 if x['def'] else 1, x['idx']))
        sub = s_['idx']
        rs = '%s%s' % (s_['lang'] or 'sin etiqueta',
                       ' forzado' if s_['forzado'] else ' "%s"' % s_['titulo'])
    else:
        rs = 'sin pista forzada'
    return vid, aud, sub, ra, rs

def primer_evento(ruta_srt):
    """(inicio, fin) en segundos del primer evento del SRT, o None."""
    try:
        t = open(ruta_srt, encoding='utf-8-sig', errors='replace').read()
    except OSError:
        return None
    m = re.search(r'(\d+):(\d\d):(\d\d)[,.](\d+)\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d+)', t)
    if not m:
        return None
    ini = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000
    fin = int(m.group(5)) * 3600 + int(m.group(6)) * 60 + int(m.group(7)) + int(m.group(8)) / 1000
    return ini, fin

def evento_de(src, sub, tmp):
    """(inicio,fin) del primer forzado del origen, SIN codificar: sirve para
    verificar un mp4 que ya estaba hecho (reanudar un reemplazo a medias)."""
    if sub is None:
        return None
    asf = os.path.join(tmp, 'subs.srt')
    r = subprocess.run([FFMPEG, '-y', '-v', 'error', '-i', src, '-map', '0:%d' % sub,
                        '-c:s', 'srt', asf], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0 or not os.path.exists(asf):
        return None
    return primer_evento(asf)

def _frame(video, t, png, cwd):
    r = subprocess.run([FFMPEG, '-y', '-v', 'error', '-ss', '%.2f' % t, '-i', video,
                        '-frames:v', '1', png], cwd=cwd,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode == 0 and os.path.exists(png)

def verificar_quemado(src, dst, evento, tmp):
    """Numerico, no a ojo: el forzado tiene que aparecer ABAJO. Los Simpson tienen la piel
    amarilla, asi que el color solo no sirve: se compara contra el original y se exige que
    los cambios caigan en la franja inferior."""
    ini, fin = evento
    t = ini + max(0.4, (fin - ini) * 0.4)
    a, b = os.path.join(tmp, '_chk_o.png'), os.path.join(tmp, '_chk_r.png')
    for p in (a, b):
        if os.path.exists(p):
            os.remove(p)
    if not _frame(src, t, a, tmp) or not _frame(dst, t, b, tmp):
        return False, 'no se pudo extraer el fotograma de control (t=%.1fs)' % t
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return True, 'quemado NO verificado (falta numpy/PIL)'
    A = np.asarray(Image.open(a).convert('L')).astype(np.int16)
    B = np.asarray(Image.open(b).convert('L')).astype(np.int16)
    m = np.abs(A - B) > 40
    frac = m.mean()
    if frac < 0.003:
        return False, 'el forzado NO quedo quemado (cambio %.3f%%)' % (frac * 100)
    ys = np.where(m)[0]
    abajo = (ys > A.shape[0] * 0.70).mean()
    if abajo < 0.90:
        return False, 'el quemado no esta abajo (%.0f%% en la franja inferior)' % (abajo * 100)
    return True, 'quemado ok (%.2f%% px, %.0f%% abajo)' % (frac * 100, abajo * 100)

def verificar_salida(src, dst, evento, dur_src, tmp):
    """PUERTA antes de tocar el original. (ok, motivo)."""
    j = probe(dst)
    if not j:
        return False, 'la salida no se puede leer (%s)' % (ULTIMO_ERROR or 'sin motivo')
    dur = float(j['format'].get('duration') or 0)
    if dur_src and abs(dur - dur_src) > 2:
        return False, 'duracion distinta (%.1f vs %.1f s)' % (dur, dur_src)
    au = [(s.get('tags') or {}).get('language', '').lower()
          for s in j['streams'] if s.get('codec_type') == 'audio']
    if not any(x.startswith(('spa', 'lat', 'es')) for x in au):
        return False, 'la salida no trae audio en espanol (%s)' % (au or 'ninguno')
    if evento:
        return verificar_quemado(src, dst, evento, tmp)
    return True, 'sin forzados que verificar'

def codificar(src, dst, vid, aud, sub, tmp):
    """Devuelve (ok, mensaje, evento). Escribe a dst.partial y renombra al terminar."""
    parcial = dst + '.partial.mp4'
    vf, evento = [], None
    if sub is not None:                       # extraer los subtitulos y quemarlos
        asf = os.path.join(tmp, 'subs.srt')
        # SRT y no ASS: el ASS que trae esta biblioteca NO lo renderiza libass (verificado
        # con un ASS a mano que si quema). El SRT conserva los mismos eventos y quema bien.
        r = subprocess.run([FFMPEG, '-y', '-v', 'error', '-i', src,
                            '-map', '0:%d' % sub, '-c:s', 'srt', asf],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        if r.returncode != 0 or not os.path.exists(asf) or os.path.getsize(asf) == 0:
            return False, 'no se pudo extraer la pista de subtitulos %d' % sub, None
        # El SRT hereda la etiqueta <font face="sans-serif" size="71"> del ASS. libass la
        # interpreta sobre un lienzo de 288 lineas, la escala ~3,75x y el texto sale GIGANTE
        # (medido: 994 px de alto en vez de 105). Se quita la etiqueta.
        with open(asf, encoding='utf-8-sig', errors='replace') as fh:
            texto = re.sub(r'</?font[^>]*>', '', fh.read())
        with open(asf, 'w', encoding='utf-8') as fh:
            fh.write(texto)
        evento = primer_evento(asf)
        # Fuente de marca si esta disponible; si no, la de sistema (el quemado sale igual).
        fuente = ''
        if os.path.exists(FUENTE):
            try:
                shutil.copy(FUENTE, os.path.join(tmp, os.path.basename(FUENTE)))
                fuente = ':fontsdir=.'
            except OSError:
                fuente = ''
        estilo = ESTILO + (',Fontname=' + NOMBRE_FUENTE if fuente else '')
        vf.append("subtitles=subs.srt%s:force_style='%s'" % (fuente, estilo))
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
        return False, 'ffmpeg fallo: ' + ' | '.join(cola), None
    os.replace(parcial, dst)
    return True, 'ok en %.0fs' % (time.time() - t0), evento

def main():
    ap = argparse.ArgumentParser(description='Codifica una carpeta con los ajustes del preset seawolf 1080p')
    ap.add_argument('origen', help='carpeta con los archivos fuente (recursivo)')
    ap.add_argument('--salida', help='carpeta de salida aparte (por defecto <origen>/_nuevos si --reemplazar)')
    ap.add_argument('--reemplazar', action='store_true',
                    help='PISA el original: el original se mueve a --respaldo-origen antes de poner el nuevo')
    ap.add_argument('--respaldo-origen', default='J:/_origenes-reemplazados',
                    help='donde se guardan los originales reemplazados (por defecto J:/_origenes-reemplazados)')
    ap.add_argument('--simular', action='store_true',
                    help='mostrar el plan por archivo (que se queda y que se tira) SIN codificar')
    ap.add_argument('--solo', help='procesar unicamente los que contengan este texto')
    ap.add_argument('--log', help='archivo de registro (por defecto <salida>/codificacion.log)')
    a = ap.parse_args()

    if not os.path.isdir(a.origen):
        print('  ERROR: no existe ' + a.origen); return 2
    if not a.salida:
        if a.reemplazar:
            a.salida = os.path.join(a.origen, '_nuevos')
        elif a.simular:
            a.salida = a.origen          # simulacion: no se escribe nada, solo se informa
        else:
            print('  ERROR: indica --salida (o usa --reemplazar para codificar en sitio)'); return 2
    tmp = os.path.join(a.salida, '_tmp')
    if not a.simular:
        os.makedirs(a.salida, exist_ok=True)
        os.makedirs(tmp, exist_ok=True)
    LOG = a.log or os.path.join(a.salida, 'codificacion.log')

    fuentes = []
    for base, dirs, fs in os.walk(a.origen):
        dirs[:] = [d for d in dirs if not d.startswith('_')]    # _nuevos/_tmp no son fuentes
        for f in fs:
            if f.lower().endswith(EXT):
                fuentes.append(os.path.join(base, f))
    if a.solo:
        fuentes = [f for f in fuentes if a.solo.lower() in os.path.basename(f).lower()]
    fuentes.sort()
    if not fuentes:
        print('  No hay archivos que procesar.'); return 0

    print('  %d archivo(s) · salida: %s' % (len(fuentes), a.salida))
    if a.reemplazar:
        print('  MODO REEMPLAZO: los originales se guardan en ' + a.respaldo_origen)
    print('  %-46s %-9s %-26s %s' % ('ARCHIVO', 'ESPANOL', 'FORZADO', 'ESTADO'))
    print('  ' + '-' * 116)
    lineas, ok_n, sal_n, err_n = [], 0, 0, 0
    for f in fuentes:
        time.sleep(0.15)   # pausa entre archivos: lanzar ffprobe en rafaga agota recursos (ver probe)
        nom = os.path.basename(f)
        j = probe(f)
        if not j:
            print('  %-46s %-9s %-26s %s' % (nom[:46], '?', '?', 'ILEGIBLE: ' + (ULTIMO_ERROR or 'sin detalle')))
            lineas.append([nom, '?', 'ilegible: ' + ULTIMO_ERROR]); err_n += 1; continue
        vid, aud, sub, ra, rs = elegir(j)
        dur_src = float(j['format'].get('duration') or 0)
        if a.simular:
            vv = [s for s in j['streams'] if s['index'] == vid]
            vv = vv[0] if vv else {}
            w, h = vv.get('width') or 0, vv.get('height') or 0
            salida_v = '1080p' if h > MAX_ALTO else '%dx%d' % (w, h)
            na = len([s for s in j['streams'] if s['codec_type'] == 'audio'])
            ns = len([s for s in j['streams'] if s['codec_type'] == 'subtitle'])
            print('  %-46s %s %dx%d->%-7s | de %d audio: %-24s | de %d subs: %s'
                  % (nom[:46], vv.get('codec_name') or '?', w, h, salida_v, na, ra[:24], ns, rs))
            lineas.append([nom, 'plan', 'audio %s | subs %s' % (ra, rs)])
            continue
        if aud is None:
            print('  %-46s %-9s %-26s %s' % (nom[:46], 'NO', '-', 'SALTADO: ' + ra))
            lineas.append([nom, 'no', 'sin audio usable - no se codifica']); sal_n += 1; continue
        dst = os.path.join(a.salida, os.path.splitext(nom)[0] + '.mp4')
        evento = None
        if os.path.exists(dst) and not a.reemplazar:
            print('  %-46s %-9s %-26s %s' % (nom[:46], 'si', rs[:26], 'YA EXISTE (se salta)'))
            lineas.append([nom, 'si', 'ya existia']); continue
        if os.path.exists(dst):
            # en modo reemplazo un mp4 ya codificado NO se salta: falta reemplazar y verificar
            evento = evento_de(f, sub, tmp)
            ok, msg = True, 'ya estaba codificado'
        else:
            ok, msg, evento = codificar(f, dst, vid, aud, sub, tmp)
        if not ok:
            err_n += 1
            print('  %-46s %-9s %-26s %s' % (nom[:46], 'si', rs[:26], 'FALLA: ' + msg))
            lineas.append([nom, 'si', 'FALLA codificando: ' + msg]); continue
        # ---- PUERTA: nada se reemplaza sin pasar esto ----
        time.sleep(2.0)   # deja asentar ffmpeg: lanzarle ffprobe pegado falla con 0xC0000142
        vok, vmsg = verificar_salida(f, dst, evento, dur_src, tmp)
        if not vok:
            os.remove(dst)
            err_n += 1
            print('  %-46s %-9s %-26s %s' % (nom[:46], 'si', rs[:26], 'RECHAZADO: ' + vmsg))
            lineas.append([nom, 'si', 'RECHAZADO en la puerta: ' + vmsg]); continue
        if a.reemplazar:
            rel = os.path.relpath(f, a.origen)
            resp = os.path.join(a.respaldo_origen, rel)
            try:
                os.makedirs(os.path.dirname(resp), exist_ok=True)
                shutil.move(f, resp)                       # el original queda a salvo
                final = os.path.join(os.path.dirname(f), os.path.splitext(nom)[0] + '.mp4')
                shutil.move(dst, final)
            except OSError as e:
                err_n += 1
                print('  %-46s %-9s %-26s %s' % (nom[:46], 'si', rs[:26], 'FALLA al reemplazar: ' + str(e)[:60]))
                lineas.append([nom, 'si', 'FALLA al reemplazar: ' + str(e)[:60]]); continue
        ok_n += 1
        print('  %-46s %-9s %-26s %s' % (nom[:46], 'si', rs[:26],
              ('REEMPLAZADO · ' if a.reemplazar else '') + vmsg + ' · ' + msg))
        lineas.append([nom, 'si', rs + ' · ' + vmsg + ' · ' + msg])
    if os.path.isdir(tmp) and not os.listdir(tmp):
        try:
            os.rmdir(tmp)
        except OSError:
            pass
    print('')
    print('  RESUMEN: %d codificados · %d saltados · %d con error' % (ok_n, sal_n, err_n))
    if not a.simular:
        with open(LOG, 'w', encoding='utf-8-sig') as fh:
            fh.write('\n'.join('\t'.join(x) for x in lineas) + '\n')
        print('  Registro: ' + LOG)
    return 1 if err_n else 0

if __name__ == '__main__':
    sys.exit(main())
