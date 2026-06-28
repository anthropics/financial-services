---
description: Build a macro and rates dashboard with economic indicators, yield curves, inflation, and swap spreads
argument-hint: "<country e.g. US> [timeframe e.g. 5Y]"
---

# Macro & Rates Dashboard

> This command uses LSEG macroeconomic data, yield curves, inflation curves, swap pricing, and historical data tools. See [CONNECTORS.md](../CONNECTORS.md) for available tools.

Build a comprehensive macroeconomic and rates dashboard showing key economic indicators, the yield curve with slope analysis, real rate decomposition, and swap spread context.

See the **macro-rates-monitor** skill for domain knowledge on macro-rates analysis.

## Workflow

### 1. Gather Input

Ask the user for:
- Country (required) — e.g., US, DE, GB, JP, CH
- Timeframe for historical series (optional, default 3Y)
- Any specific indicators of interest (optional)

Map country to currency: US→USD, DE→EUR, GB→GBP, JP→JPY.

### 2. Pull Macro Indicators

Call `qa_macroeconomic` for key indicators:
- GDP growth (quarterly series)
- CPI/inflation (monthly series)
- Unemployment rate (monthly series)
- Policy rate / central bank rate

Use wildcard mnemonic patterns to discover available series (e.g., "US\*GDP\*", "US\*CPI\*").

### 3. Get the Yield Curve

Call `interest_rate_curve` (list then calculate) for the country's government curve.

Extract yields at standard tenors. Compute: 2s10s slope, 3M-10Y slope, 5s30s slope. Classify curve shape.

### 4. Decompose Real Rates

Call `inflation_curve` (search then calculate) for the currency.

Compute real rate = nominal minus breakeven at key tenors. Assess whether real rates are accommodative or restrictive.

### 5. Swap Spread Analysis

Call `ir_swap` (list then price) at 2Y, 5Y, 10Y.

Compute swap spread = swap rate minus government yield at each tenor. Assess financial conditions.

### 6. Historical Yield Context

Call `tscc_historical_pricing_summaries` for the benchmark yield RIC with the user's timeframe.

Assess: where current yields sit in the historical range, trend direction.

### 7. Synthesize the Dashboard

Present: macro summary table, yield curve with slope metrics, real rate decomposition, swap spread table, historical context, and overall macro-rates assessment (2-3 sentences).

## Output Format

Present as a dashboard with clearly labeled sections. Lead with the overall macro assessment, then detail each component.
