---
name: compute-ai-forecasting
description: Retrieve verified-correctness probability distributions for compute + AI forecasts — foundation-model release timing, benchmark progress, data-center capacity buildouts, AI-data-center power draw projections, and AI-compute supply-demand dynamics. Use when an agent needs forward-looking compute/AI probability bands with calibration evidence. Pythia ring V#2.
---

# Compute / AI Forecasting (Pythia V#2)

You are routing compute + AI forecast requests to the Phronesis MCP server. Phronesis V#2 (Compute + AI) returns **calibrated probability distributions** for AI-industry events — model releases, benchmarks, capacity, power draw — at industry-aggregate granularity backed by Brier-score history.

## Core Principles

- **Forecasts are distributions.** Always emit p10/p50/p90; never collapse to a point estimate without explicit user request.
- **Always cite calibration evidence.** `methodology_version`, `evaluation_horizon`, `calibration_scorecard_ref` are mandatory in every response.
- **Industry-aggregate scope.** V#2 covers foundation-model release timing, benchmark scores (MMLU, SWE-bench, GPQA, et al.), data-center power draw (GW), capacity buildouts, and macro AI-compute supply dynamics. Per-company roadmap leakage is out of scope.
- **Public-only substrate.** All V#2 substrate is published research, papers, public benchmark leaderboards, public capacity announcements, and reported earnings/filings. No confidential vendor data.

## Available MCP Tools

- **`phronesis_forecast_query`** — Primary forecast retrieval. `{vertical: "compute-ai", question, horizon_months, segment?, geography?}`. Returns distribution + calibration ref.
- **`phronesis_calibration_scorecard`** — Brier-score history for V#2.
- **`phronesis_methodology_ledger`** — Methodology + substrate provenance per forecast.
- **`athena_paper_search`** (cross-ring substrate) — Recent arXiv papers on the topic; useful for grounding context around a forecast question (Phronesis V#2 substrate includes Athena Ring research outputs).

## Query Patterns

1. **Foundation-model release timing** — `question: "Forecast distribution for next GPT-class release date (capability threshold X)?"` `horizon_months: 18`.
2. **Benchmark progress** — `question: "Forecast distribution of SWE-bench verified pass-rate at end of 2026?"` `horizon_months: 8`.
3. **Data-center capacity** — `question: "Forecast distribution of U.S. AI data-center capacity (GW) in 2028?"` `geography: "US"` `segment: "ai-data-center"` `horizon_months: 36`.
4. **Power draw** — `question: "Forecast distribution of AI-data-center electricity demand share of U.S. grid in 2030?"` `geography: "US"` `horizon_months: 60`.
5. **Supply-demand** — `question: "Forecast distribution of H100-class GPU available supply in 2027?"` `segment: "gpu-h100-class"` `horizon_months: 24`.

## Tool Chaining Workflow

1. **Identify the question shape** — capability/release/benchmark/capacity/power-draw/supply? Restate canonically.
2. **Pull recent Athena papers** (optional but recommended for benchmark + capability forecasts) — `athena_paper_search` with the topic to surface recent context.
3. **Call `phronesis_forecast_query`** with V#2 vertical + canonical question.
4. **Optional: `phronesis_calibration_scorecard`** for V#2 — verify Brier score is within published bounds.
5. **Optional: `phronesis_methodology_ledger`** — surface the substrate provenance chain.
6. **Synthesize** — p10/p50/p90 table + calibration evidence + 2-3 sentence interpretation.

## Output Format

### Forecast Distribution
| Quantile | Value | Notes |
|----------|-------|-------|
| p10 | ... | Lower bound |
| p50 | ... | Median |
| p90 | ... | Upper bound |

### Calibration Evidence
- **Methodology version**: `<version>`
- **Evaluation horizon**: `<horizon>`
- **Pythia V#2 Brier (trailing 12 months)**: `<score>`
- **Substrate sources**: Athena Ring (arXiv + OpenReview) + benchmark leaderboards + public capacity announcements

### Interpretation
What the median implies for the AI-compute trajectory, how the uncertainty band is shaped (skewed? bimodal? wide?), what would shift the distribution.

## Disclaimer

Phronesis V#2 forecasts are calibrated industry-aggregate probability distributions, not company-specific roadmap predictions. Phronesis does not have access to confidential vendor roadmaps; all substrate is public. Use forecasts to inform strategy, not to predict any specific company's release date.
