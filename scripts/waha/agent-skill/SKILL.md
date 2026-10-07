---
name: seawolf-memoria-bus
description: Use when el dueno pregunta por CUALQUIER cosa que haya pasado por un canal (WhatsApp, correo, WebUI, alertas, acciones) o cuando necesites recordar algo que el agente hizo o recibio. Consulta el bus de eventos.
---

# Memoria del agente — el Bus de Eventos

**Principio:** *"Si pasa por un canal, pasa por el BUS. Y si pasa por el BUS, el agente lo sabe."*
Todo lo que entra o sale por cualquier canal (WhatsApp del cliente, correo, WebUI, alertas, acciones)
queda registrado como **evento** en el bus. Tu memoria de conversacion NO lo tiene: el bus si.

## Cuándo usar esto

Usálo SIEMPRE que el dueno pregunte por algo pasado, y no lo tengas en el contexto de la conversacion:
- *"el repo que me enviaste anoche"*, *"que paso con el ascensor del bloque 3"*,
- *"que le respondiste a X"*, *"que le pedi a Don Carlos"*, *"que acciones hiciste que yo aprobe"*,
- *"cuanto subio la cuota de octubre"*, *"cuando fue lo del tubo roto del 302"*,
- cualquier referencia a "eso que te dije", "lo de ayer", "el mensaje aquel".

## Cómo consultar

```bash
python3 /opt/waha/bus.py search "<la pregunta del dueno en lenguaje natural>" -n 5
python3 /opt/waha/bus.py search "<tema>" --channel whatsapp -n 5     # filtrar por canal
python3 /opt/waha/bus.py stats                                       # que hay en el bus
python3 /opt/waha/bus.py search "<tema>" --json                      # salida estructurada
```

Devuelve eventos con **canal, dirección (in/out), tipo, fecha, texto y artefactos** (URLs, acciones).

## Reglas duras

1. **Nunca inventes.** Si la busqueda no devuelve nada, decilo: *"no tengo registro de eso"*.
2. **Cita la fuente**: canal + fecha del evento (ej. *"te lo envie por WhatsApp el 7 de octubre a las 3:30"*).
   Eso es lo que permite al dueno auditarte.
3. **El bus es de solo lectura para ti por ahora**: no lo edites a mano. Para registrar algo nuevo,
   usa `python3 /opt/waha/bus.py add ...` (o deja que el canal que corresponda lo haga).
4. Si el dueno quiere registrar una **orden** o una **accion aprobada**, se registran con `layer=2` y
   `--approved-by <dueno>`: asi quedan auditables y buscables ("lo que yo aprobe").
5. **Privacidad:** el bus guarda lo de la Linea 2 (la del agente). La Linea 1 personal del cliente
   NO se toca nunca.

## Arquitectura (para ubicarte)

- Bus: `/opt/waha/bus.db` (SQLite + FTS5). Código: `/opt/waha/bus.py`. Doc: `intel/arquitectura-unificada-*.md`.
- Escriben al bus: `filtro.py` (mensajes y alertas de WhatsApp), `enviar_repos.py` (entregas),
  y cualquier canal que se conecte (correo, WebUI, acciones).
- El agente (vos) lee de aquí. No hay "dos cerebros": hay un bus.
