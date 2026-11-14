---
name: earnings-brief
description: >
  Produce an Earnings Call Summary HTML report for 2–5 companies using Moody's GenAI MCP tools.
  Use this skill whenever the user asks to summarize earnings calls, generate an earnings call
  summary, analyze earnings transcripts across peers, or create an earnings call report. Trigger
  even if they just name companies and mention "earnings" or "transcript".
---
 
# Earnings Brief Skill
 
Generates a professional HTML report (styled like a Moody's earnings call summary PDF) for 2–5
companies by pulling data from multiple `Moodys MCP server` MCP tools and consolidating 13
structured sections plus a hardcoded table of contents into a single HTML artifact.
 
The workflow is **single-artifact delivery**: gather all data, then write the entire filled
HTML document to a single `.html` file in `/mnt/user-data/outputs/` and present it to the user
via `present_files`. The rendered HTML artifact is the deliverable.
 
> ## ⚠️ CRITICAL — NON-NEGOTIABLE OUTPUT CONTRACT
>
> **The LLM MUST deliver the final report as a single standalone HTML artifact file.** This is
> the only acceptable form of delivery for this skill. Specifically:
>
> - The LLM **MUST** write the **complete, standalone HTML document** (`<!doctype html>` →
>   `</html>`), with every section from the streaming protocol populated inline, to a single
>   `.html` file in `/mnt/user-data/outputs/` using the `create_file` tool, then surface it
>   to the user with `present_files`.
> - The LLM **MUST NOT** emit the report inline as a fenced ` ```html ` code block, as prose,
>   Markdown, JSON, attachments, or links. The rendered HTML artifact itself is the answer.
> - The LLM **MUST NOT** split the report across multiple files, multiple messages, partial
>   snippets, or summaries.
> - If data gathering fails partially, still produce the single HTML artifact file with the
>   best-available content. When the earnings call transcript for a company cannot be
>   located, **note that fact in the Executive Summary and omit the company from every other
>   section of the report** (no rows, no subtitles, no `"--"` placeholders for that company).
>   When a transcript exists but does not contain information for a specific section, **omit
>   that company from that section only** (no subtitle, no bullets, no placeholder). Never
>   skip the artifact itself.
>
> Treat any other output shape as a hard failure of the skill.
 
## Allowed data sources
 
This skill may **only** extract information from the following two sources:
 
1. `Moodys MCP server` — tools used: `findEntity` and `searchEntityEarningsCall`. These are the
   only MCP tools that may be called. Do **not** call `getEntityCreditOpinion`,
   `getEntitySectorOutlook`, `getEntityEsg`, `getEntityPeers`, `searchEntityDocuments`,
   `searchNews`, or any other MCP tool, regardless of section.
2. `web_search` — used **only as a fallback** when `searchEntityEarningsCall` returns no usable
   earnings call transcript for a given company, and used **only** to locate and extract the
   text of that company's earnings call transcript on the web. Do not use `web_search` for
   credit opinions, sector outlooks, news, peers, ESG, or any other purpose.
   **Recency requirement (web_search fallback):** if the transcript located via `web_search`
   is older than **100 days** from today, discard it and treat the transcript as unavailable
   for that company. Do not fall back to any other source — handle the company per the
   missing-transcript policy (note in the Executive Summary, omit from every other section).
These rules apply to **every** section of the report. No section may be enriched with credit,
sector, ESG, peer, filings, or news data.
 
## Bundled files
- `assets/template.html` — self-contained static report shell (CSS + named section placeholders).
  No embedded data, no inline script. Treat this file as the **read-only structural reference**:
  read it, fill it in, and write the complete filled document to a new `.html` file in
  `/mnt/user-data/outputs/`.
## Template (shared)
 
Before emitting the HTML report, **read both**:
1. [`skills/shared/template/SKILL.md`](../shared/template/SKILL.md) — authoring rules (which
   classes / snippets are owned by the shared layer, allowed per-skill overrides, outlook-badge
   usage).
2. [`skills/shared/template/assets/template.html`](../shared/template/assets/template.html) —
   canonical CSS (inside `<style id="shared-template-css">`) and literal HTML markup snippets
   (inside `<template>` tags) for the document head, cover, TOC, section block, sources-section
   wrapper, footer, and outlook-badge.
**Lookup order — always check the shared template before inventing.** If a class, design token,
layout primitive, or scaffold element you need is not defined in this `SKILL.md` or already
present in this skill's `assets/template.html`, the shared template skill is authoritative. Do
not invent CSS, HTML scaffolds, or design tokens that the shared skill already provides; do not
silently restyle anything the shared skill owns (cover, TOC, section, sources-section wrapper,
footer, outlook-badge, design tokens, reset, body / page base).
 
At emit time, copy the **contents** (not the `<style>` wrapper) of `<style id="shared-template-css">`
from the shared asset into the parent template's reserved marker region between the CSS-comment
markers `/* BEGIN shared-template-css ... */` and `/* END shared-template-css */`. For HTML
scaffolds (head boilerplate, cover, TOC, sources-section wrapper, footer), use the literal markup
from the matching `<template>` snippet in the shared asset. The parent template no longer
carries duplicated chrome CSS — those rules ship only in the shared asset.
 
This skill uses the **`cover-multi`** variant. Skill-specific overrides retained above the
marker region: **none** for ECS (it inherits the canonical `body { font-size: 13px }` and
`.page { max-width: 900px }` defaults). Skill-specific CSS that stays local: the ECS
`.credit-badge`, the `.yoy-table` / `.ratings-table` rules, and `.ratings-factors`. All
outlook-badge usage in this skill must use the canonical pastel variants
(`stable` / `positive` / `negative` / `review` / `na`) defined by the shared skill — no
solid-fill or inline-color overrides.
 
## Citations (shared)
 
Before emitting any `[n]` reference inline, any per-section recap block, or the end-of-document
Citations block, **read both**:
1. [`skills/shared/citations/SKILL.md`](../shared/citations/SKILL.md) — authoring rules
   (numbering, hyperlinking, source data shape, carve-outs).
2. [`skills/shared/citations/assets/template.html`](../shared/citations/assets/template.html) —
   canonical CSS (inside `<style id="shared-citations-css">`) and literal HTML markup snippets
   (inside `<template>` tags) for inline references, the end-of-document Citations block, and
   the optional `.section-citations` recap.
At emit time, copy the **contents** (not the wrapper) of `<style id="shared-citations-css">`
from the shared asset into the parent template's reserved marker region, located inside
`assets/template.html` between the CSS-comment markers
`/* BEGIN shared-citations-css … */` and `/* END shared-citations-css */`. The parent
template no longer carries duplicated citation CSS — those rules ship only in the shared
asset.
 
Skill-specific carve-outs that override or extend the shared rules are listed in the section
synthesis rules below — most importantly: **the numeric `.yoy-change` cell stays
citation-free** (no `<a class="cite-ref">` or `<span class="cite-ref">` inside it). The
prefix used for the end-of-document container in this skill is `ecs`, so the container id is
`#ecs-sources`. Optional per-section recap blocks live in `#ecs-cite-a` … `#ecs-cite-l`.
 
---
 
## Step 1 — Resolve companies
 
For each company name provided by the user, call `findEntity` to get the canonical entity name
and entity ID (use the canonical name throughout the report).
 
Collect 2–5 companies. If the user gives fewer than 2, ask for more.
 
---
 
## Step 2 — Read the template
 
Read `assets/template.html` (relative to this skill directory) once. Keep its exact structure —
CSS, `<head>`, hardcoded TOC, section order, table skeletons, row labels, and element IDs — as
the scaffold for the final artifact. Do **not** copy it to the workspace and do **not** open it.
 
---
 
## Step 3 — Gather earnings call transcripts
 
For each company, fire the following calls in a single parallel batch (one message, many tool calls):
 
### Earnings call transcript (×4 per company) — primary source
| Category label        | Keywords                                                                                            |
|-----------------------|-----------------------------------------------------------------------------------------------------|
| Revenue & Price       | `Revenue, Net Sales, Sales, Volumes, Units sold, Price, Pricing`                                    |
| Sector & Market       | `Industry, Sector Performance, Demand, Market Condition`                                            |
| Supply Chain & Region | `Supply Chain, Materials, Tariffs, Input, Logistics, Regional Performance, Geographic Condition, Geography` |
| Guidance & Events     | `Business Outlook, Guidance, Revision, Corporate Events, Transaction`                               |
 
### Web search fallback (only if `searchEntityEarningsCall` returns nothing usable)
 
If — and only if — `searchEntityEarningsCall` returns no usable transcript content for a given
company, run `web_search` to locate that company's most recent earnings call transcript on the
web, and extract the transcript text from the result. The web search must be scoped solely to
finding the earnings call transcript for that entity — not to news, analyst commentary, credit
opinions, or any other content.
 
**Apply the 100-day recency rule:** check the date of the transcript located via `web_search`.
If the transcript is older than 100 days from today, discard it and treat the transcript as
unavailable for that company. Do not substitute any other source.
 
All synthesis in Step 4 must be derived exclusively from the transcript content gathered in
this step (either via `searchEntityEarningsCall` or, where applicable, the web_search
fallback). No other tools may be called.
 
### Missing-tool handling
 
If any of the tools required for a section do not exist, inform the user: One or more tools required for this section are not available under your current subscription. Unlock more of the expert insights, data, and analytics you trust. Get [in touch] with us to learn more. The [in touch] should be the link Link:https://www.moodys.com/web/en/us/capabilities/gen-ai/ai-ready-data.html
 
---
 
## Step 4 — Synthesize + emit the complete artifact
 
After data is gathered, write the **entire filled `template.html` document** — with every
element from the streaming protocol populated in place — to a single `.html` file in
`/mnt/user-data/outputs/` using the `create_file` tool, then call `present_files` on that path.
The file is the deliverable; do not also paste the HTML into the chat as a fenced code block.
 
The HTML file **must**:
 
- Be a complete, standalone HTML document (doctype → `</html>`) that renders without external
  dependencies.
- Preserve the template's `<head>` (CSS, fonts), hardcoded TOC, section order, table skeletons,
  row labels, and element IDs exactly. Only the empty targets defined below are populated.
- Be written in a single `create_file` call (no progressive `str_replace` edits, no
  multi-file split).
Render order of content inside the file follows the page top-to-bottom so the artifact is
human-readable as well as browser-renderable: cover/TOC fields first, then sections 1 → 13, then
sources.
 
Use earnings call transcript content as the **sole** source for every section. Do not enrich
with credit, sector outlook, ESG, peer, or news data — those tools are not permitted in this
skill. Write in professional financial language. Name specific companies in bullets rather
than speaking abstractly.
 
Attribute substantive claims with numbered citation references. The exact inline markup, the
URL-less fallback, and the rule that `n` matches the row position of the source inside
`#ecs-sources` are defined in [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md).
 
### Cover / header fields (write first)
- `#ecs-report-date` — e.g. `April 4, 2026` (plain text)
- `#ecs-footer-date` — same value (plain text)
- `#ecs-company-count` — number of companies (plain text)
- `#ecs-company-chips` — one `<span class="company-chip">Company Name</span>` per company (space-separated)
- `#ecs-cover-img-right`, `#ecs-cover-img-bottom` — optional. If you have image URLs or data URIs
  to use, set the `src` attributes **and** add the `has-cover-image` class to the corresponding
  container (`<div class="cover-top has-cover-image">` and/or `<div class="cover-bottom has-cover-image">`).
  If you do not have images, leave the template as-is — the empty image strips will collapse
  automatically and the cover will render as a clean navy block with the accent bar.
### Section synthesis rules
 
> **Per-section omit rule (applies to every section a–l).** If a company's earnings call
> transcript exists but does not contain information relevant to a given section, **omit
> that company from that section entirely** — do not emit a row, subtitle, bullet, or any
> "Not disclosed" placeholder for it. The section may legitimately cover fewer companies
> than the full set. (Companies whose transcript could not be located at all are handled
> per rule **a** and are excluded from every section.)
 
**a. Executive Summary** → `#ecs-executive-summary`
**Exactly one combined `<p>` paragraph of 100 words or less** that summarises the entire contents of the newsletter across all covered companies. **Do NOT write one paragraph per company** and do NOT structure it as a per-company recap — it must be a single, general, combined summary of the whole report based solely on the earnings call transcript content. May carry inline `<a class="cite-ref">[n]</a>` hyperlink citations.
If the earnings call transcript for any requested company could not be located (neither via `searchEntityEarningsCall` nor a web_search result within the 100-day window), **explicitly note that fact in the Executive Summary** (e.g., "An earnings call transcript for {Company X} could not be located and it is therefore not covered in this report."). That company must then be **omitted from every other section** — no row in the YOY tables, no subtitle, no bullets, no placeholder.
 
**b. Overall Credit Consideration** → `#ecs-credit-badge` + `#ecs-overall-credit`
Answer the question: **Are conditions in the industry and macro-environment credit positive, negative, or neutral?** Determine the answer **solely from the earnings call transcript content**, by looking across all covered companies for industry-wide trends and patterns.
Write the sentiment badge into `#ecs-credit-badge` (see snippet below).
Write one intro `<p>` (≤250 chars) that gives an overview with a **clearly formed opinion** on whether industry/macro conditions are credit positive, negative, or neutral, followed by a `<ul>` of **exactly 5 `<li>` bullets** (≤150 chars each) into `#ecs-overall-credit` that **list the five considerations supporting that view**. The intro paragraph and each bullet may carry inline citations.
**The view and every supporting consideration must be derived from trends or patterns observed across the covered companies — i.e., the industry as a whole.** Do **not** extrapolate isolated events that apply to just one company into an industry-level claim. Group companies that share a dynamic into a single bullet (e.g., "Company A and Company B both cite easing input cost pressure …"). Do **not** write one bullet per company.
Draw exclusively on the earnings call transcript. Do not consult credit opinions, sector outlooks, or any other tool.
 
**c. Revenue YOY Trend** → `#ecs-tbody-revenue`
One `<tr>` per company: company-wide YOY revenue change (`+X.XX%` / `-X.XX%` / `Up` / `Down` / `Flat` / `Not specified`) and a 70–90 char commentary. Not segment-specific. The commentary cell may carry inline citations; the numeric `.yoy-change` cell stays citation-free.
 
**d. Volumes YOY Trend** → `#ecs-tbody-volumes`
Same row format as (d) but for sales volumes. The commentary cell may carry inline citations; the numeric `.yoy-change` cell stays citation-free.
 
**e. Selling Price Trend** → `#ecs-tbody-prices`
Same row format as (d) but for selling prices. The commentary cell may carry inline citations; the numeric `.yoy-change` cell stays citation-free.
 
**f. Qualitative / Broad Industry Commentary on Revenue, Volumes & Pricing** → `#ecs-qualitative`
Exactly three paragraphs in this fixed order: **a. Revenue, b. Volumes, c. Pricing**. Each paragraph **must give a general view of the industry** in which the covered companies operate — i.e., synthesise the cross-company patterns observed in the earnings call transcripts into an industry-level commentary, not a per-company recap. **Each paragraph must be between 200 and 300 characters.**
Prefix each paragraph with a `<strong class="subsection-title">Revenue</strong>` (etc.) subheader. Derive macro framing exclusively from cross-company observations in the earnings call transcripts. Each paragraph may carry inline citations.
 
**g. End Market Conditions** → `#ecs-end-markets`
Exactly four thematic commentaries describing the market conditions in which the covered companies operate. Each commentary has a `<strong class="subsection-title">…</strong>` subheader (≤70 chars summarising the bullets) + a `<ul>` with **at least 2 `<li>` bullets**. **Combined bullet length per commentary: 250–300 characters.** Derive narratives exclusively from the earnings call transcripts. Each bullet may carry inline citations.
**Provide your view on the trends or patterns observed across all covered companies** — these commentaries must reflect cross-company industry dynamics, not isolated single-company facts repackaged.
**Each bullet (and every comment) must explicitly name the company or companies it applies to** by stating the company name directly within the sentence. If two or more companies share the dynamic, name all of them in the same bullet. Do not write company-agnostic bullets.
 
**h. Supply Chain Conditions** → `#ecs-supply-chain`
**Emit exactly three important thematic commentaries**, each covering one of the following topic areas: **(1) Raw Materials / Input Costs, (2) Trade Relations / Tariffs, or (3) Impact on Business Operations**. Pick the three most relevant topics surfaced in the transcripts (the three may be the three distinct topics above, or any combination drawn from them where the same topic recurs across companies in materially different ways). Each commentary has a `<strong class="subsection-title">…</strong>` subheader (≤70 chars summarising the bullets) + a `<ul>` with **at least 2 `<li>` bullets**. **Combined bullet length per commentary: 200–250 characters.** Each bullet may carry inline citations.
**Provide your view on the trends or patterns observed across all covered companies** — these commentaries must reflect cross-company industry dynamics, not isolated single-company facts repackaged.
**Each bullet (and every comment) must explicitly name the company or companies it applies to** by stating the company name(s) directly within the sentence. **Mention the name of the specific companies that are facing the event being described in each point.** If two or more companies share the dynamic, name all of them in the same bullet — e.g., `Company A and Company B are both investing in AI and digital transformation to streamline operations and lower delivery costs.` Do not write company-agnostic bullets.
 
**i. Business Conditions by Geography** → `#ecs-geography`
Summarise the general conditions of the market by geography. Emit exactly four regional blocks, in this order: **North America**, **Latin America**, **Europe, Middle East and Africa**, **Asia Pacific**. No other regions may be added; do not split or rename these four. Each block has a `<strong class="subsection-title">…</strong>` subheader of **no more than 70 characters that summarises the bullets below** (single line, no trailing period). Then a `<ul>` with **at least 2 `<li>` bullets**, **200–250 characters combined per region**, opens directly after the `</strong>`. Each bullet may carry inline citations.
**Provide your view on the trends or patterns observed across all covered companies** — each regional block must reflect cross-company observations of conditions in that geography, not a single-company anecdote.
**Each bullet (and every comment) must explicitly name the company or companies it applies to** by stating the company name(s) directly within the sentence. **Mention the name of the specific companies that are facing the event being described in each point.** If two or more companies share the dynamic in that region, name all of them in the same bullet. Do not write company-agnostic bullets.
If none of the covered companies discussed a given region on their earnings call, **omit that region's block entirely** rather than emitting an empty subheader.
 
**j. Next Quarter & Full Year Business Outlook / Guidance** → `#ecs-outlook`
One commentary per company (≥2 bullets, 200–250 chars combined). Include next-quarter AND full-year guidance as stated on the earnings call. Include quantitative data where available in the transcript. Each bullet may carry inline citations.
The `<strong class="subsection-title">…</strong>` subtitle **must be a single line in the form `Company Name: Short General Summary`**, where the summary is a brief, general descriptor (≤80 chars, no trailing period) of what the bullets below cover. The summary lives **inside** the `<strong>` tag, joined to the company name by a colon — it is part of the subtitle itself, not a separate sentence underneath. Example: `<strong class="subsection-title">Company Name: Focused on AI-Driven Turnaround and Pipeline Conversion</strong>`. The `<ul>` of bullets opens directly after the `</strong>`.
 
**k. Earnings Revisions for Applicable Companies** → `#ecs-revisions`
One commentary per company that revised earnings (≥2 bullets, 200–250 chars combined). Each bullet may carry inline citations.
The `<strong class="subsection-title">…</strong>` subtitle **must be a single line in the form `Company Name: Short Summary`**, where the summary is a brief descriptor (≤80 chars, no trailing period) of the revisions covered in the bullets below. The summary lives **inside** the `<strong>` tag, joined to the company name by a colon — it is part of the subtitle itself, not a separate sentence underneath. Example: `<strong class="subsection-title">Company Name: Narrowed Revenue Decline, Raised Free Cash Flow Guidance</strong>`. The `<ul>` of bullets opens directly after the `</strong>`.
Whenever a bullet states that management **raised or lowered a specific financial metric** (revenue, EPS, margin, FCF, capex, etc.), it **must support the claim with the quantitative data point from the transcript when available** — include the new figure, the prior figure, and/or the magnitude of change (e.g., `raised FY revenue guidance to $12.4B from $12.1B (+2.5%)`). Only omit the figure if the transcript itself does not provide it.
If a company did not make or did not mention any revision in its earnings call transcript, **omit that company entirely from this section** — do not emit a subtitle, summary sentence, bullets, or any "No revisions disclosed" placeholder for it.
 
**l. Corporate Events** → `#ecs-events`
One commentary per company with relevant events (≥2 bullets, 300–350 chars combined).
Cover M&A, restructurings, plant closures, force majeures **as discussed on the earnings call**. Each bullet may carry inline citations.
The `<strong class="subsection-title">…</strong>` subtitle **must be a single line in the form `Company Name: Short Summary`**, where the summary is a brief descriptor (≤80 chars, no trailing period) of the events covered in the bullets below. The summary lives **inside** the `<strong>` tag, joined to the company name by a colon — it is part of the subtitle itself, not a separate sentence underneath. Example: `<strong class="subsection-title">Company Name: Closed Target Co. Acquisition and Restructured EMEA Operations</strong>`. The `<ul>` of bullets opens directly after the `</strong>`.
 
### Citations & sources (write last)
 
- `#ecs-cite-a` … `#ecs-cite-l` — optional per-section recap blocks. Use the
  `<div class="section-citations">…</div>` markup defined in
  [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md). Omit any section's block
  if empty.
- `#ecs-sources` — end-of-document Citations rows. One `<div class="source-item">` per
  source, in `[1], [2], …` order, using the canonical row markup from the shared citations
  skill.
---
 
## Streaming protocol (element → content mapping)
 
| Element ID                       | Content type                                                       |
|----------------------------------|--------------------------------------------------------------------|
| `#ecs-report-date`               | Plain text date                                                    |
| `#ecs-footer-date`               | Plain text date (same value)                                       |
| `#ecs-company-count`             | Plain text integer                                                 |
| `#ecs-company-chips`             | Sequence of `<span class="company-chip">…</span>`                  |
| `#ecs-cover-img-right`           | `<img>` element — set `src` attribute                              |
| `#ecs-cover-img-bottom`          | `<img>` element — set `src` attribute                              |
| `#ecs-executive-summary`         | One or more `<p>`; prose may carry inline citations |
| `#ecs-credit-badge`              | Single `<div class="credit-badge …">` element                      |
| `#ecs-overall-credit`            | `<p>` intro + `<ul><li>` bullets; prose may carry inline citations |
| `#ecs-tbody-revenue`             | `<tr>` rows with `.yoy-change` class; commentary cell may carry inline citations |
| `#ecs-tbody-volumes`             | `<tr>` rows with `.yoy-change` class; commentary cell may carry inline citations |
| `#ecs-tbody-prices`              | `<tr>` rows with `.yoy-change` class; commentary cell may carry inline citations |
| `#ecs-qualitative`               | `<strong class="subsection-title">` + `<p>` (×3); prose may carry inline citations |
| `#ecs-end-markets`               | `<strong class="subsection-title">` + `<ul><li>` (×4); bullets may carry inline citations |
| `#ecs-supply-chain`              | `<strong class="subsection-title">` + `<ul><li>` (×3); bullets may carry inline citations |
| `#ecs-geography`                 | `<strong class="subsection-title">Region: Summary</strong>` + `<ul><li>` (×4 fixed regions); bullets may carry inline citations |
| `#ecs-outlook`                   | `<strong class="subsection-title">` + `<ul><li>` per company; bullets may carry inline citations |
| `#ecs-revisions`                 | `<strong class="subsection-title">` + `<ul><li>` per company; bullets may carry inline citations |
| `#ecs-events`                    | `<strong class="subsection-title">` + `<ul><li>` per company; bullets may carry inline citations |
| `#ecs-cite-a` … `#ecs-cite-l`    | `<div class="section-citations">…</div>` (optional, see shared citations skill) |
| `#ecs-sources`                   | `<div class="source-item">` rows (see shared citations skill)      |
 
### Reference HTML snippets
 
**YOY table row** (`#ecs-tbody-revenue`, `#ecs-tbody-volumes`, `#ecs-tbody-prices`):
 
```html
<tr>
  <td class="company-name">Company A</td>
  <td class="yoy-change up">+5.20%</td>
  <td>Revenue growth driven by pricing gains in North America <a href="https://example.com/transcript-q1-2026" target="_blank" class="cite-ref">[1]</a>, partially offset by volume declines in EMEA <a href="https://example.com/credit-opinion-a" target="_blank" class="cite-ref">[2]</a>.</td>
</tr>
```
 
**Company chip** (`#ecs-company-chips`):
 
```html
<span class="company-chip">Company A</span>
```
 
**Credit sentiment badge** (`#ecs-credit-badge`):
 
```html
<div class="credit-badge positive">Positive</div>
```
 
**Subsection subheader inside prose containers**:
 
```html
<strong class="subsection-title">North America</strong>
<ul>
  <li>Retail demand held up against tariff pass-through <a href="https://example.com/transcript-q1-2026" target="_blank" class="cite-ref">[1]</a>.</li>
  <li>Pricing remained disciplined across grocery and consumables <a href="https://example.com/sector-outlook" target="_blank" class="cite-ref">[3]</a>.</li>
</ul>
```
 
**Section citations recap** (`#ecs-cite-a` … `#ecs-cite-l`) and **sources rows**
(`#ecs-sources`): see [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md) for the
canonical markup. Reuse the same `[n]` numbering across inline references, optional recap
blocks, and the end-of-document Citations block.
 
### Class-selection rules
 
**`.yoy-change`** modifier (on the second `<td>` of YOY rows):
- `up` — value starts with `+`, equals `Up`, or parses to a positive number
- `down` — value starts with `-`, equals `Down`, or parses to a negative number
- `flat` — value equals `Flat` or `0`
- `na` — value is `Not specified`, `N/A`, empty, or `—`
**`.credit-badge`** modifier (for `#ecs-credit-badge`):
- `positive`, `negative`, or `neutral`. Label text is the capitalized sentiment.
### Conventions
 
- Use `<p>` for paragraphs, `<ul><li>` for bullets, `<strong class="subsection-title">…</strong>` for bold subheaders inside prose containers.
- Emit inline citations per [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md). Inline citations are the primary attribution mechanism — the optional per-section blocks (`#ecs-cite-a` … `#ecs-cite-l`) remain available as supplementary summary boxes. Numeric `.yoy-change` cells stay citation-free.
- Do NOT include overall section titles — the template already has those.
- `yoy_change` values: `+X.XX%` or `-X.XX%` if numeric, else `Up` / `Down` / `Flat` / `Not specified`.
---
 
## Step 5 — Tell the user
 
After `present_files` returns, add a single short sentence in chat confirming the report is
ready (e.g. `Earnings Call Summary for {Company A}, {Company B}, … — the report is available
above as a self-contained HTML artifact.`). Do not paste the HTML into chat and do not suggest
shell commands. The presented file itself is the deliverable.
 
---
 
## Tips
 
- Run ALL data-gathering tool calls in a single parallel batch (one message, many tool calls).
- Emit the final HTML as a single `.html` file written to `/mnt/user-data/outputs/` and
  surfaced via `present_files` — do not paste it inline as a fenced code block, do not stream
  partial sections, do not split across multiple files or messages.
- If `searchEntityEarningsCall` returns no usable transcript for a company, fall back to
  `web_search` **only** to retrieve that company's earnings call transcript from the web, and
  apply the 100-day recency rule. If no transcript can be located within that window, note
  the omission in the Executive Summary and exclude that company from every other section
  (no rows, no subtitles, no placeholders).
- Do not call any other MCP tool (no credit opinion, no sector outlook, no news, no peers, no
  ESG, no document search) — those sources are out of scope for this skill.
- Pick the correct `.yoy-change` / `.credit-badge` modifier class yourself using the rules above — the template no longer does this at render time.
- Emit `<tr>` rows directly inside each `<tbody id="ecs-tbody-…">` placeholder; do not re-create the `<table>` or `<thead>`.
- Inline citations follow the shared citations skill — read [skills/shared/citations/SKILL.md](../shared/citations/SKILL.md) before authoring any `[n]` reference or the Citations block.
