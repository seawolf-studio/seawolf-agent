import os, json, urllib.request
KEY = os.environ.get("OPENROUTER_API_KEY", "")
def call(model, system, user):
    body = json.dumps({"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "max_tokens": 320, "temperature": 0.6}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
                 "HTTP-Referer": "https://sw-st.net", "X-Title": "Seawolf SmartWeb"})
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.loads(r.read().decode())
    m = d["choices"][0]["message"]
    return m.get("content"), m.get("reasoning")
for mod in ["nvidia/nemotron-3.5-lightning:free", "deepseek/deepseek-v4.1-flash"]:
    try:
        c, rz = call(mod, "Eres un asistente de panaderia.", "hola, que venden?")
        print(mod, "=> content:", repr(c)[:160], "| reasoning_present:", bool(rz))
    except Exception as e:
        print(mod, "EXC", repr(e))
