#!/usr/bin/env python3
"""1) Da acceso del contenedor del agente al bus (/opt/waha) como volumen.
2) Diagnostica hermes-agent-core antes de decidir su retiro."""
import subprocess

CFG = "/root/.hermes/config.yaml"
txt = open(CFG, encoding="utf-8").read()

print("=== 1) VOLUMEN del sandbox para el bus ===")
old = "  docker_volumes: []"
new = ("  docker_volumes:\n"
       "    - /opt/waha:/opt/waha:ro   # bus de eventos: el agente (en contenedor) lee /opt/waha/bus.db")
if "/opt/waha:/opt/waha:ro" in txt:
    print("  ya estaba configurado")
elif old in txt:
    open(CFG + ".bak-pre-bus", "w", encoding="utf-8").write(txt)
    open(CFG, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  configurado (respaldo en config.yaml.bak-pre-bus)")
else:
    print("  NO se encontro la linea exacta; revisar a mano:")
    print("\n".join(l for l in txt.splitlines() if "docker_volumes" in l))
print()
print("  lineas ahora:")
for l in open(CFG, encoding="utf-8").read().splitlines():
    if "docker_volumes" in l or "/opt/waha" in l:
        print("   " + l)

print()
print("=== 2) hermes-agent-core: lo usa alguien? ===")
subprocess.run(["bash", "-lc",
                "curl -s -o /dev/null -w '  HTTP localhost:8085 -> %{http_code}\\n' --max-time 5 http://127.0.0.1:8085 || echo '  8085 no responde'"],
               shell=False)
r = subprocess.run(["bash", "-lc", "grep -rniE '8085|hermes-agent-core' /etc/nginx/ /etc/systemd/system/ 2>/dev/null | head -5"],
                   capture_output=True, text=True).stdout.strip()
print("  referencias en nginx/systemd:\n    " + (r.replace("\n", "\n    ") if r else "(ninguna)"))
r = subprocess.run(["bash", "-lc", "docker logs --tail 4 hermes-agent-core 2>&1 | tail -4"],
                   capture_output=True, text=True).stdout.strip()
print("  ultimas lineas del contenedor:\n    " + (r.replace("\n", "\n    ") if r else "(sin logs)"))
