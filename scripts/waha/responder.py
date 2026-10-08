#!/usr/bin/env python3
"""
RESPONDER — C1 (motor de respuestas humanas) + C2 (compuerta de aprobacion)
Seawolf Agent · Capa 2

Arquitectura: el BUS es la columna. Todo saliente hacia un tercero pasa por la compuerta.
- proponer(destino, texto, nivel): el agente NO envia; manda la PROPUESTA al dueno (L1).
- El dueno responde por WhatsApp (texto libre = orden; 'ok'/'1'/'no'/'silencio Nh' = atajos).
- El filtro publica esos mensajes del dueno al bus como kind='order'.
- Este motor los lee y ejecuta: envia con mecanica HUMANA (seen + typing + pausa + envio).

Reglas del Monarca:
- Texto libre SIEMPRE posible (asi sea emergencia) — un menu cerrado falla cuando mas importa.
- Latencia del modelo = invisible; el aviso 'escribiendo' va SOLO los ultimos segundos.
- Bot no se delata por lento sino por rapido: 1a respuesta no urgente 15s-3min aleatorio.
- 🔥 = rapido (la seguridad pesa mas que el realismo).
- Deny-by-default: nada sale a un tercero sin aprobacion (salvo regla preaprobada explicita).
"""
import json
import os
import random
import re
import sys
import time
import urllib.request
import uuid

DIR = os.path.dirname(os.path.abspath(__file__))
BUS_DB = os.environ.get("SEAWOLF_BUS_DB", "/opt/waha/bus.db")
PEND = os.path.join(DIR, "pendientes.json")
TENANTF = os.path.join(DIR, "tenant.json")
LOG = os.path.join(DIR, "responder.log")
ESTADO = os.path.join(DIR, "responder_estado.json")   # ultimo evento procesado

WAHA_URL = os.environ.get("WAHA_URL", "http://127.0.0.1:3000")
WAHA_KEY = os.environ["WAHA_API_KEY"]
SELF = os.environ.get("SELF_CHAT", "")            # chat del dueno donde llega la propuesta

# --- ritmo (configurable para pruebas) ---
TEST_FAST = os.environ.get("RESPONDER_TEST_FAST", "0") == "1"
ESPERA_NO_URGENTE = (4, 8) if TEST_FAST else (15, 180)   # segundos
ESPERA_URGENTE = (2, 4)
TOPE_ENVIOS_HORA = int(os.environ.get("RESPONDER_TOPE_HORA", "20"))
SEG_POR_15CHARS = 0.6                                      # duracion del "escribiendo"
TYPING_MAX = 4.0

sys.path.insert(0, DIR)
try:
    import bus
except Exception as e:                                          # pragma: no cover
    bus = None
    print("AVISO: sin bus (%s)" % e)


# ---------------------------------------------------------------- utilidades
def _log(msg):
    linea = "%s %s" % (time.strftime("%Y-%m-%dT%H:%M:%S"), msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea, flush=True)


