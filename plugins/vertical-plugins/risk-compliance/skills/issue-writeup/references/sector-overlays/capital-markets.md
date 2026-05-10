# Capital-markets sector overlay — issue-writeup

Loads when the scope `sector_overlay_set` includes `capital-markets`. The overlay shapes the criteria block, the severity calibration, and the closure-evidence framing for issues at SEC- and FINRA-regulated entities (broker-dealers, investment advisers, registered funds, transfer agents, exchanges, ATSs).

## Why the capital-markets overlay matters

SEC EXAMS and FINRA each have a published deficiency-letter format and a follow-up convention that is distinct from the federal banking MRA / MRIA framework and from the state-DOI insurance examination convention. The criteria block, severity calibration, and closure-evidence framing for capital-markets issues need to fit the SEC EXAMS deficiency-letter / risk-alert pattern or the FINRA Letter of Caution / examination-finding pattern.

## Source basis

- **SEC EXAMS Deficiency Letter** convention — the SEC Division of Examinations issues deficiency letters at the close of an examination listing observed deficiencies; the firm responds with a corrective-action plan within the time the letter specifies (typically 30 days). Severity calibration tracks to whether the deficiency is referred to the Division of Enforcement.
- **SEC EXAMS Risk Alerts** — published priorities and observed-deficiency categories that inform severity calibration even when the firm is not the subject of the alert.
- **SEC Rules cited in deficiency letters** — most frequently 17 CFR §240.15c3-1 (broker-dealer net capital), §240.15c3-3 (customer protection), §240.17a-3 / §240.17a-4 (recordkeeping), §240.15c3-5 (market access), §275.206(4)-7 (Investment Advisers Act compliance program), §275.204-2 (Investment Advisers Act recordkeeping), §270.38a-1 (Investment Company Act compliance program), Reg BI (broker-dealer best interest), Form CRS rules.
- **FINRA Letter of Caution** — informal disposition that closes an examination matter without formal disciplinary action; severity calibration is moderate; closure evidence is named but lighter than enforcement-track findings.
- **FINRA Examination Finding** — formal finding in the examination report; severity is high or moderate depending on the rule cited and the recurrence pattern; closure evidence is detailed and scheduled to the next exam cycle.
- **FINRA Cautionary Action and Acceptance, Waiver, and Consent (AWC)** — formal disciplinary dispositions; the issue write-up references the disposition but the full enforcement-track artifact lives outside the firm's internal issue log.
- **FINRA Rules cited in findings** — most frequently 3110 (supervision), 3120 (supervisory control system), 4511 (general books and records), 4512 (customer account information), 2010 (standards of commercial honor and just and equitable principles of trade), 2210 (communications), 2330 (variable annuities), and the Trade Reporting and Compliance Engine (TRACE) rules.
- **MSRB Rules** — for municipal-securities-active firms, MSRB Rule G-27 (supervision), G-8 (recordkeeping), G-9 (record retention), G-17 (fair dealing).

## What the overlay adds to the write-up

### SEC EXAMS deficiency-letter format

When the source type is examiner-letter and the regulator is SEC EXAMS, the criteria block follows the deficiency-letter format. A typical deficiency-letter line cites:
- The rule (e.g., "Section 206(4)-7 of the Investment Advisers Act and Rule 206(4)-7 thereunder").
- The deficiency observed (specific, with dates).
- The corrective action expected (often phrased as "the firm should").

The firm's internal issue write-up mirrors this structure: criteria carries the rule and section; condition carries the deficiency observed; recommendation carries the corrective action. The `mra_mria_classification` field is `n/a`. Severity calibration is high if the deficiency is referred to the Division of Enforcement, high or moderate if a remediation plan is requested with a short cure window, moderate if it is a no-further-action deficiency.

### FINRA Letter of Caution / examination finding format

When the source is a FINRA Letter of Caution, severity is typically moderate; the criteria block cites the FINRA rule and the firm's WSP (written supervisory procedures) section that the rule maps to. Closure evidence emphasises WSP update, supervisory-control-system enhancement, and examiner-acknowledgement at the next cycle. When the source is a FINRA examination finding, severity is high or moderate; the criteria block cites the FINRA rule and the firm's compliance-policy citation.

### Severity calibration

Capital-markets severity calibration weighs (1) customer-protection impact, (2) market-integrity impact, (3) capital adequacy / financial-stability impact, (4) supervisory-system impact, and (5) recordkeeping-and-disclosure-completeness impact. Findings that touch the customer-protection rule (Rule 15c3-3) or the net-capital rule (Rule 15c3-1) for broker-dealers carry severity weight tied to the regulatory threshold. Findings on the IA compliance program (Rule 206(4)-7) carry severity tied to the chief-compliance-officer's documented annual review.

