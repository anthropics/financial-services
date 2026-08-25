"""The Region interface.

Every regional data source (US now; EU, AU later) implements these four
capabilities. The MCP tools call the interface and never need to know which
country's system is behind it — that's what keeps the connector extensible.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..core.models import DealFilings


class Region(ABC):
    code: str = ""   # e.g. "US"
    name: str = ""   # e.g. "United States — SEC EDGAR"

    @abstractmethod
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
        """Find securitisation deals/filings matching a text query."""

    @abstractmethod
    def get_deal_filings(
        self,
        identifier: str,
        *,
        form_type: str | None = None,
        limit: int = 100,
    ) -> DealFilings:
        """List the filing history for one deal (by CIK or exact name)."""

    @abstractmethod
    def get_filing_document(
        self,
        cik: str,
        accession: str,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Retrieve a specific document's text (e.g. a 424B prospectus or 10-D)."""

    @abstractmethod
    def extract_loan_level(
        self,
        cik: str,
        accession: str,
        *,
        mode: str = "summary",          # "summary" | "full" | "filter"
        filters: dict[str, Any] | None = None,
        out_path: str | None = None,
        sample: int = 5,
        stratify_by: list[str] | None = None,
    ) -> dict[str, Any]:
        """Extract structured fields from an ABS-EE loan-level XML tape.

        `stratify_by` takes one dimension (a stratification table) or two
        (a cross-tab) — e.g. ["fico_band"] or ["fico_band", "state"].
        """

    def extract_loan_timeseries(
        self,
        cik: str,
        accessions: list[str],
        *,
        analysis: str = "static_pool_loss",
        periods: list[str] | None = None,
    ) -> dict[str, Any]:
        """Multi-tape analyses across periods (roll-rate, static-pool loss,
        prepayment). Optional capability — regions override it where supported."""
        raise NotImplementedError(
            f"Region '{self.code}' does not implement multi-tape analyses yet."
        )

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
        """CMBS commercial-mortgage loan-level analytics (DSCR, debt yield,
        occupancy, LTV, property mix, maturity profile). Optional capability."""
        raise NotImplementedError(
            f"Region '{self.code}' does not implement CMBS loan-level analytics yet."
        )
