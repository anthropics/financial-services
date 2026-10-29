"""Plain data structures shared across regions.

These are deliberately region-neutral: a 'Deal' and a 'Filing' look the same
whether the source is the US (SEC EDGAR), the EU, or Australia. Only the
regional modules know how to populate them.
"""
from __future__ import annotations

from dataclasses import dataclass, field

ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"


def accession_no_dashes(accession: str) -> str:
    """'0001694010-18-000036' -> '000169401018000036' (used in archive URLs)."""
    return accession.replace("-", "")


@dataclass
class Deal:
    """A securitisation issuing entity (an EDGAR filer / trust)."""

    cik: str
    name: str
    sic: str | None = None
    region: str = "US"


@dataclass
class FilingRef:
    """A pointer to one filing (e.g. a 424B5 prospectus, a 10-D, or an ABS-EE)."""

    cik: str
    accession: str
    form: str
    filing_date: str | None = None
    report_date: str | None = None
    primary_document: str | None = None
    description: str | None = None
    size: int | None = None
    region: str = "US"

    @property
    def filing_dir_url(self) -> str:
        """The browsable folder that holds every file in this submission."""
        return f"{ARCHIVES_BASE}/{int(self.cik)}/{accession_no_dashes(self.accession)}/"

    @property
    def document_url(self) -> str | None:
        """Direct URL to the primary document, if known."""
        if not self.primary_document:
            return None
        return self.filing_dir_url + self.primary_document


@dataclass
class DealFilings:
    """A deal plus its filing history."""

    deal: Deal
    filings: list[FilingRef] = field(default_factory=list)
