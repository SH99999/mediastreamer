# Chat-to-Git delivery process v1

## Purpose
This runbook gives all chats/agents one exact process for governed delivery from chat request to Git branch + PR.

## Mandatory preflight
1. Run `bash tools/governance/agent_git_bootstrap_v1.sh`.
2. Confirm branch is `si/<topic>` for SI/governance tasks.
3. Confirm canonical remote is `git -> https://github.com/SH99999/mediastreamer.git`.
4. Confirm push auth is available.

If preflight fails, do not fake delivery.

## Execution steps (must be followed in order)
1. Intake
   - Use the `governed_intake_v1` contract from `docs/agents/chatgpt_governed_intake_prompt_v1.md`.
   - Create or update the governed intake issue fields and decision packet.
2. Branching
   - Create or switch to a dedicated branch:
     - SI/governance: `si/<topic>`
     - Component lane: `dev/<component>`
3. Repo mutation
   - Apply scoped file changes.
   - Update required journals/status/decisions when state changes.
4. Validation
   - Run syntax and format checks relevant to changed files.
5. Git packaging
   - `git add ...`
   - `git commit -m "<focused message>"`
6. Delivery to Git
   - `git push -u git <branch>`
7. PR creation
   - Open PR `<branch> -> main`.
   - Include decision output and owner approval gate statement.

## Required owner-facing delivery message
Every agent must finish with exactly one of these status blocks.

### Delivered (YES)
```text
Delivered to Git: YES
Branch: <branch>
Commit: <sha>
PR: <url>
Owner action: review/approve PR to main.
```

### Not delivered (NO)
```text
Delivered to Git: NO
Branch: <branch or n/a>
Blocker: <single concrete blocker>
What was completed locally: <short factual list>
Owner action: <single concrete action needed, e.g. provide runtime push auth or run push command locally>
```

## Non-negotiable behavior
- Never report delivery as complete when push/PR did not happen.
- If GitHub write connector/token is unavailable, use the NO block and stop claiming repo truth mutation.
- Keep repository-facing content in English.
