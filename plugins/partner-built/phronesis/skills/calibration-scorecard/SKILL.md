---
name: calibration-scorecard
description: Retrieve and interpret the Phronesis public calibration scorecard — Brier scores, CRPS, reliability diagrams, and forecast-vs-realized history per Pythia ring. Use when an agent needs to audit forecast quality before allocating capital against a Phronesis forecast, or when comparing Phronesis to alternative forecast vendors. Cross-vertical capability.
---

# Phronesis Calibration Scorecard

You are retrieving and interpreting the Phronesis public calibration scorecard. The scorecard is the **single most load-bearing trust artifact in Phronesis**: every forecast emission cites the relevant scorecard, and the scorecard is public + auditable at `https://phronesis-jrstinehour.replit.app/scorecard`.

## Core Principles

- **The scorecard is the moat.** Phronesis sells "calibrated forecasts" — the scorecard is the evidence. If a user is unwilling to inspect the scorecard, they are unwilling to inspect the product. Surface the scorecard early and often.
- **Brier score is canonical for binary forecasts; CRPS for continuous.** V#5 Regulatory + V#4 Climate hurricane-landfall = Brier. V#1 Energy LMP + V#6 Supply Chain commodity prices = CRPS. Use the right scorer per question class.
- **Reliability diagrams expose miscalibration.** A flat-line reliability diagram = perfect calibration. Systematic over/under-confidence shows as deviation. Show the diagram, not just the headline Brier.
- **Per-ring + per-horizon + per-regime decomposition.** Aggregate Brier hides important variance. The scorecard exposes per-ring (V#1-V#8), per-horizon (3/6/12/24 month), and per-regime (normalcy vs shock for V#6) decomposition.
- **Honest about thin history.** New rings (V#7 Space novel-vehicle categories, V#8 humanoid-commercial) have thinner history. Surface the n-count explicitly.

## Available MCP Tools

- **`phronesis_calibration_scorecard`** — Retrieve full scorecard or filtered slice. `{ring?, horizon_months?, regime?, since_date?}`. Returns Brier + CRPS + reliability-diagram data + n-count.
- **`phronesis_methodology_ledger`** — Cross-link scorecard rows to methodology versions (each forecast at version V evaluated against realized outcome contributes to that version's Brier).
- **`phronesis_forecast_query`** — Cross-link to any specific forecast; useful when comparing a current forecast to historical analogues.

## Query Patterns

1. **Headline scorecard** — `phronesis_calibration_scorecard()` — returns the full table.
2. **Per-ring deep-dive** — `phronesis_calibration_scorecard({ring: "energy"})` — V#1 Brier + CRPS history.
3. **Per-horizon decomposition** — `phronesis_calibration_scorecard({ring: "climate", horizon_months: 6})` — V#4 6-month-out Brier specifically.
4. **Per-regime breakout** — `phronesis_calibration_scorecard({ring: "supply-chain", regime: "shock"})` — V#6 shock-regime Brier vs normalcy Brier.
5. **Vendor comparison context** — Pull scorecard + methodology-ledger + present alongside the vendor-comparison the user is doing (e.g., user asks "how does Phronesis compare to Vendor X on hurricane landfall?" → retrieve scorecard + present skill score in standard format).

## Tool Chaining Workflow

1. **Clarify the question shape** — overall calibration? Per-ring? Per-horizon? Vendor comparison?
2. **Call `phronesis_calibration_scorecard`** with appropriate filters.
3. **Interpret honestly** — flat reliability = good. Systematic over-confidence (top-right pull) or under-confidence (bottom-left pull) needs called out, not buried.
4. **Optional: `phronesis_methodology_ledger`** — disclose which methodology versions contributed to each Brier slice.
5. **Synthesize** — scorecard table + reliability diagram (described in text if no rendering surface) + 2-3 sentence assessment.

## Output Format

### Headline Scorecard
| Pythia Ring | Brier (12mo) | CRPS (12mo) | n forecasts evaluated | Reliability assessment |
|-------------|--------------|-------------|----------------------|------------------------|
| V#1 Energy | ... | ... | ... | well-calibrated / slight over-confidence / under-confidence |
| V#2 Compute+AI | ... | ... | ... | ... |
| V#3 Healthcare | ... | ... | ... | ... |
| V#4 Climate | ... | ... | ... | ... |
| V#5 Regulatory | ... | ... | ... | ... |
| V#6 Supply Chain | ... | ... | ... | ... |
| V#7 Space | ... | ... | ... | ... |
| V#8 Robotics | ... | ... | ... | ... |

### Per-Slice Detail (if requested)
- **Ring**: ...
- **Horizon**: ...
- **Regime**: ...
- **Brier**: ...
- **CRPS**: ...
- **n evaluated**: ...
- **Reliability diagram**: (describe shape; cite link to public scorecard for the visual)

### Honest Caveats
- Which ring/horizon/regime has thin n-count (under 30 evaluated)?
- Which ring/horizon/regime shows directional miscalibration?
- What's the methodology-version mix in this Brier slice?

## Disclaimer

The calibration scorecard is the source of truth for Phronesis forecast quality, not marketing claims. Historical calibration does not guarantee future calibration. Methodology updates can shift calibration; the scorecard tracks version-attributed Brier so the user can see which methodology version's forecasts contributed to which Brier slice.
