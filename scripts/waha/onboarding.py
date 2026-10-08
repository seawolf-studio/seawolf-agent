#!/usr/bin/env python3
"""
C4 — ONBOARDING  (`onboarding.py`)
Seawolf Agent · Capa 4

La entrevista de arranque: el agente acuerda CON el cliente su identidad y su comportamiento,
y lo guarda como configuracion del tenant (tenant.json). Ademas presenta el MAPA DE CAPACIDADES
con estado honesto (decision del Monarca: el cliente lo sabe desde el dia 1).

Como funciona:
  - `iniciar()`  manda el mapa de capacidades + la primera pregunta.
  - Mientras el onboarding esta ACTIVO, los mensajes del dueño son RESPUESTAS (no ordenes).
  - `avanzar(texto)` guarda la respuesta y manda la siguiente pregunta.
  - `cerrar()`   escribe tenant.json + el mini-contrato + registra en el bus.
El dueño puede escribir "saltar" en cualquier pregunta, o "cancelar".

Pruebas: python3 onboarding.py probar   (simula el flujo completo sin mandar nada)
"""
import json
import os
import sys
import time
import urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
ESTADOF = os.path.join(DIR, "onboarding_estado.json")
TENANTF = os.path.join(DIR, "tenant.json")
ACUERDOF = os.path.join(DIR, "onboarding_acuerdo.md")
WAHA_URL = os.environ.get("WAHA_URL", "http://127.0.0.1:3000")
WAHA_KEY = os.environ.get("WAHA_API_KEY", "")
SELF = os.environ.get("SELF_CHAT", "")

sys.path.insert(0, DIR)
try:
    import bus
except Exception:
    bus = None

MAPA = """🐺 *Yo soy su agente.* Esto es lo que puedo hacer — y en qué estado está hoy:

*ACTIVO HOY*
· Filtrar su WhatsApp: le aviso solo lo que importa (🔥 seguridad · 🟠 se puede mitigar ya · 🟡 consultas · 🟢 ruido no le llega).
· Entender *notas de voz*, *fotos* y *videos* (los escucho y los miro).
· Redactar la respuesta y *pedirle permiso antes de enviar*: usted aprueba con una palabra, con texto libre o con una nota de voz.
· Anotar todo lo que pasa en un registro que usted puede revisar.

*EN MARCHA*
· Reglas preaprobadas: casos que usted autorice de una vez (ej. "quejas de mantenimiento → avisar al técnico") para no preguntarle cada vez.
· Aviso automático cuando es urgente y usted no responde en el tiempo que usted fije.

*PRÓXIMO*
· Panel para ver todo el movimiento y las actas del conjunto.
· Cuentas para varios administradores con permisos distintos.

_Nada de esto sale a un tercero sin su autorización._"""

PREGUNTAS = [
    ("nombre_agente", "¿Cómo quiere que me llame? (si prefiere, uso *Seawolf*)", "Seawolf"),
    ("nombre_dueno", "¿Cómo se llama usted y cómo quiere que lo trate? (ej. *Sr. Gómez*, *Key*)", "Key"),
    ("negocio", "¿A qué se dedica y qué administra? ¿Cuántos conjuntos o frentes maneja?", "6 conjuntos"),
    ("tono", "¿Cómo quiere que le hable a sus contactos: *formal* o *cercano*?", "cercano"),
    ("vocabulario", "¿Qué palabras usa su sector que yo deba respetar? (ej. *shut*, *censo*, *parqueadero*)", "shut, parqueadero"),
    ("urgencia", "¿Qué es URGENTE para usted? Deme un ejemplo real de algo que le haría interrumpir a medianoche.", "un robo o una fuga"),
    ("contactos", "¿Quiénes son sus contactos clave? Guarda, administrador, técnico, cuadrante de policía… (nombre y número si quiere)", "Don Carlos técnico"),
    ("horario", "¿A qué horas quiere recibir avisos, y a qué horas NO lo molesto salvo emergencia?", "7am a 9pm"),
    ("silencio", "Para lo no urgente, ¿lo agrupo y se lo mando de una vez, o prefiere que le llegue al momento?", "agrupado"),
    ("formato", "¿Cómo prefiere mis avisos: cortos de una línea, o con el detalle del caso?", "cortos"),
]


