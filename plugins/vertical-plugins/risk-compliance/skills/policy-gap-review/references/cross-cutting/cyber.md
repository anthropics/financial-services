# Cyber cross-cutting overlay — policy-gap-review

Loads when the scope `cross_cutting_overlay_set` includes `cyber`. The overlay binds the matrix to cybersecurity-policy expectations when the policy in scope is a cybersecurity policy, an information-security policy, or a substantive policy that includes a cybersecurity section (most material policies do).

## Why cyber loads on most policy gap reviews

Most material firm policies touch information systems or customer data somewhere. A vendor-management policy carries cyber-tagged sections on third-party security; an MRM policy carries cyber-tagged sections on model-serving environment access; a consumer-deposit policy carries cyber-tagged sections on customer data protection; a board-pack policy carries cyber-tagged sections on distribution and DLP. The cyber overlay surfaces the cybersecurity-benchmark expectations the substantive policy needs to address.

The overlay is consultative. It does not duplicate the firm's CISO-owned information-security policy; it ensures the substantive policy carries the cybersecurity sections the supervisor will read.

## Source basis for cyber-policy benchmarks

- **NYDFS 23 NYCRR Part 500** — Cybersecurity Requirements for Financial Services Companies. November 2023 amendment introduced new tiering (Class A companies, covered entities, small businesses) and tighter incident-notice requirements. The most prescriptive cybersecurity-policy-content rule in US financial-services regulation; §500.3 lists fifteen content elements the policy must address.
- **FFIEC IT Examination Handbook** — Information Security booklet (governance, logical security, change management) and the Management booklet on policy-framework expectations. Operative for FFIEC-supervised institutions.
- **SEC cybersecurity rules** — 8-K Item 1.05 (material cybersecurity incident disclosure, effective December 2023) and Reg S-K Item 106 (cybersecurity risk management, strategy, and governance) for public registrants. Both impose policy-disclosure expectations.
- **Reg S-P** — 17 CFR §248.30, customer-information safeguards for SEC-registered entities. The 2024 amendment introduced incident-response and customer-notification policy requirements.
- **GLBA Safeguards Rule** — 16 CFR Part 314 (FTC) and the bank-supervisor equivalent. §314.4 lists program elements.
- **NIST Cybersecurity Framework 2.0** (February 2024) — used as a policy taxonomy where the firm anchors on it. The Govern function is new in 2.0 and is a frequent benchmark for governance-policy gaps in pre-2024 cyber policies.
- **NIST SP 800-53 Rev. 5** — Security and Privacy Controls. Used as a granular policy benchmark for federal-tied entities and for firms that anchor on FedRAMP-style profiles.
- **CISA Cross-Sector Cybersecurity Performance Goals** — voluntary baseline; sometimes referenced in supervisor expectations for critical-infrastructure entities.

## Gap patterns the cyber overlay flags

### Governance gaps

- Cybersecurity policy approval cadence and board attestation, where NYDFS §500.3 expects board (or equivalent governing-body) approval at least annually and a CISO report to the board annually under §500.4.
- CISO appointment and reporting line, where NYDFS §500.4 and Reg S-K Item 106(c) expect the policy to articulate the CISO's role and reporting.
- Risk assessment cadence, where NYDFS §500.9 expects the policy to set the cadence and methodology.

### Identity and access gaps

- Multi-factor authentication policy, where NYDFS §500.12 (post-amendment) is more prescriptive than pre-amendment; covered entities must address MFA on all individuals accessing internal networks from external networks, all privileged accounts, and all third-party applications accessing nonpublic information.
- Privileged access management policy, where NYDFS §500.7 (post-amendment) introduces explicit expectations on privileged-account management.
- Access review cadence, where the policy is silent on quarterly cadence for privileged accounts.

### Vulnerability and threat-management gaps

