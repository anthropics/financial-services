# Example: BCBS 239 risk-reporting matrix for a credit-risk monthly board pack

## Input

The Credit Risk function at a $40B regional bank (foreign banking organization, US IHC) is preparing for a regulator-driven BCBS 239 readiness review. The matrix scopes the monthly board credit-risk pack: data aggregation from the credit-loss data warehouse, manual reconciliation of stress-scenario inputs, narrative commentary by the Head of Credit Risk Reporting, and committee tabling. The persona is the Head of Credit Risk Reporting (1.5-line, embedded in the credit-risk function with a risk-reporting mandate); the audience is the firm's Data Management Committee and ultimately the board risk committee. Source posture is mixed: BCBS 239 (public) and the firm's risk-data-aggregation policy (firm-policy overlay).

## Why this scenario matters

This is the canonical BCBS 239 application of the matrix. BCBS 239 is principle-based, not rule-based, so the obligation set is the principles themselves and the controls are firm-side responses tied to each principle. The example tests the discipline of mapping principle-by-principle and surfacing principles that the firm has not controlled. It also tests the seam between the 1.5-line author (the credit-risk reporting team owns the pack) and the 2-line reviewer (the independent risk-management function challenges it).

## Output sketch

```yaml
matrix_id: CM-2026-CRR-BCBS239-01
as_of_date: 2026-05-06
engagement_id: ENG-2026-BCBS239-01

scope:
  process_or_product: "Monthly board credit-risk pack: data aggregation, reconciliation, narrative, committee tabling"
  business_unit: "Credit Risk Reporting"
  jurisdiction: "US"
  lines_of_defense: ["1.5L", "2L"]

source_list:
  - {source_type: industry-standard, label: "BCBS 239 — Principles for Effective Risk Data Aggregation and Risk Reporting", section_reference: "Principles 3, 4, 6, 7, 11", url: "https://www.bis.org/publ/bcbs239.htm"}
  - {source_type: internal-policy, label: "Firm Risk Data Aggregation and Reporting Policy v4.2"}

source_posture: mixed

obligations_in_scope:
  - OBL-BCBS239-P03  # Accuracy and integrity
  - OBL-BCBS239-P04  # Completeness
  - OBL-BCBS239-P06  # Adaptability
  - OBL-BCBS239-P07  # Accuracy of reporting
  - OBL-BCBS239-P11  # Distribution

controls:
  - control_id: C-CRR-001
    obligation_id: OBL-BCBS239-P03
    control_objective: "Source-system data feeding the credit-risk pack reconciles to the credit-loss data warehouse of record at month-end with documented variance disposition."
    control_activity: "Credit Risk Reporting team runs monthly reconciliation between credit-loss data warehouse `LGD_v3` extract and the pack input file; variances above firm-policy threshold are dispositioned with named approver."
    control_type: detective
    frequency: monthly
    owner: "Head of Credit Risk Reporting"
    evidence:
      - "credit-loss-data-warehouse:LGD_v3 monthly extract"
      - "reconciliation log path: /grc/crr/recon/<YYYY-MM>"
      - "variance disposition memo (approver named per disposition)"
    test_method: reperformance
    last_test_date: 2026-04-30
    design_effectiveness: effective
    operating_effectiveness: partially-effective
    open_issue_ids: [ISS-2026-CRR-04]

  - control_id: C-CRR-002
    obligation_id: OBL-BCBS239-P04
    control_objective: "All in-scope counterparty exposure data is captured before pack production; identified exclusions are documented with reason and impact."
    control_activity: "Pre-production completeness check against the counterparty master list; exclusions flagged in the pack appendix with reason and impact estimate."
    control_type: preventive
    frequency: monthly
    owner: "Head of Credit Risk Reporting"
    evidence:
      - "completeness check report"
      - "pack appendix exclusions table"
    test_method: inspection
    last_test_date: 2026-04-30
    design_effectiveness: effective
    operating_effectiveness: effective

  - control_id: C-CRR-004
    obligation_id: OBL-BCBS239-P07
    control_objective: "Narrative commentary in the pack reflects the underlying data and is not adjusted for tone after committee preview."
    control_activity: "Head of Credit Risk Reporting signs off on commentary prior to committee distribution; any post-distribution changes require committee chair countersignature."
    control_type: preventive
    frequency: monthly
    owner: "Head of Credit Risk Reporting"
    evidence:
      - "commentary sign-off log"
      - "version-control history on pack file"
    test_method: walkthrough
    last_test_date: 2026-03-31
    design_effectiveness: effective
    operating_effectiveness: not-tested

  - control_id: C-CRR-005
    obligation_id: OBL-BCBS239-P11
    control_objective: "Pack distribution is restricted to named recipients; out-of-cycle distribution requires documented justification."
    control_activity: "DLP-policy-tagged distribution from the document management system; out-of-cycle requests routed through Risk Reporting inbox with approver."
    control_type: preventive
    frequency: event-based
    owner: "Head of Credit Risk Reporting"
    evidence:
      - "DLP distribution log"
      - "out-of-cycle request inbox"
    test_method: inspection
    last_test_date: 2026-04-30
    design_effectiveness: effective
    operating_effectiveness: effective

coverage_gaps:
  - obligation_id: OBL-BCBS239-P06
    gap_description: "Adaptability principle is uncontrolled. Pack regenerates manually under stress scenarios; there is no pre-tested capability to produce ad-hoc cuts (geography, sector, vintage) inside the regulator's typical request window. The firm's stress-testing team can produce slices on request but not within the timing the principle implies."
    recommended_action: "Scope a stand-up of pre-defined ad-hoc cut templates with the Stress Testing team; assign accountable owner; build evidence pathway."

redundancies: []

confidence_label: medium

reviewer_questions:
  - "Does the firm have a documented data-quality threshold framework that names the variance bands and disposition authorities for control C-CRR-001? The reconciliation log references thresholds without an inspectable framework document."
  - "Should adaptability (Principle 6) coverage sit with Credit Risk Reporting or with the Stress Testing function? The gap is real; the owner is contested."
  - "ISS-2026-CRR-04 (recurring reconciliation variances on three counterparties) has been open since 2025-11. Is the operating-effectiveness rating on C-CRR-001 still `partially-effective` or has it slipped?"

human_review_required: true

revisions:
  - {date: 2026-05-06, reason: initial matrix, delta: created from BCBS 239 readiness review scope, approved_by: "Head of Credit Risk Reporting"}
```

