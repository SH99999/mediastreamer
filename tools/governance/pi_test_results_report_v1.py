#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_summary_files(root: Path):
    for summary_path in sorted(root.glob("*/**/summary.json")):
        try:
            data = json.loads(summary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        component = data.get("component") or summary_path.parts[-3]
        yield {
            "component": component,
            "run_id": data.get("run_id") or summary_path.parent.name,
            "status": data.get("status", "unknown"),
            "deploy_duration_sec": float(data.get("deploy_duration_sec", 0) or 0),
            "healthcheck_duration_sec": float(data.get("healthcheck_duration_sec", 0) or 0),
            "rollback_duration_sec": float(data.get("rollback_duration_sec", 0) or 0),
        }


def aggregate(rows):
    by_component = {}
    for row in rows:
        c = row["component"]
        by_component.setdefault(c, []).append(row)

    out = []
    for component, items in sorted(by_component.items()):
        total = len(items)
        passed = sum(1 for i in items if i["status"] == "pass")
        avg_deploy = sum(i["deploy_duration_sec"] for i in items) / total
        avg_health = sum(i["healthcheck_duration_sec"] for i in items) / total
        avg_rollback = sum(i["rollback_duration_sec"] for i in items) / total
        out.append(
            {
                "component": component,
                "runs": total,
                "passed": passed,
                "pass_rate": passed / total if total else 0,
                "avg_deploy": avg_deploy,
                "avg_health": avg_health,
                "avg_rollback": avg_rollback,
            }
        )
    return out


def to_markdown(agg):
    lines = []
    lines.append("# Pi Test Results Report v1")
    lines.append("")
    lines.append("## Summary table")
    lines.append("")
    lines.append("| Component | Runs | Passed | Pass Rate | Avg Deploy (s) | Avg Health (s) | Avg Rollback (s) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in agg:
        lines.append(
            f"| {r['component']} | {r['runs']} | {r['passed']} | {r['pass_rate']:.2%} | {r['avg_deploy']:.1f} | {r['avg_health']:.1f} | {r['avg_rollback']:.1f} |"
        )

    lines.append("")
    lines.append("## Pass-rate chart (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("xychart-beta")
    lines.append('    title "Component pass rate"')
    labels = ", ".join(f'"{r["component"]}"' for r in agg)
    values = ", ".join(f"{r['pass_rate']*100:.1f}" for r in agg)
    lines.append(f"    x-axis [{labels}]")
    lines.append('    y-axis "Pass %" 0 --> 100')
    lines.append(f"    bar [{values}]")
    lines.append("```")

    lines.append("")
    lines.append("## Avg deploy duration chart (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("xychart-beta")
    lines.append('    title "Average deploy duration (seconds)"')
    lines.append(f"    x-axis [{labels}]")
    max_deploy = max((r["avg_deploy"] for r in agg), default=0)
    ymax = int(max(10, max_deploy * 1.2))
    deploy_vals = ", ".join(f"{r['avg_deploy']:.1f}" for r in agg)
    lines.append(f'    y-axis "Seconds" 0 --> {ymax}')
    lines.append(f"    bar [{deploy_vals}]")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate markdown report from Pi test run bundles.")
    parser.add_argument("--root", required=True, help="Root directory containing artifacts/pi-test-results")
    parser.add_argument("--out", required=True, help="Output markdown file path")
    args = parser.parse_args()

    rows = list(load_summary_files(Path(args.root)))
    agg = aggregate(rows)
    markdown = to_markdown(agg)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(f"wrote_report={out_path}")
    print(f"components={len(agg)}")


if __name__ == "__main__":
    main()
