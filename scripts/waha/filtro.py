import json, os, time, base64, subprocess, tempfile, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:  # BUS DE EVENTOS: si pasa por un canal, pasa por el bus (ver intel/arquitectura-unificada-20261007.md)
    import bus
except Exception:  # nunca tumbar el filtro por el bus
    bus = None

TENANTF = "/opt/waha/tenant.json"


def _cargar_owner_lids():
    """Identidades del DUEÑO. Sus mensajes son ORDENES, no mensajes a clasificar."""
    try:
        t = json.load(open(TENANTF, encoding="utf-8"))
        d = t.get("dueno") or {}
        return {str(x).strip().lower() for x in (d.get("lid"), d.get("linea1")) if x}
    except Exception:
        return set()


OWNER_LIDS = _cargar_owner_lids()

WAHA_URL = os.environ.get("WAHA_URL", "http://127.0.0.1:3000")
WAHA_KEY = os.environ["WAHA_API_KEY"]
ORK = os.environ["OPENROUTER_API_KEY"]
GROQ = os.environ.get("GROQ_API_KEY", "")
SELF = os.environ.get("SELF_CHAT", "")
MODEL = os.environ.get("FILTRO_MODEL", "google/gemini-2.5-flash")
VMODEL = os.environ.get("VISION_MODEL", "google/gemini-2.5-flash")
STT = os.environ.get("STT_MODEL", "whisper-large-v3-turbo")
BIND_IP = os.environ.get("BIND_IP", "127.0.0.1")
BIND_PORT = int(os.environ.get("BIND_PORT", "3011"))
LOG = "/opt/waha/filtro.log"

SYS = """Eres el Filtro de ruido de un Cliente Super Ocupado (administrador de conjuntos residenciales / empresario) en Colombia. Clasifica el mensaje en UNA categoria segun este criterio:
- rojo: URGENTE. El mensaje PERTURBA LA SEGURIDAD o requiere ATENCION INMEDIATA que no puede diferirse. Ejemplos: intrusion o ingreso no autorizado, amenaza o riesgo a personas, incendio, fuga de gas, alguien herido, estafa o fraude en curso, emergencia activa.
- naranja: puede MITIGARSE ahora y arreglarse despues. La accion DEBE empezar por la mitigacion concreta. Ejemplo: tubo roto -> cerrar el registro de agua y programar plomero; plaga -> fumigar y limpiar; dano -> asegurar y agendar reparacion.
- amarillo: consulta simple que se responde con datos.
- verde: informativo o saludo, sin accion.
Para naranja y rojo, la accion debe empezar por la medida de mitigacion concreta.
Responde SOLO JSON valido con las claves cat, motivo, accion, donde cat es rojo|naranja|amarillo|verde."""


def _post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def classify(text):
    d = _post_json("https://openrouter.ai/api/v1/chat/completions",
                   {"model": MODEL, "temperature": 0, "response_format": {"type": "json_object"},
                    "max_tokens": 400,
                    # CRITICO: qwen3.7-flash razona. Con razonamiento activado medido 13.7 s/mensaje
                    # y 11x mas caro; desactivado: 1.8 s. La Capa 1 no puede razonar en voz alta.
                    "reasoning": {"enabled": False},
                    "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": text}]},
                   {"Authorization": "Bearer " + ORK})
    return json.loads(d["choices"][0]["message"]["content"])


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
        if OWNER_LIDS and (str(sender).strip().lower() in OWNER_LIDS
                           or str(chat).strip().lower() in OWNER_LIDS):
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
                                             "accion": c.get("accion"), "de": str(sender)}])
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
