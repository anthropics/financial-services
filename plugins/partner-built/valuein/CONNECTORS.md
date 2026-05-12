# Connectors

This plugin connects to the **Valuein MCP Server** at `https://mcp.valuein.biz/mcp`, which exposes SEC EDGAR fundamentals + ratios + valuation + smart-money intelligence + forensic-audit scores across the full US public-company universe. All tools are served by a single MCP server — no additional connectors required.

## How Commands Reference Tools

Commands in this plugin reference MCP tools by their exact tool name (e.g., `get_company_fundamentals`, `forensic_audit`). The tools are organized into the categories below.

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| Discovery | `search_companies`, `get_pit_universe`, `describe_schema` | Resolve tickers/CIKs/SIC codes; build survivorship-bias-free historical universes; introspect the parquet schema. |
| Fundamentals | `get_company_fundamentals`, `compare_periods`, `get_earnings_signals` | Standardized income statement / balance sheet / cash flow rows with lineage; side-by-side period comparisons; TTM-based earnings surprise signals. |
| Ratios | `get_financial_ratios` | 7 categories of pipeline-computed ratios (profitability, liquidity, leverage, efficiency, per-share, owner earnings, valuation). |
| Valuation | `get_valuation_metrics`, `get_peer_comparables`, `compute_dcf` | Merged ratio + DCF metrics per fiscal period; cross-entity peer benchmarking; standalone forward DCF with 5×5 sensitivity grid. |
| Capital Allocation | `get_capital_allocation_profile` | Deployment mix as percent of OCF (capex / R&D / M&A / dividends / buybacks / debt repayment) with red-flag detection. |
| Forensic | `forensic_audit`, `verify_fact_lineage` | Partial Beneish M-Score + Sloan accruals + solvency snapshot + red-flag narrative; fact-by-fact provenance verification against SEC EDGAR. |
| Filings | `get_sec_filing_links` | Filing URLs by ticker + date range + form type (10-K, 10-Q, 8-K, 20-F, 40-F, amendments). |
| Screening | `screen_universe` | Cross-sectional factor-score screening across the full universe with composite-rank output. |
| Smart Money (Institutional) | `get_insider_transactions`, `get_institutional_holdings`, `get_manager_portfolio`, `get_blockholders`, `get_smart_money_flow`, `get_top_holders`, `get_insider_sentiment` | Insider transactions (Forms 3 / 4 / 5 / 144), 13F holdings, manager portfolios with QoQ deltas, SC 13D / 13G blockholders + going-active flags, cross-fund smart-money flow aggregates. |
| Bulk Streaming | `get_compute_ready_stream` | Presigned R2 Parquet URLs for out-of-core analytics in DuckDB / Polars / Pandas. |

## Complete Tool Reference

### Discovery Domain

- **`search_companies`** — Search the US-listed universe by name, ticker, CIK, or SIC code. Returns ticker, name, sector, industry, exchange, and current S&P 500 membership. Use this to resolve a free-text company reference to a stable ticker before calling fundamental tools.
- **`get_pit_universe`** — Construct a survivorship-bias-free historical universe at a specific date (e.g., "S&P 500 members on 2018-06-30"). Uses `index_membership` interval semantics (effective_date → removal_date) for clean backtests.
- **`describe_schema`** — Introspect the Parquet schema available on the caller's plan. Returns table list, column types, and last-snapshot metadata.

### Fundamentals Domain

- **`get_company_fundamentals`** — Standardized income statement, balance sheet, and cash-flow rows per fiscal period. Includes a `lineage` envelope with `source_filing` (SEC accession id) + `source_url` (clickable EDGAR link) for one-click verification of every numeric value. Supports `as_of_date` for PIT backtests.
- **`compare_periods`** — Side-by-side comparison of any two fiscal periods for a ticker. Surfaces material-change flags (e.g., revenue swung > X% YoY, leverage doubled). Useful as a discovery aid before deeper analysis.
- **`get_earnings_signals`** — TTM-based EPS trend + YoY revenue surprise per entity per fiscal period. Useful for earnings-call setup and surprise-history backtesting.

### Ratios Domain

- **`get_financial_ratios`** — Pipeline-computed ratios from `ratio.parquet`, filterable by category. Categories: `profitability`, `liquidity`, `leverage`, `efficiency`, `per_share`, `owner_earnings`, `valuation`. TTM and FY variants. Pipeline-derived (no `accepted_at` — use period_end for historical cuts).

### Valuation Domain

- **`get_valuation_metrics`** — Merged ratio + DCF metrics in a single response. Returns profitability ratios (margins, ROE, ROA, ROIC), leverage (debt-to-equity), FCF + FCF margin, and DCF inputs (WACC, terminal-growth assumption, stage-1 rate, computed value per share, DDM value) when available.
- **`get_peer_comparables`** — Cross-entity benchmarking: subject + N peers (default 10) with ratios across the requested categories. Surfaces relative quality + valuation positioning.
- **`compute_dcf`** — Forward discounted-cash-flow valuation: caller provides growth + WACC + terminal assumptions, returns per-share intrinsic value + 5×5 sensitivity grid across WACC × terminal-growth. Pulls FCF base + shares from R2; caller can override any field. Does not persist results — pair with `create_report` for an authored artifact.