## What the matrix surfaces

- The matrix is principle-anchored. Each row points at a BCBS 239 principle and ties evidence to the source-system report (the LGD warehouse extract) and the reconciliation log path, not to the policy document.
- Principle 6 (adaptability) is the un-controlled principle. The matrix surfaces it explicitly in `coverage_gaps` rather than letting it sit silently.
- Confidence is medium because two of the four mapped controls have effectiveness ratings that flex (`partially-effective` on C-CRR-001 with an open issue, `not-tested` on C-CRR-004), and the data-quality threshold framework underneath C-CRR-001 has not been confirmed by the reviewer.
- Reviewer questions are specific to this matrix. They name the obligations, the controls, and the open issue rather than asking generic "is the matrix complete" prompts.
- The matrix consumes the upstream `obligation-mapping` output (the `OBL-BCBS239-*` IDs) and emits the `coverage_gaps[].obligation_id` references back into the obligation set, so the next obligation review knows the adaptability obligation is unmapped and stays open.

## Downstream uses

- `compliance-testing` consumes the controls list to scope its test plan; controls with `last_test_date` older than 18 months go to the top of the test queue.
- `issue-writeup` consumes `open_issue_ids` to ensure each open issue is properly papered with rating, owner, and remediation plan.
- `risk-committee-pack` for the board risk committee references this matrix as the underlying control evidence for the BCBS 239 readiness narrative.
