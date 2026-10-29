"""Configuration: SEC endpoints and the (required) User-Agent.

SEC's fair-access policy REQUIRES every request to declare a descriptive
User-Agent that identifies the caller with contact information. Requests
without one are blocked. We read it from the SEC_EDGAR_USER_AGENT environment
variable (set in the plugin's .mcp.json) and fall back to a project default so
the connector is compliant out of the box without hard-coding a personal email.
"""
from __future__ import annotations

import os

# A website is an acceptable SEC contact, so the public default points at the
# project site rather than embedding a personal email in published code.
DEFAULT_USER_AGENT = "ProjectAnt-Securitisation-EDGAR/0.1 (+https://danielcheah.com)"


def user_agent() -> str:
    """The User-Agent string sent on every SEC request."""
    return os.environ.get("SEC_EDGAR_USER_AGENT", DEFAULT_USER_AGENT).strip() or DEFAULT_USER_AGENT


# --- Core EDGAR endpoints (all free, public, no API key) ---------------------
EFTS_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"          # full-text deal search
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"  # a filer's filing history
ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"            # the actual documents/files

# SEC asks callers to stay at or below 10 requests/second. We default to a
# comfortably conservative spacing; override via SEC_EDGAR_MIN_INTERVAL.
MIN_REQUEST_INTERVAL = float(os.environ.get("SEC_EDGAR_MIN_INTERVAL", "0.15"))
