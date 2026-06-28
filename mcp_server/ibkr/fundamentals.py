# ABOUTME: Fundamentals tools — IB reqFundamentalData (snapshot XML) wrapper
# ABOUTME: plus a dividend-history helper over historical bars.

"""Fundamentals surface for the IBKR MCP server.

IBKR's ``reqFundamentalData`` returns raw XML from Reuters fundamentals.
This module parses the most common fields (P/E, EPS, market cap, dividend
yield, 52-week range) and returns them as a JSON dict.

``ibkr_dividends`` walks historical ``ADJUSTED_LAST`` bars and pulls
dividend payments from the synthetic ``Dividends`` column that
``ib_async`` populates on each bar when you request
``whatToShow=ADJUSTED_LAST``.

Tools:

- ``ibkr_fundamentals(symbol)``   — P/E, EPS, mkt cap, div yield, 52w hi/lo, etc.
- ``ibkr_dividends(symbol, ...)`` — last N years of dividend payments
- ``ibkr_shortable(symbol)``      — shortable share count for an equity
"""

from __future__ import annotations

import asyncio
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any

from mcp_server.ibkr.connection import (
    ib_connection,
    qualify_contracts,
    stock_contract,
)


# --- XML field extractors ---------------------------------------------------


# These XPath fragments target the Reuters Fundamentals XML that IB serves
# via reqFundamentalData. Field names are stable across reporting periods.
_FUNDAMENTAL_FIELDS: dict[str, str] = {
    "ttmEPS": ".//ttmEPS",
    "eps": ".//EPS",
    "peRatio": ".//PERatio",
    "marketCap": ".//MarketCap",
    "dividendYield": ".//DividendYield",
    "dividendPerShare": ".//DividendPerShare",
    "dividendPayDate": ".//DividendPayDate",
    "dividendExDate": ".//DividendExDate",
    "beta": ".//Beta",
    "sharesOutstanding": ".//SharesOutstanding",
    "floatShares": ".//FloatShares",
    "high52w": ".//High52Week",
    "low52w": ".//Low52Week",
    "high52wDate": ".//High52WeekDate",
    "low52wDate": ".//Low52WeekDate",
    "movingAverage50d": ".//MA50Day",
    "movingAverage200d": ".//MA200Day",
    "priceToBook": ".//PriceBook",
    "priceToSales": ".//PriceSales",
    "roe": ".//ROE",
    "roa": ".//ROA",
    "revGrowth3y": ".//RevenueGrowth3Year",
    "epsGrowth3y": ".//EPSGrowth3Year",
    "grossMargin": ".//GrossMargin",
    "operatingMargin": ".//OperatingMargin",
    "profitMargin": ".//ProfitMargin",
    "bookValuePerShare": ".//BookValuePerShare",
    "cashPerShare": ".//CashPerShare",
    "debtToEquity": ".//DebtEquity",
    "currentRatio": ".//CurrentRatio",
    "quickRatio": ".//QuickRatio",
}


def _parse_xml(xml_str: str) -> dict[str, Any]:
    """Extract a flat dict from the Reuters Fundamentals XML blob.

    Most fields sit under ``<ratio>`` or ``<amount>``; we walk the tree
    once and grab whichever tag is present.
    """
    if not xml_str or not xml_str.strip():
        return {}
    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        return {"error": f"Could not parse fundamental XML: {e}"}

    # First pass: find the deepest parent that contains all the fields
    # we care about. ReutersFundamentals wraps everything in one root.
    out: dict[str, Any] = {}
    for key, xpath in _FUNDAMENTAL_FIELDS.items():
        node = root.find(xpath)
        if node is None:
            continue
        val: str | None = node.text or node.get("value")
        if val is None:
            continue
        val = val.strip()
        out[key] = val
    return out


def _coerce_numbers(d: dict[str, Any]) -> dict[str, Any]:
    """Best-effort numeric coercion on extracted values.

    IB returns values as strings, sometimes with currency prefixes
    (e.g. "USD1.23") and sometimes in scientific notation for very
    large or very small numbers. We try to leave human-readable numbers
    alone if they look like plain decimals, otherwise coerce.
    """
    out: dict[str, Any] = {}
    for k, v in d.items():
        if not isinstance(v, str):
            out[k] = v
            continue
        # Strip currency prefix
        cleaned = re.sub(r"^[A-Z]{3}", "", v).replace(",", "").strip()
        try:
            if "." in cleaned or "e" in cleaned.lower():
                out[k] = float(cleaned)
            else:
                out[k] = int(cleaned)
        except ValueError:
            out[k] = v
    return out


