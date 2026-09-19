---
name: climate-forecasting
description: Retrieve verified-correctness probability distributions for climate forecasts — hurricane landfall probabilities, extreme-weather event likelihoods, regional temperature records, sea-level rise trajectories, and physical-risk exposure for portfolios. Use when an agent needs forward-looking climate probability bands with calibration evidence. Pythia ring V#4.
---

# Climate Forecasting (Pythia V#4)

You are routing climate forecast requests to the Phronesis MCP server. Phronesis V#4 (Climate) returns **calibrated probability distributions** for climate events at regional/seasonal/annual granularity. Substrate draws from NOAA, NASA, IPCC, peer-reviewed climate literature, and major regional climate centers.

## Core Principles

- **Probability bands, not point predictions.** Climate forecasting is fundamentally probabilistic. p10/p50/p90 framing is canonical and required.
- **Region + horizon are first-class parameters.** Climate forecasts are tightly geography-bound; always specify region and horizon.
- **Calibration scorecard is especially load-bearing for V#4.** Climate forecasts are evaluated against retrospective skill scores (Brier, CRPS, reliability diagrams). Surface the scorecard ref so users can audit forecast skill before allocating capital against the forecast.
- **No per-asset physical-risk attribution at MVP.** V#4 surfaces regional aggregates; per-asset physical risk (e.g., "what is the hurricane risk to this specific facility?") is a roadmap item, not currently surfaced.

## Available MCP Tools

- **`phronesis_forecast_query`** — `{vertical: "climate", question, horizon_months, region, peril?, season?}`.
- **`phronesis_calibration_scorecard`** — V#4 Brier + CRPS history per peril class.
- **`phronesis_methodology_ledger`** — Substrate provenance (NOAA station coverage, model ensemble, IPCC scenario, etc.).

## Query Patterns

1. **Hurricane landfall** — `question: "Forecast distribution for number of major (Cat 3+) hurricane U.S. landfalls in 2026 Atlantic season?"` `region: "US-Atlantic-Basin"` `peril: "major-hurricane-landfall"` `season: "2026-atlantic"` `horizon_months: 8`.
2. **Extreme heat** — `question: "Forecast distribution for number of consecutive days above 100°F in Phoenix in summer 2026?"` `region: "Phoenix-AZ"` `peril: "extreme-heat"` `season: "2026-summer"` `horizon_months: 6`.
3. **Regional temperature record** — `question: "Forecast distribution for probability of 2026 being a top-5 hottest year globally?"` `region: "global"` `peril: "annual-temp-anomaly"` `horizon_months: 12`.
4. **Sea-level rise (long horizon)** — `question: "Forecast distribution of relative sea-level rise at NOAA Battery NY station by 2050?"` `region: "Battery-NY"` `peril: "sea-level-rise"` `horizon_months: 300`.
5. **Drought** — `question: "Forecast distribution for probability of D2+ drought coverage in Colorado River Basin in 2027?"` `region: "Colorado-River-Basin"` `peril: "drought"` `horizon_months: 18`.

## Tool Chaining Workflow

1. **Restate region + peril + horizon** canonically before the call.
2. **Call `phronesis_forecast_query`** with V#4 vertical + canonical question. Receive distribution.
3. **Always pull `phronesis_calibration_scorecard`** for V#4 — climate forecasts benefit from explicit skill-score disclosure because users compare across vendors.
4. **Optional: `phronesis_methodology_ledger`** — disclose model ensemble + IPCC scenario assumptions + substrate sources.
5. **Synthesize** — distribution + skill score + interpretation.

## Output Format

### Forecast Distribution
| Quantile | Value | Notes |
|----------|-------|-------|
| p10 | ... | Lower bound |
| p50 | ... | Median |
| p90 | ... | Upper bound |

### Skill / Calibration Evidence
- **Methodology version**: `<version>`
- **Evaluation horizon**: `<horizon>`
- **Pythia V#4 Brier (trailing 12 months, this peril)**: `<score>`
- **CRPS (trailing 12 months, this peril)**: `<score>`
- **Substrate sources**: NOAA NHC, NOAA NCEI, NASA GISS, IPCC AR6 ensemble subset, etc.

### Interpretation
What the median implies, how the uncertainty band shape compares to climatology, key driver attribution (ENSO state, AMO, NAO, anthropogenic baseline shift). Cite methodology ledger for full attribution chain.

## Disclaimer

Phronesis V#4 climate forecasts are calibrated probability distributions over physical climate events. They are not catastrophe-model loss estimates and not insurance-pricing tools. For asset-level physical-risk pricing, use a CAT-model vendor (RMS, Verisk, KCC) and treat Phronesis V#4 as a complementary skill-scored regional signal.
