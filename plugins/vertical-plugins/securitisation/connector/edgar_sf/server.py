"""MCP server for the securitisation EDGAR connector.

Exposes the connector's capabilities as MCP tools over stdio so Claude (in
Cowork or Claude Code) can call them. Region-aware: every tool takes a `region`
argument that defaults to "US". When EU/AU modules are added and registered,
the same tools serve them with no changes here.

Run:  python -m edgar_sf.server
"""
from __future__ import annotations

import os
import re
import tempfile
from typing import Any, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # the one third-party dependency isn't installed
    import sys
    sys.stderr.write(
        "securitisation-edgar: the MCP SDK is not installed. "
        'Run:  pip install "mcp>=1.2.0"\n'
    )
    raise SystemExit(1)

from .regions import registry
from .regions.us import UsEdgar

# Register the regions this build ships with. (EU/AU would register here too.)
registry.register(UsEdgar())

mcp = FastMCP("securitisation-edgar")


@mcp.tool()
def search_securitisation_deals(
    query: str = "",
    asset_class: Optional[str] = None,
    form_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 20,
    region: str = "US",
) -> dict[str, Any]:
    """Search EDGAR's full-text index for securitisation deals and filings.

    Returns issuer name, CIK, accession number, form type, filing date and a
    document URL for each match. Use `cik` from a result with the other tools.

    Args:
        query: Free text, e.g. an issuer or shelf name ("AmeriCredit", "BMARK").
        asset_class: Optional helper — one of auto, cmbs, rmbs, credit card, clo.
            Adds the right phrase to the search.
        form_type: Restrict to a form, e.g. "ABS-EE", "424B5", "10-D", "424B5,424H".
        date_from / date_to: ISO dates (YYYY-MM-DD) to bound the filing date.
        limit: Max results (default 20).
        region: Data source; "US" (SEC EDGAR) is the only one in this build.

    Coverage note: loan-level (ABS-EE) data exists only for auto loans/leases,
    commercial mortgages, residential mortgages and debt securities. Credit-card
    ABS and CLOs do NOT have loan-level data on EDGAR.
    """
    return registry.get_region(region).search_deals(
        query, asset_class=asset_class, form_type=form_type,
        date_from=date_from, date_to=date_to, limit=limit,
    )


@mcp.tool()
def get_deal_filings(
    cik: str,
    form_type: Optional[str] = None,
    limit: int = 100,
    region: str = "US",
) -> dict[str, Any]:
    """List a deal's filing history (prospectuses, 10-D reports, ABS-EE tapes…).

    Args:
        cik: The deal's Central Index Key (numeric; leading zeros optional).
        form_type: Optional filter, e.g. "10-D", "ABS-EE", "424B5,424H".
        limit: Max filings to return (most recent first).
        region: Data source; defaults to "US".
    """
    df = registry.get_region(region).get_deal_filings(cik, form_type=form_type, limit=limit)
    return {
        "deal": vars(df.deal),
        "count": len(df.filings),
        "filings": [vars(f) | {"document_url": f.document_url} for f in df.filings],
    }


@mcp.tool()
def get_filing_document(
    cik: str,
    accession: str,
    document: Optional[str] = None,
    max_chars: int = 200_000,
    offset: int = 0,
    region: str = "US",
) -> dict[str, Any]:
    """Retrieve a filing's text (e.g. a 424B prospectus or a 10-D investor report).

    HTML is converted to plain text. Long documents are returned in chunks — use
    `offset` with the reported `total_chars` to page through a large prospectus.

    Args:
        cik: The deal's CIK.
        accession: The filing's accession number (e.g. "0001193125-17-053869").
        document: Specific file name; if omitted, the primary document is used.
        max_chars: Max characters to return per call (default 200k).
        offset: Start position, for paging through long documents.
        region: Data source; defaults to "US".
    """
    return registry.get_region(region).get_filing_document(
        cik, accession, document, max_chars=max_chars, offset=offset
    )


