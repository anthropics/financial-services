# ABOUTME: Free fundamental-data tools via yfinance — no subscription needed.
# ABOUTME: Fills the gap left by IBKR's deprecated reqFundamentalData.

"""yfinance fundamental-data surface for the MCP server.

These tools wrap the free ``yfinance`` library (Yahoo Finance) to provide
the fundamental ratios, financial statements, and market data that IBKR
no longer exposes via API. No subscription required.

Tools:

- ``yf_fundamentals(symbol)``   — P/E, EPS, market cap, margins, growth, balance sheet ratios
- ``yf_financials(symbol, ...)`` — income statement / balance sheet / cash flow (annual or quarterly)
- ``yf_quote(symbol)``           — current price, bid/ask, day range, market cap, P/E
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import yfinance as yf


# --- helpers ----------------------------------------------------------------


def _safe_float(val: Any) -> float | None:
    """Coerce to float, returning None for NaN / None / missing."""
    try:
        if val is None:
            return None
        f = float(val)
        return f if f == f else None  # NaN check
    except (ValueError, TypeError):
        return None


def _df_to_dict(df) -> dict[str, Any]:
    """Convert a pandas DataFrame (from yfinance) to a JSON-ready dict.

    Columns are dates (or period labels), rows are line items.
    Returns {line_item: {date: value}}.
    """
    if df is None or df.empty:
        return {}
    result: dict[str, Any] = {}
    for idx in df.index:
        row = df.loc[idx]
        result[str(idx)] = {
            str(col): _safe_float(row[col]) for col in df.columns
        }
    return result


# --- public tool functions --------------------------------------------------


def get_fundamentals(symbol: str) -> dict[str, Any]:
    """Fetch fundamental snapshot via Yahoo Finance (free, no subscription).

    Returns P/E, EPS, market cap, margins, growth rates, balance-sheet
    ratios, and key company info.
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    ticker = yf.Ticker(sym)
    info = ticker.info

    if not info or (isinstance(info, dict) and len(info) < 3):
        return {"error": f"No data returned for {sym}. Verify the ticker."}

    result: dict[str, Any] = {
        "symbol": sym,
        "source": "yfinance (Yahoo Finance)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_delay": "delayed (Yahoo Finance)",
    }

    # Valuation
    result["valuation"] = {
        "marketCap": _safe_float(info.get("marketCap")),
        "enterpriseValue": _safe_float(info.get("enterpriseValue")),
        "trailingPE": _safe_float(info.get("trailingPE")),
        "forwardPE": _safe_float(info.get("forwardPE")),
        "pegRatio": _safe_float(info.get("pegRatio")),
        "priceToSalesTrailing12Months": _safe_float(info.get("priceToSalesTrailing12Months")),
        "priceToBook": _safe_float(info.get("priceToBook")),
        "evToRevenue": _safe_float(info.get("enterpriseToRevenue")),
        "evToEbitda": _safe_float(info.get("enterpriseToEbitda")),
    }

    # Profitability
    result["profitability"] = {
        "trailingEPS": _safe_float(info.get("trailingEps")),
        "forwardEPS": _safe_float(info.get("forwardEps")),
        "profitMargins": _safe_float(info.get("profitMargins")),
        "grossMargins": _safe_float(info.get("grossMargins")),
        "operatingMargins": _safe_float(info.get("operatingMargins")),
        "ebitdaMargins": _safe_float(info.get("ebitdaMargins")),
        "returnOnEquity": _safe_float(info.get("returnOnEquity")),
        "returnOnAssets": _safe_float(info.get("returnOnAssets")),
    }

    # Growth
    result["growth"] = {
        "revenueGrowth": _safe_float(info.get("revenueGrowth")),
        "earningsGrowth": _safe_float(info.get("earningsGrowth")),
        "revenueGrowthQuarterly": _safe_float(info.get("revenueQuarterlyGrowth")),
        "earningsGrowthQuarterly": _safe_float(info.get("earningsQuarterlyGrowth")),
    }

    # Balance sheet health
    result["balance_sheet"] = {
        "totalCash": _safe_float(info.get("totalCash")),
        "totalDebt": _safe_float(info.get("totalDebt")),
        "debtToEquity": _safe_float(info.get("debtToEquity")),
        "currentRatio": _safe_float(info.get("currentRatio")),
        "quickRatio": _safe_float(info.get("quickRatio")),
        "totalCashPerShare": _safe_float(info.get("totalCashPerShare")),
        "bookValue": _safe_float(info.get("bookValue")),
    }

    # Capital returns
    result["capital_returns"] = {
        "dividendYield": _safe_float(info.get("dividendYield")),
        "payoutRatio": _safe_float(info.get("payoutRatio")),
        "beta": _safe_float(info.get("beta")),
        "sharesOutstanding": _safe_float(info.get("sharesOutstanding")),
        "floatShares": _safe_float(info.get("floatShares")),
    }

    # Trading data
    result["market_data"] = {
        "currentPrice": _safe_float(info.get("currentPrice")),
        "dayHigh": _safe_float(info.get("dayHigh")),
        "dayLow": _safe_float(info.get("dayLow")),
        "fiftyTwoWeekHigh": _safe_float(info.get("fiftyTwoWeekHigh")),
        "fiftyTwoWeekLow": _safe_float(info.get("fiftyTwoWeekLow")),
        "averageVolume": _safe_float(info.get("averageVolume")),
        "volume": _safe_float(info.get("volume")),
    }

    # Company info
    result["company_info"] = {
        "longName": info.get("longName") or info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        "website": info.get("website"),
        "fullTimeEmployees": _safe_float(info.get("fullTimeEmployees")),
    }

    return result


