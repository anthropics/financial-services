# DDM Model Troubleshooting Guide

**When to read this file:** if `scripts/validate_ddm.py` reports errors, OR the value per share seems unreasonable, OR the model behaves oddly when you switch scenarios.

## Validator Reports a Critical Error

### "terminal growth >= cost of equity"
- The Gordon term `D / (rₑ − g)` is infinite or negative. `g` must be strictly less than `rₑ`.
- Fix: lower the perpetual growth `g` (it should be at or below long-run nominal GDP, ~2–4%) or verify the cost-of-equity inputs (`r_f`, `β`, `ERP`).

### #REF! / #DIV/0! / #VALUE! errors
- `#REF!` — a formula points at a row that moved after headers were inserted. Lock all row positions before writing formulas; rebuild the broken references.
- `#DIV/0!` — usually `rₑ − g` evaluated to zero, or an empty cost-of-equity cell. Confirm the inputs are populated and `rₑ > g`.
- `#VALUE!` — a text value where a number is expected. Verify all inputs are numbers, not strings.

## Value per Share Seems Unreasonable

### Implied value far too high
- Check that you are discounting at the **cost of equity, not WACC** (WACC is lower, which inflates value).
- Check `rₑ − g` isn't razor-thin — a tiny spread explodes the terminal value.
- Verify the terminal value isn't >90% of total value (extend the explicit horizon if so).
- Confirm the payout ratio is sustainable (≤100%) and growth isn't above GDP.

### Implied value far too low
- Check the cost of equity isn't too high (beta or ERP overstated).
- Confirm dividends/payout reflect reality — if the company returns cash mainly via **buybacks**, switch to a total-payout DDM (see references/methodology.md §6); a dividend-only model will understate value.
- Verify the explicit-period growth isn't too conservative.

## Wrong Method for the Company
- **Non-payer or erratic payer:** the DDM is inappropriate — use `dcf-model` or `comps-analysis`.
- **Bank/insurer:** use the ROE-driven build (references/methodology.md §5); a plain growth-rate DDM ignores the ROE-vs-cost-of-equity spread that drives financial-sector value.

## Scenario Selector Not Working
- Verify the case selector cell contains 1, 2, or 3.
- Check the `IF` formulas reference the correct Bear/Base/Bull block cells and use absolute references (`$B$6`) for the selector.
- Test by changing the selector manually and confirming the dividend projection and value per share update.
