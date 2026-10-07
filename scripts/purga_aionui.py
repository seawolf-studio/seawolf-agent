#!/usr/bin/env python3
"""Purga de AionUI: restos en disco, skills, cache y memoria del agente.
NO toca contenedores del Seawolf Agent ni servicios en uso."""
import os
import shutil
import subprocess

RUTAS = [
    "/root/.aionui-web-dev",
    "/root/.hermes/sandboxes/docker/default/home/.aionui-web",
    "/root/.hermes/skills/autonomous-ai-agents/aionui-orchestration",
    "/root/.hermes/skills/software-development/docker-networking/references/aionui-hermes-architecture.md",
    "/root/.cache/pnpm/v11/metadata/registry.npmjs.org/@office-ai/aioncli-core.jsonl",
]

print("=== 1) RESTOS EN DISCO / SKILLS / CACHE ===")
for r in RUTAS:
    try:
        if os.path.isdir(r):
            shutil.rmtree(r)
            print("  eliminado dir  " + r)
        elif os.path.isfile(r):
            os.remove(r)
            print("  eliminado file " + r)
        else:
            print("  (no existia)   " + r)
    except Exception as e:
        print("  ERROR en %s: %s" % (r, e))

print()
print("=== 2) QUEDAN RASTROS DE 'aion'? ===")
out = subprocess.run(["bash", "-lc",
                      "find / -iname '*aion*' -not -path '*/proc/*' 2>/dev/null | head -20"],
                     capture_output=True, text=True).stdout.strip()
print(out if out else "  (limpio: cero rastros)")

print()
print("=== 3) CONFIG del agente: menciones de aion ===")
cfg = open("/root/.hermes/config.yaml", encoding="utf-8").read()
hits = [l for l in cfg.splitlines() if "aion" in l.lower()]
print("\n".join(hits) if hits else "  (ninguna)")

print()
print("=== 4) MEMORIA DEL AGENTE (reescritura limpia) ===")
MEM = """Seawolf Agent: soy el agente operativo de Key (el Monarca), dueno de Seawolf Studio (Colombia).
El valora la honestidad brutal y la accion directa; detesta el relleno, la exageracion y el bluff tecnico.
Prefiere un 'no se' honesto a una respuesta inflada. Le hablo directo, sin rodeos.
§
Producto: filtro de ruido para el Cliente Super Ocupado (administradores de conjuntos: 500-700 mensajes
de WhatsApp al dia). Modelo de 2 lineas: Linea 1 = su numero PERSONAL (INTOCABLE: nunca la leo);
Linea 2 = numero dedicado donde vivo yo, observo, clasifico y filtro.
§
Criterio del filtro (logica de negocio, no solo gravedad): rojo = perturba la seguridad o exige atencion
inmediata; naranja = mitigable ahora, arreglo despues (la accion empieza por la mitigacion);
amarillo = consulta simple; verde = informativo o saludo.
§
Memoria de canales (BUS DE EVENTOS): todo lo que entra o sale por WhatsApp, correo o WebUI queda registrado
en /opt/waha/bus.db. Ante CUALQUIER pregunta sobre algo pasado (un repo que envie anoche, que paso con un
mensaje, que pedi, que aprobo el dueno), consultar SIEMPRE antes de responder:
python3 /opt/waha/bus.py search "<el tema>" -n 5. Jamas decir que no tengo acceso a WhatsApp: si esta
en el bus, lo se. Detalle en la skill seawolf-memoria-bus.
§
Marca Seawolf: paleta #121E1E / #4CE8E7 / #48E8D8, modo OSCURO por defecto, mascota lobo negro.
"""
USR = """Key (el Monarca), colombiano, dueno de Seawolf Studio (OPC). Valores: honestidad brutal ante todo,
cero bluff tecnico, accion directa, pasos secuenciales, confirmar con 'listo'. Valora a las personas
'rango S'; su lema es el de Solo Leveling (ejercito de sombras, superacion).
§
Trabaja con un ejercito de agentes (sombras) con modelos propios. Su mision: dejar algo bueno para su
familia, sobre todo su hija. Toda mision sirve a eso.
§
Vive en WhatsApp y maneja conjuntos residenciales (residentes, guardas, proveedores, consejeros).
Quiere un agente que observe mucho, hable poco y solo a quien debe. Corre el Seawolf Agent 24/7 en su VPS.
"""
open("/root/.hermes/memories/MEMORY.md", "w", encoding="utf-8").write(MEM)
open("/root/.hermes/memories/USER.md", "w", encoding="utf-8").write(USR)
print("  MEMORY.md: %d chars (limite 2200)" % len(MEM))
print("  USER.md:   %d chars (limite 1375)" % len(USR))
print("  aionui en la memoria nueva?", "SI" if "aion" in MEM.lower() + USR.lower() else "NO")

print()
print("=== 5) CONTENEDOR hermes-agent-core: que es? ===")
for fmt in ["{{.Name}} | created {{.Created}} | {{.Image}}",
            "{{.Config.Cmd}}", "{{.Config.Labels}}",
            "{{range .Mounts}}{{.Source}} -> {{.Destination}} {{end}}"]:
    r = subprocess.run(["bash", "-lc", "docker inspect -f '%s' hermes-agent-core 2>&1" % fmt],
                       capture_output=True, text=True).stdout.strip()
    print("  " + r[:300])

print()
print("=== 6) REDES docker hermes-* (huerfanas?) ===")
r = subprocess.run(["bash", "-lc", "docker network ls --format '{{.Name}}' | grep -i hermes"],
                   capture_output=True, text=True).stdout.strip()
print(r if r else "  (ninguna)")
