---
name: fund-comparison
description: Use when comparing 2 to 4 funds or ETFs with Morningstar ratings, returns, risk, and holdings data.
---

# Fund Comparison

Compare 2 to 4 funds side by side using the connected Morningstar app as the data source.

## Guardrails

- Use only data returned by the Morningstar app in the current session.
- Do not infer, backfill, rank suitability, predict performance, or give investment advice.
- Show unavailable values as `N/A` and distinguish missing data from tool failure.
- Supported investment types are ETFs, open-end funds, and closed-end funds. Exclude unsupported securities and explain why.
- If funds span broad asset classes, stop and ask for comparable funds instead of mixing incompatible metrics.

## Workflow

Before running a real comparison, read `references/full-workflow.md`. It preserves Morningstar's partner-authored rules for fund resolution, exclusions, datapoints, broad-asset-class checks, holdings overlap, disclosures, and table formats.

1. Resolve each ticker, name, or identifier to the intended Morningstar fund. Ask only if the result is ambiguous.
2. Validate that 2 to 4 active supported funds remain after exclusions.
3. Retrieve the smallest complete data set needed for the comparison: category, broad asset class, rating, medalist rating, expense ratio, assets, inception date, benchmark, return periods, category ranks, risk metrics, and top holdings when available.
4. For equity funds, compare top holdings and show overlaps. For other asset classes, omit holdings overlap unless Morningstar returns meaningful holdings data.
5. Present comparison tables with funds as columns and metrics as rows.

## Output

Use this order:

1. Disclosure banner.
2. Resolution/exclusion notes, if any.
3. Snapshot table.
4. Performance table.
5. Category-rank table with a note that lower percentile rank is better.
6. Risk table.
7. Holdings overlap for equity funds only.
8. Brief caveats about category or data-availability differences.