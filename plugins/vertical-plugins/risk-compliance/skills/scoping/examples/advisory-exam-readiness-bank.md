# Example: advisory exam-readiness sprint at a regional bank

## Input

A consulting team is engaged by a $40B regional bank facing an OCC safety-and-soundness examination starting in 8 weeks. The engagement covers a credit-risk-governance and BSA/AML readiness sprint. The engagement lead is a partner; the audience is the bank's CRO and BSA officer. The bank carries an open MRA on credit concentrations and is on heightened OCC supervisory attention. Source posture is public-plus-firm-policy-plus-evidence; the bank is willing to expose its policy management system and credit-risk system of record to the engagement team.

## Why this scenario matters

This is the canonical advisory-firm exam-readiness use of the skill. The engagement charter has to be tight enough that downstream skills (`evidence-binder`, `control-matrix`, `issue-writeup`, `policy-gap-review`) inherit a clean institution profile, the right primary regulators, and an explicit out-of-scope list. The MRA posture and the OCC heightened attention drive review-gate stringency. The exam window forces a milestone-driven engagement profile.

## Output sketch

```yaml
engagement_id: ENG-2026-OCC-RDY-04
engagement_summary: >
  Eight-week credit-risk-governance and BSA/AML readiness sprint ahead of
  OCC safety-and-soundness exam window opening 2026-07-01. Excludes model
  risk, capital adequacy, and trading-book market risk (separate engagements).
as_of_date: 2026-05-06

institution:
  type: state-member-bank
  asset_size_band: $10-100B
  charter: state-chartered member bank, Delaware
  registrations: [FRB Reg Y holding company, FDIC deposit insurance]
  geographic_footprint: [Mid-Atlantic, six-state branch network]
  primary_regulators:
    - regulator: OCC
      relationship_type: primary-supervisor
      notes: heightened supervisory attention; open MRA on credit concentrations
    - regulator: FRB
      relationship_type: consolidated-supervisor
    - regulator: FDIC
      relationship_type: deposit-insurer
    - regulator: state banking department
      relationship_type: host-state
  recent_supervisory_posture:
    - Open MRA, credit concentrations, issued at 2025-Q3 exam
    - Most recent BSA/AML exam closed without MRA, two informal recommendations

engagement:
  type: exam-readiness-sprint
  sponsor: Chief Risk Officer
  audience: [CRO, BSA officer, internal audit, board risk committee secretary]
  timeframe:
    start: 2026-05-06
    target_completion: 2026-06-30
    milestones:
      - {label: scope sign-off, date: 2026-05-13}
      - {label: evidence inventory complete, date: 2026-05-27}
      - {label: gap-and-remediation memo draft, date: 2026-06-17}
      - {label: exam-response file finalized, date: 2026-06-30}
  deliverable_shape: exam-response-file
  charter_reference: SOW-2026-04 (signed 2026-05-02)

persona:
  role: engagement-partner
  function: advisory (financial-services risk practice)
  decision_rights:
    - approve scope of work and revisions
    - sign off on deliverables before client release
  review_gates:
    - partner approval
    - independent QA (firm-internal)
    - client-side QC (CRO and BSA officer) before any document goes to OCC

source_posture: public-plus-firm-policy-plus-evidence
connectors_enabled:
  - policy management system
  - credit-risk system of record
  - issue-tracking ledger
confidentiality_posture: privileged

risk_lens: [credit, financial-crime, operational]
risk_taxonomy_reference: client risk taxonomy v3.2 (provided 2026-05-04)

sector_overlay_set: [banking]
cross_cutting_overlay_set: [cyber, privacy]

out_of_scope:
  - model risk (covered under separate validation engagement)
  - CCAR / capital adequacy review
  - trading-book market risk
  - third-party risk (handled by client TPRM team in parallel)

assumptions_and_dependencies:
  - MRA remains open through engagement close
  - OCC examiner-in-charge follows the September draft document request list
  - Client risk taxonomy v3.2 is current and stable through 2026-Q3

open_questions:
  - Whether OCC will request expanded testing on commercial real estate concentration
  - Whether BSA/AML scope extends to correspondent-banking program review

revisions:
  - date: 2026-05-06
    reason: initial scope
    delta: charter created
    approved_by: engagement partner, CRO
```

## Why the scope shape matters downstream

- `evidence-binder` reads `connectors_enabled` and `confidentiality_posture` to set its evidence-collection posture.
- `control-matrix` reads `risk_lens` and `sector_overlay_set` to know which control library sections apply.
- `issue-writeup` reads `recent_supervisory_posture` to weight existing MRA context when issues are opened.
- `policy-gap-review` reads `assumptions_and_dependencies` to decide which policy-text snapshots are authoritative.
- The `out_of_scope` list is the deliberate firewall the engagement uses if scope creep arrives mid-sprint.
