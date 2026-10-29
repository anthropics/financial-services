# Connectors

This plugin connects to a single MCP server, **Aether** (`@evidinvest/aether-mcp`), which
proxies to `https://api.aether.evidinvest.com`. No additional connectors are required. The
server advertises **11 tools** in three families. Commands reference tools by their exact
names below.

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| Search | `financial_search`, `transcript_search`, `regulation_search` | First-party retrieval over SEC filings, earnings transcripts, and EU regulation |
| Marketplace — read | `list_partners`, `partner_search`, `partner_proxy_search` | Discover and query third-party seller data |
| Marketplace — sell | `seller_signup`, `seller_publish_document`, `seller_register_endpoint`, `seller_list_my_documents`, `seller_list_my_endpoints` | Publish documents or register paid endpoints as a seller |

## Search Tools

### `financial_search`
Natural-language hybrid retrieval over SEC filings (10-K/10-Q/8-K) and supply-chain
relationships. Returns ranked, structured, LLM-ready results with snippets, section titles,
filing URLs, and tickers.

| Param | Type | Notes |
|-------|------|-------|
| `query` | string | **Required.** Natural-language query. |
| `domain` | enum | `public_equity` \| `supply_chain` \| `auto` (default `auto`). |
| `limit` | number | Default 10, max 50. |
| `fields` | string[] | Optional field projection. |
| `profile` | enum | `bm25` \| `hybrid` \| `hybrid_rerank` \| `hybrid_rerank_tickerprior` (default — the production winner: hybrid + cross-encoder rerank + ticker-prior). |
| `return_format` | enum | `section` (default — full SEC section the match belongs to) \| `chunk` (matching window only) \| `both`. |

### `transcript_search`
Hybrid retrieval over earnings-call transcripts (CEO/CFO commentary + analyst Q&A). Returns
ranked verbatim speaker turns with citations. Use for forward-looking color (guidance,
narrative) that filings don't capture.

| Param | Type | Notes |
|-------|------|-------|
| `query` | string | **Required.** |
| `ticker` | string | Optional ticker filter (e.g. `NVDA`). |
| `lookback_quarters` | number | Keep calls within the last N quarters (default: no filter). |
| `speaker_role` | string | Optional: `CEO` \| `CFO` \| `Analyst` \| `Operator`. |
| `limit` | number | Default 10, max 50. |
| `profile` | enum | `bm25` \| `hybrid` (default). |

### `regulation_search`
Search a 29-act EU financial-regulation corpus (~13,000 citable chunks). Returns ranked,
citable units — Article-paragraphs, recitals, annex blocks — each with a human breadcrumb
(e.g. `MiCA 2023/1114 · Art. 4 · para. 1`). Scoped to financial regulation, not all EU law.

| Param | Type | Notes |
|-------|------|-------|
| `query` | string | **Required.** |
| `celex` | string \| string[] | Optional CELEX filter, e.g. `32014L0065` (MiFID II), `32023R1114` (MiCA), `32013R0575` (CRR), `32022R2554` (DORA), `32024R1624` (AMLR). Omit to search the whole corpus. |
| `doc_type` | string | `regulation` \| `directive` \| `rts` \| `its` \| `decision`. |
| `article` | string | Single-article filter, e.g. `"20"` or `"12a"`. |
| `chunk_type` | string | `paragraph` \| `article_intro` \| `recital` \| `table` \| `annex`. |
| `aml_topics` | string \| string[] | `cdd` \| `edd` \| `pep` \| `str_reporting` \| `governance` \| `reporting` \| `transaction_monitoring`. |
| `prefer_consolidated` | boolean | Prefer EUR-Lex consolidated text over original OJ text at equal relevance (hybrid only). |
| `limit` | number | Default 10, max 50. |
| `profile` | enum | `bm25` \| `hybrid` (default). |

## Marketplace — Read Tools

### `list_partners`
List active marketplace sellers and what each offers. Each partner exposes zero or more modes:
`indexed` (free queries via `partner_search`) and/or `proxy` (paid per-call queries via
`partner_proxy_search`). Returns pricing so you can budget before calling. Params: `ticker`
(optional coverage filter), `mode` (`indexed` \| `proxy` \| `any`), `limit`.

### `partner_search`
Search marketplace partner documents (research notes, supply-chain analyses) published by
registered sellers. Returns ranked chunks with per-document attribution and license terms.
Call `list_partners` first to scope via `partners`. Params: `query` (**required**), `partners[]`,
`doc_types[]`, `ticker_filter`, `limit`, `profile`.

### `partner_proxy_search`
Route a query server-to-server to seller-registered API endpoints. **Costs accrue per call**
regardless of result count; Aether holds seller credentials so the agent never sees the URL or
token. Params: `query` (**required**), `partners[]` (**required** — you must pick explicitly,
no surprise billing), `endpoints[]`, `ticker_filter`, `limit`, `confirm_charge` (must be `true`
to execute; otherwise returns a dry-run quote).

## Marketplace — Sell Tools

For data publishers, not analysis workflows. Briefly:

- **`seller_signup`** — create a seller account (returns an API key once; new accounts are
  `pending_review` until ops approves, unless an `invite_code` is supplied).
- **`seller_publish_document`** — publish/update a document (chunked, embedded, indexed in the
  background); re-publishing the same `external_doc_id` replaces the prior version.
- **`seller_register_endpoint`** — register a proxy endpoint (Mode B); secret stored encrypted
  at rest, per-call pricing via `price_per_call_usd_cents`.
- **`seller_list_my_documents`** / **`seller_list_my_endpoints`** — inventory + status; secrets
  never returned.
