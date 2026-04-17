# CHATGPT GIT EXCHANGE PLAYBOOK V1

## Objective
Provide a standard path for two-lane collaboration (ChatGPT + Codex) using Git artifacts with low owner effort and minimal knowledge loss.

## Quick start
1. Run bootstrap on dedicated branch:
   - `bash tools/governance/agent_git_bootstrap_v1.sh --role si --mode mode-b si/chatgpt-git-exchange-<topic>`
2. Activate governed mode:
   - `governed mode on`
3. Create/update live session continuity artifact first:
   - `exchange/chatgpt/sessions/<topic>__live_v1.md`
4. Promote with `ship to codex` into demand intake:
   - `exchange/chatgpt/demands/<topic>__intake_v1.md` -> `ready-for-codex` (internal `chatok`)
   - helper: `python3 tools/governance/chatgpt_promote_live_to_demand_v1.py --topic \"<topic>\" --ship-to-codex`
5. Codex executes from demand + repo artifacts (not chat memory):
   - `in-execution` -> `ready-for-chatgpt-review`
6. ChatGPT review gate:
   - set `pre-ok` or `changes-requested`
7. Owner-ready handoff:
   - `ready-for-owner` with PR + rollback + next owner click
8. Demand is auto-closed after owner merge + governance closeout completion.

## Execution gate classification
Each demand/idea item must include:
- `execution_gate: now|quick_win|backlog`
- `why_now`, `why_not_now`, `promotion_trigger`
- `safe_to_attach_to_current_package: yes|no`
- `related_files_outputs`, `impacted_portfolio_component`

Gate behavior:
- `now`: executes in current demand package
- `quick_win`: Codex may attach when safe/coherent
- `backlog`: preserved and visible to owner; not silently executed

## Max-delta continuity rule
No relevant chat decision/risk/request/blocker/non-loss requirement may remain chat-only for more than 5 minutes.
If durable truth update is not ready, live session capture is mandatory and demand promotion follows at `ship to codex`.

## Autonomous cycle init
Use:

```bash
python3 tools/governance/chatgpt_exchange_cycle_v1.py --topic "<topic>" --branch-plan "si/<topic>" --create-demand
```

This creates request/response files, an optional demand intake file, and appends a stream entry.

## Review trigger (how Codex knows when to evaluate ChatGPT content)
Use:

```bash
python3 tools/governance/chatgpt_exchange_watch_v1.py
```

Codex evaluates actionable artifacts when status is:
- `status: ready-for-codex`

## Internal channel vs owner handoff
- Internal ChatGPT↔Codex exchange may use compact/machine-oriented notes.
- Owner handoff must be generated as a human-readable decision packet.
- Decision packet template:
  - `exchange/chatgpt/outbox/TEMPLATE__owner_decision_packet_v1.md`

## Demand intake contract
Demand intake must include:
- source/context
- objective
- locked/open decisions
- required implementation
- required governance updates
- risks
- non-loss requirements
- execution request for Codex
- status marker

Template:
- `exchange/chatgpt/demands/TEMPLATE__intake_v1.md`

## Live session contract
Live session must include continuity fields and timestamp:
- `exchange/chatgpt/sessions/TEMPLATE__live_v1.md`

## Operating rule
Prefer short, structured artifacts over narrative text blocks.

## ChatGPT start prompt
Use:
- `docs/agents/chatgpt_start_prompt_git_exchange_v3.md`
- `docs/agents/chatgpt_start_prompt_idea_channel_v1.md`
- `docs/agents/chatgpt_capture_to_demand_prompt_v1.md`

## No-shell / GUI-only mode (single-file handoff)
If ChatGPT cannot use terminal/shell or requires repeated file permission prompts:

```bash
python3 tools/governance/chatgpt_no_shell_bundle_v1.py
```

Then upload only:
- `exchange/chatgpt/bundles/current_context_bundle_v1.md`
