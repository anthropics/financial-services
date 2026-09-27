---
name: methodology
description: "Explain what the ACI Risk Indicator methodology fields mean and where the methodology is published. Use when the user asks how ACI Risk Indicators are produced, what a field like confidence, hard caps, or certification date means, or what the ACI Framework version is. Points to the published methodology; never summarises or reconstructs it."
---

# ACI Methodology Reference

The ACI methodology is published at https://aethoncredit.com/methodology, and every tool result links it in `methodology_url`. For anything beyond the fields below, point the user there. Do not summarise, reconstruct, or explain the methodology yourself.

- **Framework.** ACI Framework v1.0. `get_risk_score` returns it in `methodology_version`.
- **Nature of the output.** ACI Risk Indicators are model-derived quantitative analytics outputs, produced from defined inputs and publicly available data. They are not a credit rating, not a credit opinion, and not advice.
- **Determinism.** Risk Indicator calculations are deterministic when the approved inputs, methodology version and configuration are held constant.

## The fields, as returned

- `score`: the indicator value, 0–100. Bands: LOW 80–100, MEDIUM 60–79, ELEVATED 40–59, HIGH 0–39.
- `criterion_scores`: per criterion, its `label`, value (`score`), `weight`, `weighted_contribution` (rounded, so contributions need not add up to the indicator value), `confidence`, `worst_case_applied`, `applicability` and `bucket`.
- `hard_caps_applied`: the hard caps the methodology applied.
- `confidence_level`: the confidence recorded with the indicator.
- `last_certified`: the date recorded for the indicator's certification, or null.
- `stress_classification`: a stored classification, where one exists.

Report each field as returned. Supply no reason, driver, or cause for any value, band, cap, or criterion. Direct any request to explain *why* a value is what it is to the published methodology.

---

*ACI Framework v1.0 · aethoncredit.com · Quantitative risk analytics outputs for independent analysis*
