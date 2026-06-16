# Partner-authored workflow details

# Fund Summary Skill

A skill for generating a fund summary or self-contained HTML report with Morningstar insights into a given fund. This skill uses Morningstar MCP tools as the only data source.

> Guardrails are defined in `SKILL.md` and the same apply here.

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

1. **Resolve** the fund from ticker, name, or Morningstar identifier using `morningstar_id_lookup_tool`. Ask only if the match is ambiguous.
2. **Retrieve all fund data in parallel batches.** Fire these as simultaneously as possible — do not wait for one group before starting the next:
   - **Batch A — Core metadata + IP**: all IDs from Core Metadata and Morningstar IP sections in one call to `morningstar_data_tool`
   - **Batch B — Performance, risk + monthly returns**: all performance/risk IDs (including HP010 trailing 10 years) in one call; split into two calls only if the response is truncated
   - **Batch C — Holdings**: all holdings IDs in one `morningstar_data_tool` call
   - **Batch D — Analyst research**: `morningstar_analyst_research_tool` (one call)
   - **Batch E — Holdings list**: `morningstar_fund_holdings_tool` (one call)
   - **Retries**: if a call returns a tool error (not empty data), retry that call once before treating the data as unavailable.
3. **Retrieve benchmark data** as soon as Batch A returns (you only need OF00P from it — do not wait for B–E to finish). Fire one `morningstar_data_tool` call for the benchmark ID: base currency (LS05M), HP010 monthly returns (trailing 10 years), and trailing/annual returns (PD00B, PD00D, PD014, PD00F, PD00H, PM494, HS803, RR015/016/017). Retry once on tool error.
4. **Deliver output** — Markdown by default; create self-contained HTML only if the user explicitly asks. See the two output workflows below.

## Datapoint Map

Batch as many datapoint IDs as possible into a single `morningstar_data_tool` call. Only split across multiple calls if the response is actually truncated — do not pre-emptively chunk.

### Core Metadata
| Datapoint | ID | Notes |
|---|---|---|
| Name | OS01W | |
| Ticker | OS385 | |
| Fund Standard Name | AA0B3 | |
| Morningstar Category | OF003 | |
| Fund Inception Date | OS00F | |
| Oldest Share Class Inception | OD003 | |
| Index Fund | OF00C | Active/passive for non-ETFs |
| Actively Managed | OF00D | ETFs only; ignore for open-end funds |
| Investment Type | LS466 | |
| Base Currency | LS05M | Display as-is; used only to populate the field and compare against benchmark currency |
| Fund Size | OF009 | Format as compact string, e.g. `1.23B`, `456.70M` |
| Share Class Closed to New Inv | OS387 | |
| Minimum Initial Purchase | OS00U | Format as comma-formatted number, no symbol (e.g. `3,000`) |
| Fee Level - Broad | UB412 | |
| Fee Level - Distribution | OS707 | |
| Prospectus Adjusted Expense Ratio | ZZ007 | |
| Category Index Id | OS38A | |
| Primary Prospectus Benchmark Id | OF00P | Use for benchmark retrieval |
| Primary Prospectus Benchmark | OF00L | |
| Manager Name (all) | OF015 | Returns array of all manager names |
| Longest Tenured Manager Name | OF059 | Used to match start_date in MANAGERS list |
| Longest Tenured Manager Start Date | OF050 | |
| Manager Ownership Level | OS276 | Returns array of "Name [$X - Range]" strings |
| Turnover Ratio % | OS03S | |
| 12 Mo Yield | PM032 | |
| SEC Yield | PM002 | |
| NAV (Daily) | OS060 | Format as raw number with commas, no symbol (e.g. `68.40`) |
| Est Net Flow 1 Mo | HS338 | Format as compact string with sign, e.g. `1.23B`, `-456.70M` |
| Est Net Flow 3 Mo | HS339 | Same |
| Est Net Flow 1 Yr | HS342 | Same |
| Morningstar Medalist Rating | MMR01 | |

