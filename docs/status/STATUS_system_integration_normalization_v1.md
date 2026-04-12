# COMPONENT STATUS — system_integration_normalization

## 1. Scope
- component name: system_integration_normalization
- aliases: SI/N, integration chat, governance/deploy control-plane
- responsibility boundaries: repository governance, branch hygiene, workflow design, deploy/rollback path standardization, repo-side process contracts, journal coherence
- non-goals: feature implementation inside specialist components except where required to normalize deploy/runtime mechanics

## 2. Current Functional Status
- works: generic repo-driven deploy and rollback workflows on `main`; branch/ref selectable deployment; Bridge deploy lane working through v6 workflows; branch doctrine largely normalized around `main` plus `dev/<component>`
- partially works: governance docs exist but original v1 placeholder files are still not replaced in place; journals exist structurally but are not yet actively streamed
- broken: no strong CI enforcement yet; several component current-state journals still placeholders or missing mature content
- tested: Bridge deploy/rollback via generic workflow v6; repo-managed wrapper path; Volumio restart and rollback behavior
- untested: generic deploy path for non-Bridge components; multi-component rollout order enforcement in CI

## 3. Repository Mapping
- correct repo area: `contracts/`, `docs/ops/`, `.github/workflows/`, `tools/deploy/`
- status branch for this work: `main` for accepted control-plane truth
- support branches used during cleanup: short-lived integration/fix/cleanup branches only
- current placement decision: belongs on `main`

## 4. Locked Decisions
### DEC-SIN-01
- decision: `main` is the truth for workflows, governance, and accepted stable/current artifacts
- rationale: operators must run workflows from one canonical place
- impact: all manually runnable workflows live on `main`

### DEC-SIN-02
- decision: evolving component work lives on `dev/<component>`
- rationale: separates stable control-plane from changing payloads
- impact: deploy workflows accept `git_ref`

### DEC-SIN-03
- decision: deployment uses clean-replace semantics, not update-in-place semantics
- rationale: current plugins are not stable enough for safe in-place update behavior
- impact: active runtime and config are removed/archived before new payload install

### DEC-SIN-04
- decision: repo-driven deployment is the only valid deploy entrypoint
- rationale: Pi-local stale wrappers cannot be trusted across multiple Pis
- impact: workflows call repo-owned wrapper/scripts and not a preinstalled bootstrap tool

### DEC-SIN-05
- decision: Bridge and tuner are first rollout priority; other components are staged behind them
- rationale: reduces ambiguity and focuses testing on the highest-leverage path
- impact: documentation and release intake should state this order explicitly

## 5. Open Decisions
- whether stable tuner should get a generic deploy lane next or remain payload-only for now
- when to promote stronger CI checks from placeholder to enforcement
- how much journal streaming discipline should be automated versus manual

## 6. Runtime / Deployment Notes
- workflows on `main`: `component-test-deploy-v6`, `component-test-rollback-v6`
- repo wrapper: `tools/deploy/sr-deploy-wrapper.sh`
- current supported deployed component in workflow: Bridge
- rollback includes plugin unregistration for Bridge via `plugins.json` state update
- baseline deploy rule includes Volumio restart and recovery wait

## 7. Known Risks
- governance placeholders still exist in old v1 paths
- journals are not yet maintained as a live stream
- CI checks are still too weak for path ownership, manifest consistency, and payload validation
- non-Bridge components do not yet have equivalent deploy/rollback maturity

## 8. Next Recommended Steps
1. replace or retire the remaining governance placeholders cleanly
2. create real current-state and stream journals for each active component
3. add CI enforcement for payload presence and path ownership
4. decide next production-grade rollout after Bridge: tuner or starter/autoswitch path

## 9. Hand-off Notes
A new specialist or Codex-style agent should treat the repository control-plane as real and current. Use `main` for workflows and governance, use `dev/<component>` for evolving payloads, and do not invent new branch doctrine locally.
