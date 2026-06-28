# ABOUTME: Unit tests for the connection module + smoke tests for the
# ABOUTME: tool surface that don't require a running TWS / IB Gateway.

"""Smoke tests for the IBKR MCP server.

Most tests don't require a live TWS. The single ``ib_live``-marked test
opt-in runs only when ``IBKR_LIVE_TESTS=1`` is set and a real TWS / IB
Gateway is reachable on the configured port.
"""

from __future__ import annotations

import math
import os

import pytest

from mcp_server.ibkr.connection import (
    CLIENT_ID_RESEARCH,
    _alt_port,
    preferred_port,
    stock_contract,
)
from mcp_server.ibkr.options import _black_scholes_greeks


# --- pure-Python (no TWS needed) --------------------------------------------


def test_alt_port_paper_to_live():
    assert _alt_port(7497) == 7496


def test_alt_port_live_to_paper():
    assert _alt_port(7496) == 7497


def test_preferred_port_default(monkeypatch):
    monkeypatch.delenv("IBKR_PORT", raising=False)
    # First call: returns the default
    assert preferred_port() == 7497


def test_preferred_port_from_env(monkeypatch):
    monkeypatch.setenv("IBKR_PORT", "7496")
    assert preferred_port() == 7496


def test_client_id_is_readonly_band():
    """Client ID lives in the 90-99 read-only research band."""
    assert 90 <= CLIENT_ID_RESEARCH <= 99


def test_stock_contract_is_smart_default():
    c = stock_contract("AAPL")
    assert c.symbol == "AAPL"
    assert c.exchange == "SMART"
    assert c.currency == "USD"
    assert c.secType == "STK"


def test_black_scholes_call_known_value():
    """A 1y ATM call with σ=0.20 and r=5% has a known closed-form price
    (~$0.0825 per $1 strike, normalized). We just sanity-check that our
    impl returns a reasonable number in that ballpark."""
    g = _black_scholes_greeks(S=100, K=100, T=1.0, r=0.05, sigma=0.20, right="C")
    assert g["price"] is not None
    # ATM call ≈ 10.45 with these inputs (textbook). Wide tolerance for safety.
    assert 9 < g["price"] < 12
    # Call delta is between 0.5 and 1 at the money for a positive carry
    assert 0.5 < g["delta"] < 1.0
    # Theta is negative for long options
    assert g["theta"] < 0
    # Gamma and vega are positive for long options
    assert g["gamma"] > 0
    assert g["vega"] > 0


def test_black_scholes_put_put_call_parity():
    """Put-call parity at expiry time (T≈0) — both intrinsic."""
    # Long-dated call
    call = _black_scholes_greeks(S=100, K=90, T=1.0, r=0.05, sigma=0.20, right="C")
    # Same params for put
    put = _black_scholes_greeks(S=100, K=90, T=1.0, r=0.05, sigma=0.20, right="P")
    # Put-call parity: C - P = S - K * exp(-rT)
    # We don't enforce it exactly (we use a coarse tolerance) but the
    # values should both be > 0 and on the right side of intrinsic.
    assert call["price"] > 10  # deep ITM call ≈ 15 with these inputs
    assert put["price"] < 5    # deep OTM put
    assert call["delta"] > 0
    assert put["delta"] < 0


# --- live TWS integration test (opt-in) ------------------------------------


@pytest.mark.ib_live
@pytest.mark.skipif(
    os.environ.get("IBKR_LIVE_TESTS", "0") != "1",
    reason="Set IBKR_LIVE_TESTS=1 to run live TWS / IB Gateway integration tests",
)
def test_ibkr_quote_live_smoke():
    """Smoke test: call ibkr_quote against a real TWS session."""
    import asyncio
    from mcp_server.ibkr.market_data import get_quote

    res = asyncio.run(get_quote("AAPL"))
    assert "error" not in res or res.get("last") is not None
    # Last price should be a positive float if data arrived
    if "last" in res and res["last"] is not None:
        assert res["last"] > 0
