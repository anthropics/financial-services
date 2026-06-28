---
name: tax-loss-harvesting
description: Identify tax-loss harvesting opportunities across taxable accounts. Finds positions with unrealized losses, suggests replacement securities, and tracks wash sale windows. Triggers on "tax-loss harvesting", "TLH", "harvest losses", "tax losses", "unrealized losses", or "year-end tax planning".
---

# Tax-Loss Harvesting

## Workflow

### Step 1: Identify Candidates

Scan taxable accounts for positions with unrealized losses:

| Security | Asset Class | Cost Basis | Current Value | Unrealized Loss | Holding Period | % Loss |
|----------|-----------|-----------|---------------|-----------------|---------------|--------|
| | | | | | ST / LT | |

**Prioritize by:**
1. Largest absolute loss (biggest tax benefit)
2. Short-term losses first (offset short-term gains taxed at ordinary income rates)
3. Positions with the largest % loss (less likely to recover quickly)

### Step 2: Gain/Loss Budget

Calculate the client's tax situation:

| Category | Amount |
|----------|--------|
| Realized short-term gains YTD | |
| Realized long-term gains YTD | |
| Realized losses YTD | |
| Net gain/(loss) position | |
| Carryforward losses from prior years | |
| **Target harvesting amount** | |

**Tax savings estimate:**
- Short-term losses × marginal ordinary income rate
- Long-term losses × capital gains rate
- Up to $3,000 net loss deduction against ordinary income
- Excess carries forward

### Step 3: Replacement Securities

For each harvest candidate, suggest a replacement that:
- Maintains similar market exposure (same asset class, sector, geography)
- Is NOT "substantially identical" (wash sale rule)
- Has similar risk/return characteristics

| Sell | Replace With | Reason | Tracking Error Risk |
|------|-------------|--------|-------------------|
| SPDR S&P 500 (SPY) | iShares Core S&P 500 (IVV) | Same index, different fund family | Minimal |
| Vanguard Total Intl (VXUS) | iShares MSCI ACWI ex-US (ACWX) | Similar exposure, different index | Low |
| Individual stock ABC | Sector ETF (XLK) | Broader exposure, no wash sale risk | Moderate |

### Step 4: Wash Sale Check

Before executing, verify no wash sales:

- Check ALL accounts in the household (taxable, IRA, Roth, spouse accounts)
- 30-day lookback: Did we buy substantially identical securities in the last 30 days?
- 30-day forward: Block repurchase of the same security for 30 days
- Check for dividend reinvestment plans (DRIPs) that could trigger wash sales
- Document the wash sale window for each trade

| Security Sold | Wash Sale Window Start | Window End | DRIP Active? | Risk |
|--------------|----------------------|-----------|-------------|------|
| | | | | |

### Step 5: Execution Plan

| Trade # | Account | Action | Security | Shares | Est. Proceeds | Est. Loss | Replacement | Notes |
|---------|---------|--------|----------|--------|--------------|-----------|-------------|-------|
| | | Sell | | | | | | |
| | | Buy | | | | | | |

**Summary:**
- Total estimated losses harvested: $
- Estimated tax savings: $ (at marginal rate of %)
- Net portfolio impact: minimal (replacement securities maintain exposure)
- Wash sale window management: [dates]

### Step 6: Post-Harvest Tracking

After 30+ days, optionally:
- Swap back to original securities (if preferred)
- Maintain replacement securities (if no reason to switch back)
- Update cost basis records
- Document for tax reporting

### Step 7: Output

- Harvest opportunity list (Excel)
- Trade execution sheet
- Wash sale tracking calendar
- Tax savings estimate summary
- Replacement security rationale

## Important Notes

- Wash sale rules are strict — violations disallow the loss AND adjust cost basis
- Substantially identical means same security, not same asset class — ETFs tracking different indexes are generally fine
- Always coordinate across all household accounts including retirement accounts
- Consider the long-term cost basis step-down — harvesting resets cost basis, which means more gains later
- Year-end is prime harvesting season but opportunities exist throughout the year
- Mutual fund capital gains distributions in December can create additional harvesting urgency
- Document everything for tax reporting and compliance
- Not all losses are worth harvesting — transaction costs and tracking error have real costs
