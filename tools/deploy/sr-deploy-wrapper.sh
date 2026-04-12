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

case "$COMPONENT" in
  bridge)
    BASE="$REPO_ROOT/components/scale-radio-bridge/deploy_candidates"
    APPLY="$BASE/apply_payload_v2.sh"
    HEALTH="$BASE/healthcheck_runtime_v2.sh"
    REMOVE="$BASE/remove_active_v2.sh"
    ;;
  *)
    echo "Unsupported component: $COMPONENT"
    exit 2
    ;;
esac

case "$ACTION" in
  deploy)
    bash "$APPLY" "$PAYLOAD"
    bash "$HEALTH" "$PAYLOAD"
    ;;
  rollback)
    bash "$REMOVE" "$PAYLOAD"
    ;;
  *)
    echo "Unsupported action: $ACTION"
    exit 2
    ;;
esac
