---
name: methodology-ledger
description: Retrieve and interpret the Phronesis methodology ledger — version-attributed reasoning chains, substrate provenance per forecast, ensemble composition, and the audit trail from input substrate to emitted distribution. Use when an agent needs to audit a specific forecast's reasoning, replicate a forecast, or compare methodology versions across forecasts. Cross-vertical capability.
---

# Phronesis Methodology Ledger

You are retrieving and interpreting the Phronesis public methodology ledger. The methodology ledger is the **reasoning-chain audit surface**: every emitted forecast links to a methodology version + substrate provenance chain + ensemble composition + reasoning trace. Sprint 5.19+ first publication; live at `https://phronesis-jrstinehour.replit.app/methodology-ledger`.

## Core Principles

- **Methodology versioning is semver.** Phronesis methodology versions are `<ring>.<major>.<minor>.<patch>`. Major bumps = ensemble recomposition. Minor bumps = substrate addition. Patch = bug fix.
- **Every forecast cites its methodology version.** When you call `phronesis_forecast_query`, the response includes `methodology_version`. The ledger is the lookup table from version → reasoning chain.
- **Substrate provenance is load-bearing.** Each methodology version lists which substrate sources contributed (e.g., V#1.3.2 = EIA + FERC + CAISO ISO + NREL + Athena ring research) and at what weight.
- **Ensemble composition is disclosed.** Forecasts are not from a single model; they are ensembles of (a) structural models, (b) statistical baselines, (c) LLM-reasoned scenarios. The ledger discloses the mix per version.
- **Reproducibility is a moat.** A user with the same methodology version + same substrate snapshot + same query should be able to approximate the same distribution. Full reproducibility is roadmap-pending; partial replication is currently feasible via ledger.

## Available MCP Tools

- **`phronesis_methodology_ledger`** — Retrieve methodology version detail. `{methodology_version}` returns full reasoning chain + substrate manifest + ensemble composition.
- **`phronesis_forecast_query`** — Cross-link to a specific forecast; useful for tracing "this forecast came from which methodology version?"
- **`phronesis_calibration_scorecard`** — Cross-link to scorecard slice for the methodology version (how did forecasts at version V calibrate post-realization?).

## Query Patterns

1. **Look up methodology version** — Forecast response cited version `energy.v1.3.2`. `phronesis_methodology_ledger({methodology_version: "energy.v1.3.2"})`.
2. **Compare methodology versions** — User asks why a current forecast differs from a prior. Retrieve both versions' ledger entries; diff substrate + ensemble.
3. **Substrate audit** — User asks which sources fed a forecast. Retrieve ledger; surface substrate manifest.
4. **Ensemble disclosure** — User asks how heavily LLM-reasoning weighs vs structural model. Retrieve ledger; surface ensemble composition.
5. **Reproducibility check** — User wants to validate a forecast independently. Retrieve ledger; surface substrate snapshot timestamp + ensemble seed (where applicable).

## Tool Chaining Workflow

1. **Identify the version** — from a forecast response, from a user-supplied version string, or by listing recent versions for a ring.
2. **Call `phronesis_methodology_ledger`** with the version.
3. **Optional: Cross-link calibration** — pull `phronesis_calibration_scorecard` filtered to this methodology version to show post-realization Brier.
4. **Synthesize** — substrate manifest + ensemble composition + reasoning chain summary.

## Output Format

### Methodology Version
- **Version**: `<ring>.<major>.<minor>.<patch>`
- **Active since**: `<date>`
- **Superseded by**: `<version or null>`
- **Ring**: V#1-V#8

### Substrate Manifest
| Source | Type | Weight | Snapshot timestamp |
|--------|------|--------|--------------------|
| EIA | structural-data | 0.35 | ... |
| FERC | regulatory-data | 0.15 | ... |
| Athena Ring (arXiv) | research | 0.20 | ... |
| ... | ... | ... | ... |

### Ensemble Composition
| Model class | Weight | Notes |
|-------------|--------|-------|
| Structural (EIA-aligned) | 0.40 | ... |
| Statistical baseline | 0.25 | ... |
| LLM-reasoned scenarios | 0.20 | ... |
| Cross-ring evidence | 0.15 | ... |

### Reasoning Chain Summary
2-5 paragraphs: how this methodology version reasons through the question class. Cite the public methodology-ledger URL for the full reasoning trace.

### Calibration Cross-Link
| Brier (this version, post-realization) | CRPS (this version) | n evaluated | Reliability |
|-----------------------------------------|---------------------|-------------|-------------|
| ... | ... | ... | ... |

## Disclaimer

The methodology ledger is the reasoning-chain audit surface, not investment advice. Methodology versions evolve; superseded versions remain in the ledger for audit + retrospective evaluation. Use the ledger to understand a forecast, not to replicate it deterministically — substrate snapshots drift, and even with the same version + snapshot, ensemble stochasticity can produce minor distribution shifts.
