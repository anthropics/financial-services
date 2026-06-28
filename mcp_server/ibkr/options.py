# ABOUTME: Options surface — chains, expiries, greeks, FOP/OPT detail.

"""Options surface for the IBKR MCP server.

Tools:

- ``ibkr_option_expiries(symbol)``  — list of tradeable expiry dates
- ``ibkr_option_chain(symbol, expiry)`` — full call+put chain with greeks
- ``ibkr_option_greeks(...)``       — manual greeks calc on a single contract
                                     (for the rare case where TWS Greeks
                                     aren't available)

All options are equity options on the underlying stock by default. For
FOPs, the user can pass ``sec_type="FUT"`` + ``fut_expiry`` and we'll
build the option on the front-month future. Kept simple — this skill is
about research, not strategy.
"""

from __future__ import annotations

import asyncio
import math
from datetime import datetime, timezone
from typing import Any

from ib_async import Contract, Option

from mcp_server.ibkr.connection import (
    ib_connection,
    qualify_contracts,
    stock_contract,
)


# --- helpers ----------------------------------------------------------------


def _option_contract(
    symbol: str,
    expiry: str,
    strike: float,
    right: str,
    exchange: str = "SMART",
    currency: str = "USD",
) -> Option:
    """Build an Option contract for a single strike on a stock."""
    return Option(symbol.upper(), expiry, float(strike), right.upper(), exchange)


def _normalize_greeks(ticker) -> dict[str, Any]:
    """Pull IB-computed greeks off a market-data ticker.

    ib_async stores option Greeks in ``ticker.modelGreeks`` (an
    OptionComputation), not as direct attributes.
    """
    g = getattr(ticker, 'modelGreeks', None)
    g = g if g is not None else type('G', (), {'impliedVol': float('nan'), 'delta': float('nan'), 'gamma': float('nan'), 'theta': float('nan'), 'vega': float('nan'), 'undPrice': float('nan')})()
    return {
        "delta": float(g.delta) if g.delta == g.delta else None,
        "gamma": float(g.gamma) if g.gamma == g.gamma else None,
        "theta": float(g.theta) if g.theta == g.theta else None,
        "vega": float(g.vega) if g.vega == g.vega else None,
        "impliedVolatility": float(g.impliedVol) if g.impliedVol == g.impliedVol else None,
        "undPrice": float(g.undPrice) if g.undPrice == g.undPrice else None,
        "last": float(ticker.last) if ticker.last == ticker.last else None,
        "bid": float(ticker.bid) if ticker.bid == ticker.bid else None,
        "ask": float(ticker.ask) if ticker.ask == ticker.ask else None,
    }


def _black_scholes_greeks(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    right: str,
) -> dict[str, float]:
    """Closed-form Black-Scholes greeks for an option.

    Used as a fallback when the TWS stream doesn't populate ``delta``
    etc. (often the case for illiquid strikes). Returns a dict with
    ``delta``, ``gamma``, ``theta``, ``vega``, ``price``.
    """
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return {
            "price": None,
            "delta": None,
            "gamma": None,
            "theta": None,
            "vega": None,
        }

    # Standard normal pdf / cdf
    def n_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    def n_pdf(x: float) -> float:
        return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    is_call = right.upper().startswith("C")

    if is_call:
        price = S * n_cdf(d1) - K * math.exp(-r * T) * n_cdf(d2)
        delta = n_cdf(d1)
        theta = (
            -(S * n_pdf(d1) * sigma) / (2 * math.sqrt(T))
            - r * K * math.exp(-r * T) * n_cdf(d2)
        ) / 365.0
    else:
        price = K * math.exp(-r * T) * n_cdf(-d2) - S * n_cdf(-d1)
        delta = n_cdf(d1) - 1.0
        theta = (
            -(S * n_pdf(d1) * sigma) / (2 * math.sqrt(T))
            + r * K * math.exp(-r * T) * n_cdf(-d2)
        ) / 365.0

    gamma = n_pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * n_pdf(d1) * math.sqrt(T) / 100.0  # per 1 vol pt

    return {
        "price": round(price, 4),
        "delta": round(delta, 4),
        "gamma": round(gamma, 4),
        "theta": round(theta, 4),
        "vega": round(vega, 4),
    }


