---
name: portfolio-risk
description: "Assess a portfolio of digital asset yield positions through the Aethon Credit Intelligence connector. Use when the user gives a set of providers with weights and wants a composite ACI assessment: composite band, per-provider indicators, concentration and any elevated warnings. Reports only what the tool returns and never proposes an allocation."
---

# ACI Portfolio Risk

Assess a set of weighted digital asset yield positions through the Aethon Credit Intelligence connector (`https://mcp.aethoncredit.com/mcp`). Available on the Professional plan and above.

## Workflow

Call `assess_portfolio_risk` with `allocations`: 2–20 positions, each a `provider_slug` and a `weight`. Each weight is 0.01–1.0, and the weights sum to 1.0 ± 0.01. If you have names rather than slugs, resolve them first with `search_providers`.

The result's `data` holds:

- `composite_score` and `risk_band` for the portfolio.
- `per_provider_scores`: for each position, `provider_slug`, `provider_name`, `module`, indicator value, `risk_band`, `weight`, `weighted_contribution`, `status`.
- `counterparty_concentration_pct`, `custody_concentration_pct`, `regulatory_mix_warning`, `elevated_warnings`, `stress_classification`, `notes`.

## Reporting

- Report only the fields returned. Supply no reasons or drivers of your own.
- A portfolio composite is **not** an ACI Risk Indicator. When you show one, quote:

  > This portfolio assessment is a computed analytical output based on individual provider Risk Indicators. It is not a certified ACI Risk Indicator.

- Report each `risk_band` as returned; if one is null, report no band. Report `elevated_warnings`, `regulatory_mix_warning` and `stress_classification` as returned, without interpreting them.
- Never propose an allocation, a rebalancing, a transaction, or any other action, and never describe one position as better or worse than another. The assessment describes the inputs given; it proposes nothing.

---

*ACI Framework v1.0 · aethoncredit.com · Quantitative risk analytics outputs for independent analysis*
