#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SALA DE MANDO — genera el panel visual del escuadron desde el Kanban REAL.
Lee el board 'escuadron' (tasks/runs/events) e inyecta los datos en el HTML.
  python sala-de-mando.py [--board escuadron]
Salida: intel/sala-de-mando/sala-de-mando.html
"""
import sqlite3, json, os, sys, time, datetime

BOARD = "escuadron"
if "--board" in sys.argv: BOARD = sys.argv[sys.argv.index("--board")+1]
DB = rf"C:\Users\Admin\AppData\Local\hermes\kanban\boards\{BOARD}\kanban.db"
OUT = r"C:\Users\Admin\intel\sala-de-mando\sala-de-mando.html"

ROSTER = [
    ("igris","Igris","Copywriting","✍️"), ("tank","Tank","Ventas / WhatsApp","🤝"),
    ("greed","Greed","Ads / Tráfico","🎯"), ("iron","Iron","Email / Secuencias","📧"),
    ("tusk","Tusk","SEO / Orgánico","🔍"),  ("kamish","Kamish","Social / Distribución","📣"),
    ("kaisel","Kaisel","Web Dev","🌐"),     ("titan","Titan","UX / UI","🎨"),
    ("jima","Jima","Automatización","⚙️"),  ("beru","Beru","Auditoría","🛡️"),
]

def ts(v):
    if not v: return None
    try: return datetime.datetime.fromtimestamp(float(v)).strftime("%H:%M:%S")
    except Exception: return None

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    tasks = [dict(r) for r in c.execute("SELECT * FROM tasks ORDER BY priority DESC, created_at DESC")]
    runs  = [dict(r) for r in c.execute("SELECT * FROM task_runs ORDER BY id DESC")]
    evs   = [dict(r) for r in c.execute("SELECT * FROM task_events ORDER BY id DESC LIMIT 40")]

    run_by_task = {}
    for r in runs: run_by_task.setdefault(r["task_id"], r)
    activos = {r["profile"] for r in runs if r["status"] == "running"}

    tareas = []
    for t in tasks:
        ru = run_by_task.get(t["id"]) or {}
        tareas.append({
            "id": t["id"], "titulo": t["title"], "sombra": t["assignee"] or "—",
            "estado": t["status"], "prio": t["priority"] or 0,
            "creada": ts(t["created_at"]), "iniciada": ts(t["started_at"]),
            "run": ru.get("status"), "pid": ru.get("worker_pid") or t.get("worker_pid"),
            "latido": ts(ru.get("last_heartbeat_at")) or ts(t.get("last_heartbeat_at")),
            "modelo": t.get("model_override") or "por perfil",
            "ws": "scratch" if t.get("workspace_kind") == "scratch" else (t.get("workspace_kind") or "—"),
            "err": (ru.get("error") or t.get("last_failure_error") or "")[:190],
            "intentos": t.get("consecutive_failures") or 0,
            "salida": (ru.get("summary") or t.get("result") or "")[:190],
        })

    eventos = [{"k": e["kind"], "t": ts(e["created_at"]), "task": e["task_id"],
                "p": (e["payload"] or "")[:150]} for e in evs]

    sombras = [{"id": s, "nombre": n, "rol": r, "icono": i,
                "activo": s in activos,
                "tareas": sum(1 for x in tareas if x["sombra"] == s)} for s, n, r, i in ROSTER]

    stats = {
        "total": len(tareas),
        "running": sum(1 for x in tareas if x["estado"] == "running"),
        "ready": sum(1 for x in tareas if x["estado"] == "ready"),
        "done": sum(1 for x in tareas if x["estado"] == "done"),
        "blocked": sum(1 for x in tareas if x["estado"] in ("blocked", "triage")),
        "sombras_on": len(activos), "sombras_total": len(ROSTER),
    }
    data = {"board": BOARD, "generado": time.strftime("%H:%M:%S"), "tareas": tareas,
            "sombras": sombras, "eventos": eventos, "stats": stats}

    tpl = open(os.path.join(os.path.dirname(OUT), "plantilla.html"), encoding="utf-8").read()
    open(OUT, "w", encoding="utf-8").write(tpl.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False)))
    print(f"Sala de Mando -> {OUT}")
    print(f"  tareas {stats['total']} | corriendo {stats['running']} | listas {stats['ready']} | sombras activas {stats['sombras_on']}")
    for t in tareas: print(f"   · {t['estado']:<8} {t['sombra']:<7} {t['titulo'][:52]}")

if __name__ == "__main__": main()
