---
description: Find public companies disclosing exposure to a supply-chain risk, grouped by ticker
argument-hint: "<risk e.g. rare-earth magnets from China>"
---

# Supply-Chain Exposure

> Uses the Aether `financial_search` tool in supply-chain mode. See [CONNECTORS.md](../CONNECTORS.md).

Find public companies whose SEC filings disclose exposure to a given supply-chain risk, then
rank and group the evidence by ticker. See the **sec-filings-research** skill for retrieval
guidance.

## Workflow

### 1. Gather Input
- The risk or dependency (required) — e.g. a region, supplier, input, or chokepoint.

### 2. Search
Call `financial_search` with:
- `query`: the risk phrased naturally (e.g. "dependence on rare-earth magnets sourced from China").
- `domain`: `supply_chain`.
- `return_format`: `section`.
- `limit`: 25 (cast wider — you're surveying the universe, not one company).

### 3. Synthesize
- Group hits by ticker; keep the single most relevant **as-filed** passage per company.
- Rank by relevance and recency.
- Quote verbatim with filing citation; do not infer exposure that isn't disclosed.

## Output Format

| Ticker | Most relevant disclosure (as-filed) | Filing | Date |
|--------|--------------------------------------|--------|------|
| … | "…" | 10-K | … |

Close with a short read on where exposure clusters, and the limits of the search (only companies
that *disclose* the risk in the covered corpus appear).
