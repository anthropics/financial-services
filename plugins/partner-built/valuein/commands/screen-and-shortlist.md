---
description: Run a factor screen across the US universe, forensic-audit the top candidates, and produce a ranked shortlist with citations
argument-hint: "<criteria description e.g. 'high-FCF low-debt' | 'magic formula'> [max_results=10]"
---

# Screen and Shortlist

> This command uses Valuein's `screen_universe`, `forensic_audit`, `get_company_fundamentals`, and `get_peer_comparables` tools. See [CONNECTORS.md](../CONNECTORS.md) for the complete tool reference.

Run a cross-sectional factor screen across the US universe, forensic-audit the top candidates, and return a ranked shortlist with citations. Caller provides the criteria description in natural language; the command translates it into factor weights for `screen_universe` and applies a forensic gate before returning the shortlist.

See the **screen-and-shortlist** skill for domain knowledge on factor design, multi-factor ranking, and forensic gating.

## Workflow

### 1. Gather Input

Ask the user for:
- Criteria description (required). Common shapes:
  - `"high-FCF low-debt"` → FCF yield DESC + debt-to-equity ASC
  - `"magic formula"` → ROIC DESC + earnings yield DESC
  - `"quality momentum"` → ROIC DESC + revenue CAGR (5Y) DESC
  - `"value with safety"` → low P/E + low debt-to-equity + positive ROA
- Max results (optional, default 10).

### 2. Screen the Universe

Call `screen_universe` with factor weights matching the criteria. The tool reads `factor_scores.parquet` which carries pre-computed percentile ranks for the canonical factor catalogue.

Take the top ~30 results before the forensic gate (so the post-gate shortlist still has the requested `max_results` survivors).

### 3. Forensic Gate

For each of the top ~30 candidates (parallelise reads):
- Call `forensic_audit` with `ticker`.
- Drop candidates where:
  - Partial M-Score > -2.22 (manipulation-risk signal), OR
  - Sloan accruals > 7.5% (earnings-quality concern), OR
  - ROA < 0 (operating at a loss).

This is the "screen survivors" set — names that scored well on the quantitative factors AND don't trip forensic-quality red flags.

### 4. Peer-Context Pass

For each survivor (cap to `max_results`):
- Call `get_peer_comparables` with `categories: ["profitability", "valuation"]`.
- Note where the candidate sits in its sector vs peer median (1-sentence per name).

### 5. Synthesize the Shortlist

Combine into the output below.

## Output Format

### Shortlist Header

Display the criteria, factor weights used, screen date, and survivor count.

### Top \<max_results\> Survivors (Ranked)

For each survivor:

#### #1 — \<TICKER\> — \<Company Name\>

- **Factor score**: composite_rank \<value\>, percentile \<n\>th
- **Forensic clean**: M-Score \<value\>, Sloan accruals \<value\>%, ROA \<value\>%
- **Peer context**: 1 sentence on where the name sits vs sector peers
- **Source**: SEC accession id for the latest 10-K (from `forensic_audit` lineage)

Repeat for #2..#N.

### Drops (Failed Forensic Gate)

For each candidate that scored well but failed the forensic check:
- **TICKER** — reason (e.g. "Sloan accruals 9.2% > 7.5% threshold")

### Methodology Note

- Screen factors: \<list>
- Forensic thresholds: M-Score ≤ -2.22, Sloan accruals ≤ 7.5%, ROA ≥ 0
- Universe: US-listed entities with `factor_scores.parquet` coverage
- Survivorship-free: includes delisted entities (use `get_pit_universe` for as-of-date queries)

### Sources

Always close with a list of cited filings: `[Accession ID]: <source_url>` for every survivor's `forensic_audit` lineage. The user should be able to one-click any number back to its SEC source.
