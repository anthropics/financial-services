# IBKR MCP Server

Read-only research surface over Interactive Brokers TWS / IB Gateway.
Exposes market data, fundamentals, options, scanner, and account views
as MCP tools so Claude Code and OMP can pull live broker data when
running the equity-research skills in this repo.

> The server is installed **only for this repo**. The repo-root
> `.mcp.json` wires the stdio command; outside this directory the
> server is invisible to Claude Code / OMP.

## What it does

- Live quotes (single + batch)
- Historical OHLCV bars
- IB/Reuters fundamental snapshot (P/E, EPS, mkt cap, margins, leverage)
- Dividend payment history
- Shortable share count
- Option expiries + chains + greeks (TWS stream with BS fallback)
- Market scanner (curated research presets)
- Symbol-scoped news headlines
- Account summary + positions (read-only)

**Nothing in this server places or cancels orders.** All client IDs use
the read-only `readonly=True` flag at the TWS level.

## Prerequisites

- Python 3.12+
- [TWS](https://www.interactivebrokers.com/en/trading/tws.php) or
  [IB Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php)
  running locally with API access enabled
- `uv` for dependency management

## TWS / IB Gateway setup

1. Open TWS (or IB Gateway).
2. Enable API access:
   - **TWS:** `Edit > Global Configuration > API > Settings`
   - Check ✅ **Enable ActiveX and Socket Clients**
   - Note the **Socket Port**:
     - **Paper trading:** 7497
     - **Live trading:** 7496
3. (Optional but recommended) Add `127.0.0.1` to **Trusted IPs**.
4. Restart TWS / Gateway if you changed API settings.

The server tries the configured port first and falls back to the
other standard port if the first connect fails. You can also force a
port with the `IBKR_PORT` environment variable.

## Install + run

From the repo root:

```bash
uv sync                                  # installs ib-async + mcp
uv run python -m mcp_server.ibkr.server  # run the server (stdio)
```

To launch it from Claude Code / OMP, just open the repo — the
`.mcp.json` at the repo root will spawn the server automatically.

## Tool surface (16 tools)

| Tool | What it returns |
|------|-----------------|
| `ibkr_status` | Health check — TWS reachable? Which port? |
| `ibkr_quote` | Live single-symbol quote (last, bid/ask, OHLC, volume) |
| `ibkr_snapshot` | Batch quote for a list of symbols |
| `ibkr_historical` | OHLCV bars over a date/duration window |
| `ibkr_contract_details` | IB contract spec (primary exchange, conId, hours) |
| `ibkr_fundamentals` | P/E, EPS, mkt cap, div yield, 52w range, margins |
| `ibkr_dividends` | Cash dividend payment history |
| `ibkr_shortable` | Shortable share count (best-effort) |
| `ibkr_option_expiries` | Tradeable expiry dates for an underlying |
| `ibkr_option_chain` | Calls + puts around ATM for one expiry |
| `ibkr_option_greeks` | Single-strike greeks (TWS stream + BS fallback) |
| `ibkr_market_scanner` | Curated equity-research scans (movers, vol, etc.) |
| `ibkr_news` | Symbol-scoped IB news headlines |
| `ibkr_account_summary` | Net liq, cash, buying power, margin |
| `ibkr_account_values` | Raw `AccountValue` rows (filter by tag) |
| `ibkr_portfolio` | Current positions across all managed accounts |

### Scanner presets

Pass these as the `scan_code` arg to `ibkr_market_scanner`:

| Preset | What it does |
|---|---|
| `top_pct_gainers_us` | Biggest % gainers (US, price > $5) |
| `top_pct_losers_us` | Biggest % losers (US, price > $5) |
| `most_active_us` | Highest volume (US, price > $5) |
| `unusual_volume_us` | Volume materially above the trailing baseline |
| `new_highs_us` | Trading near 13-week high |
| `new_lows_us` | Trading near 13-week low |
| `high_yield_dividend_us` | Highest dividend yield in the universe |
| `top_trade_ideas_long` | IB-curated long ideas |
| `top_trade_ideas_short` | IB-curated short ideas |

You can also pass a literal TWS API scan code (e.g. `"TOP_PERC_GAIN"`)
to use codes not in the preset list.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Could not connect to TWS / IB Gateway` | TWS not running, or wrong port | Start TWS / IB Gateway; verify `Configure > API > Settings` port |
| `ClientId already in use` | Another process holds the research client ID | Close the other process or change `CLIENT_ID_RESEARCH` in `connection.py` |
| `No market data permissions` | Market data subscription missing for the exchange | TWS shows which subscriptions are active under `Account > Market Data Subscriptions` |
| `reqFundamentalData` returns empty | `ReportSnapshot` is not always populated for OTC / ADR | Use the company filings instead, or pass a different `reportType` |
| Tools return `error: Could not resolve contract` | Symbol not recognized by IB | Use the full IBKR symbol (e.g. add exchange suffix for non-US tickers) |

## License

Apache 2.0 — same as the rest of this repo.
