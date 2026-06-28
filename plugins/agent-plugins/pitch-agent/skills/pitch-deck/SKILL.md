---
name: pitch-deck
description: "Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has source data (Excel/CSV) to populate into slides, user mentions populating or filling a pitch deck template, or user needs to transfer data into existing slide layouts. Not for creating presentations from scratch."
---

# Populating Investment Banking Pitch Deck Templates

## Reference Files

**Read all reference files at task start before beginning any work.** These contain critical patterns and anti-patterns that will affect your approach. Do not wait until you encounter issues.

| File | Purpose |
|------|---------|
| [`formatting-standards.md`](reference/formatting-standards.md) | Text, bullets, tables, charts, alignment |
| [`slide-templates.md`](reference/slide-templates.md) | Content mapping guidance for common slide types |
| [`xml-reference.md`](reference/xml-reference.md) | PowerPoint XML patterns for tables, shapes, arrows |
| [`calculation-standards.md`](reference/calculation-standards.md) | Financial formulas for verification (CAGR, consensus) |

---

## Workflow Decision Tree

**What type of task is this?**

```
┌─ Populating empty template with source data?
│  └─→ Follow "Template Population Workflow" below
│
├─ Editing existing populated slides?
│  └─→ Extract current content, modify, revalidate
│
└─ Fixing formatting issues on existing slides?
   └─→ See "Common Failures" table, apply targeted fixes
```

---

## ⚠️ Critical Rendering Limitation

**LibreOffice is used for validation but DOES NOT render PowerPoint files accurately.** It will mangle fonts, gradients, shape positions, text wrapping, and some table formatting.

**What this means:** A slide that passes visual validation in LibreOffice may still have issues in Microsoft PowerPoint. The validation loop catches structural issues (missing content, broken tables, placeholder formatting retained) but **cannot** catch font substitution, subtle alignment shifts, or gradient problems.

**Required action:** Always include this statement when delivering output:
> "This file was validated using LibreOffice. Please review in Microsoft PowerPoint before distribution, as rendering differences may exist."

---

## Template Population Workflow

Copy and track progress:

```
Pitch Deck Progress:
- [ ] Phase 1: Extract and validate source data
- [ ] Phase 2: Map content to template sections
- [ ] Phase 3: Populate slides with proper formatting
- [ ] Phase 4: Validate → Fix → Repeat until clean
- [ ] Phase 5: Final verification
```

### Phase 1: Data Extraction
1. **Create backup** of original template before any modifications — copy to `[filename]_backup.pptx`. Direct XML editing or unexpected errors can corrupt files.
2. Identify all source materials (Excel, CSV, PDF reports, Word documents, databases, web sources)
3. Extract relevant data points from each source
4. Validate all numbers against original sources
5. Standardize units and currency (convert all figures to the primary unit/currency used in the template)
6. Note any calculations that need verification → see [`calculation-standards.md`](reference/calculation-standards.md) for formulas

