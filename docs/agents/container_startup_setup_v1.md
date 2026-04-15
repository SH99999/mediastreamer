# CONTAINER STARTUP SETUP V1

## Recommended Codex cloud configuration (owner-facing)
Use **Auto setup script** in Codex cloud unless you have a proven need for custom startup logic.

If you use a custom setup script, keep it minimal and non-blocking:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd /workspace/mediastreamer || exit 0
bash tools/governance/container_startup_setup_v1.sh
```

## Environment variables to set in the environment UI
Required for push-capable agents:
- `GH_TOKEN=<your PAT or app token>`
- `GITHUB_TOKEN=<same value as GH_TOKEN>`

Governance defaults:
- `CANONICAL_REMOTE_NAME=git`
- `CANONICAL_REMOTE_URL=https://github.com/SH99999/mediastreamer.git`

Optional safety defaults:
- `RUN_NPM_INSTALL=false` (recommended)
- `ALLOW_CLONE_IF_MISSING=false` (recommended)
- `RUN_GOVERNANCE_DIAGNOSTICS=false` (recommended for cloud startup stability)
- `NPM_TIMEOUT_SECONDS=180`

## What `tools/governance/container_startup_setup_v1.sh` does
1. normalizes token env (`GH_TOKEN` / `GITHUB_TOKEN`)
2. verifies repo presence (does **not** clone by default)
3. configures both remotes to same canonical URL:
   - `git` (canonical)
   - `origin` (compatibility)
4. optional bounded npm install only when `RUN_NPM_INSTALL=true`
5. optionally runs governance diagnostics only when `RUN_GOVERNANCE_DIAGNOSTICS=true`:
   - `tools/governance/agent_git_bootstrap_v1.sh`
   - `tools/governance/setup_auth_check_v1.sh`

## Why this avoids startup hangs
- no clone unless explicitly allowed (`ALLOW_CLONE_IF_MISSING=true`)
- no npm install unless explicitly enabled (`RUN_NPM_INSTALL=true`)
- no diagnostics during startup unless explicitly enabled (`RUN_GOVERNANCE_DIAGNOSTICS=true`)
- diagnostics are non-fatal and designed for clear owner-action output

## Post-start check (run once in session shell)
```bash
bash tools/governance/agent_git_bootstrap_v1.sh
bash tools/governance/setup_auth_check_v1.sh
```

Expected: `push auth: ok` and `Auth check: result=ok`.
