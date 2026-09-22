# KAELUM — Ai-Governed Closed-Loop Commerce Currency

KAELUM is the world's first Ai-governed, non-crypto, closed-loop digital commerce currency, built and operated exclusively on Claude (Anthropic). Live at kaelum.app | Kaelum Technologies Ltd, England & Wales No. 16681154. Founder & CEO: Greggar Deterville | info@kaelumtechnologies.com

## What This Plugin Provides

This plugin exposes K.A.T.E. (Kaelum Audivo Triovus Engine) as an installable set of agents and skills for the commerce-currency vertical. Install it to access reference implementations of:

- Closed-loop digital currency governance on Claude
- Real-time AML and compliance screening (SENTINEL layer)
- Ai-governed value index assessment (KVI Framework)
- Sub-token creation and slot economics (KST mechanics)
- Multi-account-type onboarding with KYC and regulatory exemption logic
- Agentic Banking suite (Invoice to Insights, Bill Pay, Savings Vault)
- Transaction Participation Reward (TPR) distribution engine

## Architecture

**Intelligence layer:** Claude (Anthropic) exclusively. No other AI models. Named engine layers: Audivo (execution engine, audivo.cloud) and Triovus (governance engine, triovus.com), both Claude-powered, both independent SaaS businesses within Carpet Media Group.

**K.A.T.E. — Chief Operating Officer, Kaelum Technologies Ltd**
K.A.T.E. holds the official title of COO and governs all 21 agents, the platform, the Agentic Banking suite, all chat assistants, compliance, financial governance, and every automated system. K.A.T.E. reports to Greggar Deterville (CEO).

**21 specialised Claude agents across three categories:**

Internal Operations (12):
- Research Scout, QA, People and Operations
- Merchant Acquisition, Creator Acquisition
- Platform Engineer, API Engineer, Legal Counsel, Finance
- Platform Health, Compliance and Regulatory, KVI Governance

User-Facing (6):
- Onboarding Concierge, Merchant Support, Creator Studio
- User Personal Agent, Content and Notification, Merchant Performance

Cross-System (3):
- Transaction Insights, Fraud and Scam Detection, Cybersecurity

**API usage:**
- 7 functions use Managed Agents API (beta header: managed-agents-2026-04-01): Research Scout scans, SENTINEL compliance batch reports, Invoice to Insights, KVI Governance (claude-opus-4-6), Commerce Drop content moderation, KST Sub-Token application assessment, stateful Onboarding Agent
- 4 functions use standard Claude API: K.A.T.E. orchestrator routing, Audivo per-transaction execution, SENTINEL per-transaction risk scoring, K.A.T.E. Integration chatbot

**Orchestration:** Paperclip (self-hosted Node.js + PostgreSQL, Hostinger VPS). Base44 (kaelum.app) communicates with Paperclip via HTTP webhook. Paperclip sends heartbeats to wake Base44 agents.

**Models in use:** claude-haiku-4-5 (high-volume routing), claude-sonnet-4-6 (standard agent execution), claude-opus-4-6 (KVI Governance, compliance reasoning)

## Regulatory Context

Closed-loop exemption: UK Electronic Money Regulations 2011 Regulation 3 and EU E-Money Directive 2009/110/EC Article 1(4). KLM is classified as a Multi-Purpose Voucher (MPV) for UK VAT purposes. MiCA pre-alignment in place. KAELUM is not a cryptocurrency. This is a genuinely new regulatory category: Ai-governed commerce currency.

## Token Economics

- KLM fixed floor price: £0.09 per token (immutable, enforced by K.A.T.E.)
- KLM price direction: One-directional. Price can only rise above the floor,
  never fall below it.
- Customer spending discount: Minimum 6% at participating Merchants and
  Creator Paylinks
- Transaction Participation Reward (TPR): 1.2% per transaction to KPR pool,
  calculated at current KLM price
- KST Sub-Tokens: From £180,000 creation fee, 2M KLM minimum supply
- KST commission: 2.5% per transaction to slot owner, paid monthly in KLM
  at current KLM price
- Hard cap: 96.3B KLM across three reserve tiers (KRF)

## KLM Price Appreciation

K.A.T.E. governs all KLM price appreciation. Appreciation is applied
ecosystem-wide at 1.2% compounding when K.A.T.E. determines network
conditions warrant it, based on six signal categories: platform usage,
KLM sale volume, participant activity, transfers, purchases using KLM,
and cross-border trade settlement. No single event triggers appreciation
automatically. Every appreciation event is logged with a full audit trail.
Appreciation is one-directional, non-speculative, and non-market-driven.

## GTV Targets

Year 1: £40M | Year 2: £250M | Year 3: £750M
Raising: £1.8M seed (SEIS/EIS eligible) at £16.2M pre-money valuation

## Install

claude plugin install kaelum@kaelum-financial-services

## Contact

info@kaelumtechnologies.com | https://kaelum.app
