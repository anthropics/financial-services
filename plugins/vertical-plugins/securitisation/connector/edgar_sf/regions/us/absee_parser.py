"""Streaming extractor for ABS-EE loan-level XML (Schedule AL asset data).

Built for files that can exceed 100 MB. It parses record-by-record with
xml.etree.ElementTree.iterparse and clears each <asset> after reading it, so
memory stays flat no matter how many loans are in the pool.

It is namespace-agnostic and self-describing: it reads whatever child elements
each <asset> actually contains (by local tag name). For the high-value pool
analytics it tries the candidate field names in field_maps, so it stays correct
even if a tag name varies.

In one streaming pass `parse_tape` produces:
  * pool totals and balance-weighted averages,
  * categorical distributions,
  * delinquency buckets and period net-loss (step 1),
  * an optional stratification — one dimension, or two for a cross-tab (step 2),
  * an optional CSV of (filtered) loans.
`iter_loan_states` exposes a light per-loan view used by the multi-tape engine.
"""
from __future__ import annotations

import bisect
import csv
import xml.etree.ElementTree as ET
from typing import Any, Iterator

from . import field_maps as fm


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _to_float(text: str | None) -> float | None:
    if text is None:
        return None
    s = text.strip().replace(",", "").replace("$", "")
    if not s:
        return None
    negative = s.startswith("(") and s.endswith(")")
    if negative:
        s = s[1:-1]
    try:
        value = float(s)
    except ValueError:
        return None
    return -value if negative else value


def _pick(rec: dict[str, str], fields: list[str]) -> str | None:
    for f in fields:
        if rec.get(f):
            return rec[f]
    return None


def _pick_float(rec: dict[str, str], fields: list[str]) -> float | None:
    return _to_float(_pick(rec, fields))


# --- banding / bucketing -----------------------------------------------------

def _band(value: float | None, edges: list[float], labels: list[str]) -> str | None:
    if value is None:
        return None
    return labels[bisect.bisect_right(edges, value)]


def delinquency_bucket(days: float | None) -> str:
    """Map days-past-due to an industry bucket. Non-numeric -> 'unknown'."""
    if days is None:
        return "unknown"
    if days <= 0:
        return "current"
    if days <= 30:
        return "1-30"
    if days <= 60:
        return "31-60"
    if days <= 90:
        return "61-90"
    return "91+"


def dimension_value(rec: dict[str, str], dim: str) -> str | None:
    """Resolve a stratification dimension to a label for one loan record."""
    spec = fm.DIMENSIONS.get(dim)
    if spec is None:  # allow a raw XML field name as an ad-hoc dimension
        return rec.get(dim) or None
    kind, payload = spec
    if kind == "categorical":
        return _pick(rec, payload)
    if kind == "numeric":
        fields, (edges, labels) = payload
        return _band(_pick_float(rec, fields), edges, labels)
    if kind == "special" and payload == "delinquency_bucket":
        return delinquency_bucket(_pick_float(rec, fm.DELINQUENCY_FIELDS))
    return None


def _loan_metrics(rec: dict[str, str]) -> dict[str, Any]:
    bal = _pick_float(rec, fm.BALANCE_FIELDS)
    chargeoff = _pick_float(rec, fm.CHARGEOFF_FIELDS) or 0.0
    recovery = _pick_float(rec, fm.RECOVERY_FIELDS) or 0.0
    days = _pick_float(rec, fm.DELINQUENCY_FIELDS)
    return {
        "balance": bal,
        "original": _pick_float(rec, fm.ORIGINAL_AMOUNT_FIELDS),
        "apr": _pick_float(rec, fm.INTEREST_RATE_FIELDS),
        "remaining_term": _pick_float(rec, fm.REMAINING_TERM_FIELDS),
        "chargeoff": chargeoff,
        "recovery": recovery,
        "net_loss": chargeoff - recovery,
        "dq_days": days,
        "dq_bucket": delinquency_bucket(days),
        "is_60plus": days is not None and days >= 61,
    }


def iter_assets(stream) -> Iterator[dict[str, str]]:
    """Yield one flat {local_tag: text} dict per loan, for EITHER ABS-EE layout
    (<asset>-wrapped or flat assetTypeNumber-delimited). Delegates to the shared
    structure-agnostic iterator so auto and CMBS both parse correctly."""
    from .record_iter import iter_asset_records
    yield from iter_asset_records(stream)


def iter_loan_states(stream) -> Iterator[dict[str, Any]]:
    """Light per-loan view for the multi-tape engine (id + the fields it needs)."""
    for rec in iter_assets(stream):
        m = _loan_metrics(rec)
        zb = _pick(rec, fm.ZERO_BALANCE_FIELDS)
        yield {
            "id": _pick(rec, fm.ASSET_NUMBER_FIELDS),
            "balance": m["balance"] or 0.0,
            "original": m["original"] or 0.0,
            "net_loss": m["net_loss"],
            "chargeoff": m["chargeoff"],
            "dq_bucket": m["dq_bucket"],
            "is_60plus": m["is_60plus"],
            "zero_balance": zb,
            "fico_band": _band(_pick_float(rec, fm.CREDIT_SCORE_FIELDS), *fm.FICO_BANDS),
            "state": _pick(rec, fm.STATE_FIELDS),
        }


