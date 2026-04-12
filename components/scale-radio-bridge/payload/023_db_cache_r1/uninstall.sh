#!/bin/bash
PDIR="$(cd "$(dirname "$0")" && pwd)"
chown -R volumio:volumio "$PDIR" 2>/dev/null || true
chmod -R u+rwX,go+rX "$PDIR" 2>/dev/null || true
exit 0
