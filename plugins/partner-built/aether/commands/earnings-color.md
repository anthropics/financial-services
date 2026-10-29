---
description: Surface CEO/CFO/analyst commentary on a topic from earnings-call transcripts, quoted verbatim with speaker and date
argument-hint: "<topic> [ticker e.g. NVDA] [lookback quarters e.g. 4]"
---

# Earnings Color

> Uses the Aether `transcript_search` tool. See [CONNECTORS.md](../CONNECTORS.md) for parameters.

Pull forward-looking commentary — guidance, narrative, tone — from earnings-call transcripts
that 10-K/10-Q filings don't capture. See the **earnings-transcript-research** skill for guidance
on separating reported results from outlook.

## Workflow

### 1. Gather Input
- Topic / question (required).
- Optional: ticker, lookback window (quarters), speaker role of interest (CEO / CFO / Analyst).

### 2. Search
Call `transcript_search` with:
- `query`: the topic phrased naturally.
- `ticker`: if the user named a company.
- `lookback_quarters`: if the user wants recent calls only (e.g. 4).
- `speaker_role`: if they want only management (`CEO`/`CFO`) or only `Analyst` questions.
- `limit`: 10.

### 3. Synthesize
- Quote speaker turns **verbatim**.
- Attribute each: ticker, speaker name + role, and call date.
- Distinguish management assertions from analyst questions; flag hedged or conditional language.

## Output Format

Lead with a 1-2 sentence read on management's stance, then:

| Quote | Speaker (role) | Ticker | Call date |
|-------|----------------|--------|-----------|
| "…" | … (CEO) | … | … |

Close by noting where commentary is consistent vs shifting across quarters, and any topics
management notably avoided.
