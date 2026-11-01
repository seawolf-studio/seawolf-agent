#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODIFICAR CARPETA  (Seawolf Studio · Bellion)

Codifica una carpeta con los MISMOS ajustes del preset "seawolf 1080p"
(x264 veryfast, main, level 4.0, CRF 24 · AAC 192 estéreo · MP4 con capítulos),
eligiendo los detalles POR ARCHIVO, que es lo que el preset de VidCoder no puede hacer:

  1. AUDIO en ESPAÑOL (por idioma o por título). Si no hay -> SE SALTA en voz alta.
  2. SUBTÍTULOS FORZADOS quemados con el estilo clásico: abajo-centro, amarillo con borde
     negro, ~105 px en 1080, fuente Arvo si está disponible.

REPARTO EN TRES PROCESOS. No es capricho, es física medida en este Windows:

  · El proceso que corre un CODIFICADOR PESADO queda envenenado: después NO puede lanzar
    ffprobe ni nadie (CreateProcess -> rc=3221225794 = 0xC0000142) y NO se recupera ni en
    300 s (medido). Un proceso fresco, en cambio, funciona de inmediato.
  · Por eso: el SUPERVISOR solo reparte; cada CODIFICACIÓN corre en su propio proceso y
    muere; la VERIFICACIÓN corre en OTRO proceso fresco (nunca en el que codificó).
  · Con la verificación dentro del proceso que codificó, la puerta rechazaba todo.

Uso normal (escribe aparte, NUNCA toca el original):
    python codificar-carpeta.py "H:/caida/T01/Season 01" --salida "C:/.../prueba"
    python codificar-carpeta.py "<carpeta>" --simular          # el plan, sin codificar

Reemplazo en sitio (PISA el original; el original va a --respaldo-origen):
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

