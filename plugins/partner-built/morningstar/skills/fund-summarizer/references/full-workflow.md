# Partner-authored workflow details

# Fund Summary Skill

A skill for generating a self-contained HTML report with Morningstar insights into a given fund. This skill interacts directly with the Morningstar app to retrieve and summarize key information about a fund, including its ratings, returns, holdings, analyst research, and other relevant metrics.

# Operating Constraints

0. **Default output is the HTML report**: When the user makes a broad request for a fund summary, fund analysis, or fund report, generate the self-contained HTML report and provide the file path. This includes terse requests like "Summarize DODWX" or "Analyze VTSAX". Do not answer with only a text summary unless the user explicitly says not to create a report, asks for text only, or asks a tightly scoped factual question such as "What is the expense ratio?", "What is the Medalist Rating?", "Show top holdings", or "How has it performed YTD?".

1. **No analysis**: You should not perform any analysis or interpretation of the data retrieved from the Morningstar app. Instead, you should focus on summarizing the information in a clear and concise manner without adding any subjective opinions or insights. When summarizing the text information from analysts or articles, you should focus on extracting the key insights and presenting them without adding any additional commentary or analysis.

2. **No financial advice**: You should not provide any financial advice or recommendations based on the information retrieved from the Morningstar app. You should strictly adhere to providing factual information and summaries without making any suggestions or recommendations to the user.

3. **Use the provided template and visual guidance**: When constructing the report, you should use the provided HTML template and populate it with the relevant information about the fund. You should not deviate from the structure of the template or add any additional sections or information that is not relevant to the fund summary. You should also rely on the provided visual guidance for any charts or graphics included in the report, ensuring that they adhere to Morningstar's design standards and color guidelines.

4. **Data availability**: The information you can retrieve about the fund is limited to what is available in the Morningstar app. This only includes ETF's, open-end, and closed-end funds. This would not be available for equities. If the user asks for a summary of an equity, this skill would not apply.

# Workflow

When a user asks for a summary of a fund, you will need to interact with the Morningstar app to retrieve the necessary information. The workflow typically involves the following steps. You do not need to explicitly call out these steps in your response nor provide interim commentary, but you should follow this general process to ensure that you are retrieving and summarizing the information effectively.

## Step 1. Resolve the Fund

First, use `morningstar_id_lookup_tool` to identify the specific fund the user is asking about. If possible, use the ticker for the fund and be precise when requesting a security name, since many securities have very similar names.

If the name-based search returns multiple results, ask the user for more information to narrow down the search. Once you have identified the correct fund, you can proceed to retrieve its information.
The output from this step will include the Morningstar ID for the fund, which you will use in the next step to retrieve detailed information about the fund.

If you cannot identify a fund based on the information provided by the user, you should ask for additional details to help narrow down the search. This could include asking for the fund's ticker symbol, the name of the fund manager, or any other relevant information that could help identify the correct fund.

## Step 2. Retrieve Fund Information

Retrieve the following information from `morningstar_data_tool` using the Morningstar Fund ID obtained in the previous step. Use `morningstar_id_lookup_tool` to resolve datapoint IDs when needed; the IDs listed below are the target Morningstar datapoints. This will include key metrics such as the fund's ratings, returns, and other relevant data points that will be used to construct the summary report. These are chunked in order to be sure that the full JSON output persists in context, rather than only being able to view a truncated version, which can occur when retrieving a large number of data points in a single call.
If any of the data points are not available for the fund, you should note that in the summary report and avoid making any assumptions or interpretations based on missing data.

**Step 2 is the source of truth.** Every value assembled in Step 4 must come from the datapoints and tools listed in Step 2, or from an explicit calculation using those Step 2 values. Do not introduce additional datapoints while constructing the report. If Step 4 appears to need a datapoint that is not listed in Step 2, treat it as unavailable and display the relevant missing-data behavior unless Step 2 is first updated to include that source.

### Core Metadata
First, retrieve the core metadata for the fund, which includes the following data points:
- Name:  OS01W
- Ticker: OS385
- Fund Standard Name: AA0B3
- Morningstar Category: OF003
- Fund Inception Date: OS00F
- Inception Date of Fund's Oldest Share Class: OD003
- Index Fund: OF00C
- Actively Managed: OF00D, ETF-focused datapoint. Valid for ETFs (FE), but not applicable for open-end funds (FO). For FO funds, use the result from OF00C instead.
- Investment Type: LS466
- Base Currency: LS05M
- Fund Size: OF009
- Share Class Closed to New Inv: OS387
- Minimum Initial Purchase: OS00U
- Morningstar Fee Level - Broad: UB412
- Morningstar Fee Level - Distribution: OS707
- Prospectus Adjusted Expense Ratio: ZZ007
- Morningstar Category Index Id: OS38A
- Primary Prospectus Benchmark Id: OF00P
- Primary Prospectus Benchmark: OF00L
- Longest Tenured Manager Name: OF059
- Longest Tenured Manager Start Date: OF050
- Manager Ownership Level: OS276
- Turnover Ratio %: OS03S
- 12 Mo Yield: PM032
- SEC Yield: PM002
- NAV (Daily): OS060
- Est Fund-Level Net Flow 1 Mo (Mo-End): HS338
- Est Fund-Level Net Flow 3 Mo (Mo-End): HS339
- Est Fund-Level Net Flow 1 Yr (Mo-End): HS342
- Morningstar Medalist Rating: MMR01

