#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
TARGET="${2:-primary}"
COMPONENT="${3:-}"
GIT_REF="${4:-}"
PAYLOAD="${5:-}"
OWNER="${6:-}"
ARG7="${7:-}"
ARG8="${8:-}"

STATE_DIR="${PI_TEST_SLOT_STATE_DIR:-/opt/scale-radio/state}"
STATE_FILE="$STATE_DIR/pi_test_slot_${TARGET}.json"
LOCK_DIR="$STATE_FILE.lockdir"
mkdir -p "$STATE_DIR"

python3 - "$ACTION" "$TARGET" "$COMPONENT" "$GIT_REF" "$PAYLOAD" "$OWNER" "$ARG7" "$ARG8" "$STATE_FILE" "$LOCK_DIR" <<'PY'
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ACTION, TARGET, COMPONENT, GIT_REF, PAYLOAD, OWNER, ARG7, ARG8, STATE_FILE, LOCK_DIR = sys.argv[1:11]
state_path = Path(STATE_FILE)
lock_path = Path(LOCK_DIR)
now = int(time.time())


def iso(ts: int) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load_state():
    if not state_path.exists():
        return None
    return json.loads(state_path.read_text(encoding='utf-8'))


def save_state(state):
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def release_lockdir():
    if lock_path.exists():
        shutil.rmtree(lock_path)


def exit_with(code: int, message: str):
    print(message)
    raise SystemExit(code)


try:
    lock_path.mkdir()
except FileExistsError:
    exit_with(91, f'target-slot-lock-busy target={TARGET}')

try:
    state = load_state()
    state_name = (state or {}).get('state', 'free')
    lease_expires_at = (state or {}).get('lease_expires_at_epoch')
    expired = bool(lease_expires_at and lease_expires_at < now)

    if ACTION == 'status':
        if not state:
            print(json.dumps({'target': TARGET, 'state': 'free'}, indent=2))
            raise SystemExit(0)
        print(json.dumps(state, indent=2, sort_keys=True))
        raise SystemExit(0)

    if ACTION == 'acquire-deploy':
        hold_minutes = int(ARG7 or '240')
        if state and state_name in ('deploying', 'test_open', 'rollback_running', 'blocked') and not expired:
            exit_with(10, f'target-not-free target={TARGET} state={state_name}')
        lease_until = now + hold_minutes * 60
        save_state({
            'target': TARGET,
            'state': 'deploying',
            'component': COMPONENT,
            'git_ref': GIT_REF,
            'payload': PAYLOAD,
            'owner': OWNER,
            'acquired_at_epoch': now,
            'acquired_at': iso(now),
            'lease_expires_at_epoch': lease_until,
            'lease_expires_at': iso(lease_until),
        })
        print(f'acquired-deploy-slot target={TARGET} component={COMPONENT} git_ref={GIT_REF} payload={PAYLOAD}')
        raise SystemExit(0)

    if ACTION == 'mark-test-open':
        hold_minutes = int(ARG7 or '240')
        lease_until = now + hold_minutes * 60
        if not state:
            exit_with(12, f'no-active-slot target={TARGET}')
        save_state({
            'target': TARGET,
            'state': 'test_open',
            'component': COMPONENT,
            'git_ref': GIT_REF,
            'payload': PAYLOAD,
            'owner': OWNER,
            'acquired_at_epoch': state.get('acquired_at_epoch', now),
            'acquired_at': state.get('acquired_at', iso(now)),
            'test_opened_at_epoch': now,
            'test_opened_at': iso(now),
            'lease_expires_at_epoch': lease_until,
            'lease_expires_at': iso(lease_until),
        })
        print(f'marked-test-open target={TARGET} component={COMPONENT} git_ref={GIT_REF} payload={PAYLOAD}')
        raise SystemExit(0)

    if ACTION == 'acquire-rollback':
        if not state:
            exit_with(13, f'no-slot-to-rollback target={TARGET}')
        if state_name not in ('test_open', 'blocked') and not expired:
            exit_with(14, f'rollback-not-allowed target={TARGET} state={state_name}')
        if state.get('component') and state.get('component') != COMPONENT:
            exit_with(15, f'rollback-component-mismatch target={TARGET} state_component={state.get("component")} requested_component={COMPONENT}')
        lease_until = now + 60 * 60
        save_state({
            'target': TARGET,
            'state': 'rollback_running',
            'component': COMPONENT,
            'git_ref': GIT_REF,
            'payload': PAYLOAD,
            'owner': OWNER,
            'acquired_at_epoch': state.get('acquired_at_epoch', now),
            'acquired_at': state.get('acquired_at', iso(now)),
            'rollback_started_at_epoch': now,
            'rollback_started_at': iso(now),
            'lease_expires_at_epoch': lease_until,
            'lease_expires_at': iso(lease_until),
        })
        print(f'acquired-rollback-slot target={TARGET} component={COMPONENT} git_ref={GIT_REF} payload={PAYLOAD}')
        raise SystemExit(0)

    if ACTION == 'mark-blocked':
        reason = ARG7 or 'unspecified'
        save_state({
            'target': TARGET,
            'state': 'blocked',
            'component': COMPONENT,
            'git_ref': GIT_REF,
            'payload': PAYLOAD,
            'owner': OWNER,
            'blocked_at_epoch': now,
            'blocked_at': iso(now),
            'reason': reason,
        })
        print(f'marked-blocked target={TARGET} reason={reason}')
        raise SystemExit(0)

    if ACTION == 'release':
        reason = ARG7 or 'released'
        force = (ARG8 or '').lower() in ('1', 'true', 'yes', 'force')
        if not state:
            print(f'already-free target={TARGET}')
            raise SystemExit(0)
        if not force:
            if state.get('component') and COMPONENT and state.get('component') != COMPONENT:
                exit_with(16, f'release-component-mismatch target={TARGET} state_component={state.get("component")} requested_component={COMPONENT}')
            if state.get('git_ref') and GIT_REF and state.get('git_ref') != GIT_REF:
                exit_with(17, f'release-git-ref-mismatch target={TARGET} state_git_ref={state.get("git_ref")} requested_git_ref={GIT_REF}')
        state_path.unlink(missing_ok=True)
        print(f'released-slot target={TARGET} reason={reason}')
        raise SystemExit(0)

    exit_with(2, f'unsupported-action action={ACTION}')
finally:
    release_lockdir()
PY
