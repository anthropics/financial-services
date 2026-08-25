# Cyber cross-cutting overlay — human-review-gates

Loads when the scope `cross_cutting_overlay_set` includes `cyber`. The overlay shapes the gate matrix when gates cover incident-response decisions, materiality determinations for cyber events, cyber-disclosure decisions, and cyber-third-party arrangements.

## Why cyber belongs in many gate matrices

Cyber gates are rarely standalone; they layer onto substantive gates (vendor onboarding includes a cyber-due-diligence sub-gate; product launch includes a security-architecture-review sub-gate; incident response includes a materiality-determination gate that feeds the disclosure decision). Where the underlying gate touches information-security controls, customer-data exposure, or third-party-provided technology, the cyber overlay adds named criteria, specific independence requirements, and the documentation discipline a CISO function and an examiner will recognise.

## Source basis

- **NYDFS 23 NYCRR Part 500 — Cybersecurity Requirements for Financial Services Companies**. November 2023 amendment introduced new tiering (Class A companies, covered entities, small businesses) and tighter incident-notice requirements. §500.4 (cybersecurity governance — senior governing body responsibility; CISO reporting to senior governing body; CISO annual report) is the primary anchor for cyber-gate decision authority. §500.17 (notice of cybersecurity event; 72-hour reporting to NYDFS) anchors the incident-notice readiness gate.
- **SEC Cybersecurity Rules (effective December 2023)**. Form 8-K Item 1.05 (material cybersecurity incident disclosure within 4 business days of materiality determination); 17 CFR §229.106 (Reg S-K Item 106 cybersecurity risk management, strategy, and governance — annual disclosure for public registrants). The materiality-determination gate is a named gate at public-registrant firms; the disclosure-committee or its equivalent is the named decision authority.
- **FFIEC IT Examination Handbook**. The Information Security booklet (governance, logical security, change management) and the Audit booklet (IT-audit reportable conditions). The Information Security booklet's governance section (§II.A) frames the senior-management oversight expectation that flows into cyber-gate decision authority.
- **Reg S-P (17 CFR §248.30)**. Customer-information safeguards for SEC-registered entities. The 2024 amendment introduced incident-response and customer-notification requirements with named timelines.
- **GLBA Safeguards Rule (16 CFR Part 314)**. FTC version with functional-regulator equivalents for banks. The Safeguards Rule names the qualified individual (a designated information-security program lead) as a regulatory expectation that informs cyber-gate decision authority.
- **NIST Cybersecurity Framework 2.0 (February 2024)**. Used as a control taxonomy and as a governance scaffolding; the Govern function (introduced in CSF 2.0) overlaps directly with gate-architecture concerns and provides language for governance-gate criteria.
- **CISA cross-sector cybersecurity performance goals (CPGs)**. Voluntary baseline; sometimes referenced in supervisor expectations for critical-infrastructure-tagged entities.

## What the overlay adds to the matrix

### Decision authority — CISO and disclosure-committee gates

For NYDFS-covered entities, NYDFS §500.4 names the senior governing body and the CISO as the decision-authority backbone for cyber-program decisions. The matrix's decision-authority block names:
- The senior governing body (board of directors or equivalent) as the ultimate adopting body for cyber-program changes; the annual CISO report under §500.4(b) is a named annual gate.
- The CISO (or qualified equivalent) as the operational decision-holder for cyber-gate decisions, with reporting-line independence preserved (CISO reports to senior governing body, not to a CIO or COO that owns the IT function being reviewed).

For SEC public registrants, the disclosure committee (or equivalent body that reviews 8-K filings) is the named decision-authority for the materiality-determination gate. The named members typically include the General Counsel, the CFO, the CISO, the Chief Compliance Officer, and an independent disclosure adviser. The gate documentation requirement names the disclosure-committee minute and the materiality-determination memorandum.

### Materiality-determination gate (SEC public registrants)

The Form 8-K Item 1.05 disclosure obligation is triggered by a materiality determination, not by the incident itself. The gate matrix elevates the materiality-determination decision to a named gate with:
- **Trigger**: detection of a cybersecurity incident with potential material impact, escalated by the CISO function within a stated internal timeline.
- **Required reviewers**: disclosure committee membership; the CISO presents the technical facts, the General Counsel and CCO present the disclosure analysis, the CFO presents the financial impact, the disclosure committee renders the decision.
- **Decision criteria**: SEC materiality standard (whether a reasonable investor would consider the incident important to an investment decision), with the SEC's published interpretive guidance (the December 2023 Compliance & Disclosure Interpretations on Item 1.05) as the source anchor.
- **Stop conditions**: no go on filing if the materiality determination is not supported by the incident facts; no delay past 4 business days from materiality determination unless the Attorney General has notified that disclosure poses a substantial risk to national security or public safety (the §1.05 carve-out).
- **Documentation requirement**: the materiality-determination memorandum, the disclosure committee minutes, the legal analysis, the technical timeline, and the filing record.

### Incident-notice readiness gate

