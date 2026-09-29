# VeriType: Owner-Disjoint Confirmation Evidence Package

This repository is a compact, publishable package for the VeriType owner-disjoint, matched-budget Java type-recovery confirmation experiment. It deliberately contains only the observed evidence bundle, its SHA-256 manifest, paper-ready Results artifacts, the frozen experiment configuration, and the standard-library generation tool.

## Scope

- Cohort: 188 owner-disjoint source owners and 3,760 machine-validated Java type-recovery targets.
- Primary result: the structure-aware route recovered 3,147/3,760 targets (83.70%) and exceeded the confidence-only comparator by 1.70 percentage points (owner-clustered 95% CI 0.45 to 2.95; p = 0.012).
- Boundary: the full-feature ablation was statistically indistinguishable from the structure-aware route. The evidence supports the structure-aware method, not a claim that the full feature set is superior.
- Recorded cost: the structure-aware route used 2,155 fallback calls and $47.86 of recorded incremental fallback cost, within the $48.00 matched route cap.

## Included Evidence

`experiments/exp001_mvp/tables/veritype_cost_constrained_owner_disjoint_confirmation_v2_observed_bundle/` contains the observed machine-gold, provider-outcome, route, and cost ledgers. Its `sha256.json` manifest binds each included evidence file.

`experiments/exp001_mvp/tables/veritype_cost_constrained_owner_disjoint_confirmation_v2_paper_results_v1/` contains the local integrity report, Table 1 in Markdown and CSV, a paper-ready Results paragraph, and an editable SVG figure.

The `expected_bundle` and simulation-planning directories are intentionally excluded: they are not Results evidence.

## Reproduce the Local Check

The package uses only the Python standard library:

```bash
python3 tools/build_veritype_confirmatory_results.py
```

The command recomputes SHA-256 values for every manifest-listed observed artifact, checks the summary/audit consistency conditions, and regenerates the table, figure, Results draft, and integrity reports. It makes no network or model calls.

## Exclusions

No API keys, `.env` files, LLM response caches, transport captures, prompts, source archives, or raw model responses are included. These materials are intentionally kept outside this publication-oriented repository.
