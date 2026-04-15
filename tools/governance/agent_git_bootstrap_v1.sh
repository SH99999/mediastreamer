#!/usr/bin/env bash
set -euo pipefail

REMOTE_NAME="${CANONICAL_REMOTE_NAME:-git}"
REMOTE_URL="${CANONICAL_REMOTE_URL:-https://github.com/SH99999/mediastreamer.git}"
CANONICAL_OWNER_REPO="${CANONICAL_OWNER_REPO:-SH99999/mediastreamer}"
BASE_BRANCH="${CANONICAL_BASE_BRANCH:-main}"
AUTO_SYNC_MAIN="${AUTO_SYNC_MAIN:-true}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: not inside a git repository"
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || true)"
if [[ -z "${CURRENT_BRANCH}" ]]; then
  CURRENT_BRANCH="(detached-head)"
fi

normalize_remote_identity() {
  local url="$1"
  url="${url%.git}"
  case "${url}" in
    "https://github.com/${CANONICAL_OWNER_REPO}"|"http://github.com/${CANONICAL_OWNER_REPO}"|"git@github.com:${CANONICAL_OWNER_REPO}"|"ssh://git@github.com/${CANONICAL_OWNER_REPO}")
      echo "github.com/${CANONICAL_OWNER_REPO}"
      return 0
      ;;
    *)
      echo "${url}"
      return 0
      ;;
  esac
}

if git remote get-url "${REMOTE_NAME}" >/dev/null 2>&1; then
  CURRENT_REMOTE_URL="$(git remote get-url "${REMOTE_NAME}")"
  CURRENT_REMOTE_IDENTITY="$(normalize_remote_identity "${CURRENT_REMOTE_URL}")"
  CANONICAL_REMOTE_IDENTITY="$(normalize_remote_identity "${REMOTE_URL}")"
  if [[ "${CURRENT_REMOTE_IDENTITY}" == "${CANONICAL_REMOTE_IDENTITY}" ]]; then
    REMOTE_STATUS="ok (equivalent-url)"
  elif [[ "${CURRENT_REMOTE_URL}" != "${REMOTE_URL}" ]]; then
    git remote set-url "${REMOTE_NAME}" "${REMOTE_URL}"
    REMOTE_STATUS="ok (updated-url)"
  else
    REMOTE_STATUS="ok"
  fi
else
  git remote add "${REMOTE_NAME}" "${REMOTE_URL}"
  REMOTE_STATUS="ok (added)"
fi

PUSH_AUTH_STATUS="blocked"
PUSH_AUTH_DETAIL="auth not available in current runtime"
PROBE_REF="refs/heads/_bootstrap_auth_probe_$(date +%s)"
BASE_SYNC_STATUS="skipped"
BASE_SYNC_DETAIL="disabled or non-target branch"

if git push --dry-run "${REMOTE_NAME}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
  PUSH_AUTH_STATUS="ok"
  PUSH_AUTH_DETAIL="push dry-run succeeded"
else
  TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
  if [[ -n "${TOKEN}" ]]; then
    REMOTE_ACTUAL_URL="$(git remote get-url "${REMOTE_NAME}")"
    if [[ "${REMOTE_ACTUAL_URL}" =~ ^https://github.com/ ]]; then
      AUTH_REMOTE_URL="https://x-access-token:${TOKEN}@${REMOTE_ACTUAL_URL#https://}"
      if git push --dry-run "${AUTH_REMOTE_URL}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
        PUSH_AUTH_STATUS="ok"
        PUSH_AUTH_DETAIL="env token is usable for authenticated HTTPS push"
      else
        PUSH_AUTH_DETAIL="token present but push dry-run failed"
      fi
    else
      PUSH_AUTH_DETAIL="token present but remote is not HTTPS github URL"
    fi
  fi
fi

if [[ "${AUTO_SYNC_MAIN}" == "true" && "${CURRENT_BRANCH}" != "(detached-head)" && "${CURRENT_BRANCH}" != "${BASE_BRANCH}" ]]; then
  if git fetch "${REMOTE_NAME}" "${BASE_BRANCH}" >/dev/null 2>&1; then
    if [[ "${CURRENT_BRANCH}" =~ ^(si|dev|integration)/ ]]; then
      if [[ -n "$(git status --porcelain)" ]]; then
        BASE_SYNC_STATUS="blocked"
        BASE_SYNC_DETAIL="working tree not clean"
      elif git rebase "${REMOTE_NAME}/${BASE_BRANCH}" >/dev/null 2>&1; then
        BASE_SYNC_STATUS="ok"
        BASE_SYNC_DETAIL="rebased onto ${REMOTE_NAME}/${BASE_BRANCH}"
      else
        git rebase --abort >/dev/null 2>&1 || true
        BASE_SYNC_STATUS="blocked"
        BASE_SYNC_DETAIL="rebase conflict against ${REMOTE_NAME}/${BASE_BRANCH}"
      fi
    else
      BASE_SYNC_STATUS="skipped"
      BASE_SYNC_DETAIL="branch does not match si/*, dev/*, or integration/*"
    fi
  else
    BASE_SYNC_STATUS="blocked"
    BASE_SYNC_DETAIL="failed to fetch ${REMOTE_NAME}/${BASE_BRANCH}"
  fi
fi

echo "Bootstrap status:"
echo "- branch: ${CURRENT_BRANCH}"
echo "- remote(${REMOTE_NAME}): ${REMOTE_STATUS}"
echo "- base sync: ${BASE_SYNC_STATUS} (${BASE_SYNC_DETAIL})"
echo "- push auth: ${PUSH_AUTH_STATUS} (${PUSH_AUTH_DETAIL})"

if [[ "${PUSH_AUTH_STATUS}" == "ok" ]]; then
  echo "- ready now: create/update dedicated branch, commit, push, and open PR to main"
  echo "- owner action needed: none"
else
  echo "- ready now: local implementation, commit packaging, and PR text preparation"
  echo "- owner action needed: provide runtime git push auth (token/connector auth) or run final push locally"
fi
