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

Optional branch-target mode (recommended when you know the lane up front):

```bash
bash tools/governance/agent_git_bootstrap_v1.sh dev/bridge
```

Behavior:
- if `dev/bridge` exists on remote, it is checked out locally
- if missing, it is created from `git/main`
- invalid branch names (not `si/*`, `dev/*`, `integration/*`) are rejected
- if `GH_TOKEN`/`GITHUB_TOKEN` exists and plain push auth fails, bootstrap configures a local repo credential helper for `https://github.com` and re-probes push auth

Optional environment overrides:
- `CANONICAL_REMOTE_NAME` (default: `git`)
- `CANONICAL_REMOTE_URL` (default: `https://github.com/SH99999/mediastreamer.git`)
- `CANONICAL_BASE_BRANCH` (default: `main`)
- `AUTO_SYNC_MAIN` (default: `true`) to auto-fetch/rebase `si/*`, `dev/*`, and `integration/*` branches onto latest `git/main`

## Required first reply contract (agent -> owner)
Immediately after bootstrap, the agent must report:
1. current branch
2. canonical remote status
3. branch prep status
4. base sync status
5. push-auth status
6. what the agent can do immediately without owner input
7. what owner action is required (if any)

Use this concise format:

```text
Bootstrap status:
- branch: <branch>
- remote(git): <ok|missing|wrong-url>
- branch prep: <ok|skipped|blocked>
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
