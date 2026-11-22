# Source anchors: human-review-gates

This file holds the named, dated regulatory and professional-standard sources the human-review-gates skill anchors to. SKILL.md cites this file by path; the named anchors are not restated inline. Firm-specific anchors (named committees, GRC-platform decision-record fields, escalation ladders) belong in `references/firm-overlay.md`.

`[verify section]` placeholders mark anchors where the precise section reference still needs verification against the current edition of the source. They are deliberate, not omissions. Fabricating a section reference is worse than leaving the placeholder.

## Model-risk effective challenge

### SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (Federal Reserve and OCC, April 4, 2011, superseded April 17, 2026 by the joint guidance below)

Anchor: §V (validation, including the principle that validation is performed by staff with the authority and competence to challenge developers and is independent of the development function); §VI (governance, policies, and controls — board and senior management oversight, model risk management framework, internal audit). [verify section labels against the published letter; the interagency text uses Roman-numeral sections.]

What this skill relies on: that validation independence is a per-reviewer attribute the matrix captures; that effective challenge is the conceptual root of the human-review gate in model-risk workflows; that the gate matrix names the developer-validator separation explicitly; that board and senior-management oversight gates are part of the model-risk governance scaffolding rather than optional layers.

- §V — Model validation; independence of validators from developers. https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm
- §VI — Governance, policies, and controls. https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm

### Joint Interagency Revised Guidance on Model Risk Management — OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026 (April 17, 2026)

Anchor: Section II (scope and definitions), Section III (control environment, third-party model controls, independent challenge). The April 2026 joint guidance supersedes SR 11-7 (2011) and SR 21-8 (BSA/AML model risk, 2021). Most relevant to banking organizations with total assets over $30 billion; non-binding (does not set forth enforceable standards). Generative AI and agentic AI are explicitly out of scope (footnote 3); the principles cover traditional statistical and quantitative models and non-generative, non-agentic AI models. The bulletin contains zero references to NIST AI RMF, NIST AI 600-1, or any other NIST publication.

What this skill relies on: refreshed effective-challenge gate language for traditional and non-generative-AI models, third-party model gate framing where the model is vendor-developed or vendor-hosted, and the developer-validator separation expectations the joint guidance carries forward. For GenAI or agentic-AI gate architecture (human-in-the-loop, human-on-the-loop posture, prompt-injection escalation, agent-tool-action approval), the matrix anchors on NIST AI RMF 1.0, NIST AI 600-1, ISO/IEC 42001, the EU AI Act Article 14 human-oversight expectations, and the firm's AI governance policy rather than this bulletin.

