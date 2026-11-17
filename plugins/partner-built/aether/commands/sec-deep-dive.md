---
description: Pull the most relevant 10-K/10-Q/8-K sections on a topic for a company, with as-filed quotes and filing citations
argument-hint: "<ticker e.g. AAPL> <topic e.g. supply-chain risk in Taiwan>"
---

# SEC Deep Dive

> Uses the Aether `financial_search` tool. See [CONNECTORS.md](../CONNECTORS.md) for parameters.

Search a company's SEC filings for a topic and return the most relevant **as-filed** sections,
quoted verbatim with citations. See the **sec-filings-research** skill for retrieval-profile and
return-format guidance.

## Workflow

### 1. Gather Input
- Ticker (required).
- Topic / question (required).
- Optional: filing-type focus (10-K vs 10-Q vs 8-K), recency preference.

### 2. Search
Call `financial_search` with:
- `query`: the topic phrased naturally, scoped to the company (e.g. "Apple supply-chain concentration risk in Taiwan").
- `domain`: `public_equity`.
- `return_format`: `section` (full section context for accurate quoting).
- `profile`: leave default (`hybrid_rerank_tickerprior`).
- `limit`: 10.

If results look thin, widen the query or retry with `return_format: "both"`.

### 3. Synthesize
- Quote the relevant passages **verbatim** — never paraphrase numbers or risk language.
- Attribute every quote: ticker, filing type, section title, and filing URL from the result.
- Group by theme; note disagreements or changes in language across filings if visible.

## Output Format

Lead with a 1-2 sentence answer to the question, then:

| Quote (as-filed) | Filing | Section | Date / URL |
|------------------|--------|---------|------------|
| "…" | 10-K | Risk Factors | … |

Close with a short synthesis: what the filings actually say, and any gaps where the disclosure
is silent. Do not infer beyond the cited text.
