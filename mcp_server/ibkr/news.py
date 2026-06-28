# ABOUTME: News surface — IB news providers (BZ, DJ-N, etc.) headline feed
# ABOUTME: filtered to a single symbol's contract.

"""IB news surface.

IB's ``reqNewsBulletin`` is system-wide; we want symbol-scoped headlines.
We use ``reqHistoricalNews`` which lets us pull a per-contract news
timeline from a named IB news provider (default: ``BZ`` = Briefing.com
Trader; fallback: ``DJ-N`` = Dow Jones newswires if you have a
subscription).

Tool: ``ibkr_news(symbol, provider, lookback_days)``
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

from mcp_server.ibkr.connection import (
    ib_connection,
    qualify_contracts,
    stock_contract,
)

# Common news provider codes — IB exposes a list via reqNewsProviders.
DEFAULT_PROVIDERS: tuple[str, ...] = ("BZ", "DJ-N", "RS", "BRFG")


async def get_news(
    symbol: str,
    lookback_days: int = 14,
    provider: str = "BZ",
    max_headlines: int = 50,
    port: int | None = None,
) -> dict[str, Any]:
    """Fetch historical news headlines for ``symbol``.

    Args:
        symbol: ticker
        lookback_days: how far back to search
        provider: IB news provider code (BZ, DJ-N, RS, etc.)
        max_headlines: cap on the response

    If the requested provider returns no headlines, the function tries
    the rest of ``DEFAULT_PROVIDERS`` in order and returns whichever has
    data. The response reports which provider actually served the data.
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=max(1, lookback_days))

    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]

        # Try the requested provider first, then walk the default list.
        providers_to_try = [provider] + [p for p in DEFAULT_PROVIDERS if p != provider]
        served_by = None
        headlines: list[Any] = []
        for p in providers_to_try:
            try:
                articles = await asyncio.wait_for(
                    ib.reqHistoricalNewsAsync(
                        c.conId,
                        p,
                        start.strftime("%Y%m%d %H:%M:%S"),
                        end.strftime("%Y%m%d %H:%M:%S"),
                        max_headlines,
                    ),
                    timeout=8.0,
                )
            except (asyncio.TimeoutError, Exception):
                articles = []
            if articles:
                headlines = articles
                served_by = p
                break

    out: list[dict[str, Any]] = []
    for h in headlines:
        out.append(
            {
                "time": (
                    h.time.isoformat() if getattr(h, "time", None) is not None else None
                ),
                "providerCode": h.providerCode,
                "articleId": h.articleId,
                "headline": h.headline,
                "extraData": getattr(h, "extraData", None),
            }
        )

    return {
        "symbol": sym,
        "lookback_days": lookback_days,
        "provider_requested": provider,
        "served_by": served_by,
        "count": len(out),
        "headlines": out,
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
