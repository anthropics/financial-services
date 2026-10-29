---
name: ddm-model
description: |
  Build institutional-grade Dividend Discount Model (DDM) valuations — the income-approach complement to the dcf-model and comps-analysis skills. Projects a company's expected dividend stream, discounts it at the cost of equity (CAPM), and outputs a professional Excel model with single-stage (Gordon), two-stage, and multi-stage (H-model) options, sensitivity analysis, and an intrinsic equity value per share. Use when valuing dividend-paying equities — banks, insurers, REITs, utilities, and mature high-payout companies — where free-cash-flow DCF is unreliable or dividends are the cleanest measure of cash returned to shareholders.

  **Perfect for:**
  - Valuing banks, insurers, and other financials where unlevered free cash flow is ill-defined
  - Mature, stable dividend payers (utilities, consumer staples, telecoms)
  - REITs and income vehicles valued on their distributions
  - An income-based cross-check on a DCF or trading-comps valuation
  - Backing out the dividend growth the market is pricing into a stock (implied-growth check)

  **Not ideal for:**
  - Non-dividend-paying or early-stage growth companies (use dcf-model / comps-analysis)
  - Companies whose payout is erratic or funded by debt rather than earnings
  - Situations that need enterprise value (DDM yields equity value per share directly)
  - Making an investment recommendation — this produces an intrinsic value per share, staged for human review
---

# Dividend Discount Model (DDM) Builder

## Overview

This skill builds institutional-quality DDM valuations for dividend-paying equities. The DDM values equity **directly** as the present value of expected future dividends, discounted at the **cost of equity** — there is no WACC and no enterprise-value-to-equity bridge. Each analysis produces a detailed Excel model (a `DDM` sheet plus a `Sensitivity` sheet) and an intrinsic value per share.

The deep methodology — single-, two-, and three-stage math, the H-model, the ROE-driven build for financials, and how to reconcile DDM with DCF and comps — lives in [references/methodology.md](references/methodology.md). **Read it before building a multi-stage or a bank/insurer model.**

## ⚠️ CRITICAL: Data Source Priority (READ FIRST)

**ALWAYS follow this data source hierarchy for financial and market inputs (dividend history, payout, EPS, book value, beta, risk-free rate):**

1. **FIRST: Check for MCP data sources** — if S&P Kensho, FactSet, Daloopa, Morningstar, or LSEG MCP servers are available, use them exclusively.
2. **DO NOT use web search** if the above MCP data sources are available.
3. **ONLY if MCPs are unavailable:** use Bloomberg Terminal, SEC EDGAR filings, or other institutional sources.
4. **NEVER use web search as a primary data source** — it lacks the accuracy, audit trails, and point-in-time reliability required for institutional-grade analysis.

**Why this matters:** a valuation is only as defensible as its inputs. Every hardcoded figure in the model must carry a source and an as-of date so a reviewer can reproduce it.

## When to Use This Skill (and how it differs from dcf-model)

- **DDM discounts dividends at the cost of equity and yields equity value per share directly** — no WACC, no unlevered free cash flow, no net-debt bridge.
- Prefer DDM over `dcf-model` when free cash flow is unreliable or undefined (**banks, insurers**), or when dividends are the primary form of return (**utilities, REITs, mature payers**).
- **It complements the other valuation skills.** Run it alongside `dcf-model` and `comps-analysis` and reconcile the outputs into a valuation range (see [references/methodology.md](references/methodology.md) → *Reconciliation*).
- The discount rate is the **cost of equity** from CAPM (`rₑ = r_f + β · ERP`) — a DDM never uses WACC, so there is no debt cost and no market-value weighting. The `dcf-model` skill derives the same CAPM cost of equity in its WACC step; reuse that build for the cost-of-equity portion only.

## Tools

- Default to using the data provided by the user and the MCP servers available for sourcing dividends, payout history, EPS, book value, beta, and yields.

## Critical Constraints — Read These First

These apply throughout. Review before starting.

**Environment: Office JS vs Python/openpyxl:**
- **Inside Excel (Office Add-in / Office JS):** write formulas via `range.formulas = [[...]]`; do NOT use Python/openpyxl. Excel recalculates natively.
- **Generating a standalone .xlsx (no live Excel):** use Python/openpyxl, then run `recalc.py` (from the `xlsx-author` skill) before delivery.
- All principles below (formula strings, cell comments, section checkpoints, sensitivity loops) apply identically in both environments.