# --- public tool functions --------------------------------------------------


async def get_fundamentals(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Fetch IB/Reuters fundamental snapshot for ``symbol``.

    Returns a flat dict of common ratios. Note: IB fundamentals are
    ``ReportSnapshot`` (latest filing) — they are not as deep as
    FactSet/S&P Capital IQ but cover the basics.
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]
        # ReportSnapshot = most recent quarterly filing.
        # Note: IBKR has deprecated reqFundamentalData for most account
        # types. Many accounts now receive error 10358
        # ("Fundamentals data is not allowed").
        try:
            xml = await ib.reqFundamentalDataAsync(c, reportType="ReportSnapshot")
        except Exception as e:
            err = str(e).lower()
            if "not allowed" in err or "10358" in err:
                xml = None  # fall through to the empty-XML handler below
            else:
                raise

    # IBKR returns None/empty when fundamentals aren't entitled (error 10358
    # is logged but not raised). Handle both the exception and the silent case.
    if not xml or not xml.strip():
        return {
            "symbol": sym,
            "available": False,
            "error": (
                "IBKR fundamentals via reqFundamentalData are not available "
                "for this account. IBKR has deprecated API fundamental data "
                "for most account types. For fundamental ratios (P/E, EPS, "
                "margins, etc.), use the S&P Kensho MCP, FactSet MCP, or "
                "Daloopa MCP that are wired in this repo's financial-analysis "
                "plugin instead."
            ),
            "alternatives": [
                "S&P Kensho MCP (mcp__sp-global__*)",
                "FactSet MCP (mcp__factset__*)",
                "Daloopa MCP (mcp__daloopa__*)",
            ],
            "port": used_port,
        }

    parsed = _parse_xml(xml)
    parsed = _coerce_numbers(parsed)
    parsed["symbol"] = sym
    parsed["conId"] = c.conId
    parsed["primaryExchange"] = c.primaryExchange
    parsed["port"] = used_port
    parsed["generated_at"] = datetime.now(timezone.utc).isoformat()
    parsed["data_delay"] = "15-30 min"
    return parsed


async def get_dividends(
    symbol: str, lookback_years: int = 5, port: int | None = None
) -> dict[str, Any]:
    """Get dividend payment history for ``symbol``.

    Walks ``ADJUSTED_LAST`` daily bars and pulls the ``Dividends`` column
    populated by ``ib_async`` when an ex-dividend date is hit. Returns a
    list of cash payments in chronological order.
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    duration = f"{max(1, lookback_years)} Y"
    contract = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]
        bars = await ib.reqHistoricalDataAsync(
            c,
            endDateTime="",
            durationStr=duration,
            barSizeSetting="1 day",
            whatToShow="ADJUSTED_LAST",
            useRTH=True,
            formatDate=2,
        )

    payments: list[dict[str, Any]] = []
    for b in bars:
        amt = getattr(b, "dividends", None)
        # The synthetic dividends field is only non-zero on ex-div dates.
        if amt is not None and abs(amt) > 0:
            payments.append(
                {
                    "exDate": b.date.isoformat() if hasattr(b.date, "isoformat") else str(b.date),
                    "amount": float(amt),
                }
            )

    return {
        "symbol": sym,
        "lookback_years": lookback_years,
        "payment_count": len(payments),
        "payments": payments,
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_shortable(symbol: str, port: int | None = None) -> dict[str, Any]:
    """Return shortable share count for an equity (if the broker has it).

    IB's ``reqShortableShares`` is best-effort and may be unavailable for
    some symbols. We return a clearly-flagged result either way.
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]
        try:
            data = await asyncio.wait_for(
                ib.reqShortableSharesAsync(c), timeout=5.0
            )
        except asyncio.TimeoutError:
            return {
                "symbol": sym,
                "shortable_shares": None,
                "available": False,
                "note": "TWS did not return a shortable-shares response (may be unavailable for this symbol).",
                "port": used_port,
            }
        except Exception as e:
            return {
                "symbol": sym,
                "shortable_shares": None,
                "available": False,
                "note": f"Shortable request failed: {e}",
                "port": used_port,
            }

    return {
        "symbol": sym,
        "shortable_shares": int(data) if data is not None else None,
        "available": data is not None and int(data) > 0,
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
