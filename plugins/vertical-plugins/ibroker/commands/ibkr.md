---
description: Check IBKR MCP server health and TWS / IB Gateway connection
argument-hint: "[status|quote <symbol>|expiries <symbol>]"
---

# /ibkr

Inspect and poke the IBKR MCP server. The server only runs while
TWS or IB Gateway is up on the configured port — this command surfaces
the live state of that connection.

## Subcommands

- `/ibkr status` — call `ibkr_status` and report whether the server
  can reach TWS / IB Gateway, and on which port (paper 7497, live 7496).
- `/ibkr quote <symbol>` — call `ibkr_quote` for the given symbol and
  show last, bid / ask, day range, and volume.
- `/ibkr expiries <symbol>` — call `ibkr_option_expiries` and list
  tradeable option expiries.
- `/ibkr scan <preset>` — call `ibkr_market_scanner` with one of the
  presets: `top_pct_gainers_us`, `top_pct_losers_us`, `most_active_us`,
  `unusual_volume_us`, `new_highs_us`, `new_lows_us`,
  `high_yield_dividend_us`, `top_trade_ideas_long`,
  `top_trade_ideas_short`. Defaults to `top_pct_gainers_us`.

If no subcommand is given, default to `status`.

## Setup

If `ibkr_status` reports the server is **not reachable**:

1. Make sure **TWS** (or **IB Gateway**) is running locally.
2. Open **Edit > Global Configuration > API > Settings**.
3. Enable **ActiveX and Socket Clients**; note the port.
4. Paper trading defaults to **7497**, live trading to **7496**.
5. To force a different port, set `IBKR_PORT` in `.mcp.json` at the
   repo root.

The server is read-only — it never places or cancels orders.
