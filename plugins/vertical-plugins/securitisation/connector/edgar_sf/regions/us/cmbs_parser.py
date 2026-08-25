"""Streaming analytics for CMBS (commercial-mortgage) ABS-EE loan tapes.

Validated against a real conduit filing, so it handles the CMBS schema as it
actually is, which differs from auto:
  * loans are flat under <assets> (no <asset> wrapper) and start with
    <assetTypeNumber> - iter_cmbs_loans splits the stream on that marker;
  * a loan may own several <property> blocks - we use the first/primary property;
  * rate and occupancy are stored as decimal fractions (scaled to % here), DSCR
    is a true ratio, and LTV is computed as balance / valuation.

Memory-safe (record-by-record via iterparse).
"""
from __future__ import annotations

import csv
import re
import xml.etree.ElementTree as ET
from typing import Any, Iterator

from . import cmbs_field_maps as cfm
from .absee_parser import _match_filters, _pick, _pick_float


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _band(value, edges, labels):
    if value is None:
        return None
    import bisect
    return labels[bisect.bisect_right(edges, value)]


def _year(date_text):
    if not date_text:
        return None
    m = re.search(r"(19|20)\d{2}", date_text)
    return m.group(0) if m else None


def _as_percent(value, frac_threshold):
    if value is None:
        return None
    return value * 100 if abs(value) <= frac_threshold else value


def iter_cmbs_loans(stream) -> Iterator[dict]:
    """Yield one flat {local_tag: text} dict per loan (split on assetTypeNumber)."""
    context = ET.iterparse(stream, events=("start", "end"))
    _, root = next(context)
    rec: dict = {}
    started = False
    for event, elem in context:
        if event != "end":
            continue
        name = _localname(elem.tag)
        if len(elem) == 0:
            text = (elem.text or "").strip()
            if name == cfm.RECORD_START_FIELD:
                if started:
                    yield rec
                    rec = {}
                    root.clear()
                started = True
            if name not in rec or (text and not rec.get(name)):
                rec[name] = text
    if rec:
        yield rec


def _loan_view(rec: dict) -> dict:
    balance = _pick_float(rec, cfm.BALANCE_FIELDS)
    valuation = _pick_float(rec, cfm.VALUATION_FIELDS)
    ltv = (100.0 * balance / valuation) if (balance and valuation) else None
    return {
        "balance": balance,
        "original": _pick_float(rec, cfm.ORIGINAL_AMOUNT_FIELDS),
        "valuation": valuation,
        "noi": _pick_float(rec, cfm.NOI_FIELDS),
        "coupon_pct": _as_percent(_pick_float(rec, cfm.INTEREST_RATE_FIELDS), 1.0),
        "occupancy_pct": _as_percent(_pick_float(rec, cfm.OCCUPANCY_FIELDS), 1.5),
        "dscr_ncf": _pick_float(rec, cfm.DSCR_NCF_FIELDS),
        "ltv_pct": round(ltv, 4) if ltv is not None else None,
        "remaining_term": _pick_float(rec, cfm.REMAINING_TERM_FIELDS),
    }


_WA = {
    "coupon_pct": "coupon_pct",
    "dscr_ncf_x": "dscr_ncf",
    "occupancy_pct": "occupancy_pct",
    "ltv_pct": "ltv_pct",
    "remaining_term_months": "remaining_term",
}


def _dim_value(rec, v, dim):
    if dim == "property_type":
        x = _pick(rec, cfm.PROPERTY_TYPE_FIELDS)
        return cfm.PROPERTY_TYPE_NAMES.get(x, x) if x else None
    if dim == "property_state":
        return _pick(rec, cfm.PROPERTY_STATE_FIELDS)
    if dim == "watchlist":
        return _pick(rec, cfm.WATCHLIST_FIELDS)
    if dim == "maturity_year":
        return _year(_pick(rec, cfm.MATURITY_DATE_FIELDS))
    if dim == "dscr_band":
        return _band(v["dscr_ncf"], *cfm.DSCR_BANDS)
    if dim == "ltv_band":
        return _band(v["ltv_pct"], *cfm.LTV_BANDS)
    if dim == "occupancy_band":
        return _band(v["occupancy_pct"], *cfm.OCCUPANCY_BANDS)
    return rec.get(dim) or None


