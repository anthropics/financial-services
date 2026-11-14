---
name: rebalance-plan
description: Draft a tax- and cost-aware rebalancing plan that brings an individual investor's portfolio back within target allocation bands. Uses new cash flows first, then tax-advantaged accounts, then lowest-cost taxable lots, and outputs a staged trade list for the investor to review. Triggers on "rebalance my portfolio", "bring me back to target", "what should I sell to rebalance", "I have new cash to invest", "再平衡", "调仓".
---

# Rebalance Plan

## Step 1: Measure drift

Start from the normalised holdings in `portfolio-review` and the targets and bands in `investor-profile.md`. For each sleeve, show current %, target %, band, and the drift in percentage points and in cash.

**Only act on sleeves outside their band.** If everything is inside, say "No rebalance needed", show how close each sleeve is to its band edge, and stop.

## Step 2: Choose the least costly route, in this order

1. **New contributions, dividends and interest**: direct them to underweight sleeves.
2. **Planned withdrawals**: take them from overweight sleeves.
3. **Tax-advantaged accounts**: trade inside them first, since rebalancing there doesn't realise gains.
4. **Taxable accounts**, only if still needed:
   - Sell lots with losses first (harvest them). Watch wash-sale or equivalent rules and suggest a non-identical replacement to keep the exposure.
   - Then lots with the highest cost basis (smallest gain).
   - Prefer long-term over short-term gains where the tax rate differs.
   - Rebalance only to the band edge, not all the way to target, unless costs are negligible.

Market specifics: A-share sells carry stamp duty and are T+1. HK trades carry stamp duty on both sides. Include FX conversion cost for cross-currency moves.

## Step 3: Build the trade list

| Account | Action | Ticker | Qty (lot-rounded) | Est. value | Lot / cost basis | Est. realised gain/loss | Est. tax | Est. costs |
|---|---|---|---|---|---|---|---|---|

Then show the before/after allocation table and totals: turnover, realised gains, estimated tax, and total costs.

## Step 4: Sanity checks

- The post-trade allocation is within bands and no single-stock or sector limit is breached.
- There is no round-trip (buying and selling the same exposure across accounts).
- Cash in each account doesn't go negative, including settlement timing.
- Total costs are small relative to the drift being fixed. If costs exceed about 0.25% of portfolio value, flag it and offer a cheaper partial plan.

## Output

The trade list is **staged for the investor's review**. State assumptions: prices as of a date, the tax rates used, and lot data completeness. Recommend confirming tax treatment with a tax professional. Never submit orders.
