# Forensic QoE — managed-agent cookbook

## Overview

Pre-LOI forensic Quality-of-Earnings screen for a private-company target.
Same workflow as the OloLand Cowork plugin
[`ololand-forensic-qoe`](https://github.com/ololand-ai/ololand-plugins/tree/main/plugins/ololand-forensic-qoe) —
this directory is the Managed Agent cookbook for `POST /v1/agents`.

The cookbook drives [OloLand](https://app.ololand.ai)'s 41-tool MCP server,
which exposes deterministic financial engines (Beneish M-Score, Benford's
Law, EBITDA bridge, revenue-quality deep dive, working-capital analysis,
journal-entry testing, lapping detection) and the 246-category risk
taxonomy with cross-document reconciliation against a CPA-audited > tax >
management > AI-extracted source hierarchy.

**Output:** an IC-defensible 1-page PDF (`./out/forensic-screen-<deal_id>.pdf`)
plus a structured JSON receipt with every adjustment cited to source.

**Positioning:** stage-1 screen, not a Big-4 replacement. Big-4 forensic
QoE runs $150K-$500K and 4-8 weeks; this screen runs the same seven-
primitive battery in 72 hours and produces the IC-defensible artifact that
decides whether to commit the Big-4 spend.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OLOLAND_MCP_URL="https://api.ololand.ai/mcp"  # public OloLand MCP endpoint
../../scripts/deploy-managed-agent.sh forensic-qoe
```

The OloLand MCP server authenticates per-call via an `olo_agent_sk_*`
agent key (per-company scoped, credit-metered). Provision a key at
[`app.ololand.ai/settings/api-keys`](https://app.ololand.ai/settings/api-keys)
and supply it via the standard MCP `Authorization: Bearer` header.

## Steering events

See [`steering-examples.json`](./steering-examples.json). The cookbook is
designed to run one session per target — fan-out across a pipeline list
from your orchestration layer (Temporal / Airflow / Guidewire).

## Security & handoffs

Source documents (audited financials, tax returns, management
projections, CIM) are untrusted — they often arrive from sponsor-side
data rooms. Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`document-reader`** | **Yes** | `Read`, `Grep` only | OloLand `upload_deal_document` only |
| `forensic-runner` / Orchestrator | No (reads through OloLand engines) | `Read`, `Grep`, `Glob`, `Agent` | OloLand (analyze + verify + get + read) |
| **`report-writer`** (Write-holder) | No | `Read`, `Write`, `Edit` | OloLand `generate_forensic_screen_pdf` + `record_materialized_risks` only |

`document-reader` returns length-capped, schema-validated JSON. Document
contents are routed through OloLand's ingestion pipeline (Qdrant
embeddings + cross-document reconciler) rather than read by the
orchestrator turn — any prompt-injection inside a source PDF cannot
reach the forensic-runner or the report-writer.

`forensic-runner`'s output schema constrains the findings list shape so
the report-writer cannot be steered by an upstream injection to alter
the report's structure.

`report-writer` is the only worker with `Write`. It produces
`./out/forensic-screen-<deal>.pdf` (the rendered artifact downloaded
from OloLand) and `./out/forensic-screen-<deal>.json` (the structured
receipt), then writes back to OloLand's deal record via
`record_materialized_risks` so the institutional learning flywheel
captures the findings for cross-deal pattern matching.

**Reconciliation-gap halt.** If `forensic-runner` returns
`status: "reconciliation_gap"`, the cookbook stops before generating
the PDF. Forensic QoE on top of an unresolved revenue/EBITDA/net-debt
disagreement between source documents is not defensible — the gap is
surfaced for analyst review instead.

**Handoff:** to push the forensic findings into a full IC memo,
emit a `handoff_request` for `ic-memo` (not yet shipped as a cookbook;
analysts use the OloLand `/ic-memo-skeptical` Cowork command in the
interim).

## What this cookbook does NOT do

- **Replace Big-4 QoE.** This is a stage-1 pre-LOI screen. It runs on
  pre-LOI source material (audited financials + tax + management
  projections + CIM) and produces an IC-defensible artifact in 72h.
  A full QoE requires management transaction-level data, on-site visits,
  and customer concentration interviews — out of scope for this
  cookbook.
- **Fan out to web search.** Pre-LOI screens are deliberately walled off
  from current news and announcement-era materials. The cookbook does
  not call any web-fetching tool.
- **Make a recommendation without source citation.** Every $-figure in
  the rendered PDF is enforced to trace to a specific source document,
  page, and section by the OloLand renderer. If a citation can't be
  produced, the figure is omitted with a gap marker rather than
  invented.

## See also

- [OloLand: Anthropic Finance Ecosystem placement](https://docs.ololand.ai/anthropic-placement) — strategic context: why OloLand ships as a cookbook + plugins + direct app.
- [`ololand-forensic-qoe`](https://github.com/ololand-ai/ololand-plugins/tree/main/plugins/ololand-forensic-qoe) — the Cowork plugin (analyst surface) that shares this cookbook's tool spec.
- [OloLand MCP server](https://api.ololand.ai/mcp) — the 41-tool endpoint this cookbook drives.
