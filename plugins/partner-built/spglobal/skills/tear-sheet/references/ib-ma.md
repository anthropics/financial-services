# Investment Banking / M&A Tear Sheet

## Purpose
A company profile for transaction context — potential target, acquirer, or pitchbook inclusion. Emphasis on strategic positioning, segment detail, business relationships, and M&A activity. Valuation framed in transaction multiples, not investment thesis.

**Default page length:** 1-2 pages. IB company profiles routinely spill to a second page, especially when segment and M&A data is rich.

## Query Plan

Start with these queries. Break apart and follow up if results are incomplete.

**Query 1 — Profile + identification:**
"[Company] business description headquarters founded employees sector industry ownership structure major shareholders"
→ Header, Business Overview
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`

**Query 2 — Segments + financials:**
"[Company] revenue by segment business unit last 2 fiscal years AND annual income statement revenue gross profit EBITDA operating income net income capex free cash flow total debt cash and equivalents last 4 fiscal years"
→ Segment Breakdown (need 2 years to compute YoY growth), Financial Summary (pull 4 years; display 3; use the earliest year only for YoY growth computation)
→ **Immediately write** raw financials to `/tmp/tear-sheet/financials.csv`
→ **Immediately write** segment data to `/tmp/tear-sheet/segments.csv` (skip if no segment data returned)

**Query 3 — Valuation + comps:**
If the user provided specific comparable companies, query each:
"[Comp company] enterprise value EV/Revenue EV/EBITDA revenue growth EBITDA margin"
Otherwise:
Use the competitors tool to identify 3-5 public peers, then pull EV/Revenue (NTM), EV/EBITDA (NTM), revenue growth %, and EBITDA margin % for each.
Also: "[Company] enterprise value market capitalization EV/Revenue EV/EBITDA valuation multiples"
→ Header (EV/market cap), Trading Comps
→ **Immediately write** company multiples to `/tmp/tear-sheet/valuation.csv`
→ **Immediately write** peer data to `/tmp/tear-sheet/peer-comps.csv`

**Query 4 — M&A activity:**
"[Company] acquisitions divestitures completed transactions last 5 years deal value"
→ Company's own deals
→ **Immediately write** to `/tmp/tear-sheet/ma-activity.csv`

**Query 5 — Comparable transactions (data permitting):**
Use the specific industry from Query 1 results (e.g., "cloud observability software M&A transactions" not "technology M&A"). If the user specified comps, also try: "[comp company] acquisition deal multiples."
→ Comparable Transactions
→ **Append** comparable transactions to `/tmp/tear-sheet/ma-activity.csv` (add `type=precedent` to distinguish from company's own deals)

**Query 6 — Relationships + ownership:**
"[Company] key customers suppliers partners business relationships institutional ownership insider ownership"
→ Business Relationships, Ownership (data permitting)
→ **Immediately write** to `/tmp/tear-sheet/relationships.txt`

## Sections

Listed in priority order. See "Page Budget & Cut Order" below for explicit cut guidance.

### 1. Company Header
Key-value block with transaction-relevant identifiers.

| Field | Notes |
|---|---|
| Company name | Large, bold |
| Ticker & Exchange | If public; omit for private |
| HQ Location | City, State/Country |
| Founded | Year |
| Employees | Approximate headcount |
| Market Cap / Valuation | Market cap if public; latest known valuation if private |
| Enterprise Value | |
| Ownership | Public / PE-backed (name sponsor) / Family / Other |

For private companies: note "Private Company" prominently; skip ticker, exchange.

### 2. Business Overview
**This is a pitchbook paragraph, not a CIQ summary.** Do not paste the company description from the data tools. Rewrite in 4-6 sentences using pitchbook prose:
- Characterize the revenue model (recurring vs. transactional, subscription vs. license)
- Name the customer base at scale ("serves 80% of Fortune 500 banks")
- Identify competitive moats by name ("proprietary dataset of X", "only provider with Y")
- Frame growth vectors that would matter to a buyer or seller

The tone should be confident and specific. A banker reading this paragraph should immediately understand the company's strategic positioning.

### 3. Revenue & Segment Breakdown
Revenue by business unit or product line.

| Segment | Revenue ($M) | % of Total | YoY Growth |
|---|---|---|---|
| [Segment A] | | | |
| [Segment B] | | | |
| **Total** | | **100%** | |

**If segment data isn't available:** Replace the table with 2-3 sentences describing the revenue mix qualitatively (e.g., "Revenue is primarily derived from subscription licenses (~70%) and professional services (~30%)."). A blank table looks broken — a qualitative description still conveys useful information.

### 4. Financial Summary (3-Year + LTM)
Actual fiscal years as column headers. **If LTM (last twelve months) data is available, add an LTM column to the right of the most recent fiscal year.** Label it "LTM [quarter end date]" (e.g., "LTM Q3 2025"). Bankers work off LTM for valuation cross-checks — a fiscal-year-only view can be 6+ months stale.

| Metric ($M) | FY20XX | FY20XX | FY20XX | LTM [date] |
|---|---|---|---|---|
| Revenue | | | | |
| Revenue Growth % | | | | |
| Gross Profit | | | | |
| Gross Margin % | | | | |
| EBITDA | | | | |
| EBITDA Margin % | | | | |
| Operating Income | | | | |
| Net Income | | | | |
| Capex | | | | |
| Free Cash Flow | | | | |
| FCF Margin % | | | | |

In M&A context, margins and FCF conversion matter as much as absolute scale — a buyer is evaluating efficiency and cash generation potential.

**Capital Structure** (compact sub-table below the financial summary):

| Metric | Value |
|---|---|
| Total Debt | $XXM |
| Cash & Equivalents | $XXM |
| Net Debt | $XXM |
| Net Debt / EBITDA | X.Xx |
| S&P Credit Rating | XX (if available) |

Pull from the balance sheet data already retrieved. This is standard in any banker's company profile — total debt, leverage ratio, and credit rating tell a buyer what the financing picture looks like. If credit rating is unavailable, omit that row.

### 5. Trading Comps
Company multiples **and operating metrics** — bankers use these together, not multiples in isolation.

**Forward multiples are mandatory when available.** The table must include NTM multiples if the tools return them. Showing only trailing multiples when forward data exists is a significant gap — bankers price deals on forward earnings.

**Peer columns are expected.** If the user provided comps, each gets its own column. If not, use the competitors tool to identify 3-5 public peers, pull their multiples and operating metrics, and include them. A company-only trading comps table without peer context is incomplete for any banking use case.

| Metric | [Company] | [Comp 1] | [Comp 2] | [Comp 3] | Peer Median |
|---|---|---|---|---|---|
| EV/Revenue (NTM) | | | | | |
| EV/EBITDA (NTM) | | | | | |
| Revenue Growth % | | | | | |
| EBITDA Margin % | | | | | |

If only the company's own multiples are available after attempting peer queries, show those and list selected peer names below the table.

For private companies, skip this section.

### 6. M&A Activity
Two parts. **Deal values are expected in this section** — bankers notice when they're missing.

**Hard rule: If the M&A tools return a transaction value, it must appear in the output.** Never downgrade a known deal value to "Undisclosed" — this is a data integrity violation. Use "Undisclosed" only when the tools genuinely return no value for a transaction.

**a) Company's Own Transactions:**

**The table must include a dedicated Deal Value column.** Do not merge deal values into a Notes or Rationale column — bankers scan for numbers, and a dedicated column enables that.

| Date | Target / Divested | Deal Value ($M) | Type | Rationale |
|---|---|---|---|---|
| | | | Acquisition / Divestiture | |

If none found: "No disclosed transactions in the last 5 years."

**b) Comparable Sector Transactions (data permitting):**
Use the specific industry identified earlier (e.g., "cloud infrastructure software M&A" not "technology M&A"). If the user specified comps, also look for transactions involving those specific companies.

| Date | Target | Acquirer | EV ($M) | EV/Rev | EV/EBITDA |
|---|---|---|---|---|---|

If not available from the tools: "Comparable transaction data not available from data source." Do not fabricate precedent multiples.

### 7. Key Business Relationships
Leverages S&P Capital IQ relationship data. Group by type:

**Customers:** Top 3-5 named clients
**Suppliers:** Key vendors and technology providers
**Partners:** Strategic alliances, distribution, JVs
**Competitors:** Key competitive names

For each entry, include the relationship type and a parenthetical descriptor explaining the nature of the relationship (e.g., "AWS — cloud infrastructure (primary hosting provider)", "JPMorgan — customer (enterprise analytics platform)"). A name alone without context isn't useful. Give this section breathing room — it's strategically valuable and most competing tear sheets lack it.

### 8. Ownership Snapshot (data permitting — omit if tools return nothing)
If the tools return institutional ownership, insider ownership percentage, or top holders, include a compact block:

Top institutional holders (if available): list top 3-5 by ownership %.
Insider ownership: aggregate percentage.

For PE-backed companies, name the sponsor, acquisition year, and ownership stake. Ownership structure directly affects deal complexity — a widely held public company, a founder-controlled company, and a PE-backed company each require fundamentally different deal approaches.

If ownership data is not returned by the tools, omit this section entirely rather than showing placeholders.

**Do not include a Management Team table.** No S&P Global tool returns executive data — see Data Integrity Rule 10. Management names from training data will be stale.

## Page Budget & Cut Order

**Target: 2 pages maximum.** IB profiles can use both pages fully, but must not spill to a third. If content exceeds 2 pages, cut in this order (cut each completely before moving to the next):

1. Ownership Snapshot (section 8) — omit entirely
2. Comparable Sector Transactions (section 6b) — keep company's own M&A, cut precedents
3. Business Relationships (section 7) — compress to top 3 competitors + top 2 each of suppliers/partners/customers, drop descriptors to parenthetical only
4. Capital Structure (section 4) — merge Net Debt/EBITDA into Financial Summary as a single row
5. Trading Comparables (section 5) — reduce to 3 peers

Never cut: Business Overview (2), Revenue & Segment Breakdown (3), Financial Summary (4 core), M&A Activity company transactions (6a).

## Formatting Notes
- Business Overview and Segment Breakdown get the most visual weight.
- **M&A Activity is the signature section:** Use Accent color (#2E75B6) fill with white bold text for M&A table headers — this is the only table that uses a different header color from the standard #D6E4F0. It should catch the eye on a scan.
- **Business Relationships: give breathing room when space permits.** 6pt between each relationship group, full descriptors on each entry. But if hitting page 3, compress per the cut order above — this section is high-value but also the most compressible.
- For private companies, the header, business overview, financials, and relationships form the core; other sections may be sparse.
- **Two-page discipline:** Before rendering, mentally estimate page count. If Business Relationships + M&A Activity together will exceed one full page, start cutting per the cut order.
