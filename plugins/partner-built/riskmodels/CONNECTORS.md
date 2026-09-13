# Connectors

This plugin connects to the **RiskModels MCP Server** (`https://riskmodels.app/api/mcp/sse`),
a single hosted MCP that serves US equity factor-risk, point-in-time fundamentals,
cost of capital, and hedging tools — no additional connectors are needed. Unlike the
licensed-terminal connectors elsewhere in this repo, RiskModels is a hosted service
billed per call (free tier available); a key is set via `RISKMODELS_API_KEY`.

## How Skills Reference Tools

Skills reference MCP tools by their exact tool name (e.g. `riskmodels_decompose`,
`riskmodels_get_fundamentals`). The tools are grouped into categories below.

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| Risk Decomposition | `riskmodels_get_hedge_levels`, `riskmodels_decompose`, `get_metrics`, `riskmodels_portfolio_decompose` | L1/L2/L3 market/sector/subsector/residual decomposition with ETF hedge ratios |
| Fundamentals | `riskmodels_get_fundamentals` | Point-in-time quarterly fundamentals, ratios, CAPM cost-of-capital layer, SEC-sourced raw line items |
| Hedging | `riskmodels_hedge_position`, `riskmodels_hedge_portfolio`, `riskmodels_analyze_portfolio`, `riskmodels_get_lstar`, `riskmodels_batch_lstar` | Scale ETF hedge legs to notionals; Lstar residual isolation |
| Rankings & Signals | `riskmodels_get_rankings`, `riskmodels_screen_rankings`, `riskmodels_get_residual_signal` | Cross-sectional percentile ranks; residual mean-reversion signal |
| Return Attribution | `riskmodels_get_return_attribution`, `riskmodels_get_returns` | Daily return split into L1/L2/L3 factor + residual components |
| Discovery | `riskmodels_search_tickers`, `riskmodels_search_etfs`, `riskmodels_get_etf_holdings`, `riskmodels_search_filers`, `riskmodels_get_filer_holdings` | Resolve names/symbols; fetch real ETF and 13F-filer holdings |
| Capabilities | `riskmodels_list_endpoints`, `riskmodels_get_capability` | Enumerate the live capability surface (free) |

## Complete Tool Reference

### Risk Decomposition
- **`riskmodels_get_hedge_levels`** — L1/L2/L3 hedge snapshots side by side: hedge ratios (`*_hr`), explained-risk fractions (`*_er`), and the ETF legs (market/sector/subsector) at each depth.
- **`riskmodels_decompose`** — L3 four-bet decomposition (market / sector / subsector / residual) for one name.
- **`get_metrics`** — latest snapshot: hedge ratios, ER fractions, volatility, close, market cap.
- **`riskmodels_portfolio_decompose`** — decompose a weighted portfolio into the four layers.

### Fundamentals
- **`riskmodels_get_fundamentals`** — point-in-time quarterly fundamentals: rows visible only where `filed_date <= as_of`. Returns TTM profitability and capital-return ratios, leverage, ERM3 cascade betas, a CAPM cost-of-capital layer (`cost_of_equity`, `wacc`, `economic_profit`; caller `erp` / `rf_tenor`, `grid=true` for sensitivity), an equity-bridge decomposition, and `sec_facts` — raw line items per cell where the serving value is SEC XBRL.

### Hedging
- **`riskmodels_hedge_position`** — scale one ticker's ETF hedge ratios to a dollar position.
- **`riskmodels_hedge_portfolio`** — hedge ratios at L1/L2/L3, scaled by notionals, aggregated into ETF USD legs for a book.
- **`riskmodels_analyze_portfolio`** — holdings-weighted L1/L2/L3 hedge-level aggregate.
- **`riskmodels_get_lstar`** / **`riskmodels_batch_lstar`** — dispatch the simplest cascade level clearing the marginal-ER threshold; return residual-return series (single / up to 100 tickers).

### Rankings & Signals
- **`riskmodels_get_rankings`** — where a name sits in its sector/universe percentile for a metric.
- **`riskmodels_screen_rankings`** — full cross-section percentile/decile rank screen, server-side.
- **`riskmodels_get_residual_signal`** — aggregate L3 residual mean-reversion signal across a basket.

### Return Attribution
- **`riskmodels_get_return_attribution`** — daily gross return split into additive L1/L2/L3 factor, combined-factor, and residual return series.
- **`riskmodels_get_returns`** — daily returns with L1/L2/L3 hedge ratios and risk decomposition.

### Discovery
- **`riskmodels_search_tickers`** — search tickers by symbol or company name.
- **`riskmodels_search_etfs`** / **`riskmodels_get_etf_holdings`** — resolve an ETF and fetch its holdings.
- **`riskmodels_search_filers`** / **`riskmodels_get_filer_holdings`** — resolve a 13F filer (by name / CIK / LEI) and fetch its top holdings.

### Capabilities
- **`riskmodels_list_endpoints`** — enumerate the live public capability surface (free).
- **`riskmodels_get_capability`** — full details for one capability by id (free).
