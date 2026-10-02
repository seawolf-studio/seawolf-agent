#!/usr/bin/env python3
"""Minimal MCP (streamable HTTP) smoke test against the Graphiti server."""
import json, urllib.request

BASE = "http://127.0.0.1:8100/mcp"
H = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}


def rpc(method, params=None, rid=1, session=None):
    body = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}).encode()
    h = dict(H)
    if session:
        h["Mcp-Session-Id"] = session
    req = urllib.request.Request(BASE, data=body, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        sid = r.headers.get("Mcp-Session-Id")
        raw = r.read().decode("utf-8", "replace")
    # SSE-style response: take the last data: line
    for line in reversed([l for l in raw.splitlines() if l.startswith("data:")]):
        try:
            return json.loads(line[5:].strip()), sid
        except Exception:
            pass
    try:
        return json.loads(raw), sid
    except Exception:
        return {"raw": raw[:300]}, sid


init, sid = rpc("initialize", {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "nereus-smoke", "version": "0.1"},
})
print("initialize ->", json.dumps(init)[:220])
print("session:", sid)

tools, _ = rpc("tools/list", {}, rid=2, session=sid)
names = [t.get("name") for t in tools.get("result", {}).get("tools", [])]
print("tools:", names[:20])

# try adding an episode if the tool exists
target = None
for cand in ("add_memory", "add_episode", "add_memories"):
    if cand in names:
        target = cand
        break
if target:
    res, _ = rpc("tools/call", {
        "name": target,
        "arguments": {"name": "prueba-nereus", "episode_body": "El Monarca aprobo usar Graphiti como memoria temporal de NEREUS.",
                      "source": "text", "group_id": "nereus"},
    }, rid=3, session=sid)
    print(f"{target} ->", json.dumps(res)[:400])
else:
    print("no se encontro herramienta de alta")
