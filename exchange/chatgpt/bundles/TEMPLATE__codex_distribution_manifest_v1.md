# <topic> codex distribution manifest v1

status: in-execution
actor: codex

## manifest identity
- manifest_id: <manifest-id>
- bundle_id: <bundle-id>
- topic: <topic>
- created_at_utc: <YYYY-MM-DDTHH:MM:SSZ>
- execution_mode: sequential

## source artifacts
- raw_zip_intake: exchange/chatgpt/bundles/<topic>__raw_zip_intake_v1.md
- source_demand: exchange/chatgpt/demands/<topic>__intake_v1.md
- source_protocol: exchange/chatgpt/protocol-main/<topic>__protocol_v1.md

## validated targets
### target 001
- target_id: <target-id>
- target_branch: <si/*|dev/*>
- target_path: <repo/path>
- component_or_portfolio: <component|system-integration>
- source_bundle_paths:
  - <bundle/relative/path>
- required_checks:
  - <command>
- rollback_expectation: <revert/reset expectation>
- result_report_required: yes
