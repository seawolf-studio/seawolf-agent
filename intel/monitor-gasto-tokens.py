#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MONITOR DE GASTO DE TOKENS — Seawolf Studio
Lee state.db de Hermes (solo lectura) y reporta el gasto. Alerta temprana anti-picos.
Uso:  python monitor-gasto-tokens.py [--umbral-sesion 0.50] [--umbral-dia 2.00]
Elaborado por Bellion para el Monarca.
"""
import sqlite3, sys, datetime as dt, os, glob

UMBRAL_SESION = 0.50   # USD: alerta si una sesion supera esto
UMBRAL_DIA    = 2.00   # USD: alerta si el dia supera esto
for i, a in enumerate(sys.argv):
    if a == "--umbral-sesion" and i+1 < len(sys.argv): UMBRAL_SESION = float(sys.argv[i+1])
    if a == "--umbral-dia"    and i+1 < len(sys.argv): UMBRAL_DIA    = float(sys.argv[i+1])

def find_db():
    cands = [r"C:\Users\Admin\AppData\Local\hermes\state.db",
             os.path.expanduser("~/.hermes/state.db")]
    for c in cands:
        if os.path.exists(c): return c
    hits = glob.glob(os.path.expanduser("~/AppData/Local/hermes/**/state.db"), recursive=True)
    return hits[0] if hits else None

DB = find_db()
if not DB:
    print("No encontre state.db"); sys.exit(1)

con = sqlite3.connect("file:"+DB.replace("\\","/")+"?mode=ro&immutable=1", uri=True)
cur = con.cursor()
W = "WHERE (profile_name IS NULL OR profile_name='default')"

# --- HOY (UTC) ---
today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
r = list(cur.execute(f"""SELECT count(*), sum(input_tokens), sum(output_tokens),
    sum(cache_read_tokens), sum(reasoning_tokens), sum(estimated_cost_usd)
    FROM sessions {W} AND date(started_at,'unixepoch')=?""", (today,)))[0]
print(f"=== HOY {today} (UTC) ===")
print(f"sesiones {r[0] or 0} | in {r[1] or 0} | out {r[2] or 0} | cache {r[3] or 0} | raz {r[4] or 0} | gasto ${(r[5] or 0):.4f}")

# --- ultimos 7 dias ---
r7 = list(cur.execute(f"""SELECT sum(estimated_cost_usd) FROM sessions {W}
    AND started_at >= strftime('%s','now','-7 days')"""))[0][0] or 0
print(f"=== ULTIMOS 7 DIAS: ${r7:.4f} ===")

# --- top 5 sesiones por costo ---
print("\n=== TOP 5 SESIONES MAS CARAS ===")
for s in cur.execute(f"""SELECT title, estimated_cost_usd, input_tokens, output_tokens,
    cache_read_tokens, reasoning_tokens, started_at FROM sessions {W}
    ORDER BY estimated_cost_usd DESC LIMIT 5"""):
    d = dt.datetime.fromtimestamp(int(s[6]), dt.timezone.utc).strftime('%Y-%m-%d')
    print(f"  ${s[1]:.4f} | {d} | cache {s[4]:>11} | out {s[3]:>7} | raz {s[5]:>7} | {str(s[0])[:40]}")

# --- ALERTAS ---
print("\n=== ALERTAS ===")
alert = False
if (r[5] or 0) > UMBRAL_DIA:
    print(f"  [!] GASTO DE HOY ${r[5]:.4f} > umbral ${UMBRAL_DIA:.2f} -> cerrar sesion / protocolo"); alert = True
for s in cur.execute(f"""SELECT title, estimated_cost_usd, message_count, id FROM sessions {W}
    AND date(started_at,'unixepoch')=? ORDER BY estimated_cost_usd DESC LIMIT 5""", (today,)):
    if (s[1] or 0) > UMBRAL_SESION:
        print(f"  [!] SESION CARA ${s[1]:.4f} (msgs {s[2]}) '{str(s[0])[:35]}' -> compactar/cerrar"); alert = True
if not alert:
    print("  OK — sin picos por encima de umbral")
con.close()
