---
name: loan-tape-analysis
description: |
  Analyse Form ABS-EE loan-level data into pool stratifications and credit metrics —
  balance-weighted coupon/FICO/term, and distributions by FICO band, state, term,
  new/used, and delinquency. Tuned for auto ABS (the richest EDGAR loan-level coverage).

  **Use when:** the user wants pool stratifications, credit metrics, concentration
  analysis, or a cohort cut from an SEC ABS-EE loan tape.

  **Not for:** credit-card ABS or CLOs (no loan-level data on EDGAR), or document
  summaries (use abs-prospectus-analysis).
---

# Loan Tape Analysis (ABS-EE)

Extract structured pool analytics from an ABS-EE tape with **`extract_loan_level`**.
The tape can exceed 100 MB, so the tool streams it: **`mode="summary"`** returns pool
totals, balance-weighted averages, distributions, and a loan sample; **`mode="filter"`**
isolates a cohort and writes it to CSV.

## Key ABS-EE auto fields
| Field (XML tag) | Meaning |
|---|---|
| `originalLoanAmount` | Original financed amount |
| `reportingPeriodActualEndBalanceAmount` | **Current** balance (period end) |
| `originalInterestRatePercentage` / `reportingPeriodInterestRatePercentage` | APR / coupon |
| `obligorCreditScore` (+ `obligorCreditScoreType`) | FICO (and which model) |
| `originalLoanTerm` / `remainingTermToMaturityNumber` | Term and remaining term (months) |
| `obligorGeographicLocation` | Obligor state |
| `vehicleNewUsedCode` | New vs used |
| `paymentToIncomePercentage` | PTI |
| `currentDelinquencyStatus` | Days delinquent / status |
| `zeroBalanceCode` | Why a loan left the pool (prepaid, charged-off, repurchased) |

## Pool metrics (balance-weighted)
WA coupon/APR, **WA FICO**, WA original & remaining term, **WALA** (seasoning =
original − remaining term), WA PTI, and (where present) WA LTV. The connector reports
these directly; verify they reconcile to the matching **10-D** pool totals.

## Stratifications to build
- **FICO band:** <600, 600–659, 660–719, 720+ (and "no score").
- **APR band**, **original-term band** (≤48, 60, 72, 75+), **remaining-term band**.
- **Geography:** top states by balance, with % of pool and concentration flags.
- **New vs used.**
- **Delinquency bucket:** current, 31–60, 61–90, 90+.

For each stratum show **loan count, balance, % of pool**, and the **WA FICO / WA APR**
within the stratum.

## Cohort & trend analysis
- Use `mode="filter"` for cohorts, e.g.
  `{"obligorGeographicLocation": "TX", "obligorCreditScore": {"max": 600}}`, and export
  the CSV for bespoke cuts.
- A single ABS-EE is **point-in-time**. For prepayment/loss **trends** (CPR/CDR), pull
  the same deal's **consecutive monthly** ABS-EE tapes via `get_deal_filings`
  (`form_type="ABS-EE"`) and compare period over period; use `zeroBalanceCode` to
  separate voluntary prepayments from defaults.
- `extract_loan_timeseries` automates this by **joining loans across periods on
  `assetNumber`**. That join is only as reliable as the identifier: if an issuer
  **re-numbers, re-uses, or omits `assetNumber`** between filings (it is not guaranteed
  stable across tapes), loans can fail to match — inflating apparent prepayments (a
  carried-over loan looks like it left the pool) or dropping loans from the roll-rate
  matrix. Sanity-check that the joined loan count reconciles to each period's pool
  count before trusting roll-rate or static-pool-loss output, and fall back to
  period-over-period aggregate comparison where the identifier is unstable.

## Output
A pool-metrics header block, then stratification tables, then a short
**concentration / credit observations** note (e.g. geographic or low-FICO
concentrations, delinquency build). Cite the source filing and reporting period. State
clearly that figures are point-in-time and balance-weighted where balance is present.
This is analytical support, not investment advice.
