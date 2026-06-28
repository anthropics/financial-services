# Equity Research Tear Sheet

## Purpose
A dense snapshot for buy-side or sell-side analysts evaluating an investment. Emphasis on valuation, forward estimates, financial trajectory, and analyst consensus. Everything supports or challenges an investment thesis.

**Default page length:** 1 page. Equity research tear sheets are conventionally single-page — density is the point. If the user requests more space, extend to 2 pages.

## Query Plan

Start with these queries. If results are incomplete, break into narrower follow-ups.

**Query 1 — Profile + market data:**
"[Company] company overview sector industry market capitalization enterprise value stock price 52-week high low shares outstanding beta"
→ Header, Business Description
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`

**Query 2 — Historical financials:**
"[Company] annual income statement revenue gross profit EBITDA net income EPS free cash flow total debt cash and equivalents last 4 fiscal years"
→ Financial Summary (pull 4 years; display 3; use the earliest year only for YoY growth computation)
→ **Immediately write** raw values to `/tmp/tear-sheet/financials.csv`

**Query 2b — Segments (if available):**
"[Company] revenue by segment business unit last 2 fiscal years"
→ Revenue & Segment Breakdown (need 2 years for YoY growth). If segment data is unavailable, skip this section — do not leave a blank table.
→ **Immediately write** to `/tmp/tear-sheet/segments.csv` (skip if no segment data returned)

**Query 3 — Valuation + consensus:**
"[Company] P/E EV/EBITDA EV/Revenue valuation multiples consensus revenue EPS estimates analyst recommendations price target"
→ Valuation Snapshot, Consensus Estimates
→ **Immediately write** multiples to `/tmp/tear-sheet/valuation.csv`
→ **Immediately write** estimates to `/tmp/tear-sheet/consensus.csv`

**Query 4 — Earnings:**
"[Company] most recent earnings call key takeaways guidance"
→ Earnings Highlights
→ **Immediately write** to `/tmp/tear-sheet/earnings.txt`

**Query 5 — Stock performance:**
"[Company] stock price return 1 month 3 month 6 month 1 year YTD performance"
→ Stock Performance (no intermediate file — data goes directly into document)

**Query 6 (if user provided comps):**
"[Comp company] market cap EV/Revenue EV/EBITDA revenue growth" — repeat for each comp
→ Peer context for Valuation Snapshot
→ **Immediately write** to `/tmp/tear-sheet/peer-comps.csv`

## Sections

Listed in priority order. If constrained to one page, cut from the bottom.

### 1. Company Header
Compact key-value block rendered as a two-column borderless table per the global style config.

Left column: Ticker (exchange), sector / industry, HQ
Right column: Stock price, 52-week range, market cap, EV, shares outstanding, beta

### 2. Business Description
2-3 tight sentences. **Rewrite in your own words for an analyst audience** — do not paste the CIQ company summary verbatim. The CIQ summary is an input; the output should be concise and thesis-oriented.

For well-known, widely covered companies, assume the analyst already knows the basic business. Lead with what's *changing* — strategic pivots, portfolio reshaping, new growth vectors — not a Wikipedia-style overview. For example, for a Fortune 500 company, don't spend a sentence on "provides financial data to institutions." Instead: "Reshaping its portfolio toward higher-margin data and analytics businesses, with a pending Mobility spin-off and aggressive AI investment through its Kensho subsidiary."

For lesser-known companies, a brief "what they do" sentence is appropriate before pivoting to the thesis-relevant dynamics.

### 3. Valuation Snapshot
Centerpiece of the equity tear sheet.

| Metric | Trailing | Forward (NTM) |
|---|---|---|
| P/E | | |
| EV/EBITDA | | |
| EV/Revenue | | |
| P/FCF | | |
| Dividend Yield | | |

**Forward multiples are mandatory when available from the tools.** Showing only trailing multiples when forward data exists is a significant gap — analysts value companies on forward earnings. If forward multiples aren't available, show trailing only and note "Fwd estimates N/A."

If the user provided comparable companies, add columns for each comp (or a "Peer Median" column if 3+ comps). If no user comps, and the tools return peer data, include a Peer Median column. If neither, show the company's multiples only.

### 4. Consensus Estimates
What the Street expects — a key differentiator for this tear sheet type.

**Data availability note:** The depth of consensus data varies by company and coverage. Include whatever the tools return — analyst count, price target, Buy/Hold/Sell distribution — but do not fabricate or estimate any consensus figure. For thinly covered companies, this section may contain only revenue and EPS estimates, which is still valuable.

| Metric | FY[year] Est. | FY[year+1] Est. |
|---|---|---|
| Revenue | | |
| EPS (normalized) | | |
| EBITDA | | |

Use normalized/adjusted EPS where available — GAAP EPS can be distorted by one-time items and is less useful for forward estimates.

Below the main estimates table, include a compact analyst consensus block (if data is available from the tools):

| Analyst Consensus | |
|---|---|
| Mean Price Target | $XXX |
| # of Estimates | XX |
| Buy / Hold / Sell | XX / XX / XX |

If price target or recommendation data is unavailable, omit the analyst consensus block rather than showing empty rows. Do not fabricate these figures.

If consensus data isn't available at all, skip this entire section and note "Consensus estimates not available." Do not estimate.

### 5. Financial Summary (3-Year)
Dense single table using actual fiscal year labels.

| Metric ($M) | FY20XX | FY20XX | FY20XX |
|---|---|---|---|
| Revenue | | | |
| Revenue Growth % | | | |
| Gross Margin % | | | |
| EBITDA | | | |
| EBITDA Margin % | | | |
| Net Income | | | |
| EPS (Diluted) | | | |
| Free Cash Flow | | | |
| Net Debt | | | |

Compute derived metrics (growth %, margins) from raw data rather than querying separately.

**Capital Structure (separate compact sub-table below the Financial Summary):**
Do NOT append these rows to the 3-year Financial Summary table — blank cells in prior-year columns look like missing data. Instead, render as a separate 2-column sub-table (Metric | Value) directly below, showing only the most recent fiscal year:

| Metric | FY[latest] |
|---|---|
| Total Debt | $XXM |
| Cash & Equivalents | $XXM |
| Net Debt | $XXM |

This matches the capital structure format used in Corp Dev and IB/M&A tear sheets. Keep it tight — no extra spacing between the Financial Summary and this sub-table.

### 6. Revenue & Segment Breakdown
If segment data is available from the tools, include a compact segment revenue table. This is essential context for equity research — analysts need to see which business lines are driving growth.

| Segment | Revenue ($M) | % of Total | YoY Growth |
|---|---|---|---|
| [Segment A] | | | |
| [Segment B] | | | |

Keep this compact for the one-pager: table only, no qualitative paragraph. If segment data is unavailable, skip this section entirely — do not include a blank or placeholder table.

### 7. Recent Earnings Highlights
Include the quarter and date (e.g., "Q3 FY2025 — October 2025"). 3-4 bullets with an **investment lens** — this audience wants segment-level specifics, not strategic themes:

**Lead with guidance if provided.** If management issued forward guidance, make it the first bullet with a bold **Guidance:** prefix (e.g., "**Guidance:** FY2026 EPS of $19.40–$19.65, implying 9–10% growth; organic revenue growth of 6–8%."). Guidance is the single most actionable forward-looking data point for an analyst — do not bury it among operating highlights.

**Beat/miss context (data permitting):** If consensus estimate data is available for the reported period, frame the headline result bullet as a beat/miss: "Revenue of $X beat/missed consensus of $Y by Z%." If consensus data for the reported period is not available from the tools, describe results in absolute terms and growth rates only — do not fabricate consensus figures.

Then:
- Segment-level performance: which business lines accelerated or decelerated
- Margin trajectory: any commentary on cost structure or profitability trends

Attribute to management: "Management highlighted…" or "CFO noted…" rather than declarative claims. This section should feel like an earnings recap, not a press release summary.

### 8. Key Operating Metrics
2-3 sector-relevant KPIs if available from the data (subscriber count, same-store sales, NIM, etc.). If nothing sector-specific, compute ROE and ROIC from the financials already retrieved. Optional — drop if space is tight.

### 9. Stock Performance (cut first)
Period return table. Low analytical value for this audience — cut this before anything else.

| Period | Return |
|---|---|
| 1 Month | |
| 3 Month | |
| YTD | |
| 1 Year | |

## Formatting Notes
- **This is the densest tear sheet type.** It should feel noticeably more compressed than the other templates.
- Financial Summary table: 8pt text (size: 16), row height 240 DXA. Tightest spacing of any template.
- Valuation Snapshot and Consensus Estimates: 8.5pt text, occupy the visual center — analysts scan these first.
- Body text: 8.5pt (size: 17) — smaller than the global 9pt default. Every half-point matters on a one-pager.
- Section spacing: minimize. 6pt before section headers (not the global 12pt), 2pt after rules.
- Bold any metric showing a notable inflection (growth turning positive, margin expansion/compression).
- Prioritize information over whitespace at every turn.
