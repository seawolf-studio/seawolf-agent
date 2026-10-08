#!/usr/bin/env python3
"""
CRITERIO DE CLASIFICACION — Seawolf Agent (Capa 1)
==================================================
Vive aparte del filtro a proposito: el criterio es DOCTRINA DE NEGOCIO del Monarca,
no codigo. Se puede afinar aqui, y se prueba con probar_criterio.py sin tocar el filtro.

Reglas del Monarca (2026-10-07):
- Hurtos/robos/faltantes: COMO MINIMO se deben investigar -> nunca verde ni amarillo.
- Quejas y reclamos de residentes: nunca verde (merecen acuse de recibo).
"""
import json
import os
import urllib.request

MODEL = os.environ.get("FILTRO_MODEL", "google/gemini-2.5-flash")
ORK = os.environ.get("OPENROUTER_API_KEY", "")

SYS = """Eres el Filtro de ruido de un Cliente Super Ocupado (administrador de conjuntos residenciales / empresario) en Colombia. Clasifica el mensaje en UNA categoria segun este criterio:
- rojo: URGENTE. El mensaje PERTURBA LA SEGURIDAD o requiere ATENCION INMEDIATA que no puede diferirse. Ejemplos: intrusion o ingreso no autorizado, amenaza o riesgo a personas, incendio, fuga de gas, alguien herido, estafa o fraude en curso, emergencia activa, hurto EN CURSO o con una persona identificada o señalada.
- naranja: puede MITIGARSE ahora y arreglarse despues. La accion DEBE empezar por la mitigacion concreta. Ejemplo: tubo roto -> cerrar el registro de agua y programar plomero; plaga -> fumigar y limpiar; dano -> asegurar y agendar reparacion.
- amarillo: consulta simple que se responde con datos.
- verde: informativo o saludo, sin accion.

REGLAS ESPECIALES (obligatorias, tienen prioridad sobre lo anterior):
1. HURTOS, ROBOS, FALTANTES Y SUSTRACCIONES (paquetes abiertos o incompletos, objetos o dinero que aparecen perdidos, alguien se llevo algo, faltante de inventario): NUNCA verde ni amarillo. Como MINIMO naranja, porque DEBE INVESTIGARSE. La accion debe empezar por: revisar camaras, avisar al guarda y dejar constancia para la investigacion. Si el hurto es en curso, hay una persona identificada/señalada o hay riesgo para personas, entonces es rojo.
2. QUEJAS Y RECLAMOS DE RESIDENTES (incluidos reportes de dano, perdida o mal servicio): NUNCA verde. Como minimo amarillo, con acuse de recibo en la accion (registrar la queja y responder que se atendera).
3. OBJETOS O ESTRUCTURAS EN RIESGO EN AREAS COMUNES (maceta o matera inestable que pueda caer, reja suelta, rama a punto de quebrarse, vidrio roto, cable expuesto): NUNCA verde. Como minimo NARANJA, porque hay RIESGO DE ACCIDENTE para las personas. La accion empieza por eliminar o asegurar el riesgo.
4. PERSONA SOSPECHOSA O MERODEANDO (alguien rondando los carros o las areas comunes sin razon, persona observando casas o portones, desconocido en el parqueadero): es asunto de SEGURIDAD -> ROJO. La accion empieza por notificar al guarda y a la policia.
5. Para naranja y rojo, la accion debe empezar por la medida de mitigacion concreta.
Responde SOLO JSON valido con las claves cat, motivo, accion, donde cat es rojo|naranja|amarillo|verde."""


def _post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def classify(text, model=None):
    d = _post_json("https://openrouter.ai/api/v1/chat/completions",
                   {"model": model or MODEL, "temperature": 0,
                    "response_format": {"type": "json_object"}, "max_tokens": 400,
                    # CRITICO: qwen3.7-flash razona; sin desactivarlo medido 13.7 s/mensaje y 11x mas caro
                    "reasoning": {"enabled": False},
                    "messages": [{"role": "system", "content": SYS},
                                 {"role": "user", "content": text}]},
                   {"Authorization": "Bearer " + ORK})
    return json.loads(d["choices"][0]["message"]["content"])
