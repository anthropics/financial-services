---
name: ibkr-data-source
description: Connect Claude to Interactive Brokers TWS / IB Gateway as a live market-data and account-read source. Use whenever a research workflow needs current quotes, historical bars, fundamentals, option chains, or scanner output and IBKR is the user's preferred source. Triggers on "pull live data", "from IBKR", "TWS quote", "broker feed", "interactive brokers data", or any task in a research workflow that needs to call an ibkr_ tool.
---

# IBKR Data Source

The `ibkr_*` MCP tools are the project's bridge to Interactive Brokers
TWS / IB Gateway. Every other skill in this repo can call them through
MCP — this skill is the entry point that explains what they are, how
they connect, and when to prefer them over FactSet / S&P / Daloopa.

## Connection

TWS or IB Gateway must be running locally with API access enabled:

- **Paper trading** — port 7497
- **Live trading** — port 7496

**Port fallback**: if the configured port fails, the server retries
the other standard port. The first port to succeed is remembered for
the rest of the process.

**Verify connection** before running a workflow that depends on it:

```
ibkr_status()
```

If unreachable, see [`mcp_server/ibkr/README.md`](../../../../mcp_server/ibkr/README.md)
for setup steps.

## When to prefer IBKR vs. other data sources

| Need | Preferred source | Why |
|---|---|---|
| Live quotes, last-sale, day range | **IBKR** | Native market data, no per-call quota |
| Historical OHLCV bars (1m, 5m, 1h, 1d) | **IBKR** | Continuous history, fewer gaps than free feeds |
| Fundamental ratios (P/E, EPS, margins, mkt cap) | **S&P Kensho / FactSet / Daloopa** | IBKR deprecated `reqFundamentalData` for most accounts (error 10358). Use the other MCP providers wired in this repo. |
| Multi-year dividend history | **IBKR** | Walked from `ADJUSTED_LAST` bars |
| Option expiries + chain structure | **IBKR** | Contract resolution works without OPRA |
| Option prices + live Greeks | **IBKR** (needs OPRA sub) | Requires OPRA market data subscription |
| Market scanner (movers, unusual volume) | **IBKR** | Built-in scan codes, real-time |
| Symbol-scoped news | **IBKR** | Briefing.com / Dow Jones / Reuters providers |
| Pre-built comps spread from a database | FactSet / S&P / Daloopa | Already structured for comps work |
| Transcripts, 10-K/10-Q full text | Daloopa / SEC EDGAR | Not a market-data feed |
| Sell-side estimates history | FactSet / S&P | Not what IBKR exposes |

**Key limitation**: IBKR does NOT provide fundamental ratios (P/E, EPS,
margins, etc.) via the API for most account types. For any workflow that
needs fundamentals, use **S&P Kensho MCP** (`mcp__sp-global__*`),
**FactSet MCP** (`mcp__factset__*`), or **Daloopa MCP**
(`mcp__daloopa__*`) instead. The `ibkr_fundamentals` tool will return a
clear "not available" message directing you to these alternatives.

For multi-source workflows, **start with IBKR for market data** (quotes,
historical bars, scanner), then **layer S&P/FactSet/Daloopa for
fundamentals and estimates**. Don't duplicate — if IBKR gave you the
historical bars, don't also pull them from S&P just to "double-check".

## Tool surface

| Tool | Use it for |
|---|---|
| `ibkr_status` | Health check — is TWS reachable? |
| `ibkr_quote` | Single live quote (last, bid, ask, OHLC, volume) |
| `ibkr_snapshot` | Batch quote for a list of symbols |
| `ibkr_historical` | OHLCV bars over a duration window |
| `ibkr_contract_details` | Symbol → IB contract spec (primary exchange, conId) |
| `ibkr_fundamentals` | P/E, EPS, mkt cap, div yield, 52w range, margins |
| `ibkr_dividends` | Last N years of cash dividend payments |
| `ibkr_shortable` | Shortable share count (best-effort) |
| `ibkr_option_expiries` | Tradeable option expiry dates |
| `ibkr_option_chain` | Calls + puts around ATM for one expiry |
| `ibkr_option_greeks` | Single-strike greeks (TWS stream + BS fallback) |
| `ibkr_market_scanner` | Curated equity-research scans (movers, vol, etc.) |
| `ibkr_news` | Symbol-scoped IB news headlines |
| `ibkr_account_summary` | Net liq, cash, buying power, margin |
| `ibkr_account_values` | Raw `AccountValue` rows (filter by tag) |
| `ibkr_portfolio` | Current positions across all managed accounts |

## Workflow integration

The IBKR tools are designed to slot into the existing research skills
without rewriting them. When a skill needs live data, it should:

1. **First call**: `ibkr_status` to confirm the broker connection. If
   unreachable, fall back to web search / SEC EDGAR and note the
   fallback in the output.
2. **Quote / price sanity check**: `ibkr_quote` for current price,
   52-week range, and live volume.
3. **Historical series**: `ibkr_historical` with the right duration
   (`"1 Y"` for a year, `"5 Y"` for multi-year, `"1 D"` intraday).
4. **Fundamentals**: `ibkr_fundamentals` for the headline ratios. If
   the user needs deeper history or segment-level data, layer
   Daloopa / FactSet on top.
5. **Options**: `ibkr_option_expiries` → `ibkr_option_chain` for the
   chosen expiry. Use `ibkr_option_greeks` for a specific strike.
6. **Screening**: `ibkr_market_scanner` with a preset.

### Research loop example

```
User: Build a quick comps spread for NVDA against AMD, INTC, AVGO, MRVL, TSM.

You: ibkr_quote("NVDA")           # confirm live price + market cap input
     ibkr_fundamentals("NVDA")     # pull TTM P/E, EV, mkt cap (IB side)
     ibkr_quote("AMD"), ibkr_quote("INTC"), ...   # batch via ibkr_snapshot
     ibkr_fundamentals(...) for the same set
     -> Build the comps table. The IB side is the live trading layer;
        if a deeper comps spread is needed, defer to comps-analysis.
```

## Guardrails

- **Read-only by construction.** The server never places or cancels
  orders — all `ib_async` calls use `readonly=True`.
- **Respect `data_delay`.** Fundamentals are 15-30 min lagged; quotes
  are real-time; historical bars are end-of-day after market close.
  Always include the `generated_at` and (where present) `data_delay`
  fields in any downstream output that cites the figure.
- **Don't combine with web search for the same datum.** If IBKR gave
  you the price, don't also fetch a third-party price. Sources should
  be primary, not redundant.
- **Port fallback is not infinite.** Two fails and `ibkr_status`
  reports unreachable. Don't loop retrying inside a workflow.
