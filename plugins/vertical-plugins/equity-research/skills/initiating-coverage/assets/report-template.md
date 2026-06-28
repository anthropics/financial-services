# Equity Research Initiation Report Template

This template provides the structure for creating a comprehensive equity research initiation report. Use this as a guide when constructing the final report document.

**NOTE:** The actual report MUST be created using the DOCX skill. DO NOT generate markdown content.

**CRITICAL REQUIREMENTS:**
1. **Generate 20-30+ chart images** using Python (matplotlib/plotly) BEFORE creating the Word document
2. **Use DOCX skill**: Create professional report with proper styles, headers/footers, and formatting
3. **Embed actual chart images**: Insert the generated PNG/JPG chart files into the Word document at appropriate locations
4. **NO MARKDOWN**: Do not generate markdown content. Use DOCX skill to create a .docx file.

**CRITICAL FORMATTING GUIDANCE:**
- **MAXIMUM DENSITY**: Every page should be packed with information. Intersperse text, charts, and tables throughout.
- **NO ORPHANED SECTIONS**: Never have a section header alone or a single chart on its own page.
- **20-30+ ACTUAL CHART IMAGES**: Generate charts as image files, then embed within text sections using DOCX skill.

---

## PAGE 1: INVESTMENT UPDATE (MOST IMPORTANT PAGE)

**CRITICAL**: Page 1 is NOT a traditional executive summary. It is an **Investment Update** with a specific institutional format used by professional equity research firms.

**IMPORTANT STRUCTURAL NOTES:**
- This is an "Investment Update" or "Company Update" page, not "Executive Summary"
- Uses a rating box in top left corner
- Features stock price performance chart (Figure 1) prominently
- Contains 3-4 detailed bullet points with ■ character
- Each bullet has **bold topic header** followed by 3-5 sentence explanation
- Bottom section has financial and valuation metrics table
- All charts must have figure numbers (Figure 1, Figure 2, etc.) with source lines

### Layout Structure

**TOP LEFT - RATING BOX:**
```
Rating:             [OUTPERFORM / NEUTRAL / UNDERWEIGHT / etc.]
Price ([Date]):     $[XX.XX]
Target Price:       $[XX.XX]
52-Week Range:      $[XX.XX] - $[XX.XX]
Market Cap:         $[XX.X]B
Enterprise Value:   $[XX.X]B
```

**TOP LEFT - RESEARCH ANALYSTS:**
```
[Name], [Credentials (Ph.D., CFA, M.D., etc.)]
[Email] | [Phone]

[Name 2], [Credentials]
[Email] | [Phone]
```

**TOP RIGHT - STOCK PRICE PERFORMANCE:**
```
Figure 1 - [Company Name] Stock Price Performance
[Line chart showing stock price over 12-24 months with benchmark comparison]
Source: Company data, [Firm Name] estimates.
```

**MAIN CONTENT - GRAY HEADER BAR:**
```
[OUTPERFORM / NEUTRAL / etc.] RECOMMENDATION / COMPANY UPDATE
```

**MAIN CONTENT - DETAILED BULLETS (3-4 bullets):**

Use ■ character for bullets. Each bullet follows this format:
```
■ **[Bold Topic Header capturing main point].** Regular text explanation providing 3-5 sentences of detail with specific numbers, comparisons, and analysis. Lead with numbers and quantification where possible. Use "vs." not "versus". Be specific and concrete.

■ **[Second Topic Header].** [3-5 sentences of detailed explanation...]

■ **[Third Topic Header].** [3-5 sentences of detailed explanation...]

■ **[Fourth Topic Header - Optional].** [3-5 sentences of detailed explanation...]
```

**EXAMPLE BULLET FORMAT:**
```
■ **Vertical SaaS leadership and regulatory moat should enable $50bn+ TAM by 2030.**
Deep domain expertise in healthcare IT, strong customer retention (95%+ net revenue retention),
and cross-sell capabilities have driven Acme Health's market expansion. With the healthcare IT
market expected to reach $50bn+ by 2030, Acme Health is well-positioned to capture share given
its regulatory moat and high switching costs. Management has indicated that 70% of current
revenue comes from enterprise hospital systems, suggesting strong product-market fit.
```

