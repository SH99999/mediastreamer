# chat-backup-only-command intake snapshot v1

status: closed
pickup_rule: main-inbox-v1
snapshot_immutable: true
snapshot_id: 20260417T202000Z
created_at_utc: 2026-04-17T20:20:00Z
trigger_command: ship to codex
close_reason: codex-implementation-ready; owner review pending

## codex pickup contract
- execution_branch: si/chat-backup-only-command-v1
- pickup_ready_marker: status: pickup-ready
- pickup_source: exchange/chatgpt/inbox-main/

## source artifacts
- demand_intake: exchange/chatgpt/demands/chat-backup-only-command__intake_v1.md
- materialized_protocol: exchange/chatgpt/protocol-main/chat-backup-only-command__protocol_v1.md

## objective
- implement an explicit `backup chat only` command that preserves continuity without triggering execution.

## locked decisions
1. `backup chat only` must not create demand `ready-for-codex` or inbox-main `pickup-ready` execution triggers.
2. `ship to codex` remains the only owner-visible command that starts Codex execution pickup.

## open decisions
1. none

## risks
1. command-surface confusion if docs drift between quickstart, owner reference, protocol, and exchange standard.

## execution requests
1. update owner/protocol/governance docs and publish decision-ready packet.
