---
name: wacc-builder
description: |
  Build a defensible, fully auditable weighted-average cost of capital (WACC) — the single reusable discount-rate step that feeds DCF, LBO, and comparable-company valuations. Unlevers and relevers peer betas, derives cost of equity via CAPM and after-tax cost of debt on market-value weights, and outputs a transparent cost-of-capital worksheet ready to hand to the dcf-model, lbo-model, or comps-analysis skills.

  **Perfect for:**
  - Deriving a discount rate before running a DCF, LBO, or terminal-value calculation
  - Building a peer-beta (unlever → relever) cost of equity for a company whose own beta is noisy, newly listed, or capital-structure-distorted
  - Producing a standalone, reviewable cost-of-capital worksheet that multiple models can share
  - Re-computing WACC under a target (rather than current) capital structure for LBO or recap scenarios
  - Documenting every discount-rate assumption for investment-committee or audit review

  **Not ideal for:**
  - Setting a hurdle rate by fiat (use this to derive one, not to rubber-stamp a mandated number)
  - Pre-revenue or deeply distressed names where CAPM/peer-beta assumptions break down (flag and use scenario ranges instead)
  - Businesses valued on an equity-only basis (e.g. banks/insurers via cost of equity or excess-returns models) — use cost of equity directly, not WACC
  - Making an investment recommendation — this produces a discount rate, staged for human review, not a buy/sell call
---

# WACC Builder

## ⚠️ CRITICAL: Data Source Priority (READ FIRST)

**ALWAYS follow this data source hierarchy for market inputs (beta, risk-free rate, credit spreads, peer capital structures):**

1. **FIRST: Check for MCP data sources** — if S&P Kensho, FactSet, Daloopa, Morningstar, or LSEG MCP servers are available, use them exclusively for betas, yields, share prices, debt balances, and peer data.
2. **DO NOT use web search** if the above MCP data sources are available.
3. **ONLY if MCPs are unavailable:** use Bloomberg Terminal, SEC EDGAR filings, or other institutional sources.
4. **NEVER use web search as a primary source** for market data — it lacks the accuracy, audit trails, and point-in-time reliability required for institutional-grade analysis. Web fetch is acceptable only as a last-resort sanity check on a single current price or yield, and must be labelled as such in the worksheet.

**Why this matters:** a WACC is only as defensible as its inputs. Every figure in the worksheet must carry a source and an as-of date so a reviewer can reproduce it.

---

## Overview

This skill derives a weighted-average cost of capital that is transparent, reproducible, and portable across models. WACC is the rate that blends the after-tax cost of debt and the cost of equity by their market-value weights:

```
WACC = wₑ · rₑ + w_d · r_d · (1 − t)     [+ w_p · r_p  if preferred stock exists]
```

The value-add of a **standalone** WACC step (versus computing it inline inside a single model) is reuse and auditability: the same defensible discount rate can feed a `dcf-model`, an `lbo-model`, or the implied-return check in a `comps-analysis`, and the derivation lives in one reviewable worksheet rather than being buried in a spreadsheet tab.

## When to Use This Skill (and how it relates to the other skills)

- Invoke **before** `dcf-model` or `lbo-model` when a discount rate is needed and no vetted WACC exists yet. Hand the resulting rate (and the assumptions table) to that skill.
- `dcf-model` contains an inline WACC step for the common case; use `wacc-builder` when you want a **rigorous peer-beta derivation**, a **target-structure** WACC, or a **shared** rate across several models.
- The output is decision-support: it produces a rate and a documented rationale. It does not select the "right" number for you — where judgement is required (peer set, target leverage, premia), it surfaces the choice explicitly.

## Data & Inputs to Gather

Collect and cite each of the following (mark any value you had to assume rather than source):

- Company name and **valuation date** (all market inputs must be as-of this date).
- **Capital structure at market value:** market cap (E), total debt (D), and preferred stock (P) if any. Use market values, not book — except debt, where book is an acceptable proxy for market when the company is not distressed.
- **Risk-free rate (r_f):** government bond yield matched to the cash-flow horizon (typically the 10Y). State the tenor.
- **Equity beta:** the company's own levered beta, and/or a set of comparable-company betas for a peer-beta build.
- **Equity/market risk premium (ERP):** state the source and geography.
- **Pre-tax cost of debt (r_d):** from the company's marginal borrowing cost — YTM on traded debt, or risk-free + a credit spread implied by rating.
- **Marginal tax rate (t):** the go-forward statutory + local rate, not the reported effective rate, unless you justify otherwise.
- **Optional premia:** size premium and/or country-risk premium, when the peer set or geography warrants — always shown as separate, labelled line items.