### Capital Allocation Domain

- **`get_capital_allocation_profile`** — Detailed cash deployment per fiscal period: capex, R&D, M&A net activity, dividends paid, share repurchases, debt issuance / repayment, plus deployment mix as percent of operating cash flow. Includes red-flag booleans: `buybacks_exceed_fcf`, `total_returns_exceed_fcf`, `debt_funded_distribution`.

### Forensic Domain

- **`forensic_audit`** — Deterministic earnings-quality scores: partial Beneish M-Score (SGI + TATA + LVGI factors), Sloan accruals (total accruals / total assets), and a three-ratio solvency snapshot (debt-to-equity, debt-to-assets, ROA). Returns a ranked red-flag narrative — flags above empirical thresholds (M > -2.22, accruals > 7.5%, D/E > 3.0, negative ROA, leverage growth > 1.10).
- **`verify_fact_lineage`** — Trace any numeric fact in the warehouse back to its originating SEC filing. Returns the fact_id, accession, EDGAR URL, accepted_at timestamp, and whether the value has been restated.

### Filings Domain

- **`get_sec_filing_links`** — Filing metadata + EDGAR deep links by ticker, date range, and form type. Supports 10-K, 10-Q, 8-K, 20-F, 40-F + amendments. Returns accession, filing date, accepted_at, form type, is_amendment flag, and SEC inline-XBRL viewer URLs.

### Screening Domain

- **`screen_universe`** — Cross-sectional factor scoring across the full universe. Each ticker carries percentile ranks for revenue growth, FCF yield, ROIC, etc., plus a composite rank. Useful as the first stage in `/screen-and-shortlist`.

### Smart Money Domain (Institutional tier)

- **`get_insider_transactions`** — Form 3 / 4 / 5 / 144 line items per issuer with role + role decoration (Officer / Director / TenPercentOwner), transaction code, shares, price, and notional. Lineage anchors back to the originating SEC accession.
- **`get_institutional_holdings`** — Form 13F top holders per issuer including HHI (Herfindahl-Hirschman concentration index). Filterable by period_end and lineage detail.
- **`get_manager_portfolio`** — Full Form 13F portfolio of a single filer (CIK) at a quarter-end, with QoQ deltas per position: new / increased / decreased / exited / unchanged. Useful for "follow Tiger Cubs" / "follow Berkshire" workflows.
- **`get_blockholders`** — SC 13D + SC 13G beneficial-ownership filings per issuer with first-class `is_activist` and `going_active` flags (the latter fires on 13G → 13D conversions, the strongest activist signal).
- **`get_smart_money_flow`** — Aggregate cross-fund flow across an issuer: net institutional buys, new positions, exits, blockholder activity, and recent insider clusters. One call = "what is the institutional money doing on this name?"
- **`get_top_holders`** — Top N institutional holders per issuer with concentration metrics. Lighter-weight alternative to the full 13F surface.
- **`get_insider_sentiment`** — Insider cluster detection: multiple distinct insiders buying / selling within a lookback window. Surfaces the strongest single-name insider signal (cluster buying historically outperforms isolated buys by a wide margin).

### Bulk Streaming Domain

- **`get_compute_ready_stream`** — Returns a 1-hour-expiry presigned R2 URL for the full parquet table at the caller's tier. Use this for out-of-core analytics in DuckDB / Polars / Pandas that the per-entity tool surface can't economically support.

## Tier Gating

| Domain | Sample (no signup) | S&P 500 Free | Pro ($49/mo) | Institutional ($499/mo) |
|---|---|---|---|---|
| Discovery + Fundamentals + Ratios + Valuation + Capital Allocation + Forensic + Filings | S&P 500 / 5yr | S&P 500 / full history | Full universe / 30yr | Full universe / 1990+ |
| Smart Money (insider + 13F + 13D/G) | — | — | — | ✅ |
| Bulk Streaming (presigned URLs) | sample bucket | sp500 bucket | pro bucket | full bucket |

Sample tier is unauthenticated guest access — the `/research-equity` and `/screen-and-shortlist` commands work without signup for evaluation on S&P 500 companies.

## Authentication

The MCP client passes the caller's Valuein API token to the server via the standard MCP `Authorization` header (`Bearer <64-hex-token>`). Tokens are provisioned at https://valuein.biz/dashboard after subscription. No token is needed for the Sample tier — the server treats unauthenticated requests as guest access scoped to `R2_SAMPLE`.

## Lineage and Verification

Every numeric response from a Valuein tool carries a `lineage` envelope (compact by default, full detail on request via `lineage_detail`):

```json
{
  "source_filing": "0000320193-25-000123",
  "source_url": "https://www.sec.gov/Archives/edgar/data/320193/000032019325000123/0000320193-25-000123-index.htm",
  "restated_in_warehouse": false,
  "accepted_at": "2025-11-01T20:00:00Z",
  "first_filed_at": "2025-11-01T20:00:00Z"
}
```

The `source_url` is a clickable EDGAR deep link to the filing index — one click to verify any number against the originating SEC document. Agents should surface this URL whenever they cite a fact.
