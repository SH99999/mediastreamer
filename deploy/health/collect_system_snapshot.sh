#!/usr/bin/env bash
set -euo pipefail

PHASE="${1:-snapshot}"
COMPONENT="${2:-unknown}"
STATE_ROOT="/opt/scale-radio/state/metrics"
mkdir -p "$STATE_ROOT"
OUTFILE="$STATE_ROOT/${COMPONENT}.${PHASE}.env"

mem_total_kb="$(awk '/MemTotal:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
mem_available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
loadavg1="$(cut -d ' ' -f1 /proc/loadavg 2>/dev/null || echo 0)"
rootfs_used_percent="$(df -P / | awk 'NR==2 {gsub(/%/, "", $5); print $5}' 2>/dev/null || echo 0)"
rootfs_used_kb="$(df -Pk / | awk 'NR==2 {print $3}' 2>/dev/null || echo 0)"
failed_units="$(systemctl --failed --no-legend 2>/dev/null | wc -l | tr -d ' ')"
volumio_state="$(systemctl is-active volumio 2>/dev/null || echo unknown)"
volumio_kiosk_state="$(systemctl is-active volumio-kiosk 2>/dev/null || echo unknown)"
hybrid_state="$(systemctl is-active mediastreamer-hybrid.service 2>/dev/null || echo unknown)"
renderer_state="$(systemctl is-active scale_fm_renderer.service 2>/dev/null || echo unknown)"
autoswitch_state="$(systemctl is-active revox-autoswitch.service 2>/dev/null || echo unknown)"
chromium_count="$(pgrep -fc chromium 2>/dev/null || echo 0)"
xorg_count="$(pgrep -fc Xorg 2>/dev/null || echo 0)"
node_count="$(pgrep -fc node 2>/dev/null || echo 0)"
python3_count="$(pgrep -fc python3 2>/dev/null || echo 0)"

cat > "$OUTFILE" <<EOF
PHASE=$PHASE
COMPONENT=$COMPONENT
TIMESTAMP=$(date -u +%FT%TZ)
HOSTNAME=$(hostname)
UPTIME_SECONDS=$(cut -d ' ' -f1 /proc/uptime 2>/dev/null | cut -d '.' -f1)
KERNEL=$(uname -r)
LOADAVG1=$loadavg1
MEM_TOTAL_KB=$mem_total_kb
MEM_AVAILABLE_KB=$mem_available_kb
ROOTFS_USED_PERCENT=$rootfs_used_percent
ROOTFS_USED_KB=$rootfs_used_kb
FAILED_UNIT_COUNT=$failed_units
SERVICE_VOLUMIO=$volumio_state
SERVICE_VOLUMIO_KIOSK=$volumio_kiosk_state
SERVICE_MEDIASTREAMER_HYBRID=$hybrid_state
SERVICE_SCALE_FM_RENDERER=$renderer_state
SERVICE_REVOX_AUTOSWITCH=$autoswitch_state
PROCESS_CHROMIUM_COUNT=$chromium_count
PROCESS_XORG_COUNT=$xorg_count
PROCESS_NODE_COUNT=$node_count
PROCESS_PYTHON3_COUNT=$python3_count
EOF

echo "$OUTFILE"