**BOTTOM SECTION - FINANCIAL AND VALUATION METRICS TABLE:**
```
                            [Year-3]A   [Year-2]A   [Year-1]A   [Year]E    [Year+1]E
Revenue ($M)                [X]         [X]         [X]         [X]        [X]
Revenue Growth (%)          X.X%        X.X%        X.X%        X.X%       X.X%
Gross Margin (%)           X.X%        X.X%        X.X%        X.X%       X.X%
EBITDA ($M)                [X]         [X]         [X]         [X]        [X]
EBITDA Margin (%)          X.X%        X.X%        X.X%        X.X%       X.X%
EPS ($)                    X.XX        X.XX        X.XX        X.XX       X.XX
P/E (x)                    XX.Xx       XX.Xx       XX.Xx       XX.Xx      XX.Xx
EV/Revenue (x)             X.Xx        X.Xx        X.Xx        X.Xx       X.Xx
EV/EBITDA (x)              XX.Xx       XX.Xx       XX.Xx       XX.Xx      XX.Xx

Note: Use "A" suffix for actual/historical years, "E" suffix for estimated/projected years
Source: Company data, [Firm Name] estimates.
```

---

## FIGURE NUMBERING AND FORMATTING STANDARDS

**CRITICAL**: All charts, graphs, and tables must follow strict figure numbering conventions used in professional equity research.

### Figure Numbering Format

**Every chart/table must have:**
1. **Sequential numbering**: Figure 1, Figure 2, Figure 3, etc. (continue sequentially throughout entire report)
2. **Descriptive title**: "Figure X - [Company] [Specific Metric] [Type of Chart/Analysis]"
3. **Source line** (always at bottom): "Source: Company data, [Firm Name] estimates."

**Examples:**
- Figure 1 - [Company] Stock Price Performance
- Figure 2 - [Company] Historical and Projected Revenue Mix by Product
- Figure 3 - [Company] Revenue by Geographic Region
- Figure 4 - [Product Name] Revenue and Price per Patient per Year
- Figure 5 - [Company] Gross Margin Evolution
- Figure 6 - DCF Sensitivity Analysis ($/share)
- Figure 7 - Valuation Football Field

### Caption Format

```
Figure X - [Descriptive Title]
[Chart/Table/Graph content]
Source: Company data, [Firm Name] estimates.
```

For tables with multiple data sources:
```
Figure X - [Descriptive Title]
[Table content]
Source: Company filings, FactSet, [Firm Name] estimates.
```

### Placement Guidelines

- Figures should be numbered in order of appearance in the report
- First figure (Figure 1) is typically the stock price chart or revenue growth trajectory on Page 1
- Each figure must have its caption directly below the visual
- Source line should be in smaller font, italicized, at the very bottom of the figure

---

## PAGE 2: TABLE OF CONTENTS

```
Executive Summary....................................................1
Investment Thesis & Risks..........................................3
Company Overview.......................................................6
  Business Description & History................................6
  Management & Ownership..........................................8
  Products & Technology...........................................9
  Customers & Go-to-Market......................................11
Growth Outlook & Drivers...........................................13
Financial Analysis & Performance.................................16
  Historical Performance........................................16
  Financial Projections.........................................19
Industry Overview & Competitive Landscape.....................21
  Market Size & TAM..............................................21
  Competitive Analysis..........................................23
  Industry Trends................................................25
Valuation Analysis..................................................27
Appendices & Disclosures...........................................31
```

---

## PAGES 3-5: INVESTMENT THESIS & RISKS

**LAYOUT PRINCIPLE**: Intersperse text with 2-3 charts in this section. Each page should have both text AND graphics. Never have pages with text only or charts only.

### Investment Thesis

**[Thesis Pillar 1]: [Title - e.g., "Large and Growing TAM"]**

[Opening sentence with key statistic]