def _match_filters(rec: dict[str, str], filters: dict[str, Any] | None) -> bool:
    if not filters:
        return True
    for field, cond in filters.items():
        val = rec.get(field, "")
        if isinstance(cond, dict):  # numeric range, e.g. {"min": 0, "max": 600}
            fv = _to_float(val)
            if fv is None:
                return False
            if "min" in cond and fv < float(cond["min"]):
                return False
            if "max" in cond and fv > float(cond["max"]):
                return False
        elif isinstance(cond, (list, tuple, set)):  # membership
            if val not in {str(c) for c in cond}:
                return False
        else:  # exact match
            if val != str(cond):
                return False
    return True


class _Stratifier:
    """Accumulates per-bucket aggregates for one or two dimensions in the pass."""

    def __init__(self, dims: list[str]) -> None:
        self.dims = dims
        self.cells: dict[tuple, dict[str, float]] = {}

    def add(self, rec: dict[str, str], m: dict[str, Any]) -> None:
        key = tuple(dimension_value(rec, d) or "unknown" for d in self.dims)
        c = self.cells.get(key)
        if c is None:
            c = self.cells[key] = {
                "n": 0, "balance": 0.0, "original": 0.0,
                "apr_num": 0.0, "apr_den": 0.0, "rem_num": 0.0, "rem_den": 0.0,
                "net_loss": 0.0, "dq60_balance": 0.0,
            }
        bal = m["balance"] or 0.0
        weight = bal if bal > 0 else 1.0
        c["n"] += 1
        c["balance"] += bal
        c["original"] += m["original"] or 0.0
        c["net_loss"] += m["net_loss"]
        if m["is_60plus"]:
            c["dq60_balance"] += bal
        if m["apr"] is not None:
            c["apr_num"] += weight * m["apr"]; c["apr_den"] += weight
        if m["remaining_term"] is not None:
            c["rem_num"] += weight * m["remaining_term"]; c["rem_den"] += weight

    @staticmethod
    def _metrics(c: dict[str, float], total_balance: float) -> dict[str, Any]:
        bal = c["balance"]
        return {
            "loans": c["n"],
            "current_balance": round(bal, 2),
            "pct_of_pool": round(100 * bal / total_balance, 2) if total_balance else None,
            "wa_apr": round(c["apr_num"] / c["apr_den"], 4) if c["apr_den"] else None,
            "wa_remaining_term": round(c["rem_num"] / c["rem_den"], 2) if c["rem_den"] else None,
            "net_loss_in_period": round(c["net_loss"], 2),
            "net_loss_pct_of_balance": round(100 * c["net_loss"] / bal, 4) if bal else None,
            "dq_60plus_pct": round(100 * c["dq60_balance"] / bal, 2) if bal else None,
        }

    def _order(self, labels: set[str], dim: str) -> list[str]:
        fixed = fm.ORDERED_LABELS.get(dim)
        if fixed:
            present = [l for l in fixed if l in labels]
            return present + sorted(labels - set(present))
        return sorted(
            labels, key=lambda l: sum(
                c["balance"] for k, c in self.cells.items() if l in k
            ), reverse=True
        )

    def result(self, total_balance: float) -> dict[str, Any]:
        if len(self.dims) == 1:
            rows = [
                {"bucket": key[0], **self._metrics(c, total_balance)}
                for key, c in self.cells.items()
            ]
            order = self._order({k[0] for k in self.cells}, self.dims[0])
            rows.sort(key=lambda r: order.index(r["bucket"]))
            return {"dimensions": self.dims, "rows": rows}

        # two-dimension cross-tab
        row_labels = self._order({k[0] for k in self.cells}, self.dims[0])
        col_labels = self._order({k[1] for k in self.cells}, self.dims[1])
        matrix = []
        for r in row_labels:
            cells = {}
            for cobj in col_labels:
                c = self.cells.get((r, cobj))
                cells[cobj] = self._metrics(c, total_balance) if c else None
            matrix.append({"bucket": r, "cells": cells})
        return {
            "dimensions": self.dims,
            "row_buckets": row_labels,
            "col_buckets": col_labels,
            "matrix": matrix,
        }


