#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
COMPOSIO — helper del Ejército de Sombras
Lee COMPOSIO_API_KEY del .env de Hermes y ejecuta herramientas vía SDK v2.

  python composio.py status                      # conexiones + estado
  python composio.py connections GMAIL,NOTION    # generar enlaces OAuth (10 min)
  python composio.py gmail [N]                   # leer N correos (default 5)
  python composio.py run GMAIL_FETCH_EMAILS '{"max_results":3,"user_id":"me"}'
  python composio.py search "send whatsapp message"

NOTA CLAVE: la clave ak_ (Project API Key) es para el SDK -> header x-api-key.
El MCP (connect.composio.dev/mcp) requiere una ck_ (Consumer API Key).
"""
import os, sys, json, re

ENV = r"C:\Users\Admin\AppData\Local\hermes\.env"
USER = "monarca_seawolf"

def key():
    k = os.environ.get("COMPOSIO_API_KEY")
    if not k and os.path.exists(ENV):
        for l in open(ENV, encoding="utf-8", errors="ignore"):
            if l.startswith("COMPOSIO_API_KEY="):
                k = l.strip().split("=", 1)[1]
    if not k:
        sys.exit("Falta COMPOSIO_API_KEY (en .env o entorno)")
    return k

def client():
    from composio import Composio
    c = Composio(api_key=key())
    return c, c.sessions.create(user_id=USER)

def dump(o, n=1200):
    print(json.dumps(o, default=str, ensure_ascii=False)[:n])

def main():
    a = sys.argv[1:] or ["status"]
    cmd = a[0].lower()
    c, s = client()
    if cmd == "status":
        r = s.execute("COMPOSIO_SEARCH_TOOLS", arguments={"queries": [{"use_case": "list connected toolkits status"}]})
        d = getattr(r, "data", None) or r
        dump(d, 1500)
    elif cmd == "connections":
        tks = [t.strip().upper() for t in (a[1] if len(a) > 1 else "GMAIL,GOOGLESHEETS,GOOGLECALENDAR").split(",")]
        r = s.execute("COMPOSIO_MANAGE_CONNECTIONS", arguments={"toolkits": tks})
        d = getattr(r, "data", None) or r
        res = d.get("results", d) if isinstance(d, dict) else d
        for k, v in (res or {}).items():
            if isinstance(v, dict):
                print(f"  {k:<16} [{v.get('status')}] {v.get('redirect_url') or v.get('instruction','')}")
    elif cmd == "gmail":
        n = int(a[1]) if len(a) > 1 else 5
        r = s.execute("COMPOSIO_MULTI_EXECUTE_TOOL", arguments={
            "tools": [{"tool_slug": "GMAIL_FETCH_EMAILS", "arguments": {"max_results": n, "user_id": "me", "verbose": False}}],
            "thought": "leer correos", "current_step": "FETCH", "current_step_metric": f"0/{n}"})
        d = r.data if not isinstance(r, dict) else r.get("data")
        msgs = d["results"][0]["response"]["data"]["messages"]
        for m in msgs:
            print(f"  · {str(m.get('sender'))[:44]:<44} | {str(m.get('subject'))[:58]}")
        print(f"  LEIDOS: {len(msgs)}")
    elif cmd == "run":
        slug = a[1]; args = json.loads(a[2]) if len(a) > 2 else {}
        r = s.execute("COMPOSIO_MULTI_EXECUTE_TOOL", arguments={
            "tools": [{"tool_slug": slug, "arguments": args}],
            "thought": "manual", "current_step": "RUN", "current_step_metric": "1/1"})
        d = r.data if not isinstance(r, dict) else r.get("data")
        dump(d["results"][0].get("response"), 2000)
    elif cmd == "search":
        r = s.execute("COMPOSIO_SEARCH_TOOLS", arguments={"queries": [{"use_case": " ".join(a[1:])}]})
        d = getattr(r, "data", None) or r
        dump(d, 2000)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
