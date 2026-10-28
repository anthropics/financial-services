---
name: regulatory-forecasting
description: Retrieve verified-correctness probability distributions for regulatory forecasts — legislation-passage timing, agency rulemaking outcomes, court-ruling probabilities, tariff and trade-policy shifts, and antitrust-action likelihoods. Use when an agent needs forward-looking regulatory-event probability bands with calibration evidence. Pythia ring V#5.
---

# Regulatory Forecasting (Pythia V#5)

You are routing regulatory forecast requests to the Phronesis MCP server. Phronesis V#5 (Regulatory) returns **calibrated probability distributions** over regulatory + legislative + judicial events at jurisdiction-aggregate granularity. Substrate draws from congress.gov, Federal Register, court dockets, agency-meeting calendars, and reasoning-engine inference.

## Core Principles

- **Regulatory outcomes are inherently probabilistic.** Bill passage, agency rulemaking, court rulings — all carry conditional uncertainty. p10/p50/p90 framing is canonical.
- **Jurisdiction + body + horizon must be specified.** "Will Congress pass X" is ambiguous; "What is the probability the U.S. Senate passes bill S.XXXX by end of 117th Congress?" is canonical.
- **No predictive litigation advice.** V#5 surfaces probability distributions over public regulatory events. It does not provide legal opinions or per-case litigation advice. Phronesis Themis publish-gate enforces forbidden language (no "will rule", no "guaranteed outcome").
- **Bipartisan-neutral framing.** Outputs avoid political-stance language; users get probability bands and reasoning chains, not advocacy framing.

## Available MCP Tools

- **`phronesis_forecast_query`** — `{vertical: "regulatory", question, horizon_months, jurisdiction, body?, topic?}`.
- **`phronesis_calibration_scorecard`** — V#5 Brier-score history (regulatory events evaluated post-decision).
- **`phronesis_methodology_ledger`** — Substrate provenance (bill-text, hearing-record, agency rulemaking docket, etc.).

## Query Patterns

1. **Legislation passage** — `question: "Forecast distribution for probability that S.XXXX passes both chambers by 2027-12-31?"` `jurisdiction: "US-Federal"` `body: "Congress"` `topic: "energy-permitting-reform"` `horizon_months: 24`.
2. **Agency rulemaking** — `question: "Forecast distribution for date EPA finalizes proposed rule on Subpart W methane reporting?"` `jurisdiction: "US-Federal"` `body: "EPA"` `topic: "methane-rule"` `horizon_months: 18`.
3. **Court ruling** — `question: "Forecast distribution for SCOTUS ruling date in case docket X?"` `jurisdiction: "US-SCOTUS"` `body: "SCOTUS"` `horizon_months: 12`.
4. **Tariff / trade-policy** — `question: "Forecast distribution for probability of new Section 301 tariff actions on clean-tech imports by 2027?"` `jurisdiction: "US-Federal"` `topic: "section-301-cleantech"` `horizon_months: 18`.
5. **Antitrust action** — `question: "Forecast distribution for probability of new DOJ antitrust filings against the top-5 cloud hyperscalers by 2028?"` `jurisdiction: "US-Federal"` `topic: "antitrust-hyperscaler"` `horizon_months: 36`.

## Tool Chaining Workflow

1. **Restate canonically** — jurisdiction, body, topic, horizon. If user phrases ambiguously, ask for jurisdiction first.
2. **Call `phronesis_forecast_query`** with V#5. Receive distribution + calibration ref.
3. **Optional: `phronesis_calibration_scorecard`** — V#5 Brier is informative because regulatory event outcomes are typically binary or categorical (easier to score).
4. **Optional: `phronesis_methodology_ledger`** — surface bill-text + hearing record + docket references used.
5. **Synthesize** — probability + reasoning chain (avoid political framing).

## Output Format

### Forecast Distribution
| Quantile / Outcome | Value | Notes |
|--------------------|-------|-------|
| p10 / Less-likely outcome | ... | Lower bound or alternative outcome |
| p50 / Median | ... | Most-likely path |
| p90 / Tail | ... | Upper bound or low-probability alternative |

For binary forecasts (passes / doesn't pass): report `probability_yes` + `probability_no` + uncertainty band.

### Calibration Evidence
- **Methodology version**: `<version>`
- **Evaluation horizon**: `<horizon>`
- **Pythia V#5 Brier (trailing 12 months, this event class)**: `<score>`
- **Substrate sources**: congress.gov, Federal Register, court PACER docket, agency hearing records, etc.

### Reasoning Chain
2-3 sentences: median outcome, key dependencies (committee markup, floor calendar, conference, executive sign), what would shift the distribution. Cite methodology ledger.

## Disclaimer

Phronesis V#5 forecasts are probability distributions over public regulatory + legislative + judicial events. They are not legal advice, not lobbying analysis, and not political endorsements. Phronesis Themis publish-gate enforces the absence of advocacy language. For binding legal opinions, consult licensed counsel.
