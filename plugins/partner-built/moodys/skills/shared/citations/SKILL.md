---
name: citations
description: >
  Canonical rules and HTML/CSS contract for inline `[n]` citation references, end-of-document
  Citations blocks, and optional per-section citation recaps used across Moody's Agentic
  Solutions HTML report skills (earnings-brief, peer-analysis, issuer-brief,
  sector-brief). Parent skills must read BOTH this `SKILL.md` (rules, numbering, hyperlink
  behavior, source data shape) AND `assets/template.html` (canonical CSS block + literal HTML
  markup snippets) before emitting citations. The asset file is the single source of truth for
  the visual/markup implementation; this `SKILL.md` is the single source of truth for the
  authoring rules. Triggers when the user asks about citations, sources, references,
  footnotes, hyperlinking [n] markers, or the Sources/Citations block in any HTML report
  skill.
---

# Citations Skill (shared)

This is the **single source of truth** for how citations are authored and rendered across the
HTML report skills. Parent skills (`earnings-brief`, `peer-analysis`,
`issuer-brief`, `sector-brief`) defer to this document for inline reference
markup, the Citations block, numbering, hyperlinking, source data shape, and CSS. Each parent
skill keeps only its own carve-outs (e.g. "no citations in `.yoy-change` cells", "no citations
in financial table cells").

The canonical CSS and the literal HTML markup contracts live in
[`assets/template.html`](./assets/template.html). This `SKILL.md` describes the rules; the
asset file ships the verbatim implementation. **Parent skills must read both files** before
emitting citations.

> **Sibling skill.** [`skills/shared/template/`](../template/) owns the rest of the visual
> chrome (cover, TOC, section, sources-section wrapper, footer, outlook-badge, design tokens)
> and uses the **same inlining pattern** as this skill — parent templates reserve a CSS-comment
> marker region (`/* BEGIN shared-template-css ... */` / `/* END shared-template-css */`) and
> copy the contents of `<style id="shared-template-css">` from that skill's `assets/template.html`
> at emit time. Read both shared skills together when authoring or modifying any HTML report
> skill.

## When to read this skill

Read this skill from a parent skill **before** emitting any `[n]` reference or the
end-of-document Citations block. Parent skills must contain a directive near the top of their
`SKILL.md` instructing the agent to read **both** this file and `assets/template.html`.

## Output contract (single global rules)

1. Every report contains exactly one Citations block at the end of the document.
2. Numbering is a single global sequence `[1], [2], …` per document. The number `n` in any
   inline reference MUST equal the row position of the matching source inside
   `#{prefix}-sources` (1-indexed, in document order).
3. Internal MCP tool names are NEVER rendered in any citation row.
4. Plain `[n]` text in narrative content (not wrapped in `<a class="cite-ref">` or
   `<span class="cite-ref">`) is **not allowed**.
5. Citations are not embedded inside numeric/data cells of financial, valuation, ratings,
   risk, ESG, or YoY tables. Parent skills may extend this carve-out list.

## 1. Inline reference markup

The literal markup ships in `assets/template.html` (`<template id="cite-ref-anchor">` and
`<template id="cite-ref-span">`). Rules:

- **With URL**: copy `cite-ref-anchor` and substitute `{source_url}` and `[n]`. This is the
  default form.
- **Without URL**: copy `cite-ref-span` and substitute `[n]`. Use this fallback **only** when
  the source has no URL — the span keeps the `.cite-ref` styling without an active link.
- `n` MUST match the row position of that source inside `#{prefix}-sources`. The same `n`
  may be reused multiple times throughout the document for repeat references to the same
  source.

## 2. End-of-document Citations block

Every report renders exactly one Citations block at the end of the document. The container
markup ships in `assets/template.html` (`<template id="sources-section">`).

`{prefix}` is the parent skill's prefix (`ecs`, `pa`, `pib`, `sa`). The displayed heading is
always the literal string `Citations`. The container `<div>` keeps its existing
`#{prefix}-sources` id for backward continuity.

Three row variants ship in the asset; pick based on which fields are present:

| variant template id      | when to use                                                       |
|--------------------------|-------------------------------------------------------------------|
| `source-item-with-url`   | source has a URL **and** at least one of `source` / `date`.       |
| `source-item-no-url`     | no URL but at least one of `source` / `date`.                     |
| `source-item-no-meta`    | source has a URL but no `source` and no `date`.                   |

If only one of `source` or `date` is present, render only that field inside the `()` of
`.source-meta`. If neither is present and a URL exists, drop the `.source-meta` span entirely
(use `source-item-no-meta`).

## 3. Optional per-section recap (opt-in)

Some skills (currently `earnings-brief`, `peer-analysis`, `issuer-brief`)
render a short recap of the citations referenced inside a given section, immediately below
that section's content. This component is **opt-in**. Parent skills decide whether to use it;
the canonical CSS in `assets/template.html` ships the styling unconditionally so the option
is always available.

The recap markup ships in `assets/template.html` (`<template id="section-citations-recap">`).
Parent skills that opt in also embed empty target placeholders inside each section using the
`<template id="section-citations-target">` shape (`<div id="{prefix}-cite-{slot}"></div>`),
which the LLM later fills with a recap or leaves empty if the section has no citations.

The numbers inside a recap MUST be the same `n` values used inline and listed in the
end-of-document Citations block. A recap NEVER introduces a new numbering sequence. If a
section has no citations, omit the recap entirely (leave the target div empty).

## 4. Source data shape

Each source is described by:

| field   | required | notes                                                                 |
|---------|----------|-----------------------------------------------------------------------|
| `id`    | yes      | 1-indexed integer matching the row's position in `#{prefix}-sources`. |
| `title` | yes      | Human-readable title. Rendered inside `.source-title`.                |
| `source`| no       | Publisher / system (e.g. "Moody's Research Assistant Library").       |
| `date`  | no       | Display-formatted date (e.g. `2026-02-24` or `12 Sep 2026`).          |
| `url`   | no       | Absolute URL. If absent, use the URL-less row variant above.          |

Never render internal MCP tool names (e.g. `getEntityCreditOpinion`) in `.source-meta`.

## 5. Canonical CSS

The canonical CSS lives **only** in `assets/template.html` inside the
`<style id="shared-citations-css">…</style>` block. Parent templates do **not** carry a
duplicate copy of these rules. Each parent template instead reserves a marker region inside
its own `<style>` tag bracketed by **CSS comments** (not HTML comments — the markers sit
inside `<style>`, where `<!-- … -->` would produce CSS parse errors):

```css
/* BEGIN shared-citations-css (inlined at emit time from skills/shared/citations/assets/template.html) */
/* END shared-citations-css */
```

At emit time, the agent copies the **contents** (not the `<style>` wrapper) of
`<style id="shared-citations-css">…</style>` from the shared asset and inserts them between
those two marker comments in the final emitted HTML. Treat the canonical CSS as a single
block — do not edit values per-skill. If a parent skill needs to restyle citations, change
`assets/template.html` and the next emit picks it up automatically.

### CSS variable contract

The block above relies on these CSS custom properties being defined elsewhere in the parent
template's `:root` (they already are in every current template):

- `--accent` — link / inline-cite color
- `--navy`   — heading and source-num color
- `--g100`   — light background for `.section-citations`
- `--g200`   — border color for `.source-item` separator and `.section-citations` border
- `--g400`   — meta text color
- `--g700`   — body text color for source rows
- `--gray-100`, `--gray-200`, `--gray-400`, `--gray-700` — legacy aliases used by ECS / peer-
  analysis templates. Either set of names works; templates that already define `--gray-*` may
  alias them to `--g*` (or vice-versa) so the canonical block renders without edits.

If a template defines only one naming scheme, add aliases at the top of the `<style>` block
so both name families resolve. Example alias snippet (add only the side you are missing):

```css
:root {
  /* if template uses --gray-* but not --g*, alias them: */
  --g100: var(--gray-100);
  --g200: var(--gray-200);
  --g400: var(--gray-400);
  --g700: var(--gray-700);
}
```

## 6. Quick checklist (use before submitting a report)

- [ ] Every inline `[n]` is wrapped in `<a class="cite-ref">` (with `href` + `target="_blank"`)
      or, if no URL exists, `<span class="cite-ref">`.
- [ ] All `n` values resolve to a row inside `#{prefix}-sources` at position `n`.
- [ ] The Citations block heading reads exactly `Citations`.
- [ ] Each `.source-item` row uses `.source-num` + `.source-title` + optional `.source-meta`.
- [ ] No `.source-meta` renders an internal MCP tool name.
- [ ] No citation markup inside numeric/data cells excluded by the parent skill.
- [ ] Optional `.section-citations` recap, if used, reuses the same `n` values — it never
      starts a new numbering sequence.
- [ ] The canonical CSS from `<style id="shared-citations-css">` in
      `assets/template.html` has been inlined into the emitted HTML between the
      `/* BEGIN shared-citations-css */` / `/* END shared-citations-css */` CSS-comment
      markers that ship in the parent template.
