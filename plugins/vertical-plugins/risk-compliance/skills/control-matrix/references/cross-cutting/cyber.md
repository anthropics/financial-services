# Cyber cross-cutting overlay — control-matrix

Loads when the scope `cross_cutting_overlay_set` includes `cyber`. The overlay adds cyber-tagged rows to the matrix when the scoped process touches information systems, customer data, or third-party-provided technology services.

## Why cyber belongs in nearly every matrix

Most processes the matrix scopes touch information systems somewhere: a credit-decisioning model lives on an inference endpoint, a vendor-monitoring process pulls SOC reports from a vendor portal, a board-pack process distributes via a document-management system, a complaint-handling process accepts intake via web and email. Cyber controls are not a separate matrix; they are tagged rows inside the substantive matrix, surfaced so an examiner reading the matrix can see where the cyber surface is and what mitigates it.

The overlay is consultative. It does not duplicate the firm's CISO-owned information-security risk assessment; it ensures the substantive matrix carries the cyber rows the examiner will look for in the context of this process.

## Source basis

- **NYDFS 23 NYCRR Part 500** — Cybersecurity Requirements for Financial Services Companies. November 2023 amendment introduced new tiering (Class A companies, covered entities, small businesses) and tighter incident-notice requirements. Operative for NYDFS-licensed entities.
- **FFIEC IT Examination Handbook** — Information Security booklet (governance, logical security, change management) and the Cybersecurity Assessment Tool (where the firm uses it).
- **SEC cybersecurity rules** — 8-K Item 1.05 (material cybersecurity incident disclosure, effective December 2023) and Reg S-K Item 106 (cybersecurity risk management, strategy, and governance) for public registrants.
- **Reg S-P** — 17 CFR §248.30, customer-information safeguards for SEC-registered entities. The 2024 amendment introduced incident-response and customer-notification requirements.
- **Reg S-ID** — 17 CFR §248.201 / §248.202, Identity Theft Red Flags rules.
- **NIST Cybersecurity Framework 2.0** (February 2024) — used as a control taxonomy where the firm anchors on it.
- **NIST SP 800-53 control families** — used for granular control statements where the firm anchors on it; commonly via the FedRAMP-style profile when the firm operates federal-tied services.
- **CISA cross-sector cybersecurity performance goals** (CPGs) — voluntary baseline; sometimes referenced in supervisor expectations for critical-infrastructure entities.

## What the cyber overlay adds to the matrix

### Governance rows

- Cybersecurity policy approval and review (NYDFS §500.3 for covered entities).
- CISO appointment and reporting line (NYDFS §500.4).
- Board-level cybersecurity oversight (Reg S-K Item 106(c) for public registrants; NYDFS §500.4 for covered entities).
- Cybersecurity risk assessment cadence (NYDFS §500.9, NIST CSF 2.0 Govern function).

### Identity and access rows

- Logical access controls (FFIEC IT IS booklet §II.C.7).
- Privileged-access management (NYDFS §500.7 for privileged accounts).
- Multi-factor authentication where required (NYDFS §500.12, GLBA Safeguards Rule).
- Access-review cadence and evidence (typically quarterly for privileged accounts; the matrix names the frequency).

### Vulnerability and threat rows

- Vulnerability management program (NYDFS §500.5; FFIEC IT IS booklet).
- Penetration testing cadence and scope (NYDFS §500.5(a)(2), typically annual for covered entities; NIST CSF 2.0 Identify and Protect functions).
- Threat-intelligence consumption controls.
- Patch-management controls.

### Incident-response and continuity rows

- Incident-response plan and tabletop-exercise evidence (NYDFS §500.16; FFIEC IT IS booklet).
- Business-continuity and disaster-recovery integration with cyber (NYDFS §500.16(b) post-amendment).
- Incident-notice readiness (NYDFS §500.17 — 72-hour notice to NYDFS for material cybersecurity events; SEC 8-K Item 1.05 — 4-business-day disclosure for public-registrant material incidents; Reg S-P amended customer-notification timing).
- Ransomware-specific controls and reporting (post-amendment NYDFS §500.17 ransomware-payment notice; CISA reporting where applicable).

