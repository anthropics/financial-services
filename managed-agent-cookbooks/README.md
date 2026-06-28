# Managed-agent templates for financial services

Every agent in this repo ships **two ways**: as a Cowork plugin your analysts install today (see the vertical directories at repo root), and as a Claude Managed Agent template your platform team deploys behind your own workflow engine. **Same agent, same skills — pick your surface.** Each directory below is a deploy manifest that references the canonical system prompt and skills from the matching plugin, so there is one source of truth.

Run `../scripts/deploy-managed-agent.sh <slug>` to upload skills, create leaf workers, and `POST /v1/agents` with the resolved config. Each template ships with [`steering-examples.json`](./pitch-agent/steering-examples.json) and a per-agent README covering its security tier and handoffs.

| Agent | Vertical plugin | Cowork tile | CMA steering event | Leaf workers |
|---|---|---|---|---|
| [`pitch-agent`](./pitch-agent/) | investment-banking | Comps, precedents, LBO → branded pitch deck | `Build pitch book: <target> / <acquirer>, thesis: <text>` | researcher · modeler · **deck-writer** |
| [`market-researcher`](./market-researcher/) | equity-research | Sector or theme → overview, landscape, peer comps, ideas shortlist | `Primer: <sector or theme>, angle: <text>` | sector-reader · comps-spreader · **note-writer** |
| [`earnings-reviewer`](./earnings-reviewer/) | equity-research | Earnings call + filings → model update → note draft | `Process earnings: <ticker> <period>` | transcript-reader · model-updater · **note-writer** |
| [`meeting-prep-agent`](./meeting-prep-agent/) | wealth-management | Briefing pack before every client meeting | `Briefing pack for <client-id>, meeting <event-id>` | profiler · news-reader · **pack-writer** |
| [`model-builder`](./model-builder/) | financial-analysis | DCF, LBO, 3-statement, comps — as a file | `Build <dcf\|lbo\|3-stmt> for <ticker>, assumptions: {...}` | data-puller · **builder** · auditor |
| [`gl-reconciler`](./gl-reconciler/) | financial-analysis | Finds breaks, traces root cause, routes for sign-off | `Reconcile GL vs subledger, trade date <D>, classes: <list>` | reader · critic · **resolver** |
| [`kyc-screener`](./kyc-screener/) | financial-analysis | Parses onboarding docs, runs rules, flags gaps | `Screen onboarding packet <id>` | doc-reader · rules-engine · **escalator** |
| [`valuation-reviewer`](./valuation-reviewer/) | private-equity | Ingests GP packages, runs valuation, stages LP reporting | `Review portco valuations for fund <X> as of <date>` | package-reader · valuation-runner · **publisher** |
| [`month-end-closer`](./month-end-closer/) | financial-analysis | Accruals, roll-forwards, variance commentary | `Close <entity> for period <YYYY-MM>` | ledger-reader · rollforward · **poster** |
| [`statement-auditor`](./statement-auditor/) | private-equity | Audits LP statements before distribution | `Tie out statement batch <id> against <fund> NAV pack` | statement-reader · reconciler · **flagger** |

**Bold** leaf = the only worker with `Write`.

## Manifest vs API

The `agent.yaml` files use the real `POST /v1/agents` field names with a few conveniences the deploy script resolves:

| Manifest convention | Resolves to |
|---|---|
| `system: {file: ../../plugins/agent-plugins/<slug>/agents/<slug>.md, append: "..."}` | `system: "<inlined contents + append>"` |
| `system: {text: "..."}` | `system: "<text>"` |
| `skills: [{from_plugin: ../../plugins/agent-plugins/<slug>}]` | uploads every `skills/*` under that dir → `[{type: custom, skill_id: ...}, ...]` |
| `skills: [{path: ../../...}]` | `skills: [{type: custom, skill_id: <uploaded-id>}]` |
| `callable_agents: [{manifest: ./subagents/x.yaml}]` | `callable_agents: [{type: agent, id: <created-id>, version: latest}]` |

> **Research preview:** `callable_agents` (multi-agent delegation) supports **one delegation level**. An orchestrator can call workers; workers cannot call further subagents.

## Cross-agent handoffs

Named agents never call each other directly. When one agent needs another, it emits a `handoff_request` in its output; [`../scripts/orchestrate.py`](../scripts/orchestrate.py) (or your Temporal/Airflow/Guidewire event bus) routes it as a new steering event to the target session. The reference script hard-allowlists targets and schema-validates payloads — see its header comment for the threat model.
