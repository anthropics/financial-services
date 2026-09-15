# Output schemas — single-tape loan-level analysis (`extract_loan_level`)

The shapes `extract_loan_level` returns and the shapes this skill's deliverables
should follow. Example rows are marked **illustrative** — never present them as
extracted figures. Every metric derives from Reg AB II **Schedule AL (automobile)**
asset-level fields mapped in `connector/edgar_sf/regions/us/field_maps.py`; the
field-provenance table is at the end.

Multi-period shapes (roll-rate matrix, static-pool loss curve, prepayment by cohort)
live with the skill that produces them:
[`skills/prepayment-analysis/references/output-schemas.md`](../../prepayment-analysis/references/output-schemas.md).
Cumulative net loss is a deal-life figure, so it comes from stacked tapes, not a
single tape.

## Conventions

- **Weighting** — averages are balance-weighted on `reportingPeriodActualEndBalanceAmount`
  (current loan balance) unless a column says `count`.
- **FICO bands** — `<550 / 550–599 / 600–649 / 650–699 / 700+`. Edges configurable; source is
  `obligorCreditScore` (only where `obligorCreditScoreType` is a comparable model — flag mixed types).
- **Delinquency** — from `currentDelinquencyStatus` (days past due) → buckets
  `current / 31–60 / 61–90 / 91+`; `60+` = 61+ combined.
- **Net loss** — `chargedoffPrincipalAmount − recoveredAmount` in the period; cumulative net loss
  `% = Σ net loss ÷ original pool balance`.
- **Period key** — `reportingPeriodEndingDate`; loans keyed across months on `assetNumber`.

## 1. Pool summary (header object)

Returned with every call as context.

```json
{
  "deal": "AMCAR 2024-1", "cik": "0002020251",
  "as_of_period": "2026-04-30", "transaction_month": 24,
  "n_loans": "‹tape›", "current_balance": "‹tape›", "pool_factor_pct": "‹tape›",
  "wa_apr_pct": "‹tape›", "wa_remaining_term": "‹tape›", "wa_original_term": "‹tape›",
  "wa_fico": "‹tape›", "avg_balance": "‹tape›",
  "cumulative_net_loss_pct": "‹tape›", "dq_60plus_pct": "‹tape›"
}
```

## 2. Single-dimension stratification

One row per bucket of a chosen `dimension`.

`dimension ∈ { fico_band, state, orig_term_band, new_used, vehicle_make, pti_band, model_year, income_verification }`

| Column | Type | Definition |
|---|---|---|
| `bucket` | string | The band/category value |
| `n_loans` | int | Count of loans in bucket |
| `current_balance` | number | Σ current balance |
| `pct_of_pool` | % | Bucket balance ÷ pool balance |
| `wa_apr` | % | Balance-weighted `originalInterestRatePercentage` |
| `wa_remaining_term` | months | Balance-weighted remaining term |
| `cum_net_loss_pct` | % | Cumulative net loss ÷ bucket original balance |
| `dq_60plus_pct` | % | 60+ dpd balance ÷ bucket balance |
| `cdr_annualised` | % | Annualised conditional default rate |

Illustrative (`dimension = fico_band`):

| bucket | n_loans | pct_of_pool | wa_apr | cum_net_loss_pct | dq_60plus_pct |
|---|---|---|---|---|---|
| <550 | _illus._ | 18% | 19.1% | 9.5% | 6.1% |
| 550–599 | _illus._ | 34% | 16.9% | 6.8% | 4.0% |
| 600–649 | _illus._ | 30% | 14.8% | 4.2% | 2.3% |
| 650–699 | _illus._ | 15% | 12.6% | 2.3% | 1.1% |
| 700+ | _illus._ | 3% | 10.9% | 1.1% | 0.4% |
| **Pool** | 73,190 | 100% | 16.18% | **5.83%** | — |

> The bottom row is the 10-D figure; every row above it is the differentiator.

## 3. Cross-tab (two dimensions)

A matrix of one `cell_metric` over `row_dimension × col_dimension`
(e.g. `fico_band × state`, `cell_metric = cum_net_loss_pct`).

```json
{
  "row_dimension": "fico_band", "col_dimension": "state",
  "cell_metric": "cum_net_loss_pct",
  "cols": ["TX","FL","OH","CA","other"],
  "rows": [
    { "bucket": "<550",    "cells": ["‹tape›", "...", "...", "...", "..."], "row_total": "‹tape›" },
    { "bucket": "550–599", "cells": ["‹tape›", "...", "...", "...", "..."], "row_total": "‹tape›" }
  ],
  "col_totals": ["‹tape›", "..."]
}
```

Answers questions the pool average cannot, e.g. *"is the Texas concentration low-FICO or
high-FICO?"* Also report each tail's **share of losses vs share of balance** (e.g. the <550
slice).

## Field provenance

| Output | ABS-EE Schedule AL field(s) |
|---|---|
| FICO band, WA FICO | `obligorCreditScore`, `obligorCreditScoreType` |
| State | `obligorGeographicLocation` |
| APR | `originalInterestRatePercentage` |
| Term bands | `originalLoanTerm`, remaining = f(`loanMaturityDate`, period) |
| New/used, make, model-year | `vehicleNewUsedCode`, `vehicleManufacturerName`, `vehicleModelYear` |
| PTI band | `paymentToIncomePercentage` |
| Income/employment verification | `obligorIncomeVerificationLevelCode`, `obligorEmploymentVerificationCode` |
| Balance, pool factor | `reportingPeriodActualEndBalanceAmount`, `originalLoanAmount` |
| Delinquency states | `currentDelinquencyStatus` |
| Net loss, recoveries | `chargedoffPrincipalAmount`, `recoveredAmount`, `repossessedProceedsAmount` |
| Prepayment | `zeroBalanceCode`, `zeroBalanceEffectiveDate`, `actualPrincipalCollectedAmount` |

*Coverage caveat — loan-level tapes exist only for deals issued from late 2016 (Reg AB II) and
only for auto, CMBS, RMBS, and debt asset classes. Never credit cards or CLOs.*
