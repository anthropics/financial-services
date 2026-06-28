---
description: Analyse ABS-EE loan-level data — pool stratifications and credit metrics
argument-hint: "[deal name, CIK, or accession number]"
---

# Analyse Loan Tape (ABS-EE)

Turn a Form ABS-EE loan-level tape into pool stratifications and credit metrics —
weighted-average coupon, FICO, term, and distributions by state, vehicle, and
delinquency. Tuned for **auto** ABS (the asset class with the richest EDGAR coverage).

## Workflow

### Step 1 — Locate the ABS-EE filing
- If given a CIK, call **`get_deal_filings`** with `form_type="ABS-EE"` and pick the
  reporting period (the most recent, or one the user names).
- If given a deal name, find it first with **`search_securitisation_deals`**.

### Step 2 — Load the skill
Use `skill: "loan-tape-analysis"` for the stratification framework and metric
definitions.

### Step 3 — Extract
Call **`extract_loan_level`** with the CIK and accession:
- Default (`mode="summary"`) → pool totals, balance-weighted averages, and
  distributions. Best for the standard pool view.
- `mode="filter"` with `filters` → isolate a cohort (e.g.
  `{"obligorGeographicLocation": "TX", "obligorCreditScore": {"max": 600}}`) and
  write it to CSV for bespoke cuts.

### Step 4 — Deliver
Stratification tables (by FICO band, state, term, new/used, delinquency) and a
header block of pool metrics. Offer to export a CSV or run a specific cohort.

## Coverage note
Loan-level tapes exist for **auto, CMBS, RMBS, and debt securities** only. There is
**no loan-level data for credit-card ABS or CLOs** — say so plainly if asked.
