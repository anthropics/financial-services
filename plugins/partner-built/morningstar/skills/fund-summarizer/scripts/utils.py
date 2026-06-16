"""Shared utilities for fund summary report scripts."""


def to_number(value) -> float | None:
    """Coerce a scalar to float, returning None for missing or non-numeric values.

    Handles all value shapes that MCP tools may return:
    - Actual int/float
    - Numeric strings with optional trailing "%" (e.g. "65.2%") or commas ("1,234.56")
    - Sentinel strings ("--", "N/A", "none", etc.) → None
    - Booleans → None (avoids True==1 / False==0 confusion)
    - Anything else → None
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().rstrip("%").replace(",", "")
        if text.lower() in {"", "--", "-", "n/a", "na", "none", "null", "not returned"}:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None
