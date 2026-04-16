# repo-governance-audit owner decision packet v1

status: ready-for-owner
actor: codex

## decision summary
- recommendation: changes-requested
- confidence_band: medium
- agreement_score_chatgpt: 89.0
- agreement_score_codex: 68.0
- agreement_gap: 21.0

## key findings considered
- audit basis is incomplete; owner should require evidence update before acceptance
- follow-up audit pull is required for unresolved components

## implementation proposal (ranked)
1. **P1 — fix onboarding/auth contract breakage first**
- create or remove the missing `tools/governance/setup_auth_check_v1.sh` reference path
- add a CI/docs-reference existence check so onboarding docs cannot point to missing executable assets again
- update `container_startup_setup_v1.md`, owner/agent setup references, and any startup prompts in one change set
2. **P2 — close the governance queue lifecycle gap**
- add deterministic closeout/retire logic for SI escalation issues once the source PR is merged or explicitly superseded

## risks (essential)
- scope drift
- incomplete component normalization

## execution path
- branch: si/repo-governance-audit
- follow-up branches (optional): dev/<component>
- compare link: https://github.com/SH99999/mediastreamer/compare/main...si/repo-governance-audit

## rollback
- strategy: revert decision package commit
- command: git revert <commit>

## where to click now
- decision issues queue: https://github.com/SH99999/mediastreamer/issues?q=is%3Aopen+is%3Aissue+label%3Astate%3Aneeds-decision
- decision PR queue: https://github.com/SH99999/mediastreamer/pulls?q=is%3Aopen+is%3Apr+label%3Astate%3Aneeds-decision
- topic branch compare: https://github.com/SH99999/mediastreamer/compare/main...si/repo-governance-audit

## owner next click
- changes-requested
