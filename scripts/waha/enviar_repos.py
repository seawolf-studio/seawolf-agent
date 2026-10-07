import json, os, urllib.request, sys

try:  # BUS DE EVENTOS: todo lo que el agente envia por un canal queda en el bus
    import bus
except Exception:
    bus = None

# el archivo local de la copia (para el set de datos)
try:
    bus.REPOS_JSONL = "/opt/waha/repos_desc.jsonl"
except Exception:
    pass

WAHA_URL = "http://127.0.0.1:3000"
KEY = os.environ["WAHA_API_KEY"]
SELF = os.environ["SELF_CHAT"]
BATCH = int(os.environ.get("REPO_BATCH", "5"))
D = "/opt/waha/repos_desc.jsonl"
IDXF = "/opt/waha/repos_idx"


def enviar(texto):
    payload = json.dumps({"session": "seawolf", "chatId": SELF, "text": texto}).encode()
    req = urllib.request.Request(WAHA_URL + "/api/sendText", data=payload,
                                 headers={"X-Api-Key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


lines = [l for l in open(D, encoding="utf-8") if l.strip()]
idx = int(open(IDXF).read().strip()) if os.path.exists(IDXF) else 0

if idx >= len(lines):
    print("ya completado")
    MARK = "/opt/waha/repos_done.sent"
    if os.environ.get("REPO_NOTIFY_DONE") == "1" and not os.path.exists(MARK):
        enviar("✅ Se completaron los 100 repositorios de creación de contenido con IA.")
        open(MARK, "w").write("ok")
        print("aviso de cierre enviado (una sola vez)")
    sys.exit(0)

batch = lines[idx:idx + BATCH]
parts = []
for l in batch:
    r = json.loads(l)
    parts.append("📦 *{}* — {:,}★ · {} · {}\n🔗 {}\n\n{}".format(
        r["full_name"], r["stars"], r["language"], r["license"], r["url"], r["texto"]))
    if bus:
        try:  # registro unitario: el repo queda recuperable por lenguaje natural
            bus.emit(channel="whatsapp", direction="out", kind="artifact_delivery",
                     text="Repo {} — {:,} ★ {} {}. {}".format(
                         r["full_name"], r["stars"], r["language"], r["license"], r["texto"]),
                     peer="self:L1", actor="seawolf-agent", layer=1,
                     artifacts=[{"type": "repo", "name": r["full_name"], "url": r["url"],
                                 "stars": r["stars"], "license": r["license"],
                                 "language": r["language"], "install": r["texto"]}])
        except Exception:
            pass

msg = "🐺 *SEAWOLF · Creación de contenido con IA*\n_Repos {}-{} de {}_\n\n{}".format(
    idx + 1, idx + len(batch), len(lines), "\n\n➖➖➖➖➖\n\n".join(parts))

code = enviar(msg)
if bus:
    try:  # registro del lote
        bus.emit(channel="whatsapp", direction="out", kind="artifact_delivery",
                 text="Lote enviado: repos {}-{} de {}".format(idx + 1, idx + len(batch), len(lines)),
                 peer="self:L1", actor="seawolf-agent", layer=1,
                 artifacts=[{"type": "batch", "desde": idx + 1, "hasta": idx + len(batch),
                             "total": len(lines)}])
    except Exception:
        pass
open(IDXF, "w").write(str(idx + BATCH))
print("enviados %d-%d (HTTP %s)" % (idx + 1, idx + len(batch), code))
