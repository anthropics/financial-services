---
name: robotics-forecasting
description: Retrieve verified-correctness probability distributions for robotics forecasts — humanoid-robot commercial deployment timing, industrial-robot installation rates, autonomous-mobile-robot fleet sizes, surgical-robot adoption curves, and robotics unit-cost trajectories. Use when an agent needs forward-looking robotics-sector probability bands with calibration evidence. Pythia ring V#8.
---

# Robotics Forecasting (Pythia V#8)

You are routing robotics forecast requests to the Phronesis MCP server. Phronesis V#8 (Robotics) returns **calibrated probability distributions** over robotics-industry events at category-aggregate granularity. Substrate draws from IFR (International Federation of Robotics), industrial-automation trade press, surgical-robot installation registries, and public-company robotics-segment disclosures.

## Core Principles

- **Adoption curves dominate the question shape.** Robotics forecasts are typically "when does category X reach milestone Y?" or "what is the install-base of category X at time T?". Cast questions in adoption-curve framing.
- **Category granularity matters.** Industrial articulated arms, AMRs, humanoids, surgical robots, autonomous trucks — each is a distinct category with distinct Brier history. Always specify category.
- **Humanoid commercial deployment is a high-attention category.** V#8 tracks humanoid commercial deployment with explicit calibration; the distribution is wide and the methodology ledger discloses why.
- **Unit-cost trajectories are first-class.** V#8 surfaces per-category unit-cost decline curves (learning-rate Wright's-law style) with calibration scorecard attached.

## Available MCP Tools

- **`phronesis_forecast_query`** — `{vertical: "robotics", question, horizon_months, category, geography?, metric?}`.
- **`phronesis_calibration_scorecard`** — V#8 Brier per category.
- **`phronesis_methodology_ledger`** — Substrate provenance.

## Query Patterns

1. **Humanoid commercial deployment** — `question: "Forecast distribution for cumulative commercial humanoid-robot deployments (paid-deployment unit count) by end of 2027?"` `category: "humanoid-commercial"` `metric: "cumulative-paid-deployments"` `horizon_months: 18`.
2. **Industrial install rate** — `question: "Forecast distribution for global industrial-robot annual installations in 2026?"` `category: "industrial-articulated"` `metric: "annual-installations"` `geography: "global"` `horizon_months: 12`.
3. **AMR fleet** — `question: "Forecast distribution for U.S. warehouse AMR install-base by end of 2027?"` `category: "amr-warehouse"` `metric: "installed-base"` `geography: "US"` `horizon_months: 18`.
4. **Surgical robotics** — `question: "Forecast distribution for global da Vinci-class surgical-robot annual procedure count in 2027?"` `category: "surgical-robot"` `metric: "annual-procedures"` `geography: "global"` `horizon_months: 18`.
5. **Unit-cost trajectory** — `question: "Forecast distribution for humanoid-robot BoM cost in 2028 (median commercial unit)?"` `category: "humanoid-commercial"` `metric: "bom-cost-median"` `horizon_months: 30`.

## Tool Chaining Workflow

1. **Restate canonically** — category, metric, geography, horizon. Adoption-curve framing.
2. **Call `phronesis_forecast_query`** with V#8.
3. **Optional: `phronesis_calibration_scorecard`** — per-category Brier. Humanoid category has shorter history; disclose explicitly.
4. **Optional: `phronesis_methodology_ledger`** — IFR + trade-press + public-company segment-disclosure substrate.
5. **Synthesize** — distribution + adoption-curve interpretation + cost-trajectory reference (when relevant).

## Output Format

### Forecast Distribution
| Quantile | Value | Notes |
|----------|-------|-------|
| p10 | ... | Lower bound |
| p50 | ... | Median |
| p90 | ... | Upper bound |

### Adoption Curve Context
- Current install-base (latest available): ...
- Implied adoption rate at p50: ...% YoY
- Learning-rate (Wright's-law fit, if metric is unit-cost): ...% per doubling
- Calibration depth (n forecasts evaluated, this category): ...

### Substrate Sources
- IFR World Robotics annual reports
- Industrial-automation trade press
- Public-company robotics-segment 10-K / 10-Q disclosures
- Surgical-robot procedure registries (where public)

### Interpretation
What the median adoption rate implies, how the band is shaped (skewed? bimodal?), key triggers (cost-decline inflection, regulatory clearance, ROI threshold crossings). Cite methodology ledger.

## Disclaimer

Phronesis V#8 robotics forecasts are category-aggregate probability distributions. They are not per-company revenue forecasts and not bill-of-materials supplier scorecards. For specific-company deal diligence, combine V#8 with that company's filings + analyst coverage.
