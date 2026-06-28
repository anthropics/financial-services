---
name: ppt-template-creator
description: Creates self-contained PPT template SKILLS (not presentations) from user-provided PowerPoint templates. Use ONLY when a user wants to create a reusable skill from their template. For creating actual presentations, use the pptx skill instead.
---

# PPT Template Creator

**This skill creates SKILLS, not presentations.** Use this when a user wants to turn their PowerPoint template into a reusable skill that can generate presentations later. If the user just wants to create a presentation, use the `pptx` skill instead.

The generated skill includes:
- `assets/template.pptx` - the template file
- `SKILL.md` - complete instructions (no reference to this meta skill needed)

**For general skill-building best practices**, refer to the `skill-creator` skill. This skill focuses on PPT-specific patterns.

## Workflow

1. **User provides template** (.pptx or .potx)
2. **Analyze template** - extract layouts, placeholders, dimensions
3. **Initialize skill** - use the `skill-creator` skill to set up the skill structure
4. **Add template** - copy .pptx to `assets/template.pptx`
5. **Write SKILL.md** - follow template below with PPT-specific details
6. **Create example** - generate sample presentation to validate
7. **Package** - use the `skill-creator` skill to package into a .skill file

## Step 2: Analyze Template

**CRITICAL: Extract precise placeholder positions** - this determines content area boundaries.

```python
from pptx import Presentation

prs = Presentation(template_path)
print(f"Dimensions: {prs.slide_width/914400:.2f}\" x {prs.slide_height/914400:.2f}\"")
print(f"Layouts: {len(prs.slide_layouts)}")

for idx, layout in enumerate(prs.slide_layouts):
    print(f"\n[{idx}] {layout.name}:")
    for ph in layout.placeholders:
        try:
            ph_idx = ph.placeholder_format.idx
            ph_type = ph.placeholder_format.type
            # IMPORTANT: Extract exact positions in inches
            left = ph.left / 914400
            top = ph.top / 914400
            width = ph.width / 914400
            height = ph.height / 914400
            print(f"    idx={ph_idx}, type={ph_type}")
            print(f"        x={left:.2f}\", y={top:.2f}\", w={width:.2f}\", h={height:.2f}\"")
        except:
            pass
```

**Key measurements to document:**
- **Title position**: Where does the title placeholder sit?
- **Subtitle/description**: Where is the subtitle line?
- **Footer placeholders**: Where do footers/sources appear?
- **Content area**: The space BETWEEN subtitle and footer is your content area

### Finding the True Content Start Position

**CRITICAL:** The content area does NOT always start immediately after the subtitle placeholder. Many templates have a visual border, line, or reserved space between the subtitle and content area.

**Best approach:** Look at Layout 2 or similar "content" layouts that have an OBJECT placeholder - this placeholder's `y` position indicates where content should actually start.

```python
# Find the OBJECT placeholder to determine true content start
for idx, layout in enumerate(prs.slide_layouts):
    for ph in layout.placeholders:
        try:
            if ph.placeholder_format.type == 7:  # OBJECT type
                top = ph.top / 914400
                print(f"Layout [{idx}] {layout.name}: OBJECT starts at y={top:.2f}\"")
                # This y value is where your content should start!
        except:
            pass
```

**Example:** A template might have:
- Subtitle ending at y=1.38"
- But OBJECT placeholder starting at y=1.90"
- The gap (0.52") is reserved for a border/line - **do not place content there**

Use the OBJECT placeholder's `y` position as your content start, not the subtitle's end position.

## Step 5: Write SKILL.md

The generated skill should have this structure:
```
[company]-ppt-template/
├── SKILL.md
└── assets/
    └── template.pptx
```

### Generated SKILL.md Template

The generated SKILL.md must be **self-contained** with all instructions embedded. Use this template, filling in the bracketed values from your analysis:

````markdown
---
name: [company]-ppt-template
description: [Company] PowerPoint template for creating presentations. Use when creating [Company]-branded pitch decks, board materials, or client presentations.
---

# [Company] PPT Template

Template: `assets/template.pptx` ([WIDTH]" x [HEIGHT]", [N] layouts)

## Creating Presentations

```python
from pptx import Presentation

prs = Presentation("path/to/skill/assets/template.pptx")

# DELETE all existing slides first
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[0]

# Add slides from layouts
slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_IDX])
```

## Key Layouts

| Index | Name | Use For |
|-------|------|---------|
| [0] | [Layout Name] | [Cover/title slide] |
| [N] | [Layout Name] | [Content with bullets] |
| [N] | [Layout Name] | [Two-column layout] |

## Placeholder Mapping

**CRITICAL: Include exact positions (x, y coordinates) for each placeholder.**

### Layout [N]: [Name]
| idx | Type | Position | Use |
|-----|------|----------|-----|
| [idx] | TITLE (1) | y=[Y]" | Slide title |
| [idx] | BODY (2) | y=[Y]" | Subtitle/description |
| [idx] | BODY (2) | y=[Y]" | Footer |
| [idx] | BODY (2) | y=[Y]" | Source/notes |

### Content Area Boundaries

**Document the safe content area for custom shapes/tables/charts:**

```
Content Area (for Layout [N]):
- Left margin: [X]" (content starts here)
- Top: [Y]" (below subtitle placeholder)
- Width: [W]"
- Height: [H]" (ends before footer)

For 4-quadrant layouts:
- Left column: x=[X]", width=[W]"
- Right column: x=[X]", width=[W]"
- Top row: y=[Y]", height=[H]"
- Bottom row: y=[Y]", height=[H]"
```

**Why this matters:** Custom content (textboxes, tables, charts) must stay within these boundaries to avoid overlapping with template placeholders like titles, footers, and source lines.

## Filling Content

**Do NOT add manual bullet characters** - slide master handles formatting.

```python
# Fill title
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        if shape.placeholder_format.type == 1:  # TITLE
            shape.text = "Slide Title"

# Fill content with hierarchy (level 0 = header, level 1 = bullet)
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == [CONTENT_IDX]:
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()

            content = [
                ("Section Header", 0),
                ("First bullet point", 1),
                ("Second bullet point", 1),
            ]

            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```

## Example: Cover Slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[[COVER_IDX]])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == [TITLE_IDX]:
            shape.text = "Company Name"
        elif idx == [SUBTITLE_IDX]:
            shape.text = "Presentation Title | Date"
```

## Example: Content Slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[[CONTENT_IDX]])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        ph_type = shape.placeholder_format.type
        idx = shape.placeholder_format.idx
        if ph_type == 1:
            shape.text = "Executive Summary"
        elif idx == [BODY_IDX]:
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()
            content = [
                ("Key Findings", 0),
                ("Revenue grew 40% YoY to $50M", 1),
                ("Expanded to 3 new markets", 1),
                ("Recommendation", 0),
                ("Proceed with strategic initiative", 1),
            ]
            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```
````

## Step 6: Create Example Output

Generate a sample presentation to validate the skill works. Save it alongside the skill for reference.

## PPT-Specific Rules for Generated Skills

1. **Template in assets/** - always bundle the .pptx file
2. **Self-contained SKILL.md** - all instructions embedded, no external references
3. **No manual bullets** - use `paragraph.level` for hierarchy
4. **Delete slides first** - always clear existing slides before adding new ones
5. **Document placeholders by idx** - placeholder idx values are template-specific
