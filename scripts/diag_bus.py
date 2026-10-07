#!/usr/bin/env python3
"""Diagnostico del FTS del bus."""
import sqlite3

c = sqlite3.connect("/opt/waha/bus.db")
q = lambda s, a=(): c.execute(s, a).fetchone()
print("events:", q("SELECT COUNT(*) FROM events")[0])
print("fts rows:", q("SELECT COUNT(*) FROM events_fts")[0])
print("fts con texto no vacio:", q("SELECT COUNT(*) FROM events_fts WHERE text <> ''")[0])
print("muestra fts:", c.execute("SELECT rowid, substr(text,1,70) FROM events_fts LIMIT 2").fetchall())
print("events.id min/max:", q("SELECT MIN(id),MAX(id) FROM events"))
print("fts.rowid min/max:", q("SELECT MIN(rowid),MAX(rowid) FROM events_fts"))

TERM = '"SoVITS"'
try:
    print("MATCH sovits (solo fts):", q("SELECT COUNT(*) FROM events_fts WHERE events_fts MATCH ?", (TERM,))[0])
except Exception as e:
    print("MATCH error:", e)
try:
    print("MATCH+JOIN sovits:", q("SELECT COUNT(*) FROM events_fts f JOIN events e ON e.id=f.rowid WHERE f MATCH ?", (TERM,))[0])
except Exception as e:
    print("MATCH+JOIN error:", e)
try:
    print("bm25 alias:", c.execute("SELECT bm25(events_fts) FROM events_fts f WHERE f MATCH ? LIMIT 1", (TERM,)).fetchall())
except Exception as e:
    print("bm25 alias error:", e)
try:
    print("bm25 tabla:", c.execute("SELECT bm25(events_fts) FROM events_fts WHERE events_fts MATCH ? LIMIT 1", (TERM,)).fetchall())
except Exception as e:
    print("bm25 tabla error:", e)

print()
print("--- nombres reales de los repos que contienen SoVITS ---")
for r in c.execute("SELECT id, substr(text,1,60) FROM events WHERE text LIKE '%SoVITS%'"):
    print(r)
print()
print("--- LIKE '%clonacion%' ---")
print(q("SELECT COUNT(*) FROM events WHERE text LIKE '%clonaci%'")[0])
