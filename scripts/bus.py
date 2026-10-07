#!/usr/bin/env python3
"""
BUS DE EVENTOS — Seawolf Agent
==============================
Principio rector: "Si pasa por un canal, pasa por el BUS. Y si pasa por el BUS, el agente lo sabe."

Un solo cerebro por tenant. Los canales NO escriben a archivos sueltos: publican EVENTOS aqui.
El agente lee de aqui. Ver intel/arquitectura-unificada-20261007.md

Uso:
  python3 bus.py init
  python3 bus.py add --channel whatsapp --direction in --kind message --text "..." \
        --peer "57300...@c.us" --layer 1 --artifacts file.json
  python3 bus.py search "repo X instalacion" [-n 10] [--json]
  python3 bus.py import-repos          # backfill de los 100 repos ya enviados
  python3 bus.py stats

Como modulo:
  from bus import emit
  emit(channel="whatsapp", direction="out", kind="alert", text="...", peer="self")
"""
import argparse
import datetime
import json
import os
import re
import sqlite3
import sys
import uuid

DB = os.environ.get("SEAWOLF_BUS_DB", "/opt/waha/bus.db")
TENANT = os.environ.get("SEAWOLF_TENANT", "monarca")
REPOS_JSONL = "/opt/waha/repos_desc.jsonl"

