#!/usr/bin/env python3
"""
VIGILANTE DE SALUD (para los 72h sin el Monarca)
================================================
Cada 30 min comprueba servicios y sesion de WhatsApp. Solo avisa si ALGO FALLA DOS VECES
SEGUIDAS (nada de ruido) y una sola vez por incidente. Todo queda en el log y en el bus.

Diseño: no reinicia nada (systemd ya tiene Restart=always); solo VIGILA Y AVISA.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
ESTADOF = os.path.join(DIR, "healthcheck_estado.json")
LOG = os.path.join(DIR, "healthcheck.log")
WAHA_URL = os.environ.get("WAHA_URL", "http://127.0.0.1:3000")
WAHA_KEY = os.environ.get("WAHA_API_KEY", "")
SELF = os.environ.get("SELF_CHAT", "")
SERVICIOS = ["seawolf-filtro.service", "seawolf-responder.service", "waha-sink.service",
             "seawolf-webui.service"]

sys.path.insert(0, DIR)
try:
    import bus
except Exception:
    bus = None


def _log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), m))
    print(m, flush=True)


def _post(path, payload):
    req = urllib.request.Request(WAHA_URL + path, data=json.dumps(payload).encode(),
                                 headers={"X-Api-Key": WAHA_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def revisar():
    fallos = []
    for s in SERVICIOS:
        r = subprocess.run(["systemctl", "is-active", s], capture_output=True, text=True)
        if (r.stdout or "").strip() != "active":
            fallos.append("servicio %s = %s" % (s, (r.stdout or "?").strip()))
    try:
        req = urllib.request.Request(WAHA_URL + "/api/sessions/seawolf",
                                     headers={"X-Api-Key": WAHA_KEY})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        if d.get("status") != "WORKING":
            fallos.append("whatsapp = %s" % d.get("status"))
    except Exception as e:
        fallos.append("whatsapp inalcanzable (%s)" % str(e)[:40])
    return fallos


def main():
    try:
        est = json.load(open(ESTADOF, encoding="utf-8"))
    except Exception:
        est = {"seguidos": 0, "avisado": False}
    fallos = revisar()
    if not fallos:
        if est.get("seguidos"):
            _log("SALUD OK de nuevo (venia de %d fallos)" % est["seguidos"])
        est = {"seguidos": 0, "avisado": False}
        json.dump(est, open(ESTADOF, "w"))
        _log("salud OK")
        return 0
    est["seguidos"] = int(est.get("seguidos", 0)) + 1
    _log("FALLO (%d seguido%s): %s" % (est["seguidos"], "s" if est["seguidos"] > 1 else "", "; ".join(fallos)))
    if est["seguidos"] >= 2 and not est.get("avisado"):
        msg = ("⚠️ *Aviso del sistema*\nAlgo se cayó y no se levantó solo:\n" +
               "\n".join("· " + f for f in fallos) +
               "\n\n(Sigo vigilando. Si se recupera, se lo digo.)")
        try:
            _post("/api/sendText", {"session": "seawolf", "chatId": SELF, "text": msg})
            est["avisado"] = True
            _log("avisado al dueno")
        except Exception as e:
            _log("no pude avisar: %s" % str(e)[:60])
    if bus:
        try:
            bus.emit(channel="webui", direction="out", kind="health",
                     text="fallos: %s" % "; ".join(fallos), peer=SELF, actor="vigilante", layer=3,
                     artifacts=[{"type": "health", "fallos": fallos, "seguidos": est["seguidos"]}])
        except Exception:
            pass
    json.dump(est, open(ESTADOF, "w"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
