# Individual Investor Guide: Using Financial Services Plugins for Stock Research

> **Important Disclaimer:** Nothing in this repository constitutes investment, legal, tax, or accounting advice. These tools draft analyst work product — models, memos, research notes — for review by a qualified professional. They do not make investment recommendations, execute transactions, or bind risk. Every output is staged for human sign-off. You are responsible for verifying outputs.

---

## Table of Contents

1. [Overview](#overview)
2. [Understanding the Repository Structure](#understanding-the-repository-structure)
3. [Quick Start: Key Commands](#quick-start-key-commands)
4. [Step-by-Step Investment Workflow](#step-by-step-investment-workflow)
   - [Step 1: Screen for Investment Opportunities](#step-1-screen-for-investment-opportunities)
   - [Step 2: Compare to Similar Companies](#step-2-compare-to-similar-companies)
   - [Step 3: Analyze Earnings and Financials](#step-3-analyze-earnings-and-financials)
   - [Step 4: Build a Valuation Model](#step-4-build-a-valuation-model)
   - [Step 5: Create Your Investment Thesis](#step-5-create-your-investment-thesis)
   - [Step 6: Track Your Thesis Over Time](#step-6-track-your-thesis-over-time)
5. [Detailed Command Reference](#detailed-command-reference)
6. [Example Workflows](#example-workflows)
7. [Understanding What Each Skill Does](#understanding-what-each-skill-does)
8. [Data Requirements](#data-requirements)
9. [Tips for Beginners](#tips-for-beginners)
10. [Understanding Investment Styles](#understanding-investment-styles)

---

## Overview

This repository contains **professional-grade financial analysis tools** used by investment banks, equity researchers, and financial advisors. As an individual investor, you can leverage these same tools to:

- **Screen** for stock opportunities based on criteria you define
- **Compare** companies to their peers using institutional methodologies
- **Analyze** earnings reports and financial statements
- **Build** valuation models (DCF, Comps, etc.)
- **Create and track** investment theses
- **Monitor** catalysts that could move stocks

---

## Understanding the Repository Structure

### Key Verticals for Individual Investors

| Vertical | Best For |
|----------|----------|
| **equity-research** | Stock analysis, screening, thesis tracking, earnings |
| **financial-analysis** | DCF valuation, comparable analysis, competitive landscapes |
| **wealth-management** | Portfolio building, client proposals (useful for personal planning) |

### Other Verticals (Advanced)

| Vertical | Purpose |
|----------|---------|
| **investment-banking** | M&A materials, CIMs, deal tracking |
| **private-equity** | Deal sourcing, due diligence, IC memos |
| **fund-admin** | Fund administration and NAV |
| **operations** | KYC/compliance workflows |

---

## Quick Start: Key Commands

Here are the most important commands for your investment research workflow:

| Goal | Command | Skill |
|------|---------|-------|
| Find stock ideas | `/screen` | idea-generation |
| Compare companies | `/comps` | comps-analysis |
| Competitive analysis | `/competitive-analysis` | competitive-analysis |
| Analyze earnings | `/earnings` | earnings-analysis |
| Pre-earnings view | `/earnings-preview` | earnings-preview |
| Build DCF model | `/dcf` | dcf-model |
| Full financial model | `/3-statement-model` | 3-statement-model |
| Investment thesis | `/thesis` | thesis-tracker |
| Track catalysts | `/catalysts` | catalyst-calendar |
| Sector research | `/sector` | sector-overview |
| Full research report | `/initiate` | initiating-coverage |
| Quick company profile | `/tear-sheet` | tear-sheet (S&P Global) |

---

## Step-by-Step Investment Workflow

### Step 1: Screen for Investment Opportunities

**Command:** `/screen`

The `idea-generation` skill provides systematic stock screening:

**What it does:**
- Quantitative screens based on your criteria (value, growth, quality, short ideas, special situations)
- Thematic sweeps across sectors
- Framework for presenting investment ideas

**How to use it:**

```
/screen

Screen for [value/growth/quality] stocks in [sector] with [criteria]

Example: "Screen for quality large-cap tech stocks with strong free cash flow and reasonable valuations"
Example: "Find high-growth healthcare companies trading below their intrinsic value"
Example: "Screen for deep value industrial stocks with high dividend yields"
```

**What you'll get:**
- A list of stocks matching your criteria
- Key metrics for each (P/E, EV/EBITDA, growth rates, etc.)
- A framework for evaluating each idea
- Next steps for deeper analysis

---

### Step 2: Compare to Similar Companies

#### 2a. Comparable Company Analysis

**Command:** `/comps`

The `comps-analysis` skill builds institutional-grade comparable company analysis:

**What it does:**
- Operating metrics comparison across peers
- Valuation multiples (P/E, EV/EBITDA, P/S, P/B, etc.)
- Statistical benchmarking (quartiles, medians)
- Formula-based calculations (not hardcoded values)

**How to use it:**

```
/comps

Run a comps analysis on [Company] vs [Competitor1], [Competitor2], [Competitor3]

Example: "Run a comps analysis on Apple vs Microsoft vs Google vs Amazon"
Example: "Compare NVIDIA to AMD, Intel, and Qualcomm"
```

**What you'll get:**
- A professionally formatted Excel-style comps table
- Trading multiples for each company
- Quartile analysis (is the stock cheap or expensive vs peers?)
- Summary of key differences

#### 2b. Competitive Landscape Analysis

**Command:** `/competitive-analysis`

**What it does:**
- Market positioning maps
- 2x2 matrices comparing competitors
- Radar charts showing relative strengths
- Bull/base/bear scenario analysis
- Strategic synthesis

**How to use it:**

```
/competitive-analysis

Example: "Do a competitive analysis of the EV market focusing on Tesla vs BYD vs Ford vs GM"
Example: "Compare Spotify to Apple Music, Amazon Music, and YouTube Music"
```

---

### Step 3: Analyze Earnings and Financials

#### 3a. Post-Earnings Analysis

**Command:** `/earnings`

The `earnings-analysis` skill creates detailed earnings update reports:

**What it does:**
- Beat/miss analysis vs expectations
- Key metrics breakdown (revenue, EPS, margins, guidance)
- Updated estimates
- 8-12 charts with citations
- 8-12 page professionally formatted report

**How to use it:**

```
/earnings

Analyze the latest quarterly earnings for [Company]

Example: "Analyze Tesla's latest quarterly earnings"
Example: "Review Microsoft's Q3 2024 earnings and highlight beat/miss"
```

#### 3b. Pre-Earnings Preview

**Command:** `/earnings-preview`

**What it does:**
- Scenario analysis before earnings
- Key metrics to watch
- Historical beat/miss rates
- What analysts are expecting
- Risk/reward scenarios

**How to use it:**

```
/earnings-preview

Preview earnings for [Company] and provide key scenarios
Example: "Preview Amazon's upcoming earnings with bull/bear/base scenarios"
```

#### 3c. Full Financial Statement Analysis

**Command:** `/3-statement-model`

**What it does:**
- Complete 3-statement model (Income Statement, Balance Sheet, Cash Flow)
- Working capital schedules
- Scenario analysis
- Credit metrics

**How to use it:**

```
/3-statement-model

Build a 3-statement model for [Company]
Example: "Create a 3-statement model for Apple incorporating the last 3 years of data"
```

---

### Step 4: Build a Valuation Model

#### 4a. Discounted Cash Flow (DCF)

**Command:** `/dcf`

The `dcf-model` skill builds a comprehensive DCF analysis:

**What it does:**
- Historical financial analysis
- Revenue projections with 3 scenarios (bull/base/bear)
- Free Cash Flow build
- WACC calculation (cost of equity, cost of debt, capital structure)
- Terminal value calculation
- 3 sensitivity tables (75 cells each)
- Professional Excel formatting

**How to use it:**

```
/dcf

Build a DCF model for [Company] with [assumptions]

Example: "Build a DCF model for Johnson & Johnson using stable growth assumptions"
Example: "Create a DCF for Meta with aggressive growth assumptions"
```

**What you'll learn:**
- What the company is worth today (intrinsic value)
- How sensitive the valuation is to assumptions
- Key value drivers

#### 4b. Full Initiation Report

**Command:** `/initiate`

For the most comprehensive analysis, this skill creates institutional-quality research reports:

**What it does (5-task workflow):**
1. Company research (6-8K words)
2. Financial modeling (6-tab Excel)
3. Valuation (DCF + Comps)
4. Chart generation (25-35 charts)
5. Final DOCX report (30-50 pages)

**How to use it:**

```
/initiate

Create a full initiation report on [Company]

Example: "Create a full equity research initiation on Coinbase"
```

---

### Step 5: Create Your Investment Thesis

**Command:** `/thesis`

The `thesis-tracker` skill helps you articulate and maintain your investment thesis:

**What it does:**
- Structured framework for your investment hypothesis
- Key thesis points with supporting evidence
- Risks and counterarguments
- Track thesis points over time
- Monitor against reality (what's working, what's not)

**How to use it:**

```
/thesis

Create an investment thesis for [Company]

Example: "Create an investment thesis for Shopify highlighting the secular tailwinds in e-commerce"
Example: "Build a thesis for NVIDIA based on AI chip demand"
```

**What you'll create:**
- Clear investment thesis (1-2 paragraphs)
- Bull case vs bear case
- Key metrics to track
- Questions you need answered
- Risk factors

---

### Step 6: Track Your Thesis Over Time

#### 6a. Monitor Catalysts

**Command:** `/catalysts`

**What it does:**
- Calendar of upcoming catalysts (earnings, conferences, product launches, regulatory decisions)
- Track events that could move the stock
- Prioritize your research attention

**How to use it:**

```
/catalysts

Build a catalyst calendar for [Company] for the next 6 months
Example: "What are the key catalysts for Tesla in the next 6 months?"
```

#### 6b. Sector Overview

**Command:** `/sector`

**What it does:**
- Comprehensive industry landscape reports
- TAM/SAM market sizing
- Competitive positioning
- Key player analysis
- Thematic trends
- Valuation context

**How to use it:**

```
/sector

Provide an overview of the [sector/industry] sector
Example: "Give me a comprehensive overview of the semiconductor industry"
Example: "What's the outlook for the global airline industry?"
```

---

## Detailed Command Reference

### Equity Research Commands

| Command | Description | Output |
|---------|-------------|--------|
| `/screen` | Stock screening | Filtered stock list with key metrics |
| `/earnings` | Post-earnings analysis | 8-12 page earnings report |
| `/earnings-preview` | Pre-earnings scenarios | Bull/base/bear analysis |
| `/initiate` | Full research initiation | 30-50 page report with model |
| `/thesis` | Investment thesis creation | Structured thesis document |
| `/catalysts` | Catalyst tracking | Calendar of upcoming events |
| `/sector` | Industry landscape | Comprehensive sector report |
| `/model-update` | Update existing model | Refreshed financial model |

### Financial Analysis Commands

| Command | Description | Output |
|---------|-------------|--------|
| `/comps` | Comparable company analysis | Excel comps table |
| `/dcf` | Discounted cash flow | Excel DCF model |
| `/competitive-analysis` | Competitive landscape | Positioning maps, radar charts |
| `/3-statement-model` | 3-statement model | Linked financial statements |
| `/debug-model` | Audit Excel model | Error report |

### Partner Commands (Require Data Provider Access)

| Command | Source | Description |
|---------|--------|-------------|
| `/tear-sheet` | S&P Global | Professional company tear sheets |
| `/equity-research` | LSEG | Consensus estimates, fundamentals |

---

## Example Workflows

### Workflow 1: Finding and Researching a Tech Stock

**Day 1: Discovery**
```
User: /screen
AI: What criteria would you like to screen for?
User: Screen for quality large-cap technology stocks with strong free cash flow and reasonable valuations (P/E < 30)
```

**Day 2: Deep Dive**
```
User: /screen results show: Apple, Microsoft, Google
User: Run a comps analysis on Apple vs Microsoft vs Google
```

**Day 3: Valuation**
```
User: Build a DCF model for Apple with conservative assumptions
```

**Day 4: Thesis**
```
User: Create an investment thesis for Apple highlighting the services growth and AI opportunities
```

**Day 5: Earnings**
```
User: Analyze Apple's latest quarterly earnings
User: Build a catalyst calendar for Apple for the next 6 months
```

### Workflow 2: Comparing Two Investments

```
User: Screen for high-dividend yield consumer staples stocks
User: Run a comps analysis on Procter & Gamble vs Kimberly-Clark vs Colgate-Palmolive
User: Build a DCF for each company
User: Do a competitive analysis of the consumer staples sector
```

### Workflow 3: Pre-Earnings Trade Idea

```
User: /earnings-preview for NVIDIA ahead of their next earnings
User: Based on the preview, what options strategy might make sense (bull call spread, straddle, etc.)?
User: After earnings: /earnings to analyze the actual results
```

---

## Understanding What Each Skill Does

### Core Research Skills

| Skill | What It Does | Best For |
|-------|--------------|----------|
| `idea-generation` | Stock screening with quantitative filters | Finding new ideas |
| `comps-analysis` | Comparing multiples across peers | Relative valuation |
| `competitive-analysis` | Market positioning, strategic analysis | Understanding competition |
| `earnings-analysis` | Post-earnings beat/miss reports | Quarterly reviews |
| `earnings-preview` | Pre-earnings scenario modeling | Positioning before reports |
| `thesis-tracker` | Structured investment thesis framework | Building conviction |
| `catalyst-calendar` | Event-based stock movers | Timing entry/exit |
| `sector-overview` | Industry landscape and trends | Understanding context |

### Valuation Skills

| Skill | What It Does | Best For |
|-------|--------------|----------|
| `dcf-model` | Intrinsic value via discounted cash flows | Long-term fair value |
| `comps-analysis` | Relative valuation via multiples | Comparing vs peers |
| `3-statement-model` | Full financial model linkage | Deep financial analysis |

### Document Generation Skills

| Skill | What It Does | Output |
|-------|--------------|--------|
| `initiating-coverage` | Full institutional research report | 30-50 page DOCX |
| `earnings-analysis` | Quarterly earnings note | 8-12 page DOCX |
| `xlsx-author` | Excel file creation | .xlsx file |
| `pptx-author` | PowerPoint creation | .pptx file |

---

## Data Requirements

### What Data Sources Are Available

These skills work with data providers configured in the MCP connectors:

| Provider | Data Available |
|----------|----------------|
| Morningstar | Financial data, fundamentals |
| S&P Global (Capital IQ) | Tear sheets, consensus estimates |
| LSEG | Equity research, analytics |
| SEC Filings | 10-K, 10-Q, 8-K documents |
| Aiera | Earnings call transcripts |
| FactSet | Research platform data |
| PitchBook | Private market data |

### What You Need Access To

For full functionality, you may need API access to:

1. **S&P Global Capital IQ** - For tear-sheets, company profiles, consensus data
2. **LSEG** - For equity research and analytics
3. **Morningstar** - For financial data and fundamentals

Some features work with public data (SEC filings), while others require paid subscriptions.

### What You Can Do With Public Data

- Screen using public financial metrics
- Build DCF models with public financial statements
- Analyze earnings from 10-Q/10-K filings
- Create thesis frameworks

---

## Tips for Beginners

### 1. Start Simple

Begin with `/screen` to find ideas, then use `/comps` to compare. Don't jump straight to DCF models until you're comfortable with the basics.

### 2. Build Your Knowledge Gradually

1. **Phase 1:** Learn to screen and compare companies
2. **Phase 2:** Learn to read and analyze earnings
3. **Phase 3:** Learn valuation methodologies (DCF)
4. **Phase 4:** Build comprehensive theses

### 3. Use the Thesis Tracker

The `/thesis` command is your best friend. It helps you:
- Articulate WHY you believe in an investment
- Identify what needs to be true for your thesis to work
- Track what's actually happening vs your expectations

### 4. Always Check Catalysts

Before buying, use `/catalysts` to understand:
- When are the next earnings?
- Any product launches?
- Regulatory decisions?
- Management presentations?

### 5. Compare Multiple Valuation Methods

Don't rely on just DCF or just Comps. Use both:
- DCF tells you intrinsic value
- Comps tells you what others are paying for similar companies

### 6. Track Your Track Record

Keep records of:
- Your screening criteria and why you chose them
- Your thesis for each investment
- What actually happened vs expectations
- What you learned

### 7. Use the initiation Report for Deep Dives

When you find a company you really like, use `/initiate` for the most comprehensive analysis. It's what institutional researchers produce.

---

## Understanding Investment Styles

When you use `/screen`, you'll be asked to define your investment style. Here's what each means, how the industry defines them, and what to watch out for.

### Value Investing

**Definition:** Buying stocks that trade below their intrinsic value (cheap relative to fundamentals)

**Key Metrics:**

| Metric | What It Measures | What "Good" Looks Like |
|--------|-----------------|----------------------|
| P/E (Price/Earnings) | Price relative to earnings | Below 15-20x (varies by sector) |
| P/B (Price/Book) | Price relative to book value | Below 1.5x (below 1x is "cheap") |
| EV/EBITDA | Enterprise value vs cash earnings | Below 8-10x typically |
| P/S (Price/Sales) | Price relative to revenue | Below 1-2x |
| Dividend Yield | Cash return paid to shareholders | Above sector average |
| Debt/Equity | Leverage | Lower is better (below 0.5) |

**What "Value" Investors Look For:**
- Stocks trading at discounts to book value, earnings, or cash flow
- Stable, predictable businesses
- Companies with assets (real estate, brand value, cash) that aren't fully reflected in price
- Mature industries (utilities, financials, consumer staples)

**Things to Be Aware Of:**

- **"Value trap"** — A stock looks cheap but is actually declining. Low P/E can mean the market is pricing in earnings decline.
- **Asset quality** — Book value is only as good as the assets. Goodwill impairments can destroy book value.
- **Catalyst required** — Cheap stocks can stay cheap for years. You need a thesis for why it will re-rate.
- **Financials can be manipulated** — Earnings, book value, and debt levels can be accounting artifacts.

---

### Growth Investing

**Definition:** Buying stocks of companies with high revenue/earnings growth rates, even if they're expensive today

**Key Metrics:**

| Metric | What It Measures | What "Good" Looks Like |
|--------|-----------------|----------------------|
| Revenue Growth | YoY revenue increase | Above 15-20% |
| EPS Growth | Earnings per share growth | Above 15-20% |
| PEG Ratio | P/E relative to growth | Below 1.0 (undervalued given growth), above 2.0 (expensive) |
| Gross Margin | Profitability on core product | High and expanding |
| SGA as % of Revenue | Operating efficiency | Declining over time |

**What "Growth" Investors Look For:**
- Companies in expanding markets (AI, cloud computing, biotech)
- High gross margins (software > 70%, services > 40%)
- Scalable business models (low marginal cost)
- Network effects or moats (brand, patents, switching costs)
- Reinvesting all cash into growth

**Things to Be Aware Of:**

- **Valuation risk** — High growth + high multiple = devastating if growth disappoints
- **Concentration risk** — Growth stocks often rally together; when sentiment turns, everything drops
- **Profitability matters** — Revenue growth without path to profit is a red flag
- **Moat sustainability** — Today's disruptor is tomorrow's legacy company
- **Interest rate sensitivity** — High-growth stocks are hurt most when rates rise (future earnings worth less today)

---

### Quality Investing

**Definition:** Buying companies with strong balance sheets, high profitability, and durable competitive advantages (moats)

**Key Metrics:**

| Metric | What It Measures | What "Good" Looks Like |
|--------|-----------------|----------------------|
| Return on Equity (ROE) | Profit generated per shareholder dollar | Above 15-20% |
| Return on Invested Capital (ROIC) | How well capital is deployed | Above 10-15% |
| Gross Margin | Pricing power | High and stable/increasing |
| Net Margin | Bottom-line profitability | Above 10-15% for quality |
| Debt/EBITDA | Leverage | Below 2-3x |
| Current Ratio | Short-term liquidity | Above 1.5x |
| Free Cash Flow | Cash generated after investments | Positive and growing |

**What "Quality" Investors Look For:**
- Consistent profitability across cycles
- High ROIC — management effectively deploys capital
- Low debt or sustainable debt levels
- Strong cash flow conversion (net income → free cash flow)
- Wide moats: brand, patents, network effects, regulatory advantages
- Management with shareholder orientation

**Things to Be Aware Of:**

- **Quality at a high price** — Famous quality stocks (Coca-Cola, Apple) are not cheap
- **ROE manipulation** — Can be inflated via buybacks (less equity denominator) or debt (leverage)
- **Past performance** — Quality is a rearview mirror metric; competitive disruption is forward-looking
- **Sector context** — A 15% ROE in banking is excellent; in tech it's mediocre

---

### Income Investing

**Definition:** Prioritizing stocks that pay regular, sustainable dividends

**Key Metrics:**

| Metric | What It Measures | What "Good" Looks Like |
|--------|-----------------|----------------------|
| Dividend Yield | Annual dividend / stock price | Above 3-4% (but investigate why) |
| Payout Ratio | % of earnings paid as dividends | Below 60-70% (leaves room) |
| Dividend Growth | YoY dividend increase | Consistent growth > 5% |
| FCF Yield | Free cash flow / market cap | Higher than dividend yield |
| 5-Year Dividend History | Consistency | Uninterrupted, growing dividends |

**What "Income" Investors Look For:**
- Stable, mature businesses with predictable cash flows
- Utilities, REITs, consumer staples, telecom
- Dividend aristocrats (25+ years of consecutive increases)
- Sustainable payout ratios
- Cash flow well above dividend obligations

**Things to Be Aware Of:**

- **High yield trap** — Yield above 7-8% usually means the market smells trouble; dividend may be cut
- **Payout ratio too high** — If > 100%, the dividend is not sustainable
- **Currency risk** — International dividends can fluctuate with exchange rates
- **Inflation** — Fixed dividends lose purchasing power if dividends don't grow

---

### Momentum Investing

**Definition:** Buying stocks that have gone up recently, expecting the trend to continue

**Key Metrics:**

| Metric | What It Measures | What "Good" Looks Like |
|--------|-----------------|----------------------|
| 6-Month Price Return | Recent trend | Strong positive |
| 12-Month Price Return | Longer trend | Strong positive |
| Relative Strength (RS) | Outperformance vs index/sector | Top quartile |
| Volume Trend | Buying conviction | Increasing volume confirms trend |

**What "Momentum" Investors Look For:**
- Stocks hitting new 52-week highs
- Strong relative strength vs market/sector
- Positive news catalysts (earnings beat, product launch)
- Institutional buying (increasing ownership %)
- Technical breakout patterns

**Things to Be Aware Of:**

- **Momentum crashes** — What goes up fast can come down faster
- **No fundamental anchor** — You're buying based on price, not value
- **Late to the party** — By the time signal fires, much of the move may be over
- **Contradicts value** — Momentum stocks are often expensive; combines poorly with value screens

---

### Short Selling (Advanced)

**Definition:** Betting that a stock will decline (advanced strategy)

**Key Metrics:**

| Metric | What It Measures | What "Good" Looks Like |
|--------|-----------------|----------------------|
| Short Interest | % of float sold short | Above 20% (high pessimism) |
| Days to Cover | How long to cover shorts at avg volume | Above 5-8 days (risk of short squeeze) |
| Short Interest Ratio | Shorts / avg daily volume | High number = squeeze potential |
| Borrow Fee | Cost to borrow shares | High fees = hard to borrow |

**Things to Be Aware Of:**
- **Unlimited downside** — Stocks can infinitely exceed your price target
- **Short squeezes** — Shorts covering = buying fuel for rapid rallies
- **Dividends owed** — Must pay dividends to lender
- **Timing is everything** — Wrong on thesis but right on timing = losses

---

### Combining Styles: The Most Sensible Approach for Beginners

Most successful individual investors **combine styles**:

| Combination | Why It Works |
|-------------|--------------|
| **Quality + Value** | Find good companies trading at reasonable prices |
| **Quality + Growth** | Great companies with sustainable growth at a fair price |
| **Dividend Growth (Quality + Income)** | Companies that raise dividends consistently (quality signal) + income |

**The "GARP" Strategy (Growth at Reasonable Price):**
- PEG ratio below 1.5
- ROE above 15%
- Debt/Equity below 1x
- 5-year earnings growth above 10%

---

### Quick Reference: Screening Criteria by Style

| Style | Primary Screen | Secondary Screen |
|-------|---------------|------------------|
| **Value** | P/E < sector avg, P/B < 1.5 | EV/EBITDA < 10, Debt/Equity < 0.5 |
| **Growth** | Revenue growth > 15%, EPS growth > 15% | Gross margin > 40%, ROIC > 15% |
| **Quality** | ROE > 15%, ROIC > 10% | Net margin > 10%, Debt/EBITDA < 2x |
| **Income** | Dividend yield > 3% | Payout ratio < 70%, 5yr dividend growth > 5% |
| **Momentum** | 6-month return > sector | RS rating > 80, volume increasing |

---

### Common Pitfalls to Avoid

1. **Screening without thesis** — Finding a "cheap" stock doesn't mean it's a good investment. The market may know something you don't.

2. **Single metric obsession** — A low P/E means nothing without understanding WHY it's low. Always use multiple metrics.

3. **Ignoring industry context** — A 10% debt/equity is fine for utilities but terrible for banks.

4. **Growth without profit path** — Revenue is vanity, profit is sanity. Revenue growth is only good if there's a path to profitability.

5. **Dividend yield traps** — Above 7% yield is usually a warning sign, not a bargain.

6. **Momentum as a substitute for research** — Price momentum without understanding WHY is speculation.

7. **Survivorship bias** — Value indexes only contain surviving companies; dead value stocks are removed from averages.

8. **Backtest overfitting** — Strategies that worked historically often fail going forward due to overfitting to past data.

---

## Common Use Cases

### Use Case 1: "I want to find undervalued stocks in the healthcare sector"

```
/screen
```
Choose: value screen with criteria like P/E < 20, EV/EBITDA < 15, debt/equity < 0.5

### Use Case 2: "I own Apple and want to understand if I should hold"

```
/earnings  (analyze latest quarter)
/catalysts  (what's coming up)
/thesis  (update your thesis with new information)
/dcf  (is the intrinsic value higher than the current price?)
```

### Use Case 3: "I'm deciding between two stocks to buy"

```
/comps  (compare both companies)
/dcf  (build DCF for both)
/competitive-analysis  (understand their relative positioning)
```

### Use Case 4: "I want to understand a new industry"

```
/sector  (get comprehensive industry overview)
/screen  (find the key players)
/comps  (see how companies compare)
/competitive-analysis  (understand competitive dynamics)
```

### Use Case 5: "Earnings are coming up for NVIDIA"

```
/earnings-preview  (get scenarios and key metrics to watch)
/catalysts  (see what else is coming)
/thesis  (does your thesis still hold?)
```

---

## Next Steps After Using This Guide

1. **Install the plugins** you need (equity-research and financial-analysis are essential)
2. **Start with `/screen`** to find companies you're interested in
3. **Use `/comps`** to understand relative valuation
4. **Build a thesis** with `/thesis`
5. **Track your thesis over time** with `/catalysts` and `/earnings`

---

## Getting Help

- Use `/help` for general assistance
- Review the skill files in `plugins/vertical-plugins/equity-research/skills/` for detailed methodology
- Check the README.md for installation instructions

---

*Last Updated: June 2026*
*Version: 1.0*
