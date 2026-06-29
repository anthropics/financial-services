# Securitisation — Structured Finance (SEC EDGAR)

A vertical plugin for structured-finance / securitisation work, backed by a **free,
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
| `/securitisation:analyze-loan-tape` | Stratify a Form ABS-EE loan tape and compute pool credit metrics |
| `/securitisation:extract-waterfall` | Extract the priority of payments, with the triggers that reorder it |
| `/securitisation:review-clo-indenture` | Review a (user-supplied) CLO indenture: coverage/quality tests, concentration limits, reinvestment |

### Skills (fire automatically when relevant)
`deal-search` · `abs-prospectus-analysis` · `loan-tape-analysis` ·
`payment-waterfall-extraction` · `clo-indenture-review`

### Connector (`connector/`)
A local Python MCP server exposing five tools — `search_securitisation_deals`,
`get_deal_filings`, `get_filing_document`, `extract_loan_level` (pool stats,
stratifications and cross-tabs) and `extract_loan_timeseries` (roll-rate, static-pool
loss, prepayment across stacked tapes) — over EDGAR's public endpoints.
Standard-library only except the official `mcp` SDK. See
[`connector/README.md`](./connector/README.md).

## Coverage (honest, verified)
| Asset class | Documents (424B / 10-D) | Loan-level (ABS-EE) |
|---|---|---|
| Auto loan / lease ABS | ✅ | ✅ strong (tuned for this) |
| Conduit CMBS | ✅ | ✅ strong |
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

## Install

### Cowork
1. **Settings → Plugins → Add plugin** → paste the repo URL
   `https://github.com/dacheah/financial-services` (or upload a zip of this folder).
2. One-time, so the local connector can run:
   ```bash
   pip install mcp
   ```
   (Python 3.10+ required.) Optionally set a contact User-Agent —
   `SEC_EDGAR_USER_AGENT="Your Name your@email"` — though the bundled default works.

### Claude Code
```bash
claude plugin marketplace add dacheah/financial-services
claude plugin install securitisation@claude-for-financial-services
```

## Usage examples
```
/securitisation:search-deals AmeriCredit auto
/securitisation:parse-abs-prospectus  (then pick the 424B5)
/securitisation:analyze-loan-tape  (then pick the latest ABS-EE period)
/securitisation:extract-waterfall
/securitisation:review-clo-indenture  (attach the indenture / offering memorandum)
```

## Extensible to other regions
The connector is organised **US-first but region-neutral**: a `Region` interface with a
clean `us/` implementation (SEC EDGAR). Europe and Australia are intended to be added as
sibling `eu/` and `au/` modules implementing the same interface — every command, skill,
and tool then serves them via a `region` argument, with no other changes.

## Author
**Daniel Cheah** — [danielcheah.com](https://danielcheah.com) · [LinkedIn](https://www.linkedin.com/in/dcheah/)

## Licence
[Apache License 2.0](../../../LICENSE), matching the parent repository. SEC EDGAR data is
public; see [`DATA_PROVENANCE.md`](./DATA_PROVENANCE.md) for sources, rights, and processing.
