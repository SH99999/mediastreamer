# DEPLOY CONTRACT V2 — TUNER FIRST

Status: authoritative integration decision for the next deployment upgrade.

## Purpose

Deploy V2 upgrades the meaning of deployment from file synchronization to installation readiness for V2-capable components.

A deployment is only considered successful when the target component:
1. is resolved from the canonical repository ref,
2. is copied into the canonical deployment workspace,
3. executes its install hook,
4. executes its configuration hook,
5. activates or restarts its required runtime services,
6. passes its component health check,
7. writes deploy state and rollback state.

## Tuner-first rollout rule

Deploy V2 is introduced for the Tuner first.

This means:
- `sr-deploy tuner latest` is the first command that must become fully install-capable under V2.
- Bundle-level V2 behavior is not mandatory until the Tuner flow is proven.
- AutoSwitch is the next candidate after Tuner.
- Bridge and Fun Line remain on synchronization-oriented deployment until their installation contracts are explicitly normalized.

## Component status under Deploy V2

### Tuner
- status: next implementation target
- expectation: installed, configured, runtime-enabled, health-checked

### Starter
- status: remains governed by existing runtime and system baseline
- expectation: no V2 migration required before Tuner completion

### AutoSwitch
- status: second candidate after Tuner
- expectation: systemd service and ADC path health-check after Tuner

### Bridge
- status: still sync-oriented
- expectation: plugin runtime deployment only after separate normalization

### Fun Line
- status: still sync-oriented
- expectation: plugin runtime deployment only after separate normalization

## Canonical Tuner V2 phases

1. preflight
2. install
3. configure
4. activate
5. healthcheck
6. state-write

## Required Tuner V2 artifacts in repo

The Tuner path must contain these files before Tuner V2 is considered executable:
- `components/scale-radio-tuner/install.sh`
- `components/scale-radio-tuner/configure.sh`
- `components/scale-radio-tuner/healthcheck.sh`
- `components/scale-radio-tuner/runtime_manifest.yaml`

## Success rule

A Tuner V2 deploy is green only if:
- the install step exits successfully,
- the configure step exits successfully,
- the activation step completes,
- the healthcheck exits successfully.

## Failure rule

If any phase fails:
- the deployment must stop,
- the failing phase must be recorded in state,
- `last_successful_ref` must not be advanced.