### Performance and Risk Data
After retrieving the core metadata, you should then retrieve the performance data for the fund, which includes the following data points:
- Yearly Return: HS803, This is a timeseries datapoint, meaning you will need to include `start_date` and `end_date` to receive a value. Determine the range dynamically based on the current date and request only completed calendar years. For example, if today's date is in 2026, request data covering 2015-2025 by using `start_date="2015-01-01"` and `end_date="2025-12-31"`. The response will return one yearly return value per completed calendar year in the timeSeriesData array, which can be mapped to the annual return fields in the summary report.
- Monthly Return: HP010, This is a timeseries datapoint used for the returns chart only. Request the trailing 10 years of month-end returns, ending at the latest month-end available in the data. For funds with less than 10 years of history, request since the first available month. Use the returned monthly percentages to build the Growth of 10,000 chart described in section 4c.
- Annual Ret {year}: AR002
- Total Ret 1 Yr (Daily): PD00D
- Total Ret Annlzd 2 Yr (Daily): PD014
- Total Ret Annlzd 3 Yr (Daily): PD00F
- Total Ret Annlzd 5 Yr (Daily): PD00H
- Total Ret Annlzd 10 yr (mo-end): PM00I
- Total Ret YTD (Daily): PD00B
- Return Date (Daily): PD001
- Annual Ret % Rank Cat {year}: AR00E
- Annual Ret % Rank Cat {year-1}: AR00F
- Annual Ret % Rank Cat {year-2}: AR00G
- Annual Ret % Rank Cat {year-3}: AR00H
- Annual Ret % Rank Cat {year-4}: AR00I
- Annual Ret % Rank Cat {year-5}: AR00J
- Annual Ret % Rank Cat {year-6}: AR00K
- Annual Ret % Rank Cat {year-7}: AR00L
- Annual Ret % Rank Cat {year-8}: AR00M
- Annual Ret % Rank Cat {year-9}: AR00N
- Annual Ret % Rank Cat {year-10}: AR00O
- Sharpe Ratio 1 Yr (Mo-End): RR010
- Sharpe Ratio 3 Yr (Mo-End): RR011
- Sharpe Ratio 5 Yr (Mo-End): RR012
- Sharpe Ratio 10 Yr (Mo-End): RR013
- Std Dev 3 Yr (Mo-End): RR015
- Std Dev 5 Yr (Mo-End): RR016
- Std Dev 10 Yr (Mo-End): RR017
- Alpha 3 Yr (Mo-End): RR003
- Alpha 5 Yr (Mo-End): RR004
- Beta 3 Yr (Mo-End): RR00L
- Beta 5 Yr (Mo-End): RR00M
- Beta 10 Yr (Mo-End): RR00N
- R-Squared 3 Yr (Mo-End): RR01P
- R-Squared 5 Yr (Mo-End): RR01Q
- Upside Capture Ratio 1 Yr (Mo-End): RR152
- Upside Capture Ratio 3 Yr (Mo-End): RR153
- Upside Capture Ratio 5 Yr (Mo-End): RR154
- Upside Capture Ratio 10 Yr (Mo-End): RR155
- Downside Capture Ratio 1 Yr (Mo-End): RR158
- Downside Capture Ratio 3 Yr (Mo-End): RR159
- Downside Capture Ratio 5 Yr (Mo-End): RR160
- Downside Capture Ratio 10 Yr (Mo-End): RR161

### Holdings Data
Next, retrieve the holdings data for the fund, which includes the following data points:

- Asset Alloc Bond % (Long Rescaled): HS02D
- Asset Alloc Cash % (Long Rescaled): HS00X
- Asset Alloc Conv Bond % (Long Rescaled): HS00Y
- Asset Alloc Equity % (Long Rescaled): HS02E
- Asset Alloc Non-US Bond % (Long Rescaled): HS143
- Asset Alloc Non-US Equity % (Long Rescaled): HS141
- Asset Alloc Pref Stock % (Long Rescaled): HS00T
- Asset Alloc US Bond % (Long Rescaled): HS142
- Asset Alloc US Equity % (Long Rescaled): HS140
- Fixed Income Surveyed Style Box: HS00L
- Equity Style Box (Long): HS05A
- Average Eff Duration Survey: HS02F
- Average Credit Quality: HS00C
- Fixed-Inc Country United States % (Long Rescaled): HS125
- Fixed-Inc Country Canada % (Long Rescaled): HS122
- Fixed-Inc Region United Kingdom % (Long Rescaled): FR1AG
- Fixed-Inc Region Europe dev % (Long Rescaled): FR1AB
- Fixed-Inc Region Japan % (Long Rescaled): FR1AD
- Fixed-Inc Region Australasia % (Long Rescaled): FR1A6
- Fixed-Inc Region Asia dev % (Long Rescaled): FR1A8
- Fixed-Inc Region Emerging % (Long Rescaled): FR1A2
- Fixed-Inc Region Not Classified % (Long Rescaled): FR1A3
- Equity Region North America % (Long Rescaled): HS05C
- Equity Region Latin America % (Long Rescaled): HS06D
- Equity Region United Kingdom % (Long Rescaled): HS06E
- Equity Region Europe dev % (Long Rescaled): HS07S
- Equity Region Europe emrg % (Long Rescaled): HS06H
- Equity Region Africa/Middle East % (Long Rescaled): HS006
- Equity Region Japan % (Long Rescaled): HS06K
- Equity Region Australasia % (Long Rescaled): HS06L
- Equity Region Asia dev % (Long Rescaled): HS06N
- Equity Region Asia emrg % (Long Rescaled): HS06M
- Market Cap Giant % (Long Rescaled): HS039
- Market Cap Large % (Long Rescaled): HS03P
- Market Cap Mid % (Long Rescaled): HS049
- Market Cap Small % (Long Rescaled): HS05Z
- Market Cap Micro % (Long Rescaled): HS03Z
- P/E Ratio — Projected (Long): HS067
- P/B Ratio — Projected (Long): HS064
- P/S Ratio — Projected (Long): HS068
- Dividend Yield % — Style Factor (Long): HS066
- Sales Growth % (Long): HS035
- Cash-Flow Growth % (Long): HS033
- Average Market Cap (mil) — Long: HS03W
- Financial Health Grade (Long): HS05I
- Growth Grade (Long): HS05K
- Cash Return % (Long): HS05L
- Equity Style Factor Hist Earn Growth (Long): HS034
- Equity Style Factor LT Earn Growth (Long): HS031
- Number of Holdings (Long): HS008
- Ownership Breadth: CEIDQ
- Liquidity Frequency Intermittent Weight %: MKDXK