### Performance and Risk
| Datapoint | ID | Notes |
|---|---|---|
| Yearly Return | HS803 | Timeseries: request completed calendar years (e.g. 2015-01-01 to 2025-12-31); use for ANNUAL_RETURNS_ROWS |
| Monthly Return | HP010 | Timeseries: trailing 10 years. Pass as `MONTHLY_RETURNS_JSON`; renderer computes Growth of $10k |
| Total Ret YTD (Daily) | PD00B | |
| Total Ret 1 Yr (Daily) | PD00D | |
| Total Ret Annlzd 2 Yr (Daily) | PD014 | |
| Total Ret Annlzd 3 Yr (Daily) | PD00F | |
| Total Ret Annlzd 5 Yr (Daily) | PD00H | |
| Total Ret Annlzd 10 Yr (Daily) | PM494 | |
| Return Date (Daily) | PD001 | Use as DATA_AS_OF_DATE |
| Annual Ret % Rank Cat {year} through {year-10} | AR00E–AR00O | |
| Sharpe Ratio 1/3/5/10 Yr (Mo-End) | RR010–RR013 | |
| Std Dev 3/5/10 Yr (Mo-End) | RR015, RR016, RR017 | |
| Alpha 3/5 Yr (Mo-End) | RR003–RR004 | |
| Beta 3/5/10 Yr (Mo-End) | RR00L–RR00N | |
| R-Squared 3/5 Yr (Mo-End) | RR01P–RR01Q | |
| Upside Capture 1/3/5/10 Yr (Mo-End) | RR152–RR155 | |
| Downside Capture 1/3/5/10 Yr (Mo-End) | RR158–RR161 | |

### Holdings
| Datapoint | ID |
|---|---|
| Asset Alloc Equity % (Long Rescaled) | HS02E |
| Asset Alloc Bond % (Long Rescaled) | HS02D |
| Asset Alloc Cash % (Long Rescaled) | HS00X |
| Asset Alloc Conv Bond % (Long Rescaled) | HS00Y |
| Asset Alloc Pref Stock % (Long Rescaled) | HS00T |
| Equity Style Box (Long) | HS05A |
| Fixed Income Style Box | HS00L |
| Average Eff Duration Survey | HS02F |
| Average Credit Quality | HS00C |
| Fixed-Inc Region: US, Canada, UK, Europe dev, Japan, Australasia, Asia dev, Emerging, Not Classified | HS125, HS122, FR1AG, FR1AB, FR1AD, FR1A6, FR1A8, FR1A2, FR1A3 |
| Equity Region: N. America, Latin America, UK, Europe dev, Europe emrg, Africa/ME, Japan, Australasia, Asia dev, Asia emrg | HS05C, HS06D, HS06E, HS07S, HS06H, HS006, HS06K, HS06L, HS06N, HS06M |
| Market Cap: Giant, Large, Mid, Small, Micro | HS039, HS03P, HS049, HS05Z, HS03Z |
| P/E, P/B, P/S Ratio (Long) | HS067, HS064, HS068 |
| Dividend Yield %, Sales Growth %, Cash-Flow Growth % | HS066, HS035, HS033 |
| Average Market Cap (mil) | HS03W |
| Financial Health Grade, Growth Grade, Cash Return % | HS05I, HS05K, HS05L |
| Number of Holdings (Long) | HS256 | Set as `NUM_HOLDINGS` |
| Ownership Breadth | CEIDQ |
| Liquidity Intermittent Weight % | MKDXK |

Also call `morningstar_fund_holdings_tool` for top holdings.

### Morningstar IP
| Datapoint | ID |
|---|---|
| Medalist Rating | MMR01 |
| Medalist Rating Disclosures Type | CNAXS |
| Morningstar Rating Overall | RR01Y |
| Portfolio Risk Score | QFR0H |
| Analyst Driven % | MMR04 |
| Parent Pillar / Score Type | MMR1E, MMR14 |
| People Pillar / Score Type | MMR2E, MMR24 |
| Price Score | MMRGS |
| Process Pillar / Score Type | MMR3E, MMR34 |

### Benchmark Data
Retrieve using the Primary Prospectus Benchmark ID (datapoint: OF00P).

