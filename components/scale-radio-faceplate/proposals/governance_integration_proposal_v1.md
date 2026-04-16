# GOVERNANCE INTEGRATION PROPOSAL — scale-radio-faceplate v1

## Intent
This package is a **suggestion-only intake** for PR #85.
No protected-main truth for cross-component governance should be promoted from this package until owner approval is explicit.

## Review outcome for PR #85 (current branch proposal)
- Keep: `components/scale-radio-faceplate/**` and `journals/scale-radio-faceplate/**` as proposal truth.
- Reject for now: broad replacement of existing governance artifacts (workflow removals, status/report removals, v7->v8 pointer jumps, and unrelated journal generation shifts).
- Reason: those broad changes are outside faceplate bootstrap scope and would risk governance drift.

## Proposed acceptance scope (Phase A: suggestion intake)
1. Introduce faceplate contract component docs only:
   - `components/scale-radio-faceplate/README.md`
   - `components/scale-radio-faceplate/contracts/faceplate_contract_package_v1_2.md`
   - `components/scale-radio-faceplate/proposals/*`
   - `components/scale-radio-faceplate/reference/HANDOVER_scale-radio-faceplate_stage-b_v1.md`
2. Introduce faceplate journals:
   - `journals/scale-radio-faceplate/current_state_v1.md`
   - `journals/scale-radio-faceplate/stream_v1.md`
3. Record SI review gate and owner decision requirement in SI status/stream.

## Proposed post-approval integration scope (Phase B: governed integration)
Only after owner approval of Phase A:
1. Add explicit consumer references in relevant component current-state files (Bridge/Tuner/Fun Line/Starter) to faceplate contract ownership.
2. Add/adjust governance contracts **only if required by actual integration gaps**, in a dedicated `si/faceplate-governance-integration-*` PR package.
3. Keep deploy/runtime contracts unchanged unless a runtime owner requests implementation work from this contract.

## Owner decision options
- **Option A (recommended):** approve Phase A only (proposal + component/journal bootstrap), defer broader governance mutation.
- Option B: reject faceplate bootstrap package and keep faceplate outside repo truth.
- Option C: request split into finer PR packages before any approval.

## Merge/rollback model
- Merge path: dedicated `si/<topic>` PR to `main` after owner approval.
- Rollback path: `si/revert-faceplate-intake-v1` via `git revert` PR if acceptance proves incorrect.
