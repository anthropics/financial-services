---
name: template
description: >
  Canonical rules and HTML/CSS contract for the page chrome (head boilerplate, cover, table of
  contents, section block, sources-section wrapper, footer, outlook-badge, design tokens) shared
  across Moody's Agentic Solutions HTML report skills (earnings-call-summary, peer-analysis,
  public-information-book, sector-analysis). Sibling of `skills/shared/citations/` using the same
  inlining pattern. Parent skills must read BOTH this `SKILL.md` (authoring rules: shared-layer
  classes, allowed per-skill overrides, outlook-badge usage) AND `assets/template.html` (canonical
  CSS + literal HTML snippets) before emitting any report. The asset is the source of truth for
  markup; this file is the source of truth for rules. Triggers on questions about the template,
  page chrome, cover, table of contents, footer, layout, design tokens, color palette, fonts,
  outlook badges, or any visual scaffolding of an HTML report skill.
---

# Template Skill (shared)

This is the **single source of truth** for the visual chrome of every HTML report produced by
the parent skills `earnings-call-summary`, `peer-analysis`, `public-information-book`, and
`sector-analysis`. It owns:

- Design tokens (`--navy`, `--accent`, `--gray-*` / `--g*`, `--text`, `--positive`, `--negative`,
  `--neutral`).
- The CSS reset.
- Body and page base styling. The canonical defaults are `body { font-size: 13px }` and
  `.page { max-width: 900px }`; ECS / SA inherit them as-is, PA overrides `max-width` to
  `1050px`, and PIB overrides both (`font-size: 12.5px`, `max-width: 920px`).
- Both cover variants (`cover-simple` for PIB / SA; `cover-multi` for ECS / PA).
- TOC styling (`.toc-page`, `.toc-heading`, `.toc-list`, `.toc-num`, `.toc-label`, `.toc-dots`).
- Section styling (`.section`, `.section-heading`, `.section-content` and its descendants).
- The canonical pastel `.outlook-badge` (`stable` / `positive` / `negative` / `review` / `na`).
- Anchor base styling.
- Footer styling (`.report-footer`, `.footer-logo`).
- Print rules.
- The HTML scaffolds for the document head, both covers, the TOC block, the section block, the
  sources-section wrapper, the footer, and the outlook-badge.

The canonical CSS and the literal HTML markup contracts live in
[`assets/template.html`](./assets/template.html). This `SKILL.md` describes the rules; the asset
file ships the verbatim implementation. **Parent skills must read both files before emitting.**

## When to read this skill

Read this skill from a parent skill **before** emitting any HTML report. Parent skills must
contain a directive near the top of their `SKILL.md` instructing the agent to read **both**
this file and `assets/template.html`. The pairing is identical to the `skills/shared/citations/`
contract — every HTML report touches both shared skills.

## Lookup-order rule (non-negotiable)

Whenever the agent is about to author CSS, an HTML scaffold, a class name, a design token, or
any visual chrome that the parent skill does not itself define, it must consult this shared
template skill **first** and only fall back to inventing markup if the shared layer also does
not cover the need. Do not silently restyle anything the shared skill owns; do not invent CSS or
HTML scaffolding for elements the shared skill already provides.

## Output contract (single global rules)

1. Every emitted HTML report inlines the contents of `<style id="shared-template-css">` from
   `assets/template.html` between the `/* BEGIN shared-template-css ... */` and
   `/* END shared-template-css */` CSS-comment markers in the parent template's `<style>`
   block. Parent templates ship only the marker comments; they never duplicate the rules.
2. Every emitted HTML report uses the literal markup from the matching `<template>` snippet for
   the document head, cover (one of `cover-simple` / `cover-multi`), TOC, section block,
   sources-section wrapper, and footer. Class names and attribute order are invariant.
3. Each parent skill picks **exactly one** cover variant. Variants do not mix within a single
   report.
4. Per-skill CSS overrides (see "Per-skill overrides" below) live **above** the marker region
   in the parent template's `<style>` block — never inside it, and never as duplicated copies
   of shared rules.

## 1. Document head (snippet `document-head`)

The shared `document-head` snippet is the literal contract for the top of the parent template:
`<!DOCTYPE html>`, the `<html>` / `<head>` / `<meta>` / `<title>` boilerplate, and the
`<style>` block that contains:

