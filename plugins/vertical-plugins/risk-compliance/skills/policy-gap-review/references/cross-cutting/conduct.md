# Conduct cross-cutting overlay — policy-gap-review

Loads when the scope `cross_cutting_overlay_set` includes `conduct`. Binds the matrix to conduct-and-customer-facing-policy expectations when the policy in scope is a customer-facing policy: product approval, marketing review, complaints handling, fair lending, sales practice, fee design, or any policy whose operationalisation directly affects customers.

## Why conduct loads

Customer-facing policies are the policies whose gaps get litigated, enforced, and surfaced in news cycles. The CFPB UDAAP standard applies at the policy-design level — a policy that produces unfair, deceptive, or abusive outcomes is itself UDAAP-deficient even when individual transactions are facially compliant. Fair-lending statutes (ECOA, FHA, HMDA-anchored disparate-impact theories) impose policy-level expectations beyond the transaction-level rules. Conduct findings drive larger remediation (customer restitution, monetary penalty, public consent order) than back-office findings; the gap matrix takes conduct seriously.

## Source basis

### CFPB UDAAP framework

- **CFPB UDAAP Examination Manual** (current edition). The chapter-level expectations on policies governing consumer-facing decisions, marketing review, fee disclosure, complaint response, and product approval. The unfair-deceptive-abusive standard applies at the policy-design level.
- **CFPB Bulletins and Circulars** that announce UDAAP positions on specific practices. Bulletin 2017-01 (auto loans), Bulletin 2018-01 (Hsbc consent on credit reporting), Circular 2022-02 (deceptive representations in mortgage marketing), Circular 2022-03 (adverse action notices for AI/algorithmic decisioning), Circular 2024-04 and successors. The matrix references the circulars in force at the engagement's effective date.
- **Dodd-Frank §1031 / §1036** — the statutory UDAAP authority that supplements FTC Act §5 unfair-deceptive standard for CFPB-jurisdictional providers.

### Fair-lending statutes

- **ECOA / Reg B** — 12 CFR Part 1002. §1002.4 prohibition against discrimination on prohibited bases; §1002.6 evaluation of applications; §1002.9 adverse-action notice; Subpart B for §1071 small-business data collection (phase-in).
- **Fair Housing Act** — 42 USC §3601 et seq.; HUD's Discriminatory Effects rule (24 CFR Part 100, post-2023 reinstatement).
- **HMDA / Reg C** — 12 CFR Part 1003 — for fair-lending data accuracy and reporting policy expectations.
- **Disparate-impact theories** — recognised by the Supreme Court in Texas Department of Housing and Community Affairs v. Inclusive Communities Project (2015) under FHA; ECOA disparate-impact recognised by the federal banking agencies in interagency guidance.

### Complaint-handling expectations

- **CFPB Compliance Management System guidance** — the consumer-complaint-response pillar.
- **OCC Bulletin 2020-94 / 2021-31** — bank complaint-handling expectations under the OCC's Consumer Compliance examination procedures.
- **State complaint-handling requirements** — state-by-state, e.g., NYDFS Insurance Regulation 64 Part 216.

### Sales-practice and product-approval expectations

- **OCC Bulletin 2014-37** — Consumer Compliance: Bank Subjects.
- **FRB Consumer Compliance handbook** — current edition.
- **Sector-specific sales-practice rules** — Reg DD (deposits), Reg Z (credit-card account-opening disclosures), Reg E (prepaid disclosures), insurance suitability rules, broker-dealer best-interest rules (Reg BI under SEC Rule 15l-1).

### Marketing-review expectations

- **CFPB UDAAP** — for any consumer-facing marketing.
- **Reg N** — 12 CFR Part 1014, the Mortgage Acts and Practices Rule.
- **Reg Z marketing rules** — for credit-card and HELOC marketing.
- **State consumer-protection acts** — including UDAP statutes that often parallel FTC Act §5 with state-specific extensions.
- **SEC Marketing Rule** (Rule 206(4)-1) — for adviser marketing where the policy in scope governs adviser-side marketing.
- **FINRA Rule 2210** — for broker-dealer communications with the public.

### Fee-design and product-pricing

