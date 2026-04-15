# AGENT GIT BOOTSTRAP V1

## Purpose
Define one deterministic startup path so every development/governance agent can self-prepare branch + remote execution and report blockers immediately.

## Canonical remote rule
- canonical remote name: `git`
- canonical URL: `https://github.com/SH99999/mediastreamer.git`
- equivalent canonical SSH form is accepted and preserved: `git@github.com:SH99999/mediastreamer.git`

## Bootstrap script
Run:

```bash
bash tools/governance/agent_git_bootstrap_v1.sh
```

Optional environment overrides:
- `CANONICAL_REMOTE_NAME` (default: `git`)
- `CANONICAL_REMOTE_URL` (default: `https://github.com/SH99999/mediastreamer.git`)
- `CANONICAL_BASE_BRANCH` (default: `main`)
- `AUTO_SYNC_MAIN` (default: `true`) to auto-fetch/rebase `si/*`, `dev/*`, and `integration/*` branches onto latest `git/main`

## Required first reply contract (agent -> owner)
Immediately after bootstrap, the agent must report:
1. current branch
2. canonical remote status
3. base sync status
4. push-auth status
5. what the agent can do immediately without owner input
6. what owner action is required (if any)

Use this concise format:

```text
Bootstrap status:
- branch: <branch>
- remote(git): <ok|missing|wrong-url>
- base sync: <ok|skipped|blocked>
- push auth: <ok|blocked>
- ready now: <what will be done next>
- owner action needed: <none|exact short action>
```

## Owner action rule
If push auth is blocked, the agent must ask for exactly one concrete action first (for example: provide runtime token/auth, or run push locally), not a long checklist.

## Safety rule
Bootstrap does not bypass protected-`main` rules:
- all work stays on non-`main` branches
- promotion still happens via PR to `main`
- owner remains final merge gate