## Methodology

### Step 1 — Peer beta (unlever → relever)
Use this when the company's own beta is unreliable. For each comparable, unlever its equity beta to remove the effect of its capital structure (Hamada, assuming debt beta ≈ 0):

```
βᵤ = β_L / (1 + (1 − t) · (D/E))
```

Take the **median** unlevered beta of the peer set (median is more robust to outliers than mean), then relever to the subject company's target structure:

```
β_L = βᵤ · (1 + (1 − t) · (D/E)_target)
```

If the company's own beta is clean and its structure stable, you may use it directly — but state that choice.

### Step 2 — Cost of equity (CAPM)
```
rₑ = r_f + β_L · ERP   [+ size premium]  [+ country-risk premium]
```
List each premium as its own line so the build is auditable.

### Step 3 — After-tax cost of debt
```
r_d(after-tax) = r_d · (1 − t)
```
For a company with **no debt**, WACC collapses to the cost of equity (skip Steps 3–4's debt terms).

### Step 4 — Market-value weights
```
wₑ = E / (E + D + P)      w_d = D / (E + D + P)      w_p = P / (E + D + P)
```
Decide **current vs. target** structure deliberately: use the target for LBO/recap analyses, the current for a steady-state DCF, and say which.

### Step 5 — Assemble WACC
```
WACC = wₑ · rₑ + w_d · r_d(after-tax)  [+ w_p · r_p]
```

### Step 6 — Sanity band
Report the point estimate plus a **±0.5% band** (or a small grid over beta and ERP) so downstream sensitivity analysis has a defensible range, not a single false-precision number.

## Correct Patterns

- **Everything is sourced.** Every input line carries a source and an as-of date; assumed values are flagged as assumptions.
- **Median peer beta**, unlevered with each peer's own D/E and tax rate, then relevered once to the subject's structure.
- **Market-value weights**, matched to the chosen (current or target) capital structure.
- **Marginal tax rate**, applied consistently in both the beta relevering and the after-tax cost of debt.
- **A single blended rate handed off** with its full assumptions table, so `dcf-model`/`lbo-model` consume the derivation, not just the number.

## Common Mistakes (avoid these)

- Using **book** equity weights instead of **market** weights.
- Using the reported **effective** tax rate where the **marginal** rate is appropriate (or mixing the two between relevering and cost of debt).
- Applying the **levered** peer beta directly without unlevering/relevering to the subject's structure.
- Forgetting **Terminal Growth < WACC** must hold downstream — flag it for the DCF step (this skill provides the rate; `dcf-model` enforces the constraint).
- Mixing tenors — pairing a 10Y risk-free rate with a short-horizon ERP, or vice-versa.
- Treating a mandated hurdle rate as a derived WACC without saying so.
- False precision — reporting WACC to two decimals with no sensitivity band.

## Output / Deliverable

Produce a **Cost of Capital worksheet** containing:

1. **Assumptions table** — every input with its value, source, and as-of date.
2. **Beta build** — each peer's levered beta, D/E, tax rate and unlevered beta; the median; and the relevered subject beta.
3. **Component build** — cost of equity (with each premium as a line), after-tax cost of debt, and the market-value weights.
4. **Result** — the WACC point estimate, rounded, plus the ±0.5% band (or a small beta × ERP grid).
5. **Handoff note** — one line: "Discount rate ready for dcf-model / lbo-model."

When a spreadsheet deliverable is requested, hand the structured worksheet to the **`xlsx-author`** skill for Excel output (formulas over hardcodes, one input block, cell comments citing sources) rather than emitting a static table — this keeps the WACC live and links cleanly into a downstream model's WACC sheet.

## Workflow Integration

- **→ dcf-model / lbo-model:** pass the WACC and its assumptions table as the discount rate.
- **→ comps-analysis:** use the derived cost of equity/WACC as the implied-return cross-check on trading multiples.
- **→ xlsx-author:** render the worksheet as a live Excel WACC sheet on request.

## Guardrails

- This skill produces **decision-support**, not investment advice. It derives a discount rate; it does not recommend buying, selling, or transacting, and it does not bind risk or approve anything.
- **Every output is staged for human sign-off.** State all assumptions explicitly and flag any input that was assumed rather than sourced.
- Do not fabricate market data. If a required input (beta, yield, peer set) is unavailable from an authorised source, say so and present the WACC as a labelled range under stated assumptions rather than inventing a point value.
