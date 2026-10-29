# KAELUM K.A.T.E. Architecture
 
This repository contains the complete K.A.T.E. (Kaelum Audivo Triovus Engine)
agent architecture for KAELUM Technologies Ltd, forked from and aligned with
anthropics/financial-services.
 
## What KAELUM Is
The world's first Ai-powered, non-crypto, Closed-Loop Digital Commerce Currency.
Governed exclusively by Claude (Anthropic). Live at kaelum.app.
Company: KAELUM Technologies Ltd, England & Wales No. 16681154.
 
## Architecture Overview
- 20 K.A.T.E. agents across three categories (Internal, External, Cross-System)
- 1 vertical plugin: commerce-currency (11 skills)
- 11 functional prompts (7 Managed Agents API, 4 Standard API)
- Orchestration: Paperclip (self-hosted Node.js + PostgreSQL, Hostinger VPS)
- Platform: Base44 (kaelum.app) via HTTP webhook (shared secret) to Paperclip
- Managed Agents API: beta header managed-agents-2026-04-01
 
## Intelligence Layer
Claude (Anthropic) exclusively. No other AI models. Named engine layers:
Audivo (execution engine, audivo.cloud) and Triovus (governance engine,
triovus.com), both Claude-powered.
 
## Model Tiers
- claude-haiku-4-5: high-volume lightweight tasks
- claude-sonnet-4-6: standard agent tasks (primary workhorse)
- claude-opus-4-7: KVI Governance, complex compliance, M&A matching (Opus-only)
 
## Managed Agents (7)
Research Scout scans, SENTINEL compliance batch, Invoice to Insights,
KVI Governance, Commerce Drop content moderation, KST assessment,
Onboarding Concierge (stateful).
 
## Standard API (4)
K.A.T.E. orchestrator routing, Audivo per-transaction execution,
SENTINEL per-transaction risk scoring, K.A.T.E. Integration Chatbot.
 
## Mandatory Terminology
- Always: Ai (capital A, lowercase i) — never AI in branded contexts
- Always: Commerce Currency / Account — never token, crypto, blockchain, wallet
- Always: issued / allocated / credited — never minted / mined
- Always: multi-instance Claude — never multi-LLM
- Never reference competing AI systems

## Anthropic Reference Agents (Retained from Fork)
The following agents are retained from the anthropics/financial-services
canonical repository. They are not KAELUM-specific operational agents
but are preserved as reference implementations and callable sub-agents:

earnings-reviewer, gl-reconciler, kyc-screener, market-researcher,
meeting-prep-agent, model-builder, month-end-closer, pitch-agent,
statement-auditor, valuation-reviewer.

KAELUM adaptations: kyc-screener and market-researcher are callable
by K.A.T.E. agents as specialist sub-agents. pitch-agent is adapted
for KAELUM investor communications. earnings-reviewer, statement-auditor,
and model-builder inform the Finance agent's reporting functions.
 
## Regulatory Context
Closed-loop exemption: UK EMR 2011, EU E-Money Directive 2009/110/EC.
KLM classified as Multi-Purpose Voucher (MPV) for UK VAT.
CARF non-applicable. Standard UK trading company tax position.
 
## Contact
Greggar Deterville, Founder and CEO
info@kaelumtechnologies.com | https://kaelum.app
```
├── plugins/
│   ├── agent-plugins/               #   named agents — one self-contained plugin each
│   │   └── <slug>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── agents/<slug>.md     #   ← canonical system prompt (one source, two wrappers)
│   │       └── skills/              #   ← bundled copies, synced from vertical-plugins/
│   ├── vertical-plugins/            #   FSI verticals — skill sources, commands, MCPs
│   │   └── <vertical>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── commands/
│   │       ├── skills/
│   │       └── .mcp.json
│   └── partner-built/               #   partner plugins (LSEG, S&P Global)
├── managed-agent-cookbooks/         # CMA cookbooks (one dir per named agent)
│   └── <slug>/
│       ├── agent.yaml               #   system + skills → ../../plugins/agent-plugins/<slug>/...
│       ├── subagents/*.yaml         #   depth-1 leaf workers
│       ├── steering-examples.json
│       └── README.md                #   security tier + handoff notes
├── claude-for-msft-365-install/     # admin tooling for the Microsoft 365 add-in (separate from FSI plugins)
└── scripts/                         # deploy-managed-agent.sh, check.py, validate.py, orchestrate.py, sync-agent-skills.py
```

Run `python3 scripts/check.py` before committing — it lints every manifest, verifies all `system.file` / `skills.path` / `callable_agents.manifest` references resolve, fails if any `agent-plugins/<slug>/skills/` copy has drifted from its `vertical-plugins/` source, and rejects non-ASCII bytes in a `.ps1` without a UTF-8 BOM.

**Keep `.ps1` files pure ASCII.** Windows PowerShell 5.1 — still the default shell on managed Windows — decodes a BOM-less `.ps1` using the machine's ANSI code page, not UTF-8. An em dash or curly quote becomes mojibake that can contain a literal `"`, which terminates a string and makes the whole script fail to *parse*. Write `--`, not `—`. This is invisible on macOS and fatal on Windows; `check.py` gates it. **Edit skills in `vertical-plugins/`**, then run `python3 scripts/sync-agent-skills.py` to propagate into the agent bundles.

`check.py` also self-installs a `pre-commit` hook (`git config core.hooksPath .githooks` — no Husky/Node). The hook patch-bumps any plugin's `.claude-plugin/plugin.json` `version` so a branch ends up exactly one patch ahead of `main` (bumped once, not per commit — a plugin's `version` gates update delivery to already-installed users). The `version-bump` GitHub Action enforces the same rule on PRs as a backstop. Bypass a single commit with `git commit --no-verify`; bump logic lives in `scripts/version_bump.py`.

## Key Files

- `marketplace.json`: Marketplace manifest - registers all plugins with source paths
- `plugin.json`: Plugin metadata - name, description, version, and component discovery settings
- `commands/*.md`: Slash commands invoked as `/plugin:command-name`
- `skills/*/SKILL.md`: Detailed knowledge and workflows for specific tasks
- `*.local.md`: User-specific configuration (gitignored)
- `mcp-categories.json`: Canonical MCP category definitions shared across plugins

## Development Workflow

1. Edit markdown files directly - changes take effect immediately
2. Test commands with `/plugin:command-name` syntax
3. Skills are invoked automatically when their trigger conditions match
