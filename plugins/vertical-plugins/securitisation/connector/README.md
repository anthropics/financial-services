# Securitisation EDGAR connector (`edgar_sf`)

A free, local **MCP server** that wires US **SEC EDGAR** structured-finance data into
the `securitisation` plugin. No API key, no subscription — it uses EDGAR's public
endpoints and complies with SEC's fair-access policy (descriptive User-Agent,
request throttling).

## What it does — five tools

| Tool | What it does | EDGAR source |
|---|---|---|
| `search_securitisation_deals` | Find ABS/CLO deals & filings by text / asset class / form / date | Full-text search (`efts.sec.gov`) |
| `get_deal_filings` | List a deal's filing history (424B, 10-D, ABS-EE, 8-K …) | Submissions API (`data.sec.gov`) |
| `get_filing_document` | Fetch a prospectus (424B) or investor report (10-D) as text | Archives (`www.sec.gov/Archives`) |
| `extract_loan_level` | Stream-parse one ABS-EE tape into pool stats, delinquency buckets, period loss, stratifications and cross-tabs (`stratify_by`), with optional CSV | Archives (EX-102 asset XML) |
| `extract_loan_timeseries` | Multi-tape analyses across periods — roll-rate matrix, static-pool loss curve, prepayment — joined on `assetNumber` | Archives (EX-102 asset XML) |

## Coverage (and honest limits)

Loan-level (ABS-EE) data exists only for **auto loans/leases, commercial mortgages,
residential mortgages, and debt securities**. This build is tuned for **auto**, and
works well for **conduit CMBS** documents. **Credit-card ABS and CLOs have no
loan-level data on EDGAR** — see [`../DATA_PROVENANCE.md`](../DATA_PROVENANCE.md).

## Design — US-first, extensible

```
edgar_sf/
  config.py            endpoints + required SEC User-Agent
  core/  http_client   one compliant gateway (User-Agent, throttle, retries, gzip)
         models        Deal, FilingRef, DealFilings
  regions/ base        the Region interface every country implements
           registry    code ("US") -> implementation
           us/ edgar           search / filings / documents / extraction
               absee_parser    memory-safe streaming loan-level parser
               field_maps      ABS Schedule AL automobile field dictionaries
  server.py            exposes the tools over MCP (stdio)
```

To add **EU** or **AU** later: create `regions/eu/` (or `au/`) implementing the same
`Region` interface, register it in `server.py`, and every tool serves it via the
`region` argument — no other changes.

The loan-level parser streams record-by-record (`iterparse`) and clears each loan
after reading, so a 130 MB tape is processed with flat memory. By default
`extract_loan_level` returns pool analytics + a small sample; `mode="full"` or
`mode="filter"` additionally writes a CSV.

## Install & test

```bash
pip install -r requirements.txt        # only dependency: the official mcp SDK
python tests/test_connector.py          # offline tests (no network)
python -m edgar_sf.server               # run the MCP server (stdio)
```

The core/data logic uses only the Python standard library; `mcp` is needed only to
run the server.
