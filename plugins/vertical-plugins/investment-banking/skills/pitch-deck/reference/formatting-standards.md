# Formatting Standards Reference

This reference file contains general PowerPoint formatting guidance for pitch deck creation. These are best practices that should be adapted to the specific template being used.

---

## Table of Contents

1. [Visual Hierarchy and Layout](#visual-hierarchy-and-layout)
2. [Text Formatting](#text-formatting)
3. [Table Creation](#table-creation)
4. [Chart and Image Handling](#chart-and-image-handling)
5. [Data Visualization](#data-visualization)
6. [Font Consistency](#font-consistency)
7. [Template Adaptation](#template-adaptation)

---

## Visual Hierarchy and Layout

### Box and Section Layout

Slide layouts vary based on content requirements and template design. Common elements include:
- Header sections with titles and subtitles
- Content boxes with label sidebars
- Tables for structured data
- Charts for visual data representation
- Footnote bars at slide bottom

The specific layout should follow the template provided. Common content types and their typical structures:
- **Market definition slides**: Label boxes with bullet content + commentary sections
- **TAM/sizing slides**: Metrics callouts + data tables + key takeaways
- **Competitive analysis**: Comparison tables or matrices
- **Financial summaries**: Charts with supporting data tables

### Alignment Principles

**Vertical alignment of parallel sections:**

Boxes that are vertically stacked should have consistent:
- Left margin position
- Bullet indentation
- Text start position
- Box width

Boxes that are horizontally adjacent should have consistent:
- Top position
- Height (where content allows)
- Internal padding

---

## Text Formatting

### Bullet Point Structure

Avoid unstructured text dumps. Break content into scannable bullet points.

**Illustrative Correct Structure:**
```
✓  Consumer mobile and web language learning apps
   (Duolingo, Babbel, Memrise, Busuu)
✓  B2B enterprise language training platforms
   (goFLUENT, Speexx, Learnship)
✓  Online tutoring marketplaces
   (italki, Preply, Cambly)
```

**Illustrative Incorrect Structure (Text Dump):**
```
Consumer mobile/web apps (Duolingo, Babbel, Memrise, Busuu)
B2B enterprise platforms (Speexx, Rosetta Stone Enterprise)
Online tutoring marketplaces (Preply, italki, Cambly)
```

### Bullet Symbol Guidelines

| Context | Symbol | Usage |
|---------|--------|-------|
| Included/Positive | ✓ (checkmark) | Items within scope, features present |
| Excluded/Negative | × (cross) | Items outside scope, features absent |
| Neutral list | • (bullet) | General enumeration, commentary |
| Numbered sequence | 1. 2. 3. | Process steps, rankings |
| Sub-bullets | ‣ or – | Secondary points under main bullets |

Adapt symbol usage to match the template's existing conventions.

### Bullet Consistency

All bullets within a box/section should have identical formatting:
- Same bullet symbol throughout the box (unless intentionally differentiated)
- Same indent level for all primary bullets
- Same bullet size
- Same spacing between bullet and text
- Same font size for all bullet text at same level

### Font Size Guidelines

These are typical ranges - adjust based on template specifications:

| Element | Typical Size (pt) | Style |
|---------|-------------------|-------|
| Slide Title | 40-48 | Bold |
| Subtitle/Definition | 18-22 | Bold |
| Section Headers | 14-16 | Regular |
| Body Text/Bullets | 12-14 | Regular |
| Table Headers | 10-12 | Bold |
| Table Body | 9-11 | Regular |
| Footnotes | 8-9 | Italic |

### Text Density Guidelines

- **Maximum 6-7 bullets** per content box (adjust based on space)
- **Maximum 2 lines** per bullet point
- **Parenthetical examples** on same line or indented below
- **Avoid orphan words** - adjust line breaks to avoid single words on new lines

---

## Table Creation

### CRITICAL: Use Actual Table Objects

**Tables must be actual table objects, NOT text with tab spacing.**

Text with tabs will never align properly and looks unprofessional. Always create proper table objects.

### Table Structure Guidelines

1. **Column alignment**:
   - Text columns: Left-aligned (both header and content)
   - Numeric columns: Center-aligned or right-aligned
   - Headers should align with their column content

2. **Header row**:
   - Bold text
   - Shaded background (use template's brand color)
   - Contrasting text color for readability
   - Alignment matches column content alignment

3. **Alternating rows** (optional):
   - Light shading on alternate rows improves readability

4. **Summary/Total row**:
   - Bold text
   - Heavier top border (separator line)
   - Distinct background shading

5. **Table width**:
   - Fill the designated section width
   - Avoid tables floating in white space

### For XML implementation patterns, see [`xml-reference.md`](xml-reference.md#table-implementation)

---

## Chart and Image Handling

### Pasting Charts from Excel

When pasting charts from Excel:

1. **Paste the chart ONLY** - do not include source data tables
2. **Resize to fill the designated area** - charts should not appear as tiny thumbnails
3. **Maintain aspect ratio** - do not distort the chart
4. **Verify readability** - axis labels, legends, data labels must be legible

### Pasting Tables from Excel

When pasting tables from Excel:

1. **Paste the formatted table ONLY** - exclude any source data or calculations
2. **Resize to fill the designated area** - table should occupy its full section
3. **Verify column widths** - adjust so text is not truncated
4. **Check formatting preservation** - colors, borders, fonts may need adjustment

### Size Guidelines

**Minimum sizing principles:**
- Charts: Should occupy a substantial portion of their designated area
- Tables: Fill the designated section width completely
- Images: Sized appropriately for context, never thumbnail-sized

**Indicators of undersized visuals (avoid these):**
- Chart occupies small fraction of available space
- Text labels are unreadable
- Large empty areas surrounding the visual
- Visual appears as a "thumbnail"

### Proper Sizing Workflow

1. Identify the target area dimensions
2. Paste the chart/table
3. Immediately resize to fill the target area
4. Verify all text remains readable
5. Adjust internal elements if needed (legend position, axis labels)

---

## Data Visualization

### Key Metrics Display

When displaying key metrics (e.g., TAM, CAGR, projections), consider showing relationships between values rather than listing them statically:

- **Visual flow indicators**: Shapes (arrows, chevrons, connectors) showing progression
- **Size hierarchy**: Larger font for primary metrics, smaller for labels
- **Spatial arrangement**: Position elements to show logical flow

### Arrow and Flow Indicators

If using arrows or flow indicators:
- Use PowerPoint shape objects, not text characters
- Do not use text-based arrows (→, ⟹) in the final presentation
- Create arrows using PowerPoint's shape tools or via XML shape elements

**For XML implementation, see [`xml-reference.md`](xml-reference.md#arrow-shapes)**

---

## Font Consistency

### Cross-Box Font Consistency

All text boxes at the same hierarchy level should use identical font sizes.

**Same-level boxes that should match:**

| Box Type | Should Match With |
|----------|-------------------|
| "Segments Included" content | "Segments Excluded" content |
| "Definition" content | "Scope Rationale" content |
| Left column bullets | Right column bullets |
| All label boxes | Each other |
| All section headers | Each other |

### Verification Process

1. Identify all text boxes at the same hierarchy level
2. Check font size of each box
3. If any box differs, adjust all to match
4. Default to the larger size if content fits; otherwise use the smaller size consistently

**Exception**: Sub-bullets or secondary text may use smaller font than primary bullets, but this must be consistent across ALL boxes.

---

## Template Adaptation

These standards should be adapted to match the specific template being used:

1. **Colors**: Use the template's brand colors rather than prescribing specific colors
2. **Fonts**: Use the template's font family
3. **Spacing**: Match the template's existing spacing conventions
4. **Layout**: Follow the template's section structure

The key principles that remain constant regardless of template:
- Text must be readable against its background
- Tables must be actual table objects
- Content should fill available space appropriately
- Formatting should be consistent across parallel elements
- Charts/images should be properly sized
