# agent-registry-and-full-role-formalization intake v1

status: closed
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T00:00:00Z
- participants: owner, chatgpt

## objective
- formalize the active agent landscape in repo truth so SI knows which agents exist and are available for delegation
- let owner inspect defined agents, availability, roles, startup prompts, and bootstrap commands from Git truth

## locked decisions
1. `dev-fun-line`, `dev-autoswitch`, `dev-ux`, and `dev-hardware` should be available as formal agent roles
2. hardware must be a first-class role, not only a routing/component concept
3. SI must read delegation availability from repo truth, not implicit memory
4. owner must be able to inspect which agents are defined, whether they are available, what their role is, which startup prompt is correct, and which bootstrap command should be used

## open decisions
1. whether additional optional roles beyond the requested set should be marked `planned` in the first registry version if not actively used now

## required implementation
1. add a canonical agent registry in human-readable and machine-readable form
2. extend role/bootstrap/start-prompt materials so hardware, fun-line, autoswitch, and ux become first-class startup roles
3. update SI-facing delegation guidance so SI can read agent availability and delegation targets from repo truth
4. add an owner-visible startup index with agent, available yes/no, role summary, startup prompt path, and bootstrap command
5. add the minimum bootstrap/start helpers needed so agent creation/launch in Codex is deterministic

## required governance updates
1. keep the role system centralized and consistent with `AGENTS.md`, bootstrap docs, role profiles, and start prompts
2. link owner- and SI-facing docs to the new registry/start index without creating new dashboard or HTML sprawl

## risks
1. current repo state formalizes only SI, tuner, bridge, and generic startup roles cleanly; other desired roles remain implicit without a central registry
2. SI cannot safely delegate by repo truth if available/unavailable roles are not centralized

## non-loss requirements
1. the requested agent roster and role expectations from this chat must not remain only in chat memory
2. owner must not need to reverse-engineer role availability from labels or streams

## execution request for Codex
- execution branch: si/agent-registry-and-full-role-formalization-v1
- required output: PR to `main` + decision-ready packet + rollback command + next owner click

## execution gate
- execution_gate: now
- execution_gate_label: gate:now
- why_now: current repo role model is incomplete for requested agents and SI cannot reliably know available delegation targets from repo truth
- why_not_now: delaying leaves hardware/fun-line/autoswitch/ux implicit and increases owner friction
- promotion_trigger: owner requested full formalization and delegation awareness now
- safe_to_attach_to_current_package: yes
- related_files_outputs: docs/agents/agent_registry_v1.md; tools/governance/agent_registry_v1.json; docs/agents/agent_start_index_v1.md
- impacted_portfolio_component: system-integration

## label index (query/routing)
- expected_labels:
  - gate:now
  - state:ready-for-agent
  - component:system-integration
  - agent:system-integration
- label_truth_rule: labels route/query only; repo sections in this file remain canonical detailed truth

## lifecycle tracking
- codex_trigger: ship-to-codex
- source_pr_url:
- source_branch: si/agent-registry-and-role-availability-v1
- review_target_artifacts:
- chatgpt_review_result: pending
- owner_review_override: no
- owner_override_note:
- governance_closeout_status: done
- next_owner_click: none (closed; merged work already present on main)
