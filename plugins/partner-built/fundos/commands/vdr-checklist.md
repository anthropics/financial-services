---
description: Generate a VDR document checklist for a deal at a given diligence stage
argument-hint: "[deal name and stage, e.g. 'Acme Corp full diligence' or 'Series B closing']"
---

# VDR Checklist

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Generate the standard Virtual Data Room (VDR) document checklist for a deal at a specific diligence stage. If the user provides their current VDR index, flag missing documents and categorize items by priority.

See the **vdr-workflow** skill for domain knowledge on VDR organization, document standards, and diligence best practices.

## Workflow

### 1. Gather Inputs

Ask the user for:

- **Deal name** — company or transaction name
- **Deal type** — VC investment, PE buyout, private credit, co-investment, LP commitment
- **Diligence stage**:
  - `initial` — first look, pre-LOI (20-30 core documents)
  - `full` — post-LOI, full diligence (60-80 documents)
  - `closing` — final confirmatory diligence and signing docs (30-40 documents)
- **Sector** — optional, for sector-specific additions (e.g. healthcare adds HIPAA/FDA; fintech adds licenses)
- **Current VDR index** — optional, paste the file list to flag what's present vs. missing

If FundOS MCP is connected, call `list_documents` for the deal's room to automatically check document coverage.

### 2. Generate Stage-Appropriate Checklist

#### Initial Diligence Checklist (Pre-LOI)

**Corporate & Legal**
- [ ] Certificate of Incorporation / Articles of Organization
- [ ] Cap table (fully diluted, including option pool, warrants, convertible notes/SAFEs)
- [ ] Summary of outstanding convertible instruments (SAFEs, notes, warrants) with terms
- [ ] Board composition and observer rights summary

**Financials**
- [ ] Last 3 years audited financial statements (or reviewed if pre-audit)
- [ ] YTD management accounts (P&L, balance sheet, cash flow)
- [ ] Current month management pack
- [ ] ARR / MRR dashboard (for SaaS/subscription businesses)

**Business Overview**
- [ ] Investor deck / CIM / teaser
- [ ] Product demo or product overview document
- [ ] Customer list (top 10-20 by revenue, anonymized if needed)
- [ ] Org chart

#### Full Diligence Checklist (Post-LOI)

**Corporate & Legal**
- [ ] Certificate of Incorporation (all jurisdictions)
- [ ] Bylaws / Operating Agreement
- [ ] All amendments to charter documents
- [ ] Capitalization table — fully diluted with all instrument details
- [ ] Stockholder agreements, voting agreements, rights of first refusal
- [ ] Board minutes (last 3 years) and consents
- [ ] Material contracts list (with counterparty and expiry)
- [ ] Top 10 customer contracts
- [ ] Top 10 vendor / supplier contracts
- [ ] Office and facility leases
- [ ] IP assignment agreements (founders and all employees)
- [ ] IP portfolio — patents, trademarks, copyrights, trade secrets
- [ ] Pending / threatened litigation summary
- [ ] Regulatory licenses and permits

**Financials**
- [ ] Audited financials — 3 years (P&L, balance sheet, cash flow, notes)
- [ ] Management accounts — monthly, last 12-24 months
- [ ] Budget vs. actuals — current year
- [ ] Financial model — 3-5 year projections with assumptions
- [ ] Revenue schedule — by customer, product, geography
- [ ] Deferred revenue schedule
- [ ] Accounts receivable aging
- [ ] Accounts payable aging
- [ ] Debt schedule (all outstanding debt with terms, maturity, covenants)
- [ ] Cap table with waterfall at various exit prices

**Commercial / Go-to-Market**
- [ ] Customer contracts (top 20 by ARR or revenue)
- [ ] Customer churn data (monthly / quarterly)
- [ ] NPS / customer satisfaction scores
- [ ] Sales pipeline CRM export
- [ ] Marketing and growth strategy document
- [ ] Competitive landscape analysis

**Technology / Product**
- [ ] Product roadmap
- [ ] Technical architecture overview
- [ ] Security policies and certifications (SOC2, ISO27001, etc.)
- [ ] Data privacy policy and compliance status (GDPR, CCPA)
- [ ] Third-party software licenses and dependencies
- [ ] Source code repository access (if technology diligence)

**Team / HR**
- [ ] Org chart with headcount by department
- [ ] Executive employment agreements (CEO, CFO, CTO, key person clauses)
- [ ] Option plan and grant agreements for key employees
- [ ] Compensation benchmarking / salary bands
- [ ] Attrition data (last 12 months)
- [ ] Benefits summary

**Tax**
- [ ] Last 3 years filed tax returns (federal, state)
- [ ] R&D tax credit documentation (if applicable)
- [ ] Transfer pricing documentation (if international operations)
- [ ] Outstanding tax disputes or audits

#### Closing Checklist (Confirmatory / Signing)

**Transaction Documents**
- [ ] Definitive agreement (SPA, SHA, or term sheet upgrade)
- [ ] Disclosure schedules (all exceptions to reps and warranties)
- [ ] Certificate of incorporation (current, post-closing pro forma)
- [ ] Closing cap table (post-transaction, fully diluted)
- [ ] Board resolutions authorizing the transaction
- [ ] Stockholder consents / written approval

**Confirmatory Diligence**
- [ ] Updated financials through most recent month
- [ ] Officer's certificate (bring-down of reps and warranties)
- [ ] Good standing certificates (all jurisdictions)
- [ ] Payoff letters (if existing debt being retired at close)
- [ ] Release letters (liens, pledges, encumbrances)
- [ ] KYC/AML documentation for investors and key principals
- [ ] OFAC and sanctions screening results

**Post-Closing**
- [ ] Issued stock certificates or unit ledger entries
- [ ] Updated cap table (post-close)
- [ ] Executed final agreements (fully signed copies)
- [ ] Wire instructions confirmed

### 3. Gap Analysis (if VDR index provided)

Match the checklist against the provided VDR index:

| Document | Required | In VDR | Status |
|----------|---------|--------|--------|
| Cap Table (fully diluted) | ✓ | ✓ | ✅ Present |
| Audited Financials | ✓ | ✗ | ❌ Missing |
| Customer Contracts | ✓ | Partial | ⚠️ Incomplete |

Highlight: **Missing critical items**, **present items**, **items flagged for review**.

### 4. Output

Return:
1. **Stage-appropriate checklist** — formatted with checkboxes, organized by category
2. **Gap analysis table** — if VDR index provided (present / missing / incomplete per item)
3. **Priority items** — top 5 most critical missing documents to request first
4. **Sector-specific additions** — any items added based on company sector

## Important Notes

- Closing checklists are legal documents — the definitive agreement's closing conditions control, not this checklist
- KYC/AML documents are mandatory in most jurisdictions before any funds transfer — never waive without legal sign-off
- Missing board minutes is a common red flag — probe if there are significant gaps in the minutes history
- Cap table issues (missing options, unissued SAFEs, unclear anti-dilution provisions) are frequent deal killers — prioritize cap table review above almost everything else
- For venture investments in regulated sectors (healthcare, fintech, defense), add sector-specific regulatory documents and flag for specialist counsel
