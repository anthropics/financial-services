---
name: investor-profile
description: Build or update an individual investor's profile and a written investment policy (goals, horizon, risk capacity and tolerance, liquidity needs, tax situation, target allocation, and personal rules). Use before any portfolio review, sizing, or rebalancing work when no profile exists, or when the investor's circumstances change. Triggers on "set up my investor profile", "what should my allocation be", "write my investment policy", "IPS", "my risk tolerance", "我的投资目标", "风险偏好".
---

# Investor Profile & Investment Policy

The profile is the yardstick for every other skill in this plugin. A portfolio is only "too risky" or "on track" relative to what it is supposed to do.

## Step 1: Gather facts (ask; never assume)

Ask in one short batch, then follow up only on gaps:

| Area | Questions |
|---|---|
| Goals | What is the money for (retirement, home, education, income, general wealth)? Target amount and date for each goal? |
| Horizon | When will you first need to withdraw a meaningful amount? |
| Liquidity | Emergency fund in place (months of expenses)? Known large outflows in the next 3 years? |
| Income & stability | Is income stable? Any concentrated exposure through your employer (RSUs, options, pension)? |
| Accounts | Which account types (taxable, tax-advantaged such as 401(k)/IRA/ISA/pension, A-share / HK / US brokerage)? Which market and currency? |
| Tax | Country of tax residence; marginal rate; any carried-forward losses? |
| Experience | Years investing; instruments used (funds, stocks, options, margin)? |
| Behaviour | Largest drawdown lived through and what you did; the loss (in % and in cash) that would make you sell. |
| Constraints | Ethical or sector exclusions; instruments you won't use; max time you want to spend. |

## Step 2: Separate capacity from tolerance

- **Risk capacity** (objective): horizon, income stability, emergency fund, size of portfolio relative to needs. Score Low / Medium / High.
- **Risk tolerance** (behavioural): drawdown history and stated sell point. Score Low / Medium / High.
- **Use the lower of the two.** If they differ by two levels, say so explicitly; it is the most common source of bad outcomes.

Rough drawdown map for a diversified equity/bond mix (historical, illustrative, not a forecast):

| Equity share | Plausible peak-to-trough in a severe bear market |
|---|---|
| 30% | -10% to -15% |
| 50% | -20% to -25% |
| 70% | -30% to -35% |
| 90-100% | -45% to -55% |

Pick the equity share whose drawdown the investor said they could hold through.

## Step 3: Draft the policy

Produce a one-page Investment Policy Statement:

1. **Objectives**: each goal with amount, date, and priority.
2. **Risk profile**: capacity, tolerance, the binding one, and the max drawdown the plan is built to survive.
3. **Target allocation**: asset classes with target % and a rebalancing band (default ±5 percentage points absolute, or ±25% relative for sleeves under 20%).
4. **Position rules**: max single stock (default 5-10% of portfolio), max single sector (default 25%), max speculative sleeve (default 5-10%), max single fund issuer if relevant.
5. **Liquidity**: emergency fund held outside the portfolio; cash sleeve for known outflows.
6. **Tax placement**: which assets belong in which account type.
7. **Review cadence**: quarterly check, annual full review, and life events that trigger an off-cycle review.
8. **Personal rules**: e.g. "no margin", "no single buy larger than X", "24-hour wait before any unplanned trade".

## Step 4: Save it

Write the profile as `investor-profile.md` (or update the existing file) in a structured form other skills can read. Put a dated change log at the bottom.

## Notes

- Match the investor's language (answer in Chinese if they write in Chinese).
- Market conventions differ. For A-shares note T+1 settlement, 100-share board lots, daily price limits, and stamp duty on sells. For HK, note board lots vary by stock.
- This is a planning aid, not personalised financial advice. Recommend a licensed adviser for complex tax, estate, or retirement-income decisions.
