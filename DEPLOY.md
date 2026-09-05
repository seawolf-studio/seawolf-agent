# 🐺 DEPLOY: Seawolf Agent en VPS Hostinger
# ==============================================
# VPS: KVM2 (8GB RAM, 100GB SSD, 1TB ancho de banda)
# Sistema: Ubuntu 22.04 LTS (recomendado)

## 1. CONECTARSE AL VPS
```bash
ssh root@TU_IP_VPS
```

## 2. INSTALAR DEPENDENCIAS
```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Python 3.11+
apt install -y python3 python3-pip python3-venv curl git

# Instalar Node.js 18+ (para WebUI)
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Instalar Nginx
apt install -y nginx certbot python3-certbot-nginx
```

## 3. CLONAR REPOS
```bash
mkdir -p /opt/seawolf
cd /opt/seawolf

# Clonar WebUI
git clone https://github.com/seawolfk/seawolf-agent-webui.git webui
cd webui
pip install -r requirements.txt

# Clonar assets y skins
cd /opt/seawolf
git clone https://github.com/seawolfk/seawolf-agent.git config
```

## 4. INSTALAR HERMES (backend del agente)
```bash
bash <(curl -sSf https://hermes-agent.nousresearch.com/install.sh)
# Configurar skin Seawolf como predeterminada
cp /opt/seawolf/config/skins/seawolf.yaml ~/.hermes/skins/
echo "SKIN=seawolf" >> ~/.hermes/.env
```

## 5. CONFIGURAR NGINX
```bash
cat > /etc/nginx/sites-available/seawolf << 'EOF'
server {
    listen 80;
    server_name seawolf-agent.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8642;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/seawolf /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# SSL con Certbot
certbot --nginx -d seawolf-agent.tu-dominio.com
```

## 6. INICIAR SERVICIOS
```bash
# Iniciar WebUI
cd /opt/seawolf/webui
nohup python server.py --port 8642 > /var/log/seawolf-webui.log 2>&1 &
echo $! > /var/run/seawolf-webui.pid

# Verificar que corre
curl http://127.0.0.1:8642
```