@mcp.tool()
def extract_loan_level(
    cik: str,
    accession: str,
    mode: str = "summary",
    filters: Optional[dict[str, Any]] = None,
    out_path: Optional[str] = None,
    sample: int = 5,
    stratify_by: Optional[list[str]] = None,
    region: str = "US",
) -> dict[str, Any]:
    """Extract structured loan-level data from a Form ABS-EE filing.

    The asset tape can exceed 100 MB, so this streams it and, by default, returns
    pool-level analytics (counts, total balance, balance-weighted coupon / credit
    score / term, distributions by state/new-used/delinquency, delinquency buckets
    and period net-loss) plus a small sample of individual loans.

    Args:
        cik: The deal's CIK.
        accession: The ABS-EE filing's accession number.
        mode: "summary" (default) for pool stats + sample;
              "full" to also write every loan to a CSV file;
              "filter" to also write only loans matching `filters` to a CSV.
        filters: For filter mode, a dict of field -> condition. A scalar/list means
            equality/membership; a {"min":x,"max":y} dict means a numeric range.
            Example: {"obligorGeographicLocation": "TX",
                      "obligorCreditScore": {"max": 600}}.
        out_path: Where to write the CSV (full/filter modes). Defaults to a temp file.
        sample: Number of example loans to include in the summary (default 5).
        stratify_by: One dimension for a stratification table, or two for a cross-tab.
            Dimensions: fico_band, orig_term_band, pti_band, state, new_used,
            manufacturer, model_year, credit_score_type, delinquency_bucket.
            Examples: ["fico_band"]  or  ["fico_band", "state"]. Each bucket carries
            loans, balance, % of pool, WA APR/term, period net loss and 60+ dpd.
        region: Data source; defaults to "US".

    Only auto, CMBS, RMBS and debt-security ABS have loan-level tapes; this build
    is tuned for auto. Credit-card ABS and CLOs have no loan-level data on EDGAR.
    """
    if mode in ("full", "filter") and not out_path:
        cik_digits = re.sub(r"\D", "", cik)
        safe = re.sub(r"\W", "", accession)
        out_path = os.path.join(tempfile.gettempdir(), f"absee_{cik_digits}_{safe}.csv")
    return registry.get_region(region).extract_loan_level(
        cik, accession, mode=mode, filters=filters, out_path=out_path,
        sample=sample, stratify_by=stratify_by,
    )


@mcp.tool()
def extract_cmbs_loan_level(
    cik: str,
    accession: str,
    mode: str = "summary",
    filters: Optional[dict[str, Any]] = None,
    out_path: Optional[str] = None,
    sample: int = 5,
    stratify_by: Optional[list[str]] = None,
    region: str = "US",
) -> dict[str, Any]:
    '''Analyse a CMBS (commercial-mortgage) Form ABS-EE loan tape.

    Like extract_loan_level, but tuned for commercial mortgages: returns pool
    balance, balance-weighted DSCR (NCF), occupancy, LTV and coupon, pool debt
    yield, property-type and state concentration, the maturity profile, and the
    largest loans — plus optional stratification.

    Args:
        cik: The deal's CIK.
        accession: The CMBS ABS-EE filing's accession number.
        mode: "summary" (default), or "full"/"filter" to also write a CSV.
        filters: field -> condition (scalar/list = equality/membership;
            {"min":x,"max":y} = numeric range).
        out_path: CSV path for full/filter modes (defaults to a temp file).
        sample: Example loans to include (default 5).
        stratify_by: One or two of: property_type, property_state, dscr_band,
            ltv_band, occupancy_band, maturity_year, watchlist.
        region: Data source; defaults to "US".

    Use this for conduit CMBS; use extract_loan_level for auto ABS.
    '''
    if mode in ("full", "filter") and not out_path:
        cik_digits = re.sub(r"\D", "", cik)
        safe = re.sub(r"\W", "", accession)
        out_path = os.path.join(tempfile.gettempdir(), f"cmbs_{cik_digits}_{safe}.csv")
    return registry.get_region(region).extract_cmbs_loan_level(
        cik, accession, mode=mode, filters=filters, out_path=out_path,
        sample=sample, stratify_by=stratify_by,
    )


@mcp.tool()
def extract_loan_timeseries(
    cik: str,
    accessions: list[str],
    analysis: str = "static_pool_loss",
    periods: Optional[list[str]] = None,
    region: str = "US",
) -> dict[str, Any]:
    """Run a multi-tape (time-series) analysis across several ABS-EE filings.

    These are the analyses that only stacked loan-level data can produce — they
    join loans on `assetNumber` across periods. Pass the ABS-EE accessions for the
    same deal in chronological order (oldest first).

    Args:
        cik: The deal's CIK.
        accessions: ABS-EE accession numbers, oldest -> newest.
        analysis: One of:
            "static_pool_loss" — cumulative net-loss curve + pool factor by period;
            "roll_rate" — delinquency transition matrix between the two latest tapes;
            "prepayment" — period pool-paydown speed + voluntary-payoff tally.
        periods: Optional labels (e.g. report dates) aligned to `accessions`, used
            in the output instead of raw accession numbers.
        region: Data source; defaults to "US".

    Loan-level tapes (and therefore these analyses) exist only from ~late 2016
    (Reg AB II) and only for auto, CMBS, RMBS and debt-security ABS.
    """
    return registry.get_region(region).extract_loan_timeseries(
        cik, accessions, analysis=analysis, periods=periods
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
