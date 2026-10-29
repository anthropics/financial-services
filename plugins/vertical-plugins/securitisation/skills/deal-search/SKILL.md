---
name: deal-search
description: >-
  Find SEC-registered securitisation deals on EDGAR and retrieve their filings using the
  securitisation EDGAR connector. Covers EDGAR's data model (one CIK per trust), the ABS
  filing lifecycle and form-type glossary, asset-class search strategy, and the honest
  limits of free EDGAR coverage. Use when locating an ABS, CMBS, or auto deal, pulling a
  deal's prospectus or investor reports, or finding the latest loan-level tape for a
  shelf. Not for CLOs or 144A private deals (not on EDGAR — use clo-indenture-review on a
  supplied document), or market pricing and spreads (not on EDGAR).
---

# Securitisation Deal Search (SEC EDGAR)

> EDGAR access in this skill uses the bundled `securitisation-edgar` connector. If its tools are missing or erroring, see [CONNECTOR.md](../../CONNECTOR.md) — do not substitute web search for filings.

## How EDGAR organises securitisations
Each securitisation **trust is its own EDGAR filer** with its own **CIK** (Central
Index Key). A shelf programme (e.g. an issuer's auto receivables trusts) appears as a
series of separate trusts, one per deal (…2017-1, 2017-2, …). Deals carry SIC code
**6189 — Asset-Backed Securities**.

## The ABS filing lifecycle (form glossary)
| Form | What it is | Use it for |
|---|---|---|
| **424H** | Preliminary prospectus | Early structure / marketing terms |
| **FWP** | Free-writing prospectus | Ratings & structural term sheet |
| **424B2 / 424B5** | Final prospectus | Definitive capital structure, CE, collateral, waterfall |
| **8-K** | Closing / material events | Deal establishment, closing documents |
| **ABS-EE** | Asset-level data (EX-102 XML) | **Loan-level tape** (auto/CMBS/RMBS/debt) |
| **10-D** | Distribution report | **Monthly** servicer/investor report, pool & note activity |
| **10-K** | Annual report | Annual servicer compliance / attestations |
| **15-15D** | Suspension of reporting | Deal wind-down / termination |

A live deal typically files: 424H → FWP → 424B → 8-K → **monthly 10-D + ABS-EE** →
annual 10-K → 15-15D at the end.

## Search technique (tools)
1. **`search_securitisation_deals`** queries EDGAR full-text search:
   - `query`: issuer or shelf text ("AmeriCredit", "GMCAR", "BMARK", "Verizon").
   - `asset_class`: helper that injects the right phrase — `auto`, `cmbs`, `rmbs`,
     `credit card`, `clo`.
   - `form_type`: narrow to a filing, e.g. `424B5,424H` (prospectus), `10-D`
     (investor reports), `ABS-EE` (loan-level).
   - `date_from` / `date_to`: bound the filing date.
2. **`get_deal_filings`** (with the deal's **CIK**) lists the full lifecycle; filter
   with `form_type` to grab just the prospectus or the latest tape.

## Asset-class coverage (be honest about this)

Rights, processing, and the full coverage rationale: [DATA_PROVENANCE.md](../../DATA_PROVENANCE.md).

| Asset class | Find deals? | Documents (424B/10-D)? | Loan-level (ABS-EE)? |
|---|---|---|---|
| Auto loan / lease | ✅ | ✅ | ✅ strong |
| Conduit CMBS | ✅ | ✅ | ✅ strong |
| Credit-card ABS | ✅ | ✅ | ❌ none (excluded by rule) |
| Registered RMBS | ⚠️ rare | ⚠️ rare | ❌ effectively absent |
| CLO (144A) | ❌ | ❌ | ❌ not on EDGAR |

## Output
Return a concise table — issuer, CIK, form, filing date, report period, document
link — and propose the next action (`/parse-abs-prospectus`, `/analyze-loan-tape`,
`/extract-waterfall`). Always include the EDGAR document URL so the user can verify.
Never invent a CIK or accession — if a search returns nothing, say so and suggest a
broader query.
