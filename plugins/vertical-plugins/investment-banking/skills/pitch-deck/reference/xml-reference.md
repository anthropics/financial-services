# PowerPoint XML Reference

This file contains XML patterns for programmatic PowerPoint editing. Use these patterns when working directly with OOXML format.

**Note:** Color values in examples (e.g., `E67E22`, `D35400`) are placeholders. Replace with your template's brand colors.

---

## ⚠️ When to Use This Reference

**Use python-pptx for:**
- Creating new tables (handles cell structure and relationships automatically)
- Adding text boxes
- Inserting images
- Most shape creation
- Any operation where python-pptx provides an API

**Use direct XML editing only for:**
- Modifying properties of existing elements that python-pptx doesn't expose
- Fine-tuning cell formatting after table creation via python-pptx
- Adjusting specific shape properties not available via the python-pptx API

**NEVER use direct XML for:**
- Creating tables from scratch (relationship management is error-prone and will likely corrupt the file)
- Initial shape creation (shape ID collision risk)
- Anything you can accomplish via python-pptx

The XML patterns in this file are for **reference and targeted modifications**, not wholesale element construction.

---

## XML Editing Risks

Direct XML editing can corrupt PowerPoint files if not done carefully:
- PowerPoint XML has interdependencies (relationship files, content types)
- Invalid XML or missing relationships can corrupt the entire file
- Shape IDs must be unique across each slide

**Always work on a backup copy** — never edit the original file directly.

---

