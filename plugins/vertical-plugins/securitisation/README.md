# Securitisation — Structured Finance (SEC EDGAR)

A vertical plugin for structured-finance / securitisation work (US spelling: *securitization*), backed by a **free,
local SEC EDGAR data connector**. It searches registered ABS deals, retrieves their
prospectuses and investor reports, and extracts loan-level data from Form ABS-EE — and
ships skills for prospectus analysis, CLO indenture review, and payment-waterfall
extraction.

It is the **only connector in this marketplace that needs no paid subscription**: SEC
EDGAR is public data. Everything else here (Daloopa, Morningstar, S&P, Moody's, …)
requires a licence; this fills that gap for the structured-finance corner of the market.

> **Not investment, legal, tax, or accounting advice.** This plugin drafts analyst work
> product — deal summaries, stratifications, waterfall maps — for review by a qualified
> professional. It does not make recommendations or execute anything. You are
> responsible for verifying every output against the source filings.

## What's inside

### Slash commands
| Command | What it does |
|---|---|
| `/securitisation:search-deals` | Find registered ABS/CMBS deals on EDGAR and list a deal's filings |
| `/securitisation:parse-abs-prospectus` | Turn a 424B prospectus into a structured deal summary (tranches, credit enhancement, collateral, triggers) |
| `/securitisation:analyze-loan-tape` | Stratify a Form ABS-EE **auto** loan tape and compute pool credit metrics |
| `/securitisation:analyze-cmbs-tape` | Analyse a **CMBS** ABS-EE tape — DSCR, debt yield, property mix, maturity wall |
| `/securitisation:analyze-prepayment` | Stack a deal's monthly ABS-EE tapes for prepayment (CPR), loss (CDR), pool-factor decay and roll-rates |
| `/securitisation:deal-comps` | Compare several deals side by side — capital structure, credit enhancement, collateral, structure |
| `/securitisation:extract-waterfall` | Extract the priority of payments, with the triggers that reorder it |
| `/securitisation:review-clo-indenture` | Review a (user-supplied) CLO indenture: coverage/quality tests, concentration limits, reinvestment |

### Skills (fire automatically when relevant)
`deal-search` · `abs-prospectus-analysis` · `loan-tape-analysis` ·
`cmbs-loan-tape-analysis` · `prepayment-analysis` · `deal-comps` ·
`payment-waterfall-extraction` · `clo-indenture-review`

### Connector (`connector/`)
A local Python MCP server exposing six tools — `search_securitisation_deals`,
`get_deal_filings`, `get_filing_document`, `extract_loan_level` (auto pool stats,
stratifications and cross-tabs), `extract_cmbs_loan_level` (commercial-mortgage DSCR,
debt yield, property mix and maturity wall) and `extract_loan_timeseries` (roll-rate,
static-pool loss, prepayment across stacked tapes) — over EDGAR's public endpoints.
Standard-library only except the official `mcp` SDK. See
[`connector/README.md`](./connector/README.md).

## Coverage (honest, verified)
| Asset class | Documents (424B / 10-D) | Loan-level (ABS-EE) |
|---|---|---|
| Auto loan / lease ABS | ✅ | ✅ strong (tuned for this) |
| Conduit CMBS | ✅ | ✅ strong (dedicated DSCR / debt-yield / property analytics) |
| Credit-card ABS | ✅ | ❌ none — excluded from asset-level disclosure by rule |
| Registered private-label RMBS | ⚠️ rare | ❌ effectively absent (market is 144A) |
| CLOs | ❌ not on EDGAR | ❌ not on EDGAR (144A — use the indenture-review skill on a supplied doc) |

Full detail and methodology: [`DATA_PROVENANCE.md`](./DATA_PROVENANCE.md).

## Why the loan tape is the differentiator

Most of what this plugin does over registered ABS — finding deals, parsing a 424B, mapping a
waterfall, charting a deal's 10-D history — is reproducible from EDGAR's free, public endpoints.
The part that is **not** reproducible without this connector is **loan-level analysis**, and it
is the reason the plugin exists.

A 10-D investor report gives one **pool-wide** number per metric: e.g. AMCAR 2024-1's cumulative
net loss is `5.83%`. That single average says nothing about *which* loans drive it, in a pool
whose obligor credit scores span 500–700. Only the Form ABS-EE tape carries every loan, so only
`extract_loan_level` can split that one number into the distribution behind it — loss by FICO
band, by state, by original term, by new/used; cross-tabs such as FICO × state; and, by stacking
monthly tapes, roll-rate matrices and static-pool loss curves.

The tape is a single XML of **~130–160 MB**, beyond any general fetch path — which is precisely
why the streaming parser is the moat. Target output formats for these analyses are specified in
[`LOAN_LEVEL_OUTPUTS.md`](./LOAN_LEVEL_OUTPUTS.md).

## Installation

**Claude Code** (primary path) — run in a session:
```text
/plugin marketplace add dacheah/financial-services      # after #283 merges: anthropics/financial-services
/plugin install securitisation@claude-for-financial-services
```
Then install the connector's one dependency and restart:
```bash
pip install "mcp>=1.2.0"      # the only third-party dependency; Python 3.10+
```
Restart Claude Code, then try:
```text
/securitisation:search-deals AmeriCredit auto
```

**Cowork** — install the `securitisation` plugin from Cowork's plugin manager (or a
provided `.plugin` file), run the same `pip install "mcp>=1.2.0"` on your machine, and
start a fresh session.

