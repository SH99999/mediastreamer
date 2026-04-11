#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: sr-deploy.sh <bundle|starter|tuner|autoswitch|bridge|fun-line> <ref|latest>"
  exit 1
fi

SCOPE="$1"
REQUESTED_REF="$2"
REPO_URL="git@github.com:SH99999/mediastreamer.git"
REPO_DIR="/opt/scale-radio/repo"
STATE_DIR="/opt/scale-radio/state"
INSTALL_ROOT="/opt/scale-radio/components"
CANONICAL_REF="${REQUESTED_REF}"

if [[ "$CANONICAL_REF" == "latest" ]]; then
  CANONICAL_REF="main"
fi

mkdir -p "$STATE_DIR" "$INSTALL_ROOT"

echo "Scale Radio deploy v1"
echo "scope=$SCOPE requested_ref=$REQUESTED_REF canonical_ref=$CANONICAL_REF"

ensure_repo() {
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
}

component_source_dir() {
  case "$1" in
    starter) echo "$REPO_DIR/components/scale-radio-starter" ;;
    tuner) echo "$REPO_DIR/components/scale-radio-tuner" ;;
    autoswitch) echo "$REPO_DIR/components/scale-radio-autoswitch" ;;
    bridge) echo "$REPO_DIR/components/scale-radio-bridge" ;;
    fun-line) echo "$REPO_DIR/components/scale-radio-fun-line" ;;
    *) return 1 ;;
  esac
}

run_component_install() {
  local component="$1"
  local src
  src="$(component_source_dir "$component")"
  local dst="$INSTALL_ROOT/$component"

  if [[ ! -d "$src" ]]; then
    echo "Component source missing: $src"
    exit 2
  fi

  mkdir -p "$dst"
  rm -rf "$dst"/*
  cp -a "$src"/. "$dst"/

  if [[ -x "$src/install.sh" ]]; then
    echo "Running install hook for $component"
    "$src/install.sh"
  else
    echo "No install hook for $component; files synchronized only"
  fi

  echo "$CANONICAL_REF" > "$STATE_DIR/${component}.last_ref"
  date -u +%FT%TZ > "$STATE_DIR/${component}.last_deploy_at"
}

run_bundle() {
  run_component_install starter
  run_component_install tuner
  run_component_install fun-line
  run_component_install autoswitch
  run_component_install bridge
}

ensure_repo

case "$SCOPE" in
  bundle)
    run_bundle
    ;;
  starter|tuner|autoswitch|bridge|fun-line)
    run_component_install "$SCOPE"
    ;;
  *)
    echo "Unsupported scope: $SCOPE"
    exit 1
    ;;
esac

echo "$CANONICAL_REF" > "$STATE_DIR/last_successful_ref"
echo "$SCOPE" > "$STATE_DIR/last_scope"
date -u +%FT%TZ > "$STATE_DIR/last_deploy_request.txt"

echo "Deploy completed successfully"
