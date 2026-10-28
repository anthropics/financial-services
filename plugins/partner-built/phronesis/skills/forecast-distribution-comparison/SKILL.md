---
name: forecast-distribution-comparison
description: Compare two or more Phronesis forecast distributions — across time (forecast drift), across methodology versions, across geographies/segments, or against external vendor forecasts. Use when an agent needs to surface how a forecast has shifted, which scenarios diverge, or where Phronesis differs from competitor forecasts. Cross-vertical capability.
---

# Forecast Distribution Comparison

You are comparing two or more Phronesis forecast distributions to surface drift, divergence, or vendor-comparison signal. The output is always two columns of structured comparison + one column of interpretation — let the data show the difference, you synthesize what it means.

## Core Principles

- **Compare distributions, not point estimates.** A median can shift while the band stays the same (forecast confidence unchanged, central tendency shifted), or the band can widen while the median holds (forecast becoming more uncertain). The shape of the change matters.
- **Always use the same scoring rule across comparisons.** Brier vs Brier, CRPS vs CRPS. Cross-rule comparisons are not meaningful.
- **Methodology-version drift is a first-class category of drift.** When the methodology version changes between two Phronesis forecasts of the "same" question, surface the version diff explicitly — the comparison is partly "did the world change" and partly "did the methodology change".
- **Vendor comparison requires honest skill scoring.** Phronesis publishes Brier + CRPS via the scorecard. Compare against vendors that publish equivalent metrics. If a vendor publishes nothing comparable, say so — don't fabricate skill comparisons.

## Available MCP Tools

- **`phronesis_forecast_query`** — Retrieve a forecast distribution (current or historical, depending on `as_of_date` parameter if supported).
- **`phronesis_calibration_scorecard`** — Retrieve scorecard for skill comparison.
- **`phronesis_methodology_ledger`** — Retrieve methodology version detail to characterize methodology-driven drift.

## Comparison Patterns

1. **Forecast drift across time** — same question, two different `as_of_date` values. Surface: median shift + band shift + methodology-version diff.
2. **Methodology-version comparison** — same question, hold the substrate snapshot constant if possible, vary methodology version. Surface: how does the new version reason differently?
3. **Geography / segment comparison** — same question class, different region or segment. Surface: how the forecast varies across the cut.
4. **Vendor comparison** — Phronesis forecast vs external vendor forecast. Surface: Phronesis distribution + vendor distribution + skill score for both (Phronesis Brier from scorecard; vendor skill from vendor's public materials or "unpublished").
5. **Scenario comparison** — Phronesis baseline forecast + alternative scenario forecast (e.g., recession vs base). Surface: how the distribution shifts under the alternative scenario.

## Tool Chaining Workflow

1. **Define the comparison axis** — time / methodology / geography / vendor / scenario.
2. **Pull both (or all) forecasts** via `phronesis_forecast_query`. For time comparison, use `as_of_date` if supported; for vendor comparison, retrieve Phronesis + reference the user-supplied vendor numbers.
3. **Pull skill / calibration evidence** for both via `phronesis_calibration_scorecard` (and vendor's published skill score if available).
4. **Pull methodology-version detail** for both via `phronesis_methodology_ledger` if methodology has changed.
5. **Synthesize** — comparison table + skill comparison + 3-4 sentence interpretation of what the divergence means + what to monitor.

## Output Format

### Comparison Table
| Quantile | Forecast A | Forecast B | Δ (B - A) |
|----------|------------|------------|-----------|
| p10 | ... | ... | ... |
| p50 (median) | ... | ... | ... |
| p90 | ... | ... | ... |
| Band width (p90-p10) | ... | ... | ... |

### Skill Comparison
| | Forecast A | Forecast B |
|---|-----------|------------|
| Methodology version | ... | ... |
| Brier (trailing 12mo, this question class) | ... | ... |
| CRPS (trailing 12mo) | ... | ... |
| n evaluated | ... | ... |

### Methodology-Version Diff (if applicable)
| Component | A version | B version | Change |
|-----------|-----------|-----------|--------|
| Substrate manifest | ... | ... | added/removed/reweighted ... |
| Ensemble composition | ... | ... | ... |
| Reasoning-chain heuristics | ... | ... | ... |

### Interpretation
- **Median shift**: ... bp / units / pct
- **Band shape change**: widened / tightened / asymmetric shift
- **Driver attribution**: substrate update / methodology change / underlying-world change
- **What to monitor next**: ...

## Disclaimer

Forecast distribution comparison surfaces empirical differences between distributions. It does not predict which forecast is "correct" — that is what the calibration scorecard, accumulated over time, eventually answers. Use comparisons to understand drift and uncertainty, not to pick a winner.
