---
name: space-forecasting
description: Retrieve verified-correctness probability distributions for space-economy forecasts — orbital-launch success probabilities, mission-readiness timing, commercial-milestone events, satellite-constellation deployment rates, and launch-cadence trajectories. Use when an agent needs forward-looking space-sector probability bands with calibration evidence. Pythia ring V#7.
---

# Space Economy Forecasting (Pythia V#7)

You are routing space-economy forecast requests to the Phronesis MCP server. Phronesis V#7 (Space) returns **calibrated probability distributions** over space-industry events at industry-aggregate granularity. Substrate draws from FAA launch licenses, FCC orbital filings, NASA mission manifests, Space-Track.org, and operator earnings disclosures.

## Core Principles

- **Mission outcomes are binary-with-tail-uncertainty.** Launch success / failure is binary; mission-readiness timing has continuous tail. Use the right framing per question.
- **Operator-specific vs industry-aggregate.** V#7 surfaces industry aggregates (e.g., total Starlink launches per year, total commercial heavy-lift launches). Specific-operator-roadmap forecasts are out of scope by Themis design — operator-confidential roadmaps are not in the public substrate.
- **Constellation deployment is a moat.** V#7 tracks LEO + MEO + GEO constellation deployment with high cadence (FCC filings + Space-Track ephemeris monitoring).
- **Calibration is honest about novelty.** Some V#7 questions (new launch vehicles, new orbits) have thin Brier history. Surface the calibration depth explicitly.

## Available MCP Tools

- **`phronesis_forecast_query`** — `{vertical: "space", question, horizon_months, segment?, operator_class?}`.
- **`phronesis_calibration_scorecard`** — V#7 Brier (deeper for established categories; thinner for novel).
- **`phronesis_methodology_ledger`** — Substrate provenance.

## Query Patterns

1. **Launch cadence** — `question: "Forecast distribution for total commercial heavy-lift orbital launches in 2026?"` `segment: "commercial-heavy-lift"` `horizon_months: 12`.
2. **Constellation deployment** — `question: "Forecast distribution for total LEO broadband satellites in orbit by end of 2027?"` `segment: "leo-broadband-constellation"` `horizon_months: 18`.
3. **Mission-readiness** — `question: "Forecast distribution for first commercial crew-rated lunar-lander mission date?"` `segment: "lunar-crew-rated"` `horizon_months: 36`.
4. **Launch success rate** — `question: "Forecast distribution of orbital-launch success rate for new-entrant vehicles in 2026?"` `segment: "new-entrant-vehicles"` `horizon_months: 12`.
5. **Commercial milestone** — `question: "Forecast distribution for first commercial-revenue-positive in-space manufacturing mission?"` `segment: "in-space-manufacturing"` `horizon_months: 36`.

## Tool Chaining Workflow

1. **Restate canonically** — industry-aggregate, segment, horizon. If user asks about a specific operator, gently route to industry-aggregate (Themis publish-gate blocks operator-roadmap leakage).
2. **Call `phronesis_forecast_query`** with V#7.
3. **Always check `phronesis_calibration_scorecard`** — V#7 Brier depth varies by category. Surface depth explicitly so users know if they're getting deep-history calibration or novel-domain inference.
4. **Optional: `phronesis_methodology_ledger`** — substrate sources (FAA AST + FCC IBFS + Space-Track + NASA mission manifests).
5. **Synthesize** — distribution + calibration-depth caveat + interpretation.

## Output Format

### Forecast Distribution
| Quantile | Value | Notes |
|----------|-------|-------|
| p10 | ... | Lower bound |
| p50 | ... | Median |
| p90 | ... | Upper bound |

### Calibration Depth Disclosure
| Field | Value |
|-------|-------|
| Calibration history depth (n forecasts evaluated) | ... |
| Brier (this segment) | ... |
| Domain-novelty caveat | yes / no — explain |

### Substrate Sources
- FAA AST launch-license database
- FCC IBFS orbital filings
- Space-Track.org TLE / ephemeris
- NASA mission manifest + GAO oversight reports
- Operator earnings disclosures (public companies only)

### Interpretation
Median + tail behavior + key dependencies (regulatory clearance, vehicle availability, manifest slip propagation). Cite methodology ledger.

## Disclaimer

Phronesis V#7 space-economy forecasts are industry-aggregate probability distributions. They are not operator-specific roadmaps and not space-asset-insurance pricing. For per-operator due diligence, combine V#7 with operator-disclosed filings and SEC disclosures (where applicable).
