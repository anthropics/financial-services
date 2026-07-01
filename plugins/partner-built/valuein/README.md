# Valuein SEC EDGAR Plugin

SEC EDGAR financial statements, ratios, valuation metrics, smart-money intelligence, and forensic-audit scores — point-in-time accurate, survivorship-bias free, ~105M facts across 17,000+ US-listed entities.

## What This Plugin Does

Valuein's MCP server (`mcp.valuein.biz`) packages SEC EDGAR data into a unified analytical surface: standardized financial statements with one-click lineage to source filings, pipeline-computed ratios, DCF and reverse-DCF, forensic-audit scores (partial Beneish + Sloan accruals + solvency), and a smart-money dataset covering insider transactions (Forms 3/4/5/144) plus institutional ownership (13F / 13D / 13G). This plugin orchestrates those tools into 3 high-level workflows so an analyst doesn't have to chain calls manually.

The data is **point-in-time correct by construction** — every fact carries an `accepted_at` timestamp from SEC acceptance, and the warehouse never overwrites historical values. Backtests filter by date; restatements appear as new rows.

## Commands

| Command | Description |
|---------|-------------|
| `/research-equity` | Generate an equity research snapshot — fundamentals, ratios, peer comparables, valuation, and capital allocation context for any US ticker. |
| `/forensic-audit` | Earnings-quality red-flag brief — partial Beneish M-Score, Sloan accruals, solvency snapshot, and restatement history with citations to source filings. |
| `/screen-and-shortlist` | Run a cross-sectional factor screen, forensic-audit the top candidates, and produce a ranked shortlist with citations. |

## Skills

Each command is backed by a skill that provides domain knowledge:

| Skill | Domain Knowledge |
|-------|------------------|
| `equity-research` | Fundamental analysis, ratio interpretation, peer benchmarking, valuation metrics (DCF inputs, reverse-DCF, capital allocation scorecard). |
| `forensic-audit` | Beneish M-Score interpretation, Sloan accruals, restatement detection, leverage growth signals, citation grounding. |
| `screen-and-shortlist` | Factor-score screening, multi-factor ranking, survivorship-bias-free historical universes, forensic gating. |

## Integrations

This plugin connects to the **Valuein MCP Server** which provides US public-company financial data across these domains:

- **Entity & Universe** — Ticker / CIK / SIC resolution, current S&P 500 membership, historical PIT universe construction (survivorship-free).
- **Fundamentals** — Standardized income statement, balance sheet, cash flow rows with `lineage` envelopes that link every numeric value to the source SEC accession (`source_url` is a clickable EDGAR link).
- **Ratios** — Pipeline-computed profitability, liquidity, leverage, efficiency, per-share, owner-earnings, and valuation ratios; TTM and FY variants.
- **Valuation** — Forward DCF, reverse DCF, peer-comparable benchmarks across the full US universe.
- **Capital Allocation** — Deployment mix (capex / R&D / M&A / dividends / buybacks / debt repayment) as percent of operating cash flow with red-flag detection (buybacks-exceed-FCF, debt-funded-distribution).
- **Forensic Audit** — Partial Beneish M-Score (SGI + TATA + LVGI), Sloan accruals, solvency snapshot, ranked red-flag narrative.
- **Smart Money** (Institutional tier) — Insider transactions (Form 3 / 4 / 5 / 144), institutional ownership (13F), blockholders (SC 13D / 13G), manager portfolios with QoQ deltas, cross-fund consensus.
- **Filings** — Direct EDGAR URLs for 10-K, 10-Q, 8-K, 20-F, 40-F, amendments, by date range and form type.
- **Bulk Streaming** — Presigned R2 Parquet URLs for full-universe out-of-core analysis (DuckDB, Polars, Pandas).

See [CONNECTORS.md](CONNECTORS.md) for the complete tool reference.

## Installation

Add the marketplace and install the plugin:

```
/plugin marketplace add anthropics/financial-services
/plugin install valuein
```

## Requirements

- A Valuein account. Free tiers are available:
  - **Sample** — no signup required, S&P 500 5-year window, public read-only access.
  - **S&P 500 (Free)** — free with email signup, full S&P 500 from 1994 → present.
  - **Pro** — $49/month, full US universe (17,000+ tickers, active + delisted), 30-year history, full filings + ratios + valuation + capital-allocation surfaces.
  - **Institutional** — $499/month, adds the smart-money dataset (insider + 13F + 13D/13G), full history back to 1990, foreign issuers, filing-event webhooks, commercial redistribution license.
- For paid tiers, set your Valuein API token in the MCP authorization header. See the [Valuein quickstart](https://valuein.biz/developers/quickstart) for token provisioning.

The Sample tier serves a curated S&P 500 slice without authentication, so the `/research-equity` and `/screen-and-shortlist` commands work out of the box on supported tickers for evaluation.
