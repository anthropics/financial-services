# Aether — Agent-Native Financial Search

Search SEC filings and EU financial regulation in natural language, and get back
**as-filed, citable** text — never analyst-adjusted. Aether is a financial-vertical
search engine purpose-built for agents, exposed over MCP.

## What This Plugin Does

This plugin wires the [Aether MCP server](https://github.com/EvidInvest/aether-developer)
into Claude and packages its tools into high-level workflows. Each command orchestrates a
search tool into a complete, citation-backed answer instead of leaving you to call tools one
at a time.

The corpus today:

- **SEC filings** — 10-K / 10-Q / 8-K for the S&P 500 across ~10 years, ~1.4M retrieval chunks.
- **EU financial regulation** — a 29-act corpus (~13,000 citable units) spanning MiFID II,
  MiFIR, MAR, EMIR, MiCA, DORA, CRR/CRD IV, UCITS/AIFMD, PSD2, Solvency II, SFDR/Taxonomy/CSRD,
  the 2024 AML package, and more.
- **Marketplace** — third-party research and data published by registered sellers, searchable
  alongside the first-party corpus.

## Commands

| Command | Description |
|---------|-------------|
| `/sec-deep-dive` | Pull the most relevant 10-K/10-Q/8-K sections on a topic for a company, with as-filed quotes and filing citations |
| `/regulation-lookup` | Find the controlling EU-regulation text for a question, returned as citable Article-paragraphs / recitals |
| `/supply-chain-exposure` | Find public companies disclosing exposure to a supply-chain risk, grouped by ticker |

## Skills

| Skill | Domain Knowledge |
|-------|-----------------|
| `sec-filings-research` | Retrieval profiles, `section` vs `chunk` returns, as-filed discipline, citation hygiene |
| `eu-regulation-research` | CELEX map, consolidated vs OJ text, doc-type/article/AML-topic filters, citation breadcrumbs |

## Integrations

This plugin connects to the **Aether MCP Server**, which serves these tool families:

- **Search** — `financial_search` (SEC filings + supply-chain relationships),
  `regulation_search` (EU financial regulation).
- **Marketplace (read)** — `list_partners`, `partner_search` (indexed seller documents),
  `partner_proxy_search` (paid server-to-server seller queries).
- **Marketplace (sell)** — `seller_signup`, `seller_publish_document`,
  `seller_register_endpoint`, `seller_list_my_documents`, `seller_list_my_endpoints`.

See [CONNECTORS.md](CONNECTORS.md) for the complete tool reference and parameters.

## Installation

```
claude plugins add aether
```

## Requirements & Authentication

The MCP server is distributed on npm as [`@evidinvest/aether-mcp`](https://www.npmjs.com/package/@evidinvest/aether-mcp)
and run via `npx` (see [`.mcp.json`](.mcp.json)). Authentication options:

- **API key** — set `AETHER_API_KEY` (get one at <https://aether.evidinvest.com/developer/keys>).
  Verified accounts include a **3-month free trial** (5,000 calls/hr on Aether's first-party tools).
- **OAuth device code** — omit the key and the server prints a sign-in URL on first run; the
  token is cached and refreshed automatically.
- **Anonymous** — set `AETHER_NO_AUTH=1` to call without an account (rate-limited).

## Why Aether

- **As-filed, never adjusted.** Numbers and language come straight from the source filing, with
  the section, filing URL, and ticker attached — not a vendor's normalized model.
- **First agent-native financial search.** Built for tool-calling agents, not a human UI bolted
  onto an API.
- **One server, multiple corpora.** US disclosure and EU regulation behind a single MCP
  connector, plus an open marketplace for third-party data.
