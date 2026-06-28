# ABOUTME: Shared IB connection utilities — context manager with port fallback,
# ABOUTME: contract helpers, and request wrappers used by every tool module.

"""IBKR connection primitives.

A single ``ib_connection`` async context manager is the only thing every
tool needs to know about. It connects to TWS / IB Gateway, yields the
``IB`` instance, and disconnects on exit.

Port fallback: paper (7497) is the default. If the configured port fails
to connect, the next call retries on the other port. The first port to
succeed is remembered for the lifetime of the process via
``last_good_port`` — subsequent calls prefer it.

Only market-data + account reads are wired in. The server does not place
or cancel orders, so all client IDs are read-only.
"""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

from ib_async import IB, Contract, Stock


# Documented clientId allocation — one source of truth for every tool.
# Range 90-99 reserved for the IBKR MCP research surface.
CLIENT_ID_RESEARCH = 90

# Port fallback state — process-local.
_last_good_port: int | None = None
_last_good_account: str | None = None


def preferred_port(default: int = 7497) -> int:
    """Return the port to try first. 7497 (paper) by default.

    If a previous call in this process discovered a working port, prefer
    that — saves a connect failure on every tool invocation.
    """
    if _last_good_port is not None:
        return _last_good_port
    return int(os.environ.get("IBKR_PORT", default))


def _alt_port(port: int) -> int:
    """The other standard port. 7497 <-> 7496."""
    return 7496 if port == 7497 else 7497


async def _try_connect(ib: IB, port: int, client_id: int, timeout: float) -> bool:
    """Try to connect once. Returns True on success, False on failure."""
    try:
        await asyncio.wait_for(
            ib.connectAsync("127.0.0.1", port, clientId=client_id, readonly=True),
            timeout=timeout,
        )
        return ib.isConnected()
    except Exception:
        try:
            if ib.isConnected():
                ib.disconnect()
        except Exception:
            pass
        return False


@asynccontextmanager
async def ib_connection(
    port: int | None = None,
    client_id: int = CLIENT_ID_RESEARCH,
    timeout: float = 8.0,
    allow_fallback: bool = True,
):
    """Async context manager around an ``IB`` connection.

    Yields ``(ib, used_port)``. On exit, disconnects.

    Tries ``port`` first; if that fails and ``allow_fallback`` is True,
    retries the other standard port (7497 <-> 7496). The first port to
    succeed becomes the preferred port for subsequent calls in this
    process.
    """
    global _last_good_port

    first_port = port if port is not None else preferred_port()
    ib = IB()

    connected = await _try_connect(ib, first_port, client_id, timeout)
    used_port = first_port
    if not connected and allow_fallback:
        alt = _alt_port(first_port)
        connected = await _try_connect(ib, alt, client_id, timeout)
        if connected:
            used_port = alt

    if not connected:
        raise ConnectionError(
            f"Could not connect to TWS / IB Gateway on port {first_port}"
            + (f" or {alt}" if allow_fallback else "")
            + ". Is TWS running with API enabled?"
        )

    _last_good_port = used_port

    # Request delayed market data (15 min) by default — works without a
    # real-time market data subscription. Type 1 = live, 3 = delayed.
    try:
        ib.reqMarketDataType(3)
    except Exception:
        pass

    try:
        yield ib, used_port
    finally:
        try:
            if ib.isConnected():
                ib.disconnect()
        except Exception:
            pass


def stock_contract(symbol: str, exchange: str = "SMART", currency: str = "USD") -> Stock:
    """Build a Stock contract for the given symbol.

    Defaults to SMART routing on USD exchanges — matches what retail TWS
    users see. Override ``exchange`` for non-US listings.
    """
    return Stock(symbol.upper(), exchange, currency)


def qualifier(contract: Contract) -> Contract:
    """Resolve a contract to its IB-conId and primary exchange.

    Required before requesting market data on most contracts.
    """
    # ``qualifyContracts`` accepts varargs of Contract. We import lazily
    # because some users may run a thin server that doesn't need this.
    from ib_async import Contract as _C  # noqa: F401

    return contract  # placeholder — see qualify_contracts()


async def qualify_contracts(ib: IB, *contracts: Contract) -> list[Contract]:
    """Resolve contracts to their IB-conId and primary exchange.

    Wraps ``ib.qualifyContractsAsync`` with a timeout and returns a
    flat list of resolved contracts.
    """
    from ib_async import util

    return await asyncio.wait_for(
        ib.qualifyContractsAsync(*contracts), timeout=10.0
    )


def account_value_to_dict(av: Any) -> dict[str, Any]:
    """Normalize an ``AccountValue`` namedtuple to a plain dict."""
    return {
        "account": av.account,
        "tag": av.tag,
        "value": av.value,
        "currency": av.currency,
        "modelCode": av.modelCode,
    }


def position_to_dict(p: Any) -> dict[str, Any]:
    """Normalize a ``Position`` to a plain dict."""
    return {
        "account": p.account,
        "symbol": p.contract.symbol,
        "secType": p.contract.secType,
        "exchange": p.contract.exchange,
        "currency": p.contract.currency,
        "conId": p.contract.conId,
        "position": float(p.position),
        "avgCost": float(p.avgCost),
    }