**Discount at the COST OF EQUITY, not WACC (the #1 DDM error):**
- Dividends are cash flows to equity holders, so they are discounted at the cost of equity `rₑ = r_f + β · ERP`. Using WACC understates the discount rate and overstates value. This is the single most common DDM mistake — do not make it.

**`r > g` is mandatory:**
- The Gordon terminal value `D / (rₑ − g)` is only valid when the cost of equity exceeds the perpetual growth rate. If `g ≥ rₑ` the value is infinite or negative and the model is invalid. Enforce `g < rₑ` and keep `g` at or below long-run nominal GDP growth (preferred 2–4%; the bundled validator flags any `g` above 5%).

**Formulas Over Hardcodes (NON-NEGOTIABLE):**
- Every projected dividend, discount factor, present value, terminal value, and sensitivity cell MUST be a live Excel formula — never a number computed off-sheet and pasted in.
- The only permitted hardcodes are: (1) raw historical inputs (DPS, EPS, book value), (2) assumption drivers (growth rates, payout, cost-of-equity inputs, terminal `g`), (3) current market data (share price, shares outstanding).
- If you catch yourself computing a value off-sheet and writing the result — STOP. The model must flex when the user changes an assumption.

**Verify Step-by-Step With the User (do NOT build end-to-end):**
- After data retrieval → show the dividend history, payout trend, and cost-of-equity inputs; confirm before projecting.
- After the dividend projection → show the explicit-period DPS and growth; confirm before the terminal value.
- After the terminal value + PV → show the per-share bridge; confirm before sensitivity tables.
- Catch errors at each stage — a wrong growth or payout assumption found after the sensitivity tables are built means rebuilding everything downstream.

**Sensitivity Tables:**
- Use an **odd** number of rows and columns (standard 5×5) so there is a true center cell.
- **Center cell = base case:** build the axes so the middle row/column headers equal the model's actual cost of equity and terminal growth; the center cell's output must then equal the model's headline value per share — this is the sanity check.
- Highlight the center cell (medium-blue fill `#BDD7EE`, bold).
- Populate every cell with a full DDM recalculation formula (no placeholders, no linear approximations).
- Primary table: **cost of equity × terminal growth.** Consider a second table on the high-growth rate × high-growth period.

**Cell Comments:** add a `Source: [System/Document], [Date], [Reference], [URL if applicable]` comment as each hardcoded input is created — include a hyperlink to the filing or data source when available; do not defer to the end.

**Model Layout Planning:** define all section row positions, write all headers/labels, then write formulas against the locked positions.

**Validate Before Delivery:** run `python scripts/validate_ddm.py model.xlsx` (and, for standalone openpyxl builds, `recalc.py` from the `xlsx-author` skill). Zero formula errors required. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

**Scenario Blocks:** build separate Bear/Base/Bull assumption blocks. For auditability, prefer a single consolidation column that selects the active case with `=INDEX([Bear:Bull cells],1,$B$6)` (or `OFFSET`) over scattered nested `=IF($B$6=1,[Bear],IF($B$6=2,[Base],[Bull]))` formulas, mirroring dcf-model's case-selector pattern.

## DDM Process Workflow

### Step 1: Data Retrieval and Validation
Gather 5+ years of dividend history (DPS), payout ratio, EPS, and — for financials — book value per share and ROE, plus beta, the risk-free rate, and the equity risk premium.
- Confirm dividends are actually paid and covered by earnings (payout < 100%) and/or free cash flow.
- Confirm diluted shares outstanding (check recent buybacks/issuances).
- Sanity-check beta and the payout trend against history.

### Step 2: Dividend & Payout Analysis
Document historical DPS growth, the payout-ratio trend, and sustainability. For **financials**, derive the sustainable growth rate `g = ROE × retention ratio` (retention = 1 − payout) — see [references/methodology.md](references/methodology.md) → *DDM for financials*.

### Step 3: Select the Model
Choose single-stage, two-stage, or three-stage / H-model per the guide below and the detailed criteria in the methodology reference.

### Step 4: Cost of Equity (CAPM)
`rₑ = r_f + β · ERP` (add a size or country-risk premium only if warranted, as separate labelled lines). This is the discount rate for the entire model. **Do not use WACC.**

### Step 5: Project Dividends
Build the explicit-period DPS, either directly via a growth rate or as `payout × projected EPS`. Show both dollar amounts and the implied growth %.

### Step 6: Terminal Value
Gordon continuation at the end of the explicit period: `TVₙ = Dₙ₊₁ / (rₑ − g) = Dₙ(1 + g) / (rₑ − g)`. Enforce `g < rₑ`.

### Step 7: Discount to Present Value
`V₀ = Σₜ Dₜ / (1 + rₑ)ᵗ + TVₙ / (1 + rₑ)ⁿ`. The result is the intrinsic **equity value per share** — compare it directly to the current share price.

### Step 8: Sensitivity Analysis
Build the cost-of-equity × terminal-growth table (and optionally high-growth rate × period) per the constraints above.

### Step 9 (Financials): ROE-Driven Build
For banks/insurers, project dividends from `EPS = ROE × book value per share` and `DPS = EPS × payout`, with `g = ROE × retention`. See the methodology reference.

## Model Selection Guide

| Model | Use when | Key inputs |
|---|---|---|
| **Single-stage (Gordon)** | Mature company already at a stable, perpetual growth rate | `D₁`, `rₑ`, `g` |
| **Two-stage** | A defined high-growth period, then an abrupt step to stable growth | high-growth rate & years, then `g`, `rₑ` |
| **Three-stage / H-model** | Growth fades gradually from high to mature | initial & long-run growth, fade period, `rₑ` |

## Correct Patterns
- **Discount at the cost of equity**, applied consistently to the explicit dividends and the terminal value.
- **`g < rₑ`** and terminal `g` at or below long-run nominal GDP growth.
- **Everything sourced:** every hardcoded input carries a source and an as-of date.
- **Value per share compared to the current price**, with a sensitivity band rather than a single false-precision figure.
- **Reconcile** the DDM value against a DCF and trading comps to form a defensible range.

## Common Mistakes
- **Discounting at WACC instead of the cost of equity** (overstates value).
- **`g ≥ rₑ`**, producing an infinite or negative Gordon value.
- **Terminal growth above long-run GDP** — indefensible in perpetuity.
- **Assuming a payout ratio > 100% in perpetuity** — dividends cannot exceed earnings forever.
- **Ignoring buybacks:** for companies that return most cash via repurchases, a dividend-only DDM understates value — use a total-payout variant (see methodology reference) or a different method.
- **Applying DDM to non-payers or erratic payers** — use `dcf-model` / `comps-analysis` instead.
- **Mixing nominal and real** rates and growth.

## Excel Model Structure
- **`DDM` sheet:** inputs block (dividend history, payout, market data) → cost-of-equity build (CAPM) → explicit dividend projection → terminal value → PV bridge and value per share.
- **`Sensitivity` sheet (or section):** the cost-of-equity × terminal-growth table with the highlighted center cell.
- Use the `xlsx-author` skill to render a standalone `.xlsx` when no live Excel session is available.

## Validation
Run the bundled validator before delivery:
```
python scripts/validate_ddm.py model.xlsx
```
It checks for formula errors, enforces `cost of equity > terminal growth`, and flags an out-of-range cost of equity, an aggressive terminal growth rate, a terminal value that dominates total value, and a payout ratio above 100%. Exit code `0` = PASS. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## Deliverables
- A live Excel DDM model (formulas throughout) with a sourced assumptions block.
- The intrinsic value per share plus a sensitivity band, compared to the current price.
- A short reconciliation note positioning the DDM value against the DCF/comps range.

## Workflow Integration
- **→ `dcf-model` / `comps-analysis`:** reconcile the DDM value into a blended valuation range; the CAPM cost-of-equity inputs are the same ones `dcf-model` derives in its WACC step (reuse the cost-of-equity portion only).
- **→ `xlsx-author`:** render the model as a standalone `.xlsx`.

## Guardrails
- This skill produces **decision-support**, not investment advice. It computes an intrinsic value per share; it does not recommend buying, selling, or transacting.
- **Every output is staged for human sign-off.** State all assumptions explicitly and flag any input that was assumed rather than sourced.
- Do not fabricate dividend, payout, or market data. If a required input is unavailable from an authorised source, say so and present the value as a labelled range under stated assumptions rather than inventing a point estimate.
