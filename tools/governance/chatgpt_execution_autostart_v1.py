#!/usr/bin/env python3
"""Autostart helper for ChatGPT exchange execution.

Purpose:
- detect newest demand with `status: ready-for-codex`
- create/update one execution issue automatically

This script intentionally does not modify demand lifecycle files directly because
main is protected and demand truth should be updated from a governed Codex branch.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
DEMANDS_DIR = REPO_ROOT / "exchange" / "chatgpt" / "demands"
STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
EXEC_BRANCH_RE = re.compile(r"^- execution branch:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
TRIGGER_RE = re.compile(r"codex_trigger:\s*ship-to-codex", re.IGNORECASE)
TOPIC_SUFFIX = "__intake_v1"


@dataclass
class Demand:
    path: Path
    topic: str
    status: str
    execution_branch: str
    has_trigger: bool


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_demand(path: Path) -> Demand:
    text = read_text(path)
    status_match = STATUS_RE.search(text)
    status = status_match.group(1).strip().lower() if status_match else "missing"
    exec_branch_match = EXEC_BRANCH_RE.search(text)
    execution_branch = exec_branch_match.group(1).strip() if exec_branch_match else ""
    topic = path.stem
    if topic.endswith(TOPIC_SUFFIX):
        topic = topic[: -len(TOPIC_SUFFIX)]
    return Demand(
        path=path,
        topic=topic,
        status=status,
        execution_branch=execution_branch,
        has_trigger=bool(TRIGGER_RE.search(text)),
    )


def ready_demands() -> Iterable[Demand]:
    if not DEMANDS_DIR.exists():
        return []
    candidates: list[Demand] = []
    for path in sorted(DEMANDS_DIR.glob("*.md")):
        if path.name.startswith("TEMPLATE__"):
            continue
        demand = parse_demand(path)
        if demand.status == "ready-for-codex" and demand.has_trigger:
            candidates.append(demand)
    candidates.sort(key=lambda d: d.path.stat().st_mtime, reverse=True)
    return candidates


def github_request(url: str, token: str, method: str = "GET", data: dict | None = None) -> dict | list:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "mediastreamer-codex-autostart",
    }
    payload = None
    if data is not None:
        payload = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, headers=headers, method=method, data=payload)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {method} {url} failed ({exc.code}): {body}") from exc


def ensure_issue(repo: str, token: str, demand: Demand) -> str:
    title = f"[codex-autostart] execute demand: {demand.topic}"
    q = quote_plus(f'repo:{repo} is:issue is:open in:title "{title}"')
    search = github_request(f"https://api.github.com/search/issues?q={q}", token)
    assert isinstance(search, dict)
    items = search.get("items") or []
    if items:
        return items[0]["html_url"]

    body = "\n".join(
        [
            "Autostart execution issue generated from governed exchange demand.",
            "",
            f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
            f"- demand_path: `{demand.path.relative_to(REPO_ROOT)}`",
            f"- demand_status: `{demand.status}`",
            f"- execution_branch_hint: `{demand.execution_branch or 'si/<topic>'}`",
            "",
            "Required next step:",
            "- start implementation immediately from this demand and move lifecycle to in-execution on branch truth.",
        ]
    )
    payload = {
        "title": title,
        "body": body,
        "labels": [
            "state:ready-for-agent",
            "agent:system-integration",
            "component:system-integration",
        ],
    }
    try:
        created = github_request(
            f"https://api.github.com/repos/{repo}/issues",
            token,
            method="POST",
            data=payload,
        )
    except RuntimeError as exc:
        if "Validation Failed" not in str(exc):
            raise
        payload.pop("labels", None)
        created = github_request(
            f"https://api.github.com/repos/{repo}/issues",
            token,
            method="POST",
            data=payload,
        )
    assert isinstance(created, dict)
    return created.get("html_url", "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Autostart governed codex execution from ready demands")
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY", ""), help="owner/repo for issue creation")
    parser.add_argument("--auto-issue", action="store_true", help="create/update GitHub issue for newest ready demand")
    args = parser.parse_args()

    candidates = list(ready_demands())
    if not candidates:
        print("no-ready-demand")
        return 0

    demand = candidates[0]
    print(f"selected_topic={demand.topic}")
    print(f"selected_demand={demand.path.relative_to(REPO_ROOT)}")
    print(f"execution_branch_hint={demand.execution_branch or 'si/<topic>'}")

    if args.auto_issue:
        token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
        if not token:
            print("error: missing GH_TOKEN/GITHUB_TOKEN for --auto-issue", file=sys.stderr)
            return 2
        if not args.repo:
            print("error: missing --repo (owner/repo)", file=sys.stderr)
            return 2
        url = ensure_issue(args.repo, token, demand)
        print(f"issue_url={url}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
