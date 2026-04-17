# <topic> intake snapshot v1

status: pickup-ready
pickup_rule: main-inbox-v1
snapshot_immutable: true
snapshot_id: <YYYYMMDDTHHMMSSZ>
created_at_utc: <YYYY-MM-DDTHH:MM:SSZ>
trigger_command: ship to codex

## codex pickup contract
- execution_branch: si/<topic>-v1
- pickup_ready_marker: status: pickup-ready
- pickup_source: exchange/chatgpt/inbox-main/

## source artifacts
- demand_intake: exchange/chatgpt/demands/<topic>__intake_v1.md
- materialized_protocol: exchange/chatgpt/protocol-main/<topic>__protocol_v1.md

## objective
- 

## locked decisions
1.

## open decisions
1.

## risks
1.

## execution requests
1.
