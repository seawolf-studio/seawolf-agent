import json
d = json.load(open("/tmp/m.json"))["data"]
print("TOTAL MODELOS:", len(d))
print("--- NEMOTRON ---")
for m in d:
    if "nemotron" in m["id"].lower():
        p = m.get("pricing", {})
        print(m["id"], "| prompt:", p.get("prompt"), "| comp:", p.get("completion"))
print("--- DEEPSEEK ---")
for m in d:
    if "deepseek" in m["id"].lower():
        p = m.get("pricing", {})
        print(m["id"], "| prompt:", p.get("prompt"), "| comp:", p.get("completion"))
