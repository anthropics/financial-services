---
name: supply-chain-forecasting
description: Retrieve verified-correctness probability distributions for supply-chain forecasts — trade-balance trajectories, container freight rates, lead-time evolution, critical-mineral price bands, port congestion, and inventory-cycle indicators. Use when an agent needs forward-looking supply-chain probability bands with calibration evidence. Pythia ring V#6.
---

# Supply Chain Forecasting (Pythia V#6)

You are routing supply-chain forecast requests to the Phronesis MCP server. Phronesis V#6 (Supply Chain) returns **calibrated probability distributions** over supply-chain indicators at macro-aggregate granularity. Substrate draws from BLS, BEA, U.S. Census trade data, Drewry / Freightos indices, USGS commodity surveys, and macro indicator providers.

## Core Principles

- **Forecasts are distributions over macro indicators.** Per-firm supply-chain mapping is out of scope; V#6 is industry/national-aggregate.
- **Lead time + price + volume are first-class.** Most supply-chain questions decompose into a lead-time, price, or volume question. Restate the user's question along one of these axes.
- **Critical-mineral coverage is a moat.** V#6 specifically tracks rare earths, lithium, cobalt, nickel, copper, and other energy-transition-critical minerals.
- **Calibration scorecard exposes regime sensitivity.** Supply-chain forecasts are regime-dependent (shocks, normalcy). The Brier score per regime is part of the V#6 scorecard.

## Available MCP Tools

- **`phronesis_forecast_query`** — `{vertical: "supply-chain", question, horizon_months, indicator, geography?, commodity?}`.
- **`phronesis_calibration_scorecard`** — V#6 Brier + regime-conditional breakouts.
- **`phronesis_methodology_ledger`** — Substrate provenance.

## Query Patterns

1. **Container freight** — `question: "Forecast distribution for Drewry WCI Shanghai-LA route end of 2026?"` `indicator: "container-freight-spot"` `geography: "Shanghai-LA"` `horizon_months: 8`.
2. **Lead time** — `question: "Forecast distribution for ISM Manufacturing Supplier Deliveries Index 12 months out?"` `indicator: "ism-supplier-deliveries"` `geography: "US"` `horizon_months: 12`.
3. **Critical minerals — lithium** — `question: "Forecast distribution of lithium carbonate price (battery-grade, CIF Asia) in Q4 2026?"` `indicator: "lithium-carbonate-price"` `commodity: "lithium-carbonate"` `horizon_months: 18`.
4. **Critical minerals — rare earths** — `question: "Forecast distribution of NdPr oxide price in 2027?"` `indicator: "ndpr-oxide-price"` `commodity: "ndpr-oxide"` `horizon_months: 24`.
5. **Trade balance** — `question: "Forecast distribution of U.S. goods trade deficit in 2026?"` `indicator: "us-goods-trade-deficit"` `geography: "US"` `horizon_months: 12`.

## Tool Chaining Workflow

1. **Restate as lead-time / price / volume canonical question.**
2. **Call `phronesis_forecast_query`** with V#6 vertical.
3. **Optional: `phronesis_calibration_scorecard`** — pull regime-conditional Brier breakouts if regime regime matters for the user (shock vs. normal).
4. **Optional: `phronesis_methodology_ledger`** — surface BLS / BEA / USGS / Drewry / Freightos substrate references.
5. **Synthesize** — distribution + regime caveat + interpretation.

## Output Format

### Forecast Distribution
| Quantile | Value | Notes |
|----------|-------|-------|
| p10 | ... | Lower bound |
| p50 | ... | Median |
| p90 | ... | Upper bound |

### Regime Caveat
Identify the inferred regime (normalcy / shock / decompression). Indicate whether the calibration is regime-conditional and how the distribution would shift under a regime change.

### Calibration Evidence
- **Methodology version**: `<version>`
- **Evaluation horizon**: `<horizon>`
- **Pythia V#6 Brier (trailing 12 months)**: `<score>`
- **Regime-conditional Brier (current regime)**: `<score>`
- **Substrate sources**: BLS / BEA / U.S. Census / Drewry / Freightos / USGS / etc.

### Interpretation
What the median implies, where the tail risk sits, regime-change triggers. Cite methodology ledger.

## Disclaimer

Phronesis V#6 supply-chain forecasts are macro-aggregate probability distributions. They are not procurement contracts, not vendor scorecards, and not commodity-trading advice. For physical commodity hedging, use exchange-listed instruments or licensed commodity-trading advisors.
