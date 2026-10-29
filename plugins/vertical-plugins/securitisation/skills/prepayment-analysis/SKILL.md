---
name: prepayment-analysis
description: >-
  Measure how an ABS pool pays down and defaults over its life by stacking a deal's
  consecutive monthly Form ABS-EE tapes: prepayment speed (CPR/SMM), default and loss
  (CDR, cumulative net loss), pool-factor decay, and delinquency roll-rates, separating
  voluntary payoffs from defaults. Use when the user asks for prepayment speeds, CPR or
  CDR, static-pool loss curves, pool factor or run-off, roll-rates, or any over-time,
  across-periods view of a single deal. Not for a single point-in-time pool cut (use
  loan-tape-analysis) or cross-deal comparison (use deal-comps); credit-card ABS and CLOs
  have no loan-level data on EDGAR.
---

# Prepayment & Run-off Analysis (multi-tape ABS-EE)

> EDGAR access in this skill uses the bundled `securitisation-edgar` connector. If its tools are missing or erroring, see [CONNECTOR.md](../../CONNECTOR.md) — do not substitute web search for filings.

A single ABS-EE tape is one photograph; prepayment and loss are a *movie*. This skill
stacks a deal's **consecutive monthly** tapes and joins loans on `assetNumber` across
periods with the connector's **`extract_loan_timeseries`** tool — the analyses that
aggregate 10-D reports cannot reproduce.

## Workflow

### Step 1 — Build the period list (oldest → newest)
Call **`get_deal_filings`** with `form_type="ABS-EE"` for the deal's CIK. Collect the
ABS-EE accessions in **chronological order** and, where possible, capture each filing's
reporting-period date to use as a clean label.

### Step 2 — Pick the analysis
Call **`extract_loan_timeseries(cik, accessions, analysis=..., periods=...)`** with one of:

| `analysis` | What it returns | Reads as |
|---|---|---|
| `prepayment` | Period pool-paydown speed + voluntary-payoff tally | **CPR / SMM** — how fast the pool prepays |
| `static_pool_loss` | Cumulative net-loss curve + pool factor by period | **CDR / cumulative loss** and run-off |
| `roll_rate` | Delinquency transition matrix between the two latest tapes | Migration current → 30 → 60 → 90+ |

Pass `periods=` the reporting dates aligned to the accessions so the output is labelled
by date, not raw accession numbers.

### Step 3 — Interpret (say what the numbers mean)
- **Prepayment (CPR):** annualised voluntary paydown. The **voluntary** signal is
  `zeroBalanceCode = prepaid` — separate it from involuntary run-off (defaults /
  charge-offs) so a wave of defaults isn't mistaken for fast prepayment.
- **CDR / cumulative net loss:** the default/loss side; pair with the pool factor to see
  how much collateral remains.
- **Pool factor:** current balance ÷ original — the decay curve of the deal.
- **Roll-rates:** how delinquency buckets migrate month to month — the early-warning view.

### Step 4 — Deliver
Render to the schemas in [references/output-schemas.md](references/output-schemas.md):
a period-by-period table (CPR/SMM, CDR, cumulative loss, pool factor), a short curve
description, and a plain-English read of the trend (speeding up / slowing, loss build,
delinquency migration). Cite the deal and the reporting periods used.

## Data-quality caveat (state it)
The multi-period join is only as reliable as `assetNumber`. If an issuer re-numbers,
re-uses, or omits it between filings (it is **not guaranteed stable** across tapes),
loans can fail to match — inflating apparent prepayment (a carried-over loan looks like
it left the pool) or dropping loans from the roll-rate matrix. Sanity-check that the
joined loan count reconciles to each period's pool count before trusting the output, and
fall back to period-over-period aggregate comparison where the identifier is unstable.

## Coverage note
Loan-level tapes exist only from ~late 2016 (Reg AB II) and only for **auto, CMBS, RMBS,
and debt securities**. There is **no loan-level data for credit-card ABS or CLOs** — say
so plainly if asked.
