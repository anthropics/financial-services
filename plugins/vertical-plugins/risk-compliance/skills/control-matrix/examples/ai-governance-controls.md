# Example: model-risk control matrix for an internal-build credit-decisioning ML model

## Input

A national bank's Model Risk Management Office is building the control matrix for a tier-1 retail credit-decisioning model used in unsecured personal-loan origination. The model is a gradient-boosted classifier developed in-house; it influences approve/decline and pricing tier. The persona is the Head of Model Risk (2-line, independent of model development); the audience is the Model Risk Committee, with the matrix later cited in the SR 11-7 / OCC Bulletin 2026-13 program documentation and in the model card. Source posture is mixed: SR 11-7, OCC Bulletin 2026-13, ECOA / Reg B (public) plus the firm's Model Risk Policy and the Adverse Action Notice Standard (firm-policy overlay). Sector overlay: banking. Cross-cutting overlay: cyber (the model's serving environment is in scope of the firm's NYDFS Part 500 program).

## Why this scenario matters

This is the canonical model-risk application of the matrix and is the matrix that `model-card-builder` consumes for its controls section. It tests three things at once: obligation-anchoring across multiple regulator surfaces (model-risk supervisory guidance plus consumer-compliance rule plus cyber regulation), the control-type discipline (preventive / detective / response / compensating), and the seam where firm policy operationalises a principle-based supervisory expectation. The matrix has to be readable line-by-line by an examiner under SR 11-7 and by a CFPB exam team probing Reg B adverse-action specificity.

## Output sketch

```yaml
matrix_id: CM-2026-MRM-RET-CR-04
as_of_date: 2026-05-06
engagement_id: ENG-2026-MRM-ANNUAL-12

scope:
  process_or_product: "Tier-1 retail credit-decisioning model lifecycle: development, validation, deployment, monitoring, change management, retirement"
  business_unit: "Retail Credit Underwriting (model owner: Retail Credit Risk; model developer: Decision Sciences)"
  jurisdiction: "US"
  lines_of_defense: ["1L", "2L"]

source_list:
  - {source_type: supervisory-letter, label: "SR 11-7 (interagency model risk management guidance, 2011)", section_reference: "§IV development, §V validation, §VI governance and controls"}
  - {source_type: interagency-guidance, label: "OCC Bulletin 2026-13 (revised interagency model risk management guidance, 2026)", section_reference: "§III.A control environment, §III.B third-party model controls"}
  - {source_type: rule, label: "Regulation B (12 CFR Part 1002)", section_reference: "§1002.9 adverse action notice"}
  - {source_type: examination-manual, label: "CFPB Circular 2022-03 (adverse action notice using AI/algorithms; withdrawn May 12, 2025; historical only)"}
  - {source_type: internal-policy, label: "Firm Model Risk Policy v6.1"}
  - {source_type: internal-standard, label: "Adverse Action Notice Standard v3.0"}

source_posture: mixed

obligations_in_scope:
  - OBL-SR11-7-IV     # Development soundness
  - OBL-SR11-7-V      # Independent validation
  - OBL-SR11-7-VI     # Governance, policies, controls
  - OBL-OCC-2026-13-IIIA  # Control environment refresh
  - OBL-RegB-1002.9   # Adverse action notice specificity

controls:
  - control_id: C-MRM-101
    obligation_id: OBL-SR11-7-IV
    control_objective: "Model development is performed against the firm's Model Development Standard, with documented design rationale, data sourcing decisions, and out-of-time backtest results before submission for validation."
    control_activity: "Decision Sciences submits the model development memo and reproducible build artefacts to the Model Inventory at development completion; sign-off by Head of Decision Sciences gates submission to validation."
    control_type: preventive
    frequency: event-based
    owner: "Head of Decision Sciences"
    evidence:
      - "Model Inventory entry MIN-2026-RET-CR-04"
      - "model development memo path"
      - "reproducible build artefact bundle"
    test_method: inspection
    last_test_date: 2026-02-14
    design_effectiveness: effective
    operating_effectiveness: effective

  - control_id: C-MRM-102
    obligation_id: OBL-SR11-7-V
    control_objective: "Independent validation runs before production deployment and at the firm's defined re-validation cadence; validator is independent of development."
    control_activity: "Model Validation team produces validation report covering conceptual soundness, data and design, performance, robustness, and limitations; report is signed by Head of Model Validation and tabled at Model Risk Committee."
    control_type: preventive
    frequency: "event-based plus annual re-validation"
    owner: "Head of Model Validation"
    evidence:
      - "validation report VAL-2026-RET-CR-04"
      - "Model Risk Committee minutes 2026-03-22"
      - "validator independence attestation"
    test_method: inspection
    last_test_date: 2026-03-22
    design_effectiveness: effective
    operating_effectiveness: effective

  - control_id: C-MRM-104
    obligation_id: OBL-SR11-7-VI
    control_objective: "Production performance is monitored against documented thresholds; threshold breaches trigger documented investigation, escalation, and (where warranted) re-validation."
    control_activity: "Model Performance Monitoring team produces monthly monitoring report covering AUC, KS, PSI on inputs, score-distribution drift, segment performance, and approval-rate drift. Threshold breaches escalate to Head of Model Risk and Head of Retail Credit Risk."
    control_type: detective
    frequency: monthly
    owner: "Head of Model Performance Monitoring (within MRMO)"
    evidence:
      - "monthly monitoring report MON-2026-04"
      - "threshold-breach escalation log"
      - "PSI breach investigation memo (when triggered)"
    test_method: data-analysis
    last_test_date: 2026-04-30
    design_effectiveness: effective
    operating_effectiveness: partially-effective
    open_issue_ids: [ISS-2026-MRM-09]

  - control_id: C-MRM-201
    obligation_id: OBL-RegB-1002.9
    control_objective: "Adverse action notices generated on declines from this model state the specific, accurate principal reasons for the credit decision, consistent with Regulation B §1002.9 (CFPB Circular 2022-03, which restated this point, was withdrawn May 12, 2025; the obligation survives on the regulation)."
    control_activity: "Reason-code mapping from model output to the firm's adverse-action reason library is maintained by the Adverse Action Standard owner; monthly sampling of adverse-action notices by Consumer Compliance to confirm specificity and accuracy."
    control_type: detective
    frequency: monthly
    owner: "Head of Consumer Compliance (sampling); Adverse Action Standard owner (mapping)"
    evidence:
      - "reason-code mapping table v3.0"
      - "monthly notice sampling report"
      - "exception log for notices flagged as non-specific"
    test_method: inspection
    last_test_date: 2026-04-30
    design_effectiveness: effective
    operating_effectiveness: effective

  - control_id: C-MRM-301
    obligation_id: OBL-OCC-2026-13-IIIA
    control_objective: "Material model changes (feature change, training-window shift, score-cutoff change, performance-breach-driven re-fit) trigger documented change-management review prior to deployment."
    control_activity: "Change Management Workflow in the Model Inventory routes material changes to Head of Model Risk for sign-off; deployment is gated on sign-off."
    control_type: preventive
    frequency: event-based
    owner: "Head of Model Risk"
    evidence:
      - "change-management workflow record"
      - "sign-off log in Model Inventory"
    test_method: walkthrough
    last_test_date: 2026-01-15
    design_effectiveness: effective
    operating_effectiveness: effective

  - control_id: C-MRM-401
    obligation_id: OBL-OCC-2026-13-IIIA
    control_objective: "Production-environment access to the model artefact, scoring service, and decisioning logs is least-privilege and logged."
    control_activity: "InfoSec maintains access-control matrix for the model serving environment; quarterly access review by Head of Model Risk and by InfoSec; logs reviewed for anomalies under the firm's NYDFS Part 500 program."
    control_type: preventive
    frequency: "continuous (logging) + quarterly (review)"
    owner: "CISO function (access logging); Head of Model Risk (model-side review)"
    evidence:
      - "access-control matrix"
      - "quarterly access-review attestation"
      - "audit log sample"
    test_method: inspection
    last_test_date: 2026-03-31
    design_effectiveness: effective
    operating_effectiveness: effective

coverage_gaps:
  - obligation_id: OBL-SR11-7-V
    gap_description: "Annual re-validation has been performed for this model, but the SR 11-7 §V expectation that validation address ongoing monitoring outcomes (not just point-in-time performance) is only partially evidenced. The validation report references the monitoring suite without independently testing the monitoring thresholds."
    recommended_action: "Validation team to independently test the monitoring thresholds in the next annual cycle; document in the validation report."

redundancies: []

confidence_label: high

reviewer_questions:
  - "ISS-2026-MRM-09 records a PSI breach on `debt_to_income` ratio that has been investigated but not closed; should the model carry a heightened-monitoring posture pending closure?"
  - "Adverse action notice sampling (C-MRM-201) is performed by Consumer Compliance, not by MRMO. Does the Model Risk Policy expect MRMO independent sampling on top of the Consumer Compliance sample?"
  - "C-MRM-401 is jointly owned (CISO function and Head of Model Risk). Is the joint ownership documented in the firm's RACI for the NYDFS Part 500 program, or only in this matrix?"

human_review_required: true

revisions:
  - {date: 2026-05-06, reason: initial matrix, delta: created during MRMO annual model inventory refresh, approved_by: "Head of Model Risk"}
```

