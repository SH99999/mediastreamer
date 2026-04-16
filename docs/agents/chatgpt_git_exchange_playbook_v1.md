# CHATGPT GIT EXCHANGE PLAYBOOK V1

## Objective
Provide a standard path for two-lane collaboration (ChatGPT + Codex) using Git artifacts with low owner effort.

## Quick start
1. Run bootstrap on dedicated branch:
   - `bash tools/governance/agent_git_bootstrap_v1.sh --branch si/chatgpt-git-exchange-<topic> --role si --mode mode-b`
2. Ensure audit basis exists:
   - `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`
3. Place incoming ChatGPT package in:
   - `exchange/chatgpt/inbox/<topic>__request_v1.md`
4. Produce response package in:
   - `exchange/chatgpt/outbox/<topic>__response_v1.md`
5. Add concrete implementation list (ranked, actionable, branchable).

## Response package contract (essential only)
Every `outbox/*response*` file should include:
- summary of ask (max 5 bullets)
- assumptions/gaps (only blockers)
- concrete implementation proposals (ranked)
- proposed branch/workflow path
- owner decision needed (`accept|changes-requested|reject`)

## Minimal template
```text
# <topic> response v1

## ask summary
- ...

## blockers / missing inputs
- ...

## implementation proposals (ranked)
1. ...
2. ...
3. ...

## branch plan
- si/<topic>
- optional dev/<component>

## owner decision needed
- accept | changes-requested | reject
```

## Demand intake extension
If ChatGPT produced a demand:
1. save to `exchange/chatgpt/demands/<demand-id>__intake_v1.md`
2. map to governed issue intake
3. track resulting implementation PR from dedicated branch

## Operating rule
Prefer short, structured artifacts over narrative text blocks.
