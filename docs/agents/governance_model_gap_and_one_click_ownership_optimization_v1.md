# GOVERNANCE MODEL GAP AND ONE-CLICK OWNERSHIP OPTIMIZATION V1

## Purpose
Provide a focused assessment of current governance-model risks and two actionable improvement sets:
1) governance model hardening
2) one-click ownership and ChatGPT multi-agent status reporting optimization

## Scope used for this assessment
- `contracts/repo/*` governance standards currently referenced by SI governance index
- SI decision and stream journals currently used as truth
- owner decision click automation and status-report automation paths already present in repo

---

## Set A — Current governance model problems and improvements

### A1. Governance duplication creates drift risk
**Current problem**
- Several standards repeat near-identical rules (branch doctrine, status vocabulary, journal requirements) with overlapping but not fully synchronized wording.
- Duplicate sections inside the same file appear in at least one contract generation, increasing ambiguity about which block is authoritative.

**Risk**
- Agents can follow different valid-looking paragraphs and still diverge.
- Review overhead increases because every update needs manual sync across multiple contracts.

**Improvement proposal**
- Introduce a **single-source governance registry** (`contracts/repo/governance_source_registry_v1.md`) that defines canonical owners and source-of-truth sections for each rule class.
- In downstream contracts, replace duplicated rule blocks with references to canonical clauses.
- Add a CI doc lint check that flags duplicated headings and duplicate status vocab blocks across core governance contracts.

### A2. Status taxonomy inconsistency across standards and reports
**Current problem**
- Multiple status term sets are present (`deployment_candidate_started` vs `deploy_candidate_started`; `functional_acceptance_open` vs `functional_acceptance_pending`; plus separate status-level list).

**Risk**
- Automated status extraction can misclassify lifecycle phase.
- Owner-facing dashboards may show conflicting states for the same component.

**Improvement proposal**
- Publish `contracts/repo/status_taxonomy_contract_v1.md` as the canonical status enum.
- Require status generators and journals to validate only against this enum.
- Add a migration map (`old_status -> canonical_status`) and run one normalization sweep over journals/reports.

### A3. Governance index scale is high and slows safe execution
**Current problem**
- SI governance index read chain is very long for standard operational tasks.

**Risk**
- Agents may skip sections under time pressure.
- Onboarding latency increases, especially for replacement agents.

**Improvement proposal**
- Split read paths into three tiers:
  - **Tier 0 (must-read now)**: branch doctrine, truthful execution, deploy process, escalation, bootstrap.
  - **Tier 1 (task-conditional)**: UI/UX, release tagging, test strategy.
  - **Tier 2 (reference)**: historical and design-depth docs.
- Keep full index, but add a minimal execution profile for first-pass correctness.

### A4. Truth update obligations are clear, but enforcement is mostly procedural
**Current problem**
- Rules require journal updates and decision logs, but enforcement mostly relies on agent discipline.

**Risk**
- PRs can ship governance mutations without synchronized journal updates.

**Improvement proposal**
- Add a PR governance gate workflow that verifies:
  - SI/governance PRs include at least one SI stream entry.
  - If contract files changed, decision/status files are checked for corresponding update markers.
- Fail fast with explicit remediation instructions.

### A5. Branch policy is strong, but bootstrap defaults still allow unsafe starts
**Current problem**
- Branch `work` is explicitly disallowed for SI truth mutations, yet sessions can still start there.

**Risk**
- Early edits may happen before branch correction.

**Improvement proposal**
- Require bootstrap script invocation with requested branch arg for SI tasks (`si/<topic>`).
- Add a pre-commit hook (or CI check) that blocks SI/governance file changes when branch does not match `si/*`.

---

## Set B — One-click ownership and ChatGPT multi-agent status reporting optimization

### B1. One-click decision exists, but lacks decision-quality scoring
**Current problem**
- Structured owner decisions are captured, but decision confidence and evidence sufficiency are not scored in a standard way.

**Optimization proposal**
- Extend decision payload with mandatory compact scoring fields:
  - `evidence_quality` (0-3)
  - `rollback_readiness` (0-3)
  - `blast_radius` (low/medium/high)
  - `confidence` (0-100)
- Auto-render these in project view to prioritize low-friction safe approvals.

### B2. Multi-agent status outputs need a stable cross-agent schema
**Current problem**
- Prompt-ready reports exist, but cross-agent handoff schema is implicit.

**Optimization proposal**
- Define `status_packet_v1` JSON schema in `tools/governance/schemas/` for all agent outputs:
  - component
  - canonical status
  - evidence links
  - blockers
  - recommended owner action
  - timestamp and source commit
