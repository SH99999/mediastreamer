#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-unknown}"
LIVE_DIR="/data/plugins/user_interface/fun_linea_overlay"
STATE_DIR="/opt/scale-radio/state"

mkdir -p "$STATE_DIR"
echo "fun_line_healthcheck_${PAYLOAD_NAME}" > "$STATE_DIR/fun-line.last_phase"

required=(
  "$LIVE_DIR/index.js"
  "$LIVE_DIR/package.json"
  "$LIVE_DIR/UIConfig.json"
  "$LIVE_DIR/config.json"
  "$LIVE_DIR/node_modules/kew"
)

for path in "${required[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "SR_FUN_LINE: missing required live path $path"
    exit 2
  fi
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_FUN_LINE: volumio is not active"
  exit 2
fi
if ! systemctl is-active --quiet volumio-kiosk; then
  echo "SR_FUN_LINE: volumio-kiosk is not active"
  exit 2
fi
if [[ "$(pgrep -fc chromium || true)" -lt 1 ]]; then
  echo "SR_FUN_LINE: chromium is not running"
  exit 2
fi
if [[ "$(pgrep -fc Xorg || true)" -lt 1 ]]; then
  echo "SR_FUN_LINE: Xorg is not running"
  exit 2
fi

echo "SR_FUN_LINE: Fun Line runtime healthcheck passed for $PAYLOAD_NAME"
