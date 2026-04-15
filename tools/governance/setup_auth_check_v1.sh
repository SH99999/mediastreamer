#!/usr/bin/env bash
set -euo pipefail

REMOTE_NAME="${CANONICAL_REMOTE_NAME:-git}"
REMOTE_URL="${CANONICAL_REMOTE_URL:-https://github.com/SH99999/mediastreamer.git}"
TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
PROBE_REF="refs/heads/_auth_check_probe_$(date +%s)"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Auth check: not inside a git repository"
  exit 1
fi

if ! git remote get-url "${REMOTE_NAME}" >/dev/null 2>&1; then
  git remote add "${REMOTE_NAME}" "${REMOTE_URL}"
fi

if [[ -z "${TOKEN}" ]]; then
  echo "Auth check: GH_TOKEN/GITHUB_TOKEN missing in current runtime"
  echo "Auth check: result=blocked"
  exit 0
fi

if git push --dry-run "${REMOTE_NAME}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
  echo "Auth check: result=ok (credential helper or connector auth available)"
  exit 0
fi

REMOTE_ACTUAL_URL="$(git remote get-url "${REMOTE_NAME}")"
if [[ "${REMOTE_ACTUAL_URL}" =~ ^https://github.com/ ]]; then
  AUTH_URL="https://x-access-token:${TOKEN}@${REMOTE_ACTUAL_URL#https://}"
  if git push --dry-run "${AUTH_URL}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
    echo "Auth check: result=ok (env token usable via authenticated HTTPS URL)"
    exit 0
  fi
fi

echo "Auth check: result=blocked"
echo "Auth check: token exists but push dry-run still failed"
exit 0
