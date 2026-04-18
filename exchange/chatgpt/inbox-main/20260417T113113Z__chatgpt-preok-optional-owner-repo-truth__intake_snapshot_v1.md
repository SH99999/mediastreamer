# chatgpt-preok-optional-owner-repo-truth intake snapshot v1

status: closed
pickup_rule: main-inbox-v1
snapshot_immutable: true
snapshot_id: 20260417T113113Z
created_at_utc: 2026-04-17T11:31:13Z
trigger_command: ship to codex
close_reason: merged-on-main; demand closed

## codex pickup contract
- execution_branch: si/chatgpt-preok-optional-owner-repo-truth-v1
- pickup_ready_marker: status: pickup-ready
- pickup_source: exchange/chatgpt/inbox-main/

## source artifacts
- demand_intake: exchange/chatgpt/demands/chatgpt-preok-optional-owner-repo-truth__intake_v1.md
- materialized_protocol: exchange/chatgpt/protocol-main/chatgpt-preok-optional-owner-repo-truth__protocol_v1.md

## objective
- make ChatGPT `pre-ok` optional advisory instead of required merge gate
- keep owner merge decision repo-truth first while preserving auditability
- align canonical owner/exchange docs and demand lifecycle wording

## locked decisions
1. owner merge decision should not depend on ChatGPT pre-authorization
2. ChatGPT review remains optional advisory input
3. project custom fields remain optional convenience and must not become critical-path

## open decisions
1. none

## risks
1. wording drift across owner/exchange docs if lifecycle language is not synchronized

## execution requests
1. update canonical governance/exchange docs to reflect optional advisory pre-ok
2. publish canonical main inbox snapshot and linked demand/protocol artifacts for pickup

## related git objects
- demand_path: exchange/chatgpt/demands/chatgpt-preok-optional-owner-repo-truth__intake_v1.md
- protocol_path: exchange/chatgpt/protocol-main/chatgpt-preok-optional-owner-repo-truth__protocol_v1.md
- snapshot_path: exchange/chatgpt/inbox-main/20260417T113113Z__chatgpt-preok-optional-owner-repo-truth__intake_snapshot_v1.md
- source_pr_url: https://github.com/SH99999/mediastreamer/pull/147
