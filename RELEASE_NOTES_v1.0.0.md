# VeriType Confirmation Evidence Package v1.0.0

## What This Release Freezes

This release freezes the compact evidence package for the owner-disjoint, matched-budget confirmation experiment. It contains observed raw ledgers, their SHA-256 manifest, a local integrity report, a paper-ready Results table and figure, and the standard-library generator used to regenerate those presentation artifacts.

## Main Result

On 3,760 machine-validated targets from 188 owner-disjoint owners, the structure-aware policy recovered 3,147 targets (83.70%). It exceeded the confidence-only comparator by 1.70 percentage points (owner-clustered 95% CI 0.45 to 2.95; p = 0.012) and the hash-random replay baseline by 1.30 points (95% CI 0.30 to 2.35; p = 0.018). It was not distinguishable from the full-feature ablation (0.11 points; 95% CI -0.38 to 0.61; p = 0.74).

## Verification

Run:

```bash
python3 tools/build_veritype_confirmatory_results.py
```

The command recomputes SHA-256 values for all manifest-listed observed artifacts and regenerates the Results materials without network or model calls.

## Evidence Boundary

- Results are based only on the observed raw-ledger bundle.
- The expected/simulation bundle is excluded and must not be cited as Results evidence.
- Costs are recorded experiment costs, not current provider price quotations.
- The machine-gold endpoint is exact source-declaration reconstruction and binding preservation; this release does not claim human semantic acceptability or downstream runtime equivalence.

## Deliberate Exclusions

No credentials, LLM response caches, transport captures, prompts, source archives, or raw model responses are distributed in this repository.