class _CmbsStratifier:
    def __init__(self, dims):
        self.dims = dims
        self.cells = {}

    def add(self, rec, v):
        key = tuple(_dim_value(rec, v, d) or "unknown" for d in self.dims)
        c = self.cells.get(key)
        if c is None:
            c = self.cells[key] = {"n": 0, "balance": 0.0, "noi": 0.0,
                                   "dscr_n": 0.0, "dscr_d": 0.0, "occ_n": 0.0,
                                   "occ_d": 0.0, "ltv_n": 0.0, "ltv_d": 0.0}
        bal = v["balance"] or 0.0
        w = bal if bal > 0 else 1.0
        c["n"] += 1
        c["balance"] += bal
        c["noi"] += v["noi"] or 0.0
        for src, num, den in (("dscr_ncf", "dscr_n", "dscr_d"),
                              ("occupancy_pct", "occ_n", "occ_d"),
                              ("ltv_pct", "ltv_n", "ltv_d")):
            if v[src] is not None:
                c[num] += w * v[src]
                c[den] += w

    @staticmethod
    def _metrics(c, total):
        bal = c["balance"]
        return {
            "loans": c["n"],
            "current_balance": round(bal, 2),
            "pct_of_pool": round(100 * bal / total, 2) if total else None,
            "wa_dscr_ncf_x": round(c["dscr_n"] / c["dscr_d"], 2) if c["dscr_d"] else None,
            "wa_occupancy_pct": round(c["occ_n"] / c["occ_d"], 1) if c["occ_d"] else None,
            "wa_ltv_pct": round(c["ltv_n"] / c["ltv_d"], 1) if c["ltv_d"] else None,
            "debt_yield_pct": round(100 * c["noi"] / bal, 2) if bal else None,
        }

    def _order(self, labels, dim):
        fixed = cfm.ORDERED_LABELS.get(dim)
        if fixed:
            present = [l for l in fixed if l in labels]
            return present + sorted(labels - set(present))
        return sorted(labels, key=lambda l: sum(
            c["balance"] for k, c in self.cells.items() if l in k), reverse=True)

    def result(self, total):
        if len(self.dims) == 1:
            rows = [{"bucket": k[0], **self._metrics(c, total)} for k, c in self.cells.items()]
            order = self._order({k[0] for k in self.cells}, self.dims[0])
            rows.sort(key=lambda r: order.index(r["bucket"]))
            return {"dimensions": self.dims, "rows": rows}
        rl = self._order({k[0] for k in self.cells}, self.dims[0])
        cl = self._order({k[1] for k in self.cells}, self.dims[1])
        matrix = [{"bucket": r, "cells": {c: (self._metrics(self.cells[(r, c)], total)
                                              if (r, c) in self.cells else None) for c in cl}}
                  for r in rl]
        return {"dimensions": self.dims, "row_buckets": rl, "col_buckets": cl, "matrix": matrix}


