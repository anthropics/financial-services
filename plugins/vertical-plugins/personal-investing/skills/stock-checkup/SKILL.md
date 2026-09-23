---
name: stock-checkup
description: Quick, structured due-diligence checkup on a single listed stock for an individual investor. Covers business, financial quality, balance-sheet risk, valuation vs history and peers, red flags, and what would have to be true for the investment to work. Triggers on "check this stock", "should I look at [ticker]", "is [company] overvalued", "stock checkup", "quick DD on", "帮我看看这只股票", "个股分析".
---

# Stock Checkup

A one-to-two-page checkup, not a full initiation. The goal is for the investor to understand what they would own and what could go wrong.

## Step 1: Identify

Get the ticker, exchange, and currency. Resolve share classes and dual listings (e.g. A/H shares, ADRs), note any price gap between them, and say which listing the analysis uses.

## Step 2: Business in plain words

- What it sells, to whom, and how it makes money (segment revenue mix).
- Where it competes and the basis of competition. Is there a durable advantage (scale, network, switching cost, brand, licence, cost)?
- Key dependencies: customers, suppliers, regulators, commodity inputs, a single product.

## Step 3: Financial quality (5-10 years where available)

| Metric | Look for |
|---|---|
| Revenue growth | Consistency; organic vs acquired |
| Gross and operating margin | Level and trend vs peers |
| ROIC or ROE | Above cost of capital through the cycle? |
| Free cash flow vs net income | FCF conversion persistently below 70% is a flag |
| Share count | Dilution from issuance or stock comp vs buybacks |
| Dividends | Payout ratio; covered by FCF? |

## Step 4: Balance-sheet and governance risk

- Net debt / EBITDA, interest coverage, and the maturity wall in the next 24 months.
- Receivables or inventory growing faster than revenue.
- Related-party transactions, pledged shares by controlling holders (common in A-shares), auditor changes, qualified opinions, restatements.
- Goodwill as a share of equity; history of impairments.
- Controlling shareholder or state ownership, and minority-holder protections.

## Step 5: Valuation

- Current P/E, EV/EBITDA, P/FCF, P/B (for financials), and dividend yield.
- Each metric vs the stock's own 5-10 year range (percentile) and vs 3-6 peers. Use `comps-analysis` for the peer spread.
- Reverse-engineer the price: what revenue growth and margin does today's price imply? Is that plausible given Step 3?
- Give a range, not a point target.

## Step 6: Bull, bear, and what must be true

- **Bull case**: 3 bullets, each tied to evidence.
- **Bear case**: 3 bullets, each tied to evidence. Argue it as hard as the bull case.
- **What must be true**: the 2-3 assumptions the investment depends on, and the data point that would show each one is wrong.
- **Upcoming catalysts**: earnings date, product or regulatory events.

## Step 7: Fit with this investor

If `investor-profile.md` exists, note how a position would affect sector, region, and single-stock limits. For sizing, hand off to `position-sizing`. If the investor goes ahead, offer to open a thesis with `thesis-tracker`.

## Rules

- Cite a source and date for every number. Mark anything unsourced `[UNSOURCED]`.
- Don't issue a buy/sell rating or price target. Summarise as "evidence strongly/moderately/weakly supports the bull case", with the reasons.
- Flag stale data (e.g. last filing more than 6 months old).