## Contents
- [Table Implementation](#table-implementation)
- [Arrow Shapes](#arrow-shapes)
- [Text Boxes](#text-boxes)
- [Shapes with Fill](#shapes-with-fill)
- [Image Insertion](#image-insertion)
- [Connector Lines](#connector-lines)
- [Unit Conversions](#unit-conversions)

---

## Table Implementation

### CRITICAL: Verify Tables Are Actual Table Objects

After creating any table, you MUST verify it is an actual table object, not text with separators.

**Programmatic verification (python-pptx):**
```python
for shape in slide.shapes:
    if shape.has_table:
        print(f"✓ Found table: {len(shape.table.rows)} rows, {len(shape.table.columns)} columns")
```

**Visual verification (in exported image):**
- Columns align perfectly regardless of content length
- Cell borders are consistent
- Selecting the table selects all cells as a unit

**Failure indicators — you have created TEXT, not a table:**
- `|` characters visible between values
- Columns misalign when content length varies
- Tab characters (`\t`) used for spacing
- Multiple text boxes arranged to look like a table

Text-based "tables" cannot be edited by the recipient, will misalign when fonts change, and signal amateur work. There is no acceptable use case for pipe/tab-separated tabular data in a pitch deck.

---

### Basic Table Structure

```xml
<a:tbl>
  <a:tblPr firstRow="1" bandRow="1">
    <a:tableStyleId>{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}</a:tableStyleId>
  </a:tblPr>
  <a:tblGrid>
    <a:gridCol w="2000000"/>  <!-- Source column - width in EMUs -->
    <a:gridCol w="1200000"/>  <!-- 2024 Size column -->
    <a:gridCol w="1200000"/>  <!-- CAGR column -->
    <a:gridCol w="1200000"/>  <!-- 2030 Projection column -->
  </a:tblGrid>
  <!-- Row definitions follow -->
</a:tbl>
```

### Table Row with Cells

```xml
<a:tr h="370840">  <!-- Row height in EMUs -->
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="l"/>  <!-- Left alignment for text columns -->
        <a:r>
          <a:rPr lang="en-US" sz="1000" b="0"/>
          <a:t>Grand View Research</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr/>
  </a:tc>
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="ctr"/>  <!-- Center alignment for numeric columns -->
        <a:r>
          <a:rPr lang="en-US" sz="1000"/>
          <a:t>22.1</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr/>
  </a:tc>
  <!-- Additional cells... -->
</a:tr>
```

### Header Row Styling

```xml
<a:tr h="370840">
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="l"/>
        <a:r>
          <a:rPr lang="en-US" sz="1000" b="1">  <!-- Bold for headers -->
            <a:solidFill>
              <a:srgbClr val="FFFFFF"/>  <!-- White text -->
            </a:solidFill>
          </a:rPr>
          <a:t>Source</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr>
      <a:solidFill>
        <a:srgbClr val="E67E22"/>  <!-- Orange background -->
      </a:solidFill>
    </a:tcPr>
  </a:tc>
  <!-- Additional header cells... -->
</a:tr>
```

---

## Arrow Shapes

### Right Arrow Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="10" name="Arrow Right"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="3000000" y="2500000"/>  <!-- Position in EMUs -->
      <a:ext cx="500000" cy="300000"/>   <!-- Size in EMUs -->
    </a:xfrm>
    <a:prstGeom prst="rightArrow">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>  <!-- Arrow fill color -->
    </a:solidFill>
    <a:ln>
      <a:noFill/>  <!-- No outline -->
    </a:ln>
  </p:spPr>
</p:sp>
```

### Down Arrow Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="11" name="Arrow Down"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="2500000" y="3000000"/>
      <a:ext cx="300000" cy="500000"/>
    </a:xfrm>
    <a:prstGeom prst="downArrow">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
  </p:spPr>
</p:sp>
```

### Chevron Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="12" name="Chevron"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="3000000" y="2500000"/>
      <a:ext cx="400000" cy="600000"/>
    </a:xfrm>
    <a:prstGeom prst="chevron">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
  </p:spPr>
</p:sp>
```

---

## Text Boxes

### Basic Text Box

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="5" name="TextBox 4"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="1500000"/>
      <a:ext cx="4000000" cy="500000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:noFill/>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" rtlCol="0">
      <a:spAutoFit/>
    </a:bodyPr>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:rPr lang="en-US" sz="1400" dirty="0"/>
        <a:t>Text content here</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### Text Box with Bullet Points

```xml
<p:txBody>
  <a:bodyPr wrap="square">
    <a:spAutoFit/>
  </a:bodyPr>
  <a:lstStyle/>
  <a:p>
    <a:pPr marL="342900" indent="-342900">
      <a:buFont typeface="Wingdings" panose="05000000000000000000" pitchFamily="2" charset="2"/>
      <a:buChar char="&#252;"/>  <!-- Checkmark character -->
    </a:pPr>
    <a:r>
      <a:rPr lang="en-US" sz="1400" dirty="0"/>
      <a:t>First bullet point</a:t>
    </a:r>
  </a:p>
  <a:p>
    <a:pPr marL="342900" indent="-342900">
      <a:buFont typeface="Wingdings" panose="05000000000000000000" pitchFamily="2" charset="2"/>
      <a:buChar char="&#252;"/>
    </a:pPr>
    <a:r>
      <a:rPr lang="en-US" sz="1400" dirty="0"/>
      <a:t>Second bullet point</a:t>
    </a:r>
  </a:p>
</p:txBody>
```

### Text with White Color (for dark backgrounds)

```xml
<a:r>
  <a:rPr lang="en-US" sz="1000" b="1" i="1" dirty="0">
    <a:solidFill>
      <a:srgbClr val="FFFFFF"/>  <!-- White text -->
    </a:solidFill>
  </a:rPr>
  <a:t>White text on colored background</a:t>
</a:r>
```

---

## Shapes with Fill

### Rectangle with Solid Fill

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="20" name="Rectangle 19"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="2500000"/>
      <a:ext cx="1000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>  <!-- Orange fill -->
    </a:solidFill>
    <a:ln w="12700">  <!-- Border width -->
      <a:solidFill>
        <a:srgbClr val="D35400"/>  <!-- Darker border -->
      </a:solidFill>
    </a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr rtlCol="0" anchor="ctr"/>  <!-- Vertically centered text -->
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>  <!-- Horizontally centered -->
      <a:r>
        <a:rPr lang="en-US" sz="1600" b="1">
          <a:solidFill>
            <a:srgbClr val="FFFFFF"/>
          </a:solidFill>
        </a:rPr>
        <a:t>Label Text</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## Image Insertion

### Adding Image to Slide

```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="99" name="Company Logo"/>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rIdLogo"/>  <!-- Reference to relationship ID -->
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="10800000" y="200000"/>  <!-- Top-right position -->
      <a:ext cx="800000" cy="600000"/>   <!-- Logo dimensions -->
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

### Adding Image Relationship

In `ppt/slides/_rels/slideN.xml.rels`:

```xml
<Relationship Id="rIdLogo" 
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" 
  Target="../media/logo.png"/>
```

---

## Connector Lines

### Straight Connector

```xml
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="15" name="Straight Connector 14"/>
    <p:cNvCxnSpPr>
      <a:cxnSpLocks/>
    </p:cNvCxnSpPr>
    <p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="2500000"/>
      <a:ext cx="5000000" cy="0"/>  <!-- Horizontal line -->
    </a:xfrm>
    <a:prstGeom prst="line">
      <a:avLst/>
    </a:prstGeom>
    <a:ln w="12700">
      <a:solidFill>
        <a:srgbClr val="E67E22"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

### Dashed Line

```xml
<p:spPr>
  <a:xfrm>
    <a:off x="500000" y="4500000"/>
    <a:ext cx="5000000" cy="0"/>
  </a:xfrm>
  <a:prstGeom prst="line">
    <a:avLst/>
  </a:prstGeom>
  <a:ln w="12700">
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
    <a:prstDash val="dash"/>  <!-- Dashed style -->
  </a:ln>
</p:spPr>
```

---

## Unit Conversions

| Unit | EMUs per unit |
|------|---------------|
| 1 inch | 914400 |
| 1 cm | 360000 |
| 1 point | 12700 |
| 1 pixel (96 DPI) | 9525 |

### Common Slide Dimensions (16:9)

- Width: 12192000 EMUs (13.333 inches)
- Height: 6858000 EMUs (7.5 inches)

### Typical Element Positions

| Element | X Position | Y Position |
|---------|------------|------------|
| Logo (top-right) | 10800000 | 200000 |
| Title | 342583 | 286603 |
| Subtitle | 402591 | 1767390 |
| Footer | 342583 | 6435334 |
