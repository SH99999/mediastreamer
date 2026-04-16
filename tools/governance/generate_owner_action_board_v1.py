#!/usr/bin/env python3
"""Generate owner action board HTML from status packets + manual tasks."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKETS = REPO / "reports" / "status" / "packets"
MANUAL = REPO / "reports" / "owner" / "owner_manual_tasks_v1.json"
OUT = REPO / "reports" / "owner" / "owner_action_board_v1.html"


def load_manual() -> list[dict]:
    if not MANUAL.exists():
        return []
    return json.loads(MANUAL.read_text(encoding="utf-8"))


def load_packets() -> list[dict]:
    items: list[dict] = []
    for p in sorted(PACKETS.glob("*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        items.append(
            {
                "title": f"Review status packet: {data.get('domain', p.stem)}",
                "type": "decision",
                "needed_from_owner": data.get("next_owner_click", "review"),
                "details": f"recommended_owner_action={data.get('recommended_owner_action', 'n/a')}",
                "source": str(p.relative_to(REPO)),
            }
        )
    return items


def render(actions: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{a['type']}</td><td>{a['title']}</td><td><code>{a['needed_from_owner']}</code></td><td>{a['details']}</td><td>{a['source']}</td></tr>"
        for a in actions
    )
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"/>
<title>Owner Action Board v1</title>
<style>
body {{ font-family: Inter, Arial, sans-serif; margin:20px; background:#0b1020; color:#e7ecff; }}
table {{ width:100%; border-collapse: collapse; background:#151d35; }}
th,td {{ border:1px solid #243055; padding:8px; text-align:left; vertical-align:top; }}
code {{ color:#6ea8fe; }}
</style></head><body>
<h1>Owner Action Board v1</h1>
<p>Single list of open owner needs (decisions, inputs, tasks, feedback).</p>
<table>
<thead><tr><th>Type</th><th>Title</th><th>Needed from owner</th><th>Details</th><th>Source</th></tr></thead>
<tbody>
{rows}
</tbody></table>
</body></html>"""


def main() -> int:
    actions = load_packets() + load_manual()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(actions), encoding="utf-8")
    print(OUT.relative_to(REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
