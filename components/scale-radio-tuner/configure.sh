#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "configure" > "$STATE_DIR/tuner.last_phase"

echo "Tuner configure hook entered"
echo "Configuration rules will be added after the real tuner plugin payload is imported and normalized."
