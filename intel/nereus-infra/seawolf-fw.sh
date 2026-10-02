#!/usr/bin/env bash
# Seawolf: restrict Docker-published management ports to loopback + tailnet + docker nets.
# Idempotent. Safe to re-run.
set -u
PORTS="8000,9443,8085"
ALLOW=( "127.0.0.0/8" "100.64.0.0/10" "172.16.0.0/12" "10.0.0.0/8" )

# Remove any previous copies of our rules so re-runs stay clean.
while iptables -D DOCKER-USER -p tcp -m multiport --dports "$PORTS" -j DROP 2>/dev/null; do :; done
for net in "${ALLOW[@]}"; do
  while iptables -D DOCKER-USER -s "$net" -p tcp -m multiport --dports "$PORTS" -j RETURN 2>/dev/null; do :; done
done

# Allow trusted sources first, then drop everything else for those ports.
pos=1
for net in "${ALLOW[@]}"; do
  iptables -I DOCKER-USER "$pos" -s "$net" -p tcp -m multiport --dports "$PORTS" -j RETURN
  pos=$((pos + 1))
done
iptables -A DOCKER-USER -p tcp -m multiport --dports "$PORTS" -j DROP

echo "=== DOCKER-USER tras aplicar ==="
iptables -L DOCKER-USER -n --line-numbers