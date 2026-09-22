# Credit Memo Generation — Cowork Plugin

*Developed by [Synechron Technologies PVT LTD](https://www.synechron.com)*

---

> **⚠️ Legal Disclaimer**
>
> This plugin is provided by Synechron on an "AS IS" and "AS AVAILABLE" basis, without warranties of any kind (express, implied, or statutory), including merchantability, fitness for a particular purpose, non-infringement, accuracy, or uninterrupted availability. Synechron disclaims all liability for any loss, damage, claims, or third-party liabilities arising from or related to use of, or reliance on, the plugin or its outputs. Users are solely responsible for evaluating results, ensuring compliance with applicable laws/policies, and implementing appropriate safeguards before use in any production or regulated context. Synechron shall have no liability whatsoever in connection with the plugin or its outputs.
>
> See [DISCLAIMER.md](./DISCLAIMER.md) for full terms.

---

Generate professional Credit Memorandums in Word, PDF, and PowerPoint with 10 embedded charts. Supports public and private companies. Uses authenticated API calls with SerpApi and SEC EDGAR keys.

> ⚠️ **Important:** All outputs are AI-generated research aids and must be reviewed by a qualified credit professional before use in any lending decision. This plugin does not constitute financial advice.

---

## What's Included in v1.0.0

| Feature | Details |
|---|---|
| Output formats | Word (.docx) + PDF (watermarked) + PowerPoint (.pptx) |
| Charts/Visuals | 10 professional charts, embedded in all formats |
| API key support | SerpApi + SEC EDGAR |
| Private companies | Document upload + web fallback + gap log |
| Internal ratings | Config, upload, or intake |
| Financial history | 3–5 years + sector benchmarks |
| Guardrails | 5-layer compliance enforcement |
| Setup command | Key validation + connectivity check |
| Sector thresholds | 6 industry categories |

---

## Setup

### Step 1 — Add API Keys (Optional but Recommended)
Copy the template and add your keys:
```
config/config.template.md  →  copy and rename to  →  config/config.local.md
```
Then open `config.local.md` and fill in:

**SerpApi Key** — Get free at https://serpapi.com/dashboard
```
SERPAPI_KEY=your_actual_key_here
```

**SEC EDGAR User-Agent** — Not a password; a courtesy identifier required by the SEC.
Format: `"OrganizationName contact@youremail.com"`
```
SEC_EDGAR_KEY=Acme Credit Team analyst@acmebank.com
```

### Step 2 — Verify Setup
Run the setup command to confirm connectivity:
```
/credit-memo-generation:setup
```

---

## Commands

| Command | Description |
|---|---|
| `/credit-memo-generation:setup` | Validate API keys and check connectivity |
| `/credit-memo-generation:generate` | Full Credit Memo — Word + PDF + PowerPoint |
| `/credit-memo-generation:quick-risk-check` | 2-minute preliminary risk screen |
| `/credit-memo-generation:industry-snapshot` | Standalone industry analysis report |
| `/credit-memo-generation:refresh-data` | Update existing memo with latest data |

---

## Output Files

### Full Credit Memo (`/credit-memo-generation:generate`)
Three files per analysis:
- `Credit_Memo_[Company]_[Date].docx` — Full detailed memo (25–45 pages)
- `Credit_Memo_[Company]_[Date].pdf` — Locked PDF with CONFIDENTIAL watermark
- `Credit_Memo_[Company]_[Date]_Deck.pptx` — Executive summary deck (15–20 slides)

### Charts Generated (10)
1. Revenue & EBITDA Trend (5-Year)
2. Profit Margins vs. Industry Benchmark
3. Cash Flow Waterfall
4. Balance Sheet Composition
5. Key Financial Ratios Dashboard (Traffic Light)
6. Credit Rating Scale Visual
7. Industry Market Size & Growth
8. SWOT Matrix (4-quadrant color)
9. DSCR Stress Test (3 scenarios)
10. Management Tenure Timeline

---

## Private Company Support

When a private company is detected, the plugin prompts for document uploads and falls back to web search for missing data. All data is clearly tagged:

- `[FROM UPLOAD — Management Provided]` — from uploaded documents
- `[WEB ESTIMATE — Verify independently]` — from web search fallback
- `[NOT AVAILABLE]` — not found from any source

All private company analyses include this disclaimer:
> *"This analysis is based on management-provided financials and/or web-sourced estimates. Independent verification is strongly recommended before credit approval."*

---

## Data Handling & Privacy

Uploaded documents (financial statements, bank statements, tax returns) are processed locally within your Cowork session. They are not transmitted to third parties beyond the data sources configured in `.mcp.json`. Handle all uploaded documents in accordance with your organization's data classification policies.

---

## Configuring Data Sources

The plugin ships with free public data sources out of the box. For production use, you can configure premium providers and your own internal systems via `config/data-sources.md`.

### Built-in free sources (no configuration required)
| Source | Usage |
|---|---|
| SEC EDGAR | 10-K, 10-Q, 8-K filings (User-Agent header required — see setup) |
| SerpApi | Web/news/finance search (free tier: 100 searches/month) |
| Stock Analysis | Financial statements, ratios |
| Macrotrends | 10-year historical data |
| DiscoverCI | Company intelligence |

### Configurable premium sources
Add API keys to `config/config.local.md` and enable sources in `config/data-sources.md`:

| Provider | What it unlocks | Config key |
|---|---|---|
| Bloomberg Terminal | Real-time data, full financials, ratings, M&A | `BLOOMBERG_KEY` |
| Refinitiv / LSEG Eikon | Financial statements, estimates, news feeds | `REFINITIV_KEY` |
| FactSet | Standardised financials, estimates, ownership | `FACTSET_KEY` |
| S&P Capital IQ | Private company data, M&A comps, credit scores | `SP_CAPITAL_IQ_KEY` |
| PitchBook | Private company financials, VC/PE deal data | `PITCHBOOK_KEY` |

### Internal systems
The plugin can connect to your own databases and systems via `config/data-sources.md`:

- **Internal financial database** — REST API or MCP connector; takes highest priority when configured
- **Internal credit rating system** — REST API, MCP, or static CSV lookup table
- **CRM (Salesforce, Dynamics)** — relationship history and existing facility data
- **Document management (SharePoint, Box, Google Drive)** — for private company document ingestion

See `config/data-sources.md` for full setup instructions with examples for each source type.

*Note: Always verify compliance with each source's Terms of Service for automated access.*

---

## Citations & Source Attribution

Every Credit Memo generated by this plugin includes:

- **Inline citation numbers** `[1]`, `[2]`, etc. next to key figures in the document body
- **Appendix A — Citations & References** — full table of all sources with URLs and retrieval dates
- **Key Figure Citation Map** — links each major figure (revenue, ratings, ratios, market data) to its source

---

## Data Freshness Policy

The plugin enforces strict data freshness rules and will warn when data may be stale:

| Data type | Maximum age before warning |
|---|---|
| Quarterly financials | 6 months |
| Annual financials | 18 months |
| Credit ratings | 12 months |
| News coverage | 30-day minimum window required |
| Industry/market data | 24 months |

Every output includes a **Data Freshness Summary** box in the Executive Summary showing the age of each data category and when data was retrieved.

Freshness thresholds are configurable per organisation in `config/data-sources.md`.

---

## Disclaimer

This plugin is an AI-assisted research tool. All Credit Memorandums, risk assessments, and analyst recommendations generated by this plugin require review by a qualified credit professional before any lending decision is made.

For the full legal disclaimer covering warranties, liability, and compliance obligations, see [DISCLAIMER.md](./DISCLAIMER.md).

---

*Developed by [Synechron Technologies PVT LTD](https://www.synechron.com)*
