---
name: tear-sheet
description: "Generate professional company tear sheets using S&P Capital IQ data via the Kensho LLM-ready API MCP server. Use this skill whenever the user asks for a tear sheet, company one-pager, company profile, fact sheet, company snapshot, or company overview document — especially when they mention a specific company name or ticker. Also trigger when users ask for equity research summaries, M&A company profiles, corporate development target profiles, sales/BD meeting prep documents, or any concise single-company financial summary. This skill supports four audience types: equity research, investment banking/M&A, corporate development, and sales/business development. If the user doesn't specify an audience, ask. Works for both public and private companies."
---

# Financial Tear Sheet Generator

Generate audience-specific company tear sheets by pulling live data from S&P Capital IQ via the S&P Global MCP tools and formatting the result as a professional Word document.

## Style Configuration

These are sensible defaults. To customize for your firm's brand, modify this section — common changes include swapping the color palette, changing the font (Calibri is standard at many banks), and updating the disclaimer text.

**Colors:**
- Primary (header banner background, section header text): #1F3864
- Accent (signature section highlights): #2E75B6
- Table header row fill: #D6E4F0
- Table alternating row fill: #F2F2F2
- Table borders: #CCCCCC
- Header banner text: #FFFFFF

**Typography (sizes in half-points for docx-js):**
- Font family: Arial
- Company name: 18pt bold (size: 36)
- Section headers: 11pt bold (size: 22), Primary color
- Body text: 9pt (size: 18)
- Table text: 8.5pt (size: 17)
- Footer/disclaimer: 7pt italic (size: 14)
- Per-template overrides are specified in each reference file's Formatting Notes.

