#!/usr/bin/env bash
set -e

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo ./setup.sh"
  exit 1
fi

USER_NAME=$(logname)

echo "=== Minimal Home Server Setup ==="
echo "User: $USER_NAME"

apt update && apt upgrade -y
apt install -y ca-certificates curl gnupg ufw

echo "Installing Docker..."
curl -fsSL https://get.docker.com | sh
usermod -aG docker "$USER_NAME"

echo "Installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh
systemctl enable --now tailscaled

echo "Disable sleep on lid close..."
sed -i 's/^#HandleLidSwitch=.*/HandleLidSwitch=ignore/' /etc/systemd/logind.conf
sed -i 's/^#HandleLidSwitchDocked=.*/HandleLidSwitchDocked=ignore/' /etc/systemd/logind.conf
systemctl restart systemd-logind

echo "Firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 41641/udp
ufw allow 51820/udp
ufw --force enable

echo "Enable IP forwarding..."
cat > /etc/sysctl.d/99-wireguard.conf <<'EOF'
net.ipv4.ip_forward=1
net.ipv4.conf.all.src_valid_mark=1
EOF
sysctl -q -p /etc/sysctl.d/99-wireguard.conf

echo "Create directories..."
mkdir -p /srv/{infra,data/{gitea,homarr,prowlarr,radarr,sonarr,uptime,wireguard,postgres,redis},data/jellyfin/{cache,config},data/transmission/{config,downloads,watch},media/{movies,music,tv}}
chown -R "$USER_NAME":"$USER_NAME" /srv

echo "Setup complete!"
echo ""
echo "Next:"
echo "  1. Re-login or run: newgrp docker"
echo "  2. Run: tailscale up"
echo "  3. Copy docker-compose.yml to /srv/infra/"
echo "  4. Copy .env.example to /srv/infra/.env and fill in secrets"
echo "  5. Build newsletter image: docker build -t email_newsletter:latest <path-to-email_newsletter>"
echo "  6. Run: docker compose up -d (from /srv/infra/)"
echo "  7. Run migrations against postgres from the email_newsletter repo:"
echo "     SKIP_DOCKER=1 POSTGRES_PORT=5432 POSTGRES_PASSWORD=<pw> ./scripts/init_db.sh"
