---
name: news-sentiment
description: |
  Turn a corpus of unstructured financial text — news headlines, press releases, and regulatory filings (8-K / 10-Q / 10-K excerpts) — into a structured, fully source-cited sentiment brief for a ticker or watchlist. Each item gets a sentiment label from a fixed set, a verbatim source quote, entity/relation extraction, and an event tag; the skill then aggregates the distribution, logs notable events, and flags ambiguous or high-impact items for analyst sign-off. Produces an auditable Excel workbook (or deck) staged for human review. Use for systematic news/sentiment reads on a coverage name or list.

  **Perfect for:**
  - Screening a batch of overnight or intraday news across a coverage universe
  - Structuring the sentiment of filings/press releases with an audit trail (quote + source per label)
  - Building the sentiment input that feeds a thesis review, morning note, or a bull/bear thesis review
  - Tracking how the tone around a name shifts over a window of time

  **Not ideal for:**
  - Producing a price target, forecast, or buy/sell/hold call (out of scope — this labels text, it does not predict prices)
  - Deep single-event analysis of one earnings call (use earnings-analysis)
  - Any task requiring live trade signals or execution
---

# News & Filings Sentiment Brief

## Overview

This skill reads a corpus of financial text and produces a **structured, source-cited sentiment brief**: one labelled record per item plus an aggregated summary. It turns Claude's core strength — reading unstructured language and producing auditable structure — into a repeatable equity-research deliverable. It classifies the **stance of each text toward the company/security**, extracts the entities and event involved, and stops deliberately at a decision-ready artifact for a human analyst. It does **not** forecast prices or issue recommendations.

The full labeling rubric, confidence scale, event ontology, and worked examples live in [references/labeling-guide.md](references/labeling-guide.md). **Read it before labeling.**

## ⚠️ CRITICAL: Data Source Priority (READ FIRST)

**ALWAYS follow this data source hierarchy for the underlying news/filings:**

1. **FIRST: Check for MCP data sources** — if MT Newswires, Aiera, S&P Kensho, FactSet, or similar news/filings MCP servers are available, use them exclusively to source headlines, articles, and filings.
2. **DO NOT use web search** if the above MCP data sources are available.
3. **ONLY if MCPs are unavailable:** use SEC EDGAR filings, the company IR site, or other institutional sources.
4. **NEVER fabricate a headline, quote, or filing.** Every labelled item must trace to a real source with a verbatim quote. If you cannot source the text, do not invent it — omit it and note the gap.

## When to Use This Skill (and how it differs)

- Use this to **label a whole corpus** of news/filings systematically, with an audit trail. It is not a single-document report.
- `earnings-analysis` produces one deep report on one quarter's results; `morning-note` and `thesis-tracker` *consume* conclusions. **None of them systematically labels a corpus of items with per-item sentiment and citations** — that is this skill's gap.
- Its output is a clean input to a downstream bull/bear thesis review and to `thesis-tracker`.

## Tools

- Default to the user-provided text and the MCP news/filings servers for sourcing. Never invent source material.

## Critical Constraints — Read These First

**No forecast, no recommendation (the boundary):**
- This skill labels the sentiment *expressed in the text*. It does **not** predict price direction, set a target, or issue a buy/sell/hold view. If asked to, decline and produce the labelled brief instead — staged for a human to judge.

**Every label carries a verbatim source quote + citation:**
- For each item, capture the exact sentence(s) that justify the label, plus source and date. A label without a quote is not acceptable — the bundled validator fails any item with an empty `source_quote`.

**Label the text's stance, not your own view:**
- Sentiment reflects how the *article/filing* frames the company. Do not inject your opinion, and do not infer sentiment from a subsequent price move (no hindsight/lookahead leakage).

**Use the fixed label set — do not invent labels:**
- Sentiment ∈ `{positive, neutral, negative, mixed}`. Use `mixed` for genuinely two-sided items; use `neutral` for purely factual/procedural items. Event tags come from the taxonomy in the labeling guide (use `other` when unsure).

**Separate fact from opinion, and flag uncertainty:**
- Distinguish reported facts from editorial/analyst opinion. Set `confidence` honestly and set `needs_review = yes` for ambiguous, sarcastic, forward-looking, contradictory, or high-impact items so a human checks them.

**Watch the classic NLP traps:** negation ("not without risk"), forward-looking vs realized, company voice vs third-party/analyst voice, boilerplate risk-factor language in filings (usually `neutral`, not `negative`), and headlines that contradict the body (label the body; flag the divergence).

## Sentiment Analysis Workflow

### Step 1: Assemble & de-duplicate the corpus
Collect the items (headlines, articles, filing excerpts, transcript snippets) for the ticker/watchlist and window. Remove duplicates and syndicated reprints; keep the earliest/primary source.

