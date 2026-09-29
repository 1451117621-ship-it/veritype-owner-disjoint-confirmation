# VeriType owner-disjoint v2 observed evidence bundle

This directory contains the author-confirmed observed raw ledgers for the machine-only owner-disjoint matched-budget v2 experiment.

Evidence boundary:
- The JSONL ledgers are treated as `observed_raw_ledger` because the authors identify the source bundle as observed experiment data.
- `audit_summary.json` recomputes cohort size, provider outcomes, route counts, fallback calls, costs, and machine-gold validity from local files.
- The audit performs no network requests and no model calls.

Files:
- `machine_gold_ledger.observed_raw_ledger.jsonl`
- `provider_outcomes_primary.observed_raw_ledger.jsonl`
- `provider_outcomes_fallback.observed_raw_ledger.jsonl`
- `per_target_route_results.observed_raw_ledger.jsonl`
- `cost_ledger.observed_raw_ledger.jsonl`
- `source_summary.observed.json`
- `audit_summary.json`
- `sha256.json`
