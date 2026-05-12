---
description: Calculate fund distribution waterfall with step-by-step math and sensitivity table
argument-hint: "[fund name or proceeds amount, e.g. 'Acme Fund II $50M exit proceeds']"
---

# Waterfall

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Calculate the full LP/GP distribution waterfall — return of capital, preferred return, GP catch-up, and carried interest split — with step-by-step math at every tier and a sensitivity table across exit scenarios.

See the **waterfall-calculations** skill for domain knowledge on European vs American waterfall mechanics, carry structures, and clawback provisions.

## Workflow

### 1. Gather Inputs

If FundOS MCP is connected, call `fundos_list_fund_accounts` and `fundos_list_lps` to pull committed capital and LP roster. For the waterfall calculation, also ask:

- **Waterfall type** — European (whole-fund) or American (deal-by-deal)
- **Total distributable proceeds** — gross exit proceeds or net after transaction costs
- **LP committed / contributed capital** — total LP investment basis
- **Management fee offset** — percentage of management fees offset against carried interest (commonly 50-80%)
- **Preferred return rate** — hurdle rate (typically 6-8% per annum for PE; 0% common for VC)
- **Carried interest rate** — GP carry percentage (typically 20%; sometimes 25-30% for top-tier VC)
- **GP catch-up** — full catch-up (GP gets 100% until even) or partial catch-up (e.g. 50/50)
- **Fund inception date** — for preferred return accrual calculation
- **Distribution date** — date proceeds are being distributed
- **Prior distributions** — any prior distributions of capital or preferred return already paid

### 2. Calculate European Waterfall (Step-by-Step)

If FundOS MCP is connected, call `fundos_compute_waterfall`. Otherwise compute manually:

**Step 1 — Return of Capital**
```
LP Capital Contributed:          $XXX,XXX,XXX
GP Capital Contributed (1-2%):   $  X,XXX,XXX
Total Capital to Return:         $XXX,XXX,XXX

Available Proceeds:              $XXX,XXX,XXX
Paid in Step 1 — LP ROC:         $XXX,XXX,XXX
Paid in Step 1 — GP ROC:         $  X,XXX,XXX
Remaining After Step 1:          $XXX,XXX,XXX
```

**Step 2 — Preferred Return (Hurdle)**
```
Preferred Return Rate:           X.X% per annum
Accrual Period:                  X.X years (inception to distribution date)
LP Preferred Return Accrued:     $XXX,XXX,XXX
GP Preferred Return Accrued:     $  X,XXX,XXX

Paid in Step 2 — LP Pref:        $XXX,XXX,XXX
Paid in Step 2 — GP Pref:        $  X,XXX,XXX
Remaining After Step 2:          $XXX,XXX,XXX
```

**Step 3 — GP Catch-Up**
```
GP Catch-Up Target:              GP should receive XX% of (Step 2 pref + this catch-up)
GP Catch-Up Amount:              $  X,XXX,XXX
Paid in Step 3 — GP Catch-Up:    $  X,XXX,XXX
Remaining After Step 3:          $XXX,XXX,XXX
```

**Step 4 — Carried Interest Split**
```
LP Share:                        XX% (e.g. 80%)
GP Share (Carry):                XX% (e.g. 20%)

Paid in Step 4 — LP:             $XXX,XXX,XXX
Paid in Step 4 — GP Carry:       $  X,XXX,XXX
Remaining After Step 4:          $0
```

**Summary**
| Recipient | Amount | % of Total |
|-----------|--------|-----------|
| LP — ROC + Pref + Residual | $XXX,XXX,XXX | XX.X% |
| GP — ROC + Pref + Catch-Up + Carry | $XX,XXX,XXX | XX.X% |
| **Total** | **$XXX,XXX,XXX** | **100%** |

### 3. American Waterfall Note

For deal-by-deal waterfalls, add clawback analysis:
- GP receives carry on winning deals before fund-level losses are known
- Clawback obligation = excess carry received if full portfolio returns don't clear the hurdle
- Compute per-deal carry paid and compare to whole-fund carry entitlement

### 4. Sensitivity Table

Run the waterfall at multiple exit scenarios:

| Exit Proceeds | LP Total | LP MOIC | GP Carry | Total TVPI |
|--------------|---------|---------|---------|-----------|
| $XX,XXX,XXX  | $XX,XXX,XXX | X.Xx | $X,XXX,XXX | X.Xx |
| $XX,XXX,XXX  | $XX,XXX,XXX | X.Xx | $X,XXX,XXX | X.Xx |
| $XX,XXX,XXX  | $XX,XXX,XXX | X.Xx | $X,XXX,XXX | X.Xx |

Also compute: minimum proceeds for LP to break even, minimum for hurdle to be cleared, minimum for GP to receive any carry.

### 5. Output

Return:
1. **Step-by-step waterfall** — full calculation at each tier with running totals
2. **Summary table** — LP vs GP split in dollars and percentages
3. **Sensitivity table** — outcomes across exit scenarios
4. **Key thresholds** — break-even, hurdle clear, carry threshold

## Important Notes

- Always show all math — LP counsel and auditors will verify every number
- Confirm whether preferred return compounds annually or accrues simple — this matters significantly over long hold periods
- Management fee offset reduces GP's carry basis — confirm the offset percentage before computing catch-up
- Clawback provisions vary by LPA — read the waterfall section carefully if results seem unusual
- For multi-currency funds, all amounts should be converted at a consistent FX rate with the rate noted
