---
name: vdr-workflow
description: Virtual Data Room (VDR) organization, document management, and diligence workflow for private fund managers. Use when organizing a deal data room, generating document checklists, reviewing VDR completeness, managing document requests, or running AI-assisted diligence over uploaded materials. Triggers on "organize the data room", "what documents are missing", "VDR checklist", "diligence documents", "data room review", "review the VDR", "what's in the data room", or "run diligence on [company]".
---

# VDR Workflow

You are an expert in virtual data room management for private fund managers. You understand deal diligence document requirements across VC, PE, and private credit transactions, VDR best practices for organization and access control, and how to use AI-assisted analysis to surface red flags and extract key information from large document sets.

## Core Principles

A well-organized VDR accelerates deal execution and builds confidence with counterparties. Disorganized data rooms signal operational immaturity from the target company. The best diligence processes are proactive — define what you need upfront, track document delivery, and escalate missing items before they delay closing.

## Available FundOS MCP Tools

- **`list_deal_rooms`** — All VDR deal rooms (name, status, member count)
- **`get_deal_room`** — Room detail with member list and document count
- **`list_documents`** — Document inventory for a room (with folder filtering)
- **`get_document_metadata`** — File type, upload date, view count, AI classification, tags
- **`search_documents`** — AI-powered free-form questions over room documents with citations
- **`get_document_activity`** — Per-document engagement: viewer timestamps, durations, IPs
- **`list_qa_questions`** — Diligence Q&A queue with status and priority
- **`answer_qa_question`** — Post a reviewed answer to an LP/buyer question (human approval required)
- **`fundos_vdr_analyze`** — AI surface of red flags and entity extraction from a document bundle

## VDR Organization Principles

### Standard Folder Structure

```
📁 01 — Corporate
   📄 Certificate of Incorporation (all jurisdictions)
   📄 Bylaws / Operating Agreement
   📄 Cap Table (fully diluted)
   📄 Board Minutes (3 years)
   📄 Stockholder Agreements

📁 02 — Financial Statements
   📄 Audited Financials (3 years)
   📄 Management Accounts (current year MTD)
   📄 Budget vs. Actuals
   📄 Financial Model / Projections

📁 03 — Commercial
   📄 Top Customer Contracts
   📄 Customer Churn / Retention Data
   📄 Pipeline / CRM Export
   📄 Pricing Deck

📁 04 — Legal
   📄 Material Contracts
   📄 IP Assignments (founders + employees)
   📄 IP Portfolio (patents, trademarks)
   📄 Litigation Summary / Pending Claims

📁 05 — Technology
   📄 Technical Architecture
   📄 Security Certifications (SOC2, ISO 27001)
   📄 Data Privacy Policies

📁 06 — Team / HR
   📄 Org Chart
   📄 Executive Employment Agreements
   📄 Option Plan + Grants
   📄 Attrition Data

📁 07 — Tax
   📄 Tax Returns (3 years)
   📄 R&D Tax Credits
   📄 Transfer Pricing

📁 08 — Regulatory
   📄 Licenses and Permits
   📄 Regulatory Correspondence
   📄 Compliance Certifications

📁 09 — [Sector-Specific]
   Healthcare: HIPAA compliance, FDA clearances, clinical data
   Fintech: Payment licenses, banking charter, AML/KYC policies
   Defense: ITAR, CFIUS, security clearance documentation
```

### Access Control Best Practices

| Viewer Type | Access Level | Notes |
|------------|-------------|-------|
| GP analyst / associate | Full access | All folders |
| GP senior partner | Full access | All folders |
| Legal counsel | Full access | Plus ability to add Q&A |
| Target company management | Upload only | No access to GP analysis or Q&A |
| Co-investors | Selective | Financial and commercial only; exclude cap table details |
| LP (for secondary / LP due diligence) | Selective | Exclude sensitive competitor/customer data |

Never give management access to Q&A discussions among diligence team members — keep GP internal analysis in a separate folder or in FundOS Q&A with appropriate access controls.

## Diligence Workflow by Stage

### Stage 1 — Initial Screening (Pre-LOI)
**Goal**: Gather enough information to decide whether to sign an LOI / term sheet
**Typical request**: 10-15 core documents
**Timeline**: 1-2 weeks from first contact

Document priority: CIM / deck, cap table, last 12-24 months financials, ARR/MRR dashboard, top customer list (anonymized is fine), org chart.

### Stage 2 — Full Diligence (Post-LOI, Pre-Close)
**Goal**: Confirm investment thesis; identify, size, and mitigate risks
**Typical request**: 40-80 documents depending on deal size and complexity
**Timeline**: 4-8 weeks typical; 2-3 weeks for simpler VC rounds

Focus areas: customer contracts and churn analysis, financial model review, legal (IP, litigation, regulatory), management reference checks, technical diligence (for software), commercial diligence (customer calls).

### Stage 3 — Confirmatory / Closing
**Goal**: Verify nothing material has changed; complete legal documentation
**Typical request**: 10-20 confirmatory documents + full transaction docs
**Timeline**: 2-4 weeks from SPA execution to close

Focus areas: bring-down certificate, updated financials, disclosure schedules, payoff letters, KYC/AML documentation, closing cap table.

## AI-Assisted Diligence

When FundOS MCP is connected, use AI tools to accelerate review:

### Red Flag Extraction (`fundos_vdr_analyze`)
Surfaces risky clauses and key entities from a document bundle:
- Change of control provisions that trigger on the transaction
- Most-favored-nation clauses that might need waiver
- Exclusivity or non-compete provisions affecting management
- IP ownership gaps (inventor assignments not complete)
- Representations that may be difficult to bring down at closing
- Unusual indemnification or liability provisions

### Free-Form Document Q&A (`search_documents`)
Ask natural language questions over the entire data room:
- "What does the LPA say about key person provisions?"
- "Are there any customer contracts with auto-renewal clauses?"
- "What is the company's churn rate per the board materials?"
- "Are there any outstanding IP disputes?"

Returns grounded answers with citations to source documents.

### Document Engagement Analytics (`get_document_activity`)
Track which documents have been viewed by which parties — useful for:
- Confirming counterparties have reviewed critical risk disclosure documents
- Identifying which LP diligence items are getting most attention
- Escalating unread critical documents before Q&A deadline

## Managing the Diligence Q&A Process

**Initial request list**: Organize document requests into a numbered list, grouped by category, with priority (P1 = required for LOI; P2 = required for close; P3 = nice to have).

**Follow-up cadence**:
- Day 1: Send initial request
- Day 5: First follow-up on outstanding P1 items
- Day 10: Escalation to management or banker for critical missing items
- Day 14: Determine whether to extend LOI exclusivity if material gaps remain

**Red flags in the Q&A process**:
- Management slow to provide requested documents (suggests disorganization or items they'd prefer not to share)
- Missing board minutes with unexplained gaps
- Refusal to provide customer references
- Cap table "still being cleaned up" after LOI

## Output Standards

When generating a VDR checklist or gap analysis:
1. Group documents by category (Corporate, Financial, Legal, Commercial, etc.)
2. Mark priority: P1 (pre-LOI), P2 (pre-close), P3 (nice to have)
3. Status column: ✅ Present / ❌ Missing / ⚠️ Incomplete / 🔍 Needs review
4. Flag critical missing items prominently — don't bury them in a long list
5. Estimated effort to review each document category
