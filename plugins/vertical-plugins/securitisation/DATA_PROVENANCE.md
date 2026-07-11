# Data Provenance & Rights

This plugin uses **only free, public, rights-clean data** from the U.S. SEC's EDGAR
system. No paid subscription or API key is required or used. This note records the
sources, the licensing position, and exactly how data is processed.

## Sources
All data is retrieved at runtime from SEC EDGAR's public endpoints:

| Endpoint | Purpose |
|---|---|
| `https://efts.sec.gov/LATEST/search-index` | Full-text search for deals/filings |
| `https://data.sec.gov/submissions/CIK##########.json` | A filer's (trust's) filing history |
| `https://www.sec.gov/Archives/edgar/data/...` | The filing documents and the ABS-EE asset XML |

Nothing is retrieved from any paid, licensed, or gated source.

## Rights & licensing
- **The data:** SEC EDGAR is the SEC's system for public dissemination of required
  filings. The filings are public records, freely accessible and redistributable. There
  is no subscription or licence fee.
- **Fair-access compliance (operational, not a licence):** SEC asks callers to (a) send a
  descriptive **User-Agent** identifying themselves with contact info, and (b) stay at or
  below **10 requests/second**. The connector enforces both automatically (see
  `connector/edgar_sf/core/http_client.py`). Configure the User-Agent via the
  `SEC_EDGAR_USER_AGENT` environment variable.
- **This plugin's code:** © Daniel Cheah, licensed under **Apache 2.0** to match the
  parent repository.

## How data is processed
1. **Search** — `search_securitisation_deals` queries EDGAR full-text search and returns
   issuer, CIK, accession, form, and date.
2. **List filings** — `get_deal_filings` reads the submissions JSON for a CIK.
3. **Documents** — `get_filing_document` fetches a 424B/10-D, converts HTML to text, and
   returns it in pageable chunks.
4. **Loan-level** — `extract_loan_level` **streams** the ABS-EE EX-102 XML
   record-by-record (files can exceed 100 MB), computes pool-level analytics
   (balance-weighted averages, distributions), and returns a small sample. In `full` /
   `filter` mode it writes the (optionally filtered) records to a **local CSV** on the
   user's machine.

**Data handling:** processing is local and ephemeral. The plugin does **not** bundle,
cache server-side, or redistribute any filer data. The only data files committed to this
repository are the `connector/tests/sample_*.xml` fixtures, which are **synthetic**
(hand-written fake loans and commercial mortgages) used for offline tests — not real
filer data.

## Coverage & limits
Form ABS-EE asset-level (loan-level) data exists only for five asset classes:
residential mortgages, commercial mortgages, automobile loans, automobile leases, and
debt securities/resecuritisations. Consequently:

- **Strong loan-level coverage:** auto loan/lease ABS and conduit CMBS.
- **No loan-level data:** credit-card ABS (excluded from asset-level disclosure by rule;
  10-D reports carry pool-level data only).
- **Effectively absent:** registered private-label RMBS (the market issues under Rule
  144A, which carries no ABS-EE duty).
- **Not on EDGAR at all:** CLOs (144A private placements). The `clo-indenture-review`
  skill therefore operates on a document the user supplies, not on EDGAR.

## Out of scope (would require licensed data — deliberately excluded)
CLO collateral/payment data (Intex, trustees), 144A RMBS loan tapes, bond pricing /
spreads / yields, and ratings-agency feeds. The plugin neither uses nor depends on any
of these.

*Verified live against SEC systems in June 2026.*
