#!/usr/bin/env python3
"""
C3 — REGLAS PREAPROBADAS  (`reglas.py`)
Seawolf Agent · Capa 3

Idea: el dueño NO quiere que se le consulte todo. Define reglas ANTES:
  "quejas de mantenimiento -> avisar a Don Carlos sin preguntarme"
  "ese remitente -> responder con esta plantilla"
  "si es rojo y no respondo en 2 min -> avisa al guarda (rompe-rojo)"

Tipos de regla:
  · auto_respuesta : responde al contacto SIN aprobacion (el dueño pre-autorizo).
  · notificar      : avisa a un TERCERO (ej. Don Carlos) con el detalle.
  · rompe_rojo     : para 🔥, si el dueño no responde en N segundos, ejecuta una accion segura.

Guardas (no negociables):
  - Ninguna regla puede dispararse si el dueño la desactivo.
  - `auto_respuesta` NO aplica a 🔥 salvo que la regla diga `permitir_rojo: true`.
  - Toda accion por regla queda en el bus con approved_by="regla:<id>".
  - Si dos reglas chocan, se aplican por orden de la lista y se avisa al dueño.

Pruebas: python3 reglas.py probar
"""
import json
import os
import sys
import time
import urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
REGLASF = os.path.join(DIR, "reglas.json")
LOG = os.path.join(DIR, "reglas.log")
WAHA_URL = os.environ.get("WAHA_URL", "http://127.0.0.1:3000")
WAHA_KEY = os.environ.get("WAHA_API_KEY", "")
SELF = os.environ.get("SELF_CHAT", "")

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
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.status


def cargar():
    try:
        return json.load(open(REGLASF, encoding="utf-8"))
    except Exception:
        return {"reglas": []}


