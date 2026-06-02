---
name: fund-screener
description: Use when screening funds or ETFs by Morningstar category, ratings, fees, assets, returns, or risk.
---

# Fund Screener

Screen funds using the connected Morningstar app as the data source.

## Guardrails

- Use only data returned by the Morningstar app in the current session.
- Do not infer missing values, create synthetic scores, predict performance, or give investment advice.
- Show unavailable values as `N/A` and distinguish missing data from tool failure.
- Supported universes are ETFs, open-end funds, and closed-end funds.
- Treat filters as AND logic unless the user explicitly asks for alternatives; run separate passes for OR logic and deduplicate results.

## Workflow

Before running a real screen, read `references/full-workflow.md`. It preserves Morningstar's partner-authored rules for criteria confirmation, normalization, datapoints, result validation, output tables, disclosures, and follow-up suggestions.

1. Collect the screening criteria in one pass: universe, category, medalist rating, star rating, expense ratio, assets, and any user-specified filters.
2. Normalize user terms against Morningstar-supported datapoints and values before screening. If a close match is likely, ask for confirmation before running.
3. Run the screen, targeting a useful result set of roughly 10 to 20 funds.
4. Validate fund status and remove inactive, merged, or liquidated funds.
5. Enrich surviving results with category, active/passive status, benchmark, expense ratio, assets, inception date, medalist rating, star rating, returns, category ranks, and risk metrics when available.
6. Rank results by the user's priority. If no priority is given, sort by assets descending and then expense ratio ascending.

## Output

Use this order:

1. Disclosure banner.
2. Criteria used table, one row per active filter only, including normalized terms.
3. Result count and exclusions.
4. Snapshot table.
5. Performance table.
6. Risk and category-rank table.
7. Three concise, data-backed refinements such as tighter expense ratio, higher rating floor, narrower category, or universe changes.

If the screen returns zero or too few results, identify the likely binding criteria and ask what to relax.