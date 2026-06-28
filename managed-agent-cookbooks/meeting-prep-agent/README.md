# Meeting Prep Agent — managed-agent template

## Overview

Briefing pack before every client meeting. Same source as the [`meeting-prep-agent`](../../plugins/agent-plugins/meeting-prep-agent) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CRM_MCP_URL=... CAPIQ_MCP_URL=...
../../scripts/deploy-managed-agent.sh meeting-prep-agent
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Typically kicked from a calendar event by your workflow engine.

## Security & handoffs

Client-provided documents and inbound emails are untrusted. Three-tier split:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| `profiler` | No | `Read`, `Grep` | CRM, CapIQ (read-only) |
| **`news-reader`** | **Yes** | `Read`, `Grep` only | None |
| **`pack-writer`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`pack-writer` produces `./out/briefing-<client>.pptx`; it never opens client-provided content directly.

**Not guaranteed:** this pack is for the advisor, not the client. No client-facing send.
