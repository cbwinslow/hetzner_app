#!/bin/bash
set -euo pipefail

# Install dependencies
if ! command -v envsubst >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y gettext-base
fi

# Check required environment variables
: "${DOMAIN:?DOMAIN not set}"
: "${LETSENCRYPT_EMAIL:?LETSENCRYPT_EMAIL not set}"
: "${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN not set}"

# Download Caddy with Cloudflare DNS plugin
if ! command -v caddy >/dev/null 2>&1; then
  echo "Installing Caddy with Cloudflare DNS plugin..."
  curl -fsSL "https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com/caddy-dns/cloudflare" \
    | tar xzf - -C /usr/local/bin caddy
fi

install -d /etc/caddy

envsubst < Caddyfile > /etc/caddy/Caddyfile

cat <<'SERVICE' > /etc/systemd/system/caddy.service
[Unit]
Description=Caddy web server
After=network-online.target
Requires=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/caddy run --environ --config /etc/caddy/Caddyfile
ExecReload=/usr/local/bin/caddy reload --config /etc/caddy/Caddyfile
TimeoutStopSec=5s
LimitNOFILE=1048576
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable caddy
systemctl restart caddy

echo "Caddy with Cloudflare DNS configured and running."
