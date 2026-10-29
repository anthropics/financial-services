# News & Filings Sentiment — Labeling Guide

The rubric behind the `news-sentiment` skill. It defines the label set, the scoring and confidence scales, the entity/relation schema, the event taxonomy, and the edge cases that most often cause mislabeling. Read it before labeling a corpus.

Core principle: label the **stance the text takes toward the company/security**, backed by a verbatim quote — not your own view, and never inferred from a later price move.

## 1. Sentiment labels

The optional numeric score uses one shared boundary, **t = 0.15**, so every non-`mixed` score maps to exactly one label (disjoint and exhaustive):

| Label | Use when | Score band |
|---|---|---|
| **positive** | The text frames the news as favorable (beat, raise, win, upgrade, buyback) | score > +0.15 (typically +0.3 … +1.0) |
| **negative** | The text frames the news as unfavorable (miss, cut, loss, downgrade, probe, lawsuit) | score < −0.15 (typically −1.0 … −0.3) |
| **neutral** | Purely factual / procedural, or no clear valence (schedule set, routine 8-K, boilerplate) | −0.15 ≤ score ≤ +0.15 |
| **mixed** | Genuinely two-sided in the *same* item (beat revenue, missed margin; acquisition funded with dilution) | net figure — **read from the label, not the band** (see §2) |

Rules of thumb:
- Prefer `neutral` over a weak `positive`/`negative` when the valence is not clear from the text.
- Use `mixed` only when both a clear positive **and** a clear negative appear in the *same* item — it is not a synonym for "uncertain" (that is low `confidence`).

## 2. Sentiment score (optional, −1.0 … +1.0)

A continuous strength for the label, on the single boundary above: `positive` iff score > +0.15, `negative` iff score < −0.15, `neutral` iff |score| ≤ 0.15. Magnitude reflects intensity/materiality (a small pre-announced dividend bump ≈ +0.2; a surprise takeover premium ≈ +0.8). If the text can't support a precise number, omit the score and set `confidence: low`.

**`mixed` is the exception:** its score is a *net* of offsetting positives and negatives, so it is read from the **label**, not the band, and is **excluded** from the boundary check and from the net-score average (§8). A `mixed` item whose net |score| exceeds 0.5 is probably really positive/negative — reconsider the label. (The bundled validator enforces the range as an error and flags band/label inconsistency and large `mixed` magnitudes as warnings.)

## 3. Confidence

Enum `high` / `medium` / `low`, or a numeric value in (0, 1] where **higher = more confident** (low ≤ 0.34, medium 0.34–0.66, high > 0.66; 0 is not a valid confidence). `high` — unambiguous, single-voiced, clearly material. `medium` — some interpretation needed. `low` — ambiguous, sarcastic, heavily hedged, forward-looking, or thin sourcing.

**Mandatory review flag:** any `low`-confidence item, any `mixed` item, and any high-impact item **must** carry `needs_review = yes`. The validator warns when a low-confidence or `mixed` item is left unflagged — this is the invariant the human review queue depends on.

## 4. Entities & relations

For each item capture the **entities** (subject company + ticker, counterparties, people, regulators) and the key **relation** — who did what to whom (e.g. "Regulator X opened a probe into Company Y", "Company Y agreed to acquire Company Z"). Distinguish the **subject** of your brief from third parties mentioned; sentiment is scored toward the subject.

## 5. Event taxonomy (`event_type`)

`earnings` (reported results) · `guidance` (forward outlook change) · `m&a` (merger/acquisition/divestiture) · `litigation` (a filed lawsuit or legal claim) · `management` (exec/board change) · `product` (launch, recall, pipeline) · `regulatory` (regulator action, approval, or **investigation/probe**) · `macro` (rates, FX, sector-wide) · `capital-return` (buyback, dividend) · `rating-change` (analyst or credit rating) · `other` (use when none fit; do not force a category).

Multiple tags are allowed (comma-separated), but only when each genuinely applies — do not over-tag. A regulator's **investigation** is `regulatory`, not `litigation`; use `litigation` only once a suit or formal legal claim is filed. Use `other` rather than mislabeling.

## 6. Edge cases (the usual traps)

- **Negation:** "results were *not* without disappointment" is negative; "*not* a strong quarter" is negative. Parse the negation, don't keyword-match.
- **Forward-looking vs realized:** "expects headwinds next year" is a guidance-tinged signal, often `negative`/`mixed` with `medium`/`low` confidence — distinguish from a realized miss.
- **Company voice vs third-party voice:** a bullish company press release and a skeptical analyst note about the same event get **separate** rows with their own labels.
- **Filing boilerplate:** standard 10-K/10-Q risk-factor and forward-looking-statement language is disclosure, not news — usually `neutral`. Label only substantive, item-specific disclosures.
- **Headline vs body divergence:** label the **body**; if the headline materially oversells/undersells the body, set `needs_review = yes` and note it.
- **Sarcasm / rhetorical framing:** low confidence; flag for review.
- **Mixed materiality:** a positive item that is immaterial (routine, tiny) should carry a small score, not a large one.

## 7. Worked examples

| Source quote (verbatim) | sentiment | score | confidence | event_type | needs_review |
|---|---|---|---|---|---|
| "Q2 revenue of $2.1B beat consensus of $1.95B and the company raised full-year guidance." | positive | +0.7 | high | earnings, guidance | no |
| "The company disclosed that the SEC has opened a formal investigation into its revenue-recognition practices." | negative | −0.7 | high | regulatory | yes |
| "The board declared a regular quarterly dividend of $0.25, unchanged from the prior quarter." | neutral | 0.0 | high | capital-return | no |
| "Revenue rose 12% but operating margin fell 300 bps as input costs climbed." | mixed | +0.05 | medium | earnings | yes |
| "This 10-Q contains forward-looking statements subject to risks and uncertainties described in Item 1A." | neutral | 0.0 | high | other | no |

Note the `mixed` row: it carries `needs_review = yes` (mandatory for `mixed`), and its near-zero net score is not a `neutral` signal — its label, not its score, tells the reader it is two-sided.

## 8. Aggregation

After labeling, report: the **sentiment distribution** (counts by label); an optional **net score** computed as the average of the **non-`mixed`** item scores (mixed items are read from their label and excluded so a two-sided net can't distort the aggregate); a **notable-event log** (the highest-|score| / highest-materiality items with their quotes); and — when items span time — a simple tone-over-time series. Always surface the **review queue** (every `needs_review = yes` item, which includes all `mixed` and low-confidence items) so the analyst sees exactly what to check before relying on the brief.