[Paragraph 1: Market opportunity quantification]
- Current market size
- Growth drivers
- Company's positioning

[Paragraph 2: Why company will capture share]
- Competitive advantages
- Go-to-market strategy
- Early traction/proof points

[Paragraph 3: Financial impact]
- Revenue opportunity
- Margin profile
- Timeline

**[EMBED CHART: TAM Growth Chart]** - Stacked area chart showing market size evolution and company's opportunity

**[Thesis Pillar 2]: [Title - e.g., "Differentiated Technology/Product"]**

[Similar structure - 3 paragraphs covering the opportunity, competitive positioning, and financial impact]

**[EMBED CHART: Competitive Positioning Matrix]** - 2×2 chart showing company vs. competitors on key dimensions

**[Thesis Pillar 3]: [Title - e.g., "Strong Execution and Management"]**

[Similar structure]

**[Add 2-3 more pillars as needed]**

**[EMBED CHART: Margin Expansion Pathway]** - Waterfall or line chart showing path to margin improvement

### Investment Risks

**Company-Specific Risks**

**[Risk 1]: [Title - e.g., "Customer Concentration"]**
[Description of risk, quantification if possible, mitigating factors. 2-3 sentences.]

**[Risk 2]: [Title - e.g., "Execution Risk on Product Roadmap"]**
[Description. 2-3 sentences.]

**[Risk 3-5]: [Additional company-specific risks]**
[Continue with 3-5 total company risks]

**Industry/Market Risks**

**[Risk 1]: [Title - e.g., "Regulatory Uncertainty"]**
[Description. 2-3 sentences.]

**[Risk 2]: [Title - e.g., "Intense Competition"]**
[Description. 2-3 sentences.]

**[Risk 3-4]: [Additional industry/market risks]**
[Continue with 2-4 total industry risks]

---

## PAGES 8-19: COMPANY 101

### Company Description (1 page)

**Overview**
[3-4 paragraphs describing:
- What the company does (in plain English)
- How it makes money
- Who its customers are
- Geographic presence
- Scale/size metrics]

**Business Model Diagram/Visual**
[Insert visual showing how the company creates value]

### Company History (2-3 pages)

**The Early Days: [Founding Story Title]**

[Paragraph on founding: who, when, why, initial vision]

**Timeline of Key Milestones**

```
[Year]: [Founding event, initial funding]
[Year]: [Product launch, key milestone]
[Year]: [Major partnership, funding round]
[Year]: [Geographic expansion, new product]
[Year]: [Recent achievement]
```

**[Major Turning Point or Pivot]**
[If applicable, describe any major strategic shifts]

**[Company Name] Today: [Current State Title]**
[Paragraphs describing current position, recent developments, current strategy]

### Management & Ownership (2 pages)

**Key Executives**

For each executive:
```
[Name] - [Title]
[Bio paragraph including:
- Current role and responsibilities
- Prior experience and track record
- Key accomplishments at company
- Education/credentials]
```

**Corporate Structure & Governance**
- Entity type (C-Corp, PBC, etc.)
- Board composition
- Special governance features
- [Include governance diagram if applicable]

**Ownership Structure** [if disclosed]
- Major shareholders and ownership %
- Strategic investors
- Employee ownership
- Insider ownership trends

### Core Technology/Products (2-3 pages)

**Technology Overview**
[Description of core technology/platform]

**Product Portfolio**

For each major product:
```
[Product Name]

Description:
[What it does, key features]

Target Customers:
[Who uses it, use cases]

Pricing Model:
[How it's priced, typical contract values]

Competitive Positioning:
[How it compares to alternatives]

Traction:
[Customers, revenue, growth metrics]
```

**Product Roadmap**
[Future products/features in development]

### Customers & Distribution (2-3 pages)

**Customer Base**
- Total customers: [number]
- Customer segments (Enterprise, Mid-Market, SMB)
- Geographic breakdown
- Customer case studies/testimonials

**Go-to-Market Strategy**
- Sales channels (direct, partner, etc.)
- Sales cycle and CAC
- Key partnerships for distribution
- Marketing strategy