**Company Header Banner:**
- The header is a navy (#1F3864) banner spanning the full page width with company name in white.
- **Below the banner, key-value pairs MUST be rendered in a two-column borderless table spanning the full page width.** Left column: company identifiers (ticker, HQ, founded, employees, sector). Right column: financial identifiers (market cap, EV, stock price, shares outstanding). Each cell contains a bold label and regular-weight value on the same line (e.g., "**Market Cap** $124.7B"). Do not left-justify all fields in a single column — this wastes horizontal space and looks unprofessional. The two-column spread is the single most important visual signal that distinguishes a professional tear sheet from a default document.
  - **Implementation:** Create a 2-column table with `borders: none` and `shading: none` on all cells. Set column widths to 50% each. Place left-column fields (ticker, HQ, founded, employees) as separate paragraphs in the left cell. Place right-column fields (market cap, EV, stock price, shares outstanding) in the right cell. Each field is a single paragraph: bold run for the label, regular run for the value.
  - The specific fields in each column vary by audience — see the reference file's header spec. The principle is always: spread across the page, not clumped left.
- **Do not use a bordered table for the header key-value block.** Bordered tables are reserved for financial data only.
- Key metrics in the header (market cap, EV, stock price) should be displayed as inline key-value pairs, not in a separate bordered table.

**Section Headers:**
- Each section header gets a horizontal rule (thin line, #CCCCCC, 0.5pt) directly beneath it to create clean visual separation between sections.
- **Render the rule as a bottom border on the header paragraph itself** — do not insert a separate paragraph element for the rule. A separate paragraph adds its own before/after spacing and causes excessive whitespace below section titles.
- **Implementation:** In docx-js, apply a bottom border to the section header paragraph via `paragraph.borders.bottom = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" }`. Do not use `doc.addParagraph()` with a separate horizontal rule element. Do not use `thematicBreak`. The border must be on the heading paragraph itself with 0pt spacing after, so the rule sits tight against the header text.
- Spacing: 12pt before the header paragraph, 0pt after the header paragraph, 4pt before the next content element.

**Bullet Formatting:**
- Use a single bullet character (•) for all bulleted content across all tear sheet types. Do not mix •, -, ▸, or numbered lists within or across tear sheets.
- **Synthesis/analysis bullets** (Earnings Highlights, Strategic Fit, Integration Considerations, Conversation Starters): indented block-style formatting with left indent 360 DXA (0.25") and a hanging indent for the bullet character. These should be visually offset from body text — they're interpretive content and should look distinct from data tables and prose paragraphs.
- **Informational bullets** within relationship sections: standard body indent (180 DXA), no hanging indent.
- **Do not apply left-border accents to any bullet sections.** Left-border styling renders inconsistently in docx-js and creates visual artifacts. Use indentation and text size differentiation to distinguish signature sections instead.

**Tables (financial data only):**
- Header row: Table Header Fill (#D6E4F0) with bold dark text
- Body rows: alternating white / Table Alternating Fill (#F2F2F2)
- Borders: Table Border color (#CCCCCC), thin (BorderStyle.SINGLE, size 1)
- Cell padding: top/bottom 40 DXA, left/right 80 DXA
- Right-align all numeric columns
- Always use ShadingType.CLEAR (never SOLID — SOLID causes black backgrounds)

**Layout:**
- US Letter portrait, 0.75" margins (1080 DXA all sides)

**Number formatting:**
- Currency: USD. Use millions unless company revenue > $50B (then billions, one decimal). Label units in column headers (e.g., "Revenue ($M)"), not in individual cells.
- **Table cells: plain numbers with commas, no dollar signs.** Example: a revenue cell shows "4,916" not "$4,916". The column header carries the unit.
- Fiscal years: actual years (FY2022, FY2023, FY2024), never relative labels (FY-2, FY-1).
- Negatives: parentheses, e.g., (2.3%)
- Percentages: one decimal place
- Large numbers: commas as thousands separators

**Footer (document footer, not inline):**
Place the source attribution and disclaimer in the actual document footer (repeated on every page), not as inline body text at the bottom. The footer is exactly two lines, centered, on every page:
- Line 1: "Data: S&P Capital IQ via Kensho | Analysis: AI-generated | [Month Day, Year]"
- Line 2: "For informational purposes only. Not investment advice."
- Style: 7pt italic, centered, #666666 text color
- This footer text must be identical across all tear sheet types for the same company. Do not vary the wording by audience.
- **This footer is required on every tear sheet, every audience type, every page.** Do not omit it.

## Component Functions

**You MUST use these exact functions to create document elements. Do NOT write custom docx-js styling code.** Copy these functions into your generated Node script and call them. The Style Configuration prose above remains as documentation; these functions are the enforcement mechanism.

```javascript
const docx = require("docx");
const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType,
  Header, Footer, PageNumber, HeadingLevel, TableLayoutType,
  convertInchesToTwip
} = docx;

// ── Color constants ──
const COLORS = {
  PRIMARY: "1F3864",
  ACCENT: "2E75B6",
  TABLE_HEADER_FILL: "D6E4F0",
  TABLE_ALT_ROW: "F2F2F2",
  TABLE_BORDER: "CCCCCC",
  HEADER_TEXT: "FFFFFF",
  FOOTER_TEXT: "666666",
};

const FONT = "Arial";

// ── 1. createHeaderBanner ──
// Returns an array of docx elements: [banner paragraph, key-value table]
function createHeaderBanner(companyName, leftFields, rightFields) {
  // leftFields / rightFields: arrays of { label: string, value: string }
  const banner = new Paragraph({
    children: [
      new TextRun({
        text: companyName,
        bold: true,
        size: 36, // 18pt
        color: COLORS.HEADER_TEXT,
        font: FONT,
      }),
    ],
    shading: { type: ShadingType.CLEAR, color: "auto", fill: COLORS.PRIMARY },
    spacing: { after: 0 },
    alignment: AlignmentType.LEFT,
  });

  function buildCellParagraphs(fields) {
    return fields.map(
      (f) =>
        new Paragraph({
          children: [
            new TextRun({ text: f.label + "  ", bold: true, size: 18, font: FONT }),
            new TextRun({ text: f.value, size: 18, font: FONT }),
          ],
          spacing: { after: 40 },
        })
    );
  }

  const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
  const noShading = { type: ShadingType.CLEAR, color: "auto", fill: "FFFFFF" };

  const kvTable = new Table({
    rows: [
      new TableRow({
        children: [
          new TableCell({
            children: buildCellParagraphs(leftFields),
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: noBorders,
            shading: noShading,
          }),
          new TableCell({
            children: buildCellParagraphs(rightFields),
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: noBorders,
            shading: noShading,
          }),
        ],
      }),
    ],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });

  return [banner, kvTable];
}

// ── 2. createSectionHeader ──
// Returns a single Paragraph with bottom border rule
function createSectionHeader(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 22, // 11pt
        color: COLORS.PRIMARY,
        font: FONT,
      }),
    ],
    spacing: { before: 240, after: 0 }, // 12pt before, 0pt after
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    },
  });
}

// ── 3. createTable ──
// headers: string[], rows: string[][], options: { accentHeader?, fontSize? }
function createTable(headers, rows, options = {}) {
  const fontSize = options.fontSize || 17; // 8.5pt default
  const headerFill = options.accentHeader ? COLORS.ACCENT : COLORS.TABLE_HEADER_FILL;
  const headerTextColor = options.accentHeader ? COLORS.HEADER_TEXT : "000000";

  const cellBorders = {
    top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    left: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    right: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
  };

  const cellMargins = { top: 40, bottom: 40, left: 80, right: 80 };

  function isNumeric(val) {
    if (typeof val !== "string") return false;
    const cleaned = val.replace(/[,$%()]/g, "").trim();
    return cleaned !== "" && !isNaN(cleaned);
  }

  // Header row
  const headerRow = new TableRow({
    children: headers.map(
      (h) =>
        new TableCell({
          children: [
            new Paragraph({
              children: [
                new TextRun({
                  text: h,
                  bold: true,
                  size: fontSize,
                  color: headerTextColor,
                  font: FONT,
                }),
              ],
            }),
          ],
          shading: { type: ShadingType.CLEAR, color: "auto", fill: headerFill },
          borders: cellBorders,
          margins: cellMargins,
        })
    ),
  });

  // Data rows with alternating shading
  const dataRows = rows.map((row, rowIdx) => {
    const fill = rowIdx % 2 === 1 ? COLORS.TABLE_ALT_ROW : "FFFFFF";
    return new TableRow({
      children: row.map((cell, colIdx) => {
        const align = colIdx > 0 && isNumeric(cell)
          ? AlignmentType.RIGHT
          : AlignmentType.LEFT;
        return new TableCell({
          children: [
            new Paragraph({
              children: [
                new TextRun({ text: cell, size: fontSize, font: FONT }),
              ],
              alignment: align,
            }),
          ],
          shading: { type: ShadingType.CLEAR, color: "auto", fill: fill },
          borders: cellBorders,
          margins: cellMargins,
        });
      }),
    });
  });

  return new Table({
    rows: [headerRow, ...dataRows],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

// ── 4. createBulletList ──
// items: string[], style: "synthesis" | "informational"
function createBulletList(items, style = "synthesis") {
  const indent =
    style === "synthesis"
      ? { left: 360, hanging: 180 }   // 360 DXA left, hanging indent for bullet
      : { left: 180 };                 // 180 DXA, no hanging

  return items.map(
    (item) =>
      new Paragraph({
        children: [
          new TextRun({ text: "•  ", font: FONT, size: 18 }),
          new TextRun({ text: item, font: FONT, size: 18 }),
        ],
        indent: indent,
        spacing: { after: 60 },
      })
  );
}

// ── 5. createFooter ──
// date: string (e.g., "February 23, 2026")
function createFooter(date) {
  return new Footer({
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: `Data: S&P Capital IQ via Kensho | Analysis: AI-generated | ${date}`,
            italics: true,
            size: 14, // 7pt
            color: COLORS.FOOTER_TEXT,
            font: FONT,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: "For informational purposes only. Not investment advice.",
            italics: true,
            size: 14,
            color: COLORS.FOOTER_TEXT,
            font: FONT,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
    ],
  });
}
```

**Usage in generated scripts:**
1. Copy all functions and constants above into the generated Node.js script
2. Call `createHeaderBanner(...)` instead of manually building banner paragraphs and tables
3. Call `createSectionHeader(...)` for every section title — never manually set paragraph borders
4. Call `createTable(...)` for **all** tabular data — financial summaries, trading comps, M&A activity, relationship tables, funding history, etc. Pass `{ accentHeader: true }` for M&A activity tables (IB/M&A template). For non-numeric tables (e.g., relationships, ownership), the function still works correctly — it only right-aligns cells that contain numeric values.
5. Call `createBulletList(items, "synthesis")` for earnings highlights, strategic fit, integration considerations, and conversation starters
6. Call `createBulletList(items, "informational")` for relationship entries
7. Pass `createFooter(date)` to the Document constructor's `footers.default` property

**What these functions eliminate:**
- Black background tables (enforces `ShadingType.CLEAR` everywhere)
- Separate horizontal rule paragraphs under section headers (enforces `border.bottom` on the paragraph itself)
- Bordered key-value tables in headers (enforces `borders: none`)
- Inconsistent bullet styles (enforces `•` character only)
- Missing footers (provides the exact footer structure)

## Workflow

### Step 1: Identify Inputs

Gather up to four things before proceeding:

1. **Company** — name or ticker. If only a ticker, resolve the full company name with an initial query (e.g., use the company info tool).
2. **Audience** — one of four types:
   - **Equity Research** — for buy-side/sell-side analysts evaluating an investment
   - **IB / M&A** — for bankers profiling a company in transaction context
   - **Corp Dev** — for internal strategic teams evaluating an acquisition target
   - **Sales / BD** — for commercial teams preparing for a client meeting
3. **Comparable companies** (optional) — if the user has specific comps in mind, note them. Otherwise the skill will identify peers from S&P Global data. This matters for Equity Research, IB/M&A, and Corp Dev tear sheets.
4. **Page length preference** (optional) — defaults vary by audience (see below), but the user can override.

If the user doesn't specify an audience, ask.

### Step 2: Read the Audience-Specific Reference

Read the corresponding reference file from this skill's directory:

- Equity Research → `references/equity-research.md`
- IB / M&A → `references/ib-ma.md`
- Corp Dev → `references/corp-dev.md`
- Sales / BD → `references/sales-bd.md`

Each reference defines sections, a query plan, formatting guidance, and page length defaults.

### Step 3: Pull Data via S&P Global MCP

**First:** Create the intermediate file directory:
```bash
mkdir -p /tmp/tear-sheet/
```

Use the **S&P Global** MCP tools (also known as the Kensho LLM-ready API). Claude will have access to structured tools for financial data, company information, market data, consensus estimates, earnings transcripts, M&A transactions, and business relationships. The query plans in each reference file describe what data to retrieve for each section — map these to the appropriate S&P Global tools available in the conversation.

**After each query step, immediately write the retrieved data to the intermediate file(s) specified in the reference file's query plan.** Do not defer writes — data written to disk is protected from context degradation in long conversations.

**Query strategy:**
Each reference file includes a query plan with 4-6 data retrieval steps. These are starting points, not rigid constraints. Prioritize data completeness over minimizing calls:

- **Always pull 4 fiscal years of financial data**, even though only 3 years are displayed. The fourth (earliest) year is needed to compute YoY revenue growth for the first displayed year. Without it, the earliest year's growth rate will show "N/A" — which looks like missing data, not a design choice.
- Execute the query plan as written, using whichever S&P Global tools match the data needed.
- If a tool call returns incomplete results, try alternative tools or narrower queries. For example, if company summary doesn't include segment detail, try the segments tool directly.
- If a data point isn't returned after a targeted retry, move on — label it "N/A" or "Not disclosed."
- Never fabricate data. If the tools don't return a number, do not estimate from training knowledge.

**User-specified comps:** If the user provided comparable companies, query financials and multiples for each comp explicitly. If no comps were provided, use whatever peer data the tools return, or identify peers from the company's sector using the competitors tool.

**Optional context from the user:** Listen for additional context the user provides naturally. If they mention who the acquirer is ("we're looking at this for our platform"), what they sell ("we sell data analytics to banks"), or who the likely buyers are ("this would be interesting to Salesforce or Microsoft"), incorporate that context into the relevant synthesis sections (Strategic Fit, Conversation Starters, Deal Angle). Don't prompt for this information — just use it if offered.

**Private company handling:**
CIQ includes private company data, so query the same way. However, expect sparser results. When generating for a private company:
- Skip: stock price, 52-week range, beta, stock performance, consensus estimates, trading comps
- Lean into: business overview, relationships, ownership structure, whatever financials are available
- Note "Private Company" prominently in the header

### Step 3b: Calculate Derived Metrics

After all data collection is complete and intermediate files are written, compute all derived metrics in a single dedicated pass. This is a calculation-only step — no new MCP queries.

**Read all intermediate files back into context**, then compute:

- **Margins:** Gross Margin %, EBITDA Margin %, FCF Margin %, Operating Margin %
- **Growth rates:** YoY revenue growth, YoY segment revenue growth, YoY EPS growth
- **Efficiency ratios:** FCF Conversion (FCF/EBITDA), R&D as % of Revenue, Capex as % of Revenue
- **Capital structure:** Net Debt (Total Debt − Cash & Equivalents), Net Debt / EBITDA
- **Segment mix:** Each segment's revenue as % of consolidated total revenue (use consolidated revenue as denominator per Data Integrity Rule 8)

**Validation (moved from Arithmetic Validation):** During this calculation pass, enforce all arithmetic checks:

- **Margin calculations:** Verify EBITDA Margin = EBITDA / Revenue, Gross Margin = Gross Profit / Revenue, etc. If the computed margin doesn't match the raw numbers, use the computation from raw components.
- **Growth rates:** Verify YoY growth = (Current − Prior) / Prior. Don't rely on pre-computed growth rates if you have the underlying values.
- **Segment totals:** If showing revenue by segment, verify segments sum to total revenue (within rounding tolerance). If they don't, omit the total row rather than publishing inconsistent math.
- **Percentage columns:** Verify "% of Total" columns sum to ~100%.
- **Valuation cross-checks:** If you show both EV and EV/Revenue, verify EV / Revenue ≈ the stated multiple.

If a validation fails: attempt recalculation from raw data. If still inconsistent, flag the metric as "N/A" rather than publishing incorrect numbers. Quiet math errors in a tear sheet destroy credibility.

**Write results** to `/tmp/tear-sheet/calculations.csv` with columns: `metric,value,formula,components`

Example rows:
```
metric,value,formula,components
gross_margin_fy2024,72.4%,gross_profit/revenue,"9524/13159"
revenue_growth_fy2024,12.3%,(current-prior)/prior,"13159/11716"
net_debt_fy2024,2150,total_debt-cash,"4200-2050"
```

### Step 3c: Verify Data Files

Before generating the document, verify that all intermediate files are present and populated.

**Read each intermediate file** via separate read operations and print a verification summary:

```
=== Tear Sheet Data Verification ===
company-profile.txt: ✓ (12 fields)
financials.csv:      ✓ (36 rows)
segments.csv:        ✓ (8 rows)
valuation.csv:       ✓ (5 rows)
calculations.csv:    ✓ (18 rows)
earnings.txt:        ✓ (populated)
relationships.txt:   ⚠ MISSING
peer-comps.csv:      ✓ (12 rows)
================================
```

**Soft gate:** If any file expected for the current audience type is missing or empty, print a warning but continue. The tear sheet handles missing data gracefully with "N/A" and section skipping. However, the warning ensures visibility into what data was lost.

**Critical rule: The files — not your memory of earlier conversation — are the single source of truth for every number in the document.** When generating the DOCX in Step 4, read values from the intermediate files. Do not rely on conversation context for financial data.

### Step 4: Format as DOCX

Read `/mnt/skills/public/docx/SKILL.md` for docx creation mechanics (docx-js via Node). Apply the Style Configuration above plus the section-specific formatting in the reference file.

**Page length defaults (user can override):**
- Equity Research: 1 page (density is the convention)
- IB / M&A: 1-2 pages
- Corp Dev: 1-2 pages
- Sales / BD: 1-2 pages

If content exceeds the target, each reference file specifies which sections to cut first.

**Output filename:** `[CompanyName]_TearSheet_[Audience]_[YYYYMMDD].docx`
Example: `Nvidia_TearSheet_CorpDev_20260220.docx`

Save to `/mnt/user-data/outputs/` and present to the user.

## Data Integrity Rules

These override everything else:
1. **S&P Global tools are the only source for financial data.** Do not fill gaps with training knowledge — it may be stale or wrong.
2. **Label what you can't find.** Use "N/A" or "Not disclosed" rather than omitting a row silently.
3. **Dates matter.** Note the fiscal year end or reporting period. Don't assume calendar year = fiscal year. Market data (stock prices, market cap) should include an "as of" date.
4. **Don't mix reporting periods.** If you have FY2023 revenue and LTM EBITDA, label them distinctly.
5. **Prefer MCP-returned fields over manual computation.** If the S&P Global tools return a pre-computed field (e.g., net debt, EBITDA, FCF), use that value directly rather than computing it from components. Only compute derived metrics manually when the tools do not return the field. This reduces discrepancies.
6. **Ensure consistency across tear sheet types.** If generating multiple tear sheets for the same company (e.g., equity research and IB/M&A in the same session), the same underlying data points must produce identical values across all outputs. Net debt, revenue, EBITDA, margins, and growth rates must match exactly. Do not re-query or re-compute independently per report — reuse the same retrieved values.
7. **Never downgrade known transaction values.** If the M&A tools return a deal value for a transaction, that value must appear in the output. Do not replace a known deal value with "Undisclosed." Use "Undisclosed" only when the tools genuinely return no value for a transaction.
8. **Use consolidated revenue as the denominator for segment percentages.** When computing "% of Total" for segment tables, divide each segment's revenue by consolidated total revenue (as reported on the income statement), not by the sum of segment revenues. The sum of segments often exceeds consolidated revenue due to intersegment eliminations. Using consolidated revenue ensures percentages align with the total revenue figure shown elsewhere in the document.
9. **Always include forward (NTM) multiples when available.** If the tools return both trailing and forward valuation multiples, both must appear in the output. Forward multiples are the primary valuation reference for equity research, IB/M&A, and corp dev audiences. Never show only trailing multiples when forward data is available.
10. **No S&P Global tool returns executive or management data.** Do not populate management names, titles, or biographical details from training data — this violates Rule 1 and produces stale information. If a management section appears in a template, omit it entirely. Ownership structure (institutional holders, insider %, PE sponsor) may be included only if returned by the tools — gate with "data permitting."

## Intermediate File Rule

All data retrieved from MCP tools must be persisted to structured intermediate files before document generation. These files — not conversation context — are the single source of truth for every number in the document.

**Setup:** At the start of Step 3, create the working directory:
```
mkdir -p /tmp/tear-sheet/
```

**Write-after-query mandate:** After each MCP query step completes, immediately write the retrieved data to the appropriate intermediate file(s). Do not wait until all queries finish. Each reference file's query plan specifies which file(s) to write after each step.

**File schemas:**

| File | Format | Columns / Structure | Used By |
|---|---|---|---|
| `/tmp/tear-sheet/company-profile.txt` | Key-value text | name, ticker, exchange, HQ, sector, industry, founded, employees, market_cap, enterprise_value, stock_price, 52wk_high, 52wk_low, shares_outstanding, beta, ownership | All |
| `/tmp/tear-sheet/financials.csv` | CSV | `period,line_item,value,source` | All |
| `/tmp/tear-sheet/segments.csv` | CSV | `period,segment_name,revenue,source` | ER, IB, CD |
| `/tmp/tear-sheet/valuation.csv` | CSV | `metric,trailing,forward,source` | ER, IB, CD |
| `/tmp/tear-sheet/consensus.csv` | CSV | `metric,fy_year,value,source` | ER |
| `/tmp/tear-sheet/earnings.txt` | Structured text | Quarter, date, key quotes, guidance, key drivers | ER, IB, Sales |
| `/tmp/tear-sheet/relationships.txt` | Structured text | Customers, suppliers, partners, competitors — each with descriptors | IB, CD, Sales |
| `/tmp/tear-sheet/peer-comps.csv` | CSV | `ticker,metric,value,source` | ER, IB, CD |
| `/tmp/tear-sheet/ma-activity.csv` | CSV | `date,target,deal_value,type,rationale,source` | IB, CD |
| `/tmp/tear-sheet/calculations.csv` | CSV | `metric,value,formula,components` | All (written in Step 3b) |

**Abbreviations:** ER = Equity Research, IB = IB/M&A, CD = Corp Dev, Sales = Sales/BD.

Not every audience type uses every file — the reference files define which query steps apply. Files not relevant to the current audience type need not be created.

**Raw values only.** Intermediate files store raw values as returned by the tools. Do not pre-compute margins, growth rates, or other derived metrics in these files — that happens in Step 3b.

**Page budget enforcement:** Each reference file specifies a default page length and a numbered cut order. If the rendered document exceeds the target, apply cuts in the order specified — do not attempt to shrink font sizes or margins below the template minimums. The cut order is a strict priority stack: cut section 1 completely before touching section 2.

## Content Quality Rules

11. **Rewrite every narrative section for the audience.** The CIQ company summary is an input, not an output. Each audience type needs a different description: concise and thesis-oriented for equity research, pitchbook prose for IB, product-focused for Corp Dev, plain language for Sales/BD. Never paste the CIQ summary verbatim into any tear sheet.
12. **Differentiate earnings highlights by audience.** The same earnings call produces different takeaways for different readers. Equity research wants segment-level performance and consensus beat/miss. IB wants margin trajectory and strategic commentary. Sales/BD wants strategic themes that create conversation angles. Do not reuse the same bullets across tear sheet types.
13. **Synthesis sections are the differentiator.** Strategic Fit Analysis, Integration Considerations, Conversation Starters, and Business Overview paragraphs are where the tear sheet earns its value. These sections require analytical reasoning that connects data points into a narrative — listing company names without context is not synthesis.
14. **Flag pending divestitures in segment tables.** If a company has announced a pending divestiture of a segment or business unit, add a footnote or parenthetical to the segment table noting the pending transaction (e.g., "Mobility* — *Pending divestiture, expected mid-2026"). For Corp Dev and IB/M&A tear sheets, include a one-line note below the segment table showing pro-forma revenue and revenue mix excluding the divested segment. This helps the reader evaluate the "go-forward" business without doing the math themselves.

### Arithmetic Validation

**→ Arithmetic validation is now enforced in Step 3b (Calculate Derived Metrics).** All margin calculations, growth rates, segment totals, percentage columns, and valuation cross-checks are validated during the dedicated calculation pass, before document generation begins. See Step 3b for the full validation checklist.
