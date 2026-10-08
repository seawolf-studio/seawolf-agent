import json, os, time, base64, subprocess, tempfile, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:  # BUS DE EVENTOS: si pasa por un canal, pasa por el bus (ver intel/arquitectura-unificada-20261007.md)
    import bus
except Exception:  # nunca tumbar el filtro por el bus
    bus = None

TENANTF = "/opt/waha/tenant.json"


def _solo_digitos(s):
    return "".join(ch for ch in str(s) if ch.isdigit())


def _cargar_owner():
    """Identidades del DUEÑO. Sus mensajes son ORDENES, no mensajes a clasificar.
    Devuelve (lids, digitos): WhatsApp puede entregar el remitente como LID opaco
    (ej. 145934583394304@lid) o como numero; hay que reconocer AMBOS."""
    try:
        t = json.load(open(TENANTF, encoding="utf-8"))
        d = t.get("dueno") or {}
        lids = {str(x).strip().lower() for x in (d.get("lid"),) if x}
        digs = {_solo_digitos(d.get(x)) for x in ("lid", "linea1") if d.get(x)}
        return lids, {x for x in digs if len(x) >= 8}
    except Exception:
        return set(), set()


OWNER_LIDS, OWNER_DIGS = _cargar_owner()


def es_dueno(ident):
    i = str(ident or "").strip().lower()
    if not i:
        return False
    if i in OWNER_LIDS:
        return True
    dig = _solo_digitos(i)
    return bool(dig) and any(od in dig for od in OWNER_DIGS)

WAHA_URL = os.environ.get("WAHA_URL", "http://127.0.0.1:3000")
WAHA_KEY = os.environ["WAHA_API_KEY"]
HEARTBEAT = "/opt/waha/responder_heartbeat"


def responder_vivo(max_edad=60):
    """El motor de respuestas escribe un latido en cada vuelta. Si esta vivo, EL propone
    (aviso unificado); si esta caido, el filtro alerta solo: nunca nos quedamos sin aviso."""
    try:
        return (time.time() - os.path.getmtime(HEARTBEAT)) < max_edad
    except Exception:
        return False
ORK = os.environ["OPENROUTER_API_KEY"]
GROQ = os.environ.get("GROQ_API_KEY", "")
SELF = os.environ.get("SELF_CHAT", "")
MODEL = os.environ.get("FILTRO_MODEL", "google/gemini-2.5-flash")
VMODEL = os.environ.get("VISION_MODEL", "google/gemini-2.5-flash")
STT = os.environ.get("STT_MODEL", "whisper-large-v3-turbo")
BIND_IP = os.environ.get("BIND_IP", "127.0.0.1")
BIND_PORT = int(os.environ.get("BIND_PORT", "3011"))
LOG = "/opt/waha/filtro.log"

try:  # CRITERIO en su propio archivo: es doctrina de negocio, no codigo del filtro
    from criterio import SYS, classify
except Exception:  # nunca tumbar el filtro: si falla, el criterio local de abajo
    SYS = ""
    classify = None


def _post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


# classify() y SYS viven en criterio.py (unica fuente de verdad del criterio de negocio).


def send_self(text):
    if not SELF:
        return
    try:
        _post_json(WAHA_URL + "/api/sendText",
                   {"session": "seawolf", "chatId": SELF, "text": text}, {"X-Api-Key": WAHA_KEY})
    except Exception:
        pass


def log(rec):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def media_kind(mt):
    mt = (mt or "").lower()
    if mt.startswith("audio"):
        return "nota de voz"
    if mt.startswith("image"):
        return "imagen"
    if mt.startswith("video"):
        return "video"
    if mt.startswith("application"):
        return "documento"
    return "archivo"


def ext_for(mt):
    mt = (mt or "").lower()
    for k, v in [("ogg", "ogg"), ("mpeg", "mp3"), ("mp3", "mp3"), ("wav", "wav"), ("jpeg", "jpg"),
                 ("jpg", "jpg"), ("png", "png"), ("webp", "webp"), ("mp4", "mp4"), ("pdf", "pdf")]:
        if k in mt:
            return "." + v
    return ".bin"


def download(url, dest):
    req = urllib.request.Request(url, headers={"X-Api-Key": WAHA_KEY})
    with urllib.request.urlopen(req, timeout=90) as r, open(dest, "wb") as f:
        f.write(r.read())


def transcribe(path):
    r = subprocess.run(["curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions",
                        "-H", "Authorization: Bearer " + GROQ, "-F", "file=@" + path, "-F", "model=" + STT,
                        "-F", "language=es", "-F", "response_format=json"], capture_output=True, timeout=180)
    try:
        return json.loads(r.stdout).get("text", "").strip()
    except Exception:
        return ""