### Step 2: Label each item
For every item, in order: pull the **verbatim source quote** → assign the **sentiment** label (+ optional −1…+1 `sentiment_score` and `confidence`) → extract **entities** (companies/tickers/people) and the key relation (who did what to whom) → tag the **event_type** from the taxonomy. See [references/labeling-guide.md](references/labeling-guide.md) for the rubric and edge cases.

### Step 3: Aggregate
Compute the sentiment distribution and (optionally) a net score, build a **notable-event log** (highest-impact items), and, when items span time, a simple tone-over-time view.

### Step 4: Flag for human review
Mark low-confidence, ambiguous, contradictory, and high-impact items `needs_review = yes`. Call these out explicitly in the summary.

### Step 5: Assemble the deliverable
Produce the Excel workbook (schema below) — or a short deck — with the per-item table and the aggregated summary. Render it to a standalone `.xlsx` (or deck) using your spreadsheet/deck-authoring tooling when there is no live Excel session.

## Label Set, Confidence & Event Taxonomy (summary)

- **sentiment:** `positive` | `neutral` | `negative` | `mixed`
- **sentiment_score (optional):** −1.0 … +1.0 on a single shared boundary of ±0.15 — positive > +0.15, negative < −0.15, neutral within ±0.15; `mixed` is a net figure read from the label, not the band
- **confidence:** `low` | `medium` | `high` (or a 0–1 value, higher = more confident)
- **event_type:** `earnings`, `guidance`, `m&a`, `litigation`, `management`, `product`, `regulatory`, `macro`, `capital-return`, `rating-change`, `other`

Full definitions, the scoring rubric, and worked examples are in [references/labeling-guide.md](references/labeling-guide.md).

## Output / Deliverable

A **`Sentiment`** worksheet with one row per item and this header row (the bundled validator checks it):

| Column | Required | Notes |
|---|---|---|
| `id` | ✅ | stable item number |
| `source` | ✅ | publisher / document |
| `date` | | publication/filing date |
| `sentiment` | ✅ | one of the four labels |
| `sentiment_score` | | −1…+1, sign-consistent |
| `confidence` | | low/medium/high |
| `event_type` | | from the taxonomy |
| `source_quote` | ✅ | **verbatim** justifying quote |
| `entities` | | companies/tickers/people |
| `needs_review` | | yes/no |

Plus a **Summary** section: item count, sentiment distribution, notable-event log, and the list of items flagged for review.

## Validation

Run the bundled validator before delivery:
```
python scripts/validate_sentiment.py brief.xlsx
```
It confirms the required columns exist, every `sentiment` is in the fixed label set, every item has a non-empty `source_quote`, and any `sentiment_score` is in `[-1, 1]` (enforced as an error). It additionally flags — as warnings — a score inconsistent with its label (the ±0.15 boundary), a low-confidence or `mixed` item not marked `needs_review = yes`, and a malformed `confidence`/`event_type`. Exit `0` = PASS. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Correct Patterns
- **Every label is quote-backed and sourced** — the quote is the evidence, and it must be verbatim.
- **Label the text's stance**, using only the fixed label set; `mixed` for two-sided, `neutral` for factual.
- **Honest confidence**, with ambiguous/high-impact items flagged for review.
- **Aggregate transparently** — show the distribution and the notable-event log, not just a single net number.
- **Stop at the brief** — hand a decision-ready artifact to the analyst; never a price call.

## Common Mistakes
- **Issuing a recommendation or price target** — out of scope; produce the labelled brief instead.
- **A label with no source quote** — fails validation and destroys auditability.
- **Treating boilerplate filing risk-factors as `negative`** — standard disclosure is usually `neutral`.
- **Missing negation or forward-looking framing** ("not without risk", "expects to") and mislabeling as a result.
- **Confusing company voice with third-party/analyst voice.**
- **Hindsight leakage** — inferring sentiment from what the stock did afterward.
- **Inventing sentiment_score precision** that the text doesn't support — set `confidence: low` instead.

## Workflow Integration
- **→ `thesis-tracker`:** the labelled sentiment feeds a downstream thesis update or a bull/bear thesis review.
- **→ `morning-note`:** the notable-event log and net tone drop straight into a morning note.
- **→ rendering:** output the brief as a standalone `.xlsx` or deck using your spreadsheet/deck-authoring tooling.

## Guardrails
- This skill produces **decision-support**, not investment advice. It labels the sentiment of text; it does not forecast prices, recommend, or transact.
- **Every output is staged for human sign-off.** Every label is quote-backed; ambiguous and high-impact items are flagged for review.
- **Never fabricate source material.** If the text cannot be sourced from an authorised provider, omit it and note the gap rather than inventing a headline or quote.
