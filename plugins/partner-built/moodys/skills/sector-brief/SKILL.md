---
name: sector-brief
description: >
  Produce a Sector Brief HTML report for any industry sector using Moody's GenAI MCP tools
  and web research. Use this skill whenever the user asks to analyze a sector, write a sector
  report, do an industry analysis, create a sector overview, or generate a sector deep-dive.
  Trigger even if they just name a sector and mention "analysis", "overview", "outlook", "report",
  or "deep-dive". Also trigger for phrases like "what's happening in the retail sector" or
  "give me a sector breakdown for aerospace".
---

# Sector Brief Skill

Generates a professional HTML report (styled like a Moody's sector brief document) for a
specified industry sector. The report is research-heavy and text-driven, combining Moody's
internal research with supplemental web data across six structured sections plus an executive
summary and citations.

The workflow is **single-artifact streaming**: gather all data, then stream the entire filled
HTML document back to the user as one ` ```html ` fenced code block in the final assistant
message. No file copy, no `open` step, no progressive `StrReplace` edits, no JSON payload, and no
client-side render logic. The fenced code block is the deliverable.

> ## ⚠️ CRITICAL — NON-NEGOTIABLE OUTPUT CONTRACT
>
> **The LLM MUST deliver the report as a single HTML artifact in the assistant response.** Specifically:
>
> - The final message **MUST** contain exactly one ` ```html ` fenced code block holding the **complete, standalone HTML document** (`<!doctype html>` → `</html>`), every section populated inline.
> - The LLM **MUST NOT** write to disk, split across messages/blocks, or substitute prose, Markdown, JSON, or links for the artifact.
> - If data partially fails, emit the artifact with `"Data unavailable"` placeholders — never skip it.
>
> Treat any other output shape as a hard failure of the skill.

## Required MCP server

`Moodys MCP server` — tools used: `searchEntityDocuments` (sector research), `getEntitySectorOutlook`,
`searchNews`, `findEntity`

Web research is also required via `searchNews` or general web search tools.

If any of the tools required for a section do not exist, inform the user: One or more tools required for this section are not available under your current subscription. Unlock more of the expert insights, data, and analytics you trust. Get Link:https://www.moodys.com/web/en/us/capabilities/gen-ai/ai-ready-data.html with us to learn more.

## Bundled files

- `assets/template.html` — pre-styled scaffold with the Moody's cover, a baked-in static 6-item
  table of contents, and empty fill-in targets (cover title, date, section-content divs, sources
  container). Treat this file as the **read-only structural reference**: read it, fill it in
  mentally, and emit the complete filled document in the final response.

## Template (shared)

Before emitting the HTML report, **read both**:
1. [`skills/shared/template/SKILL.md`](../shared/template/SKILL.md) — authoring rules (which
   classes / snippets are owned by the shared layer, allowed per-skill overrides, outlook-badge
   usage).
2. [`skills/shared/template/assets/template.html`](../shared/template/assets/template.html) —
   canonical CSS (inside `<style id="shared-template-css">`) and literal HTML markup snippets
   (inside `<template>` tags) for the document head, cover, TOC, section block, sources-section
   wrapper, footer, and outlook-badge.

**Always check the shared template before inventing** any class, token, scaffold, or design element. Do not restyle anything the shared skill owns. At emit time, copy the **contents** of `<style id="shared-template-css">` into the marker region `/* BEGIN shared-template-css ... */` … `/* END shared-template-css */`. Use literal markup from the matching `<template>` snippets for all HTML chrome.

This skill uses the **`cover-simple`** variant with no skill-specific CSS overrides (inherits `body { font-size: 13px }` and `.page { max-width: 900px }`). Outlook-badge usage must use canonical pastel variants (`stable` / `positive` / `negative` / `review` / `na`) — no solid-fill or inline-color overrides.

## Citations (shared)

Before emitting any `[n]` reference inline or the end-of-document Citations block, **read both**:
1. [`skills/shared/citations/SKILL.md`](../shared/citations/SKILL.md) — authoring rules
   (numbering, hyperlinking, source data shape, carve-outs).
2. [`skills/shared/citations/assets/template.html`](../shared/citations/assets/template.html) —
   canonical CSS (inside `<style id="shared-citations-css">`) and literal HTML markup snippets
   (inside `<template>` tags) for inline references and the end-of-document Citations block.

At emit time, copy the **contents** of `<style id="shared-citations-css">` into the marker region `/* BEGIN shared-citations-css … */` … `/* END shared-citations-css */`.

The prefix used for the end-of-document container in this skill is `sa`, so the container id
is `#sa-sources`. This skill does not use the optional per-section `.section-citations` recap
component.

## Parameters

The user should provide:
- **Sector** (required — e.g., "Retail & Apparel", "Aerospace/Defense", "Banking")

If the user specifies a sub-sector like "Luxury Retail", use it as-is for focused analysis.

---

## Step 0 — Sector Picker (run before anything else)

If the user has not named a specific sector in their message, **stop** and call
`ask_user_input_v0` with a single `single_select` question before proceeding. Do **not**
begin any research or template reading until the sector is confirmed.

**Preamble:** "Which Moody's-covered sector would you like to analyze? Select one below
and I'll generate the full report."

**Options:**

- Aerospace & Defense
- Automotive Manufacturing
- Banking — Global
- Building Materials & Construction
- Chemicals
- Commercial Real Estate & REITs
- Consumer Products
- Diversified Manufacturing
- Food & Beverage
- Forest Products & Paper
- Gaming & Lodging
- Healthcare — Hospitals & Health Systems
- Healthcare — Medical Devices & Technology
- Healthcare — Pharmaceuticals
- Infrastructure & Project Finance
- Insurance
- Media & Entertainment
- Metals & Mining
- Oil & Gas — E&P
- Oil & Gas — Integrated & Refining
- Oil & Gas — Midstream & Pipeline
- Packaging
- Retail & Apparel
- Shipping & Ports
- Steel
- Structured Finance — ABS/RMBS/CMBS
- Technology — Hardware & Semiconductors
- Technology — Software & Services
- Telecommunications
- Transportation & Logistics
- Utilities — Electric
- Utilities — Gas Distribution
- Utilities — Water

Once the user selects, treat their choice exactly as if they had typed
`Run a sector brief for {selected sector}` and continue from Step 1.

If the user already named a sector, **skip this step entirely** and go straight to Step 1.

---

## Step 1 — Read the template

Read `assets/template.html` (relative to this skill directory) once. Keep its exact structure —
CSS, `<head>`, cover, hardcoded TOC, section order, and element IDs — as the scaffold for the
final artifact. Do **not** copy it to the workspace and do **not** open it.

---

## Step 2 — Research phase (parallel)

Fire ALL of the following searches in a **single parallel batch**:

### Moody's internal research (via MCP)

| Search | Purpose |
|--------|---------|
| `searchEntityDocuments` with criteria: "{Sector} Sector Overview" | Sector definition, methodology, key activities |
| `searchEntityDocuments` with criteria: "Economic factors impact on {Sector} Sector" | Macro-economic context |
| `searchEntityDocuments` with criteria: "{Sector} Sector, industry" | Financial performance data |
| `searchEntityDocuments` with criteria: "{Sector} Sector Risk and challenges" | Risk analysis |
| `searchEntityDocuments` with criteria: "{Sector} sector Outlook" | Sector outlook |
| `getEntitySectorOutlook` for a major company in the sector | Formal Moody's outlook |

### Web research (via searchNews or web tools)

| Search | Purpose |
|--------|---------|
| "Key players from {Sector} industry, market share, roles" | Key players for overview |
| "Key regions of activity and growth markets for {Sector} sector" | Geographic scope |
| "{Sector} sector aggregate revenue, profit margins, return on equity" | Financial metrics |
| "Major companies from {Sector} sector benchmark comparison" | Industry structure and dynamics |

---

## Step 3 — Synthesize all sections

Use Moody's internal research as the **primary foundation** for every section. Web sources
serve only to supplement gaps or validate findings. When conflicts arise, prioritize Moody's
unless external data provides substantial evidence for reconsideration.

Write in professional credit-research language. Always attribute sources with numbered citation
references inline. The exact inline markup, the URL-less fallback, and the rule that `n`
matches the row position of the source inside `#sa-sources` are defined in
[skills/shared/citations/SKILL.md](../shared/citations/SKILL.md).

### Executive Summary

Write after all other sections are complete. Half-page maximum. Highlight the most relevant
data from each section. No bullet points — flowing paragraphs only.

### Section 1: Sector Overview

Four subsections:
1. **Description of the Sector** — Define the industry, key activities, product/service
   categories, and business-model differences
2. **Market Size and Growth Trends** — Current market size (revenue, volume), historical
   growth rates, regional growth data
3. **Key Players** — Major companies, market share, roles within the sector
4. **Geographic Scope** — Key regions of activity, potential growth markets,
   region-specific trends

### Section 2: Macro-Economic Context

Three subsections:
1. **Economic Indicators** — How GDP growth, inflation, interest rates, consumer
   spending/confidence impact the sector
2. **Regulatory Environment** — Laws, regulations, compliance risks, tariff/trade policy
3. **Global Trends and External Factors** — Geopolitical issues, trade policies,
   technological disruptions, channel evolution

### Section 3: Financial Performance Analysis

Three subsections with **mandatory quantitative data**:
1. **Sector-Level Financial Metrics** — Aggregate revenue, profit margins, return on
   equity, other key metrics. Every metric must include the actual number (e.g., "Aggregate
   revenue of $35.2 trillion in 2025") followed by analytical commentary
2. **Historical Trends** — Past performance trends, demand/earnings trajectories,
   recent growth rates
3. **Projected Financial Outlook** — Forecast key metrics, earnings outlook, key drivers
   shaping the near-term, structural offsets and strategic responses

### Section 4: Industry Structure and Dynamics

Four subsections:
1. **Main Participants** — Benchmark major companies, roles, market share, significance
2. **Supply Chain Analysis** — Suppliers, manufacturers, distributors, customers,
   key pressure points
3. **Competitive Landscape** — Porter's Five Forces analysis with Moody's-grounded
   commentary for each force (use ratings High / Moderate / Low for each force)
4. **Barriers to Entry** — Capital requirements, regulatory hurdles, technology
   requirements, market saturation

### Section 5: Risks and Challenges

Five subsections:
1. **Operational Risks** — Supply chain disruptions, labor shortages, working capital
2. **Regulatory Risks** — Compliance requirements, policy changes, tariff exposure
3. **Market Risks** — Demand volatility, competition, pricing, category weakness
4. **Financial Performance and Capital Structure** — Refinancing risk, default outlook,
   margin pressure, deleveraging
5. **Environmental and Social Risks** — ESG considerations, climate risk, social/governance
   pressures

### Section 6: Sector Outlook

State the Moody's outlook (Positive, Stable, Negative) and date. Then provide 2-3
well-developed paragraphs explaining the rationale — primary drivers, regional nuances,
key factors and considerations. All paragraph form, no bullet points.

### Sources

Collect all sources. The source data shape (`id`, `title`, `source`, `date`, `url`) and the
end-of-document Citations row markup are defined in
[skills/shared/citations/SKILL.md](../shared/citations/SKILL.md).

---

## Inline SVG Charts — Section Instructions

After synthesizing each of the following sections, embed one inline SVG chart directly in the section content at the position indicated. All charts must be self-contained (no external scripts or stylesheets), include a `<title>` element for accessibility, and use `font-family: 'Source Sans Pro', Arial, sans-serif` inside an embedded `<style>` block.

### Section 3 — Financial Performance Analysis

Insert **Chart A** immediately after the Historical Trends subsection prose:

- Type: grouped bar chart (revenue) with a right-axis line series (EBITDA margin %)
- X-axis: fiscal years (last 3–5 years); left Y-axis: revenue ($B or $T); right Y-axis: margin (%)
- Bar color: `#003087`; line color: `#0073CF`
- `viewBox="0 0 700 320"`

### Section 4 — Industry Structure and Dynamics

Insert **Chart C** immediately after the Porter's Five Forces prose:

- Type: horizontal scored bar chart, one bar per force (5 bars)
- Map ratings to scores: High = 3, Moderate = 2, Low = 1; scale bar lengths to a 1–3 axis
- Bar colors: High = `#C0392B`, Moderate = `#E67E22`, Low = `#27AE60`
- `viewBox="0 0 700 220"`

### Section 6 — Sector Outlook

Insert **Chart D** immediately after the outlook paragraphs:

- Type: horizontal three-zone sentiment track (Negative | Stable | Positive) with a triangular marker at the current outlook position
- Zone colors: Negative = `#C0392B`, Stable = `#2980B9`, Positive = `#27AE60`; marker color matches active zone
- Label the current outlook and date below the track
- `viewBox="0 0 700 120"`

### Pre-computation requirement — mandatory, no exceptions

Before writing any SVG `x`, `y`, `width`, `height`, or `points` attribute, compute every value via bash or Python — do not calculate mentally. Record and verify computed values, then substitute into the SVG markup.

If source data for any chart is unavailable, emit a `<p>Chart data unavailable</p>` placeholder — never omit silently.

---

## Step 4 — Stream the complete HTML artifact

After all sections are synthesized, produce **one** final assistant message. The message contains:

1. A one-line summary sentence (e.g. `Sector Brief for {Sector}:`).
2. A single fenced ` ```html ` code block containing the **entire filled `template.html`
   document** — with every element from the streaming protocol populated in place. No partial
   documents, no separate code blocks per section.

The code block **must**:

- Start at column 0 with ` ```html ` and end with a closing ` ``` ` on its own line.
- Contain a complete, standalone HTML document (doctype → `</html>`) that renders without
  external dependencies.
- Preserve the template's `<head>` (CSS, fonts), cover, hardcoded TOC, section order, and
  element IDs exactly. Only the empty targets defined below are populated.

### Cover + footer

1. `#sa-cover-title` — `<strong>{Sector}</strong><br>Analysis` (HTML, not plain text).
2. `#sa-date` — report date string, e.g. `April 15, 2026`.
3. `#sa-footer-date` — same date string.

### Section headings

4. `#sa-overview-title` — override the default "Sector Overview" with
   `{Sector} — Sector Overview`.

### Section content targets

Each of the following divs takes fully-authored HTML (`<p>`, `<ul><li>`, and
`<strong class="subsection-title">…</strong>` only — no other block tags):

5. `#sa-exec` — Executive Summary. Flowing paragraphs only, no bullets.
6. `#sa-overview` — Section 1 body with four `<strong class="subsection-title">` subheaders.
7. `#sa-macro` — Section 2 body with three subheaders.
8. `#sa-financial` — Section 3 body with three subheaders. Every metric must include a
   concrete number.
9. `#sa-structure` — Section 4 body with four subheaders. Porter's Five Forces must use
   High / Moderate / Low ratings per force.
10. `#sa-risks` — Section 5 body with five subheaders.
11. `#sa-outlook` — Section 6 body. Lead with the Moody's outlook (Positive / Stable /
    Negative) and date, then 2–3 paragraphs. Paragraph form only.

### Sources container

12. `#sa-sources` — end-of-document Citations rows. One `<div class="source-item">` per
    source, in ascending `id` order, using the canonical row markup defined in
    [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md). Apply that file's rules
    for URL-less rows and missing `source`/`date` fields.

### HTML conventions

- Use `<p>` for paragraphs.
- Use `<ul><li>…</li></ul>` for bullet points (nested `<ul>` for sub-bullets).
- Use `<strong class="subsection-title">Subheader</strong>` for subsection headers within
  each section. Do not repeat the top-level section title — the template already renders it.
- Emit inline citations per
  [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md).
- Escape any `&`, `<`, `>` that appear in the narrative (`&amp;`, `&lt;`, `&gt;`).

---

## Tips

- Run ALL research searches in a single parallel batch.
- Moody's data is the foundation — web data supplements. Attribute external sources explicitly.
- The executive summary should be written last, after all other sections are synthesized.
- Citations follow the shared citations skill — read
  [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md) before authoring any `[n]`
  reference or the Citations block.

---

## Negative number formatting

Use `(-X)` for ALL negatives: `(-9%)`, `(-1.2pp)`, `(-$3.4B)`, `(-250 bps)`. Never use bare minus (`-9%`), en-dash (`–9%`), or parentheses without minus (`(9%)`). Apply to growth rates, margin changes, YoY deltas, and negative monetary values.

---

## Output and presentation (required final steps)

After assembling the report, you MUST follow this exact delivery sequence. Do not skip steps
and do not substitute alternatives. When updating this skill, do not delete or modify any
other file in the `skills/sector-brief/` folder.

1. **Write the HTML file in a single call.** Call `create_file` to write the entire HTML to
   `/mnt/user-data/outputs/{sector_slug}_sector_analysis.html` in **one** call.
   `{sector_slug}` is the lowercased, hyphenated sector name (e.g. `retail-apparel`,
   `oil-gas`).
2. **Preview the file.** Immediately after, use whatever tool is available in your current environment to present or display the final report to the user (e.g. a file presenter, inline renderer, or widget) at the end of running the skill.
3. **Show the widget.** Call `visualize:show_widget` to surface the rendered report visually
   to the user.
4. **One short follow-up sentence in chat.** Write a single brief sentence acknowledging the
   report is ready. Nothing more.

**Strict prohibitions:**

- **Never** emit the HTML as a fenced code block in the chat response.
- **Never** inline the HTML, JSON payload, or large excerpts of the report body in the chat
  message.