1. Skill-specific overrides (see below).
2. The `/* BEGIN shared-template-css ... */` marker region.
3. The `/* BEGIN shared-citations-css ... */` marker region.

Then `<body>` opens with `<div class="page">`, which wraps the cover, TOC, report body, and
footer. Substitute `{report_title}`.

## 2. Cover (snippets `cover-simple` and `cover-multi`)

Two variants. Each parent skill uses exactly one:

| variant       | used by                                  | shape                                            |
|---------------|------------------------------------------|--------------------------------------------------|
| `cover-simple`| `public-information-book`, `sector-analysis` | 1-column navy cover, top "logo + title" / bottom `.cover-meta`. |
| `cover-multi` | `earnings-call-summary`, `peer-analysis` | 2-region grid: `.cover-top` with navy `.cover-left` + optional `.cover-strip` image + `.cover-bar-top`; `.cover-bottom` is an optional landscape band. |

Cover-multi rules:

- Add the `has-cover-image` class to `.cover-top` and/or `.cover-bottom` **only when an `<img>`
  is populated** in `.cover-strip` / `.cover-landscape`. Without the class, the strip and bar
  are hidden by the canonical CSS.
- `.cover-companies` lists per-skill chips. PA marks the target entity with
  `class="company-chip target"`; ECS lists the issuer first.
- The `.cover-companies-label` text is per-skill (e.g. `PEERS`, `COMPANIES`).
- Cover-image content (the `<img>` URLs) is per-skill data; the wrapper classes are shared.

Cover-simple rules:

- One `.cover-meta` row at the bottom; populate as many `<span><strong>Label:</strong> value</span>`
  pairs as the parent skill needs. PIB always emits `Type: Public Information Book`.

## 3. Table of contents (snippet `toc-block`)

The TOC scaffold is identical across all four skills. Each parent fills the `<ul class="toc-list">`
with one `<li>` per section it emits, in document order, using the `.toc-num` / `.toc-label` /
`.toc-dots` pattern. The trailing TOC entry always points to the Citations block
(`#{prefix}-sources-anchor`, label `Citations`).

## 4. Section block (snippet `section-block`)

Every titled section in the report body uses the `<div class="section" id="{prefix}-section-{slug}">`
> `<div class="section-heading">` + `<div class="section-content">` shape. The body of
`.section-content` is skill-specific (paragraphs, tables, lists, charts).

The `<div id="{prefix}-cite-{slot}"></div>` placeholder inside `.section-content` is **opt-in**
and only relevant to skills that consume the per-section citation recap from
`skills/shared/citations/`. Skills that do not opt in omit the placeholder.

## 5. Sources-section wrapper (snippet `sources-section-block`)

This is the same wrapper that `skills/shared/citations/` defines as `<template id="sources-section">`,
re-shipped here so the document scaffold stays self-contained. The wrapper anchors the TOC link
target via `id="{prefix}-sources-anchor"` and contains `#{prefix}-sources` for the rows. The
**rows themselves** (`.source-item`) are owned by `skills/shared/citations/`, not by this skill.

## 6. Report footer (snippet `report-footer`)

The footer is identical across all four skills: navy `.report-footer` band with the Moody's
Agentic Solutions logo on the left and the report date on the right. Substitute `{YYYY-MM-DD}`.

## 7. Outlook badge (snippet `outlook-badge`)

The canonical visual treatment is **pastel background + colored text**. Five variants ship in
the canonical CSS:

| class    | when to use                                                                |
|----------|----------------------------------------------------------------------------|
| `stable` | issuer-level outlook is `STA`/`Stable`.                                    |
| `positive`| outlook is `POS`/`Positive`.                                              |
| `negative`| outlook is `NEG`/`Negative`.                                              |
| `review` | outlook is `RUR`/`On Review` (also catches "Watch" semantics).             |
| `na`     | outlook unknown / not applicable; renders muted gray.                      |

The label text is uppercased by CSS so the inner text can be mixed-case (e.g. `Stable`).

PIB previously shipped a solid-fill variant (`background: var(--positive); color: #fff`) for
its outlook badges. That carve-out is **removed** — PIB now inherits the canonical pastel
variant from this shared skill, and parent templates must not re-define `.outlook-badge` rules.