Also call `morningstar_fund_holdings_tool` for the fund's top holdings. Use the returned holding names and weights to populate the structured `TOP_HOLDINGS` list in Step 4. Do not hand-write `TOP_HOLDINGS_ROWS`; the renderer builds the table rows.

### Morningstar IP
- Morningstar Medalist Rating: MMR01
- Morningstar Medalist Rating Disclosures Type: CNAXS
- Morningstar Rating Overall: RR01Y
- Morningstar Portfolio Risk Score: QFR0H
- Morningstar Medalist Rating Analyst Driven Percentage: MMR04
- Morningstar Medalist Rating Parent Pillar: MMR1E
- Morningstar Medalist Rating Parent Pillar Score Type: MMR14
- Morningstar Medalist Rating People Pillar: MMR2E
- Morningstar Medalist Rating People Pillar Score Type: MMR24
- Morningstar Medalist Rating Price Score: MMRGS
- Morningstar Medalist Rating Process Pillar: MMR3E
- Morningstar Medalist Rating Process Pillar Score Type: MMR34

### Benchmark Data
Finally, retrieve the benchmark data for the fund, which includes the following data points, using the Primary Prospectus Benchmark ID:

First, retrieve the returns and risk capture data for this benchmark.
- Base Currency: LS05M
- Yearly Return: HS803
- Monthly Return: HP010
- Total Ret 1 Yr (Daily): PD00D
- Total Ret Annlzd 2 Yr (Daily): PD014
- Total Ret Annlzd 3 Yr (Daily): PD00F
- Total Ret Annlzd 5 Yr (Daily): PD00H
- Total Ret Annlzd 10 yr (mo-end): PM00I
- Total Ret YTD (Daily): PD00B
- Return Date (Daily): PD001
- Std Dev 3 Yr (Mo-End): RR015
- Std Dev 5 Yr (Mo-End): RR016
- Std Dev 10 Yr (Mo-End): RR017

For benchmark risk statistics, retrieve benchmark standard deviation only (RR015, RR016, RR017). Do not retrieve benchmark Sharpe, alpha, beta, or R-squared — those are either fund-level benchmark-relative statistics or require a matched currency to be meaningful.

**Benchmark Currency Gate**: After retrieving the benchmark LS05M value, compare it to the fund's `BASE_CURRENCY`. If they differ, set a `BENCHMARK_CURRENCY_MISMATCH` flag and apply the following suppressions when assembling the data package for Step 4:
- In `CUMULATIVE_RETURNS_JSON`: set every `benchmark` value to `null` for the entire series.
- In `RISK_DATA_JSON`: set `"benchmark": {}` to suppress all benchmark risk display.
- In `TRAILING_RETURNS`: keep the fund values and set benchmark values to `null`; the renderer omits Benchmark and Excess rows.
- In `ANNUAL_RETURNS`: keep the fund and percentile rank values and set benchmark values to `null`; the renderer omits Benchmark and Excess rows.
- Set `BENCHMARK_CURRENCY_NOTE_TEXT` to a brief plain-English note explaining the suppression.

### Unstructured Data

For the analyst research and Morningstar articles, use `morningstar_analyst_research_tool` and `morningstar_articles_tool` to retrieve any relevant content about the fund. This will include any analyst reports or editorial publications that provide insights into the fund's performance, management, or other relevant factors. For the article tool, use queries similar to the following to retrieve the relevant information about the fund:
- How does {fund name} compare to its peers?
- What are the key strengths and weaknesses of {fund name}?
- What are the recent developments related to {fund name}?

## Step 3. Summarize the Information

For certain types of information, you will need to summarize the data retrieved from the Morningstar app. This involves extracting key insights and presenting them in a concise and informative manner. For example, the output of the Analyst Research and Morningstar Articles Tool will contain a list of content from analyst reports and assorted editorial publications, not always in a specific order, but you should focus on summarizing the most important insights that are relevant to the fund's people, process, parent, and performance pillars.

