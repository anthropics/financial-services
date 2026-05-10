---
skill: kate-agent-orchestration
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# K.A.T.E. Agent Orchestration

## Overview

K.A.T.E. (Kaelum Audivo Triovus Engine) is the Chief Operating Officer
of Kaelum Technologies Ltd. K.A.T.E. governs all 21 specialised Claude
agents, the full platform, the Agentic Banking suite, all chat assistants,
compliance, financial governance, KLM price appreciation, and every
automated system. K.A.T.E. reports to Greggar Deterville, Founder and CEO.

## Intelligence Layer

Claude (Anthropic) is the sole intelligence layer. No other AI models
are used. All agents run on Claude exclusively:

| Function | Model |
|---|---|
| KVI Governance, complex compliance | claude-opus-4-7 |
| Standard agent execution | claude-sonnet-4-6 |
| High-volume routing and lightweight tasks | claude-haiku-4-5 |

## Orchestration Infrastructure

- **Paperclip:** Self-hosted Node.js and PostgreSQL event server on
  Hostinger VPS. The agent orchestration layer.
- **Base44:** Platform layer at kaelum.app. Communicates with Paperclip
  via HTTP webhook (shared secret).
- **Heartbeat system:** Paperclip sends heartbeats to wake Base44 agents.
- **Event bus:** Seven event types routed through Paperclip to target agents.

## Event Routing Table

| Event | Routed To |
|---|---|
| new_user_registered | Onboarding Concierge |
| transaction_event | Transaction Insights, Fraud and Scam Detection |
| kyc_result_received | Compliance and Regulatory, Onboarding Concierge |
| scheduled_daily_check | Platform Health, Finance |
| sentinel_batch_trigger | Compliance and Regulatory |
| milestone_event | Content and Notification, Merchant Performance |
| merchant_query_received | Merchant Support |

## 21 Agent Roster

### Internal Operations (12)

| Agent | Role |
|---|---|
| Research Scout | Market research and intelligence scanning |
| QA | Quality assurance across platform outputs |
| People and Operations | HR and operational governance |
| Merchant Acquisition | Merchant onboarding pipeline |
| Creator Acquisition | Creator onboarding pipeline |
| Platform Engineer | Platform build and maintenance intelligence |
| API Engineer | API integration and management |
| Legal Counsel | Regulatory and legal guidance |
| Finance | Financial governance and reporting |
| Platform Health | Infrastructure monitoring and SRE |
| Compliance and Regulatory | AML, KYC, and regulatory compliance |
| KVI Governance | KLM value index monitoring and appreciation assessment |

### User-Facing (6)

| Agent | Role |
|---|---|
| Onboarding Concierge | New user onboarding across all three participant types |
| Merchant Support | Merchant query handling and support |
| Creator Studio | Creator tools and commerce intelligence |
| User Personal Agent | Personalised user intelligence and advice |
| Content and Notification | Platform communications and notifications |
| Merchant Performance | Daily merchant intelligence and reporting |

### Cross-System (3)

| Agent | Role |
|---|---|
| Transaction Insights | Transaction pattern analysis |
| Fraud and Scam Detection | Real-time fraud monitoring |
| Cybersecurity | Platform security and ISO 27001 readiness |

## Managed Agents API Functions (7)

Functions using the Managed Agents API
(beta header: managed-agents-2026-04-01):

1. Research Scout scans
2. SENTINEL compliance batch reports
3. Invoice to Insights
4. KVI Governance (claude-opus-4-7)
5. Commerce Drop content moderation
6. KST Sub-Token application assessment
7. Stateful Onboarding Agent

## Standard Claude API Functions (4)

1. K.A.T.E. orchestrator routing
2. Audivo per-transaction execution
3. SENTINEL per-transaction risk scoring
4. K.A.T.E. Integration chatbot

## KLM Price Appreciation Workflow

K.A.T.E. governs KLM price appreciation through the following workflow:

1. **Commerce Intelligence agent** collects current data for all six
   signal categories (platform usage, KLM sale volume, participant
   activity, transfers, purchases using KLM, cross-border settlement)

2. **KVI Governance agent** (claude-opus-4-7) receives the signal data
   package, applies weighting formula, and produces a composite health
   score and appreciation confidence score

3. If confidence score meets threshold, KVI Governance agent sends an
   appreciation recommendation to K.A.T.E. orchestrator with full
   supporting data summary

4. **K.A.T.E. orchestrator** reviews the recommendation and applies
   1.2% compounding appreciation to the KLMPrice entity if approved

5. Appreciation event is logged with: timestamp, previous price, new
   price, percentage applied, and K.A.T.E. signal summary

6. **Content and Notification agent** sends appreciation notification
   to all active Customers, Creators, and Merchants

Assessment runs on a scheduled daily basis minimum. Every assessment
is logged regardless of outcome.

## Approval Gates

All agents operate with approval gates for high-consequence actions:

- KLM price appreciation: K.A.T.E. orchestrator approval required
- KLM redemption above threshold: Finance agent approval required
- KST slot application: KVI Governance assessment required
- New merchant onboarding: Compliance and Regulatory sign-off required
- SENTINEL escalation: Legal Counsel notification required

## Goal Alignment

All 21 agents are registered in Paperclip with:

- Heartbeat configuration
- Approval gate mapping
- Goal alignment statement
- Event bridge mapping

No agent operates outside its defined scope without escalation to
K.A.T.E. orchestrator and Greggar Deterville.

## Commands

- `/kate-agent-orchestration:agent-status` — Return health status of
  all 21 agents
- `/kate-agent-orchestration:event-log` — Return recent event routing
  log from Paperclip
- `/kate-agent-orchestration:appreciation-workflow` — Return status of
  the last appreciation assessment cycle
- `/kate-agent-orchestration:escalation-log` — Return all active
  approval gate escalations