## 8. Per-skill overrides

These rules are intentionally NOT in the canonical CSS. Each parent template keeps them above
the marker region (and only those — anything else inside the canonical block is shared):

| skill                       | allowed local overrides                                                |
|-----------------------------|------------------------------------------------------------------------|
| `earnings-call-summary`     | none. Cover variant: `cover-multi`.                                    |
| `peer-analysis`             | `.page { max-width: 1050px }`. Cover variant: `cover-multi`.           |
| `public-information-book`   | `body { font-size: 12.5px }`, `.page { max-width: 920px }`. Cover variant: `cover-simple`. |
| `sector-analysis`           | none. Cover variant: `cover-simple`.                                   |

Skill-specific CSS that the shared layer does not own (and which therefore stays in each
parent template indefinitely):

- All table classes (`.yoy-table`, `.ratings-table`, `.pa-table`, `.credit-drivers-table`,
  `.ki-table`, `.sc-table`, `.fin-table`, `.data-table`, `.row-label`, etc.).
- ECS `.credit-badge`, `.ratings-factors`.
- ECS / PA cover-image accent classes that are only meaningful inside `cover-multi` and that
  use skill-specific spacing (most are already shared; anything with skill-specific tweaks
  stays local).
- PA `.sub-heading`, `.chart-container`, `.chart-title`, `.chart-legend`.
- PIB chart helpers, ratings-grid helpers.
- SA sector-card / theme-card helpers.

## 9. Canonical CSS

The canonical CSS lives **only** in `assets/template.html` inside the
`<style id="shared-template-css">…</style>` block. Parent templates do **not** carry a
duplicate copy of these rules. Each parent template instead reserves a marker region inside
its own `<style>` tag bracketed by **CSS comments** (not HTML comments — the markers sit
inside `<style>`, where `<!-- … -->` would produce CSS parse errors):

```css
/* BEGIN shared-template-css (inlined at emit time from skills/shared/template/assets/template.html) */
/* END shared-template-css */
```

At emit time, the agent copies the **contents** (not the `<style>` wrapper) of
`<style id="shared-template-css">…</style>` from the shared asset and inserts them between
those two marker comments in the final emitted HTML. Treat the canonical CSS as a single
block — do not edit values per-skill. If a parent skill needs to restyle shared chrome, change
`assets/template.html` and the next emit picks it up automatically.

### CSS variable contract

The block defines the following CSS custom properties on `:root`. They are available to every
piece of skill-specific CSS that lives above the marker region:

- `--navy`, `--accent` — primary palette.
- `--gray-100`, `--gray-200`, `--gray-300`, `--gray-400`, `--gray-700` — neutral grays.
- `--g100`, `--g200`, `--g300`, `--g400`, `--g700` — short aliases for the same grays. Both
  naming schemes resolve. Skill-specific CSS may use either family interchangeably.
- `--text` — body text color.
- `--positive`, `--negative`, `--neutral` — semantic colors used by `.outlook-badge` and
  by skill-specific tables (e.g. positive / negative deltas).

## 10. Quick checklist (use before submitting a report)

- [ ] The contents of `<style id="shared-template-css">` from `assets/template.html` have been
      inlined between the `/* BEGIN shared-template-css */` / `/* END shared-template-css */`
      markers in the emitted HTML.
- [ ] The contents of `<style id="shared-citations-css">` from
      `skills/shared/citations/assets/template.html` have been inlined between the parallel
      citations markers.
- [ ] The parent template's `<style>` block contains **no duplicated copy** of any rule that
      lives in either canonical block.
- [ ] The cover uses exactly one variant (`cover-simple` or `cover-multi`) and matches the
      parent skill's declared variant.
- [ ] `.cover-multi`'s `.cover-top` / `.cover-bottom` only carries `has-cover-image` when an
      `<img>` is populated.
- [ ] All `.outlook-badge` instances use the canonical pastel variants (`stable`, `positive`,
      `negative`, `review`, `na`). No solid-fill / inline-color overrides anywhere.
- [ ] The TOC's last row points to `#{prefix}-sources-anchor` with label `Citations`.
- [ ] The emitted footer uses `.report-footer` + `.footer-logo` markup verbatim.
- [ ] Per-skill overrides above the marker region are limited to the rows in section 8.
