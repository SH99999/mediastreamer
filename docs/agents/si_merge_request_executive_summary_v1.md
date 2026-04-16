# SI MERGE REQUEST EXECUTIVE SUMMARY V1

## Purpose
Provide a one-click owner review packet so the owner can decide and merge with minimal navigation.

## Terminology note
- GitHub object type remains a Pull Request.
- In owner-facing communication, agents may label the packet as **Merge Request** when presenting a merge-ready decision bundle.

## Mandatory packet fields (agent/chats/Codex)
1. `merge_request_link` (direct PR link)
2. `files_changed_link` (PR files tab or compare link)
3. `executive_summary` (max 7 bullets; impact-first)
4. `owner_decision_needed` (`accept | changes-requested | reject`)
5. `rollback_plan` (exact revert command + post-check)
6. `risk_level` (`low | medium | high`)
7. `next_owner_click` (`approve_pr | request_changes | defer`)

## Standard owner-facing output block
```text
SI Merge Request (Prepared)
- Merge request link: <url>
- Files changed: <url>
- Executive summary:
  - <bullet 1>
  - <bullet 2>
  - <bullet 3>
- Risk level: <low|medium|high>
- Rollback: <exact revert command>
- Owner decision needed: <accept|changes-requested|reject>
- Next owner click: <approve_pr|request_changes|defer>
```

## Click-minimization rule
- preferred delivery is one direct PR link plus one files-changed link
- avoid sending owner to branch lists, commit lists, or manual compare construction
- if connector cannot create/update PR, provide one explicit blocker and one owner action only


## SI comment block (mandatory in owner-facing handoff)
Agents/chats/Codex should post the packet as an SI comment on the PR (or provide the same block in chat if connector cannot comment):

```text
<!-- si-merge-request-summary-v1 -->
SI Merge Request (Prepared)
- Merge request link: <url>
- Files changed: <url>
- Executive summary:
  - <bullet 1>
  - <bullet 2>
  - <bullet 3>
- Risk level: <low|medium|high>
- Rollback: <exact revert command>
- Owner decision needed: <accept|changes-requested|reject>
- Next owner click: <approve_pr|request_changes|defer>
```

## Branch cleanup rule
- after merge, delete short-lived merged branch locally and remotely unless a retention exception is explicitly recorded
- rollback remains safe because revert is executed from `main` history; branch retention is not required for standard rollback
