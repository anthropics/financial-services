---
name: waterfall-calculations
description: Distribution waterfall mechanics for private funds — European and American waterfall structures, preferred return accrual, GP catch-up, carried interest calculation, clawback provisions, and sensitivity modeling. Use when modeling fund distributions, computing LP/GP splits, running exit scenarios, or understanding waterfall economics. Triggers on "run the waterfall", "calculate carry", "how much does the GP get", "LP distributions", "preferred return", "carried interest", "GP catch-up", "clawback", or "exit proceeds distribution".
---

# Waterfall Calculations

You are an expert in private fund distribution waterfalls. You understand European and American waterfall structures, preferred return accrual mechanics, GP catch-up provisions, carried interest splits, and clawback obligations. You can calculate exact distributions at each waterfall tier, model sensitivity across exit scenarios, and explain the economics clearly to both GPs and LPs.

## Core Principles

Waterfall calculations are governed by the LPA — the LPA controls, not convention. Read the LPA waterfall section carefully before computing. Key variables that differ across funds: preferred return rate and compounding method, catch-up structure (full or partial), carry basis (net of fees, net of organizational costs), fee offset mechanics, and recycling provisions.

## Available FundOS MCP Tools

- **`fundos_compute_waterfall`** — European waterfall: LP/GP splits via ROC → preferred return → GP catch-up → carried interest. Returns LP/GP totals and tier breakdown.
- **`fundos_list_fund_accounts`** — Fund capital structure and commitments
- **`fundos_list_lps`** — LP roster and contribution history
- **`fundos_run_pricer`** — IRR, MOIC, WAL for individual assets (feeds into waterfall)

## Waterfall Structures

### European (Whole-Fund) Waterfall

The standard for most PE and VC funds. GP receives no carry until ALL LPs have received:
1. Return of all contributed capital
2. Preferred return on all contributed capital

**Tier 1 — Return of Capital**
All LP and GP contributed capital is returned first. GP contributes 1-2% alongside LPs.

**Tier 2 — Preferred Return (Hurdle)**
LPs (and often GP on their co-invest) receive a preferred return (hurdle rate) on their contributed capital, accrued from the date of each contribution to the date of distribution.

```
Preferred Return = Contributed Capital × [(1 + Annual Rate)^(Years) − 1]   [compound]
                 = Contributed Capital × Annual Rate × Years                 [simple]
```

Most PE LPAs use a compound 8% preferred return. Some VC funds use 0% (no hurdle).

**Tier 3 — GP Catch-Up**
After the preferred return is paid, the GP "catches up" so it receives a target % of the combined preferred return + catch-up.

```
Full catch-up: GP gets 100% until GP has received [carry %] of (pref + catch-up)
  GP catch-up = (Carry% × LP Pref) / (1 − Carry%)
  Example at 20% carry: GP catch-up = (20% × LP Pref) / 80% = 25% × LP Pref

Partial catch-up: GP and LP split at a different ratio during catch-up (e.g. 50/50)
  GP catch-up = Carry% / (1 − Partial catch-up%) × LP Pref
```

**Tier 4 — Residual Split (Carried Interest)**
Remaining proceeds split per the carry percentage: typically 80% LP / 20% GP.

### American (Deal-by-Deal) Waterfall

Each investment is evaluated independently. GP receives carry on profitable deals without waiting for the whole portfolio to clear the hurdle.

- **Advantage for GP**: Earlier carry receipts, better GP cash flow
- **Risk for LP**: GP receives carry on winners before knowing outcome of full portfolio
- **Clawback obligation**: If fund-level returns ultimately don't clear hurdle, GP must return excess carry received

American waterfall is more common in older PE funds; modern institutional LPs push for European waterfall.

### VC Waterfall (No Hurdle)

Many VC funds have a 0% preferred return (no hurdle):

1. Return of LP + GP contributed capital
2. 80/20 split of all remaining proceeds (no preferred return tier, no catch-up tier)

Some VC funds add a soft hurdle (preferred return only — no catch-up), where the carry floor just requires clearing a minimum return before carry begins.

## Preferred Return Mechanics

### Simple vs. Compound Accrual

| Method | Formula | Impact |
|--------|---------|--------|
| Simple (uncommon) | P × r × t | Lower hurdle — less LP-friendly |
| Compound (standard PE) | P × (1+r)^t − P | Higher hurdle — more LP-friendly |
| Daily compounding (rare) | P × (1+r/365)^days − P | Slightly higher than annual compound |

For a 10-year fund, the difference between simple and compound 8% is substantial — always confirm which method the LPA uses.

### Contribution Timing

Each LP contribution accrues preferred return from the date it was contributed, not from fund inception. For large funds with multiple closings over 12-18 months, LP contributions have different accrual start dates. This requires a contribution-date-level waterfall, not a single blended rate.

## Carry Basis and Fee Offsets

Most LPAs require management fees to offset against the GP's carried interest basis:

```
Carry Basis = Proceeds Available for Carry
            − Management Fees Paid × Offset% (typically 50-80%)
            − Organizational Costs × Offset%
```

A higher fee offset reduces the GP's carry basis (reducing carry owed), which effectively shifts economics to LPs.

## Clawback Provisions

In American waterfalls, clawback ensures GPs don't keep carry from winning deals if the fund doesn't clear hurdle overall:

```
Clawback = Total Carry Received − Fund-Level Carry Entitlement

Fund-Level Carry Entitlement = 0 if Total Fund Returns < Preferred Return Threshold
                              = Carry% × (Total Distributions − Total Contributions − Total Pref)
                                if Total Fund Returns > Preferred Return Threshold
```

GP clawback obligations are typically secured by escrow (10-15% of carry held in escrow), personal guarantees, or both.

## Sensitivity Analysis Reference

| Total Proceeds as % of LP Capital | DPI | GP Carry | LP Net Return |
|-----------------------------------|-----|---------|--------------|
| <100% | <1.0x | 0 | Loss |
| 100-108% (at 8% pref) | ~1.0x | 0 | Just above breakeven |
| 125% | 1.25x | ~0 | Hurdle barely cleared |
| 150% | 1.50x | Meaningful | Solid |
| 200% | 2.00x | Substantial | Strong |
| 300% | 3.00x | Large | Excellent |

Compute exact thresholds: the "no-carry point" is exactly where proceeds equal LP ROC + LP preferred return. The GP catch-up tier drives a disproportionate percentage of proceeds to GP at just above this threshold.

## Output Standards

Always show:
1. Full tier-by-tier calculation with amounts, formulas, and running totals
2. LP total (ROC + preferred return + residual) and GP total (ROC + catch-up + carry)
3. LP net MOIC and GP net MOIC
4. Clear statement of assumptions (carry rate, hurdle rate, compounding method, fee offset %)
5. Sensitivity table across exit scenarios
6. Minimum proceeds needed for: LP breakeven, hurdle clear, GP to receive any carry
