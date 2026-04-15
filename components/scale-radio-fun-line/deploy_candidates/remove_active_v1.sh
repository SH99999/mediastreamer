#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-fun-line}"
LIVE_DIR="/data/plugins/user_interface/fun_linea_overlay"
CONFIG_DIR="/data/configuration/user_interface/fun_linea_overlay"
ARCHIVE_ROOT="/opt/scale-radio/removed/fun-line"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STATE_DIR="/opt/scale-radio/state"

mkdir -p "$STATE_DIR" "$ARCHIVE_ROOT"
echo "fun_line_remove_${PAYLOAD_NAME}" > "$STATE_DIR/fun-line.last_phase"

REMOVED_LIVE=""
if [[ -d "$LIVE_DIR" ]]; then
  REMOVED_LIVE="$ARCHIVE_ROOT/live.${PAYLOAD_NAME}.${TIMESTAMP}"
  mv "$LIVE_DIR" "$REMOVED_LIVE"
fi
if [[ -d "$CONFIG_DIR" ]]; then
  mv "$CONFIG_DIR" "$ARCHIVE_ROOT/config.${PAYLOAD_NAME}.${TIMESTAMP}"
fi

if [[ -n "$REMOVED_LIVE" && -f "$REMOVED_LIVE/uninstall.sh" ]]; then
  (cd "$REMOVED_LIVE" && bash ./uninstall.sh)
fi

sudo systemctl restart volumio

for i in $(seq 1 60); do
  if systemctl is-active --quiet volumio; then
    break
  fi
  sleep 2
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_FUN_LINE: volumio did not recover after Fun Line removal"
  exit 2
fi

echo "SR_FUN_LINE: removed active Fun Line runtime for $PAYLOAD_NAME"
