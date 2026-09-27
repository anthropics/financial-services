---
name: risk-check
description: "Look up the ACI Risk Indicator for one digital asset yield provider through the Aethon Credit Intelligence connector. Use when the user asks for a provider's risk band, indicator value, hard caps, confidence, certification date, or the full per-criterion breakdown. Reports only the fields the ACI tools return; never estimates, infers, or explains a value."
---

# ACI Risk Check

Look up one digital asset yield provider's ACI Risk Indicator through the Aethon Credit Intelligence connector (`https://mcp.aethoncredit.com/mcp`).

ACI Risk Indicators are model-derived quantitative analytics outputs under the ACI Framework v1.0. Every result carries the classification anchor in `classification_anchor`; end every answer that shows ACI output with it.

## Workflow

The connector checks the user's plan on every call.

- **Professional and above:** call `get_risk_score` with the provider's `provider_slug` or `provider_name`. If nothing is found, call `search_providers` with the name as `query` and show the matches.
- **Below Professional (Sandbox, Analyst, not signed in):** call `search_providers` with the name as `query`; report name, module and risk band only. Calling `get_risk_score` while not signed in starts sign-in.
- **For the breakdown (Professional and above):** call `get_provider_detail` with the `provider_slug`.

## Reporting

`get_risk_score` returns `provider_name`, `module`, the indicator value (`score`), `risk_band`, `hard_caps_applied`, `confidence_level`, `last_certified` and `methodology_version`. `get_provider_detail` adds `criterion_scores` (per criterion: `label`, value, `weight`, `weighted_contribution`, `confidence`, `worst_case_applied`, `applicability`, `bucket`) and `stress_classification`.

- Report only the fields in `data`. ACI returns no reasons, drivers or explanations; supply none of your own.
- Report `risk_band` as returned. Never derive a band from a value, and never move a provider to a neighbouring band. If `risk_band` is null, report no band.
- If a result shows the band only, give the band only. Never estimate or infer an indicator value.
- Weighted contributions are rounded per criterion, so they need not add up to the indicator value. Do not explain the difference.
- Report `last_certified` as returned; if it is null, say no certification is recorded for the indicator.
- Report `hard_caps_applied` and `stress_classification` as returned, without explaining them.
- Report a refusal as returned. If it names a plan, point the user to https://aethoncredit.com/pricing.

Never call an ACI Risk Indicator a rating or a credit opinion, and never turn it into advice, a recommendation, or a view on whether to buy, sell, or hold.

---

*ACI Framework v1.0 · aethoncredit.com · Quantitative risk analytics outputs for independent analysis*
