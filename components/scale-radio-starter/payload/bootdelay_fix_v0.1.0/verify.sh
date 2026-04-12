#!/usr/bin/env bash
set -euo pipefail

echo '=== /boot/cmdline.txt ==='
cat /boot/cmdline.txt

echo
echo '=== bootdelay token ==='
grep -o 'bootdelay=[^ ]*' /boot/cmdline.txt || echo 'bootdelay token not found'
