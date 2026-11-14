---
name: position-sizing
description: Size a new or existing position for an individual investor using risk-based sizing, portfolio limits, volatility, liquidity, and market lot rules, and optionally stage entries over time. Triggers on "how much should I buy", "position size for [ticker]", "how many shares", "is this position too big", "size this trade", "仓位", "买多少".
---

# Position Sizing

## Inputs

- Portfolio value (investable, excluding the emergency fund) and cash available.
- Instrument, price, currency, and board lot (A-shares: 100 shares; HK: per-stock lot; US: 1 share, fractional where the broker allows).
- Conviction (Low / Medium / High) and whether the position is core or speculative.
- The exit condition: a price-based stop, or a thesis-based exit (from `thesis-tracker`).
- Limits from `investor-profile.md`: max single stock, max sector, max speculative sleeve.

## Method: compute all three, then use the smallest

1. **Risk budget.** Choose the cash loss you accept if the exit triggers. Default 0.5% of portfolio (low conviction), 1% (medium), 1.5% (high).
   `shares = (portfolio × risk%) ÷ (entry − stop)`
   If there is no price stop, use a volatility stop instead: `stop distance = 2 × ATR(14)`, or `1 × annualised vol × √(holding months / 12) × price`.
2. **Concentration cap.** `max value = portfolio × single-stock limit − existing look-through exposure`. Also check the sector cap after adding the position.
3. **Liquidity cap.** The position should be at most 5% of 20-day average daily value traded, so it can be exited in a day without moving the price.

Round down to the board lot. If the rounded size is zero, say so. Don't round up.

## Optional: Kelly check (a ceiling, never the size)

Only if the investor gives an explicit win probability p and payoff ratio b: `f* = p − (1 − p) / b`. Show f*/4 as an upper bound, and warn that inputs are guesses and full Kelly draws down severely.

## Staging

For medium or low conviction, or high-volatility names, propose 2-3 tranches (e.g. 40/30/30) with price- or time-based triggers. Recompute the risk budget on the blended entry.

## Output

| Constraint | Max shares | Max value | % of portfolio |
|---|---|---|---|
| Risk budget | | | |
| Concentration cap | | | |
| Liquidity cap | | | |
| **Binding (smallest)** | | | |

Then give the cash at risk if the stop hits, the resulting sector and single-name weights, the costs (commission, stamp duty/FX), and any profile rules that would be breached. This is arithmetic to support the investor's own decision. Don't place orders.