# --- public tool functions --------------------------------------------------


async def get_expiries(symbol: str, port: int | None = None) -> dict[str, Any]:
    """List tradeable option expiry dates for ``symbol``."""
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    contract = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        qualified = await qualify_contracts(ib, contract)
        if not qualified:
            return {"error": f"Could not resolve contract for {sym}", "symbol": sym}
        c = qualified[0]
        chains = await ib.reqSecDefOptParamsAsync(c.symbol, "", c.secType, c.conId)

    expiries: set[str] = set()
    exchanges: set[str] = set()
    for chain in chains:
        exchanges.add(chain.exchange)
        expiries.update(chain.expirations)

    return {
        "symbol": sym,
        "conId": c.conId,
        "exchanges": sorted(exchanges),
        "expiries": sorted(expiries),
        "expiry_count": len(expiries),
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_chain(
    symbol: str,
    expiry: str,
    strikes_around_atm: int = 5,
    port: int | None = None,
) -> dict[str, Any]:
    """Get the full option chain (calls + puts) for ``symbol`` at ``expiry``.

    Args:
        symbol: underlying
        expiry: IB expiry string (e.g. "20251219")
        strikes_around_atm: how many strikes above and below ATM to return
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
        # Pull a live quote on the underlying so we can pick strikes around ATM
        ticker = ib.reqMktData(c, "", False, False)
        try:
            for _ in range(30):
                if ticker.last == ticker.last or ticker.bid == ticker.bid:
                    break
                await asyncio.sleep(0.1)
            spot = (
                float(ticker.last) if ticker.last == ticker.last
                else float(ticker.close) if ticker.close == ticker.close
                else None
            )
        finally:
            ib.cancelMktData(c)

        # Discover the strike ladder for this expiry
        params = await ib.reqSecDefOptParamsAsync(c.symbol, "", c.secType, c.conId)
        strikes: list[float] = []
        chain_exchange = "SMART"
        for p in params:
            if expiry in p.expirations and p.exchange == "SMART":
                strikes = sorted({float(s) for s in p.strikes})
                chain_exchange = p.exchange
                break
        if not strikes:
            for p in params:
                if expiry in p.expirations:
                    strikes = sorted({float(s) for s in p.strikes})
                    chain_exchange = p.exchange
                    break

    if spot is None or not strikes:
        return {
            "symbol": sym, "expiry": expiry, "spot": spot,
            "error": "Could not determine spot price or strikes",
            "port": used_port,
        }

    # Pick the strikes nearest ATM
    atm_idx = min(range(len(strikes)), key=lambda i: abs(strikes[i] - spot))
    lo = max(0, atm_idx - strikes_around_atm)
    hi = min(len(strikes), atm_idx + strikes_around_atm + 1)
    selected = strikes[lo:hi]

    # Build contracts using the chain's exchange (not hardcoded SMART)
    call_contracts = [
        _option_contract(sym, expiry, k, "C", exchange=chain_exchange) for k in selected
    ]
    put_contracts = [
        _option_contract(sym, expiry, k, "P", exchange=chain_exchange) for k in selected
    ]

    async with ib_connection(port=port) as (ib, _port2):
        # Qualify option contracts — filter out any that IBKR couldn't resolve
        opt_q = await ib.qualifyContractsAsync(*call_contracts, *put_contracts)
        opt_q = [o for o in opt_q if o is not None and o.conId > 0]
        if not opt_q:
            return {
                "symbol": sym, "expiry": expiry, "error": "No valid option contracts found for this expiry/strike range",
                "port": used_port,
            }
        # Subscribe to market data with greeks (tick type 106 = Greeks)
        opt_tickers = [ib.reqMktData(o, "106", False, False) for o in opt_q]
        try:
            for _ in range(40):
                def has_delta(t):
                    g = getattr(t, 'modelGreeks', None)
                    return g is not None and g.delta == g.delta
                if any(has_delta(t) for t in opt_tickers if t.contract.right == "C") and \
                   any(has_delta(t) for t in opt_tickers if t.contract.right == "P"):
                    break
                await asyncio.sleep(0.1)
        finally:
            for o in opt_q:
                try: ib.cancelMktData(o)
                except: pass

    calls = []
    puts = []
    for t in opt_tickers:
        record = {
            "strike": float(t.contract.strike),
            "conId": t.contract.conId,
            **_normalize_greeks(t),
        }
        if t.contract.right == "C":
            calls.append(record)
        else:
            puts.append(record)
    calls.sort(key=lambda r: r["strike"])
    puts.sort(key=lambda r: r["strike"])

    return {
        "symbol": sym,
        "expiry": expiry,
        "spot": spot,
        "atm_strike": strikes[atm_idx],
        "strikes": selected,
        "calls": calls,
        "puts": puts,
        "port": used_port,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


async def compute_greeks(
    symbol: str,
    expiry: str,
    strike: float,
    right: str,
    risk_free_rate: float = 0.045,
    port: int | None = None,
) -> dict[str, Any]:
    """Compute greeks for a single option strike.

    Tries the live TWS stream first; falls back to a Black-Scholes calc
    if the stream returns no greeks (common for illiquid strikes).
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    opt = _option_contract(sym, expiry, float(strike), right)
    underlying = stock_contract(sym)
    async with ib_connection(port=port) as (ib, used_port):
        u_q = await qualify_contracts(ib, underlying)
        o_q = await qualify_contracts(ib, opt)
        if not u_q or not o_q:
            return {"error": f"Could not resolve contracts for {sym} {expiry} {strike}{right}"}
        u, o = u_q[0], o_q[0]
        t_under = ib.reqMktData(u, "", False, False)
        t_opt = ib.reqMktData(o, "106", False, False)
        try:
            for _ in range(40):
                spot_ready = t_under.last == t_under.last or t_under.close == t_under.close
                if spot_ready and t_opt.last == t_opt.last:
                    break
                await asyncio.sleep(0.1)
            spot = (
                float(t_under.last) if t_under.last == t_under.last
                else float(t_under.close) if t_under.close == t_under.close
                else None
            )
        finally:
            ib.cancelMktData(u)
            ib.cancelMktData(o)

    if spot is None:
        return {"error": "Could not get underlying spot price", "symbol": sym}

    # Time to expiry in years (act/365)
    exp_date = datetime.strptime(expiry, "%Y%m%d").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    T = max((exp_date - now).total_seconds() / (365.0 * 24 * 3600), 0.0)

    live = _normalize_greeks(t_opt)
    out: dict[str, Any] = {
        "symbol": sym,
        "expiry": expiry,
        "strike": float(strike),
        "right": right.upper(),
        "spot": spot,
        "T_years": round(T, 4),
        "risk_free_rate": risk_free_rate,
        "live_greeks": live,
        "port": used_port,
    }

    # Fallback BS calc if live greeks are missing
    if live.get("delta") is None or (live.get("impliedVolatility") or 0) <= 0:
        # Use the live last as the option price and a reasonable IV
        opt_price = live.get("last") or live.get("bid") or live.get("ask")
        iv = live.get("impliedVolatility") or 0.30  # last-resort default
        out["bs_fallback"] = _black_scholes_greeks(spot, float(strike), T, risk_free_rate, iv, right)
        out["bs_fallback"]["used_iv"] = iv
        out["bs_fallback"]["used_price"] = opt_price
    return out
