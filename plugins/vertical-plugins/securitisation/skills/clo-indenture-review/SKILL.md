---
name: clo-indenture-review
description: >-
  Review a CLO indenture or offering memorandum and extract the provisions that govern the
  deal: interest and principal waterfalls, coverage tests (OC/IC), collateral quality
  tests (WARF, WAS, diversity), concentration limits, the reinvestment regime, fees, and
  call/refi/reset terms, comparing each against US BSL market standard. Use when reviewing
  a CLO indenture or offering memorandum the user supplies. Not for finding CLOs on EDGAR
  (they are 144A and not filed there) — this skill works on a user-provided document.
---

# CLO Indenture Review

**CLOs are issued under Rule 144A and are not on SEC EDGAR.** This skill works on the
**indenture or offering memorandum the user provides** (PDF or text). State that limit
up front if they expected EDGAR retrieval.

## Quick structure primer
A CLO SPV issues rated debt (typically AAA / AA / A / BBB / BB, sometimes B) plus
**subordinated (equity) notes**, secured on a portfolio of **broadly syndicated
leveraged loans** actively managed by a **collateral manager** through a
**reinvestment period**. Cash is split into an **interest waterfall** and a
**principal waterfall**, governed by tests.

## Provisions to extract

### 1. Priority of payments
Both waterfalls, step by step (hand detail to payment-waterfall-extraction). Note
where **coverage-test failures divert** cash to delever senior notes.

### 2. Coverage tests (with cushions)
- **Overcollateralization (OC) / par value tests** per class — trigger ratio and the
  cushion to the trigger.
- **Interest coverage (IC) tests** per class.
- The **effect of failure**: redirect interest (and then principal) to pay down the
  most senior notes until cured.

### 3. Collateral quality tests
- **WARF** (Moody's weighted-average rating factor) and the rating model.
- **Weighted-average spread (WAS)** and **weighted-average coupon (WAC)**.
- **Weighted-average recovery rate (WARR)**.
- **Weighted-average life (WAL) test**.
- **Diversity score** (Moody's) and the **S&P CDO Monitor** / rating test.

### 4. Concentration limitations
Max **single obligor** (≈1.5–2%), largest **industry** buckets (≈10% / 12% / …),
**Caa/CCC** bucket (≈7.5%), **cov-lite**, **second-lien**, **DIP**, **fixed-rate**,
**non-USD**, **long-dated**, and **discount obligation** limits.

### 5. Reinvestment & trading
Reinvestment-period length; criteria to reinvest (maintain-or-improve tests);
trading gains/losses treatment; **par flush / interest diversion** test;
post-reinvestment principal rules.

### 6. Governance, fees, calls
Events of default and the **controlling class**; **senior** and **subordinated
management fees** plus any **incentive fee** (equity IRR hurdle); **non-call period**,
**optional redemption** (by equity majority), and **refinancing / reset** provisions.

## Benchmarking
Compare each extracted term against **current US BSL CLO market-standard** and **flag
off-market or borrower-favourable terms** (e.g. an unusually wide CCC bucket, a thin OC
cushion, a long reinvestment period, weak trading covenants). Be explicit that
benchmarks move over time and reflect a general market range, not advice.

## Output
A structured review: a **tests table** (test → trigger → cushion → market-standard),
the **concentration-limits table**, the **fee/call summary**, and a **flagged-items**
list. Cite the indenture section for every item; mark anything not found as
**"not located"**. This is analytical support for a professional's review — not legal
or investment advice.
