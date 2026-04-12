# REPOSITORY LANGUAGE STANDARD V2

## Leading rule
Repository-facing content is English.

## Applies to
- contracts
- workflows
- deploy scripts
- rollback scripts
- README files
- current-state journals
- stream journals
- decision logs
- PR bodies where practical
- payload-facing docs intended for future maintenance

## Allowed exceptions
The following may remain non-English if they are part of imported historical payload material and not yet normalized:
- legacy release notes
- legacy install notes
- user-facing strings inside imported payloads

When this happens, the component current-state journal should note that normalization is still pending.

## Naming rules
Prefer these repository terms consistently:
- `main` = truth
- `dev/<component>` = component work lane
- `payload` = extracted release tree inside the repo
- `deploy candidate scripts` = install/healthcheck/remove scripts for repo-driven execution
- `current_state` = factual snapshot
- `stream` = append-only event log

## Alias handling
When a component has a legacy name, document it once and prefer the normalized repo name afterward.
Example:
- `scale-radio-tuner` = normalized name
- `scale fm` = legacy alias

## Commit and PR guidance
Keep commit messages and PR titles short, explicit, and English.

## Journal guidance
Journals should use short, direct English entries and avoid conversational wording.