The plugin's [`.mcp.json`](./.mcp.json) auto-starts the local connector. Skills fire on
natural language; commands on the slash. Optionally set a contact User-Agent —
`SEC_EDGAR_USER_AGENT="Your Name your@email"` — though the bundled default works.

### Which surfaces support what
| Surface | Skills & commands | Loan-level connector |
|---|---|---|
| Claude Code | ✅ | ✅ (local runtime) |
| Cowork | ✅ | ✅ (local runtime) |
| claude.ai chat | ✅ | ❌ — needs a local runtime; document/term-sheet analysis only |

### Verify the connector is live
Ask Claude to run `search_securitisation_deals` for any issuer. If it returns EDGAR
results, the server is running. If it **web-searches instead**, the connector isn't
loaded — re-check `pip install "mcp>=1.2.0"` and restart the session. (If the SDK is
missing, the server now says so explicitly in the MCP logs rather than failing quietly.)

## Usage examples
```
/securitisation:search-deals AmeriCredit auto
/securitisation:parse-abs-prospectus  (then pick the 424B5)
/securitisation:analyze-loan-tape  (auto: pick the latest ABS-EE period)
/securitisation:analyze-cmbs-tape  (CMBS: DSCR, debt yield, maturity wall)
/securitisation:extract-waterfall
/securitisation:review-clo-indenture  (attach the indenture / offering memorandum)
```

## Extensible by design — and an honest note on other regions
The connector is organised **US-first but region-neutral**: a `Region` interface with a
clean `us/` implementation (SEC EDGAR), so new sources slot in behind the same tools via a
`region` argument.

The binding constraint for the EU and Australia, though, is **data rights, not code**.
Unlike EDGAR's fully open dissemination, EU loan-level data (European DataWarehouse / ESMA
securitisation repositories) and Australian data (RBA Securitisation Dataset) are available
only to *registered, permissioned* users and aren't freely redistributable. So a free,
rights-clean EU/AU *loan-level* module isn't currently feasible; any future regional module
would be limited to public deal/aggregate layers or a credentialed (non-free) integration,
documented as such.

## Author
**Daniel Cheah** — [danielcheah.com](https://danielcheah.com) · [LinkedIn](https://www.linkedin.com/in/dcheah/)

## Licence
[Apache License 2.0](../../../LICENSE), matching the parent repository. SEC EDGAR data is
public; see [`DATA_PROVENANCE.md`](./DATA_PROVENANCE.md) for sources, rights, and processing.