Incident-notice readiness is a control, not an event. The matrix carries an incident-notice readiness gate (typically annual or after each material exercise) with criteria sourced from NYDFS §500.17, Reg S-P amended customer-notification timing, SEC 8-K Item 1.05, GLBA Safeguards Rule customer-notification provisions, and state breach-notification statutes (which vary by state). The decision criteria address: documented materiality-determination workflow with named approver; notification template library covering each applicable jurisdiction and regulator; tabletop exercise evidence with named participants and lessons-learned tracking; dispatch-path readiness across regulator portals, customer-channels, and counterparty channels.

### Third-party cyber gates

Where the gate is a vendor-onboarding or vendor-monitoring gate at a NYDFS-covered entity, NYDFS §500.11 (third-party service-provider security policy) layers onto the substantive interagency-TPRM-anchored gate. The matrix carries cyber-specific decision criteria (vendor cybersecurity assessment, vendor's incident-notification commitment, vendor's encryption commitments under §500.15, vendor's MFA commitments under §500.12) and the CISO concurrence as a required reviewer on critical-vendor gates touching customer data or privileged-system access.

### CISO independence

For NYDFS-covered entities and for firms anchored on the GLBA Safeguards Rule's qualified-individual concept, the matrix flags CISO reporting-line independence. The CISO that reports to a CIO that owns the IT function being reviewed has structural conflict; NYDFS §500.4 explicitly addresses this by naming the senior governing body as the CISO's reporting destination. The matrix's `independence_basis` for CISO-anchored gates cites §500.4 and (for non-NYDFS firms) the firm's own policy or the GLBA Safeguards Rule.

### CSF 2.0 Govern function as scaffolding

For firms that anchor on NIST CSF 2.0, the Govern function categories (GV.OC organizational context, GV.RM risk management strategy, GV.RR roles, responsibilities, and authorities, GV.PO policy, GV.OV oversight, GV.SC cybersecurity supply chain risk management) provide gate-architecture scaffolding. Each Govern category maps to one or more gates in the matrix; the source anchor cites the specific CSF 2.0 subcategory.

## Common patterns

- **Materiality determination buried in the incident-response runbook**. Many firms have an incident-response runbook that names a materiality-determination step but does not elevate it to a board- or disclosure-committee gate. For SEC public registrants, this is a gap; the matrix's gap section flags it and recommends a named disclosure-committee gate.
- **CISO reports to CIO; CIO sits on cyber gates**. Reporting-line conflict is common in firms that have not refreshed governance to NYDFS §500.4. The matrix flags the conflict and recommends a CISO reporting-line refresh as part of the gate-architecture refresh.
- **Vendor cyber gate without CISO concurrence**. A critical-vendor onboarding gate that does not include the CISO function as a required reviewer on cyber-relevant arrangements misses the §500.11 anchor and the SEC Reg S-P safeguards-rule anchor. The matrix flags this.
- **Annual CISO report treated as a one-pager**. NYDFS §500.4(b) requires the CISO's annual report to the senior governing body to address material cybersecurity risks, the firm's cybersecurity program, and material cybersecurity events. Some firms produce a one-pager; the matrix elevates the annual CISO report to a named gate with substantive content criteria.

## Anchors used by this overlay

- 23 NYCRR Part 500 — NYDFS Cybersecurity Requirements (post-November 2023 amendment).
  - §500.4 (cybersecurity governance — senior governing body, CISO, CISO annual report)
  - §500.11 (third-party service-provider security policy)
  - §500.12 (multi-factor authentication)
  - §500.15 (encryption of nonpublic information)
  - §500.16 (incident response and business continuity)
  - §500.17 (notice of cybersecurity event; 72-hour reporting)
  https://www.dfs.ny.gov/industry_guidance/cybersecurity
- FFIEC IT Examination Handbook, Information Security booklet (September 2016). §II.A governance. https://ithandbook.ffiec.gov/it-booklets/information-security/
- 17 CFR §229.106 — SEC Reg S-K Item 106 (cybersecurity disclosure). https://www.ecfr.gov/current/title-17/chapter-II/part-229/section-229.106
- Form 8-K Item 1.05 — material cybersecurity incident disclosure (effective December 2023). https://www.sec.gov/files/form-8-k.pdf
- SEC Compliance & Disclosure Interpretations — Item 1.05 (December 2023). https://www.sec.gov/divisions/corpfin/guidance/exchange-act-form-8-k.htm
- 17 CFR §248.30 — Reg S-P (Safeguards Rule and 2024-amendment incident-response and notification). https://www.ecfr.gov/current/title-17/chapter-II/part-248/subpart-A/section-248.30
- 16 CFR Part 314 — FTC Safeguards Rule. https://www.ftc.gov/legal-library/browse/rules/safeguards-rule
- NIST Cybersecurity Framework 2.0 — Govern function (February 2024). https://www.nist.gov/cyberframework
- CISA Cross-Sector Cybersecurity Performance Goals. https://www.cisa.gov/cross-sector-cybersecurity-performance-goals
- State breach-notification statutes — vary by state; firm-overlay names the statutes that apply to the institution's jurisdictional footprint.
