---
name: sector-overview
description: Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".
---


## Data Source: IBKR (preferred when available)

For company snapshots in a sector overview, IBKR gives you the live
trading layer (price, mkt cap, dividend yield) faster than re-keying
from FactSet. When the `ibkr` MCP server is reachable (verify with
`ibkr_status`):

- **Per-name snapshot** — `ibkr_snapshot(symbols=[…])` (batch quote)
  for the 5-10 players in the universe. Returns last, day range, and
  volume in one call.
- **Per-name fundamentals** — `ibkr_fundamentals(symbol)` for P/E, mkt
  cap, div yield, margins — used in the Company Profiles table.
- **Dividend track record** — `ibkr_dividends(symbol, lookback_years=5)`
  for the "dividend payer / grower" line in each profile.
- **Universe scan** — `ibkr_market_scanner(scan_code="most_active_us")`
  with an `above_market_cap` filter to keep the universe on point.

For deeper fundamentals (segment revenue, FCF yield), layer Daloopa /
FactSet on top of the IBKR data — the two complement each other.

If `ibkr_status` reports the server is **not reachable**, fall back to
web search and SEC EDGAR for the same fields.
# Sector Overview

## Workflow

### Step 1: Define Scope

- **Sector / subsector**: What industry and how narrowly defined?
- **Purpose**: Client report, internal research, pitch material, idea generation
- **Depth**: High-level overview (5-10 pages) or deep dive (20-30 pages)
- **Angle**: Neutral landscape vs. thematic thesis (e.g., "AI infrastructure buildout")
- **Universe**: Public companies only, or include private?

### Step 2: Market Overview

**Market Size & Growth**
- Total addressable market (TAM) with source
- Historical growth rate (5-year CAGR)
- Forecast growth rate and key assumptions
- Market segmentation (by product, geography, end market, customer type)

**Industry Structure**
- Fragmented vs. consolidated — top 5 market share
- Value chain map — where does value accrue?
- Business model types (subscription, transaction, licensing, services)
- Barriers to entry (capital, regulatory, technical, network effects)

**Key Trends & Drivers**
- Secular tailwinds (3-5 major trends)
- Headwinds and risks
- Technology disruption vectors
- Regulatory developments
- M&A activity and consolidation trends

### Step 3: Competitive Landscape

**Company Profiles** (for top 5-10 players):

| Company | Revenue | Growth | EBITDA Margin | Market Share | Key Differentiator |
|---------|---------|--------|--------------|-------------|-------------------|
| | | | | | |

For each company, brief profile:
- Business description (2-3 sentences)
- Strategic positioning and moat
- Recent developments (earnings, M&A, product launches)
- Valuation snapshot (P/E, EV/EBITDA, EV/Revenue)

**Competitive Dynamics**
- How do companies compete? (price, product, service, distribution)
- Who is gaining/losing share and why?
- Disruption risk from new entrants or adjacent players

### Step 4: Valuation Context

- Sector trading multiples (current and historical range)
- Premium/discount drivers (growth, margins, market position)
- Recent M&A transaction multiples
- How does the sector compare to the broader market?

### Step 5: Investment Implications

- Where are the best risk/reward opportunities?
- What thematic bets can be expressed through this sector?
- Key debates in the sector (bull vs. bear arguments)
- Catalysts that could change the sector narrative

### Step 6: Output

- Word document or PowerPoint with:
  - Market overview and sizing
  - Competitive landscape map
  - Company comparison table
  - Valuation summary
  - Key charts: market growth, share trends, valuation history
- Excel appendix with detailed company data

## Important Notes

- Source all market size data — cite the research firm or methodology
- Distinguish between TAM hype and realistic addressable market
- Sector overviews age fast — note the date and flag data that may be stale
- Charts are essential — market size waterfall, competitive positioning matrix, valuation scatter plot
- If for a client, tailor the "so what" to their specific situation (M&A target identification, competitive positioning, market entry)