def _log(m):
    with open(os.path.join(DIR, "onboarding.log"), "a", encoding="utf-8") as f:
        f.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), m))
    print(m, flush=True)


def _post(path, payload):
    req = urllib.request.Request(WAHA_URL + path, data=json.dumps(payload).encode(),
                                 headers={"X-Api-Key": WAHA_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.status


def _enviar(texto, destino=None):
    try:
        _post("/api/sendText", {"session": "seawolf", "chatId": destino or SELF, "text": texto})
        return True
    except Exception as e:
        _log("error al enviar: %s" % str(e)[:100])
        return False


def estado():
    try:
        return json.load(open(ESTADOF, encoding="utf-8"))
    except Exception:
        return {"activo": False, "paso": 0, "respuestas": {}}


def _guardar_estado(e):
    json.dump(e, open(ESTADOF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


CAMPOS = ("horario", "tono", "formato", "silencio", "urgencia", "vocabulario", "negocio",
          "nombre_agente", "nombre_dueno")


def activo():
    e = estado()
    return bool(e.get("activo") or e.get("cambio_pendiente"))


def pedir_cambio(campo):
    """Recalibracion: el dueño pide cambiar un campo ya acordado."""
    e = estado()
    e["cambio_pendiente"] = campo
    _guardar_estado(e)
    _enviar("Listo, ¿cómo lo quiere ahora? (antes tenía: *%s*)\n_Escriba el nuevo valor o `cancelar`._"
            % _valor_actual(campo))
    _log("recalibracion pedida: %s" % campo)
    return campo


def _valor_actual(campo):
    try:
        ten = json.load(open(TENANTF, encoding="utf-8"))
    except Exception:
        return "(sin definir)"
    if campo in ("nombre_agente",):
        return (ten.get("agente") or {}).get("nombre_agente") or "(sin definir)"
    if campo in ("nombre_dueno",):
        return (ten.get("dueno") or {}).get("nombre") or "(sin definir)"
    return (ten.get("perfil") or {}).get(campo) or "(sin definir)"


def aplicar_cambio(texto):
    e = estado()
    campo = e.get("cambio_pendiente")
    if not campo:
        return None
    e.pop("cambio_pendiente", None)
    _guardar_estado(e)
    t = (texto or "").strip()
    if t.lower() in ("cancelar", "cancela", "salir"):
        _enviar("Sin cambios, entonces. Sigue como estaba.")
        return "cancelado"
    try:
        ten = json.load(open(TENANTF, encoding="utf-8"))
    except Exception:
        ten = {}
    if campo == "nombre_agente":
        ten["agente"] = dict(ten.get("agente") or {}, nombre_agente=t)
    elif campo == "nombre_dueno":
        ten["dueno"] = dict(ten.get("dueno") or {}, nombre=t)
    else:
        ten["perfil"] = dict(ten.get("perfil") or {}, **{campo: t})
    json.dump(ten, open(TENANTF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    _enviar("✅ Anotado: *%s* → %s. Lo aplico desde ya." % (campo, t))
    _log("recalibrado %s -> %s" % (campo, t))
    if bus:
        try:
            bus.emit(channel="webui", direction="in", kind="onboarding", text="recalibrado %s" % campo,
                     peer=SELF, actor="seawolf-agent", layer=4,
                     artifacts=[{"type": "onboarding", "accion": "recalibrar", "campo": campo}])
        except Exception:
            pass
    return "recalibrado"


def manejar(texto):
    """Unica entrada para los mensajes del dueño mientras C4 esta en curso."""
    e = estado()
    if e.get("cambio_pendiente"):
        return aplicar_cambio(texto)
    if e.get("activo"):
        return avanzar(texto)
    return None


def iniciar(con_mapa=True):
    e = {"activo": True, "paso": 0, "respuestas": {}, "iniciado": time.strftime("%Y-%m-%dT%H:%M:%S")}
    _guardar_estado(e)
    if con_mapa:
        _enviar(MAPA)
    _enviar("Para dejar el sistema a su medida, le voy a hacer %d preguntas cortas. "
            "*Escriba `saltar` para dejarla en automático o `cancelar` para parar.*\n\n"
            "*1/%d* · %s" % (len(PREGUNTAS), len(PREGUNTAS), PREGUNTAS[0][1]))
    _log("onboarding INICIADO")
    if bus:
        try:
            bus.emit(channel="webui", direction="in", kind="onboarding", text="onboarding iniciado",
                     peer=SELF, actor="seawolf-agent", layer=4,
                     artifacts=[{"type": "onboarding", "accion": "inicio"}])
        except Exception:
            pass
    return e["paso"]


def avanzar(texto):
    """Registra la respuesta del dueño y manda la siguiente pregunta (o cierra)."""
    e = estado()
    if not e.get("activo"):
        return None
    t = (texto or "").strip()
    if t.lower() in ("cancelar", "cancelá", "cancela", "salir"):
        e["activo"] = False
        _guardar_estado(e)
        _enviar("Onboarding *cancelado*. Uso la configuración por defecto y me sigue mandando las "
                "decisiones como siempre. Cuando quiera: *onboarding*.")
        _log("onboarding CANCELADO en el paso %s" % e.get("paso"))
        return "cancelado"

    clave, _, ejemplo = PREGUNTAS[e["paso"]]
    e["respuestas"][clave] = "" if t.lower() == "saltar" else t
    e["paso"] += 1
    _guardar_estado(e)

    if e["paso"] >= len(PREGUNTAS):
        return cerrar()
    n = e["paso"] + 1
    _enviar("*%d/%d* · %s" % (n, len(PREGUNTAS), PREGUNTAS[e["paso"]][1]))
    _log("onboarding paso %d respondido -> siguiente" % e["paso"])
    return e["paso"]


def cerrar():
    e = estado()
    r = e.get("respuestas") or {}
    try:
        ten = json.load(open(TENANTF, encoding="utf-8"))
    except Exception:
        ten = {"tenant": "cliente"}
    d = ten.get("dueno") or {}
    if r.get("nombre_dueno"):
        d["nombre"] = r["nombre_dueno"]
    ten["dueno"] = d
    ten["agente"] = dict(ten.get("agente") or {}, nombre_agente=r.get("nombre_agente") or "Seawolf")
    ten["perfil"] = {"negocio": r.get("negocio", ""), "tono": r.get("tono", "cercano"),
                     "vocabulario": r.get("vocabulario", ""), "urgencia": r.get("urgencia", ""),
                     "horario": r.get("horario", ""), "silencio": r.get("silencio", ""),
                     "formato": r.get("formato", "cortos")}
    if r.get("contactos"):
        cont = ten.get("contactos") or {}
        cont["_nota_contactos_declarados"] = r["contactos"]
        ten["contactos"] = cont
    json.dump(ten, open(TENANTF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    lineas = ["# ACUERDO DE CONFIGURACIÓN — %s" % (r.get("nombre_dueno") or "cliente"),
              "_Mini-contrato del arranque. Recalibrable cuando quiera._", ""]
    for clave, pregunta, ejemplo in PREGUNTAS:
        lineas.append("· **%s:** %s" % (clave, r.get(clave) or "(automático)"))
    lineas += ["", "**Política vigente:** nada sale a un tercero sin autorización del dueño; "
                   "el rompe-rojo queda apagado hasta que el dueño lo active."]
    open(ACUERDOF, "w", encoding="utf-8").write("\n".join(lineas) + "\n")

    e["activo"] = False
    e["cerrado"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    _guardar_estado(e)
    _enviar("✅ *Listo.* Ya quedó configurado:\n· Me llamo *%s*\n· Le hablo %s\n· Avisos: %s\n· Horario: %s\n\n"
            "El acuerdo quedó escrito en `onboarding_acuerdo.md` y lo puede recalibrar cuando quiera "
            "(dígame *cambiar horario*, *otro tono*, etc.)."
            % (r.get("nombre_agente") or "Seawolf", r.get("tono") or "cercano",
               r.get("formato") or "cortos", r.get("horario") or "sin restricción"))
    _log("onboarding CERRADO")
    if bus:
        try:
            bus.emit(channel="webui", direction="in", kind="onboarding",
                     text="onboarding completado: %s" % json.dumps(r, ensure_ascii=False)[:400],
                     peer=SELF, actor="seawolf-agent", layer=4,
                     artifacts=[{"type": "onboarding", "accion": "cierre"}])
        except Exception:
            pass
    return "cerrado"


# ------------------------------------------------------------------ CLI / prueba
def probar():
    """Simula el flujo completo CON ARCHIVOS TEMPORALES (no toca tenant.json real ni manda nada)."""
    global ESTADOF, TENANTF, ACUERDOF
    import tempfile
    reales = (ESTADOF, TENANTF, ACUERDOF)
    ESTADOF = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
    TENANTF = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
    ACUERDOF = tempfile.NamedTemporaryFile(delete=False, suffix=".md").name
    json.dump({"dueno": {}, "agente": {}}, open(TENANTF, "w"), ensure_ascii=False)
    print("=== PRUEBA DEL ONBOARDING (todo en archivos temporales) ===")
    global _enviar
    enviados = []
    _enviar_real = _enviar
    _enviar = lambda texto, destino=None: (enviados.append(texto), True)[1]
    try:
        iniciar(con_mapa=True)
        respuestas = ["Seawolfito", "Key", "6 conjuntos", "cercano", "shut, censo", "robo o fuga",
                      "Don Carlos tecnico", "7am a 9pm", "agrupado", "cortos"]
        for r in respuestas:
            avanzar(r)
        ten = json.load(open(TENANTF, encoding="utf-8"))
        acuerdo = open(ACUERDOF, encoding="utf-8").read()
        # recalibracion: pedir cambio y aplicarlo
        pedir_cambio("horario")
        aplicar_cambio("8am a 6pm")
        ten2 = json.load(open(TENANTF, encoding="utf-8"))
        ok = 0
        comprobaciones = [
            ("cerro el onboarding", estado().get("activo") is False),
            ("guardo el nombre del dueño", ten.get("dueno", {}).get("nombre") == "Key"),
            ("guardo el perfil", (ten.get("perfil") or {}).get("tono") == "cercano"),
            ("guardo los contactos declarados", bool((ten.get("contactos") or {}).get("_nota_contactos_declarados"))),
            ("escribio el acuerdo", "ACUERDO DE CONFIGURACIÓN" in acuerdo),
            ("presento el mapa de capacidades", any("Yo soy su agente" in x for x in enviados)),
            ("hizo las 10 preguntas", any("*10/10*" in x for x in enviados)),
            ("recalibro el horario", (ten2.get("perfil") or {}).get("horario") == "8am a 6pm"),
        ]
        for nombre, pasa in comprobaciones:
            print("  [%s] %s" % ("OK  " if pasa else "FALLA", nombre))
            ok += 1 if pasa else 0
        print("RESULTADO: %d/%d" % (ok, len(comprobaciones)))
        return ok == len(comprobaciones)
    finally:
        _enviar = _enviar_real
        ESTADOF, TENANTF, ACUERDOF = reales


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "probar":
        sys.exit(0 if probar() else 1)
    elif cmd == "iniciar":
        print("paso:", iniciar(con_mapa=True))
    elif cmd == "avanzar":
        print("->", avanzar(" ".join(sys.argv[2:])))
    elif cmd == "estado":
        print(json.dumps(estado(), ensure_ascii=False, indent=2))
    elif cmd == "cerrar":
        print("->", cerrar())
    else:
        print(__doc__)
