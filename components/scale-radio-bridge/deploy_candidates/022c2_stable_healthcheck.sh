#!/usr/bin/env bash
set -euo pipefail

# Verify that the stable Bridge payload is materially installed in the live Volumio plugin path.
# Inputs: none.
# Outputs: prints healthcheck status to stdout.
# Side effects: writes current Bridge phase to state.
# Failure behavior: exits non-zero if required files are missing.
# Dependencies: bash, test, Volumio plugin filesystem layout.

LIVE_DIR="/data/plugins/user_interface/radioscale_overlay_bridge"
STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "bridge_healthcheck_022c2_stable" > "$STATE_DIR/bridge.last_phase"

required=(
  "$LIVE_DIR/index.js"
  "$LIVE_DIR/config.json"
  "$LIVE_DIR/UIConfig.json"
  "$LIVE_DIR/package.json"
  "$LIVE_DIR/public/index.html"
  "$LIVE_DIR/public/style.css"
  "$LIVE_DIR/public/app.js"
  "$LIVE_DIR/i18n/strings_en.json"
)

for path in "${required[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "SR_BRIDGE: missing required live file $path"
    exit 2
  fi
done

echo "SR_BRIDGE: stable Bridge healthcheck passed"
