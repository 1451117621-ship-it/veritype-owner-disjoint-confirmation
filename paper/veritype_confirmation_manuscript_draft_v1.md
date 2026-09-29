# Cost-Constrained Structure-Aware Model Escalation for Java Type Recovery

## Methods

### Confirmation Cohort

We evaluated the prespecified routing policies on an outcome-blind, owner-disjoint cohort of 188 source owners. Each owner contributed 20 targets, yielding 3,760 Java type-recovery targets. Automatic retries were disabled. The unit for clustered inference was the owner.

### Machine-Gold Endpoint

The primary endpoint was exact reconstruction of the missing source declaration under a machine-only validation pipeline. A target entered the final cohort only after unique extraction by both javac TypeMirror and Eclipse JDT, dual-engine agreement, original-source compilation, canonical fully qualified name replacement compilation, binding preservation, zero new diagnostics, and zero unresolved bindings. This endpoint establishes exact declaration recovery and machine binding preservation; it does not establish human semantic acceptability or downstream runtime equivalence.

### Routing Policies and Cost Contract

The primary method was the structure-aware escalation policy. Prespecified comparators were confidence-only routing, hash-random replay routing, unusable-only escalation, always-primary, always-fallback, and a full-feature ablation. The principal structure-aware, confidence-only, and full-feature routes were evaluated under matched fallback-call reservations and a $48.00 recorded incremental fallback-cost cap. Costs in this paper are the recorded experiment costs, not current provider prices.

### Analysis and Integrity Checks

We report exact-recovery accuracy, correct predictions, fallback calls, no-prediction counts, and recorded incremental fallback costs. Primary contrasts use owner-clustered confidence intervals and p-values. The published evidence bundle contains raw machine-gold, provider-outcome, per-target route, and cost ledgers. A SHA-256 manifest binds every included artifact; the local audit recomputes cohort size, route counts, costs, and summary consistency without network or model calls.

## Results

The structure-aware policy recovered 3,147 of 3,760 targets (83.70%) at a recorded incremental fallback cost of $47.86, within the $48.00 cap. It required 2,155 fallback calls and produced 360 no-prediction outcomes.

Relative to the confidence-only comparator, structure-aware routing improved exact-recovery accuracy by 1.70 percentage points (owner-clustered 95% CI 0.45 to 2.95; p = 0.012). It also exceeded the hash-random replay baseline by 1.30 percentage points (95% CI 0.30 to 2.35; p = 0.018). Structure-aware routing and the full-feature ablation were practically and statistically close: the difference was 0.11 percentage points (95% CI -0.38 to 0.61; p = 0.74). Therefore, these data support the benefit of structural information for escalation decisions, but do not support a claim that adding the full feature set improves on structure-aware routing.

See `experiments/exp001_mvp/tables/veritype_cost_constrained_owner_disjoint_confirmation_v2_paper_results_v1/table_1_owner_disjoint_results.md` and `figure_1_owner_disjoint_accuracy_cost.svg` for the publication table and figure.

## Threats to Validity

### Endpoint Scope

The endpoint is deliberately narrow: exact source declaration recovery and machine binding preservation. Compile success alone was not counted as semantic validity. We did not conduct human semantic review, runtime behavior testing, or a claim of semantic equivalence.

### Provider and Cost Drift

The evidence represents recorded behavior of the primary and fallback providers at the experiment time. Provider models, transport behavior, and public pricing can change. The cost values are retained as experiment accounting records and should not be interpreted as live cost quotations.

### Cohort Generalization

Owner-disjoint sampling reduces direct repository overlap between owners, but the results remain limited to the selected public Java source population and to this machine-gold eligibility pipeline. They do not automatically generalize to all Java projects, proprietary code, other programming languages, or targets outside the eligibility criteria.

### Evidence Availability

The public package contains the observed ledger-level evidence needed to audit reported cohort counts, routing, costs, and outcomes. It intentionally excludes source archives, prompts, provider transport captures, model response caches, and credentials. Consequently, the published package supports ledger-level verification rather than a future replay of third-party model APIs.

## Data and Artifact Availability

The evidence package is available at https://github.com/1451117621-ship-it/veritype-owner-disjoint-confirmation. The observed bundle is accompanied by a SHA-256 manifest and a local integrity report. The expected/simulation bundle is deliberately absent from this repository and must not be cited as Results evidence.
