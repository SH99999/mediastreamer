#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="/opt/scale-radio"
BIN_DIR="/usr/local/bin"

sudo mkdir -p "$TARGET_DIR" "$BIN_DIR"
sudo cp deploy/pi/sr-deploy "$BIN_DIR/sr-deploy"
sudo cp deploy/pi/sr-rollback "$BIN_DIR/sr-rollback"
sudo chmod +x "$BIN_DIR/sr-deploy" "$BIN_DIR/sr-rollback"

echo "Scale Radio deploy tools installed."
