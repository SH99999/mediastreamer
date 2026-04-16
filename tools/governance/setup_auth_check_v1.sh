#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

echo "Auth setup check:"
echo "- branch: $(git branch --show-current 2>/dev/null || echo unknown)"

if git remote get-url git >/dev/null 2>&1; then
  echo "- remote(git): $(git remote get-url git)"
else
  echo "- remote(git): missing"
fi

token_present="no"
if [[ -n "${GH_TOKEN:-}" || -n "${GITHUB_TOKEN:-}" ]]; then
  token_present="yes"
fi
echo "- token-env-present: ${token_present}"

if git remote get-url git >/dev/null 2>&1; then
  if git push --dry-run git HEAD >/dev/null 2>&1; then
    echo "- push-auth: ok"
  else
    echo "- push-auth: blocked"
  fi
else
  echo "- push-auth: blocked (missing git remote)"
fi
