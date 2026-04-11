#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: sr-component-rollback.sh <tuner|bridge> [clean-absent]"
  exit 1
fi

COMPONENT="$1"
MODE="${2:-clean-absent}"
STATE_DIR="/opt/scale-radio/state"
INSTALL_ROOT="/opt/scale-radio/components"
COMPONENT_DIR="$INSTALL_ROOT/$COMPONENT"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$STATE_DIR"

echo "$MODE" > "$STATE_DIR/${COMPONENT}.rollback_mode"
date -u +%FT%TZ > "$STATE_DIR/${COMPONENT}.rollback_at"
echo "rollback" > "$STATE_DIR/${COMPONENT}.last_phase"

if [[ -x "$COMPONENT_DIR/uninstall.sh" ]]; then
  (cd "$COMPONENT_DIR" && bash ./uninstall.sh) || true
fi

if [[ -d "$COMPONENT_DIR" ]]; then
  mv "$COMPONENT_DIR" "${COMPONENT_DIR}.removed.${TIMESTAMP}"
fi

mkdir -p "$COMPONENT_DIR"

if [[ "$MODE" != "clean-absent" ]]; then
  echo "Unsupported rollback mode in V1: $MODE"
  exit 1
fi

echo "Component $COMPONENT rolled back to clean-absent state"
