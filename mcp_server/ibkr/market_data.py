# ABOUTME: Market-data tools — live quote, historical OHLCV, contract details.
# ABOUTME: Thin wrappers around ib_async that normalize to JSON-ready dicts.

"""Market data surface for the IBKR MCP server.

Tools exposed:

- ``ibkr_quote(symbol)``             — last / bid / ask / volume / day range
- ``ibkr_snapshot(symbols)``         — batch quote for multiple symbols
- ``ibkr_historical(symbol, ...)``   — OHLCV bars over a date or duration window
- ``ibkr_contract_details(symbol)``  — full IB contract spec (primary exch, conId)

All tools are read-only and return JSON-serializable dicts. Timestamps
use America/New_York where applicable; we report them as ISO 8601 with
an offset.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from ib_async import Contract

from mcp_server.ibkr.connection import (
    ib_connection,
    qualify_contracts,
    stock_contract,
)


# --- helpers ----------------------------------------------------------------


def _bar_to_dict(bar) -> dict[str, Any]:
    """Normalize a ``BarData`` namedtuple to a JSON dict."""
    return {
        "date": bar.date.isoformat() if hasattr(bar.date, "isoformat") else str(bar.date),
        "open": float(bar.open) if bar.open is not None else None,
        "high": float(bar.high) if bar.high is not None else None,
        "low": float(bar.low) if bar.low is not None else None,
        "close": float(bar.close) if bar.close is not None else None,
        "volume": int(bar.volume) if bar.volume is not None else None,
        "barCount": int(bar.barCount) if getattr(bar, "barCount", None) is not None else None,
        "average": float(bar.average) if getattr(bar, "average", None) is not None else None,
    }


def _tick_to_dict(ticker) -> dict[str, Any]:
    """Normalize a live ``Ticker`` to a JSON-ready quote."""
    return {
        "symbol": ticker.contract.symbol,
        "conId": ticker.contract.conId,
        "last": float(ticker.last) if ticker.last == ticker.last else None,  # NaN -> None
        "bid": float(ticker.bid) if ticker.bid == ticker.bid else None,
        "ask": float(ticker.ask) if ticker.ask == ticker.ask else None,
        "bidSize": int(ticker.bidSize) if ticker.bidSize == ticker.bidSize and ticker.bidSize else None,
        "askSize": int(ticker.askSize) if ticker.askSize == ticker.askSize and ticker.askSize else None,
        "open": float(ticker.open) if ticker.open == ticker.open else None,
        "high": float(ticker.high) if ticker.high == ticker.high else None,
        "low": float(ticker.low) if ticker.low == ticker.low else None,
        "close": float(ticker.close) if ticker.close == ticker.close else None,
        "prevClose": float(ticker.prevClose) if getattr(ticker, 'prevClose', None) and ticker.prevClose == ticker.prevClose else None,
        "volume": int(ticker.volume) if ticker.volume else None,
        "halted": bool(ticker.halted) if ticker.halted is not None else None,
        "time": (
            ticker.time.astimezone(timezone.utc).isoformat()
            if getattr(ticker, "time", None) is not None
            else None
        ),
    }


# --- public tool functions --------------------------------------------------


async def get_quote(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Get a live quote for ``symbol`` (SMART-routed US stock by default)."""
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]
        ticker = ib.reqMktData(c, "", False, False)
        try:
            # Wait up to 3 seconds for first data to populate
            for _ in range(30):
                if ticker.last == ticker.last or ticker.bid == ticker.bid or ticker.ask == ticker.ask:
                    break
                await asyncio.sleep(0.1)
        finally:
            ib.cancelMktData(c)

    out = _tick_to_dict(ticker)
    out["symbol"] = sym
    out["port"] = used_port
    out["generated_at"] = datetime.now(timezone.utc).isoformat()
    return out


async def get_snapshot(symbols: list[str], port: int | None = None) -> dict[str, Any]:
    """Batch live quote for a list of symbols (one TWS connection)."""
    syms = [s.upper().strip() for s in symbols if s and s.strip()]
    if not syms:
        return {"error": "Empty symbol list", "results": []}

    contracts = [stock_contract(s) for s in syms]
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, *contracts)
        if not qualified:
            return {"error": "Could not resolve any contracts", "results": []}
        tickers = [ib.reqMktData(c, "", False, False) for c in qualified]
        try:
            for _ in range(40):
                if all(
                    t.last == t.last or t.bid == t.bid or t.ask == t.ask for t in tickers
                ):
                    break
                await asyncio.sleep(0.1)
        finally:
            for c in qualified:
                ib.cancelMktData(c)

    results = []
    for t in tickers:
        d = _tick_to_dict(t)
        d["symbol"] = t.contract.symbol
        results.append(d)

    return {
        "port": used_port,
        "count": len(results),
        "results": results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_historical(
    symbol: str,
    duration: str = "1 Y",
    bar_size: str = "1 day",
    what_to_show: str = "TRADES",
    use_rth: bool = True,
    end_datetime: str | None = None,
    port: int | None = None,
) -> dict[str, Any]:
    """Fetch OHLCV historical bars.

    Args:
        symbol: ticker
        duration: e.g. "1 Y", "6 M", "30 D", "1 W", "1 Y" — IB duration strings
        bar_size: e.g. "1 day", "1 hour", "5 mins", "1 min"
        what_to_show: "TRADES", "ADJUSTED_LAST", "MIDPOINT", "BID", "ASK"
        use_rth: regular trading hours only
        end_datetime: ISO timestamp or None for "now"
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    end = end_datetime or ""
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]
        bars = await ib.reqHistoricalDataAsync(
            c,
            endDateTime=end,
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow=what_to_show,
            useRTH=int(use_rth),
            formatDate=2,
        )

    return {
        "symbol": sym,
        "conId": c.conId,
        "duration": duration,
        "bar_size": bar_size,
        "what_to_show": what_to_show,
        "use_rth": use_rth,
        "bar_count": len(bars),
        "bars": [_bar_to_dict(b) for b in bars],
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_contract_details(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Resolve a symbol to its full IB ContractDetails.

    Returns the primary exchange, conId, trading class, multiplier, and
    a list of all available single-security contract descriptions
    (different listing venues, currencies, etc.).
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        details = await ib.reqContractDetailsAsync(contract)

    out_details = []
    for d in details:
        out_details.append(
            {
                "symbol": d.contract.symbol,
                "secType": d.contract.secType,
                "exchange": d.contract.exchange,
                "primaryExchange": d.contract.primaryExchange,
                "currency": d.contract.currency,
                "conId": d.contract.conId,
                "tradingClass": d.contract.tradingClass,
                "multiplier": d.contract.multiplier,
                "longName": d.longName,
                "industry": d.industry,
                "category": d.category,
                "subcategory": d.subcategory,
                "minTick": d.minTick,
                "timeZoneId": d.timeZoneId,
                "tradingHours": d.tradingHours,
                "liquidHours": d.liquidHours,
            }
        )

    return {
        "symbol": sym,
        "count": len(out_details),
        "details": out_details,
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
