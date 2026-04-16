#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKETS = ROOT / 'reports' / 'status' / 'packets'
MANUAL = ROOT / 'reports' / 'owner' / 'owner_manual_tasks_v1.json'
ACTION_OUT = ROOT / 'reports' / 'owner' / 'owner_action_board_v1.html'
DECISION_OUT = ROOT / 'reports' / 'owner' / 'owner_decision_board_v1.html'
OUTBOX = ROOT / 'exchange' / 'chatgpt' / 'outbox'


def branch() -> str:
    try:
        return subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip() or 'main'
    except Exception:
        return 'main'


def blob_url(rel: str, br: str) -> str:
    return f'https://github.com/SH99999/mediastreamer/blob/{br}/{rel}'


def issue_query_url(query: str) -> str:
    return f'https://github.com/SH99999/mediastreamer/issues?q={query}'


def pull_query_url(query: str) -> str:
    return f'https://github.com/SH99999/mediastreamer/pulls?q={query}'


def iso_to_short(iso_value: str | None) -> str:
    if not iso_value:
        return 'n/a'
    try:
        dt = datetime.fromisoformat(iso_value.replace('Z', '+00:00'))
        return dt.astimezone(timezone.utc).strftime('%Y-%m-%d')
    except ValueError:
        return iso_value[:10]


def file_added_on(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime('%Y-%m-%d')


def human_action(val: str) -> str:
    m = {
        'approve_pr': 'Approve PR',
        'request_changes': 'Request changes',
        'defer': 'Defer decision',
        'run_workflow': 'Run workflow',
        'review': 'Review',
    }
    return m.get(val, val.replace('_', ' ').title())


def human_rec(val: str) -> str:
    m = {'accept': 'Accept', 'changes-requested': 'Changes requested', 'defer': 'Defer', 'reject': 'Reject'}
    return m.get(val, val)


def load_packet_items(br: str) -> list[dict]:
    items: list[dict] = []
    for p in sorted(PACKETS.glob('*.json')):
        data = json.loads(p.read_text(encoding='utf-8'))
        dom = data.get('domain', p.stem)
        rel_packet = str(p.relative_to(ROOT))
        rel_report = f'reports/status/{dom}.md'
        next_click = data.get('next_owner_click', 'review')

        action_url = blob_url(rel_report, br)
        where_to_act = f'Open report {dom}.md and apply owner click: {human_action(next_click)}'
        if next_click == 'approve_pr':
            action_url = pull_query_url('is%3Aopen+is%3Apr+label%3Astate%3Aneeds-decision')
            where_to_act = 'Open decision PR queue and approve the matching PR after evidence check'
        elif next_click == 'request_changes':
            action_url = issue_query_url('is%3Aopen+is%3Aissue+label%3Astate%3Aneeds-decision')
            where_to_act = 'Open decision issue queue and comment specific requested changes'
        elif next_click == 'run_workflow':
            action_url = blob_url('.github/workflows', br)
            where_to_act = 'Open workflows and run the workflow referenced by the linked status report'

        items.append({
            'type': 'decision',
            'title': f'{dom.upper()} decision',
            'needed_from_owner': human_action(next_click),
            'details': f"Recommended decision: {human_rec(data.get('recommended_owner_action', 'n/a'))}",
            'action_url': action_url,
            'where_to_act': where_to_act,
            'source': rel_packet,
            'added_on': iso_to_short(data.get('timestamp')),
        })
    return items


def load_owner_packets(br: str) -> list[dict]:
    items: list[dict] = []
    for p in sorted(OUTBOX.glob('*__owner_decision_packet_v1.md')):
        if p.name.startswith('TEMPLATE__'):
            continue
        rel = str(p.relative_to(ROOT))
        recommendation = 'review'
        status_value = 'ready-for-owner'
        for line in p.read_text(encoding='utf-8').splitlines():
            stripped = line.strip()
            if stripped.startswith('- recommendation:'):
                recommendation = stripped.split(':', 1)[1].strip()
            if stripped.startswith('status:'):
                status_value = stripped.split(':', 1)[1].strip()

        if status_value != 'ready-for-owner':
            continue

        items.append({
            'type': 'decision-packet',
            'title': p.name.replace('__owner_decision_packet_v1.md', '').replace('-', ' '),
            'needed_from_owner': human_rec(recommendation),
            'details': f'Owner decision packet recommendation: {human_rec(recommendation)}',
            'action_url': blob_url(rel, br),
            'where_to_act': 'Open packet, use where-to-click links, then apply decision block (accept | changes-requested | reject)',
            'source': rel,
            'added_on': file_added_on(p),
        })
    return items


def load_manual() -> list[dict]:
    if not MANUAL.exists():
        return []
    manual = json.loads(MANUAL.read_text(encoding='utf-8'))
    for item in manual:
        if 'added_on' not in item:
            item['added_on'] = 'n/a'
    return manual


def render(title: str, subtitle: str, rows: list[dict]) -> str:
    body = '\n'.join(
        '<tr>'
        f"<td>{r['type']}</td>"
        f"<td>{r['title']}</td>"
        f"<td><code>{r['needed_from_owner']}</code></td>"
        f"<td>{r['details']}</td>"
        f"<td><a href=\"{r['action_url']}\">open</a> — {r['where_to_act']}</td>"
        f"<td>{r.get('added_on', 'n/a')}</td>"
        f"<td>{r['source']}</td>"
        '</tr>'
        for r in rows
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<title>{title}</title><style>
body{{font-family:Inter,Arial,sans-serif;margin:20px;background:#0b1020;color:#e7ecff;}}
table{{width:100%;border-collapse:collapse;background:#151d35;}}
th,td{{border:1px solid #243055;padding:8px;text-align:left;vertical-align:top;}}
a{{color:#6ea8fe;}} code{{color:#8ac5ff;}}
</style></head><body><h1>{title}</h1><p>{subtitle}</p>
<table><thead><tr><th>Type</th><th>Title</th><th>Needed from owner</th><th>Details</th><th>Where & what to do</th><th>Added on</th><th>Source</th></tr></thead>
<tbody>{body}</tbody></table></body></html>'''


def main() -> int:
    br = branch()
    packet_items = load_packet_items(br)
    owner_packets = load_owner_packets(br)
    manual = load_manual()
    ACTION_OUT.parent.mkdir(parents=True, exist_ok=True)
    ACTION_OUT.write_text(render('Owner Action Board v1', 'Open owner needs (decision/input/task/feedback).', owner_packets + packet_items + manual), encoding='utf-8')
    DECISION_OUT.write_text(render('Owner Decision Board v1', 'Decision-focused view from status packets and owner packets.', owner_packets + packet_items), encoding='utf-8')
    print(ACTION_OUT.relative_to(ROOT))
    print(DECISION_OUT.relative_to(ROOT))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
