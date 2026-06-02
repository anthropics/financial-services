# Partner-authored workflow details

# Fund Comparison Skill
Side-by-side comparison of 2 to 4 ETFs or funds using Morningstar app tools only.
> **AI-Generated Analysis using Morningstar's data and research**
> Not investment advice; for informational use only.
## Hard Rules
1. Morningstar app tools are the only data source.
2. Never infer, estimate, or backfill financial values.
3. Missing field: `N/A`.
4. Tool failure: `N/A`.
5. No recommendations, predictions, or suitability statements.
6. Supported types: FE, FO, FC only. If any input resolves to ST, exclude that investment and notify the user.
7. Maximum 4 funds. If more than 4 are provided, ask the user to narrow the list before proceeding.
8. Number formatting: display percentages and ratios to 2 decimal places; rankings and rank values are whole numbers; format currency values with commas; abbreviate large AUM/asset values in millions (e.g. $1,234.56M) or billions (e.g. $1.23B) as appropriate.
9. Cross-category disclosure: if any funds belong to different Morningstar Categories, display a prominent warning that Medalist Ratings and Category Rankings are not directly comparable across categories and should be interpreted with caution.
## Workflow
| Phase | Goal | Tool |
|---|---|---|
| 1. Resolve | Convert all inputs to Morningstar IDs, validate types | morningstar-id-lookup-tool |
| 2. Retrieve | Pull all datapoints for all funds in one call | morningstar-data-tool |
| 3. Holdings | Retrieve top 10 holdings (equity funds only) | morningstar-fund-holdings-tool |
| 4. Present | Output comparison tables and overlap| None |
## Phase 1 - Resolve
Call `morningstar-id-lookup-tool` for each input fund.
- Proceed only for FE, FO, FC. Exclude and notify the user for any ST result.
- If fewer than 2 valid funds remain after exclusions, stop and ask the user to provide at least 2 supported funds.
- If multiple matches for a name, prefer exact ticker match; ask user to confirm if still ambiguous.
- Store all resolved Morningstar IDs.
## Phase 2 - Retrieve Data
Call `morningstar-data-tool` once with the resolved ID and all datapoints in the Datapoints Reference below.
- If Fund Status (`OS999`) indicates inactive for any fund, exclude the fund from the comparison. If fewer than 2 valid funds remain after exclusions, stop the workflow and indicate to the user "[Identifier] is inactive. Provide at least 2 active funds for comparison."
- Check `Morningstar Category Broad Group` (`OF035`) for all funds. If any two funds have different broad groups, stop immediately and respond: "[Fund A] is an [Equity/Fixed Income/etc.] fund and [Fund B] is an [Equity/Fixed Income/etc.] fund. Cross-asset-class comparisons are not supported as the metrics, benchmarks, and peer groups are fundamentally incompatible. Please provide funds from the same broad asset class."
## Phase 3 - Holdings
Only run this phase if the funds' `OF035` broad group is Equity. For all other broad groups (Fixed Income, Allocation, etc.), skip this phase entirely — do not call `morningstar-fund-holdings-tool` and omit the Holdings Overlap section from the output.

If proceeding: call `morningstar-fund-holdings-tool` once with all resolved IDs and `num_holdings: 10`.
After retrieval, identify overlapping holdings:
- A holding overlaps if the same security (matched by ticker or name) appears in 2 or more funds.
- Record each overlapping security, which funds it appears in, and the weight in each fund.
## Phase 4 - Output Format
Output order:
1. Disclosure banner — format as a blockquote:
> **AI-Generated Analysis using Morningstar's data and research**.
> Not investment advice; for informational use only.
2. Snapshot comparison
3. Performance (Returns) comparison
4. Category Rankings comparison
5. Risk Metrics comparison
6. Calendar-Year Returns comparison
7. Holdings Overlap *(equity funds only — omit this section for non-equity broad groups)*
In all comparison tables, funds are columns and metrics are rows.
Label each fund column as `[Ticker] — [Name]` consistently throughout.
Use markdown table spacing for readability: one metric per row, no wrapped rows, and insert a blank line between major sections.
If funds span multiple Morningstar Categories, display this warning immediately after the Snapshot table:
> **Cross-Category Warning:** These funds belong to different Morningstar Categories. Medalist Ratings and Category Rankings reflect performance relative to each fund's own category peer group and are not directly comparable across categories.
### Snapshot Comparison
| Metric | [Fund A] | [Fund B] | [Fund C] | [Fund D] |
|---|---|---|---|---|
| Type | | | | |
| Broad Asset Class | | | | |
| Category | | | | |
| Medalist Rating | | | | |
| Star Rating | | | | |
| Expense Ratio | | | | |
| AUM | | | | |
| Inception Date | | | | |
| Fund Status | | | | |
| Active/Passive | | | | |
| Benchmark | | | | |

Fetch CNAXS (Morningstar Medalist Rating Disclosures Type) for all funds and apply as follows:
- If a fund's CNAXS = `Issuer Initiated Rating`, append `*` to that fund's Medalist Rating value in the Snapshot table (e.g. `Gold*`).
- If a fund's CNAXS = `Tracks Morningstar Index`, append `**` to that fund's Medalist Rating value (e.g. `Gold**`).
- After the Snapshot table, output only the applicable footnotes as blockquote text exactly as written below. Omit both entirely if all funds return NA — no message or explanation when omitted.