Link: https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html (parallels: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm, https://www.fdic.gov/news/financial-institution-letters/2026/agencies-revise-interagency-model-risk-management-guidance)

## AI governance scaffolding

### NIST AI Risk Management Framework 1.0 (NIST AI 100-1, January 2023)

Anchor: Govern function categories. GV-1 (policies, processes, procedures), GV-2 (accountability structures), GV-3 (workforce diversity, equity, inclusion, accessibility), GV-4 (organizational practices on testing, performance, accuracy, transparency), GV-5 (engagement with relevant AI actors), GV-6 (third-party considerations). The framework is voluntary but heavily referenced in AI-governance committee charter language, NAIC AI Bulletin (2023), NYDFS AI Industry Letter (2024), and the Treasury AI Executive Order implementation guidance.

What this skill relies on: the Govern function categories as the named scaffolding for an enterprise-wide AI gate matrix (intake gate, tiering gate, deployment gate, ongoing-monitoring gate, retirement gate); the GV-2 accountability framing that aligns with named-role ownership in the matrix; the GV-6 third-party framing that connects AI gates to vendor-onboarding gates.

Link: https://www.nist.gov/itl/ai-risk-management-framework

### NIST AI 600-1 — Generative AI Profile (July 2024)

Anchor: Govern subcategories specific to generative AI; the profile adds gate-relevant material on model-card requirements, content provenance, and use-case approval for foundation-model-based deployments. [verify subcategory numbering against the current Profile edition.]

What this skill relies on: generative-AI-specific gate criteria where the scope flags GenAI use cases; the Profile's framing on use-case approval as a gated decision rather than a check-box.

Link: https://www.nist.gov/itl/ai-risk-management-framework

## EU AI Act human oversight

### Regulation (EU) 2024/1689 — Artificial Intelligence Act

Anchor: Article 14 (human oversight of high-risk AI systems — requirement that providers design systems for effective oversight by natural persons during the period of use, with measures appropriate to the risk and use context); Article 26 (deployer obligations of high-risk AI systems — assignment of human oversight to natural persons with the necessary competence, training, authority, and support); Article 27 (fundamental-rights impact assessment for certain deployers, which is itself a gated decision). The Act's high-risk classification triggers under Annex III drive most second-line gate work in EU-touching firms.

What this skill relies on: Article 14's specific framing that human oversight requires competence, authority, and resources, which the matrix captures as `independence_basis` and as the documentation requirement on the reviewer side; Article 26's deployer obligations that translate into named-reviewer expectations on use-case approval gates.

- Article 14 — Human oversight. https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- Article 26 — Obligations of deployers of high-risk AI systems.
- Article 27 — Fundamental-rights impact assessment.

## AI management system

### ISO/IEC 42001:2023 — AI Management Systems

Anchor: §5.3 (organizational roles, responsibilities, and authorities); §6.1.4 (AI risk assessment); §8.3 (AI system impact assessment); Annex A controls (notably A.2 policies for AI, A.6 AI system life cycle, A.10 third-party relationships). [verify section labels against the published standard.]

What this skill relies on: the AIMS-aligned governance gate documentation pattern when the firm has adopted or is moving toward ISO/IEC 42001 certification; the §8.3 impact assessment as a gate in its own right; the Annex A.10 third-party controls that connect AI gates to vendor-onboarding gates.

Link: https://www.iso.org/standard/81230.html

## Internal-audit governance

### IIA International Professional Practices Framework — Standards 2330 and 2410

Anchor: Standard 2330 (Documenting Information) — internal auditors document information sufficient to support engagement results and conclusions, with retention conventions specified; Standard 2410 (Criteria for Communicating) — engagement communications include objectives, scope, conclusions, recommendations, and action plans. The IIA released the Global Internal Audit Standards effective January 2025 which restate parts of the prior IPPF; specifically, the conclusions-and-recommendations communication convention now lives in Domain V Standard 13.x of the 2024 Standards. [verify current standard numbers; this skill carries both the prior 2410 framing and the 2024 Standards framing because firms use both during the transition window.]

What this skill relies on: the IIA framing that gate decisions are documented to a retention standard; the convention that committee gate decisions feed an audit-traceable record (the gate's documentation requirement on the matrix maps to Standard 2330 / 2024-Standards 13.x retention).

Link: https://www.theiia.org/en/standards/

### IIA Global Internal Audit Standards (effective January 2025)

Anchor: Domain V (Performing Internal Audit Services), specifically Standards 13.1 (Communicating Engagement Conclusions) and 13.2 (Engagement Communication). [verify current standard numbers; the 2024 release reorganised the prior 2410 series.]

What this skill relies on: continuity of the documentation-and-communication conventions into the 2024 Standards; explicit requirement that internal audit communications include criteria, conclusions, and recommendations, which informs how gate decisions are documented when internal audit is one of the reviewers.

Link: https://www.theiia.org/en/standards/2024-standards/

## Internal-control framework

### COSO Internal Control – Integrated Framework (May 2013)

Anchor: Component III (Control Activities) and Component V (Monitoring Activities); Principle 12 (deploys control activities through policies and procedures) and Principle 14 (selects and develops general controls over technology). [verify principle numbering against the current Framework edition.]

What this skill relies on: the COSO framing that gates are themselves a category of control activity, distinct from preventive, detective, and response controls; the convention that gate decisions are evidenced and the evidence is retained; the principle that gate design ties to policies and procedures, which lands in `references/firm-overlay.md` when the firm anchors on COSO.

Link: https://www.coso.org/internal-control

## OCC Heightened Standards (large-bank gate architecture)

### 12 CFR Part 30, Appendix D — OCC Heightened Standards for Large Insured National Banks

Anchor: Standards I–V on the risk governance framework, three-lines-of-defense, independent risk management, front-line-unit responsibilities, and the board's oversight responsibility. The Heightened Standards apply to covered banks at the OCC's asset-size population (currently $50B+ at the OCC's discretion subject to the rule's threshold framework). [verify exact appendix and standard labels; Part 30 Appendix D is the operative text.]

What this skill relies on: the Heightened Standards' explicit three-lines-of-defense architecture as the source for line-1 / line-2 / line-3 separation in the gate matrix; the board oversight standard that pulls gate-architecture artifacts into board-risk-committee adoption; the front-line-unit responsibility that aligns with the business-sponsor reviewer slot in many gates.

Link: https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20D%20to%20Part%2030

## Federal supervisory expectations on senior-management oversight

### Federal Reserve SR 16-11 — Supervisory Guidance for Assessing Risk Management at Supervised Institutions with Total Consolidated Assets Less Than $100 Billion

Anchor: Risk management framework expectations including senior management oversight of risk-taking and risk-control activities. [verify section labels against the SR letter; SR 16-11 uses unnamed paragraphs.]

What this skill relies on: continuity of senior-management-oversight expectations from SR 11-7 (model risk) into broader risk-management framework expectations, which informs the gate-architecture for non-model risk workflows at sub-$100B FRB-supervised institutions.

Link: https://www.federalreserve.gov/supervisionreg/srletters/sr1611.htm

## Third-party gate scaffolding (overlay)

### Interagency Guidance on Third-Party Relationships: Risk Management (OCC / FRB / FDIC, June 6, 2023)

Anchor: §III.A (planning), §III.B (due diligence and selection), §III.C (contract negotiation), §III.D (ongoing monitoring), §III.E (termination). Each lifecycle phase is itself a gated decision in vendor-onboarding gate matrices. [verify section labels against the published guidance; the lifecycle phases are named explicitly in the text.]

What this skill relies on: the lifecycle-phase framing as the spine of vendor-onboarding gate matrices; the criticality-decision gate that opens the lifecycle; the contract gate that requires legal and risk concurrence; the termination gate that requires evidenced exit-plan readiness.

Link: https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm

## Customer-impact gate scaffolding (overlay)

### CFPB Supervision and Examination Manual — Compliance Management System (current edition)

Anchor: The CMS chapter framing the four CMS pillars: board and management oversight, compliance program (policies and procedures, training, monitoring and corrective action), consumer complaint response, and compliance audit. [verify chapter and section labels against the current edition.]

What this skill relies on: the CMS pillar framing as the source for customer-facing gate architecture (product approval, fee-change approval, marketing approval, restitution approval); the convention that customer-impact decisions route through a CCO-led gate when the firm runs a CFPB-shaped CMS.

Link: https://www.consumerfinance.gov/compliance/supervision-examinations/

## Sector-specific and cross-cutting anchors

The sector-overlay files (`references/sector-overlays/<sector>.md`) enumerate sector-specific gate anchors (NAIC ORSA and Corporate Governance Annual Disclosure Model Act, FINRA 3110 supervisory gates, SEC Rule 206(4)-7 advisers compliance gates, OCC fintech bank-partnership sponsor-bank gates). The cross-cutting overlays (`references/cross-cutting/<topic>.md`) enumerate cross-cutting anchors (NYDFS Part 500 §500.4 senior-governing-body responsibility for cyber gates, SEC 8-K Item 1.05 disclosure-committee gates for materiality determination, CFPB UDAAP exam manual and ECOA second-look conventions for conduct gates). This file is the foundational set; the overlays add what the scope requires.

## Cross-plugin overlays (referenced when in scope)

- Model-risk gates cite SR 11-7 (historical) and the April 2026 joint guidance (current; OCC 2026-13 / SR 26-2 / FIL-15-2026) directly (anchors above).
- AI-system gates cite the NIST AI RMF, NIST AI 600-1, EU AI Act, and ISO/IEC 42001 (anchors above), plus sector-specific AI guidance via the relevant sector overlay (NAIC AI Bulletin, NYDFS AI Industry Letter).
- Third-party gates cite the Interagency Guidance and DORA Article 28 (the EU equivalent for ICT third-party relationships) where the firm's footprint is EU-touching; DORA anchors live with the third-party-operational-resilience plugin's source-anchors when present.
- Issue-rating gates cite the issue-writeup primitive's source anchors (FRB SR 13-13, OCC Bulletin 2014-39, IIA Standards) plus this skill's IIA and COSO anchors for the rating-decision-as-gate framing.
