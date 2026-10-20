# -*- coding: utf-8 -*-
# Backend del ASISTENTE SmartWeb — Seawolf Studio
# Endpoint: POST /asistente  {slug, prompt, msg}  ->  {reply}
# Modelo: Nemotron (gratis, rapido) primario -> DeepSeek flash (economico) fallback.
# Solo stdlib (sin dependencias). Key leida del entorno (systemd EnvironmentFile).
import json, os, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

KEY       = os.environ.get("OPENROUTER_API_KEY", "")
PRIMARY   = os.environ.get("ASISTENTE_MODEL_PRIMARY",  "nvidia/nemotron-3.5-lightning:free")
FALLBACK  = os.environ.get("ASISTENTE_MODEL_FALLBACK", "deepseek/deepseek-v4.1-flash")
MAXTOK    = int(os.environ.get("ASISTENTE_MAXTOK", "320"))
PORT      = int(os.environ.get("PORT", "8790"))

HITS = {}
def rate_ok(ip):
    now = time.time()
    q = [t for t in HITS.get(ip, []) if now - t < 60]
    if len(q) >= 30:
        HITS[ip] = q
        return False
    q.append(now)
    HITS[ip] = q
    return True

def call(model, system, user):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": MAXTOK, "temperature": 0.6,
        "reasoning": {"enabled": False},
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
                 "HTTP-Referer": "https://sw-st.net", "X-Title": "Seawolf SmartWeb"})
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.loads(r.read().decode())
    return (d["choices"][0]["message"]["content"] or "").strip()

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    def _json(self, code, obj):
        out = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self._cors()
        self.end_headers()
        self.wfile.write(out)
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        if self.path.startswith("/asistente/health"):
            self._json(200, {"ok": True, "primary": PRIMARY, "fallback": FALLBACK, "key": bool(KEY)})
        else:
            self._json(404, {"error": "no"})
    def do_POST(self):
        if not self.path.startswith("/asistente"):
            self._json(404, {"error": "no"}); return
        if not rate_ok(self.client_address[0]):
            self._json(429, {"reply": "Demasiadas solicitudes. Intenta en un momento."}); return
        n = int(self.headers.get("Content-Length", "0") or 0)
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            data = {}
        msg = (data.get("msg") or "").strip()[:800]
        prompt = (data.get("prompt") or "Eres un asistente de atencion al cliente.")[:1500]
        slug = str(data.get("slug") or "")[:80]
        if not msg:
            self._json(200, {"reply": "Cuentame, en que te puedo ayudar?"}); return
        system = (prompt + " Responde SIEMPRE en espanol, breve (maximo 3 frases), cercano y util. "
                  "Si no sabes un dato, ofrece escribir por WhatsApp. No inventes precios ni informacion.")
        reply, err = "", ""
        for m in (PRIMARY, FALLBACK):
            if not KEY:
                err = "no key"; break
            try:
                reply = call(m, system, msg)
                if reply:
                    break
            except Exception as e:
                err = str(e)
        if not reply:
            reply = "Disculpa, tuve un problema tecnico. Escribenos por WhatsApp y te atendemos de inmediato. 🙂"
            print("ERROR asistente:", repr(err), flush=True)
        self._json(200, {"reply": reply, "slug": slug})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("Asistente Seawolf escuchando en 127.0.0.1:%d | primary=%s | fallback=%s | key=%s"
          % (PORT, PRIMARY, FALLBACK, bool(KEY)), flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
