# <topic> owner decision packet v1

status: ready-for-owner
actor: codex

## decision summary
- recommendation: accept | changes-requested | reject
- confidence_band: high | medium | low
- agreement_score_chatgpt: <0..100>
- agreement_score_codex: <0..100>
- agreement_gap: <absolute difference>

## key findings considered
- finding 1: <explicit evidence from audit/report>
- finding 2: <explicit evidence from audit/report>

## implementation proposal (ranked)
1. <specific change + file path>
2. <specific change + file path>
3. <specific change + file path>

## risks (essential)
- <risk 1>
- <risk 2>

## execution path
- branch: si/<topic>
- follow-up branches (optional): dev/<component>
- compare link: https://github.com/SH99999/mediastreamer/compare/main...si/<topic>

## rollback
- strategy: revert decision package commit
- command: git revert <commit>

## where to click now
- decision issues queue: https://github.com/SH99999/mediastreamer/issues?q=is%3Aopen+is%3Aissue+label%3Astate%3Aneeds-decision
- decision PR queue: https://github.com/SH99999/mediastreamer/pulls?q=is%3Aopen+is%3Apr+label%3Astate%3Aneeds-decision
- topic branch compare: https://github.com/SH99999/mediastreamer/compare/main...si/<topic>

## owner next click
- accept | changes-requested | reject