def get_financials(
    symbol: str,
    statement: str = "income",
    period: str = "annual",
) -> dict[str, Any]:
    """Fetch financial statements via Yahoo Finance.

    Args:
        symbol: ticker
        statement: "income", "balance", or "cashflow"
        period: "annual" or "quarterly"
    """
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    ticker = yf.Ticker(sym)

    statement = statement.lower().strip()
    period = period.lower().strip()

    df = None
    if statement == "income":
        df = ticker.financials if period == "annual" else ticker.quarterly_financials
    elif statement == "balance":
        df = ticker.balance_sheet if period == "annual" else ticker.quarterly_balance_sheet
    elif statement == "cashflow":
        df = ticker.cashflow if period == "annual" else ticker.quarterly_cashflow
    else:
        return {"error": f"Unknown statement type '{statement}'. Use 'income', 'balance', or 'cashflow'."}

    data = _df_to_dict(df)
    if not data:
        return {"error": f"No {statement} data available for {sym}"}

    return {
        "symbol": sym,
        "statement": statement,
        "period": period,
        "source": "yfinance (Yahoo Finance)",
        "line_items": len(data),
        "periods": [str(c) for c in df.columns] if df is not None else [],
        "data": data,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def get_quote(symbol: str) -> dict[str, Any]:
    """Quick current-price snapshot via Yahoo Finance (free)."""
    sym = symbol.upper().strip()
    if not sym:
        return {"error": "Empty symbol"}

    ticker = yf.Ticker(sym)
    info = ticker.info

    return {
        "symbol": sym,
        "source": "yfinance",
        "price": _safe_float(info.get("currentPrice") or info.get("regularMarketPrice")),
        "previousClose": _safe_float(info.get("regularMarketPreviousClose")),
        "change": _safe_float(info.get("regularMarketChange")),
        "changePercent": _safe_float(info.get("regularMarketChangePercent")),
        "dayHigh": _safe_float(info.get("dayHigh")),
        "dayLow": _safe_float(info.get("dayLow")),
        "volume": _safe_float(info.get("volume")),
        "marketCap": _safe_float(info.get("marketCap")),
        "fiftyTwoWeekHigh": _safe_float(info.get("fiftyTwoWeekHigh")),
        "fiftyTwoWeekLow": _safe_float(info.get("fiftyTwoWeekLow")),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
