#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/workspace/mediastreamer}"
CANONICAL_REMOTE_URL="${CANONICAL_REMOTE_URL:-https://github.com/SH99999/mediastreamer.git}"
CANONICAL_REMOTE_NAME="${CANONICAL_REMOTE_NAME:-git}"
COMPAT_REMOTE_NAME="${COMPAT_REMOTE_NAME:-origin}"
NPM_TIMEOUT_SECONDS="${NPM_TIMEOUT_SECONDS:-180}"
RUN_NPM_INSTALL="${RUN_NPM_INSTALL:-false}"
ALLOW_CLONE_IF_MISSING="${ALLOW_CLONE_IF_MISSING:-false}"
RUN_GOVERNANCE_DIAGNOSTICS="${RUN_GOVERNANCE_DIAGNOSTICS:-false}"

log() {
  printf '[container-setup] %s\n' "$1"
}

ensure_repo() {
  if [[ -d "${REPO_DIR}/.git" ]]; then
    return 0
  fi

  if [[ "${ALLOW_CLONE_IF_MISSING}" != "true" ]]; then
    log "skip clone (repo missing and ALLOW_CLONE_IF_MISSING=false)"
    return 1
  fi

  mkdir -p "$(dirname "${REPO_DIR}")"
  log "clone repo into ${REPO_DIR}"
  git clone "${CANONICAL_REMOTE_URL}" "${REPO_DIR}"
  return 0
}
configure_remotes() {
  cd "${REPO_DIR}"

  git remote add "${CANONICAL_REMOTE_NAME}" "${CANONICAL_REMOTE_URL}" 2>/dev/null || true
  git remote set-url "${CANONICAL_REMOTE_NAME}" "${CANONICAL_REMOTE_URL}"

  git remote add "${COMPAT_REMOTE_NAME}" "${CANONICAL_REMOTE_URL}" 2>/dev/null || true
  git remote set-url "${COMPAT_REMOTE_NAME}" "${CANONICAL_REMOTE_URL}"

  log "remotes configured (${CANONICAL_REMOTE_NAME} + ${COMPAT_REMOTE_NAME})"
}

ensure_auth_env() {
  if [[ -z "${GH_TOKEN:-}" && -z "${GITHUB_TOKEN:-}" ]]; then
    log "WARN: GH_TOKEN/GITHUB_TOKEN missing (push auth may be blocked)"
    return 0
  fi

  export GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
  export GITHUB_TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
}

npm_install_safe() {
  local path="$1"

  if [[ ! -f "${path}/package.json" ]]; then
    log "skip npm (${path} has no package.json)"
    return 0
  fi

  if ! command -v npm >/dev/null 2>&1; then
    log "skip npm (${path} npm is unavailable in runtime)"
    return 0
  fi

  log "npm install in ${path}"
  if [[ -f "${path}/package-lock.json" ]]; then
    (cd "${path}" && timeout "${NPM_TIMEOUT_SECONDS}" npm ci --omit=dev --no-audit --no-fund) || log "WARN: npm ci failed in ${path}"
  else
    (cd "${path}" && timeout "${NPM_TIMEOUT_SECONDS}" npm install --omit=dev --no-audit --no-fund) || log "WARN: npm install failed in ${path}"
  fi
}

run_governance_checks() {
  cd "${REPO_DIR}"

  if [[ "${RUN_GOVERNANCE_DIAGNOSTICS}" != "true" ]]; then
    log "skip governance diagnostics (RUN_GOVERNANCE_DIAGNOSTICS=false)"
    return 0
  fi

  if [[ -f tools/governance/agent_git_bootstrap_v1.sh ]]; then
    bash tools/governance/agent_git_bootstrap_v1.sh || true
  fi

  if [[ -f tools/governance/setup_auth_check_v1.sh ]]; then
    bash tools/governance/setup_auth_check_v1.sh || true
  fi
}

main() {
  log "start"
  ensure_auth_env
  if ensure_repo; then
    configure_remotes
  else
    log "skip remote/governance checks (repo is unavailable in startup phase)"
    log "done"
    return 0
  fi

  if [[ "${RUN_NPM_INSTALL}" == "true" ]]; then
    cd "${REPO_DIR}"
    npm_install_safe "components/scale-radio-tuner/payload/current"
    npm_install_safe "components/scale-radio-fun-line/payload/current"
    npm_install_safe "components/scale-radio-bridge/payload/022c2_stable"
  else
    log "skip npm install (RUN_NPM_INSTALL=false). Use platform auto setup or set RUN_NPM_INSTALL=true."
  fi

  run_governance_checks
  log "done"
}

main "$@"
