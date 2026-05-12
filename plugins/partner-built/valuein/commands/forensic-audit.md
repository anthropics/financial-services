---
description: Earnings-quality red-flag brief — Beneish M-Score, Sloan accruals, solvency snapshot, and restatement history for a single US ticker
argument-hint: "<ticker e.g. ENRN> [include_amendments=true|false]"
---

# Forensic Audit

> This command uses Valuein's `forensic_audit`, fundamentals, filings, and capital-allocation tools. See [CONNECTORS.md](../CONNECTORS.md) for the complete tool reference.

Generate a forensic earnings-quality brief for a single US ticker. Surfaces partial Beneish M-Score components, Sloan accruals, three-ratio solvency snapshot, and the recent amendment history (10-K/A, 10-Q/A) — every red flag cites a specific SEC accession.

This command is opinionated about how a forensic analyst reads the output: it never claims "manipulation" without empirical thresholds, and it always pairs a flag with the underlying ratio and the originating filing.

See the **forensic-audit** skill for domain knowledge on Beneish interpretation, Sloan accruals, and restatement materiality.

## Workflow

### 1. Gather Input

Ask the user for:
- Ticker symbol (required).
- Whether to include amendments (optional, default true) — restatements are the strongest signal but inflate the output for clean names.

### 2. Forensic Score Baseline

Call `forensic_audit` with `ticker`. Returns:
- `m_score` (partial Beneish) with components `sgi` (sales growth index), `tata` (total accruals / total assets), `lvgi` (leverage growth index)
- `sloan_accruals` (net income − operating cash flow) / total assets
- `solvency` with `debt_to_equity`, `debt_to_assets`, `roa`
- `red_flags` ranked by severity
- `source_filing` and `sec_url` for the current period

Preserve the `partial: true` flag in the output — full Beneish (8 factors) needs AR / current assets / PPE / SGA / current liabilities that the standardised fundamentals model doesn't carry. Communicate the caveat clearly to the user.

### 3. Multi-Period Fundamentals Trend

Call `get_company_fundamentals` with `ticker`, `period: "annual"` and the last 5 fiscal years.

Compute growth-vs-margin divergence: revenue rising while gross margin falling (and accruals positive) is the classic earnings-quality risk pattern.

### 4. Filing History (Amendments)

If `include_amendments=true`, call `get_sec_filing_links` with `ticker`, `formTypes: ["10-K/A", "10-Q/A", "20-F/A", "40-F/A"]`.

Each amendment is a restatement candidate. Note the filing date and SEC URL — agents should NOT speculate about content without verifying the amendment text.

### 5. Capital-Allocation Cross-Check

Call `get_capital_allocation_profile` with `ticker`. The boolean flags `buybacks_exceed_fcf` and `debt_funded_distribution` are independent earnings-quality signals — companies funding returns with debt while accruals rise are at the higher end of the manipulation-risk distribution.

### 6. Synthesize the Brief

Combine into the output below.

## Output Format

### Forensic Brief — \<TICKER\>

**⚠️ Note on Beneish**: Valuein computes a partial M-Score from the components recoverable in standardised fundamentals (SGI + TATA + LVGI). Full Beneish (8 factors) needs balance-sheet line items that aren't in the model. Use the partial score as a directional signal, not a verdict.

### Red Flags (Most Severe First)

For each red flag returned by `forensic_audit`:
- **Flag name** (e.g. "Partial M-Score exceeds -2.22 threshold")
- One-sentence what & why (cite empirical threshold)
- Source: `[Accession ID]` → `source_url`

### Quantitative Scorecard

| Metric | Value | Empirical Threshold | Status |
|--------|-------|---------------------|--------|
| Partial M-Score | ... | > -2.22 → concern | ✅/🚩 |
| Sloan Accruals | ...% | > 7.5% → concern | ✅/🚩 |
| Debt / Equity | ... | > 3.0 → high leverage | ✅/🚩 |
| Debt / Assets | ... | > 0.6 → high leverage | ✅/🚩 |
| ROA | ...% | < 0 → unprofitable | ✅/🚩 |
| Leverage Growth Index | ... | > 1.10 → debt growing > assets | ✅/🚩 |

### Restatement History

If amendments were requested:
| Date | Form | Accession | EDGAR Link |
|------|------|-----------|------------|
| YYYY-MM-DD | 10-K/A | ... | source_url |
| ... | ... | ... | ... |

For each amendment, note that the agent should verify the amendment text against the original 10-K / 10-Q to confirm material change.

### Capital-Allocation Cross-Check

| Signal | Latest Period | Interpretation |
|--------|---------------|-----------------|
| Buybacks exceed FCF | true / false | Companies funding returns above FCF often borrow; check the debt flag. |
| Debt-funded distributions | true / false | Strongest earnings-quality red flag when combined with positive accruals. |
| Net debt change | $... | Direction matters — increases during high-accruals period = elevated risk. |

### Bottom Line (3 sentences)

State the empirical evidence for / against earnings-quality concerns. Do NOT use language like "fraud", "manipulation", or "cooking the books" — describe what the data shows and let the user reach a conclusion. Close with the recommendation: continue diligence, deeper forensic review needed, or no obvious red flags.

### Sources

Always close with the cited accession list: `[Accession ID]: <source_url>` for every fact_id used above.
