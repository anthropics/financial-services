# ABOUTME: IB market scanner — wraps reqScannerSubscription with a small
# ABOUTME: set of curated, equity-research-useful scan codes.

"""IB market scanner wrapper for the research surface.

TWS exposes hundreds of predefined scan codes (`SCAN codes`). Rather
than ship an enum, this module hard-codes a small set that matches the
most common equity-research screening needs — top % movers, unusual
volume, high IV, gap-up / gap-down, etc.

Users who need a custom code can pass ``scan_code`` explicitly; the
``location`` and ``number_of_rows`` parameters stay sensible defaults.

Tool: ``ibkr_market_scanner(scan_code, location, ...)``
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ib_async import ScannerSubscription

from mcp_server.ibkr.connection import ib_connection


# Curated scan codes — pulled from TWS API reference doc.
# https://interactivebrokers.github.io/tws-api/scanner_subscrip.html
SCAN_PRESETS: dict[str, dict[str, Any]] = {
    "top_pct_gainers_us": {
        "scanCode": "TOP_PERC_GAIN",
        "instrument": "STK",
        "locationCode": "STK.US",
        "abovePrice": "5",
        "aboveVolume": "100000",
    },
    "top_pct_losers_us": {
        "scanCode": "TOP_PERC_LOSE",
        "instrument": "STK",
        "locationCode": "STK.US",
        "abovePrice": "5",
        "aboveVolume": "100000",
    },
    "most_active_us": {
        "scanCode": "MOST_ACTIVE",
        "instrument": "STK",
        "locationCode": "STK.US",
        "abovePrice": "5",
    },
    "unusual_volume_us": {
        "scanCode": "HOT_BY_VOLUME",
        "instrument": "STK",
        "locationCode": "STK.US",
        "abovePrice": "5",
    },
    "new_highs_us": {
        "scanCode": "HIGH_VS_13W_HI",
        "instrument": "STK",
        "locationCode": "STK.US",
        "abovePrice": "5",
    },
    "new_lows_us": {
        "scanCode": "LOW_VS_13W_LO",
        "instrument": "STK",
        "locationCode": "STK.US",
        "abovePrice": "5",
    },
    "high_iv_us": {
        "scanCode": "HIGH_OPT_VOLUME_PUT_CALL_RATIO",
        "instrument": "STK",
        "locationCode": "STK.US",
    },
    "high_yield_dividend_us": {
        "scanCode": "HIGH_DIVIDEND_YIELD",
        "instrument": "STK",
        "locationCode": "STK.US",
    },
    "top_trade_ideas_long": {
        "scanCode": "TOP_TRADE_IDEAS_LONG",
        "instrument": "STK",
        "locationCode": "STK.US",
    },
    "top_trade_ideas_short": {
        "scanCode": "TOP_TRADE_IDEAS_SHORT",
        "instrument": "STK",
        "locationCode": "STK.US",
    },
}


async def run_scanner(
    scan_code: str = "top_pct_gainers_us",
    number_of_rows: int = 25,
    location: str = "STK.US",
    instrument: str = "STK",
    above_price: float | None = None,
    above_volume: int | None = None,
    market_cap_above: float | None = None,
    market_cap_below: float | None = None,
    port: int | None = None,
) -> dict[str, Any]:
    """Run an IB market scanner.

    Use one of the ``SCAN_PRESETS`` (e.g. "top_pct_gainers_us") for the
    most common equity-research queries, OR pass an explicit ``scan_code``
    that maps to a TWS API scan code (e.g. ``"TOP_PERC_GAIN"``).
    """
    preset = SCAN_PRESETS.get(scan_code)
    if preset:
        sub = ScannerSubscription(
            numberOfRows=number_of_rows,
            instrument=preset.get("instrument", instrument),
            locationCode=preset.get("locationCode", location),
            scanCode=preset.get("scanCode", scan_code),
        )
        # Apply preset filters
        for k, v in preset.items():
            if hasattr(sub, k) and k not in ("instrument", "locationCode", "scanCode"):
                setattr(sub, k, v)
        used_preset = scan_code
    else:
        # Treat input as a literal TWS scan code
        sub = ScannerSubscription(
            numberOfRows=number_of_rows,
            instrument=instrument,
            locationCode=location,
            scanCode=scan_code,
        )
        used_preset = None

    if above_price is not None:
        sub.abovePrice = above_price
    if above_volume is not None:
        sub.aboveVolume = above_volume
    if market_cap_above is not None:
        sub.marketCapAbove = market_cap_above
    if market_cap_below is not None:
        sub.marketCapBelow = market_cap_below

    async with ib_connection(port=port) as (ib, used_port):
        # reqScannerSubscription returns a list of ScanData
        data = await ib.reqScannerSubscriptionAsync(sub, [])

    out: list[dict[str, Any]] = []
    for d in data:
        # ScanData has contractDetails and rank; details fields vary
        c = d.contractDetails.contract if d.contractDetails else None
        out.append(
            {
                "rank": d.rank,
                "symbol": c.symbol if c else None,
                "conId": c.conId if c else None,
                "exchange": c.exchange if c else None,
                "primaryExchange": c.primaryExchange if c else None,
                "currency": c.currency if c else None,
                "distance": d.distance,
                "benchmark": d.benchmark,
                "projection": d.projection,
                "legsStr": d.legsStr,
            }
        )

    return {
        "preset": used_preset,
        "scan_code": sub.scanCode,
        "location": sub.locationCode,
        "instrument": sub.instrument,
        "count": len(out),
        "rows": out,
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
