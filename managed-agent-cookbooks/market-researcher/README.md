# Market Researcher — managed-agent template

## Overview

Sector or theme → industry overview → competitive landscape → peer comps → ideas shortlist → research note. Same source as the [`market-researcher`](../../plugins/agent-plugins/market-researcher) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... FACTSET_MCP_URL=...
../../scripts/deploy-managed-agent.sh market-researcher
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick from a research-queue event or fan out across a coverage map.

## Security & handoffs

Third-party reports and issuer materials are untrusted. Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`sector-reader`** | **Yes** | `Read`, `Grep` only | None |
| `comps-spreader` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | CapIQ, FactSet (read-only) |
| **`note-writer`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`sector-reader` returns length-capped, schema-validated JSON. `note-writer` produces `./out/primer-<sector>.docx` (and `.pptx` if slides requested).

**Handoff:** to model a single name surfaced in the ideas shortlist, emit a `handoff_request` for `model-builder`; `scripts/orchestrate.py` routes it as a new steering event.
