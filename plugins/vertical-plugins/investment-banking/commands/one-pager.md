---
description: Create a one-page company strip profile using branded PPT template
argument-hint: "[company name or ticker]"
---

# One-Pager Strip Profile Command

Create a professional one-page company strip profile for pitch books and deal materials.

## Workflow

### Step 1: Gather Company Information

If a company name or ticker is provided, use it. Otherwise ask:
- "What company would you like to profile?"

### Step 2: Check for Available PPT Template Skills

**First, check for existing ppt-template skills** in the skills directory:

```bash
ls skills/ | grep -E "ppt-template|brand-guidelines"
```

If template skills exist (e.g., `techcorp-ppt-template`, `gs-brand-guidelines`):
1. List available templates to the user
2. Ask which template to use, or if they want a clean professional format
3. Load the selected template skill with `skill: "[template-name]"`

If no template skills exist, ask:
- "Do you have a branded PowerPoint template file to use? If so, provide the path. Otherwise I'll use a clean professional format."

If a template file is provided:
1. Analyze the template structure to understand layouts
2. Use appropriate layout for one-pager content

### Step 3: Load Strip Profile Skill

Use `skill: "strip-profile"` to execute the profile creation:

1. **Clarify requirements**:
   - Confirm single-slide format (one-pager)
   - Ask about any specific focus areas

2. **Research company data**:
   - Company overview (HQ, founded, employees, leadership)
   - Business description and positioning
   - Key financials (Revenue, EBITDA, margins, growth)
   - Valuation metrics (Market Cap, EV, multiples)
   - Recent developments and news
   - Top shareholders (for public companies)

3. **Create the strip profile**:
   - Use 4:3 aspect ratio (10" x 7.5")
   - 4-quadrant layout:
     - Top-left: Company Overview (bullets)
     - Top-right: Business & Positioning (bullets)
     - Bottom-left: Key Financials (table)
     - Bottom-right: Stock chart + Shareholders OR Recent News
   - Apply company brand colors
   - Include accent bars on section headers

### Step 4: Visual Review

After creating the slide:
1. Convert to image for review
2. Check for text overlap/cutoff issues
3. Verify all data is populated (no placeholders)
4. Show preview to user for approval

### Step 5: Deliver Output

Provide:
1. **PowerPoint file** (.pptx) - the one-pager
2. **Image preview** - for quick review
3. **Summary** of key data points included

## One-Pager Layout Reference

```
┌─────────────────────────────────────────────────────────────────┐
│ Company Name (TICKER)                                    [Logo] │
├────────────────────────────┬────────────────────────────────────┤
│ COMPANY OVERVIEW           │ BUSINESS & POSITIONING             │
│ • HQ, Founded, Employees   │ • Core business description        │
│ • CEO, CFO                 │ • Key products/services            │
│ • Market cap, industry     │ • Competitive positioning          │
│ • Key stats                │ • Growth drivers                   │
├────────────────────────────┼────────────────────────────────────┤
│ KEY FINANCIALS             │ STOCK PERFORMANCE / OWNERSHIP      │
│ ┌──────────────────────┐   │ [1Y Stock Chart]                   │
│ │ Metric │ FY24 │ FY25E│   │                                    │
│ │ Rev    │ $XXB │ $XXB │   │ Top Shareholders:                  │
│ │ EBITDA │ $XXB │ $XXB │   │ • Vanguard: X.X%                   │
│ │ Margin │ XX%  │ XX%  │   │ • BlackRock: X.X%                  │
│ │ EV/EBITDA │ XXx │ XXx │   │ • State Street: X.X%              │
│ └──────────────────────┘   │                                    │
└────────────────────────────┴────────────────────────────────────┘
Source: Company filings, FactSet
```

## Quality Checklist

Before delivery:
- [ ] All 4 quadrants populated with real data
- [ ] No placeholder text remaining
- [ ] Company brand colors applied
- [ ] Accent bars on all section headers
- [ ] Financial table properly formatted
- [ ] Sources cited at bottom
- [ ] No text overflow or cutoff
- [ ] Investment banking quality (GS/MS/JPM standard)