def describe_image(path, mt):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    d = _post_json("https://openrouter.ai/api/v1/chat/completions",
                   {"model": VMODEL, "max_tokens": 140, "messages": [{"role": "user", "content": [
                       {"type": "text", "text": "Describe en UNA frase que muestra esta imagen (contexto: conjunto residencial en Colombia). Objetivo y breve."},
                       {"type": "image_url", "image_url": {"url": "data:" + mt + ";base64," + b64}}]}]},
                   {"Authorization": "Bearer " + ORK})
    return d["choices"][0]["message"]["content"].strip()


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        data = json.loads(self.rfile.read(n) or b"{}")
        ev = data.get("event")
        p = data.get("payload") or {}
        if ev != "message" or p.get("fromMe"):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok"); return
        frm = p.get("from") or ""
        info = (p.get("_data") or {}).get("Info") or {}
        chat = info.get("Chat") or frm
        is_group = str(chat).endswith("@g.us")
        sender = (p.get("participant") or frm) if is_group else frm
        body = (p.get("body") or "").strip()

        # --- DUEÑO = ORDEN (C2): no se clasifica ni se alerta; se publica como orden al bus ---
        if es_dueno(sender) or es_dueno(chat):
            if bus:
                try:
                    bus.emit(channel="whatsapp", direction="in", kind="order", text=body,
                             peer=str(chat), actor=str(sender), layer=2,
                             artifacts=[{"type": "order", "via": "whatsapp"}])
                except Exception:
                    pass
            log({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "from": sender, "chat": chat,
                 "group": is_group, "owner_order": True, "body": body})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return
        medi = p.get("media") or {}
        has = p.get("hasMedia")
        mt = medi.get("mimetype") or ""
        url = medi.get("url")
        kind = media_kind(mt) if has else None
        extra = ""
        tmp = None
        if has:
            if url:
                try:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext_for(mt)).name
                    download(url, tmp)
                    if mt.startswith("audio"):
                        t = transcribe(tmp)
                        extra = ("[transcripcion de " + kind + "]: " + t) if t else ("[" + kind + ": transcripcion vacia]")
                    elif mt.startswith("image"):
                        dsc = describe_image(tmp, mt)
                        extra = ("[descripcion de " + kind + "]: " + dsc) if dsc else ("[" + kind + ": descripcion vacia]")
                    else:
                        extra = "[" + kind + " adjunto]"
                except Exception as e:
                    extra = "[" + kind + ": error " + str(e)[:70] + "]"
            else:
                extra = "[" + kind + ": sin url de descarga]"
        text = " ".join(x for x in [body, extra] if x).strip()
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "from": sender, "chat": chat,
               "group": is_group, "media": kind, "body": body}
        if text:
            try:
                c = classify(text)
            except Exception as e:
                c = {"cat": "error", "motivo": str(e)[:120], "accion": ""}
            rec.update(cat=c.get("cat"), motivo=c.get("motivo"), accion=c.get("accion"), extra=extra)
            if bus:
                try:
                    bus.emit(channel="whatsapp", direction="in", kind="message", text=text,
                             peer=str(chat), actor=str(sender), layer=1,
                             artifacts=[{"type": "classification", "cat": c.get("cat"),
                                         "motivo": c.get("motivo"), "accion": c.get("accion")}])
                except Exception:
                    pass
            if c.get("cat") in ("naranja", "rojo"):
                if responder_vivo():
                    # AVISO UNIFICADO: el motor de respuestas manda UN solo mensaje
                    # (nivel + quien + accion sugerida + borrador + como responder).
                    # Asi el dueno no recibe dos avisos por lo mismo.
                    print("alerta delegada al responder (vivo)")
                else:
                    emo = {"naranja": "\U0001F7E0", "rojo": "\U0001F525"}[c["cat"]]
                    tag = "[grupo] " if is_group else ""
                    alerta = (emo + " " + c["cat"].upper() + "\n" + tag + "\U0001F4AC " + (body or extra) +
                              "\n\U0001F464 " + sender + "\n\u27A1\uFE0F " + str(c.get("accion")))
                    send_self(alerta)
                    if bus:
                        try:
                            bus.emit(channel="whatsapp", direction="out", kind="alert",
                                     text=c["cat"].upper() + " " + tag + (body or extra) +
                                          " -> " + str(c.get("accion")),
                                     peer="self:L1", actor="seawolf-agent", layer=1,
                                     artifacts=[{"type": "classification", "cat": c.get("cat"),
                                                 "accion": c.get("accion"), "de": str(sender),
                                                 "fallback": "responder_caido"}])
                        except Exception:
                            pass
            log(rec)
        if tmp:
            try:
                os.unlink(tmp)
            except Exception:
                pass
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

    def log_message(self, *a):
        pass


ThreadingHTTPServer((BIND_IP, BIND_PORT), H).serve_forever()
