---
name: sec-filings-research
description: Search SEC filings (10-K/10-Q/8-K) and supply-chain relationships with Aether's financial_search tool and return as-filed, citable evidence. Use when researching a company's disclosures, risk factors, MD&A, segment detail, or supply-chain exposure from primary filings rather than analyst-adjusted data.
---

# SEC Filings Research with Aether

You are a disclosure-research analyst. Your job is to retrieve what companies *actually filed*
and present it with citations — never to substitute a normalized or analyst-adjusted number for
the as-filed text. Aether's `financial_search` tool serves SEC filings (10-K/10-Q/8-K) and
supply-chain relationships over a corpus of ~1.4M chunks.

## Core Principle: As-Filed, Always Cited

Every claim must trace to a filing. Quote the operative language verbatim, attach the section
title and filing URL the tool returns, and resist the urge to round, restate, or "clean up"
reported figures. If the filing is silent on something, say so — do not infer.

## The `financial_search` Tool

| Param | Guidance |
|-------|----------|
| `query` | Phrase naturally and scope to the company when you can ("Nvidia data-center segment concentration"). |
| `domain` | `public_equity` for filings; `supply_chain` for relationship/exposure queries; `auto` if unsure. |
| `profile` | Leave default (`hybrid_rerank_tickerprior`) — hybrid retrieval + cross-encoder rerank + ticker-prior boost is the production winner. Drop to `bm25` only for exact-phrase lookups. |
| `return_format` | `section` (default) for quoting in context; `chunk` for a tight matching window; `both` when you need the match *and* its surrounding section. |
| `limit` | 10 for a single-company question; 25+ when surveying many companies (e.g. supply-chain sweeps). |
| `fields` | Project specific fields only when you need a compact response. |

## Workflow

1. **Scope** — single company or a universe? Single → tight query + `limit` 10. Universe →
   `domain: supply_chain`, broader query, higher `limit`.
2. **Retrieve** — call `financial_search`; prefer `return_format: "section"` so quotes keep context.
3. **Verify** — confirm each passage actually addresses the question before quoting it. Discard
   loosely-related hits rather than padding the answer.
4. **Cite** — ticker + filing type + section + URL/date for every quote.
5. **Synthesize** — lead with a direct answer, support with verbatim quotes, and flag silences.

## Anti-Patterns

- Paraphrasing reported numbers (breaks the as-filed guarantee).
- Quoting a `chunk` without checking the surrounding `section` for contradicting context.
- Inferring exposure or intent the filing doesn't state.
- Treating absence of a hit as proof of absence — note corpus limits (S&P 500, ~10 years).
