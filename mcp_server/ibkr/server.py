#!/usr/bin/env python3
# ABOUTME: MCP server entrypoint — wires every IBKR research tool to FastMCP.
# ABOUTME: Run via `uv run python -m mcp_server.ibkr.server`.

"""MCP server exposing the IBKR research surface.

Invoked from the repo-root `.mcp.json` (Claude Code) and
`plugins/vertical-plugins/ibroker/.mcp.json` (Cowork), with:

    uv run python -m mcp_server.ibkr.server

The server is read-only by construction — every tool module in this
package only invokes market-data, account-read, and contract-resolution
IBKR API calls. There is no order placement anywhere in the package.
"""

from __future__ import annotations

import asyncio
import os
import sys
import traceback
from typing import Any

# Ensure unbuffered stdout so MCP JSON-RPC frames don't get coalesced
os.environ.setdefault("PYTHONUNBUFFERED", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(write_through=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(write_through=True)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    sys.stderr.write(
        "ERROR: The `mcp` package is not installed. Run `uv sync` at the repo root.\n"
        f"  {e}\n"
    )
    raise

# Local imports — these are the tool modules registered below.
from mcp_server.ibkr import (
    account as account_mod,
)
from mcp_server.ibkr import (
    fundamentals as fundamentals_mod,
)
from mcp_server.ibkr import (
    market_data as market_data_mod,
)
from mcp_server.ibkr import (
    news as news_mod,
)
from mcp_server.ibkr import (
    options as options_mod,
)
from mcp_server.ibkr import (
    scanner as scanner_mod,
)
from mcp_server.ibkr import (
    yfinance_tools as yf_mod,
)


mcp = FastMCP("ibkr-research")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _safe(fn, *args, **kwargs) -> dict[str, Any]:
    """Wrap a tool function so IB connection / data errors become JSON."""
    try:
        result = fn(*args, **kwargs)
        if asyncio.iscoroutine(result):
            # Tool functions are async (ib_async); FastMCP runs tool fns on the
            # event loop, so await the coroutine here. Safe — ib_connection
            # opens a fresh IB() per call (no shared loop affinity).
            result = await result
        return result
    except ConnectionError as e:
        return {
            "connected": False,
            "error": str(e),
            "hint": (
                "TWS / IB Gateway is not reachable. Start TWS or IB Gateway, "
                "enable API access (Configure > API > Settings), and verify "
                "the port matches IBKR_PORT (default 7497 paper, 7496 live)."
            ),
        }
    except Exception as e:
        return {
            "error": f"{type(e).__name__}: {e}",
            "trace": traceback.format_exc(limit=4),
        }


# ---------------------------------------------------------------------------
# Health & status
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_status() -> dict[str, Any]:
    """Quick health check — report whether TWS/Gateway is reachable.

    Tries the preferred port (env IBKR_PORT, 7497, or last-good) first
    and reports a one-line verdict.
    """
    from mcp_server.ibkr.connection import (
        _alt_port,
        _try_connect,
        preferred_port,
    )
    from ib_async import IB

    first = preferred_port()
    ib = IB()
    ok = None
    # We can't await here — use the synchronous connect with a tiny timeout
    try:
        # ib_async's connect() is sync; for the health check we accept the
        # default internal timeout
        ib.connect("127.0.0.1", first, clientId=99, readonly=True, timeout=4)
        ok = first
    except Exception:
        try:
            ib.disconnect()
        except Exception:
            pass
        ib2 = IB()
        try:
            ib2.connect("127.0.0.1", _alt_port(first), clientId=99, readonly=True, timeout=4)
            ok = _alt_port(first)
        except Exception:
            pass
        finally:
            try:
                ib2.disconnect()
            except Exception:
                pass

    if ok is None:
        return {
            "reachable": False,
            "port_tried": first,
            "port_fallback_tried": _alt_port(first),
            "verdict": "TWS / IB Gateway not reachable. Start it, enable API, and verify the port.",
        }
    return {
        "reachable": True,
        "port": ok,
        "verdict": "OK",
        "tier": "paper" if ok == 7497 else "live" if ok == 7496 else "custom",
    }


# ---------------------------------------------------------------------------
# Market data
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_quote(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Live quote: last, bid, ask, open/high/low/close, volume, halted, time."""
    return await _safe(market_data_mod.get_quote, symbol, port=port)


@mcp.tool()
async def ibkr_snapshot(symbols: list[str], port: int | None = None) -> dict[str, Any]:
    """Batch live quote across a list of symbols (one TWS connection)."""
    return await _safe(market_data_mod.get_snapshot, symbols, port=port)


@mcp.tool()
async def ibkr_historical(symbol: str,
duration: str = "1 Y",
bar_size: str = "1 day",
what_to_show: str = "TRADES",
use_rth: bool = True,
end_datetime: str | None = None,
port: int | None = None,) -> dict[str, Any]:
    """Historical OHLCV bars. duration/bar_size match IB strings
    ("1 Y" / "1 day", "6 M" / "1 hour", "30 D" / "5 mins", etc)."""
    return await _safe(market_data_mod.get_historical,
    symbol,
    duration=duration,
    bar_size=bar_size,
    what_to_show=what_to_show,
    use_rth=use_rth,
    end_datetime=end_datetime,
    port=port,)


@mcp.tool()
async def ibkr_contract_details(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Resolve a symbol to its IB contract spec (primary exchange, conId,
    multiplier, trading hours, industry classification)."""
    return await _safe(market_data_mod.get_contract_details, symbol, port=port)


# ---------------------------------------------------------------------------
# Fundamentals
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_fundamentals(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Latest fundamental snapshot (P/E, EPS, mkt cap, div yield, 52w
    hi/lo, margins, leverage ratios, etc.). Lagged ~15-30 minutes."""
    return await _safe(fundamentals_mod.get_fundamentals, symbol, port=port)


@mcp.tool()
async def ibkr_dividends(symbol: str, lookback_years: int = 5, port: int | None = None) -> dict[str, Any]:
    """Cash dividend payment history, last N years."""
    return await _safe(fundamentals_mod.get_dividends, symbol, lookback_years=lookback_years, port=port)


@mcp.tool()
async def ibkr_shortable(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Shortable share count for the equity (best-effort, may be unavailable)."""
    return await _safe(fundamentals_mod.get_shortable, symbol, port=port)


# ---------------------------------------------------------------------------
# Options
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_option_expiries(symbol: str, port: int | None = None) -> dict[str, Any]:
    """List tradeable option expiry dates for ``symbol``."""
    return await _safe(options_mod.get_expiries, symbol, port=port)


@mcp.tool()
async def ibkr_option_chain(symbol: str,
expiry: str,
strikes_around_atm: int = 5,
port: int | None = None,) -> dict[str, Any]:
    """Full call+put option chain for a single expiry, sliced around ATM."""
    return await _safe(options_mod.get_chain,
    symbol,
    expiry,
    strikes_around_atm=strikes_around_atm,
    port=port,)


@mcp.tool()
async def ibkr_option_greeks(symbol: str,
expiry: str,
strike: float,
right: str,
risk_free_rate: float = 0.045,
port: int | None = None,) -> dict[str, Any]:
    """Greeks for a single option strike. Tries TWS stream first, falls
    back to a Black-Scholes calc when the live stream is missing fields."""
    return await _safe(options_mod.compute_greeks,
    symbol,
    expiry,
    strike,
    right,
    risk_free_rate=risk_free_rate,
    port=port,)


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_market_scanner(scan_code: str = "top_pct_gainers_us",
number_of_rows: int = 25,
location: str = "STK.US",
instrument: str = "STK",
above_price: float | None = None,
above_volume: int | None = None,
market_cap_above: float | None = None,
market_cap_below: float | None = None,
port: int | None = None,) -> dict[str, Any]:
    """Run an IB market scanner.

    Presets: ``top_pct_gainers_us``, ``top_pct_losers_us``, ``most_active_us``,
    ``unusual_volume_us``, ``new_highs_us``, ``new_lows_us``,
    ``high_yield_dividend_us``, ``top_trade_ideas_long``, ``top_trade_ideas_short``.

    Pass an explicit TWS scan code (e.g. ``"TOP_PERC_GAIN"``) to override.
    """
    return await _safe(scanner_mod.run_scanner,
    scan_code=scan_code,
    number_of_rows=number_of_rows,
    location=location,
    instrument=instrument,
    above_price=above_price,
    above_volume=above_volume,
    market_cap_above=market_cap_above,
    market_cap_below=market_cap_below,
    port=port,)


# ---------------------------------------------------------------------------
# News
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_news(symbol: str,
lookback_days: int = 14,
provider: str = "BZ",
max_headlines: int = 50,
port: int | None = None,) -> dict[str, Any]:
    """Symbol-scoped IB news headlines. Tries the requested provider
    first, then walks Briefing.com / Dow Jones / Reuters as fallbacks."""
    return await _safe(news_mod.get_news,
    symbol,
    lookback_days=lookback_days,
    provider=provider,
    max_headlines=max_headlines,
    port=port,)


# ---------------------------------------------------------------------------
# Account / portfolio (read-only)
# ---------------------------------------------------------------------------


@mcp.tool()
async def ibkr_account_summary(port: int | None = None) -> dict[str, Any]:
    """Net liq, cash, buying power, margin — per managed account."""
    return await _safe(account_mod.get_account_summary, port=port)


@mcp.tool()
async def ibkr_account_values(tag: str | None = None, port: int | None = None) -> dict[str, Any]:
    """Raw AccountValue rows; pass ``tag`` (e.g. ``"BuyingPower"``) to filter."""
    return await _safe(account_mod.get_account_values, tag=tag, port=port)


@mcp.tool()
async def ibkr_portfolio(port: int | None = None) -> dict[str, Any]:
    """Current positions across all managed accounts (conId, qty, avg cost)."""
    return await _safe(account_mod.get_portfolio, port=port)


# ---------------------------------------------------------------------------
# Yahoo Finance (free fundamentals — fills the IBKR gap)
# ---------------------------------------------------------------------------


@mcp.tool()
async def yf_fundamentals(symbol: str) -> dict[str, Any]:
    """Free fundamental snapshot via Yahoo Finance — P/E, EPS, market cap,
    margins, growth, balance-sheet ratios. No subscription needed. Use this
    when ibkr_fundamentals is unavailable (IBKR deprecated API fundamentals
    for most accounts)."""
    return await _safe(yf_mod.get_fundamentals, symbol)


@mcp.tool()
async def yf_financials(symbol: str, statement: str = "income", period: str = "annual") -> dict[str, Any]:
    """Full financial statements via Yahoo Finance. statement: "income",
    "balance", or "cashflow". period: "annual" or "quarterly"."""
    return await _safe(yf_mod.get_financials, symbol, statement=statement, period=period)


@mcp.tool()
async def yf_quote(symbol: str) -> dict[str, Any]:
    """Quick current-price snapshot via Yahoo Finance (free, no TWS needed)."""
    return await _safe(yf_mod.get_quote, symbol)




def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