**Customer Economics**
- LTV/CAC ratio
- Net retention rate
- Churn rates
- Expansion rates

---

## PAGES 20-22: GROWTH OUTLOOK

### Growth Framework Overview

**Short-term Growth Drivers (1-2 years)**
1. [Driver 1]
2. [Driver 2]
3. [Driver 3]

**Medium-term Growth Drivers (3-5 years)**
1. [Driver 1]
2. [Driver 2]

### Detailed Growth Driver Analysis

**[Growth Driver 1]: [Title]**

*Current State:*
[Baseline metrics, current performance]

*Opportunity:*
[Market size, company positioning, growth potential]

*Timeline & Milestones:*
- Near-term (1-2 years): [Expected progress]
- Medium-term (3-5 years): [Expected progress]

*Risks & Challenges:*
[What could prevent realization of this opportunity]

**[Repeat for each major growth driver]**

### Financial Projections

**Revenue Build-up**
[Visual showing how revenue grows from current to projected]

**Scenario Analysis**
[Table or chart showing Bear/Base/Bull case projections]

---

## PAGES 21-24: FINANCIAL ANALYSIS & PERFORMANCE

**LAYOUT PRINCIPLE**: This section should be VERY DENSE with 5-7 charts interspersed with financial tables. Each page should have multiple elements (table + 1-2 charts).

### Historical Financial Analysis

**Income Statement Highlights (3-5 Year History)**
```
                    2021    2022    2023    2024    LTM
Revenue ($M)        [X]     [X]     [X]     [X]     [X]
  Growth %          -       X%      X%      X%      X%
Gross Profit ($M)   [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
EBITDA ($M)         [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
Net Income ($M)     [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
FCF ($M)            [X]     [X]     [X]     [X]     [X]
```

**[CHART 1: Revenue Growth Trajectory]**
Line chart showing historical revenue with annotations for key milestones. Include growth % labels on chart.

**[CHART 2: REVENUE BY PRODUCT/SEGMENT]** ⭐ CRITICAL
Stacked area chart showing revenue composition by product line or business segment over time. This shows mix shift and which products are driving growth.
```
Example segments:
- Product A Revenue
- Product B Revenue
- Product C Revenue
- Services Revenue
```

**[CHART 3: REVENUE BY GEOGRAPHY]** ⭐ CRITICAL
Stacked bar chart showing revenue breakdown by geographic region over time.
```
Example regions:
- North America
- Europe
- Asia-Pacific
- Rest of World
```

### Financial Performance Analysis

**[CHART 4: Gross Margin Evolution]**
Line chart with annotations explaining margin drivers (scale, pricing, mix, etc.)

**[CHART 5: Operating Margin Progression]**
Waterfall chart showing path from gross margin to operating margin, or line chart showing EBITDA margin trend

**[CHART 6: Free Cash Flow Generation]**
Bar + line combo chart: Bars = FCF, Line = FCF margin %

**[CHART 7: Key Operating Metrics Dashboard]**
Multi-panel chart showing 3-4 key metrics:
- Customer count or user growth
- ARPU (Average Revenue Per User) or ACV (Annual Contract Value)
- Customer cohort retention or net revenue retention
- LTV/CAC or magic number or other unit economic metric

### Forward Projections (3-5 Years)

**Projected Financial Model**
```
                    2025E   2026E   2027E   2028E   2029E
Revenue ($M)        [X]     [X]     [X]     [X]     [X]
  Growth %          X%      X%      X%      X%      X%
Gross Profit ($M)   [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
EBITDA ($M)         [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
FCF ($M)            [X]     [X]     [X]     [X]     [X]
  FCF Margin %      X%      X%      X%      X%      X%
```

**Key Assumptions**
- Revenue growth drivers and assumptions
- Margin progression assumptions
- CapEx as % of revenue
- Working capital assumptions

**Charts:**
- Revenue bridge showing growth drivers
- Margin waterfall showing path to profitability/margin expansion
- Free cash flow trajectory

