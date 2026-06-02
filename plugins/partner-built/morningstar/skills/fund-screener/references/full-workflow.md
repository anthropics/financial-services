# Partner-authored workflow details

# Fund Screener Skill
Production fund screener workflow. Output only values returned by Morningstar app tools in the current session.
> **AI-Generated Analysis using Morningstar's data and research**
> Not investment advice; for informational use only.
## Hard Rules
1. Morningstar app tools are the only data source.
2. Never infer, estimate, or backfill financial values.
3. Missing field: `N/A`.
4. Tool failure: `N/A`.
5. No recommendations, predictions, or suitability statements.
6. Universes allowed: FE, FO, FC. Do not include ST.
7. Screener is AND within a call. OR requires multiple calls plus merge/deduplicate by investment ID.
8. Before screening, normalize criteria with `morningstar-id-lookup-tool` for category, medalist, rating, and any other datapoint/filter name the user mentions.
9. If a datapoint or value does not match lookup output, stop and ask the user to correct it or confirm your suggested corrected value.
10. Cross-category disclosure: if results include funds from different Morningstar Categories, note that Category Rankings are only comparable within the same category peer group.
11. Number formatting: display percentages and ratios to 2 decimal places; rankings and rank values are whole numbers; format currency values with commas; abbreviate large AUM/asset values in millions (e.g. $1,234.56M) or billions (e.g. $1.23B) as appropriate.
## Workflow
| Phase | Goal | Tool |
|---|---|---|
| 1. Collect | Capture and confirm criteria | None |
| 2. Normalize | Resolve datapoint names and criterion values | morningstar-id-lookup-tool |
| 3. Screen | Run screener pass(es) | morningstar-screener-tool |
| 4. Validate | Exclude inactive funds by Fund Status | morningstar-data-tool |
| 5. Enrich | Retrieve returns/ranks/metadata/risk | morningstar-data-tool |
| 6. Present | Ranked output plus tightening suggestions | None |
## Phase 1 - Collect Criteria
Do not call tools until criteria are confirmed.
Required criteria:
- Universe: FE / FO / FC / combination
- Morningstar Category: value or no filter (e.g. Large Value, Small Growth, Moderate Allocation, Technology, Multistrategy)
- Medalist floor: Gold / Gold or Silver / Bronze+ / Any
- Star Rating floor: 3+ / 4+ / 5 / Any
- Max Expense Ratio: value or no filter
- Min AUM: value or no filter

If fields are missing, ask once for all missing fields; include a filled example reply (e.g. `"ETF, US Large Blend, Gold, 4+, max ER 0.50%, min AUM $1B, min 3-year return 10%"`). Inform users they can add extra filters beyond these defaults.
Then show this summary and wait for `confirm`:
```text
Here is the screen I will run:
- Universe: [...]
- Category: [... or no filter]
- Medalist Rating floor: [... or no filter]
- Morningstar Rating floor: [... or no filter]
- Max Expense Ratio: [... or no filter]
- Min AUM: [... or no filter]
Reply "confirm" to run, or tell me what to change.
```
## Phase 2 - Normalize Criteria with ID Lookup

Run `morningstar-id-lookup-tool` for all user-mentioned datapoints/filters before screening.

Required normalization coverage:
- Universe mapping: first attempt ID lookup normalization for any universe term the user provides; if lookup does not provide a usable universe value, apply strict FE/FO/FC mapping and ask user to clarify when ambiguous.
- Category criterion: verify user value against lookup-returned possible values.
- Medalist criterion: verify user value against lookup-returned possible values.
- Morningstar Rating criterion: verify user value against lookup-returned possible values.
- Any additional user-mentioned datapoint criterion: resolve datapoint name and verify value against possible values when available.

Mismatch handling:
- No good datapoint match: ask user for a different datapoint name.
- No good value match: ask user for a different value.
- Close value match exists: propose corrected value and ask user to confirm before proceeding.
- Multiple plausible matches: ask user to choose.

Do not run `morningstar-screener-tool` until all criteria are resolved and confirmed.

## Phase 3 - Run Screener
Universe mapping: ETF -> FE, Open-End Fund -> FO, Closed-End Fund -> FC.
Execution:
- Single universe: one screener call.
- Multi-universe: one call per universe, then merge/deduplicate by investment ID.
- OR medalist logic (Gold OR Silver): one call per medalist value, then merge/deduplicate.
Operators must be exactly `=`, `<`, `>`.
Result handling:
- Target 10 to 20 funds.
- If >20, keep 20 by lowest Net Expense Ratio first.
- If <5, identify the tightest criterion and suggest one relaxation.
- If 0, report likely binding criterion and ask what to relax.
## Phase 4 - Validate Fund Status
Call morningstar-data-tool for all candidates with `OS999`.
Exclude funds with inactive status (liquidated, merged, closed).
Report exclusions explicitly.
## Phase 5 - Retrieve Data
Call morningstar-data-tool for all remaining funds with all datapoints listed below.

