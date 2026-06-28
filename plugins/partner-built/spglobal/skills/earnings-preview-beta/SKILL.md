---
name: earnings-preview-single
description: Generate a concise 4-5 page equity research earnings preview for a single company. Analyzes the most recent earnings transcript, competitor landscape, valuation, and recent news to produce a professional HTML report.
---

# Single-Company Earnings Preview

Generate a concise, professional equity research earnings preview for a single company. The output is a self-contained HTML file targeting 4-5 printed pages. The report is dense with figures and data, with tight narrative that gets straight to the point.

**Data Sources (ZERO EXCEPTIONS):** The ONLY permitted data sources are **Kensho Grounding MCP** (`search`) and **S&P Global MCP** (`kfinance`). Absolutely NO other tools, data sources, or web access of any kind. Specifically:
- Do NOT use `WebSearch`, `WebFetch`, `web_search`, `brave_search`, `google_search`, or ANY generic web/internet search tool — even if Kensho is slow, returns no results, or is temporarily unavailable.
- Do NOT use any browser, URL fetch, or web scraping tool.
- If Kensho Grounding returns no results for a query, try rephrasing the query or note "data not available" in the report. **NEVER fall back to web search as an alternative.**
- Every piece of information in the report must be traceable to either a `kfinance` MCP function call or a Kensho `search` call. If it cannot be sourced to one of these two, it must not appear in the report.

**Critical Rule:** You MUST complete ALL research and data collection (Phases 1-5) BEFORE writing any part of the report.

**Intermediate File Rule:** All raw data from MCP tool calls MUST be written to files in `/tmp/earnings-preview/` **immediately after each tool call returns** — before moving to the next call. This protects data from context window compression. Do NOT hold data only in memory. At the start of Phase 1, run `mkdir -p /tmp/earnings-preview` to create the directory. **Before generating the HTML report (Phase 7), you MUST read ALL intermediate files back into context using `cat` commands. The files — not your memory of earlier conversation — are the single source of truth for every number, quote, and source URL in the report. If you skip reading the files, the report WILL contain errors.**

