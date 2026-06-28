# ABOUTME: Account / portfolio tools — read-only views into the connected
# ABOUTME: IBKR account. No order placement, no account mutations.

"""Account + portfolio surface for the IBKR MCP server.

These are *optional* for the research workflow — most equity research
skills just need market data. We expose them so the user can sanity-check
position sizing and account state when working on a thesis.

Tools:

- ``ibkr_account_summary()``   — net liq, cash, buying power, margin
- ``ibkr_account_values()``    — all ``AccountValue`` rows for a tag filter
- ``ibkr_portfolio()``         — current positions with conId / avg cost
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from mcp_server.ibkr.connection import (
    account_value_to_dict,
    ib_connection,
    position_to_dict,
)


# --- public tool functions --------------------------------------------------


async def get_account_summary(port: int | None = None) -> dict[str, Any]:
    """Return a small fixed set of account-summary fields.

    Returns one entry per managed account (paper accounts typically have
    one; live accounts with multiple managed accounts get one row each).
    """
    tags = (
        "NetLiquidation",
        "AvailableFunds",
        "BuyingPower",
        "TotalCashValue",
        "EquityWithLoanValue",
        "MaintenanceMargin",
        "InitialMargin",
        "AccountType",
        "Currency",
    )

    async with ib_connection(port=port) as (ib, used_port):
        # accountSummaryAsync() loads the summary on demand (~250ms) and returns
        # the cached AccountValue list. The sync accountSummary() would nest
        # loop.run_until_complete ("event loop already running"); and
        # cancelAccountSummary() does not exist in ib_async 2.x — the per-call
        # connection handles teardown on disconnect.
        raw = await ib.accountSummaryAsync()
        grouped: dict[str, dict[str, str]] = {}
        for av in raw:
            if av.tag not in tags:
                continue
            grouped.setdefault(av.account, {})[av.tag] = av.value

    accounts = [
        {"account": acct, **vals, "currency": vals.get("Currency", "USD")}
        for acct, vals in grouped.items()
    ]
    if not accounts:
        return {
            "port": used_port,
            "accounts": [],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "note": "No managed accounts returned — verify TWS is logged in and account is not in the middle of a session change.",
        }
    return {
        "port": used_port,
        "accounts": accounts,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_account_values(
    tag: str | None = None, port: int | None = None
) -> dict[str, Any]:
    """Return raw ``AccountValue`` rows, optionally filtered by ``tag`` substring.

    Useful for pulling all available fields when ``get_account_summary``
    isn't enough.
    """
    async with ib_connection(port=port) as (ib, used_port):
        values = ib.accountValues()
        if not values:
            # Force a refresh
            await ib.reqAccountUpdatesAsync(True)
            await asyncio.sleep(1.0)
            values = ib.accountValues()

    out = [account_value_to_dict(v) for v in values]
    if tag:
        tag_up = tag.upper()
        out = [v for v in out if tag_up in v["tag"].upper() or tag_up in v["tag"].upper()]

    return {
        "port": used_port,
        "tag_filter": tag,
        "count": len(out),
        "values": out,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_portfolio(port: int | None = None) -> dict[str, Any]:
    """Return all current positions (cash + margin) across managed accounts.

    Each position includes account, symbol, secType, exchange, currency,
    conId, position size, and average cost. Market value and unrealized
    PnL are NOT included here — pull them via ``get_market_value`` or
    add per-position market data on top of this list.
    """
    async with ib_connection(port=port) as (ib, used_port):
        positions = ib.positions()
        if not positions:
            # Force a refresh — first call often needs a tick
            await ib.reqPositionsAsync()
            await asyncio.sleep(1.0)
            positions = ib.positions()

    out = [position_to_dict(p) for p in positions]

    # Roll up a tiny aggregate for convenience
    by_account: dict[str, int] = {}
    by_sec: dict[str, int] = {}
    for p in out:
        by_account[p["account"]] = by_account.get(p["account"], 0) + 1
        by_sec[p["secType"]] = by_sec.get(p["secType"], 0) + 1

    return {
        "port": used_port,
        "position_count": len(out),
        "positions": out,
        "by_account": by_account,
        "by_sec_type": by_sec,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