def parse_tape(
    stream,
    *,
    mode: str = "summary",
    filters: dict[str, Any] | None = None,
    out_path: str | None = None,
    sample: int = 5,
    top_n: int = 12,
    stratify_by: list[str] | None = None,
) -> dict[str, Any]:
    """Single streaming pass over a loan tape.

    Always returns pool-level analytics + a small sample. With `stratify_by`
    (a list of one or two dimension names) it adds a stratification / cross-tab.
    In "full"/"filter" mode it ALSO writes the (optionally filtered) loan records
    to a CSV at out_path — never the full records into memory/output.
    """
    n = n_matched = 0
    sum_balance = sum_original = 0.0
    period_chargeoff = period_recovery = 0.0
    wa_num = {k: 0.0 for k in fm.WA_METRICS}
    wa_den = {k: 0.0 for k in fm.WA_METRICS}
    cat: dict[str, dict[str, list]] = {k: {} for k in fm.CATEGORICAL}
    dq_buckets: dict[str, list] = {}
    dq60_balance = 0.0
    sample_rows: list[dict[str, str]] = []
    fields_seen: set[str] = set()
    strat = _Stratifier(stratify_by) if stratify_by else None

    writer = csv_file = None
    columns: list[str] | None = None
    write_rows = mode in ("full", "filter") and bool(out_path)

    for rec in iter_assets(stream):
        n += 1
        if len(fields_seen) < 500:
            fields_seen.update(rec.keys())
        if not _match_filters(rec, filters):
            continue
        n_matched += 1

        if write_rows:
            if writer is None:
                columns = list(rec.keys())
                csv_file = open(out_path, "w", newline="", encoding="utf-8")
                writer = csv.DictWriter(csv_file, fieldnames=columns, extrasaction="ignore")
                writer.writeheader()
            writer.writerow(rec)

        if len(sample_rows) < sample:
            sample_rows.append(rec)

        m = _loan_metrics(rec)
        balance = m["balance"]
        original = m["original"]
        if balance is not None:
            sum_balance += balance
        if original is not None:
            sum_original += original
        period_chargeoff += m["chargeoff"]
        period_recovery += m["recovery"]
        if m["is_60plus"] and balance:
            dq60_balance += balance

        slot = dq_buckets.setdefault(m["dq_bucket"], [0, 0.0])
        slot[0] += 1
        slot[1] += balance or 0.0

        weight = balance if (balance and balance > 0) else 1.0
        for key, fields in fm.WA_METRICS.items():
            v = _pick_float(rec, fields)
            if v is not None:
                wa_num[key] += weight * v
                wa_den[key] += weight

        for label, fields in fm.CATEGORICAL.items():
            cv = _pick(rec, fields)
            if cv:
                cslot = cat[label].setdefault(cv, [0, 0.0])
                cslot[0] += 1
                cslot[1] += balance if balance is not None else 0.0

        if strat is not None:
            strat.add(rec, m)

    if csv_file:
        csv_file.close()

    weighted_averages = {
        k: round(wa_num[k] / wa_den[k], 4) for k in fm.WA_METRICS if wa_den[k] > 0
    }
    distributions: dict[str, Any] = {}
    for label, counts in cat.items():
        if not counts:
            continue
        ranked = sorted(counts.items(), key=lambda kv: (kv[1][1] or kv[1][0]), reverse=True)
        distributions[label] = [
            {
                "value": value,
                "loans": c[0],
                "balance": round(c[1], 2),
                "balance_pct": round(100 * c[1] / sum_balance, 2) if sum_balance else None,
            }
            for value, c in ranked[:top_n]
        ]

    bucket_order = fm.ORDERED_LABELS["delinquency_bucket"]
    delinquency = {
        b: {
            "loans": dq_buckets[b][0],
            "balance": round(dq_buckets[b][1], 2),
            "balance_pct": round(100 * dq_buckets[b][1] / sum_balance, 2) if sum_balance else None,
        }
        for b in bucket_order if b in dq_buckets
    }

    net_loss = period_chargeoff - period_recovery
    result: dict[str, Any] = {
        "loans_in_tape": n,
        "loans_matched": n_matched,
        "total_current_balance": round(sum_balance, 2),
        "total_original_balance": round(sum_original, 2),
        "average_current_balance": round(sum_balance / n_matched, 2) if n_matched else None,
        "weighted_averages": weighted_averages,
        "weighted_average_basis": "balance-weighted where balance present, else equal-weighted",
        "distributions": distributions,
        "delinquency_buckets": delinquency,
        "dq_60plus_pct": round(100 * dq60_balance / sum_balance, 2) if sum_balance else None,
        "gross_chargeoff_in_period": round(period_chargeoff, 2),
        "recoveries_in_period": round(period_recovery, 2),
        "net_loss_in_period": round(net_loss, 2),
        "net_loss_pct_of_balance_period": round(100 * net_loss / sum_balance, 4) if sum_balance else None,
        "loss_note": "period figures from this single tape; cumulative net loss needs the multi-tape static-pool analysis",
        "fields_available": sorted(fields_seen),
        "sample_loans": sample_rows,
    }
    if strat is not None:
        result["stratification"] = strat.result(sum_balance)
    if write_rows and columns is not None:
        result["csv_path"] = out_path
        result["csv_rows"] = n_matched
        result["csv_columns"] = columns
    return result