STOP = {"que", "como", "los", "las", "una", "uno", "del", "para", "por", "con", "the", "and",
        "me", "mi", "tu", "el", "la", "de", "en", "a", "y", "o", "es", "un", "se", "al",
        "repo", "repos", "repositorio", "anoche", "ayer", "enviaste", "envio", "envias", "mandaste",
        "dime", "recuerda", "recuerdame", "acabo", "acorde", "ese", "esa", "esto", "esta",
        "puedes", "quiero", "necesito", "ayuda", "ayudame", "sobre", "cual", "cuales"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  evt_id TEXT UNIQUE, tenant TEXT NOT NULL, channel TEXT NOT NULL,
  direction TEXT NOT NULL, actor TEXT DEFAULT '', peer TEXT DEFAULT '',
  kind TEXT NOT NULL, text TEXT DEFAULT '', artifacts TEXT DEFAULT '[]',
  layer INTEGER DEFAULT 1, approved_by TEXT, ts TEXT NOT NULL, created TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_events_tenant_ts ON events(tenant, ts);
CREATE INDEX IF NOT EXISTS ix_events_channel ON events(channel, kind);
CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(text, artifacts, meta);
"""

# Sinonimos para que el lenguaje natural del dueno encuentre el evento correcto
# ("que aprobe yo" -> eventos con approved_by; "que acciones" -> kind=action...).
KIND_WORDS = {
    "action": "accion acciones ejecutada hizo realizo gestion",
    "alert": "alerta aviso urgente interrupcion",
    "message": "mensaje conversacion chat",
    "artifact_delivery": "entregado envio enviado compartido",
    "order": "orden pedido instruccion mandato",
    "audit": "auditoria registro historial",
    "classification": "clasificacion categoria filtro",
}


def _meta(channel, direction, kind, approved_by=None, actor="", peer=""):
    parts = [channel or "", kind or "", direction or "",
             KIND_WORDS.get(kind or "", ""),
             "recibido entrante" if direction == "in" else "enviado saliente",
             actor or "", peer or ""]
    if approved_by:
        parts.append("aprobado aprobada aprobacion autorizado por " + str(approved_by))
    return " ".join(p for p in parts if p)


def _conn():
    c = sqlite3.connect(DB, timeout=15)
    c.row_factory = sqlite3.Row
    return c


def init():
    c = _conn()
    c.executescript(SCHEMA)
    c.commit()
    c.close()


def emit(channel, direction, kind, text, peer="", actor="seawolf-agent",
         artifacts=None, layer=1, approved_by=None, ts=None, tenant=None):
    """Publica UN evento al bus. Devuelve el evt_id."""
    init()
    tenant = tenant or TENANT
    ts = ts or datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    created = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    evt_id = "evt_" + uuid.uuid4().hex[:12]
    art = json.dumps(artifacts or [], ensure_ascii=False)
    c = _conn()
    cur = c.execute(
        "INSERT INTO events(evt_id,tenant,channel,direction,actor,peer,kind,text,artifacts,"
        "layer,approved_by,ts,created) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (evt_id, tenant, channel, direction, actor, peer, kind, text or "", art,
         int(layer or 1), approved_by, ts, created))
    c.execute("INSERT INTO events_fts(rowid, text, artifacts, meta) VALUES(?,?,?,?)",
              (cur.lastrowid, text or "", art,
               _meta(channel, direction, kind, approved_by, actor, peer)))
    c.commit()
    c.close()
    return evt_id


def _tokens(q):
    toks = re.findall(r"[\w\u00e0-\u024f]+", q or "", re.UNICODE)
    return [t for t in toks if len(t) > 1 and t.lower() not in STOP]


def _informative(toks, tenant=None):
    """Descarta tokens que aparecen en demasiados eventos (bajo poder discriminante).
    Sin esto, un termino presente en el 100% de los eventos (ej. 'repo') contamina todo el ranking."""
    if not toks:
        return []
    c = _conn()
    total = c.execute("SELECT COUNT(*) FROM events" + (" WHERE tenant=?" if tenant else ""),
                      ([tenant] if tenant else [])).fetchone()[0] or 1
    keep = []
    for t in toks:
        sql = "SELECT COUNT(*) FROM events WHERE text LIKE ?"
        args = ["%" + t + "%"]
        if tenant:
            sql += " AND tenant=?"
            args.append(tenant)
        df = c.execute(sql, args).fetchone()[0]
        if total < 5 or df / float(total) <= 0.35:
            keep.append(t)
    c.close()
    return keep or toks


def search(q, tenant=None, limit=10, channel=None):
    """Recupera eventos por lenguaje natural. Escalera de precision:
    (1) AND de tokens informativos (preciso) -> (2) OR con bm25 -> (3) LIKE."""
    init()
    rows = []
    toks = _tokens(q)
    core = _informative(toks, tenant)

    def _fts(expr, lim):
        # NOTA: SQLite NO permite MATCH ni bm25() sobre un alias de tabla FTS5
        # ("no such column: f") -> hay que nombrar la tabla real. Si se aliasa, el
        # motor cae al plan B (LIKE por fecha) y devuelve lo reciente, no lo relevante.
        sql = ("SELECT e.*, bm25(events_fts) AS score FROM events_fts "
               "JOIN events e ON e.id = events_fts.rowid WHERE events_fts MATCH ?")
        args = [expr]
        if tenant:
            sql += " AND e.tenant = ?"
            args.append(tenant)
        if channel:
            sql += " AND e.channel = ?"
            args.append(channel)
        sql += " ORDER BY score LIMIT ?"
        args.append(int(lim))
        try:
            c = _conn()
            out = [dict(r) for r in c.execute(sql, args).fetchall()]
            c.close()
            return out
        except sqlite3.OperationalError:
            return []

    if core:
        rows = _fts(" AND ".join('"%s"' % t.replace('"', "") for t in core), limit)
    if len(rows) < min(3, limit) and len(core) > 1:
        seen = {r["id"] for r in rows}
        for r in _fts(" OR ".join('"%s"' % t.replace('"', "") for t in core), limit):
            if r["id"] not in seen:
                rows.append(r)
                seen.add(r["id"])
    if not rows:  # fallback: LIKE por cualquier token
        clause = " OR ".join(["text LIKE ? OR artifacts LIKE ?" for _ in toks]) or "0"
        args = []
        for t in toks:
            args += ["%" + t + "%", "%" + t + "%"]
        sql = "SELECT *, 0 AS score FROM events WHERE (" + clause + ")"
        if tenant:
            sql += " AND tenant = ?"
            args.append(tenant)
        if channel:
            sql += " AND channel = ?"
            args.append(channel)
        sql += " ORDER BY ts DESC LIMIT ?"
        args.append(int(limit))
        c = _conn()
        rows = [dict(r) for r in c.execute(sql, args).fetchall()]
        c.close()
    return rows[:limit]


def fmt(r):
    arts = []
    try:
        arts = json.loads(r.get("artifacts") or "[]")
    except Exception:
        pass
    head = "[%s] %s %s->%s (%s)" % (r["ts"], r["channel"], r["direction"], r["peer"] or "-", r["kind"])
    out = [head, "  " + (r.get("text") or "")[:300].replace("\n", " ")]
    for a in arts[:6]:
        if isinstance(a, dict):
            if a.get("url"):
                out.append("  - %s | %s | %s" % (a.get("name", ""), a.get("url"), a.get("install", "")[:120]))
            elif a.get("accion"):
                out.append("  - accion: %s (cat=%s)" % (str(a.get("accion"))[:150], a.get("cat")))
    return "\n".join(out)


def import_repos(path=REPOS_JSONL):
    """Backfill: los 100 repos ya enviados por WhatsApp se vuelven eventos del bus.
    Idempotente: borra un backfill anterior antes de reinsertar."""
    init()
    c = _conn()
    c.execute("DELETE FROM events_fts WHERE rowid IN "
              "(SELECT id FROM events WHERE artifacts LIKE '%\"backfill\": true%')")
    c.execute("DELETE FROM events WHERE artifacts LIKE '%\"backfill\": true%'")
    c.commit()
    c.close()
    lines = [l for l in open(path, encoding="utf-8") if l.strip()]
    # evidencia: envios.log cerro el ultimo lote a las 08:30 UTC; 20 lotes de 30 min -> arranque 23:00
    base = datetime.datetime(2026, 10, 6, 23, 0, tzinfo=datetime.timezone.utc)
    n = 0
    for i, l in enumerate(lines):
        r = json.loads(l)
        ts = (base + datetime.timedelta(minutes=30 * (i // 5))).isoformat(timespec="seconds")
        emit(channel="whatsapp", direction="out", kind="artifact_delivery",
             text="Repo %s — %s ★ %s %s. %s" % (r.get("full_name"), r.get("stars"),
                                                r.get("language"), r.get("license"),
                                                r.get("texto", "")),
             peer="self:L1", actor="seawolf-agent",
             artifacts=[{"type": "repo", "name": r.get("full_name"), "url": r.get("url"),
                         "stars": r.get("stars"), "license": r.get("license"),
                         "language": r.get("language"),
                         "install": r.get("texto", ""), "backfill": True}],
             layer=1, ts=ts)
        n += 1
    return n


def stats():
    init()
    c = _conn()
    tot = c.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    print("eventos totales: %d" % tot)
    for r in c.execute("SELECT channel, direction, kind, COUNT(*) n FROM events "
                       "GROUP BY channel, direction, kind ORDER BY n DESC"):
        print("  %-10s %-4s %-18s %d" % (r["channel"], r["direction"], r["kind"], r["n"]))
    print("rango: %s .. %s" % tuple(
        (c.execute("SELECT MIN(ts), MAX(ts) FROM events").fetchone()[0:2])))
    c.close()


def reindex():
    """Reconstruye el indice FTS desde la tabla events (necesario al cambiar el esquema
    del indice, ej. al agregar la columna meta)."""
    c = _conn()
    c.execute("DROP TABLE IF EXISTS events_fts")
    c.executescript(SCHEMA)
    rows = c.execute("SELECT * FROM events").fetchall()
    for r in rows:
        c.execute("INSERT INTO events_fts(rowid, text, artifacts, meta) VALUES(?,?,?,?)",
                  (r["id"], r["text"] or "", r["artifacts"] or "[]",
                   _meta(r["channel"], r["direction"], r["kind"], r["approved_by"],
                         r["actor"], r["peer"])))
    c.commit()
    n = len(rows)
    c.close()
    return n


def main():
    ap = argparse.ArgumentParser(description="Bus de eventos Seawolf Agent")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("stats")
    sub.add_parser("import-repos")
    sub.add_parser("reindex")

    a = sub.add_parser("add")
    a.add_argument("--channel", required=True)
    a.add_argument("--direction", required=True, choices=["in", "out"])
    a.add_argument("--kind", required=True)
    a.add_argument("--text", required=True)
    a.add_argument("--peer", default="")
    a.add_argument("--actor", default="seawolf-agent")
    a.add_argument("--layer", type=int, default=1)
    a.add_argument("--approved-by", default=None)
    a.add_argument("--artifacts", default=None, help="ruta a un JSON con la lista de artefactos")

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("-n", "--limit", type=int, default=10)
    s.add_argument("--channel", default=None)
    s.add_argument("--json", action="store_true")

    args = ap.parse_args()
    if args.cmd == "init":
        init()
        print("bus listo en " + DB)
    elif args.cmd == "stats":
        stats()
    elif args.cmd == "import-repos":
        print("importados %d repos al bus" % import_repos())
    elif args.cmd == "reindex":
        print("reindexados %d eventos" % reindex())
    elif args.cmd == "add":
        arts = json.load(open(args.artifacts, encoding="utf-8")) if args.artifacts else []
        print(emit(args.channel, args.direction, args.kind, args.text, peer=args.peer,
                   actor=args.actor, artifacts=arts, layer=args.layer,
                   approved_by=args.approved_by))
    elif args.cmd == "search":
        rows = search(args.query, limit=args.limit, channel=args.channel)
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            if not rows:
                print("(sin resultados)")
            for r in rows:
                print(fmt(r))
                print()


if __name__ == "__main__":
    main()
