#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKETS = ROOT / 'reports' / 'status' / 'packets'
MANUAL = ROOT / 'reports' / 'owner' / 'owner_manual_tasks_v1.json'
ACTION_OUT = ROOT / 'reports' / 'owner' / 'owner_action_board_v1.html'
DECISION_OUT = ROOT / 'reports' / 'owner' / 'owner_decision_board_v1.html'


def branch() -> str:
    try:
        return subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip() or 'main'
    except Exception:
        return 'main'


def blob_url(rel: str, br: str) -> str:
    return f'https://github.com/SH99999/mediastreamer/blob/{br}/{rel}'


def human_action(val: str) -> str:
    m = {
        'approve_pr':'Approve PR',
        'request_changes':'Request changes',
        'defer':'Defer decision',
        'run_workflow':'Run workflow',
        'review':'Review',
    }
    return m.get(val, val.replace('_',' ').title())


def human_rec(val: str) -> str:
    m = {'accept':'Accept','changes-requested':'Changes requested','defer':'Defer'}
    return m.get(val, val)


def load_packet_items(br: str) -> list[dict]:
    items = []
    for p in sorted(PACKETS.glob('*.json')):
        data = json.loads(p.read_text(encoding='utf-8'))
        dom = data.get('domain', p.stem)
        rel_packet = str(p.relative_to(ROOT))
        rel_report = f'reports/status/{dom}.md'
        items.append({
            'type':'decision',
            'title':f'{dom.upper()} decision',
            'needed_from_owner':human_action(data.get('next_owner_click','review')),
            'details':f"Recommended decision: {human_rec(data.get('recommended_owner_action','n/a'))}",
            'action_url':blob_url(rel_report, br),
            'where_to_act':f'Open report {dom}.md and decide next click',
            'source':rel_packet,
        })
    return items


def load_manual() -> list[dict]:
    if not MANUAL.exists():
        return []
    return json.loads(MANUAL.read_text(encoding='utf-8'))


def render(title: str, subtitle: str, rows: list[dict]) -> str:
    body = '\n'.join(
        '<tr>'
        f"<td>{r['type']}</td>"
        f"<td>{r['title']}</td>"
        f"<td><code>{r['needed_from_owner']}</code></td>"
        f"<td>{r['details']}</td>"
        f"<td><a href=\"{r['action_url']}\">open</a> — {r['where_to_act']}</td>"
        f"<td>{r['source']}</td>"
        '</tr>' for r in rows
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<title>{title}</title><style>
body{{font-family:Inter,Arial,sans-serif;margin:20px;background:#0b1020;color:#e7ecff;}}
table{{width:100%;border-collapse:collapse;background:#151d35;}}
th,td{{border:1px solid #243055;padding:8px;text-align:left;vertical-align:top;}}
a{{color:#6ea8fe;}} code{{color:#8ac5ff;}}
</style></head><body><h1>{title}</h1><p>{subtitle}</p>
<table><thead><tr><th>Type</th><th>Title</th><th>Needed from owner</th><th>Details</th><th>Where & what to do</th><th>Source</th></tr></thead>
<tbody>{body}</tbody></table></body></html>'''


def main() -> int:
    br = branch()
    packet_items = load_packet_items(br)
    manual = load_manual()
    ACTION_OUT.parent.mkdir(parents=True, exist_ok=True)
    ACTION_OUT.write_text(render('Owner Action Board v1','Open owner needs (decision/input/task/feedback).', packet_items + manual), encoding='utf-8')
    DECISION_OUT.write_text(render('Owner Decision Board v1','Decision-focused view from status packets.', packet_items), encoding='utf-8')
    print(ACTION_OUT.relative_to(ROOT))
    print(DECISION_OUT.relative_to(ROOT))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
