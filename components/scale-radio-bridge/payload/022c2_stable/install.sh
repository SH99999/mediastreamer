#!/bin/bash
set -e
PDIR="$(cd "$(dirname "$0")" && pwd)"
CDIR="/data/configuration/user_interface/radioscale_overlay_bridge"
CFG="$CDIR/config.json"
DEF="$PDIR/config.json"
mkdir -p "$CDIR"
DEFAULT_FILE="$DEF" TARGET_FILE="$CFG" node <<'NODE'
const fs = require('fs');
const d = JSON.parse(fs.readFileSync(process.env.DEFAULT_FILE, 'utf8'));
let e = {};
try { e = JSON.parse(fs.readFileSync(process.env.TARGET_FILE, 'utf8')); } catch (err) {}
const m = JSON.parse(JSON.stringify(d));
for (const [k, def] of Object.entries(d)) {
  if (!Object.prototype.hasOwnProperty.call(e, k)) continue;
  const src = e[k];
  if (src && typeof src === 'object' && Object.prototype.hasOwnProperty.call(src, 'value')) m[k].value = src.value;
  else m[k].value = src;
}
fs.writeFileSync(process.env.TARGET_FILE, JSON.stringify(m, null, 2));
NODE
chown -R volumio:volumio "$CDIR" || true
chmod 755 "$CDIR" || true
chmod 664 "$CFG" || true
npm install --omit=dev