Use plain English, active voice, short declarative sentences, strong verbs, and one idea per bullet. Avoid throat-clearing openers, mechanical recitations of performance figures, jargon without plain explanation, over-qualified hedging, and generic conclusions ("investors should monitor performance going forward"). Return ~1-3 sentences for each pillar, and up to 5 short sentences for the overall analyst summary. Do not include any subjective opinions or recommendations in your summaries. Focus on presenting the information in a clear and concise manner that is easy for the user to understand.

## Step 4. Construct the Report

Build the report whenever the request is a broad fund summary, analysis, or report request. Create a Python dictionary mapping every placeholder key to its value (see tables below), then call the renderer script to produce the final HTML. The HTML file is the primary deliverable; do not stop at a text summary unless the user explicitly asked not to create a report or asked a tightly scoped factual question.

Step 2 remains authoritative during report construction. Step 4 is only a packaging and formatting step: assemble structured data, plain text, and chart JSON from the Step 2 retrieval results and Step 3 summaries. Do not ask the language model to write table-row HTML for holdings or returns. The renderer owns report HTML, SVG charts, icons, pillar score scales, and derived table rows.

```python
data = {
    "FUND_NAME": "...",
    "TICKER": "...",
    # ... all keys from 4a, 4b, 4c below
}
render_report(data, output_path=f"{data['TICKER']}-fund-summary.html")
```

Call `render_report(data, output_path=f"{data['TICKER']}-fund-summary.html")` from `scripts/render.py`, or run `python <skill-dir>/scripts/render.py --data data.json --output <ticker>-fund-summary.html`. If importing the function from outside the `scripts` directory, add `<skill-dir>/scripts` to `sys.path` first. The renderer reads `assets/template.html`, replaces all `{{PLACEHOLDER}}` tokens, builds derived HTML from structured inputs, serializes any dict/list values to JSON automatically, writes the HTML output file, and attempts a sibling PDF copy when the local environment supports it.

For direct PDF export from an already rendered HTML report, run:

```bash
python <skill-dir>/scripts/export_report.py <ticker>-fund-summary.html --format pdf
```

`render.py` and `export_report.py` use the companion Node helper plus Playwright when available. They prefer the Codex-bundled Node runtime and fall back to already-cached Playwright browsers, so they can export report HTML without re-retrieving Morningstar data. If a sandboxed environment blocks Chromium, the renderer still succeeds with the HTML report. Use `--require-pdf` only when PDF output is mandatory.

### Renderer Data Package Contract

The object passed to `render_report(data, ...)` should contain only source values, structured inputs, plain text, and chart JSON. The skill should return these categories:

- Direct scalar fields from Section 4a, such as `FUND_NAME`, `TICKER`, `CATEGORY`, `MEDALIST_RATING`, `STAR_RATING`, `PROCESS_RATING`, `PRICE_RATING`, and `DATA_AS_OF_DATE`.
- Structured repeated-content fields from Section 4b: `TOP_HOLDINGS`, `TRAILING_RETURNS`, `ANNUAL_RETURNS`, `ANALYST_SUMMARY_PARAGRAPHS`, `PILLAR_SUMMARIES`, `STYLE_BOX_EQUITY`, `STYLE_BOX_FIXED_INCOME`, `FI_DURATION`, `FI_CREDIT_QUALITY`, `FIXED_INCOME_REGION_ROWS`, `REGIONAL_EXPOSURE_ROWS`, `MARKET_CAP_ROWS`, and `EQUITY_PORTFOLIO_STATS_ROWS`.
- Chart data fields from Section 4c: `CUMULATIVE_RETURNS_JSON`, `ASSET_ALLOCATION_JSON`, and `RISK_DATA_JSON`.
- Control flags/plain text such as `BENCHMARK_CURRENCY_MISMATCH` and `BENCHMARK_CURRENCY_NOTE_TEXT`.

Leave renderer-generated placeholders unset. Do not include `TOP_HOLDINGS_ROWS`, `TRAILING_RETURNS_ROWS`, `ANNUAL_RETURNS_HEADERS`, `ANNUAL_RETURNS_ROWS`, `ANALYST_SUMMARY`, `PROCESS_SUMMARY_HTML`, `PEOPLE_SUMMARY_HTML`, `PARENT_SUMMARY_HTML`, `PRICE_SUMMARY_HTML`, `BENCHMARK_LEGEND_ENTRY`, `BENCHMARK_CURRENCY_NOTE`, `RETURNS_CHART_SVG`, `DONUT_CHART_SVG`, `STAR_RATING_ICON`, `MPRS_VISUAL`, `PROCESS_ICON`, `PEOPLE_ICON`, `PARENT_ICON`, pillar score scale placeholders, section class placeholders, row HTML placeholders, or section note placeholders. The renderer derives those from the source values above.

**Active / Index determination:**
- OF00C ("Index Fund") is the broad flag across all fund types. OF00C = Yes, then "Index"; OF00C = No, then "Active".
- For ETFs only, OF00D ("Actively Managed") provides a more specific signal: OF00D = Yes, then "Active"; OF00D = No, then "Index".
- For non-ETFs (FO), derive from OF00C only (OF00D is not applicable).

### 4a. Simple Placeholder Mapping

