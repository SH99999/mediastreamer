#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess


@dataclass
class JournalAuditRow:
    component: str
    active_stream: str
    older_streams: list[str]
    stale_write_violation: bool
    historical_marker_missing: list[str]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_read_order_items(text: str) -> list[str]:
    lines = text.splitlines()
    in_read_order = False
    items: list[str] = []
    for line in lines:
        if line.startswith("## ") and line.strip() == "## Read order":
            in_read_order = True
            continue
        if in_read_order and line.startswith("## "):
            break
        if in_read_order:
            m = re.match(r"^\d+\.\s+`([^`]+)`", line.strip())
            if m:
                items.append(m.group(1).strip())
    return items


def git_last_commit_ts(root: Path, rel_path: str) -> int:
    proc = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%ct", "--", rel_path],
        capture_output=True,
        text=True,
        check=False,
    )
    out = proc.stdout.strip()
    return int(out) if out.isdigit() else 0


def audit_journal_revision(root: Path) -> list[JournalAuditRow]:
    rows: list[JournalAuditRow] = []
    stream_files = sorted(root.glob("journals/*/stream_v*.md"))
    by_component: dict[str, list[Path]] = {}
    for p in stream_files:
        component = p.parent.name
        by_component.setdefault(component, []).append(p)

    for component, files in sorted(by_component.items()):
        versioned = []
        for p in files:
            m = re.search(r"stream_v(\d+)\.md$", p.name)
            if m:
                versioned.append((int(m.group(1)), p))
        versioned.sort(key=lambda t: t[0])
        active_v, active_path = versioned[-1]
        active_rel = active_path.relative_to(root).as_posix()
        active_ts = git_last_commit_ts(root, active_rel)

        older = [p for v, p in versioned if v < active_v]
        stale_write_violation = False
        missing_marker: list[str] = []
        for p in older:
            rel = p.relative_to(root).as_posix()
            ts = git_last_commit_ts(root, rel)
            if ts > active_ts:
                stale_write_violation = True
            text = read(p).lower()
            if "historical" not in text and "read-only" not in text:
                missing_marker.append(rel)

        rows.append(
            JournalAuditRow(
                component=component,
                active_stream=active_rel,
                older_streams=[p.relative_to(root).as_posix() for p in older],
                stale_write_violation=stale_write_violation,
                historical_marker_missing=missing_marker,
            )
        )

    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    governance_index = root / "contracts/repo/system_integration_governance_index_v7.md"
    onboarding = root / "docs/agents/system_integration_recovery_onboarding_v7.md"

    governance_items = extract_read_order_items(read(governance_index))
    onboarding_items = extract_read_order_items(read(onboarding))

    governance_set = set(governance_items)
    onboarding_set = set(onboarding_items)
    overlap = governance_set & onboarding_set
    union = governance_set | onboarding_set

    missing_from_disk = [item for item in sorted(union) if not (root / item).exists()]

    # Onboarding time model (minutes)
    quick_min = len(onboarding_items) * 0.5
    standard_min = len(onboarding_items) * 1.0
    deep_min = len(onboarding_items) * 1.75

    journal_rows = audit_journal_revision(root)
    stale_violations = [r for r in journal_rows if r.stale_write_violation]
    marker_violations = [r for r in journal_rows if r.historical_marker_missing]

    generated_at = datetime.now(timezone.utc).isoformat()
    out = root / "reports/governance/onboarding_journal_revision_audit_v1.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Onboarding & Journal Revision Audit v1",
        "",
        f"_Generated: {generated_at}_",
        "",
        "## Onboarding unification check",
        f"- governance_index_read_order_count: {len(governance_items)}",
        f"- onboarding_read_order_count: {len(onboarding_items)}",
        f"- overlap_count: {len(overlap)}",
        f"- jaccard_similarity: {len(overlap) / max(1, len(union)):.3f}",
        f"- missing_read_order_paths_on_disk: {len(missing_from_disk)}",
        "",
        "## Onboarding time estimate",
        f"- quick_path_minutes (30s per document): {quick_min:.1f}",
        f"- standard_path_minutes (60s per document): {standard_min:.1f}",
        f"- deep_path_minutes (105s per document): {deep_min:.1f}",
        "",
        "## Journal revision audit",
        f"- components_with_versioned_streams: {len(journal_rows)}",
        f"- stale_write_violations: {len(stale_violations)}",
        f"- historical_marker_violations: {len(marker_violations)}",
        "",
        "## Journal rows",
    ]

    for row in journal_rows:
        lines.extend([
            f"### {row.component}",
            f"- active_stream: `{row.active_stream}`",
            f"- older_streams: `{', '.join(row.older_streams) if row.older_streams else '-'}`",
            f"- stale_write_violation: `{str(row.stale_write_violation).lower()}`",
            f"- historical_marker_missing: `{', '.join(row.historical_marker_missing) if row.historical_marker_missing else '-'}`",
            "",
        ])

    if missing_from_disk:
        lines.append("## Missing read-order paths")
        lines.extend([f"- `{p}`" for p in missing_from_disk])
        lines.append("")

    lines.extend([
        "## Executed logic",
        "1. parse read-order lists in governance index + onboarding docs",
        "2. compute overlap/unification and path existence",
        "3. estimate onboarding time using quick/standard/deep model",
        "4. audit journal stream revision discipline via git last-commit timestamps and historical markers",
    ])

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("onboarding_journal_revision_audit=ok")
    print(f"report={out.relative_to(root)}")
    print(f"stale_write_violations={len(stale_violations)}")
    print(f"historical_marker_violations={len(marker_violations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
