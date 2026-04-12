#!/usr/bin/env bash
set -euo pipefail

mapfile -t files < <(find . -type f -name '*.sh' | sort)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "CI: no shell scripts found"
  exit 0
fi

for file in "${files[@]}"; do
  echo "CI: bash -n $file"
  bash -n "$file"
done

echo "CI: shell syntax checks passed"