### Fundraising & Valuation [For Private Companies]

**Fundraising History**
```
Round    Date      Amount    Valuation    Lead Investor(s)
Seed     [Date]    $XM       $XM          [Investor]
Series A [Date]    $XM       $XM          [Investor]
Series B [Date]    $XM       $XM          [Investor]
[etc.]
```

**Valuation Evolution Chart**
[Visual showing valuation progression over time]

**Current Valuation Metrics**
- Latest valuation: $XXbn
- Implied valuation multiple: XX.Xx
- Comparison to public peers

---

## PAGES 26-31: INDUSTRY OVERVIEW

### Industry Definition & Market Size

**Industry Overview**
[2-3 paragraphs on:
- Industry definition and scope
- Current market size
- Historical growth rates
- Key trends and drivers]

**Market Size Chart**
[Visual showing market growth from historical through projected]

### Competitive Landscape

**Competitive Positioning Matrix**
[2x2 chart showing company vs. competitors on key dimensions]

**Competitive Comparison Table**
```
Metric              [Company]  Comp A   Comp B   Comp C   Comp D
Revenue ($B)        [X]        [X]      [X]      [X]      [X]
Growth %            X%         X%       X%       X%       X%
Market Share        X%         X%       X%       X%       X%
Gross Margin        X%         X%       X%       X%       X%
Key Differentiator  [X]        [X]      [X]      [X]      [X]
```

**Competitive Analysis Narrative**
[2-3 paragraphs analyzing:
- Competitive strengths and weaknesses
- Market positioning
- Share gains/losses
- Competitive moats]

### Total Addressable Market

**TAM Calculation**
```
Current TAM (2025):              $XXbn
Projected TAM (2030):            $XXbn
CAGR:                            XX%

Segmentation:
- [Segment A]:                   $XXbn
- [Segment B]:                   $XXbn
- [Segment C]:                   $XXbn
```

**TAM Growth Chart**
[Visual showing TAM expansion over time by segment]

**Company's Market Opportunity**
```
Total TAM (2030):                $XXbn
Serviceable TAM:                 $XXbn
Company's Realistic Share:       XX%
Implied Revenue Potential:       $XXbn
```

### Industry Dynamics

**Porter's Five Forces Analysis**
- Threat of new entrants: [High/Medium/Low] - [Explanation]
- Bargaining power of suppliers: [High/Medium/Low] - [Explanation]
- Bargaining power of buyers: [High/Medium/Low] - [Explanation]
- Threat of substitutes: [High/Medium/Low] - [Explanation]
- Industry rivalry: [High/Medium/Low] - [Explanation]

**Key Industry Trends**
1. [Trend 1]: [Description and impact]
2. [Trend 2]: [Description and impact]
3. [Trend 3]: [Description and impact]

---

## PAGES 32-34: VALUATION ANALYSIS

### Valuation Methodology Summary

```
Valuation Method            Weight    Implied Value    Weighted Value
DCF Analysis                50%       $XX - $YY        $ZZ
Trading Comparables         30%       $XX - $YY        $ZZ
Precedent Transactions      20%       $XX - $YY        $ZZ
                           ────       ─────────────    ─────────
Weighted Average Price Target         $AA - $BB        $CC
```

### DCF Analysis

**Key Assumptions**
```
Revenue Growth (2025-2029):         XX% CAGR
Terminal Growth Rate:               X.X%
WACC:                               X.X%
Terminal Year EBITDA Margin:        XX%
```

**Figure X - DCF Sensitivity Analysis ($/share)**

CRITICAL FORMAT: DCF sensitivity must be shown as a 2-way heat map table with color coding.

```
                        Terminal Growth Rate
WACC        2.0%      2.5%      3.0%      3.5%      4.0%
8.0%        $52       $55       $58       $62       $66
9.0%        $48       $51       $54       $57       $61
10.0%       $45       $47       $50       $53       $56
11.0%       $42       $44       $47       $49       $52
12.0%       $39       $41       $44       $46       $49

Color coding: Green (higher values) → Yellow (mid) → Red (lower values)
Source: [Firm Name] estimates.
```

