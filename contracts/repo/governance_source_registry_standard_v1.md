# GOVERNANCE SOURCE REGISTRY STANDARD V1

## Purpose
Define one machine-readable registry for governance source-of-truth domains and enforce duplicate-authority detection.

## Canonical registry
- `tools/governance/governance_source_registry_v1.json`

## Registry fields
Each domain entry must include:
- `id`
- `authority_file`
- `duplicate_forbidden_patterns`

## Lint contract
- Lint script: `tools/governance/governance_source_registry_lint_v1.py`
- Workflow: `.github/workflows/governance-source-registry-lint-v1.yml`
- Lint fails when:
  - authority file is missing
  - authority pattern is missing in declared authority file
  - the same authority pattern appears in other governed docs

## Rollback
- disable lint workflow by reverting `.github/workflows/governance-source-registry-lint-v1.yml`
- restore previous behavior by reverting registry + lint script commit

## Safety
The registry lint is a governance guardrail.
If it blocks unexpectedly:
- document the blocker in SI stream
- switch to temporary warn-only mode by disabling workflow until authority mapping is corrected
- do not bypass by duplicating canonical rules across random files