- **CFPB junk-fees focus** — circulars and bulletins addressing overdraft fees, NSF fees, surprise fees, return-deposited-item fees. The matrix references the circulars in force at the engagement's effective date.
- **Reg Z late-fee rules** — including the 2024 final rule on credit-card late fees (status subject to ongoing litigation; the matrix references the rule in force at the engagement's effective date).
- **Reg DD overdraft disclosure** — including the post-2010 Reg E §1005.17 opt-in for ATM and one-time debit overdraft.

## Gap patterns the conduct overlay flags

### UDAAP-design gaps

- Product-approval policies that lack a UDAAP review step before launch. Frequent gap site for fintech product policies and bank-fintech-program policies.
- Marketing-review policies that do not require UDAAP review of marketing materials, scripts, or social-media content.
- Fee-design policies that allow fee structures the CFPB has flagged as junk-fee-adjacent without an articulated business-justification framework.
- Complaint-handling policies that do not surface UDAAP-implicating complaint patterns to the policy-owner level for remediation.

### Fair-lending policy gaps

- Adverse-action-notice content policy under Reg B §1002.9, where the policy does not require principal-reasons specificity at the rigor Reg B and Comment 9(b)(2)-3 of the Official Staff Commentary expect (frequent gap site for ML-decisioning policies).
- Prohibited-basis monitoring policy (testing, comparator-file analysis, exception-and-override review) where the policy is silent or generic.
- Disparate-impact assessment policy, where the policy is silent on the disparate-impact dimension.
- Section 1071 small-business data collection policy, where the firm meets the originations-volume threshold and the policy is silent or pre-rule.

### Complaint-handling policy gaps

- Complaint-channel coverage policy (intake methods, response timing, escalation) where the policy is silent on a channel the firm operates (social media, app store reviews, executive-office complaints, regulator-forwarded complaints).
- Root-cause analysis and remediation-loop policy, where the policy treats complaints as a customer-service operation rather than as a feedback loop into product design.
- Complaint-data analytics and reporting policy, where the policy is silent on the analytics expected to surface UDAAP-implicating patterns.
- CFPB Complaint Database engagement policy, where the policy is silent on the firm's response timing and content.

### Sales-practice and best-interest gaps

- Suitability policy (annuity, life, structured product) under the operative rule, where the policy lags the post-2020 best-interest amendments most states have adopted.
- Reg BI policy under Rule 15l-1 (broker-dealer best-interest), where the policy is silent on the four obligations (disclosure, care, conflicts of interest, compliance).
- Sales-incentive design policy, where compensation structures create UDAAP risk and the policy is silent on the incentive-design review.

### Marketing-review gaps

- Algorithmic and AI-generated marketing content review policy, where the policy is silent on the review of GenAI-produced marketing copy.
- Influencer and third-party endorser policy, where the policy is silent on the FTC Endorsements Guides expectations.
- Cross-channel consistency policy, where the policy is silent on the obligation that disclosures present in one channel are not undone in another (the CFPB and FTC have repeatedly flagged this).

## Implications for matrix construction

- **UDAAP gaps are usually `partial` or `weak`, rarely `missing`.** Most firms have product-approval, marketing-review, and complaint-handling policies; the question is whether they require the design-level UDAAP review the CFPB expects.
- **Fair-lending policy gaps surface as `partial` more often than `missing`.** The matrix is honest about the rigor gap rather than rating an existing-but-thin policy as covered.
- **Customer impact is a severity driver.** Severity rationale on conduct rows references the population the gap could harm and the harm pattern (financial loss, denial of credit, data exposure, deceptive impression).
- **Cross-policy interactions are common.** A product-approval policy gap interacts with the marketing-review policy and the sales-incentive-design policy; the matrix surfaces all three rather than fixing one in isolation.

## Anchors used by this overlay

- CFPB UDAAP Examination Manual — current edition.
- CFPB Circulars and Bulletins on UDAAP positions — current at engagement effective date.
- Dodd-Frank §1031 / §1036 — 12 USC §5531 / §5536.
- 12 CFR Part 1002 — Regulation B (ECOA), including §1002.4, §1002.6, §1002.9, Subpart B (§1071).
- 12 CFR Part 1003 — Regulation C (HMDA).
- 42 USC §3601 et seq. — Fair Housing Act.
- 24 CFR Part 100 — HUD Discriminatory Effects rule.
- 12 CFR Part 1014 — Regulation N (MAP Rule).
- 12 CFR Part 1026 — Regulation Z, including credit-card marketing and 2024 late-fee rule [verify litigation status].
- 12 CFR Part 1030 — Regulation DD (Truth in Savings).
- 12 CFR Part 1005 — Regulation E, including §1005.17 overdraft opt-in.
- 17 CFR §240.15l-1 — SEC Reg BI.
- 17 CFR §275.206(4)-1 — Adviser Marketing Rule.
- FINRA Rule 2210 — Communications with the Public.
- OCC Bulletin 2014-37 / 2020-94 / 2021-31 — bank consumer compliance and complaint handling [verify operative bulletins].
- FTC Act §5 — 15 USC §45.
