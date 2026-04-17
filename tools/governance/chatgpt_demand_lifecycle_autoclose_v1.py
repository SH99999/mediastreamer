#!/usr/bin/env python3
"""Auto-close demand artifacts when merge + closeout criteria are satisfied."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
DEMANDS = ROOT / "exchange" / "chatgpt" / "demands"
STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
LINE_RE = re.compile(r"^-\s*([^:]+):\s*(.*)$")
PR_RE = re.compile(r"github\.com/([^/]+/[^/]+)/pull/(\d+)")


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def extract_status(text: str) -> str:
    m = STATUS_RE.search(text)
    return m.group(1).strip().lower() if m else "missing"


def replace_status(text: str, value: str) -> str:
    if STATUS_RE.search(text):
        return STATUS_RE.sub(f"status: {value}", text, count=1)
    return f"status: {value}\n" + text


def parse_kv_lines(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = LINE_RE.match(line.strip())
        if not m:
            continue
        out[m.group(1).strip().lower().replace(" ", "_")] = m.group(2).strip()
    return out


def pr_merged(source_pr_url: str, token: str) -> bool:
    m = PR_RE.search(source_pr_url)
    if not m:
        return False
    repo, pr_num = m.group(1), m.group(2)
    req = Request(
        f"https://api.github.com/repos/{repo}/pulls/{pr_num}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return bool(data.get("merged"))


def maybe_close(path: Path, token: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    status = extract_status(text)
    meta = parse_kv_lines(text)

    if status not in {"pre-ok", "ready-for-owner"}:
        return False

    review = meta.get("chatgpt_review_result", "pending").lower()
    override = meta.get("owner_review_override", "no").lower()
    closeout = meta.get("governance_closeout_status", "pending").lower()
    source_pr = meta.get("source_pr_url", "")

    review_ok = review == "pre-ok" or (review == "owner-override" and override == "yes")
    if not review_ok or closeout != "done" or not source_pr:
        return False
    if not pr_merged(source_pr, token):
        return False

    out = replace_status(text, "closed")
    stamp = datetime.now(timezone.utc).isoformat()
    trigger = "merged_pr+pre_ok+closeout_done" if review == "pre-ok" else "merged_pr+owner_override+closeout_done"
    out += f"\n- auto_closed_at_utc: {stamp}\n- auto_close_trigger: {trigger}\n"

    if not dry_run:
        path.write_text(out, encoding="utf-8")
    print(f"auto-closed: {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or ""
    if not token:
        print("warning: no token; skipping auto-close")
        return 0

    changed = 0
    for path in sorted(DEMANDS.glob("*__intake_v*.md")):
        if path.name.startswith("TEMPLATE__"):
            continue
        if maybe_close(path, token, args.dry_run):
            changed += 1

    print(f"auto_closed_count={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
