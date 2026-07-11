---
description: Prepayment & run-off across a deal's monthly ABS-EE tapes — CPR/CDR, static-pool loss, pool factor
argument-hint: "[deal name or CIK]"
---

# Analyse Prepayment & Run-off (multi-tape ABS-EE)

> Uses the bundled EDGAR connector — if its tools are missing or erroring, see [CONNECTOR.md](../CONNECTOR.md).

Stack a deal's consecutive monthly Form ABS-EE tapes into a life-of-deal view —
prepayment speed (CPR/SMM), default/loss (CDR, cumulative net loss), pool-factor decay,
and delinquency roll-rates.

## Workflow

### Step 1 — Build the period list
Call **`get_deal_filings`** with `form_type="ABS-EE"` for the CIK; collect the ABS-EE
accessions **oldest → newest** with their reporting-period dates. If given a name, find
the deal first with **`search_securitisation_deals`**.

### Step 2 — Load the skill
Use `skill: "prepayment-analysis"` for the CPR/CDR framework and the `assetNumber`
data-quality caveat.

### Step 3 — Run the time-series
Call **`extract_loan_timeseries(cik, accessions, analysis=..., periods=...)`** with
`analysis` = `prepayment`, `static_pool_loss`, or `roll_rate`. Pass the dates as
`periods` so output is labelled by reporting date.

### Step 4 — Deliver
A period-by-period table (CPR/SMM, CDR, cumulative loss, pool factor), the curve, and a
plain-English trend read. Separate voluntary payoffs (`zeroBalanceCode = prepaid`) from
defaults. Cite the deal and periods.

## Coverage note
Loan-level tapes exist only from ~late 2016 and only for **auto, CMBS, RMBS, and debt
securities** — **not** credit-card ABS or CLOs.
