# Dividend Discount Model — Methodology Reference

Detailed math and modelling guidance for the `ddm-model` skill. Read this before building a multi-stage model or valuing a financial institution.

All DDM variants share one principle: the intrinsic value of a share is the present value of the dividends it will pay, discounted at the **cost of equity** `rₑ` (never WACC). Every variant requires `rₑ > g` for any perpetual-growth term.

## Table of Contents
1. [Cost of equity](#1-cost-of-equity)
2. [Single-stage (Gordon growth)](#2-single-stage-gordon-growth)
3. [Two-stage DDM](#3-two-stage-ddm)
4. [Three-stage DDM and the H-model](#4-three-stage-ddm-and-the-h-model)
5. [DDM for financials (ROE-driven)](#5-ddm-for-financials-roe-driven)
6. [Total-payout DDM (buybacks)](#6-total-payout-ddm-buybacks)
7. [Justified multiples cross-check](#7-justified-multiples-cross-check)
8. [Reconciliation with DCF and comps](#8-reconciliation-with-dcf-and-comps)
9. [Worked example (two-stage)](#9-worked-example-two-stage)

---

## 1. Cost of equity
Discount every DDM at the cost of equity from CAPM:
```
rₑ = r_f + β · ERP      (+ size premium, + country-risk premium if warranted)
```
- `r_f` — risk-free rate, matched to a long horizon (typically the 10Y government yield).
- `β` — levered equity beta of the company (or a peer-derived beta).
- `ERP` — equity risk premium for the relevant market.

Do **not** use WACC: dividends are cash flows to equity, so the equity discount rate applies. (The `dcf-model` skill derives the same CAPM cost of equity in its WACC step — reuse that, taking the cost-of-equity portion only.)

## 2. Single-stage (Gordon growth)
For a company already at a stable, perpetual dividend growth rate `g`:
```
V₀ = D₁ / (rₑ − g) = D₀ (1 + g) / (rₑ − g)        requires rₑ > g
```
Use only when growth is genuinely mature and stable. The value is extremely sensitive to the `rₑ − g` spread — always show a sensitivity table over both.

## 3. Two-stage DDM
An explicit high-growth phase of `n` years at `g₁`, then a stable perpetual rate `g`:
```
PV(explicit) = Σₜ₌₁ⁿ  D₀ (1 + g₁)ᵗ / (1 + rₑ)ᵗ

TVₙ = Dₙ₊₁ / (rₑ − g) = D₀ (1 + g₁)ⁿ (1 + g) / (rₑ − g)

V₀ = PV(explicit) + TVₙ / (1 + rₑ)ⁿ               requires rₑ > g
```
The terminal value is computed **at the end of year `n`** and then discounted `n` periods back. A common error is discounting `TVₙ` by `n+1` periods — it is already an end-of-year-`n` value.

## 4. Three-stage DDM and the H-model
Three-stage models a high-growth phase, a linear-decline (fade) phase, and a stable phase. The **H-model** is a closed-form approximation of a growth rate that declines *linearly* from an initial `g_S` to a long-run `g_L` over a fade period of `2H` years:
```
V₀ = [ D₀ (1 + g_L) + D₀ · H · (g_S − g_L) ] / (rₑ − g_L)      requires rₑ > g_L
```
- `H` = half the length of the fade period (e.g. a 10-year linear fade → `H = 5`).
- The first term is the value as if the company grew at `g_L` forever; the second term is the extra value from the above-normal growth during the fade.
- Use the H-model as a fast approximation or a cross-check; build the full three-stage schedule explicitly when precision matters.

## 5. DDM for financials (ROE-driven)
For banks and insurers, "free cash flow" is ill-defined, so the DDM is the natural method — but drive dividends from profitability rather than a bare growth rate:
```
retention  b = 1 − payout
sustainable growth  g = ROE · b
EPSₜ = ROE · BVPSₜ₋₁
BVPSₜ = BVPSₜ₋₁ + EPSₜ · b          (retained earnings build book value)
DPSₜ = EPSₜ · payout
```
Then discount `DPSₜ` at `rₑ` exactly as in the two-/three-stage models. This links value directly to the spread between ROE and the cost of equity: a bank earning `ROE = rₑ` is worth book value; `ROE > rₑ` justifies a premium to book. Regulatory capital minimums cap how much can be paid out — do not assume a payout that breaches capital requirements.

## 6. Total-payout DDM (buybacks)
When a company returns most cash through **buybacks**, a dividend-only DDM understates value. Two fixes:
- **Total-payout per share:** replace `DPSₜ` with `(dividends + net buybacks)ₜ / shares`, holding the analysis on a per-share basis.
- **Aggregate then divide:** discount total cash returned to equity, then divide by (declining) shares outstanding.
Be careful that share count falls as buybacks occur; keep the per-share and aggregate views consistent.

## 7. Justified multiples cross-check
The Gordon model implies "justified" multiples that sanity-check the output against comps:
```
justified leading P/E = payout / (rₑ − g)
justified P/B         = (ROE − g) / (rₑ − g)
```
If the DDM's implied P/E or P/B is wildly different from where the peer group trades, revisit the assumptions.

## 8. Reconciliation with DCF and comps
The DDM yields **equity value per share directly** — directly comparable to the current price and to a DCF's equity value per share and the comps-implied price. Present all methods in a range and weight by fit:
- Weight **DDM** highest for financials, REITs, utilities, and mature high-payout names.
- Weight **DCF** (`dcf-model`) highest for non-financial operating companies with meaningful reinvestment.
- Weight **comps** (`comps-analysis`) for a market-relative read.
Always present a range (Bear/Base/Bull), not a point estimate.

## 9. Worked example (two-stage)
Inputs: current dividend `D₀ = $2.00`; Stage 1 growth `g₁ = 8%` for `n = 5` years; stable growth `g = 3%`; cost of equity `rₑ = 9%`.

| Year | DPS | PV @ 9% |
|---:|---:|---:|
| 1 | 2.1600 | 1.9817 |
| 2 | 2.3328 | 1.9635 |
| 3 | 2.5194 | 1.9455 |
| 4 | 2.7210 | 1.9276 |
| 5 | 2.9387 | 1.9099 |
| **PV of explicit dividends** | | **9.7281** |

Terminal value (first stable-phase dividend `D₆ = 2.9387 × 1.03 = 3.0268`):
```
TV₅ = D₆ / (rₑ − g) = 3.0268 / (0.09 − 0.03) = 50.4469
PV of TV₅ = 50.4469 / (1.09)⁵ = 32.7870
```
Intrinsic value per share:
```
V₀ = 9.7281 + 32.7870 = $42.52
```
The terminal value is **77.1%** of the total — healthy for a 5-year explicit period. If it exceeded ~90%, the explicit horizon would be too short (the bundled `validate_ddm.py` flags this). Compare `$42.52` to the current share price and reconcile against the DCF and comps ranges before drawing any conclusion — and remember every output is staged for human review, not a recommendation.
