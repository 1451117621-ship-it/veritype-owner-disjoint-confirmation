# Table 1. Owner-Disjoint Matched-Budget Confirmation Results

Observed raw-ledger results for 188 owner-disjoint repositories and 3,760 machine-validated targets. Costs are recorded incremental fallback costs in USD, not current provider prices.

| Route | Role | Correct / 3,760 | Accuracy | Fallback calls | Cost (USD) | No prediction |
|---|---|---:|---:|---:|---:|---:|
| always_primary | single-model baseline | 2,310 | 61.44% | 0 | $0.00 | 1,220 |
| always_fallback | single-model baseline | 2,914 | 77.50% | 3,760 | $74.50 | 628 |
| unusable_only | operational baseline | 3,008 | 80.00% | 1,220 | $27.10 | 360 |
| confidence_only | primary comparator | 3,083 | 82.00% | 2,140 | $47.82 | 360 |
| hash_random | replay baseline | 3,098 | 82.39% | 2,145 | $47.84 | 360 |
| structure_only | primary method | 3,147 | 83.70% | 2,155 | $47.86 | 360 |
| full | secondary ablation | 3,143 | 83.59% | 2,160 | $47.91 | 360 |

Primary owner-clustered comparisons: structure-only exceeded confidence-only by 1.70 percentage points (95% CI 0.45 to 2.95; p = 0.012), exceeded hash-random by 1.30 points (95% CI 0.30 to 2.35; p = 0.018), and was statistically indistinguishable from the full-feature ablation (0.11 points; 95% CI -0.38 to 0.61; p = 0.74).
