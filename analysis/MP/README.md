# MP Materials — Competitive Analysis

Investment-decision-oriented competitive analysis for MP Materials (NYSE: MP),
produced using the `competitive-analysis` and `comps-analysis` skills in this
repo at `plugins/vertical-plugins/financial-analysis/skills/`.

## Files

| File | Built by | What it is |
|---|---|---|
| **`MP-Competitive-Analysis.pptx`** | `build_deck.py` | 18-slide deck: thesis → market → industry → peer deep dives → comparative scoreboard → moats → bull/base/bear → catalysts → decision frame |
| **`MP-Comps-Analysis.xlsx`** | `build_comps.py` | 5-tab peer comp workbook: Inputs · Operating Metrics · Valuation · REE-Specific (capacity multiples) · Notes |
| `build_deck.py` / `build_comps.py` | — | Reproducible build scripts. Edit the `INPUTS` dict / slide content and re-run to refresh. |
| `charts/` | matplotlib | Intermediate PNGs embedded in the PPTX (NdPr price chart, 2×2 positioning matrix). |

## Peer set (6 names, per `comps-analysis` 4–6 rule)

| Tier | Ticker | Role |
|---|---|---|
| Western pure-play | NYSE: MP | Target |
| Western pure-play | ASX: LYC (Lynas) | Closest peer — only other scaled non-US Western producer |
| US junior | NYSE: UUUU (Energy Fuels) | Uranium + REE processing pivot |
| US junior | Nasdaq: USAR (USA Rare Earth) | Mine-to-magnet pure-play, $1.6B gov't backing |
| Chinese major (context) | SHA: 600111 (China Northern RE) | World's largest REE producer |
| Critical-minerals adjacent | NYSE: ALB (Albemarle) | Lithium reference |

## Methodology notes

- **Skill workflow**: Phase 1 scope (use-case = investment decision, peer set
  confirmed, depth = "deep MP+Lynas, lighter others"), Phase 2 outline approved,
  then build. See the `competitive-analysis` SKILL.md for the canonical method.
- **Comps philosophy**: blue = hardcoded input (every cell has a comment citing
  source/assumption), black = formula, statistics block (Max/75/Median/25/Min)
  on every comparable column.
- **Industry-specific lens**: standard EV/EBITDA is limited because most peers
  have negative or pre-scale EBITDA. The REE-Specific tab adds
  **EV per MT/yr NdPr capacity** — the cleaner cross-peer comparable.
- **Date**: As of May 2026. Re-run build scripts after refreshing `INPUTS`.

## Data sources & gaps

**Used**: SEC EDGAR (MP, USAR 10-Q FY2026 Q1); MP investor relations; Lynas
reporting centre; StockAnalysis.com; SMM; Discovery Alert; S&P Global
research note (Lynas 2026 outlook); Energy Fuels Phase 2 BFS; CNBC; Center
on Global Energy Policy.

**Not used** (and why):
- **MCP terminal connectors** (CapIQ / FactSet / Daloopa / LSEG via the
  `financial-analysis` plugin's `.mcp.json`) were not configured in this
  environment. Where the skill prescribes MCP-first data, public sources
  were substituted and flagged with `[E]` in cell comments.
- **Forward consensus from sell-side feeds** — public aggregator estimates used
  instead; variance may exist.

## Reproducing / refreshing

```bash
cd analysis/MP
pip install openpyxl python-pptx matplotlib
python3 build_comps.py   # → MP-Comps-Analysis.xlsx
python3 build_deck.py    # → MP-Competitive-Analysis.pptx + charts/*.png
```

## Caveats

- Research and decision framing only — **not investment advice**.
- Cross-check valuation against a primary terminal before any binding decision.
- `[E]` estimates are clearly marked in the Excel cell comments; review before
  use.
