# CANONICAL GOVERNANCE SOURCES V1

## Purpose
This document defines source precedence when multiple governance documents exist in the repository.

## Leading rule
If two repository governance documents overlap or appear inconsistent, use the higher-precedence document listed here.

## Precedence order
### 1. Canonical branch and component doctrine
- `contracts/repo/branch_strategy_v2.md`
- `contracts/repo/component_artifact_model_v1.md`
- `contracts/repo/overlay_component_contract_v1.md`

These define:
- what `main` means
- what `dev/<component>` means
- what `integration/staging` means
- how one component may contain multiple deployable artifacts/plugins
- how overlay components such as Bridge must be governed

### 2. Naming and release doctrine
- `contracts/repo/naming_and_release_numbering_standard_v1.md`
- `contracts/repo/release_intake_and_delivery_status_v2.md`

These define:
- naming rules
- release numbering rules
- payload naming rules
- lifecycle status and promotion rules

### 3. Journal and language doctrine
- `contracts/repo/component_journal_policy_v2.md`
- `contracts/repo/repository_language_standard_v2.md`

### 4. Agent-facing operational files
- `AGENTS.md`
- `components/AGENTS.md`
- `docs/agents/*`

## Interpretation rule
Older or superseded files may remain in the repository for history or transition support.
They must not override the documents listed above.

## Specific conflict resolution
- If `branch_strategy_v1.md` and `branch_strategy_v2.md` differ, `branch_strategy_v2.md` wins.
- If any older branch wording implies that `integration/staging` is a second truth branch, this document and `branch_strategy_v2.md` override it.
- If a component has multiple plugins/artifacts and an older document is ambiguous, `component_artifact_model_v1.md` wins.
- If a naming or release numbering question is open, `naming_and_release_numbering_standard_v1.md` wins unless a newer canonical replacement exists.