- Require all reporting agents to emit this schema, then transform to markdown views.

### B3. Missing deterministic “owner next click” routing
**Current problem**
- Reports summarize status, but the next owner click is not always encoded as a strict action contract.

**Optimization proposal**
- Add `next_owner_click` field with enumerated values:
  - `approve_pr`
  - `request_changes`
  - `run_workflow`
  - `defer`
- Include URL and fallback text command for each click target.

### B4. Need stronger chat intake routing for specialized agents
**Current problem**
- Intake prompts exist, but routing to the right specialist agent can still depend on manual interpretation.

**Optimization proposal**
- Add router rules:
  - `governance-mutation` -> SI governance agent
  - `runtime-regression` -> component specialist
  - `owner-decision-needed` -> owner decision packet agent
- Persist routing decision in issue/PR metadata to keep auditability.

### B5. Status reporting cadence should be event-driven + scheduled
**Current problem**
- Report generation can be run, but cadence and trigger hierarchy are not fully standardized.

**Optimization proposal**
- Trigger status generation on:
  1) merge to `main`
  2) labeled owner decision events
  3) deploy/rollback workflow completion
  4) daily schedule
- Publish one compact “delta since last report” block for owner speed.

### B6. “One-click ownership” should include safe rollback button semantics
**Current problem**
- Rollback is documented, but not always represented as first-class owner one-click action with explicit guardrails.

**Optimization proposal**
- Add rollback action contract:
  - `rollback_target`
  - `required_prechecks`
  - `expected_recovery_state`
  - `post_rollback_verification_url`
- Show this in owner operational page and decision packet side-by-side with approve action.

---

## Suggested implementation order (low risk -> higher impact)
1. Canonical status taxonomy + migration map
2. status_packet_v1 schema for all agent status outputs
3. next_owner_click contract and report rendering
4. governance source registry and duplication lint checks
5. branch enforcement automation for SI files
6. decision-quality scoring and rollback one-click contract extensions

## PR packaging plan and mandatory rollback contract
All proposed changes should ship in small, reversible PR packages.

### Package matrix
1. **PR-P1: status taxonomy contract + migration map**
   - scope: add canonical enum contract and journal/report mapping
   - rollback: revert PR; restore previous enum readers; regenerate reports from previous commit
   - owner decision gate: required

2. **PR-P2: `status_packet_v1` schema + report adapter**
   - scope: add JSON schema and markdown transformer compatibility layer
   - rollback: set workflow toggle `STATUS_PACKET_V1_ENABLED=false` and revert adapter commit
   - owner decision gate: required

3. **PR-P3: `next_owner_click` enforcement**
   - scope: require deterministic owner action in generated status pages
   - rollback: disable enforcement with `OWNER_NEXT_CLICK_REQUIRED=false`
   - owner decision gate: required

4. **PR-P4: governance source registry + duplication lint checks**
   - scope: introduce single-source registry and CI duplicate-rule checks
   - rollback: disable lint workflow file and revert registry references
   - owner decision gate: required

5. **PR-P5: SI branch-scope guard for governance files**
   - scope: block SI-governance file mutations outside `si/*` branches in CI
   - rollback: set guard mode to warn-only (`SI_BRANCH_GUARD_ENFORCE=false`)
   - owner decision gate: required

6. **PR-P6: owner decision scoring + rollback one-click action contract**
   - scope: add scoring fields and rollback contract fields to decision packets/views
   - rollback: feature-flag field validation (`OWNER_DECISION_SCORING_ENABLED=false`)
   - owner decision gate: required

### Rollback operating rules (applies to all packages)
- every PR must include:
  - exact rollback command block (`git revert <merge_commit>` or `git revert <commit_range>`)
  - impacted workflows/files list
  - post-rollback verification checklist and links
- no package is allowed to remove the existing manual owner decision fallback path
- if automation degrades, rollback must be possible in one revert PR without data-loss migration

## Acceptance checkpoints
- No duplicate contradictory status enums in active governance contracts.
- Every generated status report contains `next_owner_click` and source commit.
- Every SI governance PR contains SI stream evidence and passes branch-scope checks.
- Owner can decide approve/change/defer from one view in <= 3 clicks.

## Owner-facing summary
The current model is strong in doctrine but vulnerable to duplication drift, taxonomy inconsistencies, and uneven automation contracts between decision capture and cross-agent status exchange. The optimization path is to standardize schemas, reduce duplicated authority text, and encode deterministic owner click actions with evidence quality and rollback safety.