**Scenario Analysis**
```
Scenario      Enterprise Value    Equity Value    Price/Share
Bear Case     $XXbn              $XXbn           $XX
Base Case     $XXbn              $XXbn           $XX
Bull Case     $XXbn              $XXbn           $XX
```

### Trading Comparables

**Figure X - Comparable Companies Analysis**

CRITICAL FORMAT: Comp table must have two-part structure with statistical summary.

**Part 1: Individual Company Data**
```
Company         Ticker   Market   EV/Rev   EV/Rev   EV/EBITDA  EV/EBITDA  Rev     EBITDA
                         Cap($B)  2024E    2025E    2024E      2025E      Growth  Margin
Peer A          PERA     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Peer B          PERB     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Peer C          PERC     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Peer D          PERD     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
[Company]       COMP     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
```

**Part 2: Statistical Summary**
```
Max                      XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
75th Percentile          XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Median                   XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
25th Percentile          XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Min                      XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%

Source: FactSet, company filings, [Firm Name] estimates.
```

**Implied Valuation**
[Calculation showing application of peer multiples to company's metrics]

### Precedent Transactions [If Applicable]

**Figure X - Precedent Transaction Analysis**
```
Date        Target       Acquirer      Deal      EV/Rev   EV/EBITDA  Premium
                                      Value($B)
[MM/YYYY]   [Company A]  [Buyer A]    X.X       X.Xx     XX.X       XX%
[MM/YYYY]   [Company B]  [Buyer B]    X.X       X.Xx     XX.X       XX%
[MM/YYYY]   [Company C]  [Buyer C]    X.X       X.Xx     XX.X       XX%
────────────────────────────────────────────────────────────────────
Median                                          X.Xx     XX.X       XX%

Source: Capital IQ, company filings, [Firm Name] estimates.
```

**Control Premium Analysis**
[Discussion of typical premiums in the industry]

### Valuation Summary

**Figure X - Valuation Football Field**

CRITICAL FORMAT: Football field must be a horizontal bar chart showing all valuation methods.

```
Valuation Method                Low End ────── Range ────── High End

DCF Analysis                    $42 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $58

Trading Comps (NTM)             $45 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $55

Precedent Trans.                $48 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $60
                                                      ↑
                                            Current Price: $50
────────────────────────────────────────────────────────────────
Valuation Range:                $42                        $60

Color coding: Each method should have distinct color bar
Add vertical line showing current stock price
Source: [Firm Name] estimates.
```

**Price Target & Recommendation**
```
Current Price:              $XX.XX ([Date])
Price Target:               $YY.YY
Upside/Downside:            ZZ%

Recommendation:             BUY / HOLD / SELL
Time Horizon:               12 months

Catalysts:
• [Near-term catalyst with timeframe]
• [Medium-term catalyst with timeframe]
• [Long-term catalyst with timeframe]
```

---

## PAGES 35+: APPENDICES & DISCLOSURES

### Appendix A: Detailed Financial Model
[Reference to Excel model]

### Appendix B: Management Bios
[Extended bios if not included in main text]

### Appendix C: Product Detail
[Additional product information if needed]

### Appendix D: Industry Data Sources
[List of sources used for industry analysis]

### Required Disclosures
- Analyst certification
- Important disclosures
- Company-specific disclosures
- Legal entity disclosures
- Other regulatory disclosures

---

## GRAPHICS & CHARTS TO INCLUDE

**TARGET: 20-30+ charts throughout the report**

**CRITICAL PRINCIPLE**: Charts should be embedded within text sections, NOT grouped on separate pages. Every page (except TOC) should have at least one chart or table.

### Page 1 - Executive Summary (3 charts)
1. Revenue/ARR growth trajectory (line chart, historical + projected)
2. Key metrics dashboard (multi-panel chart)
3. Market positioning or margin progression

### Pages 3-5 - Investment Thesis & Risks (3 charts)
4. TAM growth and opportunity (stacked area chart)
5. Competitive positioning matrix (2×2 with bubbles)
6. Margin expansion pathway (waterfall or line)

### Pages 6-17 - Company 101 (6-8 charts)
7. Business model diagram (flow chart)
8. Company timeline (horizontal timeline)
9. Funding history (bar chart with valuation line)
10. Organization chart
11. Product portfolio matrix
12. Customer segmentation (pie or tree map)
13. Geographic revenue breakdown
14. Customer cohort retention

### Pages 18-20 - Growth Outlook (4 charts)
15. Revenue bridge showing drivers (waterfall)
16. Market share evolution (line chart)
17. Product roadmap (timeline)
18. Geographic expansion (map with timeline)

### Pages 21-24 - Financials (7 charts) ⭐ CRITICAL SECTION
19. Revenue growth trajectory (line with annotations)
20. **Revenue by product/segment** (stacked area) ⭐ MUST HAVE
21. **Revenue by geography** (stacked bar) ⭐ MUST HAVE
22. Gross margin evolution (line chart)
23. Operating margin progression (waterfall or line)
24. Free cash flow trajectory (bar + line combo)
25. Key operating metrics dashboard (multi-panel)
26. Scenario comparison (grouped bar: Bear/Base/Bull)

### Pages 25-30 - Industry Overview (6 charts)
27. Market size evolution (area chart with CAGR)
28. Competitive landscape map (2×2)
29. Market share pie chart
30. Market share evolution over time (line chart)
31. TAM segmentation
32. Industry trend charts

### Pages 31-34 - Valuation (5 charts)
33. DCF sensitivity analysis (heat map)
34. DCF waterfall (PV of cash flows → equity value)
35. Trading comps scatter plot (growth vs. multiple)
36. Peer valuation multiples (grouped bar)
37. Valuation football field (range chart)
38. Price target scenarios (bar with upside/downside)

**Chart Style Guidelines:**
- **Consistent color scheme** throughout (pick 3-5 brand colors)
- **Professional fonts** (Arial, Calibri, or similar)
- **Clear labels and legends** on every chart
- **Source citations** at bottom of each chart
- **High information density** - use chart space efficiently
- **Mix of chart types** for visual interest
- **Annotations** to highlight key insights
- **Embedded in text** - never standalone pages
- **Sparklines in tables** where appropriate

---

## NOTES ON USING THIS TEMPLATE

1. **PAGE 1 IS CRITICAL:** The executive summary on page 1 must contain ALL key information - fast facts, financial snapshot, 3 charts, valuation summary, thesis, and risks. This is the most important page.

2. **MAXIMUM DENSITY:** Professional equity research is EXTREMELY information-dense. Every page should be packed with interspersed text, charts, and tables. Aim for 60-80% page coverage with minimal white space.

3. **NO ORPHANED SECTIONS:** Never have a section header alone, or a single chart/table on its own page. Always combine elements. Example: DON'T put "Financial Snapshot" on page 6 by itself - integrate it with surrounding content.

4. **20-30+ CHARTS:** Include extensive graphics throughout, with specific emphasis on:
   - **Revenue by product/segment** (stacked area chart)
   - **Revenue by geography** (stacked bar chart)
   - **Financial performance trends** (multiple charts)
   - Charts should be embedded within text, not grouped separately

5. **Use DOC Skill:** This outline should be converted to a professional Word document using the DOC skill, with proper formatting, styles, headers/footers, and page numbers

6. **Intersplice Content:** Text paragraphs should have charts embedded inline. Each page should have 2-4 distinct elements (tables, charts, text blocks).

7. **Consistent Formatting:** Use consistent styles for headers, body text, tables, and charts throughout. Pick a color scheme and stick to it.

8. **References:** Include citations and sources for all data points

9. **Proofread:** Always proofread for accuracy, especially financial data and calculations

10. **Executive Summary Last:** While it appears on page 1, write this section last after completing the full analysis

11. **Balance:** Present both positive and negative aspects objectively

12. **Specific > Generic:** Use specific data and examples rather than generic statements