| Placeholder | Source | Format |
|---|---|---|
| `{{FUND_NAME}}` | OS01W | As-is |
| `{{FUND_STANDARD_NAME}}` | AA0B3 | As-is |
| `{{TICKER}}` | OS385 | Uppercase |
| `{{CATEGORY}}` | OF003 | As-is |
| `{{INCEPTION_DATE}}` | OS00F | YYYY-MM-DD |
| `{{OLDEST_SHARE_CLASS_INCEPTION}}` | OD003 | YYYY-MM-DD |
| `{{ACTIVE_INDEX_LABEL}}` | Non-ETFs: "Active" if OF00C=No, "Index" if OF00C=Yes. ETFs: "Active" if OF00D=Yes, "Index" if OF00D=No. | Single word |
| `{{INVESTMENT_TYPE}}` | LS466 | As-is |
| `{{BASE_CURRENCY}}` | LS05M | e.g. "USD" |
| `{{FUND_SIZE}}` | OF009 | Format as "$X.XB" or "$X.XM" |
| `{{CLOSED_TO_NEW}}` | OS387 | "Yes" or "No" |
| `{{MIN_INITIAL_PURCHASE}}` | OS00U | Format with $ and commas |
| `{{FEE_LEVEL}}` | UB412 | As-is (e.g. "Low", "Below Average") |
| `{{FEE_LEVEL_DISTRIBUTION}}` | OS707 | As-is |
| `{{EXPENSE_RATIO}}` | ZZ007 | Format as "X.XX%" |
| `{{PROSPECTUS_BENCHMARK}}` | OF00L | Full benchmark name |
| `{{MANAGER_NAME}}` | OF059 | As-is |
| `{{MANAGER_INITIALS}}` | Derived from OF059 | First letter of first + last name |
| `{{MANAGER_START_DATE}}` | OF050 | YYYY-MM-DD |
| `{{MANAGER_OWNERSHIP}}` | OS276 | As-is (e.g. "$1M+") |
| `{{TURNOVER_RATIO}}` | OS03S | Format as "XX%" |
| `{{TWELVE_MONTH_YIELD}}` | PM032 | Format as "X.XX%" |
| `{{SEC_YIELD}}` | PM002 | Format as "X.XX%" |
| `{{NAV}}` | OS060 | Plain number with 2 decimals, no currency symbol |
| `{{EST_NET_FLOW_1M}}` | HS338 | Plain value, compact if useful (e.g. "123.4M"), no currency symbol |
| `{{EST_NET_FLOW_3M}}` | HS339 | Plain value, compact if useful, no currency symbol |
| `{{EST_NET_FLOW_1Y}}` | HS342 | Plain value, compact if useful, no currency symbol |
| `{{MEDALIST_RATING}}` | MMR01 | Word: "Gold", "Silver", "Bronze", "Neutral", or "Negative" |
| `{{MEDALIST_ANALYST_PCT}}` | MMR04 | Numeric string without a percent sign, because the template appends "%" |
| `MEDALIST_DISCLOSURE_TYPE` | CNAXS | Pass the returned value when present. If CNAXS is blank, `NA`, or `N/A`, leave it unset; that is expected and does not need a missing-data note. The renderer displays present values below the Analyst-Driven percentage and adds the matching bottom footnote for `Issuer Initiated Rating` or `Tracks Morningstar Index`. |
| `{{STAR_RATING}}` | RR01Y | Provide the overall rating as an integer 1-5 when possible; the renderer selects the matching star SVG from `assets/icons`. |
| `{{MPRS}}` | QFR0H | As-is (numeric score); the renderer adds the MPRS dial visual and pointer automatically. |
| `{{PARENT_RATING}}` | MMR1E | Pass the returned pillar label as a plain string, such as `High`, `Above Average`/`Above Avg`, `Average`, `Below Average`/`Below Avg`, or `Low`. Do not turn this into HTML. The renderer normalizes the label and resolves the Morningstar pillar score icon and scale. |
| `{{PARENT_SCORE_TYPE}}` | MMR14 | Pass the returned score type as a plain string. `Quantitative` selects the Quant icon; `Not returned`, blank, or any non-quant value selects the Analyst icon. A `^Q` suffix on the rating value also selects the Quant icon. |
| `{{PEOPLE_RATING}}` | MMR2E | Same label handling as `PARENT_RATING`; pass the returned value so the renderer can resolve the icon and scale. |
| `{{PEOPLE_SCORE_TYPE}}` | MMR24 | Same score-type handling as `PARENT_SCORE_TYPE`. |
| `{{PROCESS_RATING}}` | MMR3E | Same label handling as `PARENT_RATING`; pass the returned value so the renderer can resolve the icon and scale. |
| `{{PROCESS_SCORE_TYPE}}` | MMR34 | Same score-type handling as `PARENT_SCORE_TYPE`. |
| `{{PRICE_RATING}}` | MMRGS | Price score, float value. The renderer displays this value in the Price card. Do not convert it into a qualitative rating unless Step 2 returns a qualitative price rating source. |
| `{{NUM_HOLDINGS}}` | HS008 | Integer with commas |
| `{{OWNERSHIP_BREADTH}}` | CEIDQ | As-is |
| `{{LIQUIDITY_INTERMITTENT}}` | MKDXK | Format as "X.X%" |
| `{{DATA_AS_OF_DATE}}` | PD001 (Return Date Daily) | YYYY-MM-DD |
| `{{REPORT_DATE}}` | Today's date | YYYY-MM-DD |
| `{{BENCHMARK_NAME}}` | Derived from OF00L | Shortened display name for chart legend |
| `BENCHMARK_CURRENCY_MISMATCH` | Derived by comparing fund LS05M with benchmark LS05M | Boolean. When true, the renderer suppresses benchmark table/chart values that would be misleading. |
| `BENCHMARK_CURRENCY_NOTE_TEXT` | Plain-text note when `BENCHMARK_CURRENCY_MISMATCH` is true | Plain English. The renderer wraps it in the report note markup. Leave blank when currencies match. |
| `{{BENCHMARK_LEGEND_ENTRY}}` | Renderer-generated from OF00L + `BENCHMARK_CURRENCY_MISMATCH` | Leave unset. When currencies match, the renderer creates the legend entry from `BENCHMARK_NAME`; when currencies differ, it hides the benchmark. |
| `{{BENCHMARK_CURRENCY_NOTE}}` | Renderer-generated from `BENCHMARK_CURRENCY_NOTE_TEXT` | Leave unset. The renderer wraps `BENCHMARK_CURRENCY_NOTE_TEXT` in the report note markup. |

