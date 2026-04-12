#!/usr/bin/env bash
set -euo pipefail

INSTALL_ROOT=/opt/mediastreamer-bootdelay-fix
BACKUP_DIR="$INSTALL_ROOT/backup"

latest_backup="$(ls -1t "$BACKUP_DIR"/cmdline.txt.*.bak 2>/dev/null | head -n1 || true)"
if [[ -z "$latest_backup" ]]; then
  echo 'No backup found. Nothing restored.'
  exit 1
fi

cp "$latest_backup" /boot/cmdline.txt

echo 'Restored /boot/cmdline.txt from:'
echo "$latest_backup"
echo 'Reboot required.'
