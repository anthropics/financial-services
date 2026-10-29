# Conduct cross-cutting overlay — human-review-gates

Loads when the scope `cross_cutting_overlay_set` includes `conduct`. The overlay shapes the gate matrix when gates cover customer-facing decisions: product approval, fee-change approval, marketing approval, restitution approval, fair-lending second-look on adverse action, sales-practice supervision, and complaint-handling escalation.

## Why conduct belongs in customer-facing gate matrices

Customer-impact decisions carry distinct supervisory expectations: the CFPB UDAAP exam manual frames the unfair, deceptive, or abusive lens; ECOA frames the second-review-of-adverse-action lens; FINRA's Rule 2111 (suitability) and Reg BI (Regulation Best Interest) frame the broker-dealer customer-impact lens; state DOI conduct-of-business regulation frames the insurance-claims-and-sales lens. A gate matrix that treats customer-facing decisions as administrative misses the substantive criteria that examiners will probe and the restitution-eligibility analysis that often follows from a gate failure.

## Source basis

- **CFPB Supervision and Examination Manual — UDAAP**. The CFPB's UDAAP analytical framework is the reference for "unfair", "deceptive", and "abusive" determinations on consumer-facing acts and practices. The framework's three-prong tests (substantial injury, not reasonably avoidable, not outweighed by countervailing benefits — for unfairness; representations, omissions, and practices that mislead, materially — for deception; specific abusive criteria) are the named criteria for UDAAP risk-review gates.
- **CFPB Supervision and Examination Manual — Compliance Management System (CMS)**. The CMS chapter framing the four CMS pillars: board and management oversight, compliance program, consumer complaint response, and compliance audit. The CMS framework anchors the customer-facing decision-authority structure (CCO function as the named gate-decision-holder for many customer-impact decisions).
- **Equal Credit Opportunity Act (ECOA) and Reg B (12 CFR Part 1002)**. ECOA's anti-discrimination requirements and Reg B's adverse-action notice and second-review provisions. §1002.6 (rules concerning evaluation of applications) and §1002.9 (notifications) are the primary anchors for fair-lending second-review gates.
- **Truth in Lending Act (TILA) and Reg Z (12 CFR Part 1026)**. Disclosure requirements and ability-to-repay determinations for covered loans; named gates on disclosure-review and ability-to-repay decisions.
- **Real Estate Settlement Procedures Act (RESPA) and Reg X (12 CFR Part 1024)**. Loan-servicing customer-impact decisions including loss-mitigation and default management.
- **FINRA Rule 2111 — Suitability** and **Regulation Best Interest (17 CFR §240.15l-1)**. Broker-dealer customer-impact framework; named gates on customer-suitability assessment and Reg BI compliance.
- **NYDFS Section 200 fair access regulations and other state DFS conduct rules** (varies). State-specific conduct rules layered onto federal expectations.
- **NAIC Unfair Trade Practices Act and state DOI claims-handling regulations**. Insurance-claims and sales conduct framework; gates on claims-decision review and policyholder-complaint escalation.
- **CFPB Circulars** (when issued). Specific interpretive circulars frame named-conduct gates; firms typically refresh gate matrices in response to material circulars (e.g., Circular 2022-03 on adverse action notice provisions for AI-driven credit decisions).

## What the overlay adds to the matrix

### Decision authority — CCO function

For consumer-finance firms anchored on the CFPB's CMS framework, the Chief Compliance Officer (or equivalent role under the CMS structure) is the named decision-authority for customer-impact gates. The matrix's decision-authority block names:
- The CCO as the operational decision-holder for product approval, fee-change approval, marketing approval, and restitution-decision gates.
- The compliance committee or consumer compliance committee as the standing committee body where named gates fire.
- The board (typically through a board compliance committee, audit committee, or consumer-products committee where the firm has one) as the oversight body for material customer-impact gate decisions.

For broker-dealers, the named decision-authority shifts to the supervisory principal under FINRA Rule 3110 plus the CCO under SEC Rule 206(4)-7 (for dual-registrants). For insurers, the decision-authority shifts to the named claims-handling officer (per state DOI requirements) and the named market-conduct officer.

### Product-approval gate

A product-approval gate for a consumer financial product names:
- **Trigger**: introduction of a new product, material change to an existing product, or extension of a product to a new customer segment or geography.
- **Required reviewers**: business sponsor (line 1), CCO (line 2), CRO (line 2), General Counsel, fair-lending officer, BSA Officer (when AML-relevant), CISO (when cyber-relevant), and (for sponsor-bank arrangements) the partner-fintech lead.
- **Decision criteria**: UDAAP risk assessment (substantial injury, reasonable avoidability, countervailing benefits); fair-lending impact assessment under ECOA; disclosure adequacy under TILA / RESPA; suitability framework under Rule 2111 / Reg BI for broker-dealer products; complaint-handling readiness; restitution-readiness for likely-error scenarios.
- **Stop conditions**: no go-live if the UDAAP risk assessment surfaces unmitigated risks; no go-live if the fair-lending impact analysis is incomplete; no go-live if disclosures are not finalized and reviewed by counsel; no go-live for AI-driven decisions if the adverse-action-notice framework is not validated against Reg B §1002.9 and Comment 9(b)(2)-3 of the Official Staff Commentary.
- **Documentation requirement**: product approval memorandum, UDAAP risk assessment, fair-lending impact analysis, disclosure review record, suitability/Reg BI documentation (where applicable), CCO sign-off log.