Required in this Phase 5 call:
- Include `Inception Date` (`OS00F`) in `datapoint_ids` along with all other enrichment datapoints.

Validation checks:
- Inception consistency: if inception is too recent for a period, label `N/A - fund launched [year], insufficient history for [N]-year period`.
- If `OS00F` is missing for a fund, label `Inception Date` as `N/A` and skip inception-consistency validation for that fund.
- Preserve exact returned values and units.
- Do not create synthetic recommendation scores.
## Phase 6 - Output Format
Output order:
1. Disclosure banner — format as a blockquote:
> **AI-Generated Analysis using Morningstar's data and research**
> Not investment advice; for informational use only.
2. Criteria used — must be table, one row per active filter only; omit any criterion where no filter was applied:
3. Criteria normalization notes (only when corrections/confirmations were needed)
4. Result count and exclusions
5. Snapshot table
6. Performance (Returns) table
7. Risk (Mo-End) table
8. Category Rankings table
9. Calendar-year matrix
10. Follow-up tightening suggestions
Ranking order: Total Net Assets (AUM) descending.
Table readability rules: use one datapoint per row, avoid wrapped rows, and insert a blank line between each table/section.

### Snapshot Table
| Fund Name | Ticker | Type | Morningstar Category | Active/Passive | Benchmark | Morningstar Medalist Rating | Morningstar Star Rating | Net Expense Ratio | Total Net Assets (AUM) | Inception Date |
|---|---|---|---|---|---|---|---|---|---|---|

If no Morningstar Category filter was applied, or if results include funds from more than one Morningstar Category, display this warning immediately after the Snapshot table:
> **Cross-Category Warning:** Results include funds from multiple Morningstar Categories. Medalist Ratings and Category Rankings reflect performance relative to each fund's own category peer group and are not directly comparable across categories.

Fetch CNAXS (Morningstar Medalist Rating Disclosures Type) for all funds and apply as follows:
- If a fund's CNAXS = `Issuer Initiated Rating`, append `*` to that fund's Medalist Rating value in the Snapshot table (e.g. `Gold*`).
- If a fund's CNAXS = `Tracks Morningstar Index`, append `**` to that fund's Medalist Rating value (e.g. `Gold**`).
- After the Snapshot table, output only the applicable footnotes as blockquote text exactly as written below. Omit both entirely if all funds return NA — no message or explanation when omitted.

> *\* **Medalist Rating Disclaimer:** In Australia and New Zealand only, starting from June 2026, Morningstar may receive a fee from product issuers for preparing Morningstar Medalist Rating on their financial product(s) domiciled in Australia or New Zealand (an "Issuer Initiated Rating"). An Issuer Initiated Rating will apply to a strategy and its associated share classes. Morningstar will clearly identify each Issuer Initiated Rating on the front page of the report and will provide disclosure relating to the party that has paid the associated fee. Fees for an Issuer Initiated Rating are not linked to the rating outcome, and the paying entity has no influence over the analytical process or rating outcome.*

> *\*\* **Medalist Rating Disclaimer:** Certain managed investments use indexes created by and licensed from Morningstar, Inc., and its subsidiaries as their tracking index. We mitigate any actual or potential conflicts of interest arising from these activities by maintaining and enforcing information barriers, including both technological and non-technological controls, and conducting ongoing monitoring through Morningstar's Compliance department. Morningstar will clearly identify manager research related to such indexes on the front page of the report. Morningstar does not provide qualitative ratings or opinions for investments managed by Morningstar or managed investments that track Morningstar indexes that incorporate discretionary inputs assigned by Morningstar employees on an ongoing basis, such as Morningstar Economic Moat Ratings, or ESG Ratings.*

### Performance (Returns) Table
| Fund Name | Ticker | Total Return 1 Mo | Total Return 3 Mo | Total Return 6 Mo | Total Return 1 Yr | Total Return 3 Yr (Ann.) | Total Return 5 Yr (Ann.) | Total Return 10 Yr (Ann.) |
|---|---|---|---|---|---|---|---|---|

### Risk (Mo-End) Table
| Fund Name | Ticker | Portfolio Risk Score | Std Dev 1 Yr | Std Dev 3 Yr | Std Dev 5 Yr | Sharpe Ratio 1 Yr | Sharpe Ratio 3 Yr | Sharpe Ratio 5 Yr |
|---|---|---|---|---|---|---|---|---|

