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
Do the full governance flow: create/update intake issue fields, prepare decision_output_v1, update required governance/journal docs, commit on si/<topic>, push branch, open PR to main, and report only final approval action for owner.
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
  execution_request:
    branch_topic: "si/<topic>"
    require_pr_to_main: true
    report_mode: "owner-approval-only"
```

## Expected agent output
The agent should return:
1. intake artifact path(s) or issue update fields
2. `decision_output_v1` block
3. branch + commit + PR URL
4. one explicit owner action: approve/merge PR (or exact blocker)

## Notes
- `source_proposal_uri` can be a GitHub file URL, gist URL, issue comment URL, or an existing repo path.
- If the proposal exists only in another chat, put it into a file once (gist/repo file) and reference the URI; after that no repeated copy/paste is needed.
