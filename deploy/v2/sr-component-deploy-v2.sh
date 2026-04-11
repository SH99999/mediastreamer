#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: sr-component-deploy-v2.sh <tuner|bridge> <ref|latest>"
  exit 1
fi

COMPONENT="$1"
REQUESTED_REF="$2"
REPO_URL="git@github.com:SH99999/mediastreamer.git"
REPO_DIR="/opt/scale-radio/repo"
STATE_DIR="/opt/scale-radio/state"
INSTALL_ROOT="/opt/scale-radio/components"
CANONICAL_REF="$REQUESTED_REF"

if [[ "$CANONICAL_REF" == "latest" ]]; then
  CANONICAL_REF="main"
fi

case "$COMPONENT" in
  tuner|bridge) ;;
  *) echo "Deploy V2 fast loop currently supports only tuner or bridge"; exit 1 ;;
esac

mkdir -p "$STATE_DIR" "$INSTALL_ROOT"

echo "preflight" > "$STATE_DIR/${COMPONENT}.last_phase"

rollback_on_error() {
  echo "failure" > "$STATE_DIR/${COMPONENT}.last_phase"
  date -u +%FT%TZ > "$STATE_DIR/${COMPONENT}.last_failure_at"
  bash "$(dirname "$0")/sr-component-rollback.sh" "$COMPONENT" clean-absent || true
}
trap rollback_on_error ERR

if [[ ! -d "$REPO_DIR/.git" ]]; then
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone "$REPO_URL" "$REPO_DIR"
fi

git -C "$REPO_DIR" fetch --all --tags --prune
if git -C "$REPO_DIR" show-ref --verify --quiet "refs/remotes/origin/$CANONICAL_REF"; then
  git -C "$REPO_DIR" checkout -B "$CANONICAL_REF" "origin/$CANONICAL_REF"
else
  git -C "$REPO_DIR" checkout "$CANONICAL_REF"
fi

SRC="$REPO_DIR/components/scale-radio-${COMPONENT}"
DST="$INSTALL_ROOT/$COMPONENT"
mkdir -p "$DST"
rm -rf "$DST"/*
cp -a "$SRC"/. "$DST"/

pushd "$DST" >/dev/null
bash ./install.sh
bash ./configure.sh
bash ./healthcheck.sh
popd >/dev/null

trap - ERR

echo "$CANONICAL_REF" > "$STATE_DIR/${COMPONENT}.last_ref"
echo "$CANONICAL_REF" > "$STATE_DIR/${COMPONENT}.last_successful_ref"
echo "$COMPONENT" > "$STATE_DIR/last_scope"
date -u +%FT%TZ > "$STATE_DIR/last_deploy_request.txt"
echo "state_write" > "$STATE_DIR/${COMPONENT}.last_phase"

echo "Deploy V2 completed for $COMPONENT"
