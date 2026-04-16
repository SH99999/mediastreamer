# STATUS PROMPT REPORTS V1

## Purpose
Enable short prompt-based status responses with pre-generated, clickable, and visualized markdown reports.

## Generator
Run:

```bash
python3 tools/governance/generate_status_reports_v1.py --repo-root . --out-dir reports/status
```

Generated files:
- `reports/status/index.md`
- `reports/status/tuner.md`
- `reports/status/governance.md`
- `reports/status/ui.md`
- `reports/status/bridge.md`
- `reports/status/decisions.md`
- `reports/status/blocker.md`

## Prompt aliases
- `status tuner`
- `status governance`
- `status ui`
- `status bridge`
- `status decisions`
- `status blocker`

## Output contract
Each report must provide:
- short bullet summary
- clickable links to source objects in repository
- visual block (Mermaid chart)
- concise next-action context where available

## Source-of-truth rule
Reports are generated from repo truth files so prompts can be handled without hidden external state.
