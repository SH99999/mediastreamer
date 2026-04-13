#!/usr/bin/env bash
set -euo pipefail

fail() { echo "CI: $1"; exit 1; }

components=(
  scale-radio-bridge
  scale-radio-tuner
  scale-radio-starter
  scale-radio-autoswitch
  scale-radio-fun-line
  scale-radio-hardware
)

for component in "${components[@]}"; do
  readme="components/${component}/README.md"
  current_state="journals/${component}/current_state_v1.md"
  stream="journals/${component}/stream_v1.md"

  [[ -f "$readme" ]] || fail "Missing component README: $readme"
  [[ -f "$current_state" ]] || fail "Missing component current-state journal: $current_state"
  [[ -f "$stream" ]] || fail "Missing component stream journal: $stream"

  if grep -Eiq 'reserved path|^# Component Root$|placeholder|This path is reserved' "$readme"; then
    fail "Stub/placeholder README detected: $readme"
  fi

done

echo "CI: active component hygiene checks passed"
