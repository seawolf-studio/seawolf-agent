#!/usr/bin/env python3
"""Limpieza: borra los eventos basura del bucle del responder (peer=SELF, text='Ok')
y reajusta los marcadores de estado para no reprocesar nada."""
import json
import sqlite3
import sys

sys.path.insert(0, "/opt/waha")
DB = "/opt/waha/bus.db"
c = sqlite3.connect(DB)
antes = c.execute("SELECT COUNT(*) FROM events").fetchone()[0]

# basura = ordenes emitidas por el propio motor (peer = chat del dueno), no las del canal
junk = c.execute("SELECT id FROM events WHERE kind='order' AND peer=? AND text=?",
                 ("573125330127@c.us", "Ok")).fetchall()
ids = [r[0] for r in junk]
print("eventos basura detectados: %d" % len(ids))
for i in ids:
    c.execute("DELETE FROM events_fts WHERE rowid=?", (i,))
    c.execute("DELETE FROM events WHERE id=?", (i,))
c.commit()
despues = c.execute("SELECT COUNT(*) FROM events").fetchone()[0]
print("bus: %d -> %d eventos" % (antes, despues))

mx = c.execute("SELECT MAX(id) FROM events").fetchone()[0] or 0
mo = c.execute("SELECT MAX(id) FROM events WHERE kind=?", ("order",)).fetchone()[0] or 0
orden = c.execute("SELECT COUNT(*) FROM events WHERE kind=?", ("order",)).fetchone()[0]
c.close()
json.dump({"ultimo_orden": mo, "ultimo_msg": mx}, open("/opt/waha/responder_estado.json", "w"))
print("estado reajustado: ultimo_msg=%s ultimo_orden=%s" % (mx, mo))
print("kind=order restantes (deben ser SOLO las del canal):", orden)
