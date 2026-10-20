import os, json, urllib.request
KEY = os.environ.get("OPENROUTER_API_KEY", "")
def call(model, extra):
    body = {"model": model, "messages": [
        {"role": "system", "content": "Eres el asistente de una panaderia. Responde breve y en espanol, maximo 2 frases."},
        {"role": "user", "content": "hola, que venden?"}], "max_tokens": 300}
    body.update(extra)
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "HTTP-Referer": "https://sw-st.net"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode())
    m = d["choices"][0]["message"]
    return m.get("content")
tests = [
  ("nvidia/nemotron-3.5-lightning:free", {"reasoning": {"enabled": False}}),
  ("nvidia/nemotron-3.5-lightning:free", {"max_tokens": 1200}),
  ("deepseek/deepseek-v4.1-flash",       {"reasoning": {"enabled": False}}),
  ("deepseek/deepseek-v4.1-flash",       {"max_tokens": 1200}),
]
for model, extra in tests:
    try:
        print(model, extra, "=>", repr(call(model, extra))[:170])
    except Exception as e:
        print(model, extra, "EXC", repr(e)[:220])
