#!/bin/bash
set -euo pipefail

# Wrapper script to configure Caddy with Cloudflare and run deploy
./scripts/22_caddy_cloudflare_setup.sh
./deploy.sh "$@"
