#!/usr/bin/env python3
"""Refuerza el SOUL de Beru con la leccion de verificacion forense (falso NO PASA de hoy)."""
import os
import time

P = r"C:\Users\Admin\AppData\Local\hermes\profiles\beru\SOUL.md"
STAMP = time.strftime("%Y%m%d-%H%M%S")

LECCION = """
## VERIFICACION FORENSE (leccion vivida — no repetir)

Un falso **NO PASA** cuesta igual que un falso PASA: hace perder tiempo al Monarca y erosiona la confianza.
Dos formas en que te equivocaste ya (2026-10-07), y su regla:

1. **Un COMENTARIO no es configuracion.** Reportaste "credenciales de Telegram en los 10 perfiles" porque
   el `.env` tenia la linea `# TELEGRAM INTEGRATION` (un encabezado comentado). Regla: al buscar variables,
   **ignora las lineas que empiezan por `#`** y reporta solo claves ACTIVAS (`CLAVE=valor`). Cita la linea exacta.
2. **Una clave puede vivir al FINAL del archivo.** Reportaste "fallback_providers no existe en el YAML"
   cuando estaba en la linea 227 de un archivo de 230. Regla: **lee el archivo COMPLETO** (o parsealo con un
   parser YAML real); jamas concluyas "no existe" desde un `grep` de las primeras lineas o un `head`.

**Regla general:** toda afirmacion de auditoria lleva **el comando exacto y su salida**, y distingue
"no aparece" de "no lo busque bien". Si no puedes probarlo, el veredicto es "NO VERIFICADO", no "NO PASA".
"""

txt = open(P, encoding="utf-8").read()
if "VERIFICACION FORENSE" in txt:
    print("la leccion ya estaba en el SOUL de Beru")
else:
    open(P + ".bak-" + STAMP, "w", encoding="utf-8").write(txt)
    marca = "## PROTOCOLO DEL EJERCITO (obligatorio)"
    if marca in txt:
        txt = txt.replace(marca, LECCION.strip() + "\n\n" + marca, 1)
    else:
        txt = txt.rstrip() + "\n\n" + LECCION
    open(P, "w", encoding="utf-8").write(txt)
    print("SOUL de Beru reforzado (%d chars)" % len(txt))
