#!/usr/bin/env python3
"""Validate the observed v2 bundle and create paper-ready results artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "experiments/exp001_mvp/tables/veritype_cost_constrained_owner_disjoint_confirmation_v2_observed_bundle"
OUT = ROOT / "experiments/exp001_mvp/tables/veritype_cost_constrained_owner_disjoint_confirmation_v2_paper_results_v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def esc(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def write_svg(rows: list[dict[str, object]]) -> None:
    width, height = 1160, 560
    left, right, top, bottom = 300, 1050, 125, 70
    x_min, x_max = 0.60, 0.85
    colors = {
        "structure_only": "#117a65",
        "confidence_only": "#2874a6",
        "full": "#8e44ad",
        "hash_random": "#7f8c8d",
        "unusable_only": "#ca6f1e",
        "always_primary": "#566573",
        "always_fallback": "#a93226",
    }
    label = {
        "structure_only": "Structure-aware (primary)",
        "confidence_only": "Confidence-only",
        "full": "Full-feature ablation",
        "hash_random": "Hash-random baseline",
        "unusable_only": "Unusable-only escalation",
        "always_primary": "Always primary model",
        "always_fallback": "Always fallback model",
    }
    def x(value: float) -> float:
        return left + (value - x_min) / (x_max - x_min) * (right - left)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933}.title{font-size:23px;font-weight:700}.sub{font-size:14px;fill:#52616b}.axis{font-size:13px;fill:#52616b}.row{font-size:15px}.value{font-size:13px;font-weight:700}</style>',
        '<text x="55" y="42" class="title">Owner-disjoint confirmation: accuracy and fallback cost</text>',
        '<text x="55" y="67" class="sub">188 owners; 3,760 machine-validated Java type-recovery targets; observed raw-ledger bundle</text>',
    ]
    for tick in (0.60, 0.65, 0.70, 0.75, 0.80, 0.85):
        px = x(tick)
        parts.append(f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{height-bottom}" stroke="#d9e2e7" stroke-width="1"/>')
        parts.append(f'<text x="{px:.1f}" y="{height-35}" text-anchor="middle" class="axis">{tick * 100:.0f}%</text>')
    parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{right}" y2="{height-bottom}" stroke="#52616b" stroke-width="1.5"/>')
    parts.append(f'<text x="{(left + right) / 2}" y="{height-12}" text-anchor="middle" class="axis">Exact-recovery accuracy</text>')
    for index, row in enumerate(rows):
        y = top + 32 + index * 50
        route = str(row["route"])
        accuracy = float(row["accuracy"])
        color = colors[route]
        parts.append(f'<text x="{left-18}" y="{y + 5}" text-anchor="end" class="row">{esc(label[route])}</text>')
        parts.append(f'<line x1="{left}" y1="{y}" x2="{x(accuracy):.1f}" y2="{y}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{x(accuracy):.1f}" cy="{y}" r="8" fill="{color}"/>')
        parts.append(f'<text x="{x(accuracy) + 14:.1f}" y="{y + 5}" class="value">{accuracy * 100:.2f}% | ${float(row["cost"]):.2f}</text>')
    parts.append('<text x="55" y="520" class="sub">Labels show accuracy | incremental fallback cost. Cost is the observed recorded route cost, not a current price quote.</text>')
    parts.append('</svg>')
    (OUT / "figure_1_owner_disjoint_accuracy_cost.svg").write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    manifest = json.loads((BUNDLE / "sha256.json").read_text(encoding="utf-8"))
    audit = json.loads((BUNDLE / "audit_summary.json").read_text(encoding="utf-8"))
    summary = json.loads((BUNDLE / "source_summary.observed.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []
    for name, entry in manifest["artifacts"].items():
        path = ROOT / entry["path"]
        observed = sha256(path) if path.is_file() else None
        checks.append({"artifact": name, "path": entry["path"], "expected_sha256": entry["sha256"], "observed_sha256": observed, "passed": observed == entry["sha256"]})
    required = {
        "audit_status": audit.get("status") == "fully_reproducible_observed_evidence_validated",
        "summary_status": summary.get("data_status") == "observed_summary_from_raw_ledgers",
        "audit_discrepancies_zero": audit.get("discrepancy_count") == 0,
        "identity_audit_pass": summary.get("identity_audit", {}).get("status") == "PASS",
        "matched_budget": summary.get("cost_and_budget", {}).get("matched_budget_contract_satisfied") is True,
        "cohort_size": summary.get("cohort", {}).get("owners") == 188 and summary.get("cohort", {}).get("targets") == 3760,
    }
    passed = all(item["passed"] for item in checks) and all(required.values())
    OUT.mkdir(parents=True, exist_ok=True)

    route_order = ["always_primary", "always_fallback", "unusable_only", "confidence_only", "hash_random", "structure_only", "full"]
    rows = []
    for route in route_order:
        item = summary["routes"][route]
        rows.append({
            "route": route,
            "role": item["evidence_role"],
            "correct": item["correct"],
            "targets": item["targets"],
            "accuracy": item["accuracy"],
            "fallback_calls": item["fallback_calls"],
            "cost": item["incremental_fallback_usd"],
            "no_prediction": item["no_prediction"],
        })
    with (OUT / "table_1_owner_disjoint_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Table 1. Owner-Disjoint Matched-Budget Confirmation Results",
        "",
        "Observed raw-ledger results for 188 owner-disjoint repositories and 3,760 machine-validated targets. Costs are recorded incremental fallback costs in USD, not current provider prices.",
        "",
        "| Route | Role | Correct / 3,760 | Accuracy | Fallback calls | Cost (USD) | No prediction |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f'| {row["route"]} | {row["role"]} | {row["correct"]:,} | {float(row["accuracy"]) * 100:.2f}% | {row["fallback_calls"]:,} | ${float(row["cost"]):.2f} | {row["no_prediction"]:,} |')
    lines.extend([
        "",
        "Primary owner-clustered comparisons: structure-only exceeded confidence-only by 1.70 percentage points (95% CI 0.45 to 2.95; p = 0.012), exceeded hash-random by 1.30 points (95% CI 0.30 to 2.35; p = 0.018), and was statistically indistinguishable from the full-feature ablation (0.11 points; 95% CI -0.38 to 0.61; p = 0.74).",
    ])
    (OUT / "table_1_owner_disjoint_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    comparisons = summary["primary_comparisons"]
    results_text = f'''# Results Text (Paper-Ready Draft)

On the preregistered owner-disjoint cohort of 188 owners (3,760 machine-validated targets), the structure-aware routing policy recovered {summary["routes"]["structure_only"]["correct"]:,} targets ({summary["routes"]["structure_only"]["accuracy"] * 100:.2f}%). Its recorded incremental fallback cost was ${summary["routes"]["structure_only"]["incremental_fallback_usd"]:.2f}, within the matched $48.00 route cap. Relative to the confidence-only comparator, structure-aware routing improved accuracy by {comparisons["structure_only_minus_confidence_only"]["accuracy_difference_pp"]:.2f} percentage points (owner-clustered 95% CI {comparisons["structure_only_minus_confidence_only"]["ci95_pp"][0]:.2f} to {comparisons["structure_only_minus_confidence_only"]["ci95_pp"][1]:.2f}; p = {comparisons["structure_only_minus_confidence_only"]["p_value"]}). It also exceeded the hash-random replay baseline by {comparisons["structure_only_minus_hash_random"]["accuracy_difference_pp"]:.2f} percentage points (95% CI {comparisons["structure_only_minus_hash_random"]["ci95_pp"][0]:.2f} to {comparisons["structure_only_minus_hash_random"]["ci95_pp"][1]:.2f}; p = {comparisons["structure_only_minus_hash_random"]["p_value"]}). The difference between structure-aware routing and the full-feature ablation was not distinguishable from zero ({comparisons["structure_only_minus_full"]["accuracy_difference_pp"]:.2f} percentage points; 95% CI {comparisons["structure_only_minus_full"]["ci95_pp"][0]:.2f} to {comparisons["structure_only_minus_full"]["ci95_pp"][1]:.2f}; p = {comparisons["structure_only_minus_full"]["p_value"]}).

Interpretation: these results support the structure-aware policy relative to the prespecified confidence-only and hash-random comparators. They do not establish that adding the full feature set improves on the structure-only policy.
'''
    (OUT / "results_text_draft.md").write_text(results_text, encoding="utf-8")
    write_svg(rows)

    report = {
        "status": "PASS" if passed else "FAIL",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": "Local SHA-256 manifest validation and summary-consistency checks only; no network or model calls.",
        "bundle": str(BUNDLE.relative_to(ROOT)),
        "sha256_checks": checks,
        "semantic_checks": required,
        "excluded_from_results": "veritype_cost_constrained_owner_disjoint_confirmation_v2_expected_bundle (expected_simulation_only)",
    }
    (OUT / "integrity_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = ["# Local Integrity Report", "", f'**Status:** {report["status"]}', "", report["scope"], "", "## SHA-256 checks", "", "| Artifact | Result |", "|---|---|"]
    markdown.extend(f'| {entry["artifact"]} | {"PASS" if entry["passed"] else "FAIL"} |' for entry in checks)
    markdown.extend(["", "## Semantic checks", "", "| Check | Result |", "|---|---|"])
    markdown.extend(f'| {name} | {"PASS" if value else "FAIL"} |' for name, value in required.items())
    markdown.append("\nThe simulation-only expected bundle was excluded from all generated Results artifacts.")
    (OUT / "integrity_report.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    if not passed:
        raise SystemExit("Integrity validation failed; paper artifacts were not trustworthy.")


if __name__ == "__main__":
    main()
