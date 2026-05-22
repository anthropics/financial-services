# P&L Analyser — managed-agent template

## Overview

Parses a P&L statement or management accounts file, computes actual vs budget/prior-period variances with root-cause attribution, and produces CFO-ready management commentary.

Same source as the [`pnl-analyser`](../../plugins/agent-plugins/pnl-analyser) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
../../scripts/deploy-managed-agent.sh pnl-analyser
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with a period reference and optional comparison baseline (budget, prior month, prior year).

## Security & handoffs

The agent reads uploaded financial documents that may be authored externally. The template isolates write access:

| Tier | Touches uploaded docs? | Tools | Connectors |
|---|---|---|---|
| **`statement-reader`** | **Yes** | `Read`, `Grep` only | None |
| **`variance-runner`** | No (structured data only) | `Read` only | None |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | None |
| **`commentary-writer`** (Write-holder) | No | `Read`, `Write` | None |

The `statement-reader` returns length-capped, schema-validated JSON only. The `commentary-writer` writes to `./out/`; it never opens the original uploaded document.

**Not guaranteed:** no commentary is approved for external distribution without human sign-off.
