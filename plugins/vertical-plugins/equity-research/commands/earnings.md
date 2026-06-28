---
description: Analyze quarterly earnings and create an earnings update report
argument-hint: "[company name or ticker] [quarter, e.g. Q3 2024]"
---

# Earnings Analysis Command

Create a professional equity research earnings update report analyzing quarterly results.

## Workflow

### Step 1: Gather Information

Parse the input for:
- Company name or ticker
- Quarter (e.g., Q3 2024, Q2 FY25)

If not provided, ask:
- "What company's earnings would you like to analyze?"
- "Which quarter? (e.g., Q3 2024)"

### Step 2: Verify Timeliness

**CRITICAL**: Before proceeding, verify you have the latest data:
1. Search for "[Company] latest earnings results [current year]"
2. Verify the earnings release is within the last 3 months
3. Confirm transcript date matches release date

If data is stale, inform the user and search for the latest.

### Step 3: Load Earnings Analysis Skill

Use `skill: "earnings-analysis"` to create the report:

1. **Data Collection** (search for latest):
   - Earnings release (press release)
   - 10-Q filing from SEC EDGAR
   - Earnings call transcript
   - Investor presentation/supplemental materials
   - Consensus estimates (Bloomberg/FactSet)

2. **Beat/Miss Analysis**:
   - Revenue vs consensus: Beat/Miss by $X or X%
   - EPS vs consensus: Beat/Miss by $X or X%
   - Key segment performance vs expectations
   - Explain WHY results differed

3. **Key Metrics Analysis**:
   - Revenue breakdown by segment/geography
   - Margin trends (gross, operating, net)
   - Guidance: raised/maintained/lowered
   - Updated forward estimates

4. **Generate Charts** (8-12):
   - Quarterly revenue progression
   - Quarterly EPS progression
   - Margin trends
   - Revenue by segment
   - Beat/miss summary
   - Estimate revisions
   - Valuation charts

5. **Create Report** (8-12 pages):
   - Page 1: Summary with rating and price target
   - Pages 2-3: Detailed results analysis
   - Pages 4-5: Key metrics & guidance
   - Pages 6-7: Updated investment thesis
   - Pages 8-10: Valuation & estimates
   - Sources section with clickable hyperlinks

### Step 4: Deliver Output

Provide:
1. **DOCX report** - 8-12 page earnings update
2. **Summary** highlighting:
   - Beat/miss on key metrics
   - Guidance changes
   - Thesis impact (positive/negative/neutral)

## Report Structure Reference

```
PAGE 1: EARNINGS SUMMARY
┌─────────────────────────────────────────────────────────────────┐
│ [Company] Q3 2024 Earnings Update                               │
│ Rating: BUY | Price Target: $XXX (from $XXX)                    │
├─────────────────────────────────────────────────────────────────┤
│ KEY TAKEAWAYS                                                   │
│ • Revenue beat by X% on strong [segment] performance            │
│ • EPS beat by $X.XX driven by margin expansion                  │
│ • FY guidance raised to $X.XX-$X.XX (from $X.XX-$X.XX)         │
│ • Thesis intact; maintain BUY rating                            │
├─────────────────────────────────────────────────────────────────┤
│ RESULTS SNAPSHOT                                                │
│ ┌─────────────┬──────────┬──────────┬──────────┐               │
│ │ Metric      │ Actual   │ Consensus│ Beat/Miss│               │
│ │ Revenue     │ $X.XXB   │ $X.XXB   │ +X.X%    │               │
│ │ EPS         │ $X.XX    │ $X.XX    │ +$X.XX   │               │
│ │ Gross Margin│ XX.X%    │ XX.X%    │ +XXbps   │               │
│ └─────────────┴──────────┴──────────┴──────────┘               │
└─────────────────────────────────────────────────────────────────┘

PAGES 2-3: DETAILED RESULTS
- Segment-by-segment analysis
- Geographic breakdown
- Key drivers of beat/miss

PAGES 4-5: METRICS & GUIDANCE
- Margin analysis
- Full-year guidance comparison
- Updated quarterly estimates

PAGES 6-7: THESIS UPDATE
- What's changed
- Risks and catalysts
- Investment recommendation

PAGES 8-10: VALUATION
- Updated DCF/comps if material
- Price target justification
- Scenario analysis

SOURCES SECTION (with clickable hyperlinks):
- Earnings Release: [hyperlink]
- Form 10-Q: [EDGAR hyperlink]
- Earnings Call Transcript: [hyperlink]
- Consensus estimates: Bloomberg as of [date]
```

## Quality Checklist

Before delivery:
- [ ] Earnings data is from latest quarter (not stale)
- [ ] Beat/miss quantified with specific numbers
- [ ] All charts embedded (8-12 total)
- [ ] Sources section with clickable hyperlinks
- [ ] Every figure/table has source citation
- [ ] Guidance changes clearly documented
- [ ] Rating and price target stated upfront
- [ ] 8-12 pages, 3,000-5,000 words
