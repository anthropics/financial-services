# Content Mapping Reference

This file provides guidance for mapping source data to pitch deck template sections. The process is template-agnostic—these principles apply regardless of the specific template design.

## Contents

- [Template Analysis Process](#template-analysis-process)
- [Content Mapping Workflow](#content-mapping-workflow)
- [Common Slide Types and Data Requirements](#common-slide-types-and-data-requirements)
- [Mapping Verification Checklist](#mapping-verification-checklist)
- [Handling Data-Template Mismatches](#handling-data-template-mismatches)
- [Template-Specific Adaptation](#template-specific-adaptation)

---

## Template Analysis Process

Before populating any template, analyze its structure:

### Step 1: Identify All Content Areas

Scan each slide for:
- **Title/header placeholders** — Where slide titles go
- **Subtitle/definition areas** — Secondary headers or definitions
- **Content boxes** — Main content areas (may have label sidebars)
- **Table placeholders** — Areas designated for tabular data
- **Chart/visual areas** — Spaces for charts, diagrams, or images
- **Metric callout boxes** — Highlighted key figures
- **Footnote/source bars** — Bottom areas for citations and notes
- **Logo placeholder** — Usually top-right corner

### Step 2: Note Template Conventions

Each template has its own style. Observe:
- **Color scheme** — What colors are used for headers, backgrounds, accents?
- **Font choices** — What fonts and sizes are already set?
- **Box styling** — Do content boxes have sidebars, borders, or shading?
- **Bullet styles** — What bullet symbols does the template use?
- **Alignment patterns** — How are parallel sections aligned?

### Step 3: Identify Instruction vs. Output Areas

Templates often include guidance:
- **Instruction boxes** — Colored boxes with guidance text (often yellow background, white text)
- **Placeholder text** — Text in [brackets] indicating what to replace
- **Example content** — Sample content showing expected format

**Key distinction**: Instruction boxes tell you what to do; they should be reformatted or removed in final output. Output areas are where your content goes.

---

## Content Mapping Workflow

### Step 1: Inventory Source Data

Create a list of all available data:
- Market size figures and ranges
- Growth rates (CAGR, YoY)
- Company names and descriptions
- Segment definitions
- Financial metrics
- Source citations and dates
- Footnote content

### Step 2: Match Data to Template Sections

For each template section, identify:

| Template Section | Required Data | Source Location |
|------------------|---------------|-----------------|
| [Section name] | [Data needed] | [Where to find it] |

### Step 3: Identify Gaps

After mapping, note:
- **Missing data** — Template requires data not in sources
- **Extra data** — Sources contain data with no template home
- **Format mismatches** — Data exists but in wrong format

### Step 4: Resolve Gaps Before Populating

- Missing data: Flag for user or search for additional sources
- Extra data: Confirm if it should be excluded or if template needs adjustment
- Format mismatches: Transform data to required format

---

## Common Slide Types and Data Requirements

These are typical data requirements for common slide types. Your specific template may vary—always follow the template's actual structure.

### Market Definition Slides

**Typical content areas:**
- Segments included in scope (with examples/key players)
- Segments excluded from scope (with examples)
- Market definition text
- Scope rationale/justification

**Data mapping considerations:**
- Source data should clearly distinguish included vs. excluded segments
- Key players should be mapped to their respective segments
- Definition text should align with how sources define the market

**Data typically needed:**
- List of market segments to include (with key player examples)
- List of market segments to exclude (with examples)
- Market definition text
- Scope rationale or justification

**Formatting principle:** Parallel sections (included vs. excluded) should use matching formatting.

**Verification questions:**
- Does every segment have the appropriate symbol (✓ for included, × for excluded)?
- Are key players correctly assigned to segments?
- Does the definition match the source methodology?

### Market Sizing / TAM Slides

**Typical content areas:**
- Current market size (with year)
- Growth rate (CAGR with period)
- Future projection (with target year)
- Source-by-source breakdown table
- Consensus/summary figures
- Key takeaways or insights

**Data typically needed:**
- Market size figures with base year
- Growth rates (CAGR with time period)
- Projection figures with target year
- Source citations for each data point

**Example column headers:** Source | [Base Year] Size | CAGR | [Target Year] Projection

**Formatting principle:** If showing multiple sources, include a consensus/summary row.

**Data mapping considerations:**
- Multiple sources may have different estimates—map each to table rows
- Consensus figures require calculation from individual sources
- Projections should be verifiable using CAGR formula

**Verification questions:**
- Do all source figures match original documents?
- Is the consensus calculated correctly (not just copied from one source)?
- Are projection years consistent across all figures?
- Do CAGR-based projections match when manually verified?

### Competitive Landscape Slides

**Typical content areas:**
- Comparison table with competitors as columns
- Feature/capability rows
- Financial metric rows (revenue, growth, market share)
- Key observations or positioning notes

**Data typically needed:**
- List of competitors to compare
- Features or capabilities for each
- Financial metrics (revenue, growth, market share) if available
- Time period for financial data

**Formatting principle:** Subject company should be visually distinguished from competitors (e.g., bold text, different background color, border, or positioned in rightmost column).

**Data mapping considerations:**
- Ensure all competitors from source data are included
- Feature comparisons should use consistent criteria
- Financial figures should be from comparable periods

**Verification questions:**
- Are all competitors from the source data represented?
- Is the subject company visually distinguished?
- Are financial figures from the same time period?
- Is the ✓/× usage consistent and accurate?

### Financial Summary Slides

**Typical content areas:**
- Key metric callouts (headline figures)
- Historical financials table (actuals)
- Projected financials table (estimates)
- Growth rates and margins
- Optional trend charts

**Data typically needed:**
- Historical financials (actuals) for recent years
- Projected financials (estimates) for future years
- Key metrics: Revenue, Growth %, Margins, EBITDA

**Example column headers:** Metric | FY[Year-2] | FY[Year-1] | FY[Year]A | FY[Year+1]E | FY[Year+2]E

**Formatting principle:** Clearly distinguish historical (A) from projected (E) data.

**Data mapping considerations:**
- Clearly distinguish historical (A) from projected (E) data
- Ensure metric definitions match source (Revenue vs. Net Revenue, EBITDA vs. Adjusted EBITDA)
- Growth rates should be calculated consistently

**Verification questions:**
- Are historical vs. projected periods clearly labeled?
- Do calculated growth rates match source or manual calculation?
- Are metric definitions consistent with source documents?

### Transaction Comparables Slides

**Typical content areas:**
- Transaction table (date, target, acquirer, deal value)
- Valuation multiples (EV/Revenue, EV/EBITDA)
- Summary statistics (mean, median, high, low)
- Implied valuation for subject company

**Data typically needed:**
- Transaction details: Date, Target, Acquirer, Deal Value
- Valuation multiples: EV/Revenue, EV/EBITDA
- Subject company metrics for implied valuation

**Formatting principle:** Include summary statistics (Mean, Median, High, Low) for multiples.

**Data mapping considerations:**
- Multiples should be calculated from transaction data, not just copied
- Summary statistics require calculation across all transactions
- Implied valuation applies multiples to subject company metrics

**Verification questions:**
- Are all relevant transactions from the source included?
- Are multiples calculated correctly (EV ÷ Metric)?
- Do summary statistics cover all transactions in the table?
- Is implied valuation clearly labeled as illustrative?

---

## Mapping Verification Checklist

Before moving to formatting, verify mapping completeness:

### Data Completeness
- [ ] Every template placeholder has mapped source data
- [ ] All source citations are recorded for footnotes
- [ ] No placeholder [brackets] remain unmapped

### Data Accuracy
- [ ] Figures match original source documents exactly
- [ ] Years and time periods are correctly noted
- [ ] Company names are spelled correctly
- [ ] Calculated values (consensus, projections, multiples) verified

### Logical Consistency
- [ ] Included vs. excluded segments are logically coherent
- [ ] Historical data precedes projected data chronologically
- [ ] Comparison data uses consistent time periods
- [ ] Totals and subtotals sum correctly

### Source Attribution
- [ ] Every data point can be traced to a source
- [ ] Source names and publication years recorded
- [ ] Footnote numbers assigned for special notes

---

## Handling Data-Template Mismatches

### Template Requires More Data Than Available

**Options:**
1. Flag the gap explicitly for user review
2. Mark section as "Data not available" with explanation
3. Search for additional sources if appropriate
4. Recommend template adjustment if data doesn't exist

**Do not:** Fabricate data or make unsupported estimates.

### Source Has More Data Than Template Accommodates

**Options:**
1. Include most relevant/recent data points
2. Summarize or aggregate where appropriate
3. Add footnotes referencing additional available data
4. Recommend template expansion if data is critical

### Data Format Doesn't Match Template Format

**Common transformations:**
- Individual figures → Range (use min-max from sources)
- Detailed breakdown → Summary category
- Annual figures → CAGR (calculate from endpoints)
- Absolute values → Percentages (calculate share)
- Multiple sources → Consensus (apply methodology)

### Template Uses Different Terminology

**Resolution process:**
1. Identify template term and source term
2. Confirm they refer to the same concept
3. Use template terminology in output
4. Add footnote if clarification needed

---

## Template-Specific Adaptation

Remember: This guidance describes common patterns, not requirements. Always:

1. **Follow the template** — If template uses different section names, use those
2. **Match template style** — Use template's existing fonts, colors, bullet styles
3. **Preserve template structure** — Don't rearrange sections unless necessary
4. **Respect template spacing** — Content should fit designated areas without overflow

The goal is to populate the template as designed, not to redesign it.
