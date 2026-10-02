#!/usr/bin/env python3
import json, time, urllib.request, statistics

VB = "http://127.0.0.1:17600"
GW = "http://127.0.0.1:8799"
PID = "54a57975-e277-480d-9b6c-1a57d22c0f33"

TEXT = ("Claro, Monarca. Tengo tres cosas listas para ti. "
        "Primero, el informe de la manana esta preparado. "
        "Segundo, hay dos correos que requieren tu decision. "
        "Por ultimo, tu agenda de hoy tiene una reunion a las tres.")


def vb_full(text):
    body = json.dumps({"profile_id": PID, "text": text, "language": "es", "engine": "kokoro"}).encode()
    req = urllib.request.Request(VB + "/generate/stream", data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        data = r.read()
    return time.time() - t0, len(data)


def read_exact(f, n):
    buf = b""
    while len(buf) < n:
        c = f.read(n - len(buf))
        if not c:
            break
        buf += c
    return buf


def gw_speak(text):
    body = json.dumps({"text": text}).encode()
    req = urllib.request.Request(GW + "/speak", data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    ttfa = None
    frames = 0
    total_bytes = 0
    with urllib.request.urlopen(req, timeout=600) as r:
        f = r.fp
        while True:
            hdr = read_exact(f, 4)
            if len(hdr) < 4:
                break
            n = int.from_bytes(hdr, "big")
            if n == 0:
                break
            wav = read_exact(f, n)
            if ttfa is None:
                ttfa = time.time() - t0
            frames += 1
            total_bytes += len(wav)
    return ttfa, time.time() - t0, frames, total_bytes


print("=== BASELINE: parrafo completo, una peticion ===")
base = []
for i in range(3):
    t, sz = vb_full(TEXT)
    base.append(t)
    print(f"  intento {i+1}: total={t:.2f}s bytes={sz}")

print("\n=== CHUNKED: gateway por frases (nuevo) ===")
ttfas, totals = [], []
for i in range(3):
    ttfa, total, frames, tb = gw_speak(TEXT)
    ttfas.append(ttfa); totals.append(total)
    print(f"  intento {i+1}: TTFA={ttfa:.2f}s total={total:.2f}s frases={frames} bytes={tb}")

print(f"\nRESUMEN baseline total medio={statistics.mean(base):.2f}s")
print(f"RESUMEN nuevo: TTFA medio={statistics.mean(ttfas):.2f}s | total medio={statistics.mean(totals):.2f}s")
print("FIN")