> *\* **Medalist Rating Disclaimer:** In Australia and New Zealand only, starting from June 2026, Morningstar may receive a fee from product issuers for preparing Morningstar Medalist Rating on their financial product(s) domiciled in Australia or New Zealand (an "Issuer Initiated Rating"). An Issuer Initiated Rating will apply to a strategy and its associated share classes. Morningstar will clearly identify each Issuer Initiated Rating on the front page of the report and will provide disclosure relating to the party that has paid the associated fee. Fees for an Issuer Initiated Rating are not linked to the rating outcome, and the paying entity has no influence over the analytical process or rating outcome.*

> *\*\* **Medalist Rating Disclaimer:** Certain managed investments use indexes created by and licensed from Morningstar, Inc., and its subsidiaries as their tracking index. We mitigate any actual or potential conflicts of interest arising from these activities by maintaining and enforcing information barriers, including both technological and non-technological controls, and conducting ongoing monitoring through Morningstar's Compliance department. Morningstar will clearly identify manager research related to such indexes on the front page of the report. Morningstar does not provide qualitative ratings or opinions for investments managed by Morningstar or managed investments that track Morningstar indexes that incorporate discretionary inputs assigned by Morningstar employees on an ongoing basis, such as Morningstar Economic Moat Ratings, or ESG Ratings.*

### Performance (Returns)
| Metric | [Fund A] | [Fund B] | [Fund C] | [Fund D] |
|---|---|---|---|---|
| Total Return 1 Mo | | | | |
| Total Return 3 Mo | | | | |
| Total Return 6 Mo | | | | |
| Total Return 1 Yr | | | | |
| Total Return 3 Yr | | | | |
| Total Return 5 Yr | | | | |
| Total Return 10 Yr | | | | |

### Category Rankings
| Metric | [Fund A] | [Fund B] | [Fund C] | [Fund D] |
|---|---|---|---|---|
| Cat Rank 1 Mo | | | | |
| Cat Rank 3 Mo | | | | |
| Cat Rank 6 Mo | | | | |
| Cat Rank 1 Yr | | | | |
| Cat Rank 3 Yr | | | | |
| Cat Rank 5 Yr | | | | |
| Cat Rank 10 Yr | | | | |
*Category rank is percentile within Morningstar Category. Lower = better.*
### Risk Metrics (Mo-End)
| Metric | [Fund A] | [Fund B] | [Fund C] | [Fund D] |
|---|---|---|---|---|
| Portfolio Risk Score | | | | |
| Std Dev 1 Yr | | | | |
| Std Dev 3 Yr | | | | |
| Std Dev 5 Yr | | | | |
| Sharpe Ratio 1 Yr | | | | |
| Sharpe Ratio 3 Yr | | | | |
| Sharpe Ratio 5 Yr | | | | |
### Calendar-Year Returns
| Metric | [Fund A] | [Fund B] | [Fund C] | [Fund D] |
|---|---|---|---|---|
| Return YYYY | | | | |
| Cat Rank YYYY | | | | |
| Return YYYY-1 | | | | |
| Cat Rank YYYY-1 | | | | |
| Return YYYY-2 | | | | |
| Cat Rank YYYY-2 | | | | |
| Return YYYY-3 | | | | |
| Cat Rank YYYY-3 | | | | |
| Return YYYY-4 | | | | |
| Cat Rank YYYY-4 | | | | |
Replace YYYY with actual calendar year labels from Morningstar datapoint names.
### Holdings Overlap *(equity funds only)*
Only include rows for securities that appear in 2 or more funds. Do not add rows for holdings that appear in only one fund.
| Holding | [Fund A] Wt% | [Fund B] Wt% | [Fund C] Wt% | [Fund D] Wt% |
|---|---|---|---|---|
If no overlap exists, omit the table entirely and state: "No overlapping holdings found in the top 10 of each fund."
Omit this section entirely if the broad group is not Equity.
---
## Datapoints Reference (morningstar-data-tool)
| Group | Datapoint Name | Morningstar ID |
|---|---|---|
| Metadata | Morningstar Medalist Rating | MMR01 |
| Metadata | Morningstar Medalist Rating Disclosures Type | CNAXS |
| Metadata | Morningstar Rating Overall | |
| Metadata | Morningstar Category | OF003 |
| Metadata | Net Expense Ratio | OS00M |
| Metadata | Total Net Assets | OS006 |
| Metadata | Inception Date | OS00F |
| Metadata | Fund Status | OS999 |
| Performance | Total Ret 1 Mo (mo-end) | |
| Performance | Total Ret 3 Mo (mo-end) | |
| Performance | Total Ret 6 Mo (mo-end) | |
| Performance | 1 Year Total Return | PM00C |
| Performance | 3 Year Total Return Annualized | PM00E |
| Performance | 5 Year Total Return Annualized | PM00G |
| Performance | 10 Year Total Return Annualized | PM00I |
| Performance | Annual Ret {year} | AR002 |
| Performance | Annual Ret {year-1} | AR003 |
| Performance | Annual Ret {year-2} | AR004 |
| Performance | Annual Ret {year-3} | AR005 |
| Performance | Annual Ret {year-4} | AR006 |
| Category Rankings | 1 Month % Rank in Category | PM005 |
| Category Rankings | 3 Month % Rank in Category | PM007 |
| Category Rankings | 6 Month % Rank in Category | PM009 |
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
| Fund Context | Morningstar Category Broad Group | OF035 |
| Fund Context | Actively Managed | OF00D |
| Fund Context | Index Fund | OF00C |
| Fund Context | Enhanced Index | OF005 |
| Fund Context | Primary Prospectus Benchmark | OF00L |
| Fund Context | Morningstar Category Index | OS38B |