### Fee-change and marketing-change gates

Fee-change approval gates and marketing-change approval gates carry the same scaffolding as product approval but at lighter weight, with the CCO function as the named decision-holder. The decision criteria typically address: UDAAP risk on the change, customer-disclosure adequacy, fair-lending impact (where the change affects customer segments differently), and consumer-complaint-handling readiness. Stop conditions address: material UDAAP risk; missing disclosures; potential disparate impact under ECOA without supporting analysis.

### Fair-lending second-review gate

For credit decisions, ECOA and Reg B frame the second-review-of-adverse-action expectation. Some firms run a structured second-review program where adverse-action decisions on protected-class applicants flow through a second reviewer before final decision; the gate is named, the second reviewer is independent of the original decision, and the documentation requirement names the second-review log. Reg B §1002.9 and Comment 9(b)(2)-3 of the Official Staff Commentary (for AI-driven credit decisions) require that adverse-action notices be specific and accurate; the gate's decision criteria address notice-quality independent of the second-review-of-decision question.

### Restitution-decision gate

Where a consumer-impact issue surfaces (compliance-testing exception, complaint-pattern, regulatory finding), the restitution-decision is itself a gate. The matrix names: the trigger (issue confirmed with customer-population scope); the required reviewers (CCO, General Counsel, finance, business sponsor, board committee for material restitutions); the decision criteria (population scope, harm calculation, restitution methodology, communications-and-disbursement plan); the stop conditions (no execution if population scope is unsupported; no execution if methodology has not been reviewed by an independent reviewer); the documentation requirement (restitution memorandum, board approval where material, third-party-administrator scope-of-work where applicable).

### Complaint-pattern escalation gate

Consumer complaints, in the aggregate, are a leading indicator of customer-impact issues. The CMS framework expects firms to monitor complaint patterns and escalate material patterns to compliance or risk committees. The matrix names the complaint-pattern escalation gate: the trigger (complaint-volume threshold, root-cause-pattern threshold, regulator-inquiry trigger); the required reviewers (CCO, head of complaints function, business owner of the affected product); the decision criteria (whether the pattern reflects a substantive issue, requires product or process change, requires restitution analysis); the documentation requirement (escalation memorandum, complaint-pattern analysis, root-cause analysis).

### Insurance claims-handling gate

For insurers, state DOI claims-handling regulations frame named gates on disputed-claim escalation, claim-denial review, and material-loss-reserve-change decisions. The decision authority typically routes through the chief claims officer with claims committee oversight; the documentation requirement names the claim file and the claims committee minutes.

## Common patterns

- **Marketing approval treated as creative-review only**. Marketing approval often runs through marketing and legal but skips the CCO function. For consumer financial products, the CFPB treats marketing as a UDAAP risk surface; the matrix elevates marketing approval to a CCO-named gate.
- **Fair-lending second-review delegated to underwriting**. The second-review on adverse-action decisions is sometimes delegated within the underwriting function; this fails the independence test under ECOA second-review framing. The matrix flags the conflict and recommends an independent second-reviewer slot.
- **Restitution treated as operational reconciliation**. Restitution decisions sometimes run through finance and operations without committee oversight; the matrix elevates material restitutions to a board-committee-adopted decision with the methodology and population-scope independently reviewed.
- **Reg BI and FINRA suitability treated as separate gates with conflicting criteria**. For dual-registrant firms, Reg BI and FINRA Rule 2111 set parallel customer-impact frameworks with overlapping but distinct criteria. The matrix harmonizes the two with named decision criteria that satisfy both.
- **CFPB circular gap**. Firms sometimes delay refreshing gate criteria in response to material CFPB circulars; the matrix's gap section flags the unaddressed circulars and recommends specific gate-criteria updates.

## Anchors used by this overlay

- CFPB Supervision and Examination Manual — UDAAP module. https://www.consumerfinance.gov/compliance/supervision-examinations/
- CFPB Supervision and Examination Manual — Compliance Management System module. https://www.consumerfinance.gov/compliance/supervision-examinations/
- 15 USC §1691 et seq. — Equal Credit Opportunity Act. https://www.consumerfinance.gov/rules-policy/regulations/1002/
- 12 CFR Part 1002 — Reg B (ECOA implementing regulation), §1002.6 evaluation of applications, §1002.9 notifications. https://www.ecfr.gov/current/title-12/chapter-X/part-1002
- 12 CFR Part 1026 — Reg Z (TILA implementing regulation). https://www.ecfr.gov/current/title-12/chapter-X/part-1026
- 12 CFR Part 1024 — Reg X (RESPA implementing regulation). https://www.ecfr.gov/current/title-12/chapter-X/part-1024
- FINRA Rule 2111 — Suitability. https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111
- 17 CFR §240.15l-1 — Regulation Best Interest. https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.15l-1
- CFPB Circular 2022-03 — Adverse Action Notification Requirements in Connection with Credit Decisions Based on Complex Algorithms. **Withdrawn May 12, 2025; historical only.** Reg B §1002.9 and Comment 9(b)(2)-3 of the Official Staff Commentary continue to apply on their own terms. https://www.consumerfinance.gov/compliance/circulars/circular-2022-03/
- NAIC Unfair Trade Practices Act (MDL-880) and state DOI claims-handling regulations. https://content.naic.org/sites/default/files/MO880.pdf
- State market-conduct regulations — vary by state; firm-overlay names the state-specific rules that apply.