**Fiscal Quarter Rule:** NEVER infer the fiscal quarter from the calendar report date. Many companies have non-standard fiscal years (e.g., Walmart's FY ends Jan 31, so a Feb 2026 report covers Q4 FY2026, not Q4 2025 or Q1 2026). Always use the fiscal quarter and fiscal year exactly as stated in the earnings call name returned by `get_next_earnings_from_identifiers` or `get_earnings_from_identifiers` (e.g., "Walmart Q4 FY2026 Earnings Call" means the quarter is Q4 FY2026). Use that verbatim in the report title, headers, tables, and all references. If the call name is ambiguous, cross-reference with `get_financial_line_item_from_identifiers` period labels.

**Length Rule:** The report must be concise. Target 4-5 pages when printed. Do NOT write long multi-paragraph narratives. Use tight, punchy bullet points. Every sentence must earn its place. If you can say it in fewer words, do so.

**Verbatim Quote Rule:** When quoting management in `<blockquote>` tags, the text MUST be copied **exactly** from the transcript — word for word, including filler words and sentence fragments. Do NOT paraphrase, rearrange, combine sentences from different parts of the transcript, or "clean up" quotes. If you cannot find the exact phrase in the transcript, do NOT present it as a direct quote. Instead, paraphrase in your own narrative voice without blockquote formatting (e.g., "Management noted that data center demand remains significant"). Every blockquote must be a verbatim, copy-paste excerpt that can be verified against the transcript.

**Calculation Integrity Rule:** For any multi-step calculation (implied quarterly figures from annual guidance, LTM P/E, y/y growth rates, segment y/y changes), write out each step explicitly and verify intermediate results before using them in the next step. If you state A + B + C = X, verify X is arithmetically correct before using X in a subsequent formula. If the appendix shows a sum that does not equal its stated components, the report is wrong. When in doubt, recompute from raw data rather than reusing a previously calculated intermediate.

**Ratio Nomenclature Rule:** All valuation ratios must be explicitly labeled as **LTM** (Last Twelve Months) or **NTM** (Next Twelve Months). Never use "trailing" or "forward" — always use LTM or NTM. LTM ratios use the sum of the most recent 4 reported quarters. NTM ratios use the **sum of the next 4 quarterly consensus mean EPS estimates** from `get_consensus_estimates_from_identifiers` — NOT a single annual figure. Both LTM and NTM P/E must be computed and displayed in the competitor comparison table.

**Hyperlink Rule (STRICTLY ENFORCED):** Every claim in the report — numeric AND non-numeric — MUST be wrapped in an `<a href="#ref-N" class="data-ref">` hyperlink pointing to the corresponding entry in the Appendix. **This is not optional. Every single number in the report must be a clickable link.** This includes: revenue figures, EPS, margins, growth rates, market caps, P/E ratios, stock returns, price targets, segment revenue, and any other financial metric. It also includes qualitative claims from transcripts or Kensho searches. If you state it as fact, it must link to a source. Assign each unique claim a sequential reference ID (`ref-1`, `ref-2`, etc.). The hyperlink style is subtle — navy color, no underline, dotted underline on hover. **Do NOT write any number in the report body without wrapping it in an `<a>` tag.** Example: write `<a href="#ref-1" class="data-ref">$152.3B</a>`, NEVER write `$152.3B` as plain text.

---

## Phase 1: Company Profile & Setup

1. Parse the single company ticker from `$ARGUMENTS` (strip whitespace).
2. Run `mkdir -p /tmp/earnings-preview` to create the working directory.
3. Call `get_latest()` to establish current reporting period context.
4. Call `get_info_from_identifiers` — record market cap, industry.
5. Call `get_company_summary_from_identifiers` — record business description.
6. Call `get_next_earnings_from_identifiers` — record upcoming earnings date and fiscal quarter name.

**Immediately write** `/tmp/earnings-preview/company-info.txt`:
```
TICKER: [ticker]
COMPANY: [full name]
INDUSTRY: [industry]
MARKET_CAP: [value] (as of [date])
NEXT_EARNINGS_DATE: [date]
NEXT_EARNINGS_QUARTER: [Q# FY#### exactly as returned by API]
BUSINESS_DESCRIPTION: [2-3 sentence summary]
```

---

## Phase 2: Earnings Transcript Analysis (MANDATORY — COMPLETE BEFORE WRITING)

1. Call `get_latest_earnings_from_identifiers` to get the most recent completed earnings call `key_dev_id`.
2. Call `get_transcript_from_key_dev_id` for that transcript.
3. **Immediately write** `/tmp/earnings-preview/transcript-extracts.txt` with the following sections. Write this file WHILE you still have the transcript in context — do not wait:

```
TRANSCRIPT_SOURCE: [Call Name, e.g., "Q3 2025 Earnings Call"]
KEY_DEV_ID: [key_dev_id]
CALL_DATE: [date]
FISCAL_QUARTER: [Q# FY####]

=== VERBATIM QUOTES (copy-paste exactly — do NOT paraphrase) ===
QUOTE_1: "[exact text from transcript]"
SPEAKER_1: [Name], [Title]
CONTEXT_1: [1 sentence on where this appeared — prepared remarks or Q&A]

QUOTE_2: "[exact text from transcript]"
SPEAKER_2: [Name], [Title]
CONTEXT_2: [context]

QUOTE_3: "[exact text from transcript]"
SPEAKER_3: [Name], [Title]
CONTEXT_3: [context]

QUOTE_4: "[exact text from transcript]"
SPEAKER_4: [Name], [Title]
CONTEXT_4: [context]

=== GUIDANCE (quantitative only) ===
- [metric]: [range or point estimate as stated by management]
- [metric]: [range or point estimate]

=== KEY DRIVERS ===
- [driver 1 with supporting data point]
- [driver 2 with supporting data point]
- [driver 3 with supporting data point]

=== HEADWINDS & RISKS ===
- [risk 1 with quantification if available]
- [risk 2]

=== ANALYST Q&A THEMES ===
- [theme 1: what analysts pushed on]
- [theme 2]
- [theme 3]

=== SYNTHESIS: THEMES TO WATCH NEXT QUARTER ===
- [theme 1]
- [theme 2]
- [theme 3]
```

---

## Phase 3: Competitor Analysis

1. Call `get_competitors_from_identifiers` with `competitor_source="all"`.
2. Select **top 5-7 most relevant public competitors**.
3. For the company AND all selected competitors, gather:
   - `get_prices_from_identifiers` with `periodicity="day"`, last 12 months
   - `get_financial_line_item_from_identifiers` for `diluted_eps`, `period_type="quarterly"`, `num_periods=8`
   - `get_capitalization_from_identifiers` with `capitalization="market_cap"` (latest)
   - `get_consensus_estimates_from_identifiers` with `period_type="quarterly"`, `num_periods_forward=4` — this returns consensus mean EPS estimates for the next 4 quarters, which are summed to compute NTM EPS

**After each tool call returns, immediately append the raw data to the appropriate intermediate file:**

**Write** `/tmp/earnings-preview/prices.csv` — one row per (ticker, date, close). Include the `source` column with the exact MCP function call. Write the subject company's prices first, then each competitor's as you fetch them:
```
ticker,date,close,source
D,2025-02-19,55.67,get_prices_from_identifiers(identifier='D',periodicity='day')
D,2025-02-20,55.82,get_prices_from_identifiers(identifier='D',periodicity='day')
...
DUK,2025-02-19,111.79,get_prices_from_identifiers(identifier='DUK',periodicity='day')
...
```
Note: the `source` value is the same for all rows from a single call — write it on every row so it's always available.

**Write** `/tmp/earnings-preview/peer-eps.csv` — one row per (ticker, period, eps). Write immediately after each `diluted_eps` call:
```
ticker,period,diluted_eps,source
D,Q4 2024,1.09,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
D,Q1 2025,-0.11,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
...
DUK,Q4 2024,1.52,get_financial_line_item_from_identifiers(identifier='DUK',line_item='diluted_eps',period_type='quarterly')
...
```

**Write** `/tmp/earnings-preview/peer-market-caps.csv` — one row per ticker. Write immediately after each `market_cap` call:
```
ticker,market_cap,retrieval_date,source
D,55900000000,2026-02-19,get_capitalization_from_identifiers(identifier='D',capitalization='market_cap')
DUK,98300000000,2026-02-19,get_capitalization_from_identifiers(identifier='DUK',capitalization='market_cap')
...
```

**Write** `/tmp/earnings-preview/consensus-eps.csv` — one row per (ticker, period, consensus mean EPS). Write immediately after each `get_consensus_estimates_from_identifiers` call:
```
ticker,period,consensus_mean_eps,num_estimates,source
D,Q4 2025,0.88,12,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
D,Q1 2026,0.72,10,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
D,Q2 2026,0.91,9,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
D,Q3 2026,1.05,8,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
DUK,Q4 2025,1.48,14,get_consensus_estimates_from_identifiers(identifier='DUK',period_type='quarterly',num_periods_forward=4)
...
```

4. **Do NOT calculate P/E or returns yet.** The raw data is now on disk. Calculations happen in Phase 6 (Verification), reading from these files.

**Date Consistency Rule (stock returns):** When computing comparative stock returns (YTD %, 1-yr %, 30d %, 90d %), ALL tickers MUST use the **exact same start and end dates**. After writing all price data to `prices.csv`, identify the first trading date that appears in ALL tickers' data and use that as the common base date. Do NOT use different base dates for different tickers (e.g., the subject from Feb 19 and peers from Feb 28). If a ticker's data starts later than others, use the first overlapping date for ALL calculations. State the common base date in the appendix for every return calculation.

**P/E Currency Rule (LTM P/E):** When computing LTM P/E for each company, use that company's **most recent 4 reported quarters** from `peer-eps.csv` — not a fixed calendar window applied to all. If a peer has already reported Q4 2025 while the subject company has only reported through Q3 2025, the peer's LTM EPS should include Q4 2025. Check the latest reported period for each company and use the 4 most recent periods per company. Note in the appendix which 4 quarters were used for each P/E calculation.

**Market Cap Date-Stamp:** When reporting market cap, use the `retrieval_date` from `peer-market-caps.csv`. If it differs from the report date, note this in the appendix.

---

## Phase 4: News, Estimates & Sector Intelligence (via Kensho Grounding)

Run these `search` queries for **each** category below. Do NOT skip any.

**CRITICAL — Capture Source URLs:** Every Kensho `search` result includes a **source URL** for the underlying article, report, or data page. You MUST record the URL alongside each finding.

**After EACH search call, immediately append the results to** `/tmp/earnings-preview/kensho-findings.txt` using the format below. Do NOT wait until all searches are done — write after each one:

```
=== SEARCH: "[query used]" ===
DATE_RUN: [today's date]
CATEGORY: [estimates|analyst_ratings|risks|news|sector]

FINDING_1: [key finding or excerpt]
URL_1: [source URL from search result]
SOURCE_1: [publication name, date if available]

FINDING_2: [key finding or excerpt]
URL_2: [source URL]
SOURCE_2: [publication name, date]

[...continue for all relevant results from this search...]
```

**Earnings estimates & analyst sentiment:**
1. `search` for "[TICKER] earnings estimates consensus EPS revenue upcoming quarter"
   - Record: consensus EPS, consensus revenue, estimate revision direction over last 90 days.
   - **Append to kensho-findings.txt immediately.**
2. `search` for "[TICKER] analyst ratings price target upgrades downgrades"
   - Record: recent upgrades/downgrades, price target range, bull/bear thesis summaries.
   - **Append to kensho-findings.txt immediately.**
3. `search` for "[TICKER] risks bear case concerns investors"
   - Record: key debates, bear arguments, swing factors for the upcoming print.
   - **Append to kensho-findings.txt immediately.**

**Recent news (MANDATORY — do not skip):**
4. `search` for "[TICKER] [company name] recent news developments"
   - Record: material news from the last 60 days — M&A, product launches, executive changes, regulatory actions, partnerships, legal developments, tariffs, or any event that could affect the upcoming earnings print or forward guidance.
   - For each item, note the date, headline, potential earnings impact.
   - **Append to kensho-findings.txt immediately.**

**Sector context:**
5. `search` for "[company industry/sector] sector outlook trends"
   - Record: sector-level tailwinds/headwinds, macro data, competitive dynamics.
   - **Append to kensho-findings.txt immediately.**

---

## Phase 5: Financial Data Collection

**Quarterly financials (last 8 quarters):**
`get_financial_line_item_from_identifiers` with `period_type="quarterly"`, `num_periods=8` for:
`revenue`, `gross_profit`, `operating_income`, `ebitda`, `net_income`, `diluted_eps`

**After each line item call returns, immediately append to** `/tmp/earnings-preview/financials.csv`. Write the raw values exactly as returned — do NOT round or convert yet. Include the `source` column with the exact MCP function call and parameters:
```
ticker,period,line_item,value,source
D,Q4 2024,revenue,3941000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q1 2025,revenue,3400000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q2 2025,revenue,4076000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q3 2025,revenue,3810000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q4 2024,diluted_eps,1.09,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
D,Q1 2025,diluted_eps,-0.11,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
...
```

**Do NOT calculate margins or growth rates yet.** Write raw data only. Calculations happen in Phase 6.

**Segment data:**
- `get_segments_from_identifiers` with `segment_type="business"`, `period_type="quarterly"`, `num_periods=8`
- You need 8 quarters (not 4) so you have the year-ago quarter for y/y comparisons. To calculate y/y for Q3 2025, you need Q3 2024 — which is the 5th quarter back. **If the prior-year quarter's segment data is not available in the API response, do NOT estimate or fabricate it. State "y/y not available" in the report.**

**Immediately write** `/tmp/earnings-preview/segments.csv`:
```
ticker,period,segment_name,revenue,source
D,Q3 2024,Dominion Energy Virginia,2762000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2024,Dominion Energy South Carolina,848000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2024,Contracted Energy,260000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2025,Dominion Energy Virginia,3311000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2025,Dominion Energy South Carolina,945000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2025,Contracted Energy,297000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
...
```

**Earnings history (for stock chart annotations):**
- `get_earnings_from_identifiers` — collect past earnings dates within the 12-month price window.
- **Immediately write** `/tmp/earnings-preview/earnings-dates.csv`:
```
ticker,earnings_date,call_name,source
D,2025-05-02,Q1 2025 Earnings Call,get_earnings_from_identifiers(identifier='D')
D,2025-08-01,Q2 2025 Earnings Call,get_earnings_from_identifiers(identifier='D')
D,2025-10-31,Q3 2025 Earnings Call,get_earnings_from_identifiers(identifier='D')
...
```

---

## Phase 6: Verification & Calculations (MANDATORY — DO NOT SKIP)

Before generating the report, read back ALL intermediate files and perform calculations from the clean data. This phase ensures data integrity by working from files rather than compressed conversation context.

1. **Read all intermediate files** using bash `cat` commands:
   - `cat /tmp/earnings-preview/company-info.txt`
   - `cat /tmp/earnings-preview/transcript-extracts.txt`
   - `cat /tmp/earnings-preview/financials.csv`
   - `cat /tmp/earnings-preview/segments.csv`
   - `cat /tmp/earnings-preview/prices.csv`
   - `cat /tmp/earnings-preview/peer-eps.csv`
   - `cat /tmp/earnings-preview/peer-market-caps.csv`
   - `cat /tmp/earnings-preview/consensus-eps.csv`
   - `cat /tmp/earnings-preview/kensho-findings.txt`
   - `cat /tmp/earnings-preview/earnings-dates.csv`

2. **Calculate derived metrics** from the raw data now in context:
   - Gross margin % = gross_profit / revenue (per quarter)
   - Operating margin % = operating_income / revenue (per quarter)
   - Revenue y/y growth % = (current Q revenue - year-ago Q revenue) / year-ago Q revenue
   - EPS y/y growth % = same logic; use "n.m." if base is negative
   - Segment y/y growth % = match segment by name to year-ago Q; if missing, note "y/y not available"
   - LTM P/E per company = latest price / sum of most recent 4 quarterly EPS (check which 4 quarters are available per ticker using `peer-eps.csv`)
   - NTM P/E per company = latest price / NTM EPS, where **NTM EPS = sum of the next 4 quarterly consensus mean EPS estimates** from `consensus-eps.csv`. Add all 4 quarters' consensus_mean_eps values for each ticker. If fewer than 4 forward quarters are available for a peer, mark NTM P/E as "n/a". Note in the appendix which 4 quarters were summed.
   - Stock returns (YTD, 1-yr, 30d, 90d) = find the **common first date across all tickers** in `prices.csv`, then compute returns from that date

3. **Cross-check**:
   - Verify every segment y/y has the actual prior-year row in `segments.csv`. If not, mark "y/y not available."
   - Verify all stock return base dates are identical across tickers.
   - Verify any multi-step calculation by re-summing components (e.g., LTM EPS sum matches the 4 quarterly values).
   - Verify all verbatim quotes in `transcript-extracts.txt` are exact copy-pastes (not paraphrases).

4. **Write** `/tmp/earnings-preview/calculations.csv` with all derived values:
```
ticker,metric,value,formula,components
D,gross_margin_Q3_2025,32.5%,gross_profit/revenue,"gross_profit=1238100000,revenue=3810000000"
D,revenue_yoy_Q3_2025,+9.3%,(Q3_2025-Q3_2024)/Q3_2024,"Q3_2025=3810000000,Q3_2024=3486000000"
D,ltm_pe,24.2x,price/ltm_eps,"price=65.46,ltm_eps=2.70,quarters=Q4_2024+Q1_2025+Q2_2025+Q3_2025"
D,ntm_pe,18.5x,price/ntm_eps,"price=65.46,ntm_eps=3.56,quarters=Q4_2025(0.88)+Q1_2026(0.72)+Q2_2026(0.91)+Q3_2026(1.05),source=get_consensus_estimates_from_identifiers"
D,yoy_return,+17.6%,(end-start)/start,"end=65.46,start=55.67,base_date=2025-02-19"
DUK,yoy_return,+13.0%,(end-start)/start,"end=126.32,start=111.79,base_date=2025-02-19"
...
```

This file becomes the single source of truth for all numbers in the report.

---

## Phase 7: Generate the HTML Report

**STOP — BEFORE WRITING ANY HTML, YOU MUST READ ALL INTERMEDIATE FILES. THIS IS A BLOCKING PREREQUISITE.**

This is not optional. You MUST run each `cat` command below as a **separate bash tool call** (not combined into one). This ensures each file's contents are individually loaded and visible in the conversation. Do NOT combine them into a single command. Do NOT skip any file.

Run these commands **one at a time, each as its own bash call**:

1. `cat /tmp/earnings-preview/company-info.txt`
2. `cat /tmp/earnings-preview/transcript-extracts.txt`
3. `cat /tmp/earnings-preview/financials.csv`
4. `cat /tmp/earnings-preview/segments.csv`
5. `cat /tmp/earnings-preview/prices.csv`
6. `cat /tmp/earnings-preview/peer-eps.csv`
7. `cat /tmp/earnings-preview/peer-market-caps.csv`
8. `cat /tmp/earnings-preview/consensus-eps.csv`
9. `cat /tmp/earnings-preview/kensho-findings.txt`
10. `cat /tmp/earnings-preview/earnings-dates.csv`
11. `cat /tmp/earnings-preview/calculations.csv`

**After reading ALL files, you MUST print a summary message to the user** that lists every file and its status. Use exactly this format:

```
--- DATA FILE VERIFICATION ---
1. company-info.txt        ✓ loaded ([N] lines)
2. transcript-extracts.txt ✓ loaded ([N] lines)
3. financials.csv          ✓ loaded ([N] rows)
4. segments.csv            ✓ loaded ([N] rows)
5. prices.csv              ✓ loaded ([N] rows)
6. peer-eps.csv            ✓ loaded ([N] rows)
7. peer-market-caps.csv    ✓ loaded ([N] rows)
8. consensus-eps.csv       ✓ loaded ([N] rows)
9. kensho-findings.txt     ✓ loaded ([N] lines)
10. earnings-dates.csv     ✓ loaded ([N] rows)
11. calculations.csv       ✓ loaded ([N] rows)

All intermediate data files loaded successfully.
Generating report using file data as the single source of truth.
---
```

If any file is missing or empty, STOP and tell the user which file failed. Do NOT proceed to generate the report with missing data.

**Every number, quote, source URL, and MCP function call reference in the HTML report must come from these files — not from your memory of earlier conversation turns.** The files are the single source of truth. Earlier conversation context may have been compressed or summarized and WILL contain errors if relied upon. If a data point is not in the files, it should not appear in the report.

See [report-template.md](report-template.md) for the complete HTML template, CSS, and Chart.js configuration.

**MANDATORY — Use Template Helper Functions for Charts:**
The report-template.md provides pre-built, debugged Chart.js helper functions. You MUST use these exact functions to create charts. Do NOT write custom inline Chart.js code. The helpers are:
- `createRevEpsChart(canvasId, labels, revenueData, epsData, revLabel)` — for Figure 1
- `createMarginChart(canvasId, labels, grossMargins, opMargins)` — for Figure 2
- `createRevGrowthChart(canvasId, labels, growthData)` — for Figure 3
- `createAnnotatedPriceChart(canvasId, labels, prices, earningsDates, ticker)` — for Figure 5
- `createCompPerfChart(canvasId, labels, datasets)` — for Figure 6
- `createPEChart(canvasId, companies)` — for Figure 7

Each chart call MUST be in its own `<script>` tag wrapped in a try-catch block. This ensures a bug in one chart does not prevent other charts from rendering. Example:
```html
<script>
try {
  createRevEpsChart('chart-rev-eps', [...], [...], [...], 'Revenue ($B)');
} catch(e) { console.error('Figure 1 error:', e); }
</script>
<script>
try {
  createMarginChart('chart-margins', [...], [...], [...]);
} catch(e) { console.error('Figure 2 error:', e); }
</script>
```

### Report Structure (4-5 pages total)

The report has two halves: **narrative** (pages 1-2) and **figures** (pages 3-5). Keep these tightly integrated.

---

**AI DISCLAIMER (MANDATORY — must appear in 3 places):**
You MUST include the following disclaimer text in the report HTML. This is not optional — the report is incomplete without it:

> **"Analysis is AI-generated — please confirm all outputs"**

It must appear in exactly these 3 locations:
1. **Header banner** — immediately before the cover header, as a centered yellow banner: `<div class="ai-disclaimer">Analysis is AI-generated — please confirm all outputs</div>`
2. **Footer** — inside the page-footer div, as a prominent yellow banner: `<div class="footer-disclaimer">Analysis is AI-generated — please confirm all outputs</div>`
3. **Appendix** — as the first line of the appendix section, before the table: `<div class="ai-disclaimer">Analysis is AI-generated — please confirm all outputs</div>`

---

**PAGE 1: Cover & Thesis**

- **AI disclaimer banner** (yellow, centered — see AI DISCLAIMER rule above)
- **Header**: Company name (TICKER) | Industry | Report date
- **Title**: Thematic, specific to the quarter (e.g., "Walmart Inc. (WMT) Q4 FY2026 Earnings Preview: Holiday Harvest — Can Furner's First Print Confirm the $1T Thesis?")
- **Executive thesis** (2-3 short paragraphs max with bullet points):
  - What we expect from this print in 1-2 sentences
  - 4-6 bullet points covering: our EPS estimate vs consensus, guidance expectations, key metrics to watch, what would move the stock, key debates
  - Keep it direct and opinionated — take a view, don't hedge everything
- **Key management quotes** from the most recent earnings call woven into the narrative where relevant. Do NOT put these under a separate heading. Integrate them naturally as supporting evidence for your thesis points. Format as indented blockquotes.

---

**PAGE 2: Estimates, Themes & News**

- **Consensus Estimates Table** (single table, labeled as a figure):
  - Columns: Metric | Consensus | Our Estimate | y/y Change
  - Rows: Revenue, EPS, Gross Margin, Operating Income, and 2-3 company-specific KPIs that matter (e.g., comp sales, eComm growth, membership revenue — whatever the Street cares about for THIS company)
  - **Color-coding is strictly mechanical:** If the y/y change value is negative, use `class="neg"` (red). If positive, use `class="pos"` (green). If zero or N/A, use `class="neutral"`. The sign of the number determines the class — do NOT override based on interpretation. A -1.1% is ALWAYS red, even if the decline is small.
  - This is the ONLY guidance/estimates section. Do not repeat estimate data elsewhere.

- **Key Metrics Beyond Headline EPS** (bulleted list, 3-5 items):
  - The specific metrics that will determine if this is a good or bad quarter beyond the EPS number
  - For each: what the metric is, what consensus/management expects, why it matters
  - Be specific: "Walmart Connect ad revenue growth (consensus ~30% y/y, 3Q was 33%)"

- **Themes to Watch** (3-5 bullets):
  - Forward-looking items for the upcoming report
  - What management needs to deliver on, what could surprise, what the bears are focused on
  - Each theme: 1-2 sentences max

- **Recent News & Developments** (3-5 bullets):
  - Material news from the last 60 days, one line each
  - Date + headline + brief impact assessment
  - Only include items that could affect the upcoming print or guidance

---

**PAGES 3-5: Figures (all charts and tables)**

All figures are numbered sequentially. Every figure has a title and source line.

- **Figure 1: Quarterly Revenue & Diluted EPS** — Bar/line combo, 8 quarters
- **Figure 2: Margin Trends (Gross & Operating %)** — Dual line chart, 8 quarters
- **Figure 3: Revenue Growth y/y %** — Bar chart with green/red conditional coloring. **Only include quarters where both current and year-ago data exist** (typically the most recent 4 quarters from the 8 fetched). Do NOT include quarters where y/y cannot be computed — the chart should have 4 bars, not 8.
- **Figure 4: Business Segment Revenue** — Table: Segment | Latest Q Rev ($M) | % of Total | y/y Change
- **Figure 5: 1-Year Stock Price with Earnings Dates** — Price line with vertical annotation lines at earnings dates, labeled with quarter and 1-day post-earnings move
- **Figure 6: Stock Performance vs. Competitors (Indexed to 100)** — Multi-line chart, subject company as thick solid line, competitors as thinner dashed lines
- **Figure 7: LTM P/E vs. Competitors** — Horizontal bar chart, subject company highlighted in navy
- **Figure 8: Competitor Comparison Table** — Ticker | Company | Mkt Cap | LTM P/E | NTM P/E | YTD % | 1-Yr %

---

**APPENDIX: Data Sources & Calculations (MANDATORY — DO NOT SKIP OR ABBREVIATE)**

The appendix MUST begin with the AI disclaimer banner: `<div class="ai-disclaimer">Analysis is AI-generated — please confirm all outputs</div>`

The final page(s) of the report MUST include an Appendix table that documents **every claim** — numeric and non-numeric — cited in the report. **Every number that appears in the report body must have a corresponding row in this appendix, and every such number in the report body must be a clickable `<a href="#ref-N">` hyperlink that scrolls to its appendix row.** If a number appears in the report without a hyperlink to the appendix, the report is incomplete.

- **Table columns**: Ref # | Fact | Value | Source & Derivation
- **Ref #**: Sequential ID matching the hyperlink anchors in the report body (`ref-1`, `ref-2`, etc.). Each row has an `id="ref-N"` attribute so hyperlinks scroll to it.
- **Fact**: Human-readable label (e.g., "Q3 FY2026 Revenue", "LTM P/E — WMT", "Management flagged tariff headwinds", "Barclays upgraded to Overweight")
- **Value**: The exact figure as displayed in the report (e.g., "$152.3B", "24.5%", "28.1x"). For non-numeric facts, leave blank or write "N/A".
- **Source & Derivation**: This is the critical column. **Every row must have a specific, detailed source — not just a label.** Follow these rules strictly:

  **For raw financial data from S&P Capital IQ (revenue, EPS, gross profit, operating income, net income, EBITDA, prices, market cap, etc.):**
  - State the MCP function used and its key parameters. Format: `S&P Capital IQ — [function_name](identifier='[TICKER]', line_item='[item]', period_type='[type]', period='[Q# FY####]')`
  - Examples:
    - `S&P Capital IQ — get_financial_line_item_from_identifiers(identifier='WMT', line_item='revenue', period_type='quarterly', period='Q3 FY2026')`
    - `S&P Capital IQ — get_financial_line_item_from_identifiers(identifier='WMT', line_item='diluted_eps', period_type='quarterly', period='Q3 FY2026')`
    - `S&P Capital IQ — get_prices_from_identifiers(identifier='WMT', periodicity='day')`
    - `S&P Capital IQ — get_capitalization_from_identifiers(identifier='WMT', capitalization='market_cap')`
  - **Do NOT just write "S&P Capital IQ" with no detail.** The reader must know exactly which data point from which tool call produced this number.

  **For calculated values (margins, growth rates, P/E, returns, y/y changes):**
  - Show the full formula with **hyperlinked components** — each component must be an `<a href="#ref-N">` link back to the appendix row for that raw data point. This is critical: the reader must be able to click through from the calculated value to each of its inputs.
  - Example: `Gross Margin = <a href='#ref-5'>Gross Profit $37.2B</a> / <a href='#ref-1'>Revenue $152.3B</a> = 24.4%. Source: S&P Capital IQ (calculated)`
  - Example: `LTM P/E = <a href='#ref-20'>Price $172.35</a> / (<a href='#ref-8'>Q1 EPS $1.47</a> + <a href='#ref-9'>Q2 EPS $1.84</a> + <a href='#ref-10'>Q3 EPS $1.53</a> + <a href='#ref-11'>Q4 EPS $1.80</a>) = $172.35 / $6.64 = 25.9x`
  - Example: `Revenue y/y growth = (<a href='#ref-12'>Q3 FY26 Rev $165.8B</a> - <a href='#ref-3'>Q3 FY25 Rev $160.8B</a>) / <a href='#ref-3'>Q3 FY25 Rev $160.8B</a> = +3.1%`
  - **Every formula component must be a clickable hyperlink.** Do NOT write formulas with plain-text numbers.

  **For transcript-sourced claims (quotes, management commentary, guidance):**
  - Write the **verbatim excerpt sentence** from the transcript.
  - Reference the transcript by its full name and the `key_dev_id` used to fetch it.
  - Format: `"[verbatim quote]" — [Speaker], [Title]. Source: [Q# FY#### Earnings Call Transcript] (key_dev_id: [ID])`
  - Example: `"We expect comp sales growth of 3-4% in Q4" — CEO John Furner. Source: Q3 FY2026 Earnings Call Transcript (key_dev_id: 12345678)`

  **For Kensho Grounding search results (news, analyst ratings, consensus estimates):**
  - Write the key finding or excerpt from the search result.
  - **MANDATORY: Include the source URL** returned by the Kensho `search` tool as a clickable `<a href="[URL]" target="_blank">` hyperlink. This is the most important part — readers must be able to click through to the original source.
  - Format: `"[finding/excerpt]" — <a href="[URL]" target="_blank">[Source Title or Publication]</a>. Query: search("[query used]")`
  - Example: `"Barclays upgraded WMT to Overweight with $210 price target on Jan 15, 2026." — <a href="https://www.investing.com/news/barclays-upgrades-wmt" target="_blank">Investing.com, Jan 15 2026</a>. Query: search("WMT analyst ratings price target upgrades downgrades")`
  - If no URL was returned for a particular result, write "Source URL not available" and still include the search query.

**Completeness check:** Before finalizing the report, scan every number in the report body. If any number is not wrapped in `<a href="#ref-N" class="data-ref">`, fix it. If any appendix row has a Source & Derivation that is just a bare label like "S&P Capital IQ" with no function call detail, fix it. If any calculated value's formula lacks hyperlinked components, fix it. If any Kensho-sourced claim lacks a source URL, fix it.

Group the appendix rows by section (Financials, Valuation, Estimates & Consensus, Transcript Claims, News & Analyst Commentary, Stock Performance) with subheadings. Use smaller font size (10-11px).

---

## Phase 8: Output

1. Write the complete HTML file to `earnings-preview-[TICKER]-YYYY-MM-DD.html` in the current working directory.
2. Open it in the browser: `open earnings-preview-[TICKER]-YYYY-MM-DD.html`
3. Tell the user the file has been created and summarize the key findings.

---

## Writing Guidelines

- **NO EMOJIS**: Do not use any emojis anywhere in the report. This is a professional research document.
- **CONCISE**: Target 4-5 printed pages. Every sentence must carry weight. Use bullets, not paragraphs, wherever possible. If a section feels long, cut it.
- **Be specific with numbers**: "$52.4B revenue, up 5.2% y/y" not "strong revenue growth."
- **Take a view**: This is an earnings preview, not a summary. State what you expect, what matters, and why. Be opinionated but back it with data.
- **Management quotes without headers**: Weave 3-4 key management quotes from the most recent call directly into the narrative as blockquotes. Do not create a "Key Management Quotes" section heading — let them flow naturally as supporting evidence.
- **Professional tone**: Sell-side equity research style — analytical, direct, data-driven.
- **Charts must use real data**: Every chart populated with actual MCP data. Never fabricate.
- **Competitor context**: Frame valuation relative to peers. A 25x P/E means nothing without knowing peers trade at 20x or 35x.
- **Hyperlinked claims**: Every factual claim — numeric or qualitative — must be an `<a class="data-ref">` tag linking to its appendix entry. Numbers: `<a href="#ref-1" class="data-ref">$152.3B</a>`. Qualitative: `<a href="#ref-25" class="data-ref">management flagged tariff headwinds as the primary margin risk</a>`. No fact should appear without a traceable source in the appendix.
