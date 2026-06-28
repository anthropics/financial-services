# Corporate Development Tear Sheet

## Purpose
A target evaluation profile for an internal Corp Dev team assessing a potential acquisition. Unlike the IB/M&A profile (which tells a strategic *story* for a pitch), this is an analytical document focused on strategic fit: how the target's products, customers, technology, and operations overlap with or complement the acquirer's. The Corp Dev audience already knows their own company — they need to understand the target through the lens of "should we buy this, and what would integration look like?"

**Default page length:** 1-2 pages. Corp Dev teams are comfortable with denser profiles and won't penalize a second page if the content is substantive.

## Query Plan

Start with these queries. Break apart and follow up if results are incomplete.

**Query 1 — Target profile:**
"[Company] business description products services technology platform headquarters founded employees sector industry"
→ Header, Business & Product Overview
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`

**Query 2 — Financials:**
"[Company] annual income statement revenue gross profit EBITDA operating income net income capex free cash flow R&D expense total debt cash and equivalents last 4 fiscal years"
→ Financial Summary (pull 4 years; display 3; use the earliest year only for YoY growth computation. R&D is especially important for Corp Dev — they want to understand the target's investment in IP)
→ **Immediately write** raw values to `/tmp/tear-sheet/financials.csv`

**Query 3 — Segments + customers:**
"[Company] revenue by segment business unit last 2 fiscal years key customers end markets customer concentration"
→ Revenue Mix (need 2 years for YoY growth), Customer Analysis
→ **Immediately write** segment data to `/tmp/tear-sheet/segments.csv` (skip if no segment data returned)

**Query 4 — Relationships + competitive landscape:**
"[Company] key customers suppliers partners competitors business relationships technology vendors"
→ Strategic Fit Analysis, Ecosystem Map
→ **Immediately write** to `/tmp/tear-sheet/relationships.txt`

**Query 5 — Valuation + peers:**
If user provided specific comps:
"[Comp company] enterprise value EV/Revenue EV/EBITDA revenue growth EBITDA margin"
Otherwise:
Use the competitors tool to identify 3-5 public peers, then pull EV/Revenue (NTM), EV/EBITDA (NTM), revenue growth %, and EBITDA margin % for each.
Also: "[Company] enterprise value market capitalization valuation multiples"
→ Valuation Context
→ **Immediately write** company multiples to `/tmp/tear-sheet/valuation.csv`
→ **Immediately write** peer data to `/tmp/tear-sheet/peer-comps.csv`

**Query 6 — Ownership (data permitting):**
"[Company] ownership structure investors institutional ownership insider ownership"
→ Ownership snapshot (no intermediate file — included in company-profile.txt if available)

## Sections

Listed in priority order. See "Page Budget & Cut Order" below for explicit cut guidance.

### 1. Company Header
Similar to IB/M&A but adds a "Strategic Relevance" tagline.

| Field | Notes |
|---|---|
| Company name | Large, bold |
| Ticker & Exchange | If public; omit for private |
| HQ Location | |
| Founded / Employees | |
| Enterprise Value | Market cap for public; latest valuation for private |
| Ownership | Public / PE-backed / Founder-led / etc. |
| **Strategic Relevance** | One sentence: why this target is attractive to an acquirer (synthesized from data) |

The "Strategic Relevance" line is unique to Corp Dev. Write from a neutral analytical perspective, not from the target's marketing language. Frame what an acquirer *gets* — not what the target *is*. Good: "Dominant position in commodity price benchmarks with regulatory moat and 70%+ gross margins — a capital-light, high-barrier data asset." Bad: "The world's leading provider of financial data and analytics." The former tells a corp dev team why this is attractive; the latter is a press release.

### 2. Business & Product Overview
**Do not paste the CIQ company summary.** Rewrite in 4-6 sentences (one paragraph, not two) with a product and technology focus — this audience evaluates acquisitions, not investments:
- Core products/services and what problem they solve
- Technology or platform architecture (at a high level)
- Key differentiators and competitive moat
- Customer segments — who buys this and why
- Current strategic direction

Write with an acquirer's lens. The reader is thinking: "How would this fit with what we already have?" The description should make it easy to spot overlaps and complements.

### 3. Revenue Mix & Customer Profile
Two sub-sections:

**a) Revenue by Segment** (if available):

| Segment | Revenue ($M) | % of Total | YoY Growth |
|---|---|---|---|

**b) Customer Analysis:**
Below the segment table (or in place of it if segments aren't available), write a qualitative paragraph covering:
- Customer concentration: are the top 5 customers >30% of revenue? (Critical for acquisition risk)
- Customer type: enterprise vs. SMB vs. consumer
- Contract structure: subscription vs. transactional vs. license (if known)
- Geographic mix

Customer concentration is the single most important signal here — if the tools return any data on top customers or revenue concentration, highlight it prominently. If data is sparse, write what you can infer from the business description and relationships. Keep this to 2-3 sentences — it's context for the segment table, not a standalone analysis.

### 4. Strategic Fit Analysis
**This is the signature section of the Corp Dev tear sheet.** It is required — do not skip or compress it. It uses the Business Relationships data from S&P Capital IQ to map overlaps and complements.

Organize as three buckets. **Each bucket must be 2-3 sentences of analytical reasoning, not a list of company names.** Listing "Customers: Microsoft, JPMorgan, Google" without context is useless. Instead, explain *what the overlap or complement means* for an acquisition.

**Customer Overlap:** Do the target's customers also buy from the acquirer (or the acquirer's industry)? Shared customers = easier cross-sell, but also risk of channel conflict. Name shared relationships and explain the implications.

**Technology / Product Complement:** Does the target fill a gap in the acquirer's portfolio? What does their tech stack look like? Who are their technology vendors? If they're already using the acquirer's technology, explain why that's a strong integration signal.

**Competitive Displacement:** Is the target a competitor, or does acquiring them remove a competitor from the market? Name the target's key competitors and explain how the competitive landscape would change post-acquisition.

This section requires synthesis — combine relationship data with the business overview to draw connections. If the user has told you who the acquirer is, tailor to that acquirer. If not, write it generically but still analytically.

**Length discipline:** The 2-3 sentence target per bucket above is a hard constraint, not a suggestion. Each bullet should front-load the insight, then support with one specific data point. The actual outputs frequently balloon to 5-7 sentences per bullet — this is the primary driver of page 3 spillover. If you find yourself writing more than 3 sentences, move the excess detail to Integration Considerations.

### 5. Financial Summary (3-Year)
Similar to IB/M&A but with added emphasis on R&D and capital efficiency.

| Metric ($M) | FY20XX | FY20XX | FY20XX |
|---|---|---|---|
| Revenue | | | |
| Revenue Growth % | | | |
| Gross Margin % | | | |
| EBITDA | | | |
| EBITDA Margin % | | | |
| R&D Expense | | | |
| R&D as % of Revenue | | | |
| Capex | | | |
| Free Cash Flow | | | |
| FCF Conversion (FCF/EBITDA) | | | |

R&D intensity signals how much of the target's value is in IP vs. services. FCF conversion signals integration complexity — high-capex businesses are harder to integrate. If R&D expense isn't separately reported, note "Not separately disclosed" in the row rather than "N/A" — this itself is informative (suggests R&D may be embedded in COGS or SG&A).

**Capital Structure** (compact sub-table below the financial summary):

| Metric | Value |
|---|---|
| Total Debt | $XXM |
| Cash & Equivalents | $XXM |
| Net Debt | $XXM |
| Net Debt / EBITDA | X.Xx |

Frame for acquisition context: below the table, include one sentence interpreting leverage (e.g., "Net debt of $X represents Y.Yx EBITDA leverage, which is manageable for an investment-grade acquirer but would compound leverage in an LBO scenario."). Pull from the balance sheet data already retrieved.

### 6. Valuation Context
**This section is required for public companies.** Corp Dev teams need market context to frame a potential bid. If the tools return valuation multiples, this section must appear. Do not cut it for space — cut Ownership Snapshot (Section 7) first.

Not a formal valuation — Corp Dev teams do their own DCFs. This provides market context.

**a) Trading multiples** (if public):

**Peer context is essential, not optional.** If the user provided comps, show each in its own column. If no comps were provided, use the competitors tool to identify 3-5 public peers, then pull EV/Revenue (NTM), EV/EBITDA (NTM), revenue growth %, and EBITDA margin % for each.

| Metric | [Company] | [Peer 1] | [Peer 2] | [Peer 3] | Peer Median |
|---|---|---|---|---|---|
| EV/Revenue (NTM) | | | | | |
| EV/EBITDA (NTM) | | | | | |
| Revenue Growth % | | | | | |
| EBITDA Margin % | | | | | |

A company's multiples in isolation tell a corp dev team nothing — they need relative context to assess whether the target is cheap or rich vs. the peer set. This is the minimum viable valuation context for a target profile.

If peer multiples are unavailable from the tools, show the company's own multiples and list selected peer names below the table for the reader's reference.

**b) Precedent transactions (data permitting):**
If the M&A tools return recent transactions involving the company's peers or within the same sub-sector, display them:

| Date | Target | Acquirer | EV ($M) | EV/Rev | EV/EBITDA |
|---|---|---|---|---|---|

Frame as context: "Recent transactions in [sub-sector] have valued targets at X–Yx revenue."

If precedent transaction data is not available from the tools, note "Precedent transaction data not available from data source" rather than omitting silently. Do not fabricate precedent multiples.

For private companies, skip trading multiples. Precedent transactions (data permitting) are still useful.

### 7. Ownership Snapshot (data permitting — omit if tools return nothing)
If the tools return ownership data, include a compact block: founder/family control %, PE sponsor details, institutional concentration. Ownership structure directly impacts deal complexity and is relevant for integration considerations.

**Do not include a Management Team table.** No S&P Global tool returns executive data — see Data Integrity Rule 10. Management names from training data will be stale.

### 8. Integration Considerations
**Required section — do not cut.** This is the analytical capstone of the Corp Dev tear sheet. Synthesized observations drawn from everything above. 3-4 substantive bullets:
- **Key risks:** Customer concentration, key-person dependency, technology debt indicators
- **Integration complexity:** Geography (multi-country = harder), employee count, number of products
- **Synergy signals:** Shared customers, complementary products, overlapping technology vendors
- **Open questions:** What would a corp dev team need to diligence before making a bid? Focus on concrete, actionable diligence items — not open-ended strategic questions. Good examples: regulatory approval timeline and jurisdictions, change-of-control provisions in key contracts, key-person retention risk (especially founders/CTOs), customer contract transferability, IP ownership structure, outstanding litigation. Bad examples: "How defensible is X?" or "What is the long-term market opportunity?" — these are analyst questions, not diligence items.

Label clearly as analytical observations, not facts from the data source.

## Page Budget & Cut Order

**Target: 2 pages.** Corp Dev profiles can fill both pages with substantive content, but must not spill to a third unless the user explicitly requests a longer format. If content exceeds 2 pages, cut in this order (cut each completely before moving to the next):

1. Ownership Snapshot (section 7) — omit entirely
2. Customer Analysis prose under Revenue Mix (section 3) — reduce to 2 sentences max
3. Valuation Context prose (section 6) — keep peer comp table, cut interpretive paragraph below it
4. Precedent Transactions (section 6b) — keep the "not available" note, remove if space-critical
5. Capital Structure prose — keep table, cut interpretive paragraph below it
6. Strategic Fit Analysis (section 4) — compress each bullet to 2-3 sentences max (do not remove the section)

Never cut: Business & Product Overview (2), Financial Summary (5 core table), Integration Considerations (8).

## Formatting Notes
- **Strategic Fit Analysis is the centerpiece.** Give it distinctive formatting:
  - Bump text to 9.5pt (size: 19) — slightly larger than standard body text. This section should look like the most important content on the page.
  - Use the standard indented block-style bullets from the global style config (360 DXA left indent).
  - Do not apply left-border accents — they render inconsistently in docx-js.
- Financial Summary should include R&D and FCF conversion prominently.
- Valuation Context with peer comps is required for public companies — do not cut before Ownership Snapshot.
- For private targets, the profile leans heavily on qualitative sections (Business Overview, Strategic Fit, Relationships) — this is expected and still highly valuable.
- Tone: analytical and evaluative, not promotional. This isn't a pitch — it's an assessment.
- **Two-page discipline:** Before rendering, mentally estimate page count. The combination of Strategic Fit (3 long bullets) + Integration Considerations (4 bullets) alone can consume a full page — if so, compress Strategic Fit bullets first.
