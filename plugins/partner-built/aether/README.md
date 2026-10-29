# Aether — Agent-Native Financial Search

Search SEC filings, earnings-call transcripts, and EU financial regulation in natural
language, and get back **as-filed, citable** text — never analyst-adjusted. Aether is a
financial-vertical search engine purpose-built for agents, exposed over MCP.

## What This Plugin Does

This plugin wires the [Aether MCP server](https://github.com/EvidInvest/aether-developer)
into Claude and packages its tools into high-level workflows. Each command orchestrates a
search tool into a complete, citation-backed answer instead of leaving you to call tools one
at a time.

The corpus today:

- **SEC filings** — 10-K / 10-Q / 8-K for the S&P 500 across ~10 years, ~1.4M retrieval chunks.
- **Earnings-call transcripts** — CEO / CFO commentary and analyst Q&A, for forward-looking
  color that filings don't capture.
- **EU financial regulation** — a 29-act corpus (~13,000 citable units) spanning MiFID II,
  MiFIR, MAR, EMIR, MiCA, DORA, CRR/CRD IV, UCITS/AIFMD, PSD2, Solvency II, SFDR/Taxonomy/CSRD,
  the 2024 AML package, and more.
- **Marketplace** — third-party research and data published by registered sellers, searchable
  alongside the first-party corpus.

## Commands

| Command | Description |
|---------|-------------|
| `/sec-deep-dive` | Pull the most relevant 10-K/10-Q/8-K sections on a topic for a company, with as-filed quotes and filing citations |
| `/earnings-color` | Surface CEO/CFO/analyst commentary on a topic from earnings-call transcripts, quoted verbatim with speaker + date |
| `/regulation-lookup` | Find the controlling EU-regulation text for a question, returned as citable Article-paragraphs / recitals |
| `/supply-chain-exposure` | Find public companies disclosing exposure to a supply-chain risk, grouped by ticker |

## Skills

| Skill | Domain Knowledge |
|-------|-----------------|
| `sec-filings-research` | Retrieval profiles, `section` vs `chunk` returns, as-filed discipline, citation hygiene |
| `earnings-transcript-research` | Speaker-role and lookback filtering, separating guidance from reported results |
| `eu-regulation-research` | CELEX map, consolidated vs OJ text, doc-type/article/AML-topic filters, citation breadcrumbs |

## Integrations

This plugin connects to the **Aether MCP Server**, which serves these tool families:

- **Search** — `financial_search` (SEC filings + supply-chain relationships),
  `transcript_search` (earnings calls), `regulation_search` (EU financial regulation).
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

This is a **remote MCP server** over Streamable HTTP at
`https://api.aether.evidinvest.com/mcp` (see [`.mcp.json`](.mcp.json)) — works in both
Claude Cowork and Claude Code, nothing to install. Authentication:

- **OAuth device code** — on first connect the client walks you through sign-in at
  <https://aether.evidinvest.com>; the token is cached and refreshed automatically.
  Verified accounts include a **3-month free trial** (5,000 calls/hr on Aether's first-party tools).
- **Anonymous** — connect without signing in to try it out, rate-limited to 5 calls/hour.

A self-hosted / stdio option (`npx @evidinvest/aether-mcp` with `AETHER_API_KEY`) is also
available — see the [aether-developer repo](https://github.com/EvidInvest/aether-developer).

## Why Aether

- **As-filed, never adjusted.** Numbers and language come straight from the source filing, with
  the section, filing URL, and ticker attached — not a vendor's normalized model.
- **First agent-native financial search.** Built for tool-calling agents, not a human UI bolted
  onto an API.
- **One server, three corpora.** US disclosure, earnings narrative, and EU regulation behind a
  single MCP connector, plus an open marketplace for third-party data.