| Datapoint | ID | Notes |
|---|---|---|
| Base Currency | LS05M | Pass as `BENCHMARK_CURRENCY`; renderer computes the currency gate automatically |
| Yearly Return | HS803 | Timeseries |
| Monthly Return | HP010 | Timeseries; pass as benchmark values in `MONTHLY_RETURNS_JSON` |
| Total Ret (Daily) YTD / 1/2/3/5/10 Yr | PD00B, PD00D, PD014, PD00F, PD00H, PM494 | |
| Std Dev 3/5/10 Yr (Mo-End) | RR015, RR016, RR017 | Only std dev; do not retrieve benchmark Sharpe, alpha, beta, or R-squared since these are already benchmark relative. |

**Benchmark Currency Gate**: pass `BENCHMARK_CURRENCY` (the benchmark's LS05M value) in the data package. The renderer compares it to `BASE_CURRENCY`, sets `BENCHMARK_CURRENCY_MISMATCH`, and auto-generates `BENCHMARK_LEGEND_ENTRY` and `BENCHMARK_CURRENCY_NOTE`. Your only responsibility: if the two currencies differ, omit Benchmark and Excess rows from `TRAILING_RETURNS_ROWS` and `ANNUAL_RETURNS_ROWS`. Do not null benchmark scalar values — just omit the rows.

## Output Workflow A — Markdown (default)

Use when the user has not explicitly requested an HTML report.

Apply the Formatting Rules table above to all displayed values. Mirror the structure and section depth of the HTML report, using Markdown headers, bold labels, horizontal rules, and tables so the output renders richly inline in chat.

Present in this order:

---
*AI-generated analysis using Morningstar data. For informational purposes only — not investment advice.*

---

### 1. Fund Snapshot
Two-column key/value table: name, ticker, category, investment type, active/passive, inception date, benchmark, AUM, expense ratio, fee level, NAV, yield. Highlight closed-to-new-investors status in bold if applicable.

### 2. Ratings
Present as a compact table with columns: **Medalist Rating**, **Star Rating**, **MPRS**, and analyst-driven %. Follow with a **Pillar Ratings** sub-table (Process / People / Parent / Price). Then quote the analyst summary in a blockquote if available.

### 3. Performance
**Trailing Returns** (`unit` value as column header, e.g. `% Total Return`): table with periods as rows and Fund / Benchmark / Excess as columns. Excess = fund − benchmark; show `--` if benchmark currency differs from fund currency.

**Calendar-Year Returns**: table with years as columns and Fund / Benchmark / Cat Rank as rows. Show `--` if benchmark currency differs from fund currency.

### 4. Risk
**Capture Ratios**: table — periods (1/3/5/10 yr) as columns, Upside Capture / Downside Capture as rows.

**Risk Statistics**: table — periods as columns, Std Dev / Sharpe / Alpha / Beta / R-Squared as rows (fund vs. benchmark std dev where applicable).

### 5. Portfolio
**Asset Allocation**: small table — Equity / Bond / Cash / Other with % values.

**Top 10 Holdings**: ranked table — Holding / Weight (%).

**Style & Exposure** (if available): style box description in text (e.g. "Large-Cap Blend"), followed by compact region-exposure table and market-cap breakdown table.

**Equity Stats** (if available): P/E, P/B, P/S, dividend yield %, sales growth %, cash-flow growth %, average market cap, financial health grade, growth grade, cash return % — presented as a two-column key/value table. Only include rows with available data.

### 6. Fees, Flows & Operations
Table: expense ratio, fee level, turnover. Then flows table: 1M / 3M / 1Y. Then manager block: name, start date (longest-tenured only), ownership level for each manager. Flag closed to new investors if applicable.

---
*Data as of `DATA_AS_OF_DATE`. Report generated `REPORT_DATE`.*

---

For narrow questions, answer only the requested section or metric.

## Output Workflow B — HTML Report (explicit request only)

Use when the user explicitly asks for an HTML report, a self-contained file, or similar.

Assemble a flat data package and pass to the renderer. **The model is responsible for formatting all scalar values and building all HTML row strings.** The renderer only handles assets that require filesystem I/O (logo, icons) and SVG charts that require math (Growth of $10k line chart, allocation donut). Everything else must be set by the model before calling render_report.

### Worked example — minimal complete data package

Build this dict in memory from MCP responses, then pass directly to `render_report`. Do not write intermediate JSON files or helper scripts — assemble the dict inline and call `render_report` once.

```python
data = {
    # --- Scalars (format before setting) ---
    "FUND_NAME":              "Vanguard Total International Stock ETF",
    "TICKER":                 "VXUS",
    "FUND_STANDARD_NAME":     "Vanguard Total International Stock ETF",
    "CATEGORY":               "Foreign Large Blend",
    "INVESTMENT_TYPE":        "ETF",
    "ACTIVE_INDEX_LABEL":     "Index",
    "BASE_CURRENCY":          "USD",
    "INCEPTION_DATE":         "2011-01-26",
    "OLDEST_SHARE_CLASS_INCEPTION": "2011-01-26",
    "CLOSED_TO_NEW":          "No",
    "PROSPECTUS_BENCHMARK":   "FTSE Global All Cap ex US NR USD",
    "BENCHMARK_NAME":         "FTSE Global All Cap ex US",
    "FUND_SIZE":              "$74.5B",
    "NAV":                    "$68.4",
    "MIN_INITIAL_PURCHASE":   "1",
    "EXPENSE_RATIO":          "0.07%",
    "FEE_LEVEL":              "Low",
    "FEE_LEVEL_DISTRIBUTION": "Low",
    "TWELVE_MONTH_YIELD":     "3.12%",
    "SEC_YIELD":              "3.05%",
    "TURNOVER_RATIO":         "4.00%",
    "EST_NET_FLOW_1M":        "$1.2B",
    "EST_NET_FLOW_3M":        "-$456.0M",
    "EST_NET_FLOW_1Y":        "$2.1B",
    "NUM_HOLDINGS":           "8793",
    "PCT_TOP_10":             "10.23%",
    "OWNERSHIP_BREADTH":      "Wide",
    "LIQUIDITY_INTERMITTENT": "0.05%",
    "MEDALIST_RATING":        "Gold",
    "MEDALIST_ANALYST_PCT":   "100",
    "MEDALIST_DISCLOSURE_TYPE": "Analyst",  # pass CNAXS value as-is; "" or omit if unavailable
    # MEDALIST_DISCLOSURE_TYPE_DISPLAY and MEDALIST_DISCLOSURE_FOOTNOTE are AUTO —
    # icon_embedder generates them from MEDALIST_DISCLOSURE_TYPE; do not set them manually
    "STAR_RATING":            "3",
    "MPRS":                   "82",
    "PROCESS_RATING":         "Above Average", "PROCESS_SCORE_TYPE": "Quantitative",
    "PEOPLE_RATING":          "Above Average", "PEOPLE_SCORE_TYPE":  "Quantitative",
    "PARENT_RATING":          "Above Average", "PARENT_SCORE_TYPE":  "Quantitative",
    "PRICE_RATING":           "2",
    "ALLOC_EQUITY_FUND":      "98.50%",
    "ALLOC_BOND_FUND":        "0.00%",
    "ALLOC_CASH_FUND":        "1.20%",
    "ALLOC_ALT_FUND":         "0.00%",
    "ALLOC_OTHER_FUND":       "0.30%",
    "STYLE_BOX_EQUITY":       "Foreign Large Blend",
    "STYLE_BOX_FIXED_INCOME": "N/A",
    "FI_DURATION":            "--",
    "FI_CREDIT_QUALITY":      "--",
    "DATA_AS_OF_DATE":        "2025-05-31",
    "REPORT_DATE":            "2026-06-11",
    "BENCHMARK_CURRENCY":         "USD",  # benchmark's LS05M; renderer derives gate, legend, and note

    # --- Section visibility (set ALL of these — never leave unset) ---
    "RISK_SECTION_CLASS":                      "",
    "FIXED_INCOME_SECTION_CLASS":              "is-empty",
    "FIXED_INCOME_STATS_SECTION_CLASS":        "is-empty",
    "FIXED_INCOME_REGION_SECTION_CLASS":       "is-empty",
    "EQUITY_PROFILE_SECTION_CLASS":            "",
    "REGIONAL_EXPOSURE_SECTION_CLASS":         "",
    "MARKET_CAP_SECTION_CLASS":                "",
    "EQUITY_PORTFOLIO_STATS_SECTION_CLASS":    "",
    "STYLE_BOX_SECTION_CLASS":                 "",

    # --- Section notes (set to "" unless a note is warranted) ---
    "FIXED_INCOME_SECTION_NOTE":               "",
    "REGIONAL_EXPOSURE_SECTION_NOTE":          "",
    "MARKET_CAP_SECTION_NOTE":                 "",
    "EQUITY_PORTFOLIO_STATS_SECTION_NOTE":     "",

    # --- Analyst summaries (one <p> per paragraph) ---
    "ANALYST_SUMMARY": "<p>Vanguard Total International Stock ETF offers broad exposure to non-US equities at a rock-bottom fee.</p>",
    "PROCESS_SUMMARY_HTML": "<p>The fund tracks the FTSE Global All Cap ex US Index using full replication.</p>",
    "PEOPLE_SUMMARY_HTML":  "<p>Vanguard's indexing team is deep and experienced.</p>",
    "PARENT_SUMMARY_HTML":  "<p>Vanguard's investor-owned structure aligns its interests with shareholders.</p>",
    "PRICE_SUMMARY_HTML":   "<p>At 0.07% the expense ratio is among the lowest in the category.</p>",

    # --- Managers ---
    "MANAGERS_HTML": (
        '<div class="manager">'
        '<div class="manager-avatar">WC</div>'
        '<div><div class="manager-name">William Coleman</div>'
        '<div class="manager-meta">Since 2019-04-01 &middot; Ownership: $100,001 - $500,000</div>'
        '</div></div>'
    ),

    # --- Returns tables ---
    "TRAILING_RETURNS_UNIT": "% Total Return",
    "TRAILING_RETURNS_ROWS": (
        '<tr class="row-fund"><td>Fund</td><td>9.43</td><td>24.44</td><td>19.65</td><td>17.45</td><td>7.53</td><td>9.49</td></tr>'
        '<tr><td>Benchmark</td><td>10.16</td><td>25.58</td><td>20.30</td><td>17.84</td><td>7.76</td><td>9.54</td></tr>'
        '<tr class="row-excess"><td>Excess</td><td>-0.73</td><td>-1.15</td><td>-0.65</td><td>-0.39</td><td>-0.23</td><td>-0.05</td></tr>'
    ),
    "ANNUAL_RETURNS_HEADERS": "<th>2020</th><th>2021</th><th>2022</th><th>2023</th><th>2024</th>",
    "ANNUAL_RETURNS_ROWS": (
        '<tr class="row-fund"><td>Fund</td><td>11.28</td><td>8.06</td><td>-16.00</td><td>15.66</td><td>4.82</td></tr>'
        '<tr><td>Benchmark</td><td>11.06</td><td>8.31</td><td>-15.88</td><td>15.87</td><td>5.08</td></tr>'
        '<tr class="row-excess"><td>Excess</td><td>+0.22</td><td>-0.25</td><td>-0.12</td><td>-0.21</td><td>-0.26</td></tr>'
        '<tr><td>Percentile Rank</td><td>48</td><td>52</td><td>47</td><td>51</td><td>70</td></tr>'
    ),

    # --- Top holdings ---
    "TOP_HOLDINGS_ROWS": (
        "<tr><td>Taiwan Semiconductor Manufacturing</td><td>2.45%</td></tr>"
        "<tr><td>Novo Nordisk A/S</td><td>1.32%</td></tr>"
        "<tr><td>Samsung Electronics</td><td>1.18%</td></tr>"
    ),

    # --- Risk tables (4 columns: 1Y, 3Y, 5Y, 10Y) ---
    # Color rules for RISK_CAPTURE_ROWS:
    #   delta = round(value - 100, 2), formatted with explicit sign (e.g. "-2.80", "+0.61")
    #   Upside Capture:   delta > 0 → delta-positive (▲ green); delta < 0 → delta-negative (▼ red)
    #   Downside Capture: delta < 0 → delta-positive (▲ green, fund protected more than benchmark)
    #                     delta > 0 → delta-negative (▼ red, fund fell more than benchmark)
    #   Sharpe Ratio: no delta span — just metric-fund value
    # Color rules for RISK_STATS_ROWS:
    #   Std Deviation: fund value in metric-fund; benchmark value below using metric-benchmark (no arrow)
    #   Alpha / Beta / R-Squared: metric-fund only, no delta (already benchmark-relative)
    "RISK_CAPTURE_ROWS": (
        '<tr><td>Sharpe Ratio</td>'
        '<td><span class="metric-fund">0.55</span></td>'
        '<td><span class="metric-fund">0.61</span></td>'
        '<td><span class="metric-fund">0.48</span></td>'
        '<td><span class="metric-fund">0.52</span></td>'
        '</tr>'
        '<tr><td>Upside Capture</td>'
        '<td><span class="metric-fund">97.2</span><span class="metric-delta delta-negative">-2.80</span></td>'
        '<td><span class="metric-fund">98.1</span><span class="metric-delta delta-negative">-1.90</span></td>'
        '<td><span class="metric-fund">98.5</span><span class="metric-delta delta-negative">-1.50</span></td>'
        '<td><span class="metric-fund">99.0</span><span class="metric-delta delta-negative">-1.00</span></td>'
        '</tr>'
        '<tr><td>Downside Capture</td>'
        '<td><span class="metric-fund">98.3</span><span class="metric-delta delta-positive">-1.70</span></td>'
        '<td><span class="metric-fund">97.8</span><span class="metric-delta delta-positive">-2.20</span></td>'
        '<td><span class="metric-fund">98.0</span><span class="metric-delta delta-positive">-2.00</span></td>'
        '<td><span class="metric-fund">98.5</span><span class="metric-delta delta-positive">-1.50</span></td>'
        '</tr>'
    ),
    "RISK_STATS_ROWS": (
        '<tr><td>Std Deviation</td>'
        '<td><span class="metric-fund">&#8212;</span></td>'
        '<td><span class="metric-fund">14.20</span><span class="metric-benchmark">benchmark 13.92</span></td>'
        '<td><span class="metric-fund">15.10</span><span class="metric-benchmark">benchmark 15.48</span></td>'
        '<td><span class="metric-fund">13.80</span><span class="metric-benchmark">benchmark 15.10</span></td>'
        '</tr>'
        '<tr><td>Alpha</td>'
        '<td><span class="metric-fund">&#8212;</span></td>'
        '<td><span class="metric-fund">-0.42</span></td>'
        '<td><span class="metric-fund">-0.25</span></td>'
        '<td><span class="metric-fund">&#8212;</span></td>'
        '</tr>'
    ),

    # --- Portfolio rows ---
    # REGIONAL_EXPOSURE_HEADER / MARKET_CAP_HEADER: include the Benchmark column ONLY
    # if the benchmark actually returned data for those rows. If all benchmark values
    # are null, use only "<tr><th>Region</th><th>Fund</th></tr>" (no Benchmark column)
    # and omit the benchmark <td> from every row in REGIONAL_EXPOSURE_ROWS_HTML.
    # The example below shows the with-benchmark variant; adjust when data is absent.
    "REGIONAL_EXPOSURE_HEADER": "<tr><th>Region</th><th>Fund</th><th>Benchmark</th></tr>",
    "REGIONAL_EXPOSURE_ROWS_HTML": (
        '<tr><td>Greater Europe</td>'
        '<td><div class="region-cell"><span class="region-bar"><span style="width:38.5%"></span></span><span class="region-value">38.50%</span></div></td>'
        '<td><div class="region-cell"><span class="region-bar bench"><span style="width:38.2%"></span></span><span class="region-value">38.20%</span></div></td>'
        '</tr>'
    ),
    "MARKET_CAP_HEADER": "<tr><th>Market Cap</th><th>Fund</th><th>Benchmark</th></tr>",
    "MARKET_CAP_ROWS_HTML": (
        '<tr><td>Giant</td>'
        '<td><div class="region-cell"><span class="region-bar"><span style="width:40.1%"></span></span><span class="region-value">40.10%</span></div></td>'
        '<td><div class="region-cell"><span class="region-bar bench"><span style="width:39.8%"></span></span><span class="region-value">39.80%</span></div></td>'
        '</tr>'
    ),
    "FIXED_INCOME_REGION_HEADER": "",
    "FIXED_INCOME_REGION_ROWS_HTML": "",
    "EQUITY_PORTFOLIO_STATS_HEADER": "<tr><th>Statistic</th><th>Fund</th></tr>",
    "EQUITY_PORTFOLIO_STATS_ROWS_HTML": (
        "<tr><td>P/E Ratio</td><td>14.20</td></tr>"
        "<tr><td>P/B Ratio</td><td>1.82</td></tr>"
    ),
    "STYLE_BOX_ROWS": "<tr><td>Equity Style Box</td><td>Foreign Large Blend</td></tr>",

    # --- Chart inputs (AUTO fields built from these by renderer) ---
    # MONTHLY_RETURNS_JSON merges TWO SEPARATE HP010 series into one list by date:
    #   fund_return      — HP010 retrieved on the FUND ID
    #   benchmark_return — HP010 retrieved on the BENCHMARK ID (step 3 above)
    # These are different numbers from different securities. Do NOT reuse the fund's
    # HP010 for benchmark_return. Match rows by date; use null for benchmark_return
    # only when BENCHMARK_CURRENCY_MISMATCH is true or a date has no benchmark data.
    "MONTHLY_RETURNS_JSON": [
        {"date": "2016-06-30", "fund_return": 0.52, "benchmark_return": 0.61},
        {"date": "2016-07-31", "fund_return": 1.84, "benchmark_return": 1.92},
        # ... full 10-year HP010 history, one entry per month ...
    ],
    "ASSET_ALLOCATION_JSON": [
        {"label": "Equity", "value": 98.5},
        {"label": "Cash",   "value": 1.2},
        {"label": "Other",  "value": 0.3},
    ],
}

from render import render_report
render_report(data, output_path="{TICKER}-fund-summary.html")
```

After `render_report` completes, render the output file as an inline HTML artifact so the user can see it immediately. Do not just report the file path.

Every key shown above must be set. Replace the sample values with actual MCP data. Do not write a builder script — assemble `data` inline and call `render_report` once.

**Renderer-only — do not set these manually:** `RETURNS_CHART_SVG` (AUTO from `MONTHLY_RETURNS_JSON`), `DONUT_CHART_SVG` (AUTO from `ASSET_ALLOCATION_JSON`), `BENCHMARK_CURRENCY_MISMATCH`, `BENCHMARK_LEGEND_ENTRY`, `BENCHMARK_CURRENCY_NOTE` (AUTO from `BASE_CURRENCY` and `BENCHMARK_CURRENCY`), `STAR_RATING_DISPLAY`, `STAR_RATING_ICON`, `MPRS_VISUAL`, `*_ICON`, `*_SCORE_SCALE`, `PRICE_SCORE`, `MEDALIST_DISCLOSURE_TYPE_DISPLAY`, `MEDALIST_DISCLOSURE_FOOTNOTE`, `LOGO_BASE64`. If chart data is genuinely unavailable, set the placeholder to `""` — never a prose message string.

**Before rendering:** every `*_SECTION_CLASS` must be `""` or `"is-empty"`; every `*_SECTION_NOTE` and `*_HEADER` must be set (use `""` when empty). Never leave these unset.

## HTML Report Support

Use `scripts/render.py` with `assets/template.html` and `assets/icons/`. The renderer embeds the logo, selects icon SVGs, builds the Growth of $10k and allocation charts, substitutes all `{{PLACEHOLDER}}` tokens, and writes the output file. All other content must be provided by the model in the data package.

CLI: `python <skill-dir>/scripts/render.py --data data.json --output <ticker>-fund-summary.html`

Output file is written to the current working directory as `{TICKER}-fund-summary.html`. After writing, render it as an inline HTML artifact.

## Quality Checks

- All `--` / `N/A` markers are explicit; no blank cells or unresolved `{{...}}` tokens.
- `REPORT_DATE` = today's date. `DATA_AS_OF_DATE` = PD001 value.
- Active/Index label: non-ETFs use OF00C; ETFs use OF00D.
- `BENCHMARK_CURRENCY_NOTE` non-empty and benchmark rows/chart suppressed when currencies differ.
- File is fully self-contained (no relative asset paths).