### Closure-evidence framing

Closure evidence for SEC EXAMS deficiency-letter findings names the corrective-action-plan response, the implementation evidence (system change, policy update, training delivered, supervisory enhancement), and the readiness for the next examination touchpoint. For FINRA findings, closure evidence names the WSP update, the supervisory-control-system update, and the readiness for the next FINRA cycle exam. Investment-adviser findings under Rule 206(4)-7 carry closure evidence in the chief-compliance-officer's annual review documentation.

### Books-and-records-driven findings

Recordkeeping is the single most-cited category in SEC EXAMS deficiency letters and FINRA findings. The criteria block for recordkeeping findings cites 17 CFR §240.17a-3 and §240.17a-4 (broker-dealer), 17 CFR §275.204-2 (IA), or FINRA Rule 4511 directly. Cause for recordkeeping findings ties to the specific recordkeeping control that failed (preservation-format control, record-retention-period control, electronic-storage WORM-compliance control after the 2022 amendment).

## Common patterns

- **Annual-review-cycle findings on Investment Advisers**. Rule 206(4)-7 requires advisers to adopt and implement policies and procedures and to review them no less frequently than annually. Findings on the annual review (no review performed, review performed but not documented, review documented but not actioned) are common SEC EXAMS deficiencies. Severity is typically moderate to high.
- **Form CRS findings on dual-registered firms**. Findings on Form CRS delivery, content, or filing carry customer-impact severity weight; the consumer-protection lens applies.
- **Regulation Best Interest findings**. Reg BI findings on care obligation, disclosure obligation, conflict-of-interest obligation, or compliance obligation carry customer-impact severity weight; the FINRA Reg BI Risk Monitoring Reports inform severity calibration.
- **Net-capital and customer-reserve findings**. 15c3-1 and 15c3-3 findings carry the highest severity in the broker-dealer space; closure-evidence emphasises the financial-impact remediation and the net-capital recomputation.

## Implications for the CCCE

- **Criteria** for capital-markets-overlay issues cite the federal rule first (SEC, FINRA, MSRB), then the firm's WSP / compliance-policy section second. The order matters; SEC EXAMS and FINRA expect the regulatory criterion to lead.
- **Cause** for supervisory-system findings ties to the specific WSP element that failed (review-cadence control, escalation-path control, surveillance-output control). For recordkeeping findings, cause maps to the specific control attribute on preservation, retention, or accessibility.
- **Effect** for capital-markets issues quantifies customer-protection impact, market-integrity impact, capital-adequacy impact, and recordkeeping-and-disclosure-completeness impact distinctly. Customer-protection effects are typically named in customer-count and dollar-impact terms.
- **Closure evidence** for SEC EXAMS findings includes the corrective-action-plan response document; for FINRA findings, includes the WSP update and the supervisory-control-system update.

## Anchors used by this overlay

- 17 CFR Part 240 — Securities Exchange Act rules. https://www.ecfr.gov/current/title-17/chapter-II/part-240
  - §240.15c3-1 (Net Capital)
  - §240.15c3-3 (Customer Protection)
  - §240.15c3-5 (Risk Management Controls for Brokers or Dealers with Market Access)
  - §240.17a-3 / §240.17a-4 (Recordkeeping; 2022 amendment to 17a-4 on electronic-storage standard)
- 17 CFR Part 275 — Investment Advisers Act rules. https://www.ecfr.gov/current/title-17/chapter-II/part-275
  - §275.206(4)-7 (Compliance Procedures and Practices)
  - §275.204-2 (Books and Records)
- 17 CFR Part 270 — Investment Company Act rules.
  - §270.38a-1 (Compliance Procedures and Practices of Investment Companies)
- Form CRS — 17 CFR §249.640 / §279.10. [verify current section labels.]
- Regulation Best Interest — 17 CFR §240.15l-1. [verify section labels.]
- FINRA Rule Book. https://www.finra.org/rules-guidance/rulebooks/finra-rules
  - Rule 3110 (Supervision)
  - Rule 3120 (Supervisory Control System)
  - Rule 4511 (General Books and Records)
  - Rule 4512 (Customer Account Information)
  - Rule 2010 (Standards of Commercial Honor)
  - Rule 2210 (Communications with the Public)
- MSRB Rule Book. https://www.msrb.org/rules-and-interpretations/msrb-rules
  - Rule G-27 (Supervision)
  - Rule G-8 (Books and Records)
  - Rule G-9 (Record Retention)
  - Rule G-17 (Fair Dealing)
- SEC EXAMS Risk Alerts. https://www.sec.gov/exams/risk-alerts (informs severity calibration when the firm's deficiency category is published).
