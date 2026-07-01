"""US region implementation — SEC EDGAR.

Implements the four Region capabilities against EDGAR's free, public endpoints:
  - search_deals        -> EDGAR full-text search (efts.sec.gov)
  - get_deal_filings    -> submissions API (data.sec.gov)
  - get_filing_document -> the Archives document store (www.sec.gov/Archives)
  - extract_loan_level  -> stream-parse the ABS-EE EX-102 loan tape
"""
from __future__ import annotations

import html
import re
import urllib.parse
from typing import Any

from ... import config
from ...core.http_client import SecHttpClient
from ...core.models import Deal, DealFilings, FilingRef, accession_no_dashes
from ..base import Region
from . import absee_parser, cmbs_parser, timeseries

# Map friendly asset-class names to the phrase that best identifies them in
# EDGAR's full-text index (issuer names / cover text).
ASSET_CLASS_PHRASES = {
    "auto": "automobile",
    "automobile": "automobile",
    "auto loan": "automobile",
    "auto lease": "automobile lease",
    "cmbs": "commercial mortgage",
    "commercial mortgage": "commercial mortgage",
    "rmbs": "residential mortgage",
    "residential mortgage": "residential mortgage",
    "credit card": "credit card",
    "student loan": "student loan",
    "clo": "collateralized loan obligation",
}


def _digits(value: Any) -> str:
    return re.sub(r"\D", "", str(value))


def _clean_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</(p|div|tr|h[1-6]|li)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t\f\r]+", " ", raw)
    raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
    return raw.strip()


