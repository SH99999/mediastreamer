# Audit Basis v1 (active)

status: ready-for-codex
actor: chatgpt

## Scope
- component/governance scope: governance consistency, agent onboarding, one-click ownership, deploy/test/rollback doctrine, versioned truth handling, roles, rules of engagement, and visible security concerns
- audit surface used: current repo truth on `main`, current exchange lane on `si/chatgpt-git-exchange-v1`, recent merged governance PRs, workflows, reports, and issue queue state reachable through the GitHub connector
- objective: give Codex a ranked, branchable execution package with explicit risks, mitigation proposals, and owner-decision framing

## Findings (essential, ranked)
1. Governance model is structurally strong and increasingly CI-backed, but operational consistency still lags behind doctrine. The strongest evidence is the active branch-scope guard, source-registry lint, next-owner-click enforcement, and one-click integration proof.
2. Agent onboarding is functional but still too heavy for safe fast-start. The current read-order and onboarding package is large enough to create skip-risk, even after mode-B safe-start improvements.
3. One-click ownership is technically validated for decision packets and status rendering, but the lifecycle is not yet fully closed end-to-end. Queue hygiene and closeout automation still leave room for stale decision/escalation state after merge.
4. Autonomous deploy/test/rollback doctrine is coherent and conservative, but real support is still limited to the current normalized subset. The system should not be described as broadly autonomous beyond the support matrix and evidence-backed lanes.
5. Versioned repo truth preserves history well, but active-vs-historical separation is still incomplete. Older stream generations remain readable without a fully normalized historical marker discipline.
6. Highest-priority concrete defect: onboarding/startup documentation still references `tools/governance/setup_auth_check_v1.sh`, but the referenced script is not present on `main`.

## Ranked issue list
1. missing auth-diagnostic script behind active onboarding/startup docs
2. stale queue/closeout risk for governance escalation items after merge
3. onboarding read-chain and execution-path overload
4. incomplete active-vs-historical document separation for older stream generations
5. one-click semantics still coupled too loosely to evidence-backed delivery acceptance and queue closeout
6. autonomous-delivery interpretation risk if support-matrix boundaries are not kept explicit

## Proposed next step for Codex
- keep exchange work on `si/chatgpt-git-exchange-v1`
- implementation lane suggestions:
  - `si/auth-diagnostics-contract-fix`
  - `si/governance-queue-closeout-automation`
  - `si/history-marker-and-superseded-cleanup`
  - `si/onboarding-tiered-execution-profile`
  - `si/one-click-delivery-evidence-gate`
- expected Codex output:
  - validate findings against current `main`
  - convert ranked items into executable branch packages / PR sequence
  - prepare owner-ready decision packet with rollback and risk framing

## Handover
- Codex should treat this basis as the current ChatGPT audit position for the exchange loop
- keep status as `ready-for-codex` until Codex publishes the next governed response artifact
