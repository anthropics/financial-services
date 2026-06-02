---
name: fund-summarizer
description: Use when summarizing a fund or ETF with Morningstar ratings, returns, risk, holdings, fees, and caveats.
---

# Fund Summarizer

Create a concise fund summary or report using the connected Morningstar app as the data source.

## Guardrails

- Use only data returned by the Morningstar app in the current session.
- Do not infer missing values, add outside research, predict performance, or give investment advice.
- Show unavailable values as `N/A` and distinguish missing data from tool failure.
- Supported investment types are ETFs, open-end funds, and closed-end funds. If the user asks for an equity or unsupported security, explain that this skill is fund-focused and ask for a supported fund.
- Preserve Morningstar terminology for ratings, categories, benchmarks, and analyst research.

## Workflow

For broad summaries, detailed reports, or any HTML report, read `references/full-workflow.md` before retrieving data. It preserves Morningstar's partner-authored datapoint map, missing-data rules, structured report inputs, and renderer contract.

1. Resolve the fund from ticker, name, or Morningstar identifier. Ask only if the match is ambiguous.
2. Retrieve core profile data: name, ticker, category, investment type, inception date, benchmark, active/passive status, assets, fees, yield, manager tenure, and fund status.
3. Retrieve ratings and research context: medalist rating, star rating, pillar ratings when available, portfolio risk score, analyst summary, and relevant disclosures.
4. Retrieve performance and risk context: trailing returns, calendar-year returns, category ranks, standard deviation, Sharpe ratio, upside/downside capture, and flows when available.
5. Retrieve portfolio context: asset allocation, sector/geography exposure, market-cap style, top holdings, turnover, and sustainability data when available.
6. Build the smallest useful deliverable for the user request. Use Markdown by default; create self-contained HTML only if the user explicitly asks for an HTML report.

## HTML Report Support

When creating an HTML report, use `scripts/render.py`. It reads `assets/template.html`, `assets/icons/`, and the Morningstar logo asset, with visual guidance in `references/design_guide.md`.

Report rendering always creates the HTML report and attempts a sibling PDF copy when the local environment supports it. If PDF export is unavailable, deliver the HTML report. For command-line PDF export from an existing HTML report, run `scripts/export_report.py` against the rendered report HTML.

## Output

Use this order:

1. Morningstar disclosure: AI-generated analysis using Morningstar data; informational only, not investment advice.
2. Fund snapshot.
3. Ratings and analyst context.
4. Performance and category-rank context.
5. Risk and portfolio context.
6. Fees, flows, and operational details.
7. Data-availability notes and caveats.

Keep the summary factual and skimmable. For broad requests, include the main tables and a short neutral narrative. For narrow questions, answer only the requested metric or section.
