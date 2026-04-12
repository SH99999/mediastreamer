#!/usr/bin/env bash
set -euo pipefail

INSTALL_ROOT=/opt/mediastreamer-bootdelay-fix
BACKUP_DIR="$INSTALL_ROOT/backup"
LOG_DIR="$INSTALL_ROOT/logs"
mkdir -p "$BACKUP_DIR" "$LOG_DIR"

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
cp /boot/cmdline.txt "$BACKUP_DIR/cmdline.txt.$timestamp.bak"

current="$(cat /boot/cmdline.txt)"
updated="$current"

if grep -q 'bootdelay=' /boot/cmdline.txt; then
  updated="$(printf '%s' "$updated" | sed -E 's/bootdelay=[^ ]+/bootdelay=0/g')"
else
  updated="$updated bootdelay=0"
fi

printf '%s\n' "$updated" > /boot/cmdline.txt
printf '%s\n' "$timestamp" > "$INSTALL_ROOT/installed_at_utc.txt"
printf '%s\n' "v0.1.0" > "$INSTALL_ROOT/version.txt"
cp "$0" "$INSTALL_ROOT/install.sh.snapshot" || true
cp /boot/cmdline.txt "$LOG_DIR/cmdline.after.$timestamp.txt"

echo 'bootdelay fix installed.'
echo 'Previous /boot/cmdline.txt backup:'
echo "$BACKUP_DIR/cmdline.txt.$timestamp.bak"
echo 'Reboot required.'
