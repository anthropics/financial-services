---
name: phronesis
description: |
  Cross-vertical, p10/p50/p90-banded forward forecasts via the Phronesis MCP — useful when financial analysis needs verified-correctness forecast inputs across 8 verticals (energy, compute/AI, healthcare, climate, regulatory, supply-chain, space, robotics) with calibration-scorecard-attributed confidence bands and methodology-ledger citations.

  **Use when:**
  - Building a model that needs a forward-looking input (revenue driver, cost curve, regulatory timeline, technology adoption rate) where a single point estimate undersells the uncertainty
  - Cross-vertical analysis (e.g., energy-transition × supply-chain bottlenecks, AI infra × compute demand)
  - DCF terminal-value assumptions that need defensible uncertainty bands
  - Scenario analysis with calibrated probability distributions

  **Not ideal for:**
  - Backward-looking historical financial data (use S&P Global / FactSet / Daloopa instead)
  - Single-company forecasts (Phronesis returns vertical-level + archetype-level forecasts; combine with company-specific MCP data for company-level outputs)
  - Sub-monthly time horizons (Phronesis cadence is monthly+ for most verticals)
---

# Phronesis Forecasting MCP

## Overview

The Phronesis MCP returns **verified-correctness forecasts** with p10/p50/p90 uncertainty bands across 8 verticals. Each forecast carries a Calibration Scorecard reference (transparency about historical forecast accuracy per vertical) and methodology ledger citations (which data sources, model versions, and reasoning chains produced the forecast).

Provided by **Sustainable Finance Partners, LLC** (Phronesis is the SFP product brand for the energy-transition agent constellation).

## Verticals covered (8/8 LIVE)

| Vertical | Phronesis ring | Example forecast targets |
|---|---|---|
| V#1 Energy | `pythia/energy/` | Solar PPA pricing, battery cost curves, grid demand |
| V#2 Compute / AI | `pythia/compute/` | GPU price trends, datacenter capacity, AI workload mix |
| V#3 Healthcare | `pythia/healthcare/` | Drug approval timelines, payer mix shifts, M&A pipeline |
| V#4 Climate | `pythia/templates/climate/` | Catastrophe loss projections, transition risk timelines |
| V#5 Regulatory | `pythia/templates/regulatory/` | IRA tax credit utilization, state RPS trajectories, agency rulemaking |
| V#6 Supply-Chain | `pythia/templates/supply_chain/` | Lithium / nickel / cobalt mint forecasts, manufacturing capacity |
| V#7 Space | `pythia/space/` | Launch cadence, satellite-constellation deployments |
| V#8 Robotics | `pythia/robotics/` | Robotic-system unit economics, deployment density |

## Calling pattern

Phronesis MCP exposes Hermes Tier-1 tools. The forecast intake is `forecast_submit` (returns a forecast for a given subject + archetype + horizon + geography). Read the Calibration Scorecard at the public attribution URL to gauge per-vertical historical accuracy before relying on a forecast in a model.

**Public Calibration Scorecard:** [phronesis-jrstinehour.replit.app/scorecard.json](https://phronesis-jrstinehour.replit.app/scorecard.json) — JSON-formatted; each row shows historical forecast accuracy per vertical × archetype × horizon.

## Output shape

Every Phronesis forecast carries:
- **point_forecast**: `{value, units, as_of_date}`
- **uncertainty_band**: `{p10, p50, p90}` — institutional-grade banded estimates, NOT single-point
- **caveats**: bracketed CAVEAT codes (e.g., `TRAINING_DATA_CUTOFF`, `LIMITED_HISTORY`) — these matter; surface them in any analysis using the forecast
- **rationale**: methodology ledger citation + reasoning chain

## Pricing model

Subscription-gated runtime access per Phronesis Tier 1-6 monetization stack (canonical model alongside Moody's MCP, FactSet MCP, S&P Global MCP). MCP submission to this repo is free under Apache 2.0.

## When to combine with other MCPs in this plugin

- **Pair with S&P Global / FactSet / Daloopa**: pull historical financials there, layer Phronesis forecasts as forward inputs in your model
- **Pair with Moody's**: forecast vertical fundamentals (Phronesis) + credit/risk overlay (Moody's)
- **Pair with PitchBook / Aiera**: investor-context (PitchBook) + earnings-context (Aiera) + forward forecast (Phronesis) = full triangulation
- **Pair with LSEG**: macro/rates (LSEG) + vertical-deep forecasts (Phronesis)

---

*Copyright 2026 Sustainable Finance Partners, LLC. Licensed under Apache 2.0. MCP runtime access subscription-gated per Phronesis Tier 1-6 monetization stack.*
