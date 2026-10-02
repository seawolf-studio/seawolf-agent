#!/usr/bin/env bash
set -u
cd /opt/nereus/graphiti/mcp_server
# Bajar el stack FalkorDB (incompatible)
cd docker && docker compose -f docker-compose-falkordb.yml -f docker-compose.override.yml down 2>&1 | tail -2
cd /opt/nereus/graphiti/mcp_server

KEY=$(awk -F= '/^OPENROUTER_API_KEY=/{print $2}' /root/.hermes/.env | tr -d '"')
PW=$(openssl rand -hex 16)

cat > .env <<EOF
OPENAI_API_KEY=${KEY}
OPENAI_API_URL=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4o-mini
EMBEDDER_MODEL=openai/text-embedding-3-small
SEMAPHORE_LIMIT=3
GRAPHITI_GROUP_ID=nereus
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=${PW}
NEO4J_DATABASE=neo4j
EOF
chmod 600 .env

cat > docker/docker-compose.neox.yml <<'EOF'
services:
  neo4j:
    ports: !override
      - "127.0.0.1:7474:7474"
      - "127.0.0.1:7687:7687"
  graphiti-mcp:
    ports: !override
      - "127.0.0.1:8100:8000"
EOF

echo "=== .env graphiti-neo4j (secretos ocultos) ==="
grep -vE "^OPENAI_API_KEY|^NEO4J_PASSWORD" .env
cd docker
setsid nohup docker compose -f docker-compose-neo4j.yml -f docker-compose.neox.yml up -d > /opt/nereus/graphiti-neo4j.log 2>&1 < /dev/null &
echo "lanzado"
