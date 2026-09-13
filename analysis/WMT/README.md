# Walmart Inc. — Competitive Analysis

Investment-decision-oriented competitive analysis for Walmart (NYSE: WMT),
produced using the `competitive-analysis` and `comps-analysis` skills in this
repo at `plugins/vertical-plugins/financial-analysis/skills/`.

Mirrors the methodology and shape of `analysis/MP/`.

## Files

| File | Built by | What it is |
|---|---|---|
| **`WMT-Competitive-Analysis.pptx`** | `build_deck.py` | 18-slide deck: thesis → market → industry → peer deep dives → comparative scoreboard → moats → bull/base/bear → catalysts → decision frame |
| **`WMT-Comps-Analysis.xlsx`** | `build_comps.py` | 5-tab peer comp workbook: Inputs · Operating Metrics · Valuation · Retail-Specific (comp sales, e-com mix, ads, membership) · Notes |
| **`WMT-Competitive-Analysis.html`** | `build_html_view.py` | Tablet-friendly single-file HTML view of the same 18 sections (charts embedded as base64) |
| `build_deck.py` / `build_comps.py` / `build_html_view.py` | — | Reproducible build scripts. Edit the `INPUTS` dict / slide content and re-run to refresh. |
| `charts/` | matplotlib | Intermediate PNGs embedded in the PPTX and HTML (peer comp-sales bars, 2×2 positioning matrix). |

## Peer set (6 names, per `comps-analysis` 4–6 rule)

| Tier | Ticker | Role |
|---|---|---|
| Mass-merch / general | NYSE: WMT | Target |
| Warehouse club premium | Nasdaq: COST | Closest peer — premium-valued membership economics (Lynas-analog deep dive) |
| Mass-merch / general | NYSE: TGT | Direct US discount/big-box overlap |
| Marketplace / digital | Nasdaq: AMZN | Omnichannel + ads template, AWS-distorted multiples |
| Pure-play grocery | NYSE: KR | Largest US pure-play grocer |
| Warehouse club | NYSE: BJ | Smaller-scale COST follower |

## Methodology notes

- **Skill workflow**: Phase 1 scope confirmed via `ask_user_question` (use-case
  = investment decision, peer set confirmed, depth = "deep WMT+COST, lighter
  others"), Phase 2 outline approved, then build. See the `competitive-analysis`
  SKILL.md for the canonical method.
- **Comps philosophy**: blue = hardcoded input (every cell has a comment citing
  source/assumption), black = formula, statistics block (Max/75/Median/25/Min)
  on every comparable column.
- **Industry-specific lens**: standard EV/EBITDA is reasonably comparable here,
  but headline AMZN multiples are AWS-distorted. The Retail-Specific tab adds
  **comp sales growth, e-com %, ad revenue $, and membership revenue $** —
  the columns that actually differentiate the peer set.
- **Date**: As of May 2026. Re-run build scripts after refreshing `INPUTS`.

## Data sources & gaps

**Used**: SEC EDGAR (Q1 FY26 10-Q and FY25 10-K for each issuer); WMT, COST,
TGT, AMZN, KR, BJ investor relations releases; StockAnalysis.com / Yahoo
Finance for market data; eMarketer / IAB for US retail-media TAM; Bain,
KeyBanc retail primers; press coverage (CNBC, Bloomberg).

**Not used** (and why):
- **MCP terminal connectors** (CapIQ / FactSet / Daloopa / LSEG via the
  `financial-analysis` plugin's `.mcp.json`) were not configured in this
  environment. Where the skill prescribes MCP-first data, public sources were
  substituted and flagged with `[E]` in cell comments.
- **Walmart Connect ad-business revenue** is NOT separately disclosed in WMT
  filings — the ~$5B run-rate is aggregated from mgmt commentary across recent
  earnings calls and interviews. Cell comment documents the assumption.

## Reproducing / refreshing

```bash
cd analysis/WMT
pip install openpyxl python-pptx matplotlib
python3 build_comps.py        # → WMT-Comps-Analysis.xlsx
python3 build_deck.py         # → WMT-Competitive-Analysis.pptx + charts/*.png
python3 build_html_view.py    # → WMT-Competitive-Analysis.html
```

## Caveats

- Research and decision framing only — **not investment advice**.
- Cross-check valuation against a primary terminal before any binding decision.
- `[E]` estimates are clearly marked in the Excel cell comments; review before
  use.
- AMZN consolidated multiples include AWS — they materially distort a
  "retail-only" comparison. Segment-level disaggregation not performed here.
- Operating-lease liabilities are excluded from Net Debt (material for AMZN,
  ~$80B+; modest for others).