### Category Rankings Table
| Fund Name | Ticker | Category Rank 1 Yr | Category Rank 3 Yr | Category Rank 5 Yr | Category Rank 10 Yr |
|---|---|---|---|---|---|
*Category rank is percentile within Morningstar Category. Lower = better. Only directly comparable across funds in the same category — flag with a note if results span multiple categories.*
### Calendar-Year Matrix
| Fund Name | Ticker | Return {year} | Return {year-1} | Return {year-2} | Return {year-3} | Return {year-4} | Category Rank {year} | Category Rank {year-1} | Category Rank {year-2} | Category Rank {year-3} | Category Rank {year-4} |
|---|---|---|---|---|---|---|---|---|---|---|---|
Replace {year} with actual calendar year labels from Morningstar datapoint names.
## Follow-Up Suggestions
Always return 3 to 5 data-backed suggestions.
Allowed suggestion dimensions: Medalist floor, Star Rating floor, max expense ratio, minimum AUM, universe, category.
Quantify impact when possible.
Example: "Lowering ER cap from 0.50% to 0.20% would reduce results from 18 to 9."
Do not suggest unsupported filters.

After the suggestions, always ask:
> Would you like a detailed analysis of any specific fund from these results? If so, provide the fund identifier.
## Datapoints and Tool Usage
### Screener Datapoints (morningstar-screener-tool)
| Datapoint Name | Morningstar ID | Used For |
|---|---|---|
| Morningstar Medalist Rating | MMR01 | Medalist rating floor filter |
| Morningstar Rating Overall | RR01Y | Star rating floor filter |
| Morningstar Category | OF003 | Asset class/category filter |
| Net Expense Ratio | OS00M | Max expense ratio filter |
| Total Net Assets | OS006 | Fund size context |
### Enrichment Datapoints (morningstar-data-tool)
| Group | Datapoint Name | Morningstar ID |
|---|---|---|
| Performance | Total Ret 1 Mo (mo-end) | PM133 |
| Performance | Total Ret 3 Mo (mo-end) | PM006 |
| Performance | Total Ret 6 Mo (mo-end) | PM008 |
| Performance | 1 Year Total Return | PM00C |
| Performance | 3 Year Total Return Annualized | PM00E |
| Performance | 5 Year Total Return Annualized | PM00G |
| Performance | 10 Year Total Return Annualized | PM00I |
| Performance | Annual Ret {year} | AR002 |
| Performance | Annual Ret {year-1} | AR003 |
| Performance | Annual Ret {year-2} | AR004 |
| Performance | Annual Ret {year-3} | AR005 |
| Performance | Annual Ret {year-4} | AR006 |
| Category Rankings | 1 Year % Rank in Category | PM00D |
| Category Rankings | 3 Year % Rank in Category | PM00F |
| Category Rankings | 5 Year % Rank in Category | PM00H |
| Category Rankings | 10 Year % Rank in Category | PM00J |
| Category Rankings | Annual Ret % Rank Cat {year} | AR00E |
| Category Rankings | Annual Ret % Rank Cat {year-1} | AR00F |
| Category Rankings | Annual Ret % Rank Cat {year-2} | AR00G |
| Category Rankings | Annual Ret % Rank Cat {year-3} | AR00H |
| Category Rankings | Annual Ret % Rank Cat {year-4} | AR00I |
| Risk | Morningstar Portfolio Risk Score | QFR0H |
| Risk | Std Dev 1 Yr (Mo-End) | RR014 |
| Risk | Std Dev 3 Yr (Mo-End) | RR015 |
| Risk | Std Dev 5 Yr (Mo-End) | RR016 |
| Risk | Sharpe Ratio 1 Yr (Mo-End) | RR010 |
| Risk | Sharpe Ratio 3 Yr (Mo-End) | RR011 |
| Risk | Sharpe Ratio 5 Yr (Mo-End) | RR012 |
| Fund Metadata | Net Expense Ratio | OS00M |
| Fund Metadata | Total Net Assets | OS006 |
| Fund Metadata | Inception Date | OS00F |
| Fund Metadata | Fund Status | OS999 |
| Fund Metadata | Morningstar Category | OF003 |
| Fund Metadata | Morningstar Medalist Rating | MMR01 |
| Fund Metadata | Morningstar Medalist Rating Disclosures Type | CNAXS |
| Fund Metadata | Morningstar Rating Overall | RR01Y |
| Fund Context | Actively Managed | OF00D |
| Fund Context | Index Fund | OF00C |
| Fund Context | Enhanced Index | OF005 |
| Fund Context | Primary Prospectus Benchmark | OF00L |
| Fund Context | Morningstar Category Index | OS38B |
