"""Structure-agnostic ABS-EE record iterator.

SEC ABS-EE asset tapes come in two layouts across asset classes:
  * WRAPPED: each loan is an <asset>...</asset> element;
  * FLAT: loans sit directly under <assets>, each starting with <assetTypeNumber>
    and with no wrapper (confirmed for CMBS).

iter_asset_records handles BOTH in one streaming, memory-safe pass, so a parser
need not know which layout a given filing uses. It yields one flat
{local_tag: text} dict per loan (first non-empty value wins for repeated tags).
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Iterator


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def iter_asset_records(stream, start_field: str = "assetTypeNumber") -> Iterator[dict]:
    context = ET.iterparse(stream, events=("start", "end"))
    _, root = next(context)
    rec: dict = {}
    started = False
    wrapped = False
    for event, elem in context:
        if event != "end" or elem is root:
            continue  # skip the root (it looks empty after root.clear())
        name = _localname(elem.tag)
        if len(elem) == 0:  # leaf element
            text = (elem.text or "").strip()
            if name == start_field and not wrapped:  # FLAT boundary
                if started:
                    yield rec
                    rec = {}
                    root.clear()
                started = True
            if name not in rec or (text and not rec.get(name)):
                rec[name] = text
        elif name == "asset":  # WRAPPED boundary: one loan per <asset>
            wrapped = True
            if rec:
                yield rec
                rec = {}
                root.clear()
                started = False
    if rec:
        yield rec