def parse_cmbs_tape(stream, *, mode="summary", filters=None, out_path=None,
                    sample=5, top_n=10, stratify_by=None):
    n = n_matched = 0
    sum_balance = sum_original = sum_noi = 0.0
    wa_num = {k: 0.0 for k in _WA}
    wa_den = {k: 0.0 for k in _WA}
    cat = {k: {} for k in cfm.CATEGORICAL}
    maturity = {}
    top_loans = []
    sample_rows = []
    fields_seen = set()
    strat = _CmbsStratifier(stratify_by) if stratify_by else None

    writer = csv_file = None
    columns = None
    write_rows = mode in ("full", "filter") and bool(out_path)

    for rec in iter_cmbs_loans(stream):
        n += 1
        if len(fields_seen) < 600:
            fields_seen.update(rec.keys())
        if not _match_filters(rec, filters):
            continue
        n_matched += 1
        v = _loan_view(rec)
        bal = v["balance"] or 0.0

        if write_rows:
            if writer is None:
                columns = list(rec.keys())
                csv_file = open(out_path, "w", newline="", encoding="utf-8")
                writer = csv.DictWriter(csv_file, fieldnames=columns, extrasaction="ignore")
                writer.writeheader()
            writer.writerow(rec)
        if len(sample_rows) < sample:
            sample_rows.append(rec)

        if v["balance"] is not None:
            sum_balance += v["balance"]
        if v["original"] is not None:
            sum_original += v["original"]
        if v["noi"] is not None:
            sum_noi += v["noi"]

        w = bal if bal > 0 else 1.0
        for out_key, vkey in _WA.items():
            val = v[vkey]
            if val is not None:
                wa_num[out_key] += w * val
                wa_den[out_key] += w

        for label, fields in cfm.CATEGORICAL.items():
            cv = _pick(rec, fields)
            if cv:
                if fields is cfm.PROPERTY_TYPE_FIELDS:
                    cv = cfm.PROPERTY_TYPE_NAMES.get(cv, cv)
                slot = cat[label].setdefault(cv, [0, 0.0])
                slot[0] += 1
                slot[1] += bal

        yr = _year(_pick(rec, cfm.MATURITY_DATE_FIELDS))
        if yr:
            ms = maturity.setdefault(yr, [0, 0.0])
            ms[0] += 1
            ms[1] += bal

        top_loans.append({
            "property": _pick(rec, cfm.PROPERTY_NAME_FIELDS),
            "type": cfm.PROPERTY_TYPE_NAMES.get(_pick(rec, cfm.PROPERTY_TYPE_FIELDS) or "",
                                                _pick(rec, cfm.PROPERTY_TYPE_FIELDS)),
            "state": _pick(rec, cfm.PROPERTY_STATE_FIELDS),
            "balance": round(bal, 2),
            "dscr_ncf_x": v["dscr_ncf"],
            "occupancy_pct": round(v["occupancy_pct"], 1) if v["occupancy_pct"] is not None else None,
            "ltv_pct": v["ltv_pct"],
        })

        if strat is not None:
            strat.add(rec, v)

    if csv_file:
        csv_file.close()

    weighted_averages = {k: round(wa_num[k] / wa_den[k], 4) for k in _WA if wa_den[k] > 0}
    distributions = {}
    for label, counts in cat.items():
        if not counts:
            continue
        ranked = sorted(counts.items(), key=lambda kv: (kv[1][1] or kv[1][0]), reverse=True)
        distributions[label] = [
            {"value": value, "loans": c[0], "balance": round(c[1], 2),
             "balance_pct": round(100 * c[1] / sum_balance, 2) if sum_balance else None}
            for value, c in ranked[:top_n]
        ]
    maturity_profile = [
        {"maturity_year": y, "loans": maturity[y][0], "balance": round(maturity[y][1], 2),
         "balance_pct": round(100 * maturity[y][1] / sum_balance, 2) if sum_balance else None}
        for y in sorted(maturity)
    ]
    top_loans.sort(key=lambda r: r["balance"], reverse=True)

    result = {
        "asset_class": "cmbs",
        "loans_in_tape": n,
        "loans_matched": n_matched,
        "total_current_balance": round(sum_balance, 2),
        "total_original_balance": round(sum_original, 2),
        "average_loan_balance": round(sum_balance / n_matched, 2) if n_matched else None,
        "pool_debt_yield_pct": round(100 * sum_noi / sum_balance, 2) if sum_balance else None,
        "weighted_averages": weighted_averages,
        "weighted_average_basis": "balance-weighted; rate & occupancy scaled to percent, LTV = balance/valuation, DSCR is a ratio",
        "distributions": distributions,
        "maturity_profile": maturity_profile,
        "largest_loans": top_loans[:top_n],
        "fields_available": sorted(fields_seen),
        "sample_loans": sample_rows,
        "notes": "Concentration uses each loan's primary (first) property; figures are point-in-time from this tape.",
    }
    if strat is not None:
        result["stratification"] = strat.result(sum_balance)
    if write_rows and columns is not None:
        result["csv_path"] = out_path
        result["csv_rows"] = n_matched
    return result
