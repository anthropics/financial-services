# Sales / Business Development Tear Sheet

## Purpose
A briefing document to prepare a sales or BD team for a client meeting. Emphasis on understanding the prospect's business, what leadership is publicly prioritizing, and identifying angles to connect your product/service to their needs. Financials are simplified to scale and trajectory.

This is the most narrative-driven tear sheet type. It reads like a briefing memo, not a data sheet.

**Default page length:** 1-2 pages. No strict convention — prioritize readability over compression.

## Query Plan

Start with these queries. Follow up if results are incomplete.

**Query 1 — Company profile + financials:**
"[Company] business description overview products services headquarters employees sector industry revenue gross margin last 2 fiscal years"
→ Header, Company Overview, Financial Snapshot
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`
→ **Immediately write** raw financials to `/tmp/tear-sheet/financials.csv`

**Query 2 — Strategy + earnings:**
"[Company] most recent earnings call strategic priorities CEO commentary guidance key initiatives"
→ Strategic Priorities
→ **Immediately write** to `/tmp/tear-sheet/earnings.txt`

**Query 3 — Relationships + news:**
"[Company] key customers suppliers partners competitors business relationships recent acquisitions partnerships announcements"
→ Key Relationships, Recent News
→ **Immediately write** to `/tmp/tear-sheet/relationships.txt`

Three queries is usually sufficient. For well-known companies, these return rich results. For smaller or private companies, Queries 2 and 3 may be sparse — that's fine. The qualitative sections still deliver value because Claude synthesizes whatever is available into useful framing.

## Sections

Listed in priority order. Cut from the bottom if space is constrained.

### 1. Company Header
Streamlined — identification only, no valuation metrics.

| Field | Notes |
|---|---|
| Company name | Large, bold |
| Ticker & Exchange | If public; omit for private |
| HQ | City, State/Country |
| Industry / Sector | |
| Employees | |
| Annual Revenue (latest) | Round to nearest $B or $M |
| Market Cap | If public; omit for private |
| FY Revenue Guidance | If available from earnings data; e.g., "6–8% organic growth" |
| FY EPS or EPS Guidance | If public company; pull from `earnings.txt` |
| Key Financial Metric | Adj. EPS, EBITDA margin, or similar — one headline number |

Forward guidance and EPS data come from Query 2 (earnings) — source from `earnings.txt` when populating the header, not just `company-profile.txt`.

One horizontal band at the top. No enterprise value, no beta — this audience doesn't need them.

### 2. Company Overview
The most important section. A sales rep should read this and walk into a meeting with a solid grasp of the prospect.

**Do not paste the CIQ company summary.** It reads like an SEC filing and will lose a non-finance audience. Rewrite in 3-5 sentences of plain language:
- What the company does (no investor jargon — say "sells" not "monetizes", say "yearly revenue" not "top-line CAGR")
- Who their customers are
- How they make money
- Where they operate
- What makes them distinctive

Write in prose paragraphs. A non-finance person should understand every sentence.

### 3. Strategic Priorities & Management Commentary
What is leadership focused on right now? If you know what the CEO is talking about, you can align your pitch.

**This is NOT an earnings recap.** Do not reuse the same bullets as the equity research tear sheet. Extract 3-5 *strategic themes* with thematic labels and supporting data points:

- **AI/Data Monetization:** Management is investing aggressively in AI capabilities, allocating $X to R&D in FY2024 and launching three new AI-powered products.
- **Margin Expansion:** CEO cited operational efficiency as a top priority, targeting 200bps of operating margin improvement through automation.
- **International Growth:** Opening new offices in EMEA; Europe now represents 25% of revenue, up from 18%.

Each bullet should answer: "What does this company care about right now, and what evidence supports it?" A sales rep should read these and immediately see angles to connect their product.

If earnings call data isn't available (common for private companies), replace with "Recent Developments" pulling from whatever news or announcements the tools return.

### 4. Financial Snapshot
Simplified. Single compact table — just scale, direction, and one profitability signal. A sales rep needs to know three things: how big is this company, is it growing, and is it healthy.

| Metric | FY[prior year] | FY[latest] | YoY Change |
|---|---|---|---|
| Revenue | | | +X% |
| Gross Margin % | | | +X.Xpp |
| Employees | | | |

Three rows maximum. No EBITDA, no EV multiples, no balance sheet, no net income. Gross margin (not EBITDA, not net income) is the right single profitability metric for a sales audience — it's intuitive ("how much they keep after direct costs") and signals business health without requiring finance literacy. If the rep needs deeper financials, they can request the equity research version.

For private companies, this table may have only revenue and employees — two data points showing scale and growth are enough for a sales meeting.

### 5. Key Relationships & Ecosystem
Helps reps understand the prospect's world and identify angles.

Four labeled lists, 3-5 names each with one-line descriptors:

**Customers:** Who they sell to. Helps understand their go-to-market and shared target customers.
Example: "JPMorgan Chase — customer (enterprise analytics platform deployment)"

**Vendors / Technology:** What they buy. Identifies displacement or integration opportunities.
Example: "AWS — vendor (primary cloud infrastructure); Snowflake — vendor (data warehouse)"

**Partners:** Who they work with. Co-sell angles, mutual connections.
Example: "Deloitte — partner (implementation for enterprise clients)"

**Competitors:** Who they compete against. Positioning context.
Example: "Bloomberg — competitor (financial data terminal)"

Every entry needs a parenthetical descriptor so the rep understands *what* the relationship means, not just *who*.

If relationship data isn't available, note "Relationship data not available" and move on.

### 6. Recent News & Developments
3-5 bullets, each one sentence, most recent first. Include date if available. **Lead with the latest earnings report** — it's the most important recent event for a sales meeting and sets the context for everything else. Then: M&A, product launches, leadership changes, major wins.

**Include upcoming catalysts at the end of the section** with a "**Coming Up:**" label. Examples: upcoming earnings dates, pending divestitures, product launches, investor days, regulatory milestones. These create natural engagement windows for sales outreach and are often the best reason to reach out ("I noticed you have your Investor Day coming up in Q2..."). Pull from earnings call commentary and M&A data (pending transactions).

### 7. Conversation Starters (cut first)
2-3 suggested talking points synthesized from the data above. **Each starter must reference a specific strategic priority from Section 3** — generic questions are useless. Frame as questions.

**Tag each starter with a suggested persona** — e.g., (CTO), (CFO), (CDO), (Head of Data), (VP Engineering), (Head of Procurement). A rep meeting with a CTO needs a different opener than one meeting with a CFO. If the user specified who they're meeting with, generate starters for that persona only.

Examples:
- *(CTO/CDO)* "You mentioned [specific AI initiative from Section 3] on your last earnings call — how is that impacting your [relevant need]?"
- *(CFO/COO)* "With your [margin expansion target from Section 3], are you evaluating tools that could accelerate that timeline?"
- *(VP Strategy/Corp Dev)* "I noticed [Company] recently acquired [target] — does that change your approach to [capability]?"

If the user described what product/service they're selling, tailor these to connect the prospect's priorities to that offering. If not, keep them grounded in the prospect's strategic themes but generic in solution framing.

**Validation test:** Before finalizing each conversation starter, verify it contains at least one specific number, date, product name, or initiative name drawn from the tear sheet. A question that could apply to any company in the sector is not a good conversation starter. "How are you thinking about AI?" is generic. "Your CEO mentioned $1B in AI investment since 2018 and 20% adoption of the iLEVEL auto-ingestion feature — how is that changing your analysts' workflows?" is specific and demonstrates preparation.

This section is Claude's synthesis, not raw data from the tools. Label it clearly.

## Formatting Notes
- **This should be the warmest, most readable tear sheet.** Rigorous content, but the formatting should feel like a briefing memo, not a data terminal.
- Body text: use the full 9pt (size: 18). No compression — readability over density.
- Line spacing: 1.15x on body paragraphs (slightly more generous than default). This template is the one where whitespace is a feature, not waste.
- Company Overview and Strategic Priorities should take ~40-50% of the page.
- Financial Snapshot: visually compact, secondary prominence. Keep it small and clean.
- Key Relationships: consider two-column layout (Customers + Vendors on left, Partners + Competitors on right) to save vertical space while keeping descriptors visible.
- Conversation Starters: use the indented block-style bullets. These are the payoff of the document — they should stand out visually.
