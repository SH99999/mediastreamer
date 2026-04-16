#!/usr/bin/env bash
set -euo pipefail

REMOTE_NAME="${CANONICAL_REMOTE_NAME:-git}"
REMOTE_URL="${CANONICAL_REMOTE_URL:-https://github.com/SH99999/mediastreamer.git}"
CANONICAL_OWNER_REPO="${CANONICAL_OWNER_REPO:-SH99999/mediastreamer}"
BASE_BRANCH="${CANONICAL_BASE_BRANCH:-main}"
AUTO_SYNC_MAIN="${AUTO_SYNC_MAIN:-true}"
REQUESTED_BRANCH="${REQUESTED_BRANCH:-}"
ROLE_HINT="${ROLE_HINT:-generic}"
CONTEXT_MODE="${BOOTSTRAP_CONTEXT_MODE:-classic}"

print_usage() {
  cat <<'EOF'
Usage:
  bash tools/governance/agent_git_bootstrap_v1.sh [branch]
  bash tools/governance/agent_git_bootstrap_v1.sh --branch <si/*|dev/*|integration/*> [--role <role>] [--mode <classic|mode-b>]

Options:
  --branch <name>   Explicit branch prep target.
  --role <name>     Role profile hint (tuner | bridge | si | governance | generic).
  --mode <name>     Context mode:
                    - classic (existing behavior)
                    - mode-b  (need-to-know startup + deferred references)
  --help            Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      print_usage
      exit 0
      ;;
    --branch)
      REQUESTED_BRANCH="${2:-}"
      shift 2
      ;;
    --role)
      ROLE_HINT="${2:-generic}"
      shift 2
      ;;
    --mode)
      CONTEXT_MODE="${2:-classic}"
      shift 2
      ;;
    --*)
      echo "error: unknown option: $1"
      print_usage
      exit 1
      ;;
    *)
      if [[ -z "${REQUESTED_BRANCH}" ]]; then
        REQUESTED_BRANCH="$1"
      else
        echo "error: unexpected positional argument: $1"
        print_usage
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ "${CONTEXT_MODE}" != "classic" && "${CONTEXT_MODE}" != "mode-b" ]]; then
  echo "error: --mode must be classic or mode-b"
  exit 1
fi

role_bootstrap_lines() {
  local role="$1"
  local mode="$2"
  case "${role}" in
    tuner)
      echo "- role profile: tuner"
      echo "- branch hint: dev/tuner"
      echo "- startup packet: AGENTS.md; tools/governance/agent_git_bootstrap_v1.sh; docs/agents/agent_git_bootstrap_v1.md; journals/scale-radio-tuner/current_state_v2.md"
      ;;
    bridge)
      echo "- role profile: bridge"
      echo "- branch hint: dev/bridge"
      echo "- startup packet: AGENTS.md; tools/governance/agent_git_bootstrap_v1.sh; docs/agents/agent_git_bootstrap_v1.md; journals/scale-radio-bridge/current_state_v1.md"
      ;;
    si|system-integration|governance)
      echo "- role profile: system-integration"
      echo "- branch hint: si/<topic>"
      echo "- startup packet: AGENTS.md; tools/governance/agent_git_bootstrap_v1.sh; docs/agents/agent_git_bootstrap_v1.md; contracts/repo/system_integration_governance_index_v7.md"
      ;;
    *)
      echo "- role profile: generic"
      echo "- branch hint: si/<topic> or dev/<component>"
      echo "- startup packet: AGENTS.md; tools/governance/agent_git_bootstrap_v1.sh; docs/agents/agent_git_bootstrap_v1.md"
      ;;
  esac

  if [[ "${mode}" == "mode-b" ]]; then
    echo "- context mode: mode-b (need-to-know first, deferred full read-order)"
    echo "- deferred packet: docs/agents/role_bootstrap_reference_map_v1.md (single-source deferred links)"
    echo "- deferred profile source: docs/agents/role_bootstrap_profiles_v1.md (role pack + escalation triggers)"
  else
    echo "- context mode: classic (full standard read-order expected)"
  fi
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: not inside a git repository"
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || true)"
if [[ -z "${CURRENT_BRANCH}" ]]; then
  CURRENT_BRANCH="(detached-head)"
fi
BRANCH_PREP_STATUS="skipped"
BRANCH_PREP_DETAIL="no requested branch"

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

if [[ -n "${REQUESTED_BRANCH}" ]]; then
  if [[ "${REQUESTED_BRANCH}" =~ ^(si|dev|integration)/ ]]; then
    if [[ "${CURRENT_BRANCH}" == "${REQUESTED_BRANCH}" ]]; then
      BRANCH_PREP_STATUS="ok"
      BRANCH_PREP_DETAIL="already on requested branch"
    else
      if git show-ref --verify --quiet "refs/remotes/${REMOTE_NAME}/${REQUESTED_BRANCH}"; then
        git checkout -B "${REQUESTED_BRANCH}" "${REMOTE_NAME}/${REQUESTED_BRANCH}" >/dev/null 2>&1
        BRANCH_PREP_STATUS="ok"
        BRANCH_PREP_DETAIL="checked out ${REQUESTED_BRANCH} from ${REMOTE_NAME}/${REQUESTED_BRANCH}"
      elif git fetch "${REMOTE_NAME}" "${BASE_BRANCH}" >/dev/null 2>&1 && git show-ref --verify --quiet "refs/remotes/${REMOTE_NAME}/${BASE_BRANCH}"; then
        git checkout -B "${REQUESTED_BRANCH}" "${REMOTE_NAME}/${BASE_BRANCH}" >/dev/null 2>&1
        BRANCH_PREP_STATUS="ok"
        BRANCH_PREP_DETAIL="created ${REQUESTED_BRANCH} from ${REMOTE_NAME}/${BASE_BRANCH}"
      elif git show-ref --verify --quiet "refs/heads/${REQUESTED_BRANCH}"; then
        git checkout "${REQUESTED_BRANCH}" >/dev/null 2>&1
        BRANCH_PREP_STATUS="ok"
        BRANCH_PREP_DETAIL="checked out existing local branch"
      else
        BRANCH_PREP_STATUS="blocked"
        BRANCH_PREP_DETAIL="could not create or checkout requested branch"
      fi
      CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || true)"
      if [[ -z "${CURRENT_BRANCH}" ]]; then
        CURRENT_BRANCH="(detached-head)"
      fi
    fi
  else
    BRANCH_PREP_STATUS="blocked"
    BRANCH_PREP_DETAIL="requested branch must match si/*, dev/*, or integration/*"
  fi
fi

PUSH_AUTH_STATUS="blocked"
PUSH_AUTH_DETAIL="auth not available in current runtime"
PROBE_REF="refs/heads/_bootstrap_auth_probe_$(date +%s)"
BASE_SYNC_STATUS="skipped"
BASE_SYNC_DETAIL="disabled or non-target branch"
TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"

if git push --dry-run "${REMOTE_NAME}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
  PUSH_AUTH_STATUS="ok"
  PUSH_AUTH_DETAIL="push dry-run succeeded"
elif [[ -n "${TOKEN}" ]]; then
  REMOTE_ACTUAL_URL="$(git remote get-url "${REMOTE_NAME}")"
  if [[ "${REMOTE_ACTUAL_URL}" =~ ^https://github.com/ ]]; then
    git config --local credential.helper \
      '!f() { test -n "${GH_TOKEN:-${GITHUB_TOKEN:-}}" || exit 0; echo username=x-access-token; echo password="${GH_TOKEN:-${GITHUB_TOKEN:-}}"; }; f'
    if git push --dry-run "${REMOTE_NAME}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
      PUSH_AUTH_STATUS="ok"
      PUSH_AUTH_DETAIL="configured credential helper from GH_TOKEN/GITHUB_TOKEN"
    else
      AUTH_REMOTE_URL="https://x-access-token:${TOKEN}@${REMOTE_ACTUAL_URL#https://}"
      if git push --dry-run "${AUTH_REMOTE_URL}" "HEAD:${PROBE_REF}" >/dev/null 2>&1; then
        PUSH_AUTH_STATUS="ok"
        PUSH_AUTH_DETAIL="env token is usable for authenticated HTTPS push"
      else
        PUSH_AUTH_DETAIL="token present but push dry-run failed"
      fi
    fi
  else
    PUSH_AUTH_DETAIL="token present but remote is not HTTPS github URL"
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
echo "- branch prep: ${BRANCH_PREP_STATUS} (${BRANCH_PREP_DETAIL})"
echo "- base sync: ${BASE_SYNC_STATUS} (${BASE_SYNC_DETAIL})"
echo "- push auth: ${PUSH_AUTH_STATUS} (${PUSH_AUTH_DETAIL})"
role_bootstrap_lines "${ROLE_HINT}" "${CONTEXT_MODE}"

if [[ "${PUSH_AUTH_STATUS}" == "ok" ]]; then
  echo "- ready now: create/update dedicated branch, commit, push, and open PR to main"
  echo "- owner action needed: none"
else
  echo "- ready now: local implementation, commit packaging, and PR text preparation"
  echo "- owner action needed: provide runtime git push auth (token/connector auth) or run final push locally"
fi
