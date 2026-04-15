#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-}"
if [[ -z "$PAYLOAD_NAME" ]]; then
  echo "SR_FUN_LINE: missing payload name"
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PAYLOAD_DIR="$COMPONENT_ROOT/payload/${PAYLOAD_NAME}"
LIVE_DIR="/data/plugins/user_interface/fun_linea_overlay"
CONFIG_DIR="/data/configuration/user_interface/fun_linea_overlay"
ARCHIVE_ROOT="/opt/scale-radio/removed/fun-line"
STATE_DIR="/opt/scale-radio/state"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$STATE_DIR" "$ARCHIVE_ROOT"
echo "fun_line_apply_${PAYLOAD_NAME}" > "$STATE_DIR/fun-line.last_phase"

if [[ ! -f "$PAYLOAD_DIR/index.js" ]]; then
  echo "SR_FUN_LINE: missing payload index.js at $PAYLOAD_DIR"
  exit 2
fi
if [[ ! -f "$PAYLOAD_DIR/package.json" ]]; then
  echo "SR_FUN_LINE: missing payload package.json at $PAYLOAD_DIR"
  exit 2
fi

if [[ -d "$LIVE_DIR" ]]; then
  mv "$LIVE_DIR" "$ARCHIVE_ROOT/live.before_${PAYLOAD_NAME}.${TIMESTAMP}"
fi
if [[ -d "$CONFIG_DIR" ]]; then
  mv "$CONFIG_DIR" "$ARCHIVE_ROOT/config.before_${PAYLOAD_NAME}.${TIMESTAMP}"
fi

mkdir -p "$(dirname "$LIVE_DIR")"
mkdir -p "$LIVE_DIR"
cp -a "$PAYLOAD_DIR"/. "$LIVE_DIR"/
chmod +x "$LIVE_DIR/install.sh" "$LIVE_DIR/uninstall.sh" 2>/dev/null || true

(cd "$LIVE_DIR" && npm install --omit=dev)

if [[ -f "$LIVE_DIR/install.sh" ]]; then
  (cd "$LIVE_DIR" && bash ./install.sh)
fi

chown -R volumio:volumio "$LIVE_DIR" 2>/dev/null || true
sudo systemctl restart volumio

for i in $(seq 1 60); do
  if systemctl is-active --quiet volumio; then
    break
  fi
  sleep 2
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_FUN_LINE: volumio did not recover after installing $PAYLOAD_NAME"
  exit 2
fi

echo "SR_FUN_LINE: applied Fun Line payload $PAYLOAD_NAME"
