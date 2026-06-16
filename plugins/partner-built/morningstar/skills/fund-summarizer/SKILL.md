---
name: fund-summarizer
description: Use when summarizing a fund or ETF with Morningstar ratings, returns, risk, holdings, fees, and caveats.
---

# Fund Summarizer

Create a concise fund summary or report using the connected Morningstar app as the data source.

## Guardrails

- Use only data returned by the Morningstar app in the current session.
- Do not infer missing values, add outside research, predict performance, or give investment advice.
- Show unavailable numeric values as `--` and unavailable text as `N/A`. Distinguish missing data from tool failure.
- Supported investment types are ETFs, open-end funds, and closed-end funds. If the user asks for an equity or unsupported security, explain that this skill is fund-focused and ask for a supported fund.
- Preserve Morningstar terminology for ratings, categories, benchmarks, and analyst research.
- Do not read script source files to understand the data schema — use `references/full-workflow.md` instead. You may invoke `scripts/render.py` when the user explicitly requests an HTML report.
- Do not write helper scripts or render wrappers to produce the HTML report — assemble the data dict inline and call `render_report` once.

## Formatting Rules

| Value type | Rule |
|---|---|
| Percentages and ratios | 2 decimal places (e.g. `8.23%`, `1.05`) |
| Category ranks, MPRS | Whole number (e.g. `47`, `82`) |
| Currency amounts | Raw number with commas, no symbol (e.g. `1,234.56`) |
| Large AUM / flows | B/M compact, no symbol (e.g. `1.23B`, `456.70M`) |
| Dates | YYYY-MM-DD |
| Missing numeric | `--` |
| Missing text | `N/A` |

## Workflow

For broad summaries, detailed reports, or any HTML report, read `references/full-workflow.md` before retrieving data. It preserves Morningstar's partner-authored datapoint map, missing-data rules, structured report inputs, and renderer contract.

1. Resolve the fund from ticker, name, or Morningstar identifier. Ask only if the match is ambiguous.
2. Retrieve all fund data in parallel batches — fire these simultaneously, do not wait for one before starting the next:
   - **Core metadata + ratings/IP** in one `morningstar_data_tool` call
   - **Performance, risk, and monthly returns** (HP010, trailing 10 years) in one `morningstar_data_tool` call
   - **Holdings** in one `morningstar_data_tool` call
   - **Analyst research** via `morningstar_analyst_research_tool`
   - **Top holdings** via `morningstar_fund_holdings_tool`
3. Retrieve benchmark data in one `morningstar_data_tool` call: base currency, HP010 monthly returns (trailing 10 years), and trailing/annual returns. Fire this as soon as step 2 batch A returns (you only need the benchmark ID from it).
4. Build the smallest useful deliverable for the user request. Use Markdown by default; create self-contained HTML only if the user explicitly asks for an HTML report or a sharable artifact. 

## HTML Report Support

When creating an HTML report, use `scripts/render.py`. It reads `assets/template.html`, `assets/icons/`, and the Morningstar logo asset, with visual guidance in `references/design_guide.md`. The renderer produces a self-contained HTML file — no PDF export.

## Output

Use this order:

1. Morningstar disclosure: AI-generated analysis using Morningstar data; informational only, not investment advice.
2. Fund snapshot.
3. Ratings and analyst context.
4. Performance and category-rank context.
5. Risk and portfolio context.
6. Fees, flows, and operational details.
7. Data-availability notes and caveats.

Keep the summary factual and skimmable. For broad requests, include the main tables and a short neutral narrative. For narrow questions, answer only the requested metric or section. If the user asks for an HTML report, produce a single file with all sections, tables, and charts. For other requests, use Markdown with tables and bullet points as needed.