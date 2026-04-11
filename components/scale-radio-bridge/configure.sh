#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "configure" > "$STATE_DIR/bridge.last_phase"

echo "Bridge configure hook entered"
echo "Bridge configuration rules will be added after the real bridge payload is imported and normalized."
