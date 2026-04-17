# ChatGPT governed intake prompt v1

## Purpose
This document gives the owner a no-copy-paste chat prompt so an agent can take proposal content from a URI/file reference and do the Git/governance lifting.

## Owner quick prompt (minimal)
Use this exact prompt in chat when you want the agent to run intake and Git steps:

```text
Governed intake request.
Source proposal location: <URI or repo path>
Proposal revision/digest: <commit SHA, file hash, or dated version>
Demand type: <ui_ux|component_runtime|cross_component|system_integration>
Impacted components: <comma-separated component suffixes>
Decision needed from owner: <single sentence>
Options: <opt-a>; <opt-b>; <opt-c>
Recommended option: <opt-a|opt-b|opt-c>
Run `governed mode on`, then create/update live session at exchange/chatgpt/sessions/<topic>__live_v1.md within 5 minutes for every material delta.
Use `ship to codex` to promote into exchange/chatgpt/demands/<topic>__intake_v1.md, update protocol-main, and publish canonical intake snapshot under `exchange/chatgpt/inbox-main/` (`status: pickup-ready`).
Do the full governance flow: prepare documented Codex job via git, execute on si/<topic>, update required governance/journal truth, move demand through in-execution->ready-for-chatgpt-review->pre-ok->ready-for-owner->closed (automatic closure after merge + closeout), push branch, open PR to main, and report only final approval action for owner.
Codex must classify and maintain execution gate (`now|quick_win|backlog`) and perform routing/decomposition; owner does not classify components/streams/docs manually.
Codex may attach `quick_win` items to current package only when low-risk/coherent; otherwise preserve as `backlog` with promotion trigger.
```

## Owner prompt (strict form)
Use this when you want deterministic parsing and less back-and-forth:

```yaml
governed_intake_v1:
  source_proposal_uri: "<URI or repo path>"
  proposal_revision: "<immutable revision/hash>"
  demand_type: "<ui_ux|component_runtime|cross_component|system_integration>"
  impact: "<component-only|cross-component|system-wide>"
  components: ["<suffix-1>", "<suffix-2>"]
  decision_need: "<single-sentence decision>"
  decision_options:
    - id: "opt-a"
      text: "<option a>"
    - id: "opt-b"
      text: "<option b>"
    - id: "opt-c"
      text: "<option c>"
  recommended_option: "opt-a"
  non_loss_requirements:
    - "capture demand artifact in repo within 5 minutes"
  execution_request:
    branch_topic: "si/<topic>"
    require_pr_to_main: true
    require_chatgpt_pre_ok: true
    report_mode: "owner-approval-only"
```

## Expected agent output
The agent should return:
1. demand intake artifact path + status
2. branch + commit + PR URL
3. rollback command
4. next owner click
5. one explicit owner action: approve/merge PR (or exact blocker)

## Notes
- `source_proposal_uri` can be a GitHub file URL, gist URL, issue comment URL, or an existing repo path.
- If the proposal exists only in another chat, capture it into `exchange/chatgpt/sessions/<topic>__live_v1.md` first, then use `ship to codex`.
