# Connectors

This plugin connects to the **LFA MCP Server**, which provides financial analytics tools from LSEG (London Stock Exchange Group). All tools are served by a single MCP server — no additional connectors are needed.

## How Commands Reference Tools

Commands in this plugin reference MCP tools by their exact tool name (e.g., `bond_price`, `interest_rate_curve`). The tools are organized into categories for clarity:

## Tool Categories

| Category | Placeholder | Tools | Description |
|----------|-------------|-------|-------------|
| Bond Pricing | `~~bond-pricing` | `bond_price`, `bond_future_price` | Price bonds and bond futures with full analytics |
| FX Pricing | `~~fx-pricing` | `fx_spot_price`, `fx_forward_price` | FX spot and forward rate pricing |
| Interest Rate Curves | `~~ir-curves` | `interest_rate_curve`, `inflation_curve` | Government yield curves and inflation breakevens |
| Credit Curves | `~~credit-curves` | `credit_curve` | Credit spread curves by issuer type |
| FX Curves | `~~fx-curves` | `fx_forward_curve` | FX forward point curves |
| Options | `~~options` | `option_value`, `option_template_list` | Option valuation with Greeks |
| Swaps | `~~swaps` | `ir_swap` | Interest rate swap pricing |
| Volatility Surfaces | `~~volatility` | `fx_vol_surface`, `equity_vol_surface` | FX and equity implied vol surfaces |
| Quantitative Analytics | `~~qa` | `qa_ibes_consensus`, `qa_company_fundamentals`, `qa_historical_equity_price`, `qa_macroeconomic` | Analyst estimates, fundamentals, prices, macro data |
| Time Series | `~~time-series` | `tscc_historical_pricing_summaries` | Historical pricing summaries (interday/intraday) |
| Fixed Income Analytics | `~~yieldbook` | `yieldbook_bond_reference`, `yieldbook_cashflow`, `yieldbook_scenario`, `fixed_income_risk_analytics` | Bond reference data, cashflows, scenarios, OAS/duration |

## Complete Tool Reference

### Bond Domain
- **`bond_price`** — Calculate bond pricing, valuation, and analytics. Accepts ISIN, RIC, CUSIP, or AssetId. Returns yield, duration, convexity, DV01, accrued interest. Supports what-if scenarios via price/yield overrides.
- **`bond_future_price`** — Calculate bond future pricing and analytics. Returns fair value, cheapest-to-deliver identification, delivery basket, conversion factors, and contract DV01.

### FX Domain
- **`fx_spot_price`** — FX spot rate pricing for ISO currency pairs. Returns mid/bid/ask rates.
- **`fx_forward_price`** — FX forward rate pricing at specific tenors or dates. Returns forward points, outright rates, and carry.

### Curves Domain
- **`interest_rate_curve`** — Government yield curves. Two-phase: list available curves, then calculate curve points. Returns par/zero rates, discount factors, forward rates.
- **`credit_curve`** — Credit spread curves. Search by country and issuer type (Corporate, Sovereign, Agency, etc.), then calculate spread term structure.
- **`inflation_curve`** — Inflation breakeven curves. Search by country/currency, then calculate breakeven rates and real yields.
- **`fx_forward_curve`** — FX forward point curves. List curves, then calculate forward points across all standard tenors.

### Swaps Domain
- **`ir_swap`** — Interest rate swap pricing. Two-phase: list templates by currency/index, then price swaps at specified tenors. Returns par rates, DV01, NPV.

### Options Domain
- **`option_value`** — Option valuation supporting vanilla, barrier, binary, and Asian options. Returns premium, full Greeks (delta, gamma, vega, theta, rho), and risk metrics.
- **`option_template_list`** — List available option templates for pricing.

### Volatility Domain
- **`fx_vol_surface`** — FX volatility surface generation using SABR model. Returns vol surface across tenors and delta strikes.
- **`equity_vol_surface`** — Equity implied volatility surface. Supports equities/indices via RIC and futures via RICROOT.

### Quantitative Analytics Domain
- **`qa_ibes_consensus`** — IBES analyst consensus estimates (EPS, revenue, EBITDA, DPS). Forward-looking estimates with analyst count, dispersion, and high/low ranges.
- **`qa_company_fundamentals`** — Reported company financials (income statement, balance sheet metrics). Historical fiscal year data.
- **`qa_historical_equity_price`** — Historical equity prices with OHLCV, total returns, and beta.
- **`qa_macroeconomic`** — Macroeconomic indicators database. Search by mnemonic or description, retrieve latest values or time series.

### Time Series Domain
- **`tscc_historical_pricing_summaries`** — Historical pricing summaries for any RIC. Supports interday (daily, weekly, monthly) and intraday (1min to 1hr) intervals.

### Fixed Income Analytics (YieldBook) Domain
- **`yieldbook_bond_reference`** — Bond reference data: security type, sector, ratings, coupon, maturity, issuer.
- **`yieldbook_cashflow`** — Bond cashflow projections: future coupon and principal payment schedules.
- **`yieldbook_scenario`** — Bond scenario analysis: price/yield under parallel rate shifts.
- **`fixed_income_risk_analytics`** — Bond risk analytics: OAS, effective duration, key rate durations, convexity.
