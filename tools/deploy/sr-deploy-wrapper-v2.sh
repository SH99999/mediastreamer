#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
COMPONENT="${2:-}"
PAYLOAD="${3:-}"
REPO_ROOT="${4:-${GITHUB_WORKSPACE:-}}"

if [[ -z "$ACTION" || -z "$COMPONENT" || -z "$PAYLOAD" || -z "$REPO_ROOT" ]]; then
  echo "Usage: sr-deploy <deploy|rollback> <component> <payload> <repo_root>"
  exit 1
fi

resolve_bridge_payload() {
  local requested="$1"
  local payload_root="$REPO_ROOT/components/scale-radio-bridge/payload"
  if [[ -d "$payload_root/$requested" ]]; then
    printf '%s\n' "$requested"
    return 0
  fi

  case "$requested" in
    current_dev)
      if [[ -d "$payload_root/023_db_cache_r1" ]]; then
        echo "SR_BRIDGE: resolving payload alias current_dev -> 023_db_cache_r1" >&2
        printf '%s\n' "023_db_cache_r1"
        return 0
      fi
      ;;
    current)
      if [[ -d "$payload_root/022c2_stable" ]]; then
        echo "SR_BRIDGE: resolving payload alias current -> 022c2_stable" >&2
        printf '%s\n' "022c2_stable"
        return 0
      fi
      ;;
  esac

  echo "SR_BRIDGE: unresolved payload alias $requested under $payload_root" >&2
  exit 2
}

case "$COMPONENT" in
  bridge)
    BASE="$REPO_ROOT/components/scale-radio-bridge/deploy_candidates"
    APPLY="$BASE/apply_payload_v2.sh"
    HEALTH="$BASE/healthcheck_runtime_v2.sh"
    REMOVE="$BASE/remove_active_v2.sh"
    RESOLVED_PAYLOAD="$(resolve_bridge_payload "$PAYLOAD")"
    ;;
  *)
    echo "Unsupported component: $COMPONENT"
    exit 2
    ;;
esac

case "$ACTION" in
  deploy)
    bash "$APPLY" "$RESOLVED_PAYLOAD"
    bash "$HEALTH" "$RESOLVED_PAYLOAD"
    ;;
  rollback)
    bash "$REMOVE" "$RESOLVED_PAYLOAD"
    ;;
  *)
    echo "Unsupported action: $ACTION"
    exit 2
    ;;
esac