def _post(path, payload):
    req = urllib.request.Request(WAHA_URL + path, data=json.dumps(payload).encode(),
                                 headers={"X-Api-Key": WAHA_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.status


def tenant():
    try:
        return json.load(open(TENANTF, encoding="utf-8"))
    except Exception:
        return {}


def pendientes():
    try:
        return json.load(open(PEND, encoding="utf-8"))
    except Exception:
        return {}


def _guardar_pend(d):
    open(PEND, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))


def _estado():
    try:
        return json.load(open(ESTADO, encoding="utf-8"))
    except Exception:
        return {"ultimo_evento": 0}


def _guardar_estado(e):
    open(ESTADO, "w", encoding="utf-8").write(json.dumps(e))


def _contar_envios_hora():
    """Tope de volumen: cuantos salientes en la ultima hora (del log)."""
    hace = time.time() - 3600
    n = 0
    if not os.path.exists(LOG):
        return 0
    for l in open(LOG, encoding="utf-8", errors="replace"):
        if "ENVIADO" not in l:
            continue
        try:
            ts = time.mktime(time.strptime(l[:19], "%Y-%m-%dT%H:%M:%S"))
        except Exception:
            continue
        if ts >= hace:
            n += 1
    return n


# ---------------------------------------------------------------- mecanica humana (C1)
def enviar_humano(chat_id, texto, urgente=False):
    """seen -> typing (solo lo ultimo) -> envio. La latencia del modelo NO se muestra."""
    if _contar_envios_hora() >= TOPE_ENVIOS_HORA:
        _log("TOPE DE VOLUMEN alcanzado (%d/h). Saliente BLOQUEADO a %s" % (TOPE_ENVIOS_HORA, chat_id))
        return False

    if urgente:
        espera = random.uniform(*ESPERA_URGENTE)
    else:
        espera = random.uniform(*ESPERA_NO_URGENTE)
    _log("A la espera %.1fs antes de escribir a %s (%s)" % (espera, chat_id, "urgente" if urgente else "normal"))
    time.sleep(espera)

    # marcar como leido + aviso de escritura SOLO en la ultima parte
    for path, payload in (("/api/sendSeen", {"session": "seawolf", "chatId": chat_id}),
                          ("/api/startTyping", {"session": "seawolf", "chatId": chat_id})):
        try:
            _post(path, payload)
        except Exception as e:
            _log("  (aviso: %s no disponible: %s)" % (path, str(e)[:60]))

    dur = min(TYPING_MAX, max(1.0, len(texto) / 15.0 * SEG_POR_15CHARS * 4))
    time.sleep(dur)
    try:
        _post("/api/stopTyping", {"session": "seawolf", "chatId": chat_id})
    except Exception:
        pass
    try:
        _post("/api/sendText", {"session": "seawolf", "chatId": chat_id, "text": texto})
        _log("ENVIADO a %s: %s" % (chat_id, texto[:80]))
    except Exception as e:
        _log("ERROR al enviar a %s: %s" % (chat_id, str(e)[:120]))
        return False
    if bus:
        try:
            bus.emit(channel="whatsapp", direction="out", kind="action", text=texto,
                     peer=chat_id, actor="seawolf-agent", layer=2,
                     approved_by=(tenant().get("dueno", {}) or {}).get("nombre", "dueno"),
                     artifacts=[{"type": "approved_reply"}])
        except Exception:
            pass
    return True


# ---------------------------------------------------------------- compuerta (C2)
def proponer(destino, texto, nivel, de="un contacto", propuesta=None, mensaje=None, accion=None):
    """El agente NO envia: propone al dueno en UN SOLO mensaje (aviso + propuesta).
    Devuelve el id del pendiente."""
    pid = "p" + uuid.uuid4().hex[:6]
    d = pendientes()
    d[pid] = {"destino": destino, "texto": texto, "nivel": nivel, "de": de,
              "creado": time.strftime("%Y-%m-%dT%H:%M:%S"), "estado": "pendiente",
              "propuesta": propuesta or texto, "mensaje_original": mensaje or "", "accion": accion or ""}
    _guardar_pend(d)

    emo = {"rojo": "\U0001F525", "naranja": "\U0001F7E0"}.get(str(nivel).lower(), "\U0001F535")
    lineas = ["%s *%s — requiere su decisión*" % (emo, str(nivel).upper()),
              "\U0001F4E9 De: %s" % de]
    if mensaje:
        lineas.append("\U0001F4AC «%s»" % str(mensaje)[:300])
    if accion:
        lineas.append("\u26A1 Acción sugerida: %s" % str(accion)[:200])
    lineas += ["", "\U0001F4DD *Respuesta que propongo enviar:*",
               "«%s»" % (propuesta or texto), "",
               "Responda: *ok* o *1* → enviar · *no* → descartar",
               "…o escríbame su propia respuesta (texto libre = orden)"]
    cuerpo = "\n".join(lineas)
    try:
        _post("/api/sendText", {"session": "seawolf", "chatId": SELF, "text": cuerpo})
        _log("AVISO UNIFICADO %s enviado al dueno (%s) para %s" % (pid, SELF, destino))
    except Exception as e:
        _log("ERROR al proponer: %s" % str(e)[:120])
    if bus:
        try:
            bus.emit(channel="whatsapp", direction="out", kind="approval", text=cuerpo,
                     peer=SELF, actor="seawolf-agent", layer=2,
                     artifacts=[{"type": "proposal", "id": pid, "destino": destino, "nivel": nivel,
                                 "unificado": True}])
        except Exception:
            pass
    return pid


def procesar_orden(texto, de="dueno"):
    """Texto libre = ORDEN. Atajos son conveniencia, nunca la unica puerta."""
    t = (texto or "").strip()
    if not t:
        return
    d = pendientes()
    abiertos = [k for k, v in d.items() if v.get("estado") == "pendiente"]
    bajo = t.lower()

    # silencio
    m = re.match(r"silencio\s*(\d+)?\s*([hm])?", bajo)
    if m:
        horas = int(m.group(1) or 1)
        _guardar_estado({**_estado(), "silencio_hasta": time.time() + horas * 3600})
        _post("/api/sendText", {"session": "seawolf", "chatId": SELF,
                                "text": "🌙 Modo silencio activado por %d h (lo 🔥 seguirá pasando)." % horas})
        _log("ORDEN: silencio %dh" % horas)
        return

    if not abiertos:
        _log("ORDEN recibida sin propuestas abiertas: %s" % t[:80])
        if bus:
            bus.emit(channel="whatsapp", direction="in", kind="order_processed", text=t, peer=SELF,
                     actor=de, layer=2, artifacts=[{"type": "order", "sin_pendientes": True}])
        return

    pid = abiertos[-1]                     # la mas reciente
    p = d[pid]

    if bajo in ("ok", "1", "si", "sí", "dale", "envialo", "envíalo", "mandalo", "mándalo"):
        salida = p["propuesta"]
        accion = "aprobada tal cual"
    elif bajo in ("no", "2", "cancelar", "descartar", "nel"):
        p["estado"] = "descartada"
        _guardar_pend(d)
        _post("/api/sendText", {"session": "seawolf", "chatId": SELF, "text": "✅ Descartada. No envié nada."})
        _log("ORDEN: propuesta %s descartada" % pid)
        if bus:
            # kind='order_processed' (NO 'order'): el motor lee el bus, y si emitiera 'order'
            # se reprocesaria a si mismo en bucle infinito (bug medido 2026-10-07: 68 eventos basura).
            bus.emit(channel="whatsapp", direction="in", kind="order_processed", text=t, peer=SELF,
                     actor=de, layer=2, approved_by=None,
                     artifacts=[{"type": "order", "accion": "descartar", "id": pid}])
        return
    else:
        salida = re.sub(r"^edita:\s*", "", t, flags=re.I)   # texto libre manda
        accion = "reemplazada por instruccion del dueno"

    p["estado"] = "aprobada"
    p["enviado"] = salida
    _guardar_pend(d)
    urgente = str(p.get("nivel", "")).lower() in ("rojo", "🔥", "urgente")
    ok = enviar_humano(p["destino"], salida, urgente=urgente)
    _log("ORDEN: propuesta %s %s -> %s" % (pid, accion, "enviada" if ok else "FALLO"))
    if not ok:
        # un fallo silencioso es peor que un fallo: el dueno TIENE que enterarse
        try:
            _post("/api/sendText", {"session": "seawolf", "chatId": SELF,
                                    "text": "⚠️ No pude entregar el mensaje a ese contacto (no existe en WhatsApp o fue rechazado). El texto NO salió."})
        except Exception:
            pass
    if bus:
        # 'order_processed', nunca 'order' (evita que el motor se reprocese a si mismo)
        bus.emit(channel="whatsapp", direction="in", kind="order_processed", text=t, peer=SELF, actor=de,
                 layer=2, approved_by=(tenant().get("dueno", {}) or {}).get("nombre", "dueno"),
                 artifacts=[{"type": "order", "accion": accion, "id": pid, "nivel": p.get("nivel"),
                             "enviado": bool(ok)}])


# ---------------------------------------------------------------- redaccion (el agente piensa)
SYS_CAPA2 = """Eres el asistente operativo de {dueno}, quien administra conjuntos residenciales en Colombia.
Actuas como un humano competente y discreto, NUNCA como un bot. Espanol, tono cordial y breve.
Redactas LA RESPUESTA QUE {dueno} daria a un contacto (residente, guarda, proveedor).
Reglas:
1. Claro, conciso y concreto. Cero relleno. Si cabe en una linea, una linea (max 2-3 cortas).
2. No repites lo que el contacto ya dijo. Varias el fraseo; nada de formulas de robot.
3. No prometes lo que no se pueda cumplir ni plazos que no controlas.
4. Si es una emergencia, la respuesta empieza por la mitigacion concreta y dice a quien llamar si aplica.
5. NUNCA revelas que eres IA. Escribes como una persona ocupada y educada (0-1 emoji).
Devuelve SOLO el texto del mensaje, sin comillas ni explicaciones."""


def borrador(mensaje, nivel, de="un contacto"):
    """El agente redacta la respuesta propuesta. Latencia del modelo = invisible para el tercero."""
    key = os.environ.get("OPENROUTER_API_KEY", "")
    modelo = os.environ.get("DRAFT_MODEL", "qwen/qwen3.7-flash")
    if not key:
        return None
    prompt = ("Nivel del filtro: %s\nDe: %s\nMensaje recibido: %s\n\n"
              "Redacta la respuesta." % (nivel, de, mensaje))
    body = {"model": modelo, "temperature": 0.4, "max_tokens": 600,
            # qwen3.7-flash RAZONA: sin desactivarlo gasta todo el presupuesto en 'reasoning'
            # y devuelve content vacio (finish_reason=length). Medido 2026-10-07.
            "reasoning": {"enabled": False},
            "messages": [{"role": "system",
                          "content": SYS_CAPA2.replace("{dueno}", (tenant().get("dueno", {}) or {}).get("nombre", "el dueno"))},
                         {"role": "user", "content": prompt}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + key,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.load(r)
        txt = (d["choices"][0]["message"].get("content") or "").strip().strip('"')
        _log("BORRADOR generado con %s (%d chars)" % (modelo, len(txt)))
        return txt or None
    except Exception as e:
        _log("ERROR al redactar: %s" % str(e)[:140])
        return None


def ten_pend():
    return pendientes()


def nombre_contacto(ident):
    """Traduce un LID/numero a un nombre humano si esta en el directorio del tenant."""
    try:
        cont = tenant().get("contactos") or {}
        i = str(ident or "").strip().lower()
        if i in cont:
            return cont[i].get("nombre") or ident
        dig = "".join(ch for ch in i if ch.isdigit())
        for k, v in cont.items():
            kd = "".join(ch for ch in str(k) if ch.isdigit())
            if kd and dig and (kd in dig or dig in kd):
                return v.get("nombre") or ident
    except Exception:
        pass
    return ident


def vigilar(intervalo=3):
    """Bucle del bus:
       (a) mensajes del DUEÑO (kind='order') -> ejecutar la compuerta;
       (b) mensajes entrantes naranja/rojo -> redactar y PROPONER (nunca enviar solo)."""
    _log("RESPONDER en vigilancia (intervalo %ss, test_fast=%s, tope=%d/h)"
         % (intervalo, TEST_FAST, TOPE_ENVIOS_HORA))
    while True:
        try:  # latido: el filtro lo lee para saber si delegar el aviso (aviso unificado)
            open("/opt/waha/responder_heartbeat", "w").write(str(time.time()))
        except Exception:
            pass
        try:
            e = _estado()
            if bus:
                c = bus._conn()
                # (a) ordenes del dueno
                for r in c.execute("SELECT * FROM events WHERE id > ? AND kind='order' AND direction='in' "
                                   "ORDER BY id ASC", (int(e.get("ultimo_orden", 0)),)).fetchall():
                    r = dict(r)
                    e["ultimo_orden"] = r["id"]
                    _guardar_estado(e)
                    procesar_orden(r.get("text") or "", de=r.get("actor") or "dueno")
                # (b) entrantes que ameritan respuesta
                for r in c.execute("SELECT * FROM events WHERE id > ? AND kind='message' AND direction='in' "
                                   "ORDER BY id ASC", (int(e.get("ultimo_msg", 0)),)).fetchall():
                    r = dict(r)
                    e["ultimo_msg"] = r["id"]
                    _guardar_estado(e)
                    try:
                        arts = json.loads(r.get("artifacts") or "[]")
                    except Exception:
                        arts = []
                    cat = next((str(a.get("cat", "")).lower() for a in arts if isinstance(a, dict) and a.get("cat")), "")
                    if cat in ("rojo", "naranja"):
                        texto = r.get("text") or ""
                        de = nombre_contacto(r.get("peer") or r.get("actor") or "")
                        if de == (r.get("peer") or r.get("actor")):
                            de = r.get("actor") or r.get("peer") or "un contacto"
                        accion = next((str(a.get("accion", "")) for a in arts
                                       if isinstance(a, dict) and a.get("accion")), "")
                        txt = borrador(texto, cat, de) or "Ok, lo estoy atendiendo."
                        proponer(destino=r.get("peer") or "", texto=txt, nivel=cat, de=de,
                                 propuesta=txt, mensaje=texto, accion=accion)
                    else:
                        _log("entrante %s (%s): no amerita respuesta" % (r["id"], cat or "sin nivel"))
                c.close()
        except Exception as ex:
            _log("(error en vigilancia: %s)" % str(ex)[:120])
        time.sleep(intervalo)


# ---------------------------------------------------------------- CLI
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ayuda"
    if cmd == "vigilar":
        vigilar()
    elif cmd == "proponer":
        # proponer <destino> <nivel> <texto...>
        destino, nivel, texto = sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])
        print(proponer(destino, texto, nivel))
    elif cmd == "orden":
        procesar_orden(" ".join(sys.argv[2:]))
    elif cmd == "enviar":
        destino, texto = sys.argv[2], " ".join(sys.argv[3:])
        print(enviar_humano(destino, texto))
    elif cmd == "pendientes":
        print(json.dumps(pendientes(), ensure_ascii=False, indent=2))
    else:
        print(__doc__)
