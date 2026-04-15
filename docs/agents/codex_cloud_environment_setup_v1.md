# CODEX CLOUD ENVIRONMENT SETUP V1

## Purpose
Provide a single copy/paste setup checklist for owners configuring Codex cloud environments for this repository.

## 1) Base environment values
Set these environment variables in the Codex cloud environment:

```text
GH_TOKEN=<PAT-or-app-token>
GITHUB_TOKEN=<same-as-GH_TOKEN>
CANONICAL_REMOTE_NAME=git
CANONICAL_REMOTE_URL=https://github.com/SH99999/mediastreamer.git
RUN_NPM_INSTALL=false
ALLOW_CLONE_IF_MISSING=false
RUN_GOVERNANCE_DIAGNOSTICS=false
NPM_TIMEOUT_SECONDS=180
```

## 2) Startup script mode
Recommended: keep Codex cloud on **Auto setup script**.

If custom startup is required, use only:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd /workspace/mediastreamer || exit 0
bash tools/governance/container_startup_setup_v1.sh
```

Do not add global `npm install` loops in startup.
Do not run bootstrap/auth checks in startup unless debugging (`RUN_GOVERNANCE_DIAGNOSTICS=true`).

## 3) Remote compatibility rule
Agents use remote `git` as canonical. Keep `origin` aligned as compatibility alias.
This is handled automatically by `tools/governance/container_startup_setup_v1.sh`.

## 4) Session verification
After environment starts, run:

```bash
bash tools/governance/agent_git_bootstrap_v1.sh
bash tools/governance/setup_auth_check_v1.sh
```

Pass criteria:
- `remote(git): ok`
- `push auth: ok`
- `Auth check: result=ok`

Note: `agent_git_bootstrap_v1.sh` now attempts a local credential-helper configuration from `GH_TOKEN`/`GITHUB_TOKEN` when plain HTTPS push auth fails, then rechecks push auth.

## 5) If push is still blocked
- verify `GH_TOKEN` and `GITHUB_TOKEN` are visible in runtime session env
- verify token has repo write + pull request write permissions
- keep branch discipline: `dev/<component>` or `si/<topic>` and PR to `main`

## 6) Why a doc link can show 404
- If a file exists only on an unmerged branch, opening the `main` URL will show 404.
- Use the branch selector in GitHub UI or open the file from the PR "Files changed" tab.