def probe(f, intentos=5):
    """JSON de ffprobe, o None. Reintenta con espera escalonada para el fallo acumulativo
    de recursos (rc=3221225794 = 0xC0000142) al lanzar varios seguidos."""
    global ULTIMO_ERROR
    esperas = (0.5, 1.5, 3.0, 6.0)
    for i in range(intentos):
        try:
            r = subprocess.run([FFPROBE, '-v', 'error', '-show_entries',
                'stream=index,codec_type,codec_name,width,height'
                ':stream_tags=language,title:stream_disposition=forced,default',
                '-show_entries', 'format=duration,size', '-of', 'json', f],
                capture_output=True, text=True, encoding='utf-8', errors='replace')
            if r.returncode == 0:
                return json.loads(r.stdout)
            ULTIMO_ERROR = (r.stderr or '').strip().replace('\n', ' ')[:150] or ('rc=%d sin mensaje' % r.returncode)
        except Exception as e:
            ULTIMO_ERROR = str(e)[:150]
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
    """(inicio,fin) del primer forzado del origen, SIN codificar."""
    if sub is None:
        return None
    asf = os.path.join(tmp, 'subs_chk.srt')
    r = subprocess.run([FFMPEG, '-y', '-v', 'error', '-i', src, '-map', '0:%d' % sub,
                        '-c:s', 'srt', asf], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0 or not os.path.exists(asf):
        return None
    return primer_evento(asf)

def _frame(video, t, png, cwd):
    if os.path.exists(png):
        os.remove(png)
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
        # (medido: 994 px de alto en vez de 105). Se quita la etiqueta.
        with open(asf, encoding='utf-8-sig', errors='replace') as fh:
            texto = re.sub(r'</?font[^>]*>', '', fh.read())
        with open(asf, 'w', encoding='utf-8') as fh:
            fh.write(texto)
        fuente = ''                                    # fuente de marca si esta disponible
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
    cmd = [FFMPEG, '-y', '-v', 'warning', '-i', src,
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

def dst_de(a, f):
    return os.path.join(a.salida, os.path.splitext(os.path.basename(f))[0] + '.mp4')

def tmp_de(a):
    t = os.path.join(a.salida, '_tmp'); os.makedirs(t, exist_ok=True); return t

# ---------------------------------------------------------------- proceso 2: CODIFICAR
def codificar_uno(a, f):
    """En ESTE proceso que va a morir: probar el origen, elegir y codificar. NADA mas:
    despues del codificador este proceso ya no puede lanzar ffprobe."""
    nom = os.path.basename(f)
    j = probe(f)
    if not j:
        return 'ILEGIBLE', ULTIMO_ERROR or 'sin motivo', '', '', ''
    vid, aud, sub, ra, rs = elegir(j)
    if aud is None:
        return 'SALTADO', ra, '', '', ''
    dur_src = j['format'].get('duration') or '0'
    os.makedirs(a.salida, exist_ok=True)
    dst = dst_de(a, f)
    # en modo reemplazo el resultado ES un mp4 en la carpeta de origen: si ya tiene su
    # contraparte en _nuevos, ese archivo ya se reemplazo antes y NO se vuelve a tocar.
    if a.reemplazar and nom.lower().endswith('.mp4') and os.path.exists(dst):
        return 'YA EXISTE', 'ya reemplazado antes', '', '', ''
    if os.path.exists(dst) and not a.reemplazar:
        return 'YA EXISTE', nom, '', '', ''
    if os.path.exists(dst):                     # reanudar: ya codificado
        return 'CODIFICADO', 'ya estaba codificado', ra, rs, dur_src
    ok, msg = codificar(f, dst, vid, aud, sub, tmp_de(a))
    if not ok:
        return 'FALLA', msg, ra, rs, ''
    return 'CODIFICADO', msg, ra, rs, dur_src

# ---------------------------------------------------------- proceso 3: VERIFICAR Y PONER
def verificar_uno(a, f):
    """En ESTE proceso fresco (que nunca codifica): la PUERTA y, si pasa, el reemplazo."""
    j = probe(f)
    if not j:
        return 'PUERTA FALLA', ULTIMO_ERROR or 'no se pudo leer el original', ''
    vid, aud, sub, ra, rs = elegir(j)
    dur_src = float(j['format'].get('duration') or 0)
    dst = dst_de(a, f)
    if not os.path.exists(dst):
        return 'PUERTA FALLA', 'no esta la salida', ''
    evento = evento_de(f, sub, tmp_de(a)) if sub is not None else None
    vok, vmsg = verificar_salida(f, dst, evento, dur_src, tmp_de(a))
    if not vok:
        try:
            os.remove(dst)
        except OSError:
            pass
        return 'RECHAZADO', vmsg, rs
    if a.reemplazar:
        rel = os.path.relpath(f, a.origen)
        resp = os.path.join(a.respaldo_origen, rel)
        try:
            os.makedirs(os.path.dirname(resp), exist_ok=True)
            shutil.move(f, resp)                            # el original queda a salvo
            final = os.path.join(os.path.dirname(f), os.path.splitext(os.path.basename(f))[0] + '.mp4')
            shutil.move(dst, final)
        except OSError as e:
            return 'FALLA al reemplazar', str(e)[:90], rs
        return 'REEMPLAZADO', vmsg, rs
    return 'OK', vmsg, rs

def main():
    ap = argparse.ArgumentParser(description='Codifica una carpeta con los ajustes del preset seawolf 1080p')
    ap.add_argument('origen', help='carpeta con los archivos fuente (recursivo)')
    ap.add_argument('--salida', help='carpeta de salida aparte (por defecto <origen>/_nuevos si --reemplazar)')
    ap.add_argument('--reemplazar', action='store_true',
                    help='PISA el original: el original se mueve a --respaldo-origen antes de poner el nuevo')
    ap.add_argument('--respaldo-origen', default='J:/_origenes-reemplazados',
                    help='donde se guardan los originales reemplazados')
    ap.add_argument('--simular', action='store_true',
                    help='mostrar el plan por archivo (que se queda y que se tira) SIN codificar')
    ap.add_argument('--solo', help='procesar unicamente los que contengan este texto')
    ap.add_argument('--log', help='archivo de registro (por defecto <salida>/codificacion.log)')
    ap.add_argument('--un-archivo', dest='un_archivo', help='INTERNO: codifica este archivo y sale')
    ap.add_argument('--verificar', help='INTERNO: verifica (y pone) este archivo ya codificado y sale')
    a = ap.parse_args()

    if not os.path.isdir(a.origen):
        print('  ERROR: no existe ' + a.origen); return 2
    if not a.salida:
        if a.reemplazar:
            a.salida = os.path.join(a.origen, '_nuevos')
        elif a.simular:
            a.salida = a.origen          # simulacion: no se escribe nada
        else:
            print('  ERROR: indica --salida (o usa --reemplazar para codificar en sitio)'); return 2

    # ---- procesos hijos: uno hace UNA sola cosa y muere ----
    if a.un_archivo:
        e, d, ra, rs, dur = codificar_uno(a, a.un_archivo)
        print('%s\t%s\t%s\t%s\t%s\t%s' % (e, os.path.basename(a.un_archivo), d, ra, rs, dur))
        return 2 if e in ('FALLA', 'ILEGIBLE') else 0
    if a.verificar:
        e, d, rs = verificar_uno(a, a.verificar)
        print('%s\t%s\t%s\t%s' % (e, os.path.basename(a.verificar), d, rs))
        return 2 if e in ('RECHAZADO', 'PUERTA FALLA', 'FALLA al reemplazar') else 0

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

    if not a.simular:
        os.makedirs(a.salida, exist_ok=True)
        os.makedirs(os.path.join(a.salida, '_tmp'), exist_ok=True)
    LOG = a.log or os.path.join(a.salida, 'codificacion.log')

    print('  %d archivo(s) · salida: %s' % (len(fuentes), a.salida))
    if a.reemplazar:
        print('  MODO REEMPLAZO: los originales se guardan en ' + a.respaldo_origen)
    print('  %-46s %-15s %s' % ('ARCHIVO', 'ESTADO', 'DETALLE'))
    print('  ' + '-' * 116)

    # ---- simulacion: barata, cabe en un proceso ----
    if a.simular:
        for f in fuentes:
            time.sleep(0.15)
            j = probe(f)
            nom = os.path.basename(f)
            if not j:
                print('  %-46s %-15s %s' % (nom[:46], 'ILEGIBLE', ULTIMO_ERROR)); continue
            vid, aud, sub, ra, rs = elegir(j)
            vv = [s for s in j['streams'] if s['index'] == vid]
            vv = vv[0] if vv else {}
            w, h = vv.get('width') or 0, vv.get('height') or 0
            salida_v = '1080p' if h > MAX_ALTO else '%dx%d' % (w, h)
            na = len([s for s in j['streams'] if s['codec_type'] == 'audio'])
            ns = len([s for s in j['streams'] if s['codec_type'] == 'subtitle'])
            print('  %-46s %s %dx%d->%-7s | de %d audio: %-22s | de %d subs: %s'
                  % (nom[:46], vv.get('codec_name') or '?', w, h, salida_v, na, ra[:22], ns, rs))
        return 0

    # ---- real: el SUPERVISOR solo reparte; nunca codifica ni verifica ----
    script = os.path.abspath(__file__)
    lineas, cuenta = [], {}

    def corre(extra):
        cmd = [sys.executable, script, a.origen, '--salida', a.salida]
        if a.reemplazar:
            cmd += ['--reemplazar', '--respaldo-origen', a.respaldo_origen]
        r = subprocess.run(cmd + extra, capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        sal = (r.stdout or '').strip().splitlines()
        return (sal[-1] if sal else '').split('\t')

    for f in fuentes:
        p = corre(['--un-archivo', f])
        estado, nombre = (p[0], p[1]) if len(p) > 1 else ('SIN RESPUESTA', os.path.basename(f))
        detalle = p[2] if len(p) > 2 else ''
        rs = p[4] if len(p) > 4 else ''
        if estado != 'CODIFICADO':
            cuenta[estado] = cuenta.get(estado, 0) + 1
            print('  %-46s %-15s %s' % (nombre[:46], estado, detalle[:52]))
            lineas.append([nombre, estado, detalle])
            continue
        # la PUERTA va en OTRO proceso fresco: el que codifico esta envenenado
        time.sleep(2.0)
        q = corre(['--verificar', f])
        # el hijo de verificar a veces no arranca justo despues del codificador: reintentar
        for espera in (4, 10, 25):
            if q and q[0]:
                break
            time.sleep(espera)
            q = corre(['--verificar', f])
        estado2 = q[0] if q else 'SIN RESPUESTA'
        detalle2 = q[2] if len(q) > 2 else ''
        rs2 = q[3] if len(q) > 3 else rs
        cuenta[estado2] = cuenta.get(estado2, 0) + 1
        print('  %-46s %-15s %s' % (nombre[:46], estado2, (rs2 + ' | ' + detalle2)[:52]))
        lineas.append([nombre, estado2, rs2 + ' | ' + detalle2])

    print('')
    print('  RESUMEN: ' + ' · '.join('%s %d' % (k, v) for k, v in sorted(cuenta.items())))
    with open(LOG, 'w', encoding='utf-8-sig') as fh:
        fh.write('\n'.join('\t'.join(x) for x in lineas) + '\n')
    print('  Registro: ' + LOG)
    malos = ('FALLA', 'RECHAZADO', 'ILEGIBLE', 'SIN RESPUESTA', 'PUERTA FALLA', 'FALLA al reemplazar')
    return 0 if not any(cuenta.get(k, 0) for k in malos) else 1

if __name__ == '__main__':
    sys.exit(main())
