# News Sentiment Brief — Troubleshooting Guide

**When to read this file:** if `scripts/validate_sentiment.py` reports errors, or the labels don't look right on review.

## Validator Reports Errors

### "Missing required column(s): ..."
- The `Sentiment` sheet's header row (row 1) must contain columns that map to `id`, `source`, `sentiment`, and `source_quote`. The validator accepts common synonyms (e.g. `quote` for `source_quote`, `label` for `sentiment`), but one of each required field must be present. Fix the header row.

### "sentiment '<x>' is not one of [...]"
- Only `positive`, `neutral`, `negative`, `mixed` are allowed. Words like "bullish", "bull", "up", "buy" are not labels — map them to the fixed set (and note that buy/sell language should not appear at all; this skill does not make calls).

### "source_quote is empty"
- Every labelled item must carry a verbatim quote justifying the label. Re-open the source and paste the exact sentence(s). A label without evidence is not acceptable.

### "sentiment_score outside [-1, 1]"
- Scores are bounded to −1…+1. Rescale, or drop the score and set `confidence: low` if the text can't support a precise number.

## Labels Don't Look Right

### Everything is coming out `neutral`
- You may be over-applying `neutral` to items that have a clear valence, or labeling filing boilerplate. Re-read section 6 of the labeling guide (negation, forward-looking, boilerplate) and re-check the body text, not just the headline.

### Label/score consistency warnings
- Scores map to labels on one boundary, ±0.15: `positive` needs score > +0.15, `negative` < −0.15, `neutral` within ±0.15. A warning here means the label and the score disagree — confirm the label matches the quote, then fix whichever is wrong. (`mixed` is exempt: its net score is read from the label, but a `mixed` item with |score| > 0.5 warns because it is probably really positive/negative.)

### "low-confidence / mixed item is not flagged needs_review=yes"
- Every `mixed` item and every low-confidence item **must** carry `needs_review = yes` — that is what populates the human review queue. Set the flag (or, if the corpus genuinely has none to review, confirm the labels/confidence are right). If your table has no `needs_review` column at all, add one; the validator warns when review-worthy items have nowhere to be flagged.

### Too many / too few items flagged for review
- `needs_review = yes` should cover ambiguous, sarcastic, forward-looking, contradictory, and high-impact items. If almost nothing is flagged on a noisy corpus, you are probably over-confident; if everything is flagged, tighten the rubric and raise confidence where the text is clear.

## Wrong Tool
- Deep single-quarter analysis → use `earnings-analysis`.
- A forecast, price target, or buy/sell view → **out of scope**; this skill only labels text and stages it for human judgment.