## What the matrix surfaces

- Obligation-anchoring across three regulatory surfaces: SR 11-7 / OCC Bulletin 2026-13 (model risk), Reg B (consumer compliance), and the cyber overlay onto OCC Bulletin 2026-13 §III.A (control environment) via NYDFS Part 500 access controls. The matrix names each.
- Control-type discipline: C-MRM-101 (preventive: documentation gate on validator submission), C-MRM-102 (preventive: independence-tested validation), C-MRM-104 (detective: monthly monitoring with breach escalation), C-MRM-201 (detective: reason-specificity sampling), C-MRM-301 (preventive: change-management gate), C-MRM-401 (preventive: access controls). No response controls in this slice; if a model failure event triggers a response runbook, that goes in a separate row.
- Joint ownership is captured explicitly. C-MRM-401 names CISO function and Head of Model Risk; the reviewer question probes whether the joint ownership is papered in the firm's NYDFS RACI.
- The reviewer questions are specific. None of them ask generic "is the matrix complete"; each names a control or an obligation.
- Coverage gap is partial-mapping, not absent-mapping: SR 11-7 §V is mapped, but the validation expectation around monitoring-outcome testing is only partially evidenced. The matrix surfaces the partial seam rather than rating the obligation green.

## Downstream uses

- `model-card-builder` consumes the controls list as the model card's controls section; control IDs in the card cross-reference back to this matrix.
- `compliance-testing` consumes the matrix to scope SR 11-7 compliance test work; the C-MRM-201 sampling cadence informs the test scope on Reg B notice quality.
- `issue-writeup` consumes ISS-2026-MRM-09 to ensure the open PSI-breach issue is properly papered with rating, owner, and remediation plan.
- `exam-brief` for an OCC safety-and-soundness or CFPB exam pulls this matrix as evidence of the firm's model-risk control framework for retail credit decisioning.
- The banking sector overlay (`references/sector-overlays/banking.md`) drives the inclusion of the Reg B obligation row (CFPB Circular 2022-03 was withdrawn May 12, 2025; historical only); without the overlay, the matrix would be SR 11-7-only and would miss the consumer-compliance surface that an exam will probe.
