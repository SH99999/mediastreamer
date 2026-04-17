# STATUS PROMPT REPORTS V1

## Purpose
Enable short prompt-based status responses with pre-generated, clickable, and visualized markdown reports.

## Generator
Run:

```bash
python3 tools/governance/generate_status_reports_v1.py --repo-root . --out-dir reports/status
```

Deterministic timestamp mode (optional, useful for reproducible regeneration during review):

```bash
python3 tools/governance/generate_status_reports_v1.py --repo-root . --out-dir reports/status --generated-at 2026-04-16T00:00:00+00:00
```

Generated files:
- `reports/status/index.md`
- `reports/status/tuner.md`
- `reports/status/governance.md`
- `reports/status/ui.md`
- `reports/status/bridge.md`
- `reports/status/decisions.md`
- `reports/status/blocker.md`
- `reports/status/packets/*.json`

## Prompt aliases
- `status tuner`
- `status governance`
- `status ui`
- `status bridge`
- `status decisions`
- `status blocker`

## Output contract
Each report must provide:
- short bullet summary
- clickable links to source objects in repository
- visual block (Mermaid chart)
- concise next-action context where available

## Source-of-truth rule
Reports are generated from repo truth files so prompts can be handled without hidden external state.


## status_packet_v1 contract
- canonical schema: `tools/governance/schemas/status_packet_v1.schema.json`
- governance contract: `contracts/repo/status_packet_reporting_contract_v1.md`
- generated markdown reports must include owner action contract fields (`recommended_owner_action`, `next_owner_click`, `source_commit`)
- generated markdown reports must include decision scoring and rollback one-click fields (`decision_scoring.*`, `rollback_action.command`)
- generated markdown reports must include explicit claim classes (`claim_classes.governance_docs`, `claim_classes.runtime_validation`, `claim_classes.autonomy_eligibility`)
- generated markdown reports must include normalized component claim fields (`component_claims.deploy_ready`, `component_claims.tested_on_target`, `component_claims.rollback_verified`, `component_claims.runtime_validated`, `component_claims.autonomy_eligible`)
- runtime/autonomy claims must only render as validated/eligible when evidence fields are present (`runtime_claim.*`, `autonomy_claim.*`)
- generated JSON packets under `reports/status/packets/` are the cross-agent handoff payload


## Enforcement checks
- next-owner-click enforcement script: `tools/governance/status_next_owner_click_enforcement_v1.py`
- source-registry lint script: `tools/governance/governance_source_registry_lint_v1.py`
- both should pass in CI for report/governance mutations


## Integration proof check
Run:

```bash
python3 tools/governance/run_integration_check_one_click_v1.py
```

Output:
- `reports/governance/integration_check_one_click_v1.md`


## Onboarding + journal revision audit
Run:

```bash
python3 tools/governance/onboarding_journal_revision_audit_v1.py
```

Output:
- `reports/governance/onboarding_journal_revision_audit_v1.md`