- Vulnerability management program policy, where NYDFS §500.5 expects continuous monitoring or vulnerability assessments; pre-amendment policies often stop at periodic scanning.
- Penetration testing cadence, where NYDFS §500.5(a)(2) expects annual penetration testing for covered entities.
- Patch-management policy, where the policy lacks named SLAs for critical-vulnerability remediation.

### Incident-response gaps

- Incident-response plan, where NYDFS §500.16 expects the policy to address detection, response, recovery, communication, and reporting; gap rows often surface on the post-amendment expansion to ransomware and extortion.
- Incident-notice readiness, where the policy does not name the materiality-determination workflow, the named approver, the notification template, or the dispatch path. NYDFS §500.17 imposes a 72-hour notice for material cybersecurity events; SEC 8-K Item 1.05 imposes a 4-business-day disclosure for public-registrant material incidents; Reg S-P amended customer-notification timing.
- Ransomware-payment notice (post-amendment NYDFS §500.17) and CISA reporting expectations where applicable.

### Third-party-cyber gaps

- Third-party service-provider security policy, where NYDFS §500.11 imposes specific content elements that pre-amendment policies often miss.
- Vendor cyber-incident notification policy, where the policy says vendors will notify but does not name the expected timing in the contract template.
- Subservice-provider transparency policy, where the policy is silent on the SOC report's complementary subservice organisation controls (CSOCs).

### Data-protection gaps

- Encryption policy, where NYDFS §500.15 expects encryption of nonpublic information in transit and at rest, with documented compensating controls if not feasible.
- Data-loss prevention (DLP) policy, where the policy is silent or generic.
- Data-classification policy, where the policy does not feed protective controls to data tiers.

### Public-registrant disclosure-process gaps

For SEC public registrants, the matrix carries gap rows on the cyber-disclosure process itself: materiality-determination policy (who decides, against what threshold, with what documentation), 8-K filing-timing policy (4 business days from materiality determination), and Reg S-K Item 106 annual disclosure policy (governance, risk management strategy, board oversight). Frequent gap site for pre-2023 disclosure policies.

### AI-system cybersecurity gaps (when in scope)

- Model-artefact integrity policy (signing, attestation).
- Model-serving-endpoint authentication and rate-limiting policy.
- Prompt-injection and adversarial-input handling policy.
- Tool-and-agent-privilege boundary policy (when scope includes agentic AI).

## Implications for matrix construction

- **Cyber-policy gaps are usually `partial` or `outdated`, rarely `missing`.** Most firms have a cybersecurity policy; the question is whether it addresses the named benchmark's content elements at the rigor the rule expects.
- **The matrix surfaces the materiality-determination workflow as a control, not a fact.** A policy that says "we will determine materiality" is partial until the materiality-determination workflow is named.
- **Joint ownership is common and explicit.** Cyber-policy gaps for AI models name the CISO function and the model owner together; cyber-policy gaps for vendor controls name the CISO function and the head of TPRM together.
- **Pre-November-2023 NYDFS policies almost always carry `outdated` rows.** The 2023 amendment expanded enough content that policies untouched since 2017-2022 will not pass the post-amendment expectations.

## Anchors used by this overlay

- 23 NYCRR Part 500 — NYDFS Cybersecurity Requirements (post-November 2023 amendment) [verify section labels for amended provisions].
- FFIEC IT Examination Handbook, Information Security booklet (September 2016) [verify currently posted edition].
- 17 CFR §229.106 — SEC Reg S-K Item 106 (cybersecurity risk management, strategy, and governance disclosure).
- Form 8-K Item 1.05 — material cybersecurity incident disclosure (effective December 2023).
- 17 CFR §248.30 — Reg S-P (Safeguards Rule and 2024-amendment incident-response and notification).
- 16 CFR Part 314 — FTC Safeguards Rule [verify post-amendment edition].
- NIST Cybersecurity Framework 2.0 (February 2024).
- NIST SP 800-53 Rev. 5 — Security and Privacy Controls for Information Systems and Organizations.
- CISA Cross-Sector Cybersecurity Performance Goals.
