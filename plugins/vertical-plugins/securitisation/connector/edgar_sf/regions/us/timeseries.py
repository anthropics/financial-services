"""Multi-tape analyses — the part only loan-level data (stacked over time) can do.

Each function takes:
  * `open_tape(key)` — returns a fresh byte stream for one period's ABS-EE tape,
  * `periods` — an ordered (oldest -> newest) list of (label, key) pairs.

Tapes are read one at a time and closed immediately, so memory stays bounded to
at most one period's per-loan state (keyed on assetNumber), never the raw XML.
"""
from __future__ import annotations

from typing import Any, Callable

from . import field_maps as fm
from .absee_parser import iter_loan_states

Opener = Callable[[str], Any]

_STATE_ORDER = [
    "Current", "1-30", "31-60", "61-90", "91+",
    "Charged-off", "Prepaid", "Repurchased",
    "Paid off", "Paid off / removed", "Resolved (other)", "Unknown",
]


def _from_state(dq_bucket: str) -> str:
    return "Current" if dq_bucket == "current" else (
        "Unknown" if dq_bucket == "unknown" else dq_bucket
    )


def _to_state(loan: dict[str, Any]) -> str:
    if loan["chargeoff"] and loan["chargeoff"] > 0:
        return "Charged-off"
    zb = loan.get("zero_balance")
    if zb:
        return fm.ZERO_BALANCE_STATES.get(str(zb).strip(), "Resolved (other)")
    if (loan["balance"] or 0) <= 0:
        return "Paid off"
    return _from_state(loan["dq_bucket"])


def _ordered(states) -> list[str]:
    present = [s for s in _STATE_ORDER if s in states]
    return present + [s for s in states if s not in present]


def _read(open_tape: Opener, key: str):
    stream = open_tape(key)
    try:
        for loan in iter_loan_states(stream):
            yield loan
    finally:
        try:
            stream.close()
        except Exception:
            pass


def roll_rate(open_tape: Opener, periods: list[tuple[str, str]], *, basis: str = "balance") -> dict[str, Any]:
    """Delinquency transition matrix between the two most recent tapes."""
    if len(periods) < 2:
        raise ValueError("roll_rate needs at least two periods (oldest -> newest).")
    (label0, key0), (label1, key1) = periods[-2], periods[-1]

    prev: dict[str, dict[str, Any]] = {}
    for loan in _read(open_tape, key0):
        if loan["id"]:
            prev[loan["id"]] = {"dq_bucket": loan["dq_bucket"], "balance": loan["balance"]}
    curr: dict[str, dict[str, Any]] = {}
    for loan in _read(open_tape, key1):
        if loan["id"]:
            curr[loan["id"]] = loan

    matrix: dict[str, dict[str, float]] = {}
    from_totals: dict[str, float] = {}
    for lid, p in prev.items():
        fr = _from_state(p["dq_bucket"])
        weight = p["balance"] if (basis == "balance" and p["balance"]) else 1.0
        loan = curr.get(lid)
        to = _to_state(loan) if loan is not None else "Paid off / removed"
        matrix.setdefault(fr, {})
        matrix[fr][to] = matrix[fr].get(to, 0.0) + weight
        from_totals[fr] = from_totals.get(fr, 0.0) + weight

    rows = []
    for fr in _ordered(matrix):
        total = from_totals[fr] or 1.0
        cols = matrix[fr]
        rows.append({
            "from_state": fr,
            "from_weight": round(from_totals[fr], 2),
            "to": {to: round(100 * cols[to] / total, 2) for to in _ordered(cols)},
        })
    return {
        "analysis": "roll_rate",
        "basis": basis,
        "period_from": label0,
        "period_to": label1,
        "states": _ordered(set(matrix) | {t for c in matrix.values() for t in c}),
        "rows": rows,
    }


def static_pool_loss(open_tape: Opener, periods: list[tuple[str, str]]) -> dict[str, Any]:
    """Cumulative net-loss curve and pool factor by period (oldest -> newest)."""
    if not periods:
        raise ValueError("static_pool_loss needs at least one period.")
    original_pool = None
    cumulative = 0.0
    rows = []
    for i, (label, key) in enumerate(periods):
        end_balance = sum_original = net = 0.0
        n = 0
        for loan in _read(open_tape, key):
            end_balance += loan["balance"] or 0.0
            sum_original += loan["original"] or 0.0
            net += loan["net_loss"]
            n += 1
        if original_pool is None:
            original_pool = sum_original or end_balance
        cumulative += net
        rows.append({
            "period": label,
            "period_index": i + 1,
            "loans": n,
            "end_balance": round(end_balance, 2),
            "pool_factor_pct": round(100 * end_balance / original_pool, 4) if original_pool else None,
            "period_net_loss": round(net, 2),
            "cumulative_net_loss": round(cumulative, 2),
            "cumulative_net_loss_pct": round(100 * cumulative / original_pool, 4) if original_pool else None,
        })
    return {
        "analysis": "static_pool_loss",
        "original_pool_balance": round(original_pool or 0.0, 2),
        "original_pool_basis": "sum of originalLoanAmount on the first (oldest) tape",
        "rows": rows,
    }


def prepayment(open_tape: Opener, periods: list[tuple[str, str]]) -> dict[str, Any]:
    """Period pool-paydown speed plus a clean voluntary-payoff tally."""
    if not periods:
        raise ValueError("prepayment needs at least one period.")
    prev_balance = None
    rows = []
    for i, (label, key) in enumerate(periods):
        end_balance = vol_balance = 0.0
        vol_loans = 0
        for loan in _read(open_tape, key):
            end_balance += loan["balance"] or 0.0
            zb = loan.get("zero_balance")
            if zb and fm.ZERO_BALANCE_STATES.get(str(zb).strip()) == "Prepaid":
                vol_loans += 1
                vol_balance += loan["original"] or loan["balance"] or 0.0
        paydown = cpr = None
        if prev_balance:
            smm = (prev_balance - end_balance) / prev_balance
            paydown = round(100 * smm, 4)
            if 0 <= smm < 1:
                cpr = round(100 * (1 - (1 - smm) ** 12), 4)
        rows.append({
            "period": label,
            "period_index": i + 1,
            "end_balance": round(end_balance, 2),
            "pool_paydown_pct": paydown,
            "cpr_total_pct": cpr,
            "voluntary_payoff_loans": vol_loans,
            "voluntary_payoff_balance": round(vol_balance, 2),
        })
        prev_balance = end_balance
    return {
        "analysis": "prepayment",
        "note": (
            "pool_paydown_pct / cpr_total_pct include scheduled principal and losses; "
            "voluntary_payoff_* (zeroBalanceCode = prepaid) is the clean prepay signal. "
            "True voluntary SMM needs scheduledPrincipalAmount, not always on the tape."
        ),
        "rows": rows,
    }


ANALYSES = {
    "roll_rate": roll_rate,
    "static_pool_loss": static_pool_loss,
    "prepayment": prepayment,
}
