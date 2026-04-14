# COMPONENT STATUS — system_integration_normalization

Status note: this v2 file supersedes the earlier v1 snapshot as the current repo-facing SI/N status file.

## 1. Scope
- component name: system_integration_normalization
- legacy names / aliases: SI/N, integration chat, normalization lane
- responsibility boundaries: branch doctrine, workflow model, deploy semantics, rollback semantics, repo governance, release-path normalization, cross-component integration policy, repo-native handoff quality
- non-goals: specialist feature implementation inside component payloads, UI/UX design ownership, hardware feature implementation, source engine implementation

## 2. Current Functional Status
- what currently works:
  - `main` holds the active governance, workflow, contract, and agent-onboarding control plane
  - repo-driven deployment works through the current generic deploy/rollback workflow family on `main`
  - bridge deploy lane is operational from `dev/bridge`
  - bridge rollback unregisters the plugin and restarts Volumio
  - active component journals now exist in repo form for Bridge, Tuner, Starter, AutoSwitch, Fun Line, and Hardware
  - active component README hygiene and journal presence are now CI-checked on `main`
  - system integration now has a repo-native governance index, onboarding note, status, decisions, and stream path
- what partially works:
  - the process-doc extension in PR `#40` is open but not yet merged
  - non-bridge deploy maturity is still uneven compared with Bridge
  - some repo-truth cleanup is still active and not all older lower-value documents have been retired yet
- what is broken:
  - there is still no equally mature deploy/rollback proof across all active components
  - governance cleanup is not finished enough to guarantee zero ambiguity in every older document
- what was tested:
  - bridge deploy and rollback through the repo-driven workflow model on a real Pi
  - wrapper-free repo-driven execution path
  - active-component journal/README CI on `main`
- what is untested:
  - full generic deploy/rollback validation for every active component branch
  - stronger CI enforcement for SI-specific recovery/onboarding discipline

## 3. Repository Mapping
- correct component path in repo: `journals/system-integration-normalization/`
- correct payload path(s): none
- correct branch: `main` for truth; dedicated temporary working branches for repo-control-plane changes
- whether component belongs on main or dev branch right now: main

## 4. Locked Decisions
### DEC-SIN-01
- decision: `main` is the truth branch for workflows, governance, contracts, and accepted stable artifacts.
- rationale: operator-visible execution and repo doctrine need one canonical source.
- impact: workflows and governance live on `main`.

### DEC-SIN-02
- decision: active component work belongs on `dev/<component>` unless the component block is intentionally promoted to `main` truth.
- rationale: separates unstable component work from the stable control plane.
- impact: active component development remains on `dev/*` lanes unless governance says otherwise.

### DEC-SIN-03
- decision: deployment uses clean-replace semantics, not update-in-place.
- rationale: current runtime maturity is still not strong enough for safe in-place mutation.
- impact: deploy candidate scripts and workflow behavior remove/replace instead of patching live state.

### DEC-SIN-04
- decision: workflows must live on `main` and accept a selected `git_ref`.
- rationale: manual operator-visible entrypoints must remain on the truth branch.
- impact: deploy and rollback workflow families stay on `main`.

### DEC-SIN-05
- decision: the repo-shipped wrapper model is the accepted deployment entrypoint model.
- rationale: stale Pi-local wrappers create drift and multi-host inconsistency.
- impact: wrapper behavior is controlled from repo truth.

### DEC-SIN-06
- decision: rollback must unregister the plugin in Volumio when relevant.
- rationale: file removal alone leaves operational residue.
- impact: plugin rollback paths must clean runtime state and registration state.

### DEC-SIN-07
- decision: Bridge may remain inactive after install for now if runtime deployment, overlay reachability, and rollback are working.
- rationale: current acceptance is based on proven runtime path and rollback reality.
- impact: Bridge acceptance threshold remains pragmatic until activation behavior improves.

### DEC-SIN-08
- decision: governance doctrine belongs in `contracts/repo/`, while agent-facing onboarding and recovery material belongs in `docs/agents/` and must point back to governance and journals.
- rationale: one governance home is needed, but agent recovery docs still need an explicit place.
- impact: reduces future scattering of process truth across random repo paths.

### DEC-SIN-09
- decision: system integration must maintain repo-native status, decisions, and stream files.
- rationale: SI/N governs the repo-control-plane and cannot depend on chat-only memory.
- impact: SI/N now follows the same journal discipline expected from active components.

## 5. Open Decisions
- whether PR `#40` should merge as-is or receive follow-up refinement before merge
- how strict the next SI-specific CI enforcement should become
- whether older lower-value governance files should be removed or simply remain indexed as lower-precedence historical material
- how quickly non-bridge deploy lanes should be normalized to the same maturity standard as Bridge

## 6. Runtime / Deployment Notes
- install assumptions:
  - self-hosted Pi runner with labels matching workflow requirements
  - repo checkout available during workflow run
- uninstall / rollback assumptions:
  - active runtime path can be moved aside
  - Volumio restart and recovery check are required
- services:
  - `volumio`
  - `volumio-kiosk`
- configs:
  - component-specific paths under `/data/configuration/...`
  - Volumio plugin registration state in `/data/configuration/plugins.json`
- ports:
  - Bridge overlay has been validated on `:5511`
- files / folders that matter:
  - `.github/workflows/component-test-deploy-v6.yml`
  - `.github/workflows/component-test-rollback-v6.yml`
  - `tools/deploy/sr-deploy-wrapper.sh`
  - `contracts/repo/`
  - `journals/system-integration-normalization/`
- dependencies:
  - repo checkout on workflow runner
  - active component branch/payload

## 7. Known Risks
- technical risks:
  - non-bridge deploy lanes are still not equally proven
  - some older governance material may still create noise until cleanup continues
- integration risks:
  - active `dev/<component>` branches drifting behind `main`
  - repo truth being changed without matching journal/governance updates
- rollback risks:
  - only Bridge rollback is currently well-proven
- handoff risks:
  - recovery quality falls quickly if SI stream and onboarding docs stop being maintained

## 8. Next Recommended Steps
1. merge or finalize the process-doc layer currently represented by PR `#40`
2. keep the SI stream updated for every meaningful repo-control-plane change
3. decide whether SI recovery/onboarding files should gain explicit CI enforcement
4. continue normalizing deploy maturity beyond Bridge
5. keep active component branches aligned to current `main` whenever practical

## 9. Hand-off Notes
A new specialist or integration chat should start from the governance index, onboarding file, SI status, SI decisions, SI stream, and only then move into component-specific journals and open PR review.