### Phase 2: Content Mapping
1. **Open and visually review the template** — understand its structure, style, and existing content before modifying
2. Analyze template structure — identify all placeholder areas and content boxes
3. Map source data to corresponding template sections → see [`slide-templates.md`](reference/slide-templates.md) for mapping guidance
4. Identify placeholder guidance boxes (colored instruction boxes from task creator)
5. Note any data gaps or mismatches → see [`slide-templates.md`](reference/slide-templates.md#handling-data-template-mismatches) for resolution

### Phase 3: Template Population
1. **Remove or reformat placeholder boxes** — colored instruction boxes show WHAT to create, not HOW to format. Delete them and create properly formatted content in their place. See [Critical Anti-Patterns](#critical-anti-patterns-never-do-these).
2. Populate each section with mapped content (focus on content first)
3. **Then apply formatting** to match template style → see [`formatting-standards.md`](reference/formatting-standards.md)
4. Create tables as actual table objects (NEVER use pipe/tab-separated text) → see [`xml-reference.md`](reference/xml-reference.md#table-implementation)
5. Create arrows/shapes as PowerPoint objects → see [`xml-reference.md`](reference/xml-reference.md#arrow-shapes)
6. Insert company logo if provided in task files; if not available, flag to user: "[LOGO NOT PROVIDED - please supply company logo]"

### Phase 4: Validate → Fix → Repeat

**This is a feedback loop. Repeat until all checks pass OR escalation is triggered.**

```bash
# Convert to images for visual validation
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
```

**Validation checklist (check each slide image):**
- [ ] Text readable against background?
- [ ] Tables are actual objects (columns aligned, NOT pipe/tab-separated text)?
- [ ] Charts/tables fill designated areas?
- [ ] Bullet formatting consistent within sections?
- [ ] Font sizes match across same-level boxes?
- [ ] No content beyond slide boundaries?
- [ ] **No placeholder formatting retained** (no large colored boxes with data dumped in)?
- [ ] **No text-based "tables"** (no `|` or tab separators creating fake columns)?
- [ ] **Cross-slide consistency**: Same metrics/figures identical across all slides where they appear?

**Fix cycle protocol:**

| Cycle | Action |
|-------|--------|
| 1 | Fix all identified issues, re-validate |
| 2 | Fix remaining issues, re-validate |
| 3 | If issues persist, document remaining problems and escalate to user |

**After 3 cycles, if issues remain:**
1. List each unresolved issue with slide number and description
2. Explain what was attempted
3. Deliver the file with explicit disclaimer: "The following issues could not be resolved automatically: [list]. Manual review required."

**Do not** continue cycling indefinitely. Some issues (font rendering, complex shape alignment) may require manual intervention in PowerPoint.

### Phase 5: Final Verification

Run through the [Final Quality Checklist](#final-quality-checklist) before delivering.

---

## Quick Reference Tables

### Bullet Symbols

| Context | Symbol | Usage |
|---------|--------|-------|
| Included/Positive | ✓ | Items within scope, features present |
| Excluded/Negative | × | Items outside scope, features absent |
| Neutral list | • | General enumeration, commentary |
| Numbered sequence | 1. 2. 3. | Process steps, rankings |
| Sub-bullets | – | Secondary points under main bullets |

### Slide Hierarchy Levels (Typical)

These are typical ranges—adjust based on template specifications:

| Level | Examples | Typical Size | Style |
|-------|----------|--------------|-------|
| Title | Slide title | 40-48pt | Bold |
| Subtitle | Market definition, slide descriptor | 18-22pt | Bold |
| Section Header | "Key Projections", "Commentary" | 14-16pt | Regular |
| Block Label | "Segments Included", "Definition" sidebar | 12-14pt | Regular |
| Block Content | Bullet points, body text | 11-14pt | Regular |
| Table Header | Column headers | 10-12pt | Bold |
| Table Body | Cell content | 9-11pt | Regular |
| Footnotes | Sources, notes | 8-9pt | Italic |

### Font Consistency Matching

Boxes at the **same hierarchy level** MUST use identical font sizes:

| Same Level | Must Match With |
|------------|-----------------|
| "Segments Included" | "Segments Excluded" |
| "Definition" | "Scope Rationale" |
| Left column bullets | Right column bullets |
| All block labels | Each other |
| All section headers | Each other |

### Rounding for Presentation

These are **typical conventions** — adjust based on the magnitude of values and template style:

| Value Type | Typical Rounding | Example |
|------------|------------------|---------|
| Large market sizes ($10bn+) | Nearest $1bn | 18.5 → $19bn |
| Smaller market sizes (<$10bn) | Nearest $0.5bn or $0.1bn | 2.3 → $2.5bn |
| Size ranges | Match precision of sources | 14.9-22.1 → $15-22bn |
| CAGR | Whole % or 0.5% | 16.4% → 16% or 16.5% |
| Market share | Nearest 5% or match source | 21.4% → 20% |
| Multiples | 1 decimal | 9.69 → 9.7x |

**Principle:** Rounding should not materially change the figure. For smaller values, use finer precision.

### Text Density Rules

- Max 6-7 bullets per content box
- Max 2 lines per bullet point
- Parenthetical examples: same line or indented below
- No orphan words (single word on new line)

### Alignment Principles

**Vertically stacked boxes** must have identical:
- Left margin position, bullet indentation, text start position, box width

**Horizontally adjacent boxes** must have identical:
- Top position, height (where possible), internal padding

### Multi-Slide Consistency

When the same data appears on multiple slides:
- Use identical figures, formatting, and terminology
- If a metric is updated on one slide, update all occurrences
- Cross-reference during validation to catch mismatches

---

## MUST Requirements

These requirements are non-negotiable regardless of template:

| Requirement | Details |
|-------------|---------|
| **Text Readability** | All text MUST have sufficient contrast with background. Examples: white/light text on dark blue, dark green, black backgrounds; black/dark text on white, light gray, light yellow backgrounds. |
| **Actual Table Objects** | Tabular data MUST be table objects, not tab-separated text. See [`xml-reference.md`](reference/xml-reference.md#table-implementation). |
| **Proper Chart/Table Sizing** | Pasted visuals MUST fill designated area. See [`formatting-standards.md`](reference/formatting-standards.md#chart-and-image-handling). |
| **Consistent Formatting** | Bullets within section MUST match (symbol, size, indent). Same-level boxes MUST use same font size. |
| **Content Boundaries** | All content MUST stay within slide edges. Footnote box width: ~32.5cm for 16:9, ~24cm for 4:3. |
| **No Placeholder Formatting** | Remove colored instruction boxes. Main body: dark text on light background per template. |

---

## Critical Anti-Patterns: NEVER DO THESE

These failures occur when placeholder formatting is mistaken for output formatting. Recognizing these patterns is essential.

### Anti-Pattern 1: Populating Data INTO Placeholder Boxes

**What happens:** Template has colored instruction boxes (yellow, orange, etc.) with guidance text. Model replaces the guidance text with actual data BUT KEEPS THE COLORED BOX.

**Why it's wrong:** The colored box IS the placeholder. It tells you what content goes there. The output should have different formatting — typically dark text on white/light background, or properly styled shapes.

**Recognition test:** If your populated slide has large colored rectangles filled with data text, you have copied the placeholder format instead of replacing it.

**Critical distinction — two types of "placeholders":**

| Type | How to identify | What to do |
|------|-----------------|------------|
| **Instruction boxes** | Bright colors (yellow, orange), contains guidance text like "Insert X here", white/light text on colored background | DELETE the entire shape, then create new content with production formatting |
| **Layout placeholders** | Part of slide master/layout, neutral colors matching template theme, "Click to add text" | KEEP the shape, REPLACE the text content only |

If uncertain: check if the shape exists on an empty slide from the same template. Layout placeholders persist; instruction boxes are regular shapes.

### Anti-Pattern 2: Text-Based "Tables"

**What happens:** Model creates table-like content using separator characters (`|`, tabs, spaces) instead of actual table objects.

**Why it's wrong:** This is NOT a table. Columns will never align properly, it cannot be formatted consistently, and it looks unprofessional.

**Recognition test:** If you're typing `|` characters or relying on spaces/tabs to create columns, you're creating text, not a table.

**MUST verify:** After creating any table, verify it is an actual table object. See [`xml-reference.md`](reference/xml-reference.md#critical-verify-tables-are-actual-table-objects) for verification methods.

### Anti-Pattern 3: Inheriting Placeholder Contrast

**What happens:** Placeholder uses light text on colored background (e.g., white on yellow). Model populates data but keeps this color scheme, resulting in hard-to-read output.

**Why it's wrong:** Placeholder colors are deliberately distinct to signal "replace me." Production slides typically use dark text on light backgrounds for body content.

**Recognition test:** If your populated content has light/white text on bright colored backgrounds in body areas (not headers), you've inherited placeholder formatting.

**Correct approach:** Apply production formatting — typically dark text (#000000 or #333333) on white or light backgrounds for body content. Headers and accent areas may use brand colors.

### Summary: Placeholder vs. Production

| Element | Placeholder (Input) | Production (Output) |
|---------|---------------------|---------------------|
| Instruction boxes | Colored background, guidance text | Removed or reformatted |
| Data areas | "[Insert data here]" text | Actual data with clean formatting |
| Tables | Description of what table should contain | Actual table object with rows/columns |
| Body text | Light text on colored background | Dark text on light background |

**The placeholder tells you WHAT to create, not HOW to format it.**

---

## Common Failures

For detailed explanations of the most critical failures, see [Critical Anti-Patterns](#critical-anti-patterns-never-do-these) above.

| Failure | Solution | Reference |
|---------|----------|-----------|
| Unstructured text dumps | Break into bullets (✓, ×, •) | [`formatting-standards.md`](reference/formatting-standards.md#bullet-point-structure) |
| Pipe/tab-separated "tables" | Create actual table objects — text with separators is NOT a table | [`xml-reference.md`](reference/xml-reference.md#table-implementation) |
| Poor text/background contrast | Audit every text element | — |
| Tiny pasted charts | Resize to fill area, paste chart only | [`formatting-standards.md`](reference/formatting-standards.md#proper-sizing-workflow) |
| Source data pasted with charts | Select only chart object before copy | — |
| Data dumped into placeholder boxes | Delete colored instruction boxes, create new properly formatted content | [Anti-Patterns](#critical-anti-patterns-never-do-these) |
| Inconsistent bullets | Define style once, apply to all | [`formatting-standards.md`](reference/formatting-standards.md#bullet-consistency) |
| Inconsistent fonts across boxes | Standardize same-level boxes | [`formatting-standards.md`](reference/formatting-standards.md#font-consistency) |
| Content overflow | Set explicit box widths (footnotes: 32.5cm for 16:9, 24cm for 4:3) | — |
| Missing logo | Use logo from task files; if not provided, flag to user | — |
| Remaining `[brackets]` | Search and replace all placeholders | — |
| Text arrows (→, ⟹) | Use PowerPoint shape objects | [`xml-reference.md`](reference/xml-reference.md#arrow-shapes) |

---

## Error Handling

**If PDF/image conversion fails:**
1. Check LibreOffice is installed: `which soffice`
2. Try alternative: `libreoffice --headless --convert-to pdf presentation.pptx`
3. If still failing, open in PowerPoint/LibreOffice manually and export

**If source data has inconsistencies or conflicts:**
1. **Priority order**: Use data explicitly provided in the task files first
2. If using data from other sources (web search, external documents), flag this to the user
3. Document any discrepancies explicitly
4. Add footnote explaining data source choice

**If calculations don't match source projections:**
1. Show your calculation methodology
2. Note the discrepancy and possible causes (different base year, methodology)
3. Present both values if material difference
4. Flag to user for resolution

---

## Table Structure Guidelines

When creating tables (MUST be actual table objects):

**Column Alignment:**
- Text columns: Left-aligned (header and content)
- Numeric columns: Right-aligned or center-aligned (header matches content)

**Header Row:**
- Bold text
- Shaded background (template's brand color)
- White or contrasting text

**Consensus/Total Row:**
- Bold text
- Separator line above
- Distinct background shading

**Width:** Fill designated section width completely.

For XML implementation, see [`xml-reference.md`](reference/xml-reference.md#table-implementation).

---

## Footnote Format

**Format:**
```
Sources: [Source 1] (Year), [Source 2] (Year).
Notes: (1) [First note]; (2) [Second note].
```

**Example:**
```
Sources: Grand View Research (2024), Mordor Intelligence (2024), Markets and Markets (2023).
Notes: (1) Excludes hardware revenue; (2) Includes both B2B and B2C segments.
```

All superscript numbers (¹, ², ³) in slide body MUST have corresponding Notes entries.

---

## Logo Placement

- Use logo file provided in task materials
- If no logo provided, flag to user: "[LOGO NOT PROVIDED - please supply company logo]"
- Position: typically top-right, consistent size across slides, must not overlap content

---

## Data Requirements by Slide Type

For detailed data requirements, formatting principles, and example column headers for each slide type, see [`slide-templates.md`](reference/slide-templates.md#common-slide-types-and-data-requirements).

Common slide types covered: Market Definition, Market Sizing/TAM, Competitive Landscape, Financial Summary, Transaction Comparables.

---

## Final Quality Checklist

Before delivering the populated template, verify:

### Data Accuracy
- [ ] All figures match original source documents
- [ ] Calculated values verified against formulas (see [`calculation-standards.md`](reference/calculation-standards.md))
- [ ] Years and time periods are correct
- [ ] Company/competitor names spelled correctly
- [ ] Same figures are identical across all slides where they appear

### Content Mapping
- [ ] Every template section populated with appropriate data
- [ ] No `[bracket]` placeholder text remaining
- [ ] All source citations included in footnotes
- [ ] Footnote numbers (¹²³) have corresponding Notes entries

### Formatting
- [ ] Text readable against all backgrounds (sufficient contrast)
- [ ] Tables are actual table objects (NOT pipe/tab-separated text)
- [ ] Charts/tables fill designated areas (no thumbnails)
- [ ] Bullet formatting consistent within each section
- [ ] Font sizes match across same-level boxes
- [ ] No content extends beyond slide boundaries
- [ ] No placeholder boxes retained with data dumped inside
- [ ] No colored instruction boxes in final output

### Template Compliance
- [ ] Placeholder instruction boxes reformatted or removed
- [ ] Formatting matches template style (colors, fonts)
- [ ] Logo present and correctly positioned
- [ ] Production formatting applied (dark text on light background for main content)

### Final Step
- [ ] Recommend user validate in Microsoft PowerPoint before distribution (LibreOffice may render differently)
