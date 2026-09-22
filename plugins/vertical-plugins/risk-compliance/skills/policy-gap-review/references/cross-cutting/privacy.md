# Privacy cross-cutting overlay — policy-gap-review

Loads when the scope `cross_cutting_overlay_set` includes `privacy`. Binds the matrix to privacy-and-data-handling-policy expectations when the policy in scope is a privacy policy, a customer-data-handling policy, a data-governance policy, or a substantive policy that includes a section on personally identifiable information or nonpublic personal information.

## Source basis

### GLBA Safeguards Rule and Privacy Rule

- **16 CFR Part 314** (FTC Safeguards Rule, post-amendment 2021/2023) and the bank-supervisor equivalent for prudentially-supervised institutions. §314.4 lists program elements: designate a qualified individual, conduct a written risk assessment, implement safeguards (access controls, identification and inventory of data, encryption, secure development, MFA, secure disposal, change management, monitoring), test, train, oversee service providers, written incident-response plan, periodic reporting to board.
- **16 CFR Part 313** (FTC Privacy Rule), with bank-supervisor-equivalent rules for prudential-supervised institutions and Reg P (12 CFR Part 1016) for CFPB-supervised institutions.

### Reg P — 12 CFR Part 1016

Anchor: §1016.4 initial privacy notice; §1016.5 annual privacy notice (with the post-2015 exception for institutions meeting the FAST Act conditions); §1016.10 sharing limitations and opt-out; §1016.13 affiliate sharing under FCRA. [verify section labels.]

### Reg S-P — 17 CFR §248.30

Anchor: SEC customer-information safeguards rule. The 2024 amendment introduced incident-response and customer-notification policy requirements that pre-2024 policies almost always miss. [verify post-2024 amendment numbering.]

### State privacy laws

- **California Consumer Privacy Act / California Privacy Rights Act** (CCPA/CPRA) — Cal. Civ. Code §1798.100 et seq. Operative for businesses meeting the threshold; financial-services entities are partially exempt for GLBA-covered information but the exemption is narrower than commonly assumed.
- **Virginia Consumer Data Protection Act** (VCDPA), **Colorado Privacy Act** (CPA), **Connecticut Data Privacy Act** (CTDPA), and a growing list of state laws since 2023. Each carries its own thresholds and policy expectations; the matrix references the operative state laws where the firm has covered consumers.

### FCRA-related anchors

- **FCRA** — 15 USC §1681 et seq., for any policy touching consumer-report information.
- **Reg V** — 12 CFR Part 1022, including affiliate-marketing rules and the Identity Theft Red Flags rules under Subpart J (the Reg S-ID parallel).
- **Reg V furnisher accuracy and integrity rules** under §1022.42 et seq.

### Sectoral rules touching privacy

- **HIPAA** — 45 CFR Part 160, 164 (when the firm holds protected health information; less common in financial services but applies to insurance entities holding member health data).
- **Gramm-Leach-Bliley** umbrella applies across financial services; the matrix's privacy section anchors here for most engagements.

## Gap patterns the privacy overlay flags

### Information-security-program policy gaps

- Designation of a qualified individual responsible for the security program (§314.4(a)).
- Written risk assessment (§314.4(b)) at the cadence the rule expects, with documented methodology.
- Written incident-response plan (§314.4(h) post-2021 amendment), with named roles and customer-notification triggers.
- Periodic written report to the board (§314.4(i) post-2021 amendment) at least annually.

### Privacy-notice policy gaps

- Initial privacy notice content (Reg P §1016.4 / Reg S-P §248.4), where the policy does not name the content elements the rule requires.
- Annual privacy notice (Reg P §1016.5 / Reg S-P §248.5), where the policy is silent on the FAST Act exception conditions for opt-out-eligible institutions.
- Opt-out mechanics (Reg P §1016.7 / Reg S-P §248.7), where the policy does not name the opt-out method or the response timing.
- Affiliate-marketing opt-out under FCRA §624 (Reg V §1022.20-§1022.27), where the policy is silent on the affiliate-marketing-specific opt-out separate from Reg P opt-out.

### Customer-incident-notification policy gaps (Reg S-P 2024 amendment)

- Customer-notification triggers and timing under the 2024 Reg S-P amendment (notify customers as soon as practicable but not later than 30 days after determining unauthorised access or use occurred or is reasonably likely to have occurred). Pre-2024 customer-notification policies almost always miss this.
- Service-provider oversight including contractual obligation to notify the firm of incidents within a named timeframe.
- Documentation of the materiality determination and the customer-list scoping.

### State-privacy-law gaps

- CCPA/CPRA disclosure requirements under §1798.100, where the policy does not address the categories of information the firm collects, the sources, the business purposes, the disclosures to third parties, and the consumer rights.
- Consumer-rights handling (access, deletion, correction, portability, opt-out of sale/share) where the policy is silent on the workflow and timing.
- Service-provider and third-party contractor flow-down provisions, where the firm-side contract templates do not pass through the state-law required terms.

### FCRA and Reg V gaps

- Furnisher accuracy and integrity policy (Reg V §1022.42), where the firm furnishes information to a consumer reporting agency and the policy is silent on the accuracy-and-integrity expectations.
- Identity Theft Red Flags policy (Reg V Subpart J / Reg S-ID), where the policy is silent on the red-flags identification, response, and program-administration content elements.
- FCRA dispute handling under §1681s-2(b), where the policy is silent on the firm's investigation obligations on receiving a CRA dispute.

### Sectoral overlays

- HIPAA policy expectations where the firm is a covered entity or business associate.
- Children's Online Privacy Protection Act (COPPA) where the firm collects information from users under 13; rare in financial services but applies in some fintech edu-products.

## Implications for matrix construction

- **GLBA Safeguards is the most-cited privacy benchmark** because it imposes prescriptive program-element expectations. Most privacy-policy gaps trace to a Safeguards element the policy does not address at the rigor the rule expects.
- **The 2024 Reg S-P customer-notification amendment is a high-frequency `outdated` row.** Policies that were refreshed in 2022-2023 typically do not address the 2024 amendment.
- **State-privacy-law gaps appear as a layered set.** Where the firm operates across multiple state perimeters, the matrix surfaces gaps state-by-state rather than rolling up to a single "state privacy" row.
- **GLBA-exemption claims under CCPA/CPRA need explicit support.** A policy that broadly cites the GLBA exemption without addressing the narrowing courts have applied is a gap; the matrix flags the exemption-scope question for legal review.

## Anchors used by this overlay

- 16 CFR Part 314 — FTC Safeguards Rule [verify post-2021/2023 amendment edition].
- 16 CFR Part 313 — FTC Privacy Rule.
- 12 CFR Part 1016 — Regulation P (CFPB privacy rule).
- 17 CFR §248.30 — Reg S-P [verify post-2024 amendment numbering].
- 12 CFR Part 1022 — Regulation V (FCRA implementation), including Subpart J (Identity Theft Red Flags) and §1022.20-§1022.27 (affiliate marketing).
- 15 USC §1681 — FCRA.
- Cal. Civ. Code §1798.100 et seq. — CCPA/CPRA.
- Va. Code §59.1-575 et seq. — VCDPA.
- Colo. Rev. Stat. §6-1-1301 et seq. — CPA.
- Conn. Gen. Stat. §42-515 et seq. — CTDPA.
- 45 CFR Parts 160, 164 — HIPAA Privacy and Security Rules (when in scope).
- 16 CFR Part 312 — COPPA (when in scope).