### 4b. Constructed / Multi-Value Placeholders

Use structured inputs for repeated content. The renderer turns these structures into escaped report markup such as `{{TOP_HOLDINGS_ROWS}}`, `{{TRAILING_RETURNS_ROWS}}`, `{{ANNUAL_RETURNS_HEADERS}}`, `{{ANNUAL_RETURNS_ROWS}}`, portfolio detail sections, benchmark notes, and pillar summaries. Do not hand-write rows, section wrappers, inline styles, or CSS classes in the skill output. Leave renderer-generated placeholders unset in normal execution.

**`TOP_HOLDINGS`** - Structured top 10 holdings from `morningstar_fund_holdings_tool`:
```json
[
  {"name": "Holding Name", "weight": 12.34}
]
```
The renderer builds `{{TOP_HOLDINGS_ROWS}}`. If `PCT_TOP_10` is not provided, the renderer sums the first 10 numeric weights and formats the result as `XX.X%`.

**`TRAILING_RETURNS`** - Structured trailing returns in fixed period order:
```json
[
  {"period": "YTD", "fund": 8.21, "benchmark": 8.19},
  {"period": "1 Yr", "fund": 22.45, "benchmark": 22.40},
  {"period": "2 Yr", "fund": 18.92, "benchmark": 18.88},
  {"period": "3 Yr", "fund": 14.33, "benchmark": 14.29},
  {"period": "5 Yr", "fund": 18.76, "benchmark": 18.71},
  {"period": "10 Yr", "fund": 16.12, "benchmark": 16.08}
]
```
Use fund PD00B/PD00D/PD014/PD00F/PD00H/PM00I and matching benchmark values retrieved in Step 2. Values are numbers, not strings, and do not include percent signs. If `BENCHMARK_CURRENCY_MISMATCH` is true, keep the fund values and set benchmark values to `null`; the renderer omits Benchmark and Excess rows.

**`ANNUAL_RETURNS`** - Structured annual returns for the completed calendar years retrieved from HS803:
```json
[
  {"year": 2025, "fund": 13.97, "benchmark": 17.77, "rank": 70}
]
```
Use fund HS803, benchmark HS803, and percentile ranks from AR00E-AR00O mapped to the corresponding years. Values are numbers, not strings. If `BENCHMARK_CURRENCY_MISMATCH` is true, keep fund and rank values and set benchmark values to `null`; the renderer omits Benchmark and Excess rows.

**`ANALYST_SUMMARY_PARAGRAPHS`** - Plain-text paragraph list derived from Step 3. The renderer escapes the text and builds `{{ANALYST_SUMMARY}}`.
```json
[
  "Short analyst narrative paragraph."
]
```

**`PILLAR_SUMMARIES`** - Plain-text pillar summary lists derived from Step 3. The renderer escapes the text and builds the pillar summary markup.
```json
{
  "process": ["Process summary."],
  "people": ["People summary."],
  "parent": ["Parent summary."],
  "price": ["Price summary."]
}
```

**Allocation placeholders** - Use Step 2 fund holdings datapoints only. Set `{{ALLOC_EQUITY_FUND}}` from HS02E, `{{ALLOC_BOND_FUND}}` from HS02D, and `{{ALLOC_CASH_FUND}}` from HS00X. Use `{{ALLOC_ALT_FUND}}` only if an explicit alternative allocation is available from Step 2; otherwise use `0.0%`. Use OTHER for HS00Y + HS00T + any remainder to reach 100%. Because Step 2 does not retrieve benchmark asset allocation datapoints, set benchmark allocation placeholders to `--` unless Step 2 has been explicitly expanded first.

**Portfolio detail structured inputs** - Provide plain values and row lists only. The renderer decides which optional sections are visible, formats values, builds tables/bars, handles benchmark columns, and inserts unavailable notes.

Set these fund-only style-box inputs when available:
```json
{
  "STYLE_BOX_EQUITY": "Large Blend",
  "STYLE_BOX_FIXED_INCOME": "Medium / Moderate"
}
```
Use HS05A for `STYLE_BOX_EQUITY` and HS00L for `STYLE_BOX_FIXED_INCOME`. Leave a key unset or `null` when unavailable.

Set these fixed-income profile inputs when available:
```json
{
  "FI_DURATION": 6.24,
  "FI_CREDIT_QUALITY": "A"
}
```
Use HS02F for `FI_DURATION` and HS00C for `FI_CREDIT_QUALITY`. Pass duration as a number when possible; the renderer adds the years suffix.