def guardar(d):
    json.dump(d, open(REGLASF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def evaluar(nivel, texto, remitente=""):
    """Devuelve las reglas activas que casan con este caso."""
    d = cargar()
    t = (texto or "").lower()
    r = (remitente or "").lower()
    salida = []
    for reg in d.get("reglas", []):
        if not reg.get("activa"):
            continue
        c = reg.get("cuando") or {}
        if c.get("nivel") and str(nivel).lower() not in [str(x).lower() for x in c["nivel"]]:
            continue
        if c.get("palabras") and not any(p.lower() in t for p in c["palabras"]):
            continue
        if c.get("remitente") and str(c["remitente"]).lower() not in r:
            continue
        salida.append(reg)
    return salida


def aplicar(regla, nivel, texto, remitente, destino):
    """Ejecuta una regla. Devuelve un texto-resumen de lo hecho (o None si no aplico)."""
    e = regla.get("entonces") or {}
    tipo = e.get("tipo")
    rid = regla.get("id")
    hecho = []

    if tipo == "auto_respuesta":
        if str(nivel).lower() == "rojo" and not e.get("permitir_rojo"):
            _log("regla %s NO aplica: es rojo y la regla no lo permite" % rid)
            return None
        plantilla = e.get("plantilla") or "Recibido, lo estamos atendiendo."
        try:
            _post("/api/sendText", {"session": "seawolf", "chatId": destino, "text": plantilla})
            hecho.append("respuesta automatica enviada a %s" % destino)
        except Exception as ex:
            _log("regla %s: fallo el envio (%s)" % (rid, str(ex)[:80]))
            return None

    elif tipo == "notificar":
        dest = e.get("destino")
        if not dest:
            _log("regla %s sin destino: no aplica" % rid)
            return None
        msg = (e.get("plantilla") or "Aviso: %s" % texto)[:900]
        try:
            _post("/api/sendText", {"session": "seawolf", "chatId": dest, "text": msg})
            hecho.append("aviso enviado a %s" % dest)
        except Exception as ex:
            _log("regla %s: fallo el aviso (%s)" % (rid, str(ex)[:80]))
            return None

    elif tipo == "rompe_rojo":
        # no es una accion inmediata: la ejecuta el temporizador del responder
        return None

    else:
        return None

    if hecho and bus:
        try:
            bus.emit(channel="whatsapp", direction="out", kind="action", text="; ".join(hecho),
                     peer=destino, actor="seawolf-agent", layer=3,
                     approved_by="regla:%s" % rid,
                     artifacts=[{"type": "rule_action", "regla": rid, "nombre": regla.get("nombre"),
                                 "tipo": tipo, "nivel": nivel}])
        except Exception:
            pass
    if hecho:
        _log("regla %s (%s) APLICADA: %s" % (rid, regla.get("nombre"), "; ".join(hecho)))
    return "; ".join(hecho) if hecho else None


def regla_rompe_rojo(nivel):
    """Busca una regla rompe_rojo aplicable a este nivel (y sus segundos)."""
    for reg in cargar().get("reglas", []):
        if not reg.get("activa"):
            continue
        c = reg.get("cuando") or {}
        e = reg.get("entonces") or {}
        if e.get("tipo") != "rompe_rojo":
            continue
        if c.get("nivel") and str(nivel).lower() not in [str(x).lower() for x in c["nivel"]]:
            continue
        return reg
    return None


def ejecutar_rompe_rojo(regla, destino, nivel, texto):
    """Ejecuta la accion segura preaprobada (sin respuesta del dueño)."""
    e = regla.get("entonces") or {}
    dest = e.get("destino")
    rid = regla.get("id")
    if not dest:
        return None
    msg = (e.get("plantilla") or "URGENTE (%s): %s" % (nivel, texto))[:900]
    try:
        _post("/api/sendText", {"session": "seawolf", "chatId": dest, "text": msg})
    except Exception as ex:
        _log("rompe-rojo %s: fallo (%s)" % (rid, str(ex)[:80]))
        return None
    if bus:
        try:
            bus.emit(channel="whatsapp", direction="out", kind="action",
                     text="rompe-rojo: aviso enviado a %s" % dest, peer=dest,
                     actor="seawolf-agent", layer=3, approved_by="regla:%s" % rid,
                     artifacts=[{"type": "rule_action", "regla": rid, "tipo": "rompe_rojo",
                                 "nivel": nivel, "motivo": "sin respuesta del dueno"}])
        except Exception:
            pass
    if SELF:  # el dueño se entera DESPUES (transparencia)
        try:
            _post("/api/sendText", {"session": "seawolf", "chatId": SELF,
                                    "text": "⚡ Regla *%s* aplicada: no respondió en %ss a un 🔥, "
                                            "así que avisé a %s. Usted sigue al mando."
                                            % (rid, e.get("segundos", 120), dest)})
        except Exception:
            pass
    _log("rompe-rojo %s EJECUTADA -> %s" % (rid, dest))
    return dest


# ------------------------------------------------------------------ CLI
def probar():
    """Prueba determinista del motor, sin mandar nada a nadie.
    Usa un archivo TEMPORAL: las reglas de prueba jamas tocan el reglas.json real."""
    print("=== PRUEBA DEL MOTOR DE REGLAS (archivo temporal) ===")
    import tempfile
    global REGLASF
    real = REGLASF
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
    REGLASF = tmp
    try:
        guardar({"reglas": [
            {"id": "r1", "nombre": "Quejas de mantenimiento -> avisar a Don Carlos", "activa": True,
             "cuando": {"nivel": ["naranja"], "palabras": ["mantenimiento", "ascensor", "fuga", "humedad"]},
             "entonces": {"tipo": "notificar", "destino": "573000000001@c.us",
                          "plantilla": "Don Carlos, hay un caso de mantenimiento: %s"}},
            {"id": "r2", "nombre": "Acuse automatico a quejas", "activa": True,
             "cuando": {"nivel": ["amarillo"], "palabras": ["queja"]},
             "entonces": {"tipo": "auto_respuesta", "plantilla": "Recibimos su queja, la estamos revisando."}},
            {"id": "r3", "nombre": "Rompe-rojo -> avisar al guarda", "activa": False,
             "cuando": {"nivel": ["rojo"]},
             "entonces": {"tipo": "rompe_rojo", "destino": "573000000002@c.us", "segundos": 120}},
        ]})
        casos = [
            ("Quejas de mantenimiento", "naranja", "El ascensor lleva tres dias sin funcionar", "r1"),
            ("Acuse automatico", "amarillo", "Quiero poner una queja por el ruido", "r2"),
            ("No debe casar", "verde", "Buenos dias, gracias", None),
            ("No casa por palabra", "naranja", "Se rompio el tubo del bano", None),
            ("Rojo no auto-responde", "rojo", "Hay un incendio en el 3er piso", None),
        ]
        ok = 0
        for nombre, nivel, texto, esperado in casos:
            ids = [r["id"] for r in evaluar(nivel, texto)]
            pasa = (esperado in ids) if esperado else (not ids)
            print("  [%s] %-26s nivel=%-8s reglas=%s" % ("OK  " if pasa else "FALLA", nombre, nivel, ids))
            ok += 1 if pasa else 0
        rr = regla_rompe_rojo("rojo")
        pasa_rr = (rr is None)
        print("  [%s] rompe-rojo desactivada -> no se dispara (%s)" % ("OK  " if pasa_rr else "FALLA", rr))
        ok += 1 if pasa_rr else 0
        total = len(casos) + 1
        print("RESULTADO: %d/%d" % (ok, total))
        return ok == total
    finally:
        REGLASF = real
        try:
            os.unlink(tmp)
        except Exception:
            pass


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "probar":
        sys.exit(0 if probar() else 1)
    elif cmd == "listar":
        print(json.dumps(cargar(), ensure_ascii=False, indent=2))
    else:
        print(__doc__)
