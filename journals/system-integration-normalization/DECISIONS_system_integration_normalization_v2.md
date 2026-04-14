# DECISION LOG — system_integration_normalization

Status note: this v2 file supersedes the earlier v1 snapshot as the current repo-facing SI/N decision log.

## Decision Entries

### DEC-system_integration_normalization-01
- Status: locked
- Decision: `main` is the canonical truth branch for workflows, governance, contracts, and accepted stable artifacts.
- Date context: repository normalization phase
- Why this was chosen: one operator-visible control plane is required to avoid branch and workflow ambiguity.
- What it affects: workflow placement, governance docs, accepted stable payload promotion.
- What it explicitly does NOT affect: whether unstable component work may continue on `dev/*` branches.
- Follow-up needed: keep branch doctrine wording consistent across docs.

### DEC-system_integration_normalization-02
- Status: locked
- Decision: active component work belongs on `dev/<component>` unless the component block is already stable enough for `main` truth or governance explicitly promotes it.
- Date context: branch cleanup and normalization phase
- Why this was chosen: separates unstable work from stable operator-facing repo truth.
- What it affects: branch selection for active component lanes.
- What it explicitly does NOT affect: intentional promotion of a stable component block to `main`.
- Follow-up needed: keep active `dev/*` branches aligned to current `main` whenever practical.

### DEC-system_integration_normalization-03
- Status: locked
- Decision: deployment uses clean-replace semantics, not update-in-place semantics.
- Date context: early Bridge deployment governance
- Why this was chosen: current plugin/runtime stability is not high enough for safe in-place updates.
- What it affects: deploy candidate scripts, rollback logic, payload install behavior.
- What it explicitly does NOT affect: future possibility of update-in-place once stability is proven.
- Follow-up needed: encode this in all new component deploy candidate scripts.

### DEC-system_integration_normalization-04
- Status: locked
- Decision: workflows must live on `main` and accept a selected `git_ref`.
- Date context: manual workflow visibility normalization
- Why this was chosen: GitHub manual workflows are operator-friendly when visible on the default truth branch.
- What it affects: manual deploy and rollback workflows.
- What it explicitly does NOT affect: where evolving component payloads live.
- Follow-up needed: keep only the current supported workflow generation visible.

### DEC-system_integration_normalization-05
- Status: locked
- Decision: the repo-shipped wrapper is the accepted deployment entrypoint model.
- Date context: stale Pi-local wrapper mismatch investigation
- Why this was chosen: multi-host consistency requires the repo to ship the execution model.
- What it affects: wrapper logic and workflow execution path.
- What it explicitly does NOT affect: existence of older Pi-local wrappers; those simply should not be trusted.
- Follow-up needed: extend wrapper-backed maturity beyond Bridge.

### DEC-system_integration_normalization-06
- Status: locked
- Decision: rollback must also unregister the plugin in Volumio when relevant.
- Date context: Bridge rollback hardening
- Why this was chosen: removing files without unregistering plugin state leaves operational residue.
- What it affects: Bridge rollback logic and future plugin rollback paths.
- What it explicitly does NOT affect: non-plugin components that have no Volumio plugin registration.
- Follow-up needed: apply the same rule to future plugin-based components.

### DEC-system_integration_normalization-07
- Status: locked
- Decision: Bridge may remain inactive after install for now if runtime deployment, overlay reachability, and rollback are working.
- Date context: validated Bridge deploy tests
- Why this was chosen: runtime path and overlay behavior proved operational even though activation state is not yet ideal.
- What it affects: current Bridge acceptance threshold.
- What it explicitly does NOT affect: future expectation of better activation behavior.
- Follow-up needed: keep documenting this as an accepted temporary state until improved.

### DEC-system_integration_normalization-08
- Status: locked
- Decision: governance doctrine belongs in `contracts/repo/`; agent-facing onboarding and recovery material belongs in `docs/agents/` and must point back to governance and journals.
- Date context: governance recovery and handoff hardening
- Why this was chosen: one governance home is required, but replacement chats also need an explicit recovery entrypoint.
- What it affects: placement of repo-control-plane doctrine and onboarding material.
- What it explicitly does NOT affect: component-specific journals under `journals/<component>/`.
- Follow-up needed: avoid creating parallel governance directories.

### DEC-system_integration_normalization-09
- Status: locked
- Decision: system integration must maintain repo-native status, decisions, and stream files.
- Date context: governance recovery and handoff hardening
- Why this was chosen: SI/N owns the repo-control-plane and cannot depend on chat-only memory.
- What it affects: required documentation discipline for SI/N itself.
- What it explicitly does NOT affect: the existing requirement for active components to maintain their own journals.
- Follow-up needed: keep SI stream updated after each meaningful repo-control-plane change.

### DEC-system_integration_normalization-10
- Status: locked
- Decision: repo-control-plane changes should be prepared in dedicated branches and reviewed through pull requests to `main`.
- Date context: current git operating discipline
- Why this was chosen: reviewable PRs keep governance and integration changes explicit and auditable.
- What it affects: governance changes, workflow changes, journal additions, and repo-control-plane modifications.
- What it explicitly does NOT affect: the owner's right to decide approval timing or merge order.
- Follow-up needed: keep SI/governance changes scoped and reviewable.

## Superseded Decisions
- No individual locked decision is superseded in this v2 file.
- The earlier v1 decision-log file remains a historical snapshot, while this v2 file becomes the current operating decision log.