For fixed-income, equity region, market-cap, and equity-stat sections, pass row lists using this shape:
```json
[
  {"label": "North America", "fund": 85.4, "benchmark": null},
  {"label": "Europe Developed", "fund": 7.2, "benchmark": null}
]
```
Use numbers for percentage values and `null` for unavailable values. Do not pre-format percent signs. Do not use `--` inside these row lists; the renderer displays missing values consistently.

Profile section visibility is renderer-owned and based on whether structured inputs contain returned data:
- Fixed Income Profile is visible when at least one of `FI_DURATION`, `FI_CREDIT_QUALITY`, or `FIXED_INCOME_REGION_ROWS` contains meaningful fixed-income data. It is hidden when fixed-income profile values are empty/unavailable and fixed-income regional rows are empty or only zero exposure.
- If `FI_DURATION` and `FI_CREDIT_QUALITY` are empty but `FIXED_INCOME_REGION_ROWS` contains returned regional values, the renderer omits the fixed-income stats subpanel and still renders the regional table.
- Equity Profile is visible when at least one of `REGIONAL_EXPOSURE_ROWS`, `MARKET_CAP_ROWS`, or `EQUITY_PORTFOLIO_STATS_ROWS` contains meaningful equity data. It is hidden when equity profile row lists are empty/unavailable or only zero exposure/zero numeric stats.
- Returned zero values are valid returned data for individual displayed rows, but all-zero row lists should not make a profile section visible by themselves. Use `null` for values that were not returned; do not add `--` placeholder values just to force a section to appear.
- Leave renderer-generated profile placeholders unset, including `FIXED_INCOME_SECTION_CLASS`, `FIXED_INCOME_STATS_SECTION_CLASS`, `FIXED_INCOME_REGION_SECTION_CLASS`, `EQUITY_PROFILE_SECTION_CLASS`, row HTML placeholders, headers, and section notes.

Before populating `FIXED_INCOME_REGION_ROWS`, check whether the fund has meaningful fixed-income exposure or fixed-income profile data. If HS02D, HS142, HS143, HS02F, HS00C, and all fixed-income regional datapoints are unavailable or zero, set `STYLE_BOX_FIXED_INCOME`, `FI_DURATION`, and `FI_CREDIT_QUALITY` to `null`, and set `FIXED_INCOME_REGION_ROWS` to `[]`. Do not populate fixed-income regional rows with `0.0` values solely because Morningstar returned zeroes for an equity-only fund.

Before populating equity profile rows, check whether the fund has meaningful equity exposure or equity profile data. If HS02E, HS05A, all regional exposure datapoints, all market-cap datapoints, and all numeric equity-stat datapoints are unavailable or zero, and text/grade equity-stat datapoints are unavailable, set `STYLE_BOX_EQUITY` to `null` and set `REGIONAL_EXPOSURE_ROWS`, `MARKET_CAP_ROWS`, and `EQUITY_PORTFOLIO_STATS_ROWS` to `[]`. Do not populate equity profile rows with `0.0` values solely because Morningstar returned zeroes for a non-equity fund.

Populate `FIXED_INCOME_REGION_ROWS` in this order: United States (HS125), Canada (HS122), United Kingdom (FR1AG), Europe Developed (FR1AB), Japan (FR1AD), Australasia (FR1A6), Asia Developed (FR1A8), Emerging (FR1A2), Not Classified (FR1A3). Include benchmark values from the matching Step 2 benchmark datapoints when available.

Populate `REGIONAL_EXPOSURE_ROWS` in this order: North America (HS05C), Latin America (HS06D), United Kingdom (HS06E), Europe Developed (HS07S), Europe Emerging (HS06H), Africa/Middle East (HS006), Japan (HS06K), Australasia (HS06L), Asia Developed (HS06N), Asia Emerging (HS06M). Step 2 retrieves these as fund datapoints only; set `benchmark` to `null`.

Populate `MARKET_CAP_ROWS` in this order: Giant (HS039), Large (HS03P), Mid (HS049), Small (HS05Z), Micro (HS03Z). Step 2 retrieves these as fund datapoints only; set `benchmark` to `null`.

Populate `EQUITY_PORTFOLIO_STATS_ROWS` in this order: P/E Ratio - Projected (HS067), P/B Ratio - Projected (HS064), P/S Ratio - Projected (HS068), Dividend Yield (HS066), Sales Growth (HS035), Cash-Flow Growth (HS033), Average Market Cap (mil) (HS03W), Financial Health Grade (HS05I), Growth Grade (HS05K), Cash Return (HS05L), Historical Earnings Growth (HS034), Long-Term Earnings Growth (HS031). Use this row shape:
```json
[
  {"label": "P/E Ratio - Projected", "fund": 24.6, "benchmark": null, "format": "ratio"},
  {"label": "Dividend Yield", "fund": 1.2, "benchmark": null, "format": "pct"},
  {"label": "Financial Health Grade", "fund": "B", "benchmark": null, "format": "plain"}
]
```
Use `format: "pct"` for percentage datapoints, `format: "ratio"` for ratio datapoints, `format: "compact"` for Average Market Cap when numeric, and `format: "plain"` for grades or text values. Step 2 retrieves these as fund datapoints only; set `benchmark` to `null`.

