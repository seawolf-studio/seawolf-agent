#!/usr/bin/env python3
"""PRUEBA DE COMBATE — Ejercito de Sombras.
Una mision real por sombra en SU propio perfil (hermes -p <sombra> chat -q ...).
Verifica DOS cosas: (1) que responde, (2) que USA herramientas (deja un archivo).
Escribe resultados a intel/prueba-combate-ejercito-<stamp>.md"""
import json
import os
import subprocess
import time

SOMBRAS = ["igris", "tank", "greed", "iron", "tusk", "kamish", "kaisel", "titan", "jima", "beru"]
INTEL = r"C:\Users\Admin\seawolf-agent\intel"
ESTADO = os.path.join(INTEL, "estado-sombras")
os.makedirs(ESTADO, exist_ok=True)
STAMP = time.strftime("%Y%m%d-%H%M%S")

MISION = ("Confirma tu estado operativo. Usa la herramienta terminal para crear el archivo "
          "'{ruta}' cuyo contenido sea exactamente 'OPERATIVO {sombra} - <tu rol en 6 palabras>'. "
          "Despues responde SOLO con esta linea: OPERATIVO: {sombra} - <tu rol en 6 palabras>. "
          "No expliques nada mas.")

resultados = {}
for s in SOMBRAS:
    ruta = os.path.join(ESTADO, "%s.txt" % s).replace("\\", "/")
    mision = MISION.format(ruta=ruta, sombra=s)
    t0 = time.time()
    try:
        p = subprocess.run(["hermes", "-p", s, "chat", "-q", mision, "--yolo"],
                           capture_output=True, text=True, timeout=300, encoding="utf-8",
                           errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        out, rc = "(TIMEOUT de 300s)", -1
    dt = time.time() - t0
    archivo = os.path.exists(os.path.join(ESTADO, "%s.txt" % s))
    operativo = "OPERATIVO" in out.upper()
    session = ""
    for line in out.splitlines():
        if line.strip().lower().startswith("session"):
            session = line.strip()[:80]
    veredicto = "PASA" if (archivo and operativo) else ("PARCIAL" if operativo else "FALLA")
    resultados[s] = {"rc": rc, "seg": round(dt, 1), "archivo": archivo,
                     "responde": operativo, "session": session, "veredicto": veredicto,
                     "cola": out.strip()[-400:]}
    print("%-8s %-8s %6.1fs  archivo=%-5s responde=%-5s  %s"
          % (s, veredicto, dt, archivo, operativo, session), flush=True)

ok = sum(1 for v in resultados.values() if v["veredicto"] == "PASA")
parc = sum(1 for v in resultados.values() if v["veredicto"] == "PARCIAL")

md = ["# PRUEBA DE COMBATE — EJERCITO DE SOMBRAS",
      "**Fecha:** %s · **Ejecutada por:** Bellion (via hermes -p por perfil)" % STAMP,
      "**Criterio:** PASA = responde Y deja el archivo (usa herramientas).", "",
      "| Sombra | Veredicto | Seg | Archivo | Responde | Session |",
      "|---|---|---|---|---|---|"]
for s, v in resultados.items():
    md.append("| %s | %s | %.1f | %s | %s | %s |"
              % (s, v["veredicto"], v["seg"], "si" if v["archivo"] else "no",
                 "si" if v["responde"] else "no", v["session"][:40]))
md += ["", "**Resumen: %d PASA · %d PARCIAL · %d FALLA de %d**" % (ok, parc, len(SOMBRAS) - ok - parc, len(SOMBRAS)), ""]
for s, v in resultados.items():
    md += ["## %s — %s" % (s, v["veredicto"]), "```", v["cola"][-300:], "```", ""]

with open(os.path.join(INTEL, "prueba-combate-ejercito-%s.md" % STAMP), "w", encoding="utf-8") as f:
    f.write("\n".join(md))
json.dump(resultados, open(os.path.join(INTEL, "prueba-combate-%s.json" % STAMP), "w"),
          ensure_ascii=False, indent=2)
print("\nRESUMEN: %d PASA / %d PARCIAL / %d FALLA de %d" % (ok, parc, len(SOMBRAS) - ok - parc, len(SOMBRAS)))
print("Informe: %s" % os.path.join(INTEL, "prueba-combate-ejercito-%s.md" % STAMP))
