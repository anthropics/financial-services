---
description: Generate a comprehensive equity research snapshot with consensus estimates, fundamentals, and price performance
argument-hint: "<ticker e.g. AAPL> [period e.g. FY2024-FY2026]"
---

# Research Equity

> This command uses LSEG quantitative analytics, historical pricing, and macroeconomic data tools. See [CONNECTORS.md](../CONNECTORS.md) for available tools.

Generate a comprehensive equity research snapshot combining analyst consensus estimates, historical financials, price performance, and macroeconomic context.

See the **equity-research** skill for domain knowledge on fundamental analysis and estimate interpretation.

## Workflow

### 1. Gather Input

Ask the user for:
- Ticker symbol (required) — IBES ticker format (e.g., AAPL, MSFT, VOD)
- Forward period of interest (optional, default: next 2 fiscal years)
- Any specific focus areas (e.g., earnings, revenue, dividends)

### 2. Gather Consensus Estimates

Call `qa_ibes_consensus` with the ticker for FY1 and FY2 estimates.
- Measures: EPS, Revenue, EBITDA, DPS
- Period type: "A" (annual)

Extract: median/mean estimate, analyst count, high/low range, dispersion.

### 3. Pull Historical Fundamentals

Call `qa_company_fundamentals` for the last 3-5 fiscal years.

Extract: revenue growth, margin trends, leverage, earnings trajectory.

### 4. Assess Price Performance

Call `qa_historical_equity_price` for 1Y history.

Compute: YTD return, 1Y return, 52-week range, beta.

### 5. Recent Price Action Detail

Call `tscc_historical_pricing_summaries` with `interval: "P1D"`, `tenor: "3M"`.

Extract: daily OHLCV, volume trends, recent momentum.

### 6. Macro Context

Call `qa_macroeconomic` for GDP, CPI, and policy rate in the company's primary market.

Summarize: economic environment as tailwind or headwind for the sector.

### 7. Synthesize the Report

Present: consensus estimates table, historical financials summary, valuation metrics (forward P/E = price / consensus EPS), price performance, macro backdrop, and investment thesis summary.

## Output Format

Present as a structured research note. Lead with the investment thesis summary (1-2 sentences), then detail supporting sections with tables.
