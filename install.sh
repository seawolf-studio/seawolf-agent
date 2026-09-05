# 🐺 SEAWOLF AGENT — Deployment automático
# Versión: 1.0.0
# Ejecutar en el VPS Hostinger

set -e

echo "🐺 Seawolf Agent — Instalación automática"
echo "=========================================="

# 1. Dependencias
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv curl git nginx certbot python3-certbot-nginx curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 2. Directorios
mkdir -p /opt/seawolf
cd /opt/seawolf

# 3. Clonar repos
echo "📥 Clonando WebUI..."
git clone https://github.com/seawolfk/seawolf-agent-webui.git webui

echo "📥 Clonando config..."
git clone https://github.com/seawolfk/seawolf-agent.git config

# 4. Instalar Python deps
cd webui
pip install -r requirements.txt 2>/dev/null || pip install flask

# 5. Instalar Hermes + skin
echo "🤖 Instalando Hermes Agent..."
bash <(curl -sSf https://hermes-agent.nousresearch.com/install.sh)
mkdir -p ~/.hermes/skins
cp /opt/seawolf/config/skins/seawolf.yaml ~/.hermes/skins/
echo "SKIN=seawolf" >> ~/.hermes/.env

echo ""
echo "✅ Instalación completada."
echo "Próximo paso: Configurar Nginx y SSL en DEPLOY.md"