### Third-party-cyber rows

- Third-party service-provider security policy and ongoing assessment (NYDFS §500.11).
- SOC 2 Type II review controls for vendor SOC reports.
- Subservice-provider transparency controls (the SOC report's CSOCs).
- Vendor cyber-incident notification controls (contractual, with named timing).

### Data-protection rows

- Encryption in transit and at rest (NYDFS §500.15 for nonpublic information).
- Data-loss prevention controls (DLP).
- Data-classification controls feeding the right protective controls to the right data.

### Public-registrant disclosure-process rows

For SEC public registrants, the matrix carries rows for the cyber-disclosure process itself: materiality-determination control (who decides, against what threshold, with what documentation), 8-K filing-timing control (4 business days from materiality determination, with documented exceptions for national-security or law-enforcement deferral), and Reg S-K Item 106 annual disclosure controls (governance, risk management strategy, board oversight).

### Operational-tech and AI-system rows (when in scope)

When the matrix scopes a process touching AI inference endpoints, the cyber overlay adds:
- Model-artefact integrity controls (signing, attestation).
- Model-serving-endpoint authentication and rate-limiting controls.
- Prompt-injection and adversarial-input detection (where the firm has the layer; absence is itself recordable).
- Tool-and-agent-privilege boundary controls (when the scoped process uses agentic AI).

## Implications for matrix construction

- **Cyber-tagged rows carry a `control_type` honestly.** Preventive (access controls, encryption), detective (logging, anomaly detection, monitoring), response (incident-response runbook, notice-readiness), compensating (where a primary control is not yet in place but a secondary monitors for the gap).
- **Joint ownership is common and explicit.** Cyber-tagged rows for AI models name the CISO function and the model owner together; cyber-tagged rows for vendor controls name the CISO function and the head of TPRM together.
- **Incident-notice readiness is a control, not a fact.** A row that says "we will notify within 72 hours if we determine an event is reportable" is not yet a control; the row is a control when the materiality-determination workflow, the named approver, the notification template, and the dispatch path are all evidenced.
- **The CISO function is a reviewer or a co-owner, not the matrix author.** The matrix lives with the process owner; the CISO reviews cyber-tagged rows.

## Common pitfalls in cyber-overlay matrices

- **Treating SOC 2 as universal third-party assurance.** A SOC 2 Type II covers what the auditor scoped; the matrix row notes the scope of the SOC report and the gaps the firm covers via direct due diligence.
- **Conflating the firm's NIST CSF 2.0 self-assessment with the matrix.** The CSF self-assessment is a posture artifact; the matrix is the obligation-anchored control inventory. They reference each other; they are not the same artifact.
- **Burying the cyber-disclosure process for public registrants.** Materiality-determination is itself a control. A matrix that lists technical controls but omits the disclosure-decision workflow misses the rows the SEC will probe after a material incident.
- **Vendor cyber-incident-notification controls without contractual anchor.** A control that says "vendor will notify us within X hours" is not a control unless the contract obligates the vendor and the firm has a process for receiving and acting on the notice.

## Anchors used by this overlay

- 23 NYCRR Part 500 — NYDFS Cybersecurity Requirements (post-November 2023 amendment) [verify section labels for amended provisions].
- FFIEC IT Examination Handbook, Information Security booklet (September 2016) [verify currently posted edition].
- 17 CFR §229.106 — SEC Reg S-K Item 106 (cybersecurity risk management, strategy, and governance disclosure).
- Form 8-K Item 1.05 — material cybersecurity incident disclosure (effective December 2023).
- 17 CFR §248.30 — Reg S-P (Safeguards Rule and 2024-amendment incident-response and notification).
- 17 CFR §248.201 / §248.202 — Reg S-ID (Identity Theft Red Flags).
- 16 CFR Part 314 — FTC Safeguards Rule (for non-bank financial institutions); functional-regulator equivalents for banks.
- NIST Cybersecurity Framework 2.0 (February 2024).
- NIST SP 800-53 Rev. 5 — Security and Privacy Controls for Information Systems and Organizations.
- CISA Cross-Sector Cybersecurity Performance Goals.
