#!/usr/bin/env python3
"""NEREUS voice gateway — sentence-level chunked TTS.

Splits a reply into sentences and streams each sentence's audio as soon as it
is ready, so perceived latency is the FIRST (short) sentence, not the whole
paragraph. Framing: [uint32 BE length][WAV bytes] repeated, then close.
Backed by the local VoiceBox HTTP API.
"""
import json
import re
import struct
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VOICEBOX = "http://127.0.0.1:17600"
DEFAULT_PROFILE = "54a57975-e277-480d-9b6c-1a57d22c0f33"  # Kokoro ES em_alex
DEFAULT_ENGINE = "kokoro"
PORT = 8799

_SENT = re.compile(r"[^.!?¡¿\n]+[.!?…]*", re.UNICODE)


def split_sentences(text):
    parts = [s.strip() for s in _SENT.findall(text) if s.strip()]
    return parts or [text.strip()]


def synthesize(sentence, profile_id, engine):
    body = json.dumps(
        {"profile_id": profile_id, "text": sentence, "language": "es", "engine": engine}
    ).encode()
    req = urllib.request.Request(
        VOICEBOX + "/generate/stream", data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"  # simple: no Content-Length, close at end

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"ok": True, "gateway": "nereus-voice"})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/speak":
            self._json(404, {"error": "not found"})
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            self._json(400, {"error": "invalid json"})
            return
        text = (payload.get("text") or "").strip()
        if not text:
            self._json(400, {"error": "text required"})
            return
        profile = payload.get("profile_id") or DEFAULT_PROFILE
        engine = payload.get("engine") or DEFAULT_ENGINE
        sentences = split_sentences(text)

        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("X-Nereus-Sentences", str(len(sentences)))
        self.end_headers()
        try:
            for s in sentences:
                wav = synthesize(s, profile, engine)
                self.wfile.write(struct.pack(">I", len(wav)))
                self.wfile.write(wav)
                self.wfile.flush()
        except Exception:
            pass

    def _json(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
