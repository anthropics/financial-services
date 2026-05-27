---
name: earnings-transcript-research
description: Search earnings-call transcripts with Aether's transcript_search tool for forward-looking management commentary and analyst Q&A. Use when you need guidance, narrative, tone, or color that 10-K/10-Q filings don't capture, quoted verbatim with speaker and call date.
---

# Earnings Transcript Research with Aether

You are an analyst mining earnings calls for what management *said* — guidance, framing, tone,
and the questions analysts pressed on. This is the forward-looking layer that audited filings
omit. Aether's `transcript_search` tool returns ranked verbatim speaker turns with citations.

## Core Principle: Quote the Speaker, Date the Claim

Management commentary is only useful if it's attributed and time-stamped. Quote speaker turns
verbatim, label the speaker and role, and stamp the call date. Distinguish a CEO assertion from
an analyst's premise — they carry very different weight.

## The `transcript_search` Tool

| Param | Guidance |
|-------|----------|
| `query` | Natural language; topic-first ("data-center demand durability"). |
| `ticker` | Scope to a company (e.g. `NVDA`) when the question is single-name. |
| `lookback_quarters` | Restrict to recent calls (e.g. 4) when recency matters; omit for full history. |
| `speaker_role` | `CEO` / `CFO` for management view; `Analyst` to see what the sell-side is probing; `Operator` rarely useful. |
| `limit` | 10 default; raise for cross-company theme sweeps. |
| `profile` | `hybrid` (default) for topical questions; `bm25` for exact-phrase. |

## Workflow

1. **Frame** — guidance vs. reported results vs. analyst concern? Choose `speaker_role` accordingly.
2. **Scope time** — set `lookback_quarters` if the user cares about the latest stance, not history.
3. **Retrieve** — call `transcript_search`.
4. **Separate signal** — split management claims from analyst questions; flag hedged/conditional
   language ("we expect", "should", "if conditions hold").
5. **Cite** — speaker name + role + ticker + call date for every quote.

## Anti-Patterns

- Presenting an analyst's framing as management's view.
- Dropping the call date — outlook commentary ages fast.
- Smoothing hedged language into a hard commitment.
- Mixing transcript color with as-filed numbers without labeling which is which (use the
  `sec-filings-research` skill for the filed figures).
