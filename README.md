# Claude for Financial Services

Reference agents, skills, and data connectors for the financial-services workflows we see most — investment banking, equity research, private equity, and wealth management.

Everything here is available **two ways from one source**: install it as a [Claude Cowork](https://claude.com/product/cowork) plugin, or deploy it through the [Claude Managed Agents API](https://docs.claude.com/en/api/managed-agents) behind your own workflow engine. Same system prompt, same skills — you choose where it runs.

> [!IMPORTANT]
> Nothing in this repository constitutes investment, legal, tax, or accounting advice. These agents draft analyst work product — models, memos, research notes, reconciliations — for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding; every output is staged for human sign-off. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your firm.

What's in the repo:

- **[Agents](#agents)** — named, end-to-end workflow agents (Pitch Agent, Market Researcher, GL Reconciler, …). Each ships as a Cowork plugin **and** as a [Claude Managed Agent template](./managed-agent-cookbooks) you deploy via `/v1/agents`.
- **[Vertical plugins](#vertical-plugins)** — the underlying skills, slash commands, and data connectors, bundled by FSI vertical. Install these on their own if you just want `/comps`, `/dcf`, `/earnings` and the connectors without a full agent.

## Agents

Each agent is named for the workflow it runs. They're starting points: install the ones that match your work, then tune the prompts, skills, and connectors to how your firm does it.

Each agent plugin is **self-contained** — it bundles the skills it uses, so installing the agent is all you need.

| Function | Agent | What it does |
|---|---|---|
| **Coverage & advisory** | **[Pitch Agent](./plugins/agent-plugins/pitch-agent)** | Comps, precedents, LBO → branded pitch deck, end to end |
| | **[Meeting Prep Agent](./plugins/agent-plugins/meeting-prep-agent)** | Briefing pack before every client meeting |
| **Research & modeling** | **[Market Researcher](./plugins/agent-plugins/market-researcher)** | Sector or theme → industry overview, competitive landscape, peer comps, ideas shortlist |
| | **[Earnings Reviewer](./plugins/agent-plugins/earnings-reviewer)** | Earnings call + filings → model update → note draft |
| | **[Model Builder](./plugins/agent-plugins/model-builder)** | DCF, LBO, 3-statement, comps — live in Excel |
| **Fund admin & finance ops** | **[Valuation Reviewer](./plugins/agent-plugins/valuation-reviewer)** | Ingests GP packages, runs valuation template, stages LP reporting |
| | **[GL Reconciler](./plugins/agent-plugins/gl-reconciler)** | Finds breaks, traces root cause, routes for sign-off |
| | **[Month-End Closer](./plugins/agent-plugins/month-end-closer)** | Accruals, roll-forwards, variance commentary |
| | **[Statement Auditor](./plugins/agent-plugins/statement-auditor)** | Audits LP statements before distribution |
| **Operations & onboarding** | **[KYC Screener](./plugins/agent-plugins/kyc-screener)** | Parses onboarding docs, runs the rules engine, flags gaps |

For Managed Agent deployment — `agent.yaml`, leaf-worker subagents, steering-event examples, and per-agent security notes — see **[managed-agent-cookbooks/](./managed-agent-cookbooks)**.

## Repository Layout

```
plugins/
  agent-plugins/               # Named agents — one self-contained plugin each
  vertical-plugins/            # Skill + command bundles by FSI vertical, plus MCP connectors
  partner-built/               # Partner-authored plugins (LSEG, S&P Global)
managed-agent-cookbooks/       # Claude Managed Agent cookbooks — one dir per agent
claude-for-msft-365-install/   # Admin tooling to provision the Claude Microsoft 365 add-in
scripts/                       # deploy-managed-agent.sh · check.py · validate.py · orchestrate.py · sync-agent-skills.py
```

## Getting Started

### Cowork

In Cowork, open **Settings → Plugins → Add plugin** and either:

- **Paste this repo URL** — `https://github.com/anthropics/financial-services` — then pick the agents and verticals you want from the marketplace list, or
- **Upload a zip** — zip any directory under `plugins/` (e.g. `plugins/agent-plugins/pitch-agent/`) and drop it in.

### Claude Code

```bash
# Add the marketplace
claude plugin marketplace add anthropics/financial-services

# Core skills + connectors (install first)
claude plugin install financial-analysis@claude-for-financial-services

# Named agents — pick the ones you want
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services

# Vertical skill bundles
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

Once installed, agents appear in Cowork dispatch, skills fire automatically when relevant, and slash commands are available in your session (`/comps`, `/dcf`, `/earnings`, `/ic-memo`, …).

### Claude Managed Agents

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

Each template under [`managed-agent-cookbooks/`](./managed-agent-cookbooks) references the same system prompt and skills as its plugin counterpart. The deploy script resolves file references, uploads skills, creates leaf-worker subagents, and POSTs the orchestrator to `/v1/agents`. See [`scripts/orchestrate.py`](./scripts/orchestrate.py) for a reference event loop that routes `handoff_request` events between agents via your own orchestration layer.

> **Research Preview:** subagent delegation (`callable_agents`) is a preview capability. See per-agent READMEs for security and handoff guidance.

## How It Fits Together

| | What it is | Where it lives |
|---|---|---|
| **Agents** | Self-contained plugins that own a workflow end to end — system prompt plus the skills it uses. Cowork and the Managed Agent wrapper both reference the same directory. | `plugins/agent-plugins/<slug>/` |
| **Skills** | Domain expertise, conventions, and step-by-step methods Claude draws on automatically when relevant. Authored once in the verticals; each agent bundles a synced copy of the ones it needs. | `plugins/vertical-plugins/<vertical>/skills/` (source) · `plugins/agent-plugins/<slug>/skills/` (bundled) |
| **Commands** | Slash actions you trigger explicitly (`/comps`, `/earnings`, `/ic-memo`). | `plugins/vertical-plugins/<vertical>/commands/` |
| **Connectors** | [MCP servers](https://modelcontextprotocol.io/) that wire Claude to your data — terminals, research platforms, document stores. | `plugins/vertical-plugins/financial-analysis/.mcp.json` |
| **Managed-agent wrappers** | `agent.yaml` + depth-1 subagents + steering examples for headless deployment. | `managed-agent-cookbooks/<slug>/` |

Everything is file-based — markdown and JSON, no build step.

## Vertical Plugins

Start with **financial-analysis** — it carries the shared modeling skills and all data connectors. Add verticals for the workflows you need.

| Plugin | What it adds |
|---|---|
| **[financial-analysis](./plugins/vertical-plugins/financial-analysis)** *(core)* | Comps, DCF, LBO, 3-statement, deck QC, Excel audit. All 11 data connectors. |
| **[investment-banking](./plugins/vertical-plugins/investment-banking)** | CIMs, teasers, process letters, buyer lists, merger models, deal tracking. |
| **[equity-research](./plugins/vertical-plugins/equity-research)** | Earnings notes, initiations, model updates, thesis and catalyst tracking. |
| **[private-equity](./plugins/vertical-plugins/private-equity)** | Sourcing, screening, diligence checklists, IC memos, portfolio monitoring. |
| **[wealth-management](./plugins/vertical-plugins/wealth-management)** | Client reviews, financial plans, rebalancing, reporting, TLH. |
| **[fund-admin](./plugins/vertical-plugins/fund-admin)** | GL recon, break tracing, accruals, roll-forwards, variance commentary, NAV tie-out. |
| **[operations](./plugins/vertical-plugins/operations)** | KYC document parsing and rules-grid evaluation. |
| **[lseg](./plugins/partner-built/lseg)** *(partner)* | Bond RV, swap curves, FX carry, options vol, macro-rates monitoring on LSEG data. |
| **[sp-global](./plugins/partner-built/spglobal)** *(partner)* | Tear sheets, earnings previews, funding digests on S&P Capital IQ. |

## MCP Integrations

All connectors are centralized in the **financial-analysis** core plugin and shared across the rest.

| Provider | URL |
|---|---|
| [Daloopa](https://www.daloopa.com/) | `https://mcp.daloopa.com/server/mcp` |
| [Morningstar](https://www.morningstar.com/) | `https://mcp.morningstar.com/mcp` |
| [S&P Global](https://www.spglobal.com/) | `https://kfinance.kensho.com/integrations/mcp` |
| [FactSet](https://www.factset.com/) | `https://mcp.factset.com/mcp` |
| [Moody's](https://www.moodys.com/) | `https://api.moodys.com/genai-ready-data/m1/mcp` |
| [MT Newswires](https://www.mtnewswires.com/) | `https://vast-mcp.blueskyapi.com/mtnewswires` |
| [Aiera](https://www.aiera.com/) | `https://mcp-pub.aiera.com` |
| [LSEG](https://www.lseg.com/) | `https://api.analytics.lseg.com/lfa/mcp` |
| [PitchBook](https://pitchbook.com/) | `https://premium.mcp.pitchbook.com/mcp` |
| [Chronograph](https://www.chronograph.pe/) | `https://ai.chronograph.pe/mcp` |
| [Egnyte](https://www.egnyte.com/) | `https://mcp-server.egnyte.com/mcp` |

> MCP access may require a subscription or API key from the provider.

## Claude for Microsoft 365 — Install Tooling

If your firm runs Claude inside Excel, PowerPoint, Word, and Outlook via the Microsoft 365 add-in, [`claude-for-msft-365-install/`](./claude-for-msft-365-install) is the admin tooling to provision it against **your own cloud** — Vertex AI, Bedrock, or an internal LLM gateway — instead of Anthropic's API.

It's a Claude Code plugin (not a Cowork plugin) that walks an IT admin through generating the customized add-in manifest, granting Azure admin consent, and writing per-user routing config via Microsoft Graph. Install with:

```bash
claude plugin install claude-for-msft-365-install@claude-for-financial-services
/claude-for-msft-365-install:setup
```

This is separate from the agents and vertical plugins above — it's the on-ramp that gets the add-in deployed in a tenant, after which the agents and skills here are what runs inside it.

## Making It Yours

These are reference templates — they get better when you tune them to how your firm works.

- **Swap connectors** — point `.mcp.json` at your data providers and internal systems.
- **Add firm context** — drop your terminology, processes, and formatting standards into skill files.
- **Bring your templates** — `/ppt-template` teaches Claude your branded PowerPoint layouts.
- **Adjust agent scope** — edit `agents/<slug>.md` to match how your team actually runs the workflow.
- **Add your own** — copy the structure for workflows we haven't covered.

## Skill & Command Reference

<details>
<summary><b>financial-analysis</b> — core modeling, Excel, deck QC</summary>

| Skill | Command | Description |
|---|---|---|
| comps-analysis | `/comps` | Comparable company analysis with trading multiples |
| dcf-model | `/dcf` | DCF valuation with WACC and sensitivity analysis |
| lbo-model | `/lbo` | Leveraged buyout model |
| 3-statement-model | `/3-statement-model` | Populate 3-statement financial model templates |
| audit-xls | `/debug-model` | Excel model audit — formula tracing, hardcode detection, balance checks |
| clean-data-xls | — | Normalize and clean tabular data in Excel |
| deck-refresh | — | Re-link and refresh embedded charts/tables across a deck |
| competitive-analysis | `/competitive-analysis` | Competitive landscape and market positioning |
| ib-check-deck | — | QC presentations for errors and consistency |
| pptx-author | — | Produce a `.pptx` file headlessly (Managed Agent mode) |
| xlsx-author | — | Produce a `.xlsx` file headlessly (Managed Agent mode) |
| ppt-template-creator | `/ppt-template` | Create reusable PPT template skills |
| skill-creator | — | Guide for creating new skills |

</details>

<details>
<summary><b>investment-banking</b> — deal materials and execution</summary>

| Skill | Command | Description |
|---|---|---|
| strip-profile | `/one-pager` | One-page company profiles for pitch books |
| pitch-deck | — | Populate pitch deck templates with data |
| datapack-builder | — | Build data packs from CIMs and filings |
| cim-builder | `/cim` | Draft Confidential Information Memorandums |
| teaser | `/teaser` | Anonymous one-page company teasers |
| buyer-list | `/buyer-list` | Strategic and financial buyer universe |
| merger-model | `/merger-model` | Accretion/dilution M&A analysis |
| process-letter | `/process-letter` | Bid instructions and process correspondence |
| deal-tracker | `/deal-tracker` | Track live deals, milestones, and action items |

</details>

<details>
<summary><b>equity-research</b> — coverage and publishing</summary>

| Skill | Command | Description |
|---|---|---|
| earnings-analysis | `/earnings` | Post-earnings quarterly update reports |
| earnings-preview | `/earnings-preview` | Pre-earnings scenario analysis and key metrics |
| initiating-coverage | `/initiate` | Institutional-quality initiation reports |
| model-update | `/model-update` | Update financial models with new data |
| morning-note | `/morning-note` | Morning meeting notes and trade ideas |
| sector-overview | `/sector` | Industry landscape and thematic reports |
| thesis-tracker | `/thesis` | Maintain and update investment theses |
| catalyst-calendar | `/catalysts` | Track upcoming catalysts across coverage |
| idea-generation | `/screen` | Stock screening and idea sourcing |

</details>

<details>
<summary><b>private-equity</b> — sourcing through portfolio ops</summary>

| Skill | Command | Description |
|---|---|---|
| deal-sourcing | `/source` | Discover companies, check CRM, draft founder outreach |
| deal-screening | `/screen-deal` | Quick pass/fail on inbound CIMs and teasers |
| dd-checklist | `/dd-checklist` | Diligence checklists by workstream |
| dd-meeting-prep | `/dd-prep` | Prep for management presentations and expert calls |
| unit-economics | `/unit-economics` | ARR cohorts, LTV/CAC, net retention, revenue quality |
| returns-analysis | `/returns` | IRR/MOIC sensitivity tables |
| ic-memo | `/ic-memo` | Investment committee memo drafting |
| portfolio-monitoring | `/portfolio` | Track portfolio company KPIs and variances |
| value-creation-plan | `/value-creation` | Post-close 100-day plans and EBITDA bridges |
| ai-readiness | `/ai-readiness` | Assess a portfolio company's AI readiness |

</details>

<details>
<summary><b>wealth-management</b> — advisor workflows</summary>

| Skill | Command | Description |
|---|---|---|
| client-review | `/client-review` | Prep for client meetings with performance and talking points |
| financial-plan | `/financial-plan` | Retirement, education, estate, and cash-flow projections |
| portfolio-rebalance | `/rebalance` | Allocation drift analysis and tax-aware rebalancing |
| client-report | `/client-report` | Client-facing performance reports |
| investment-proposal | `/proposal` | Proposals for prospective clients |
| tax-loss-harvesting | `/tlh` | Identify TLH opportunities and manage wash sales |

</details>

## Contributing

Everything here is markdown and YAML. Fork, edit, PR. For new content:

- New skill → add it under `plugins/vertical-plugins/<vertical>/skills/`, then run `python3 scripts/sync-agent-skills.py` to propagate to any agent that bundles it.
- New agent → `plugins/agent-plugins/<slug>/` (with `agents/<slug>.md` + `skills/`) and a matching `managed-agent-cookbooks/<slug>/`.
- Run `python3 scripts/check.py` before pushing — it lints every manifest, verifies all cross-file references resolve, and fails if any bundled skill has drifted from its vertical source.

## License

[Apache License 2.0](./LICENSE)
