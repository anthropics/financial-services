# Connector — `securitisation-edgar` (setup, health check, recovery)

This plugin bundles a **local Python MCP server** (`connector/`) that provides all
EDGAR data access. The skills and commands assume its tools are available. This note
is the single reference for confirming the connector is healthy and recovering it
when it is not. Internals and architecture: [`connector/README.md`](./connector/README.md).

## The six tools

| Tool | What it does |
|---|---|
| `search_securitisation_deals` | Find ABS/CMBS deals and filings by text, asset class, form type, date |
| `get_deal_filings` | List a deal's (CIK's) full filing history — 424B, 10-D, ABS-EE, 8-K … |
| `get_filing_document` | Fetch a prospectus or investor report as pageable text |
| `extract_loan_level` | Stream-parse an **auto** ABS-EE tape — pool stats, stratifications, cross-tabs, CSV export |
| `extract_cmbs_loan_level` | Stream-parse a **CMBS** ABS-EE tape — DSCR, debt yield, occupancy, LTV, property mix, maturity wall |
| `extract_loan_timeseries` | Multi-tape analyses — roll-rates, static-pool loss, prepayment — joined on `assetNumber` |

## Health check

The connector is healthy when the six tools above are visible in the session's tool
list. Quick probe: call `search_securitisation_deals` for any large issuer (e.g.
"AmeriCredit"). EDGAR results back = healthy.

## If the tools are missing or erroring

**Do not silently substitute web search for connector tools.** Web results are not
EDGAR filings; presenting them as such defeats the plugin's provenance guarantees.
State plainly that the connector is not running, then walk the user through recovery:

1. **Install the one dependency** (the server itself is standard-library only):
   ```bash
   pip install "mcp>=1.2.0"
   ```
   Python **3.10+** is required.
2. **Restart the session** (Claude Code: restart; Cowork: start a fresh session).
   Plugin MCP servers start when the plugin loads — a mid-session install is not
   picked up until restart.
3. **Re-run the health check** above.

While the connector is down, the document-analysis skills still work on
**user-supplied documents**: `clo-indenture-review` (always document-based),
`payment-waterfall-extraction`, and `abs-prospectus-analysis` (attach the 424B or
indenture instead of fetching it). Loan-level analysis has no fallback — it needs
the connector.

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Tools absent from the session | `mcp` SDK not installed, or session not restarted after install | Steps 1–2 above |
| `ModuleNotFoundError: edgar_sf` | Server launched outside the plugin runtime, so `${CLAUDE_PLUGIN_ROOT}` was never expanded | Point `cwd`/`PYTHONPATH` at an absolute path to `connector/` — see [`connector/README.md`](./connector/README.md) |
| EDGAR requests blocked / 403 | Missing or rejected User-Agent | Set `SEC_EDGAR_USER_AGENT="Your Name your@email"`; a compliant project default applies when unset |
| Loan-level calls feel slow | Normal: tapes run ~130–160 MB and requests are throttled to respect SEC fair-access | Let it stream; the parser holds flat memory. Warn the user it can take minutes |
| Time-series counts don't reconcile | `assetNumber` unstable across an issuer's tapes | See the data-quality caveat in the `prepayment-analysis` skill; fall back to aggregate period-over-period comparison |

## Environment variables

| Variable | Required | Default |
|---|---|---|
| `SEC_EDGAR_USER_AGENT` | No | A compliant project User-Agent (`connector/edgar_sf/config.py`) — set your own contact to identify yourself to the SEC |
| `SEC_EDGAR_MIN_INTERVAL` | No | `0.15` seconds between requests (SEC asks ≤ 10 req/s) |

The plugin's [`.mcp.json`](./.mcp.json) deliberately sets no `SEC_EDGAR_USER_AGENT`,
so a value you export in your environment is respected.
