# PERFORMANCE AND STATUS MATRIX V1

Status: authoritative integration standard for deployment-time observability.

## Purpose

This matrix defines the minimum before-and-after checks that must be collected around plugin or component deployment on the Pi.

## Leading rule

A deployment is not operationally complete unless pre-deploy and post-deploy status snapshots are collected and evaluated.

## Snapshot phases

For a managed component deployment, the system must collect:
- `pre_deploy`
- `post_deploy`

## Metrics that must be collected

### Core system status
- timestamp
- hostname
- uptime
- kernel
- current git ref if available

### Resource status
- 1 minute load average
- memory total
- memory available
- root filesystem used percent

### Service status
- `volumio`
- `volumio-kiosk`
- `mediastreamer-hybrid.service`
- `scale_fm_renderer.service`
- `revox-autoswitch.service`
- failed unit count

### Process visibility
Presence of key runtime processes where available:
- chromium
- Xorg
- node
- python3

## Evaluation classes

### hard fail
The deploy must be treated as failed if any of these occur:
- `volumio` is not active after deployment
- root filesystem reaches 95 percent or more used
- failed unit count increases after deployment

### warning and escalation
The deploy remains technically successful but must be flagged for review if any of these occur:
- 1 minute load average increases by more than 2.0
- available memory drops by more than 250 MB
- root filesystem usage increases by more than 200 MB

## Functional test rule

Even if all technical checks pass, the operator may still decide that the component is functionally not acceptable.
In that case the clean-absent rollback path remains mandatory.

## Current responsibility split

- integration chat defines the matrix and escalation thresholds
- deployment scripts collect and evaluate snapshots
- operator decides functional accept or reject after visible testing