**Pillar summaries** - Use `ANALYST_SUMMARY_PARAGRAPHS` and `PILLAR_SUMMARIES` as the structured inputs. The renderer builds `{{ANALYST_SUMMARY}}`, `{{PEOPLE_SUMMARY_HTML}}`, `{{PROCESS_SUMMARY_HTML}}`, `{{PARENT_SUMMARY_HTML}}`, and `{{PRICE_SUMMARY_HTML}}`.

### 4c. Chart JSON Blocks

These are inserted as JavaScript object literals (no quotes around the placeholder):

**`{{CUMULATIVE_RETURNS_JSON}}`**
```json
[
  {"date": "2016-04-30", "fund": 10000.00, "benchmark": 10000.00},
  {"date": "2016-05-31", "fund": 10215.44, "benchmark": 10180.12}
]
```
Built from HP010 monthly return timeseries for the fund and benchmark. Use the latest common month-end as the end date when both series are available. Start 10 years before that end date when possible; for newer funds or benchmarks, start at the first month where both have HP010 data inside the 10-year window. Add a starting observation at the month-end immediately before the first compounded monthly return with both values set to `10000.00`. For each subsequent month, compound the prior value as `prior_value * (1 + monthly_return / 100)`. Values are Growth of 10,000 levels as numbers (not strings), two decimal places.

If the benchmark has no usable HP010 data or no overlap with the fund, still build the fund series over the trailing 10 years or since the fund's first available month, whichever is shorter. Set benchmark values to `null` for each date so the chart renders the fund line without inventing benchmark data. If occasional monthly returns are missing after the common start, use `null` for that series on that date and resume compounding only when continuous data is available.

**`{{ASSET_ALLOCATION_JSON}}`**
```json
[
  {"label": "Equity", "value": 65.2},
  {"label": "Bond", "value": 20.1},
  {"label": "Cash", "value": 8.4},
  {"label": "Other", "value": 6.3}
]
```
Built from HS02E, HS02D, HS00X. "Other" = 100 minus the sum of Equity + Bond + Cash (includes convertibles + preferred).

**`{{RISK_DATA_JSON}}`**
```json
{
  "fund": {
    "sharpe": [0.82, 0.91, 0.76, 0.88],
    "upside": [112.3, 108.5, 105.2, 107.1],
    "downside": [95.4, 88.2, 91.0, 89.5],
    "stddev": [null, 14.20, 15.10, 13.80],
    "alpha": [null, 1.25, 0.85, null],
    "beta": [null, 0.94, 0.96, 0.98],
    "rsquared": [null, 92.10, 91.40, null]
  },
  "benchmark": {
    "stddev": [null, 15.00, 16.20, 14.30]
  }
}
```
Arrays ordered [1Y, 3Y, 5Y, 10Y]. Map from fund RR010–RR013, RR152–RR155, RR158–RR161, RR015–RR017, RR003–RR004, RR00L–RR00N, and RR01P–RR01Q. Map benchmark standard deviation from RR015–RR017 only — do not include `benchmark.sharpe`. The Sharpe delta is left blank (no benchmark Sharpe is retrieved). The upside/downside capture delta is always `fund value − 100`. Use `null` for unavailable periods, including 1Y stddev/alpha/beta/R-squared, 10Y alpha, and 10Y R-squared when no datapoint is available.

If `BENCHMARK_CURRENCY_MISMATCH` is true, set `"benchmark": {}` to suppress all benchmark risk display.

### 4d. Missing Data Handling

| Situation | Behavior |
|---|---|
| Numeric field unavailable | Display "--" |
| Text field unavailable | Display "N/A" |
| Entire section unavailable (e.g. no analyst research) | Keep the section visible, show "Analyst research not available for this fund." |
| Chart data partially missing | Use `null` in the JSON array; the inline SVG renderer leaves missing points out and resumes when values return |
| Benchmark not resolvable | Show benchmark name as text; use `null` for all benchmark values in charts/tables |
| Benchmark currency ≠ fund currency | Set `BENCHMARK_CURRENCY_MISMATCH`; null all `benchmark` values in `CUMULATIVE_RETURNS_JSON`, set `"benchmark": {}` in `RISK_DATA_JSON`, set benchmark values to `null` in `TRAILING_RETURNS` and `ANNUAL_RETURNS`, and populate `BENCHMARK_CURRENCY_NOTE_TEXT` |

### 4e. Output

Write the final HTML to the active workspace or the user-requested output path. Present the HTML file path, plus the PDF file path if the sibling PDF copy was produced. Keep any accompanying text brief and mention important data limitations only when relevant. There are other fund analysis and fund rating skills available if the user wants a deeper dive into specific aspects of the fund.

## Step 5. Quality Checks

Before delivering the report file path to the user, verify:

- [ ] All "--" or "N/A" markers are explicit (no blank cells)
- [ ] File is fully self-contained (no relative asset paths)
- [ ] Report date = today's date
- [ ] Active/Index label derived correctly (OF00C for non-ETFs, OF00D for ETFs)
- [ ] Broad fund summary/analysis/report requests produced an HTML report, not only a text summary
- [ ] If the sibling PDF copy was produced, its file path is included with the HTML path
- [ ] If benchmark and fund currencies differ, `BENCHMARK_CURRENCY_NOTE` is non-empty, all benchmark chart/table series are suppressed, and `BENCHMARK_LEGEND_ENTRY` is `""`
