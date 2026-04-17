# CHATGPT GIT EXCHANGE PLAYBOOK V1

## Objective
Provide a standard path for two-lane collaboration (ChatGPT + Codex) using Git artifacts with low owner effort and minimal knowledge loss.

## Quick start
1. Run bootstrap on dedicated branch:
   - `bash tools/governance/agent_git_bootstrap_v1.sh --role si --mode mode-b si/chatgpt-git-exchange-<topic>`
2. Create demand intake first:
   - `exchange/chatgpt/demands/<topic>__intake_v1.md`
3. Set demand status progression:
   - `draft` -> `chatok` -> `ready-for-codex`
4. Codex executes from demand + repo artifacts (not chat memory):
   - `in-execution` -> `ready-for-chatgpt-review`
5. ChatGPT review gate:
   - set `pre-ok` or `changes-requested`
6. Owner-ready handoff:
   - `ready-for-owner` with PR + rollback + next owner click
7. Mark `closed` after owner decision path completes.

## Max-delta continuity rule
No relevant chat decision/risk/request/blocker/non-loss requirement may remain chat-only for more than 5 minutes.
If durable truth update is not ready, demand intake capture is mandatory.

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

## Operating rule
Prefer short, structured artifacts over narrative text blocks.

## ChatGPT start prompt
Use:
- `docs/agents/chatgpt_start_prompt_git_exchange_v3.md`
- `docs/agents/chatgpt_start_prompt_idea_channel_v1.md`

## No-shell / GUI-only mode (single-file handoff)
If ChatGPT cannot use terminal/shell or requires repeated file permission prompts:

```bash
python3 tools/governance/chatgpt_no_shell_bundle_v1.py
```

Then upload only:
- `exchange/chatgpt/bundles/current_context_bundle_v1.md`