class UsEdgar(Region):
    code = "US"
    name = "United States — SEC EDGAR"

    def __init__(self, client: SecHttpClient | None = None) -> None:
        self.client = client or SecHttpClient(
            user_agent=config.user_agent(),
            min_interval=config.MIN_REQUEST_INTERVAL,
        )

    # ---- 1) search -----------------------------------------------------------
    def search_deals(
        self,
        query: str,
        *,
        asset_class: str | None = None,
        form_type: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        q = (query or "").strip()
        if asset_class:
            phrase = ASSET_CLASS_PHRASES.get(asset_class.lower(), asset_class)
            q = f'{q} "{phrase}"'.strip()
        params = {"q": q or '"asset-backed"'}
        if form_type:
            params["forms"] = form_type
        if date_from or date_to:
            params["dateRange"] = "custom"
            params["startdt"] = date_from or "2001-01-01"
            params["enddt"] = date_to or "2099-12-31"
        url = config.EFTS_SEARCH_URL + "?" + urllib.parse.urlencode(params)
        data = self.client.get_json(url)

        hits = data.get("hits", {})
        total = hits.get("total", {}).get("value")
        results = []
        for hit in hits.get("hits", [])[:limit]:
            src = hit.get("_source", {})
            ciks = src.get("ciks") or []
            cik = ciks[0] if ciks else None
            adsh = src.get("adsh") or ""
            hit_id = hit.get("_id", "")
            filename = hit_id.split(":", 1)[1] if ":" in hit_id else None
            display = (src.get("display_names") or [""])[0]
            doc_url = None
            if cik and adsh and filename:
                doc_url = f"{config.ARCHIVES_BASE}/{int(cik)}/{accession_no_dashes(adsh)}/{filename}"
            results.append(
                {
                    "issuer": re.sub(r"\s*\(CIK.*\)\s*$", "", display).strip(),
                    "cik": cik,
                    "accession": adsh,
                    "form": src.get("form") or (src.get("root_forms") or [None])[0],
                    "filed": src.get("file_date"),
                    "sic": (src.get("sics") or [None])[0],
                    "document_url": doc_url,
                }
            )
        return {
            "region": self.code,
            "query": q,
            "total_matches": total,
            "returned": len(results),
            "results": results,
        }

    # ---- 2) deal filings -----------------------------------------------------
    def get_deal_filings(
        self,
        identifier: str,
        *,
        form_type: str | None = None,
        limit: int = 100,
    ) -> DealFilings:
        cik_digits = _digits(identifier)
        if not cik_digits:
            raise ValueError(f"Could not parse a CIK from '{identifier}'. Provide the numeric CIK.")
        url = config.SUBMISSIONS_URL.format(cik10=cik_digits.zfill(10))
        data = self.client.get_json(url)

        deal = Deal(cik=data.get("cik", cik_digits), name=data.get("name", ""), sic=data.get("sic"))
        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        wanted = {f.strip().upper() for f in form_type.split(",")} if form_type else None

        filings: list[FilingRef] = []
        for i in range(len(forms)):
            if wanted and forms[i].upper() not in wanted:
                continue
            filings.append(
                FilingRef(
                    cik=deal.cik,
                    accession=recent["accessionNumber"][i],
                    form=forms[i],
                    filing_date=_get(recent, "filingDate", i),
                    report_date=_get(recent, "reportDate", i) or None,
                    primary_document=_get(recent, "primaryDocument", i),
                    description=_get(recent, "primaryDocDescription", i),
                    size=_get(recent, "size", i),
                )
            )
            if len(filings) >= limit:
                break
        return DealFilings(deal=deal, filings=filings)

    # ---- 3) get a document's text -------------------------------------------
    def get_filing_document(
        self,
        cik: str,
        accession: str,
        document: str | None = None,
        *,
        max_chars: int = 200_000,
        offset: int = 0,
    ) -> dict[str, Any]:
        cik_int = int(_digits(cik))
        base = f"{config.ARCHIVES_BASE}/{cik_int}/{accession_no_dashes(accession)}/"
        if not document:
            document = self._primary_document(base)
        url = base + document
        raw = self.client.get_text(url)
        text = _clean_html(raw) if document.lower().endswith((".htm", ".html", ".txt")) else raw
        chunk = text[offset : offset + max_chars]
        return {
            "region": self.code,
            "cik": cik_int,
            "accession": accession,
            "document": document,
            "url": url,
            "total_chars": len(text),
            "offset": offset,
            "returned_chars": len(chunk),
            "truncated": offset + max_chars < len(text),
            "text": chunk,
        }

    def _primary_document(self, base_url: str) -> str:
        items = self.client.get_json(base_url + "index.json").get("directory", {}).get("item", [])
        html_docs = [
            it for it in items
            if it["name"].lower().endswith((".htm", ".html")) and "index" not in it["name"].lower()
        ]
        html_docs.sort(key=_item_size, reverse=True)
        if html_docs:
            return html_docs[0]["name"]
        for it in items:
            if it["name"].lower().endswith(".txt"):
                return it["name"]
        raise FileNotFoundError("No readable primary document found in this filing.")

    # ---- 4) loan-level extraction -------------------------------------------
    def _open_asset_tape(self, cik_int: int, accession: str):
        base = f"{config.ARCHIVES_BASE}/{cik_int}/{accession_no_dashes(accession)}/"
        asset_file = self._asset_data_file(base)
        url = base + asset_file
        return self.client.open_stream(url), asset_file, url

    def extract_loan_level(
        self,
        cik: str,
        accession: str,
        *,
        mode: str = "summary",
        filters: dict[str, Any] | None = None,
        out_path: str | None = None,
        sample: int = 5,
        stratify_by: list[str] | None = None,
    ) -> dict[str, Any]:
        cik_int = int(_digits(cik))
        stream, asset_file, url = self._open_asset_tape(cik_int, accession)
        try:
            summary = absee_parser.parse_tape(
                stream, mode=mode, filters=filters, out_path=out_path,
                sample=sample, stratify_by=stratify_by,
            )
        finally:
            try:
                stream.close()
            except Exception:
                pass
        summary.update(
            {
                "region": self.code,
                "cik": cik_int,
                "accession": accession,
                "asset_data_file": asset_file,
                "source_url": url,
                "mode": mode,
            }
        )
        return summary

    # ---- 4b) CMBS commercial-mortgage loan-level ----------------------------
    def extract_cmbs_loan_level(
        self,
        cik: str,
        accession: str,
        *,
        mode: str = "summary",
        filters: dict[str, Any] | None = None,
        out_path: str | None = None,
        sample: int = 5,
        stratify_by: list[str] | None = None,
    ) -> dict[str, Any]:
        cik_int = int(_digits(cik))
        stream, asset_file, url = self._open_asset_tape(cik_int, accession)
        try:
            summary = cmbs_parser.parse_cmbs_tape(
                stream, mode=mode, filters=filters, out_path=out_path,
                sample=sample, stratify_by=stratify_by,
            )
        finally:
            try:
                stream.close()
            except Exception:
                pass
        summary.update(
            {
                "region": self.code,
                "cik": cik_int,
                "accession": accession,
                "asset_data_file": asset_file,
                "source_url": url,
                "mode": mode,
            }
        )
        return summary

    # ---- 5) multi-tape time-series analyses ---------------------------------
    def extract_loan_timeseries(
        self,
        cik: str,
        accessions: list[str],
        *,
        analysis: str = "static_pool_loss",
        periods: list[str] | None = None,
    ) -> dict[str, Any]:
        fn = timeseries.ANALYSES.get(analysis)
        if fn is None:
            raise ValueError(
                f"Unknown analysis '{analysis}'. Choose one of: {sorted(timeseries.ANALYSES)}."
            )
        cik_int = int(_digits(cik))
        accs = [a for a in accessions if a]
        if not accs:
            raise ValueError("Provide at least one ABS-EE accession (oldest -> newest).")
        labels = periods if (periods and len(periods) == len(accs)) else accs
        pairs = list(zip(labels, accs))

        def open_tape(acc: str):
            stream, _, _ = self._open_asset_tape(cik_int, acc)
            return stream

        result = fn(open_tape, pairs)
        result.update({"region": self.code, "cik": cik_int, "accessions": accs})
        return result

    def _asset_data_file(self, base_url: str) -> str:
        items = self.client.get_json(base_url + "index.json").get("directory", {}).get("item", [])
        xmls = [it for it in items if it["name"].lower().endswith(".xml")]
        if not xmls:
            raise FileNotFoundError(
                "No XML asset-data file found in this filing — is it actually a Form ABS-EE filing?"
            )
        # The EX-102 loan tape is by far the largest XML in an ABS-EE submission.
        xmls.sort(key=_item_size, reverse=True)
        return xmls[0]["name"]


def _get(arrays: dict[str, list], key: str, i: int):
    seq = arrays.get(key) or []
    return seq[i] if i < len(seq) else None


def _item_size(item: dict) -> int:
    try:
        return int(item.get("size") or 0)
    except (TypeError, ValueError):
        return 0
