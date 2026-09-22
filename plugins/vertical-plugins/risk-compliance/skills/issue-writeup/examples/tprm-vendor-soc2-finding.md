# Example: TPRM critical-vendor SOC 2 qualified-opinion finding

## Input

The Vendor Risk Management team at a mid-sized broker-dealer (registered with the SEC and FINRA, also state-licensed in 38 states) has received the most recent SOC 2 Type II report for its critical fraud-screening vendor (the vendor screens 100% of new account openings and a sample of high-risk transactions). The SOC 2 Type II report covers the period 2025-04-01 through 2026-03-31 and carries a qualified opinion on Trust Services Criterion CC6.1 (logical access). The qualifying paragraph notes that during the audit period the vendor's privileged-access reviews were not performed at the contractually committed quarterly cadence on two of four quarters. The firm has no documented compensating control on its side. The Head of Vendor Risk has confirmed the condition with the vendor's customer-success team and is writing up the issue. Persona is the Head of Vendor Risk Management (2-line independent), audience is the Vendor Risk Committee with a copy to the Operational Risk Committee. Source posture is mixed: Interagency Guidance on Third-Party Relationships and NYDFS Part 500 (public), and the firm's third-party policy (firm-policy overlay).

## Why this scenario matters

Vendor-monitoring exceptions are the most common second-line finding in many firms; the SOC 2 qualified-opinion case is the canonical version. The example tests the discipline that vendor findings name the specific Trust Services Criterion, that the firm-side compensating control is itself a control attribute under review, and that severity is calibrated against vendor criticality, customer-data exposure, and the absence of a compensating control. It also tests the cyber cross-cutting overlay: the criterion is a cyber-tagged finding, and the criteria section pulls from both the TPRM source anchors and the cyber overlay.

## Output sketch

```yaml
issue_id: ISS-2026-VRM-Vendor-Atlas-014
title: "Critical fraud-screening vendor SOC 2 Type II qualified opinion on logical access (CC6.1) without firm-side compensating control"
engagement_id: ENG-2026-VRM-Q2-Critical-Vendor-Review
as_of_date: 2026-04-28
status: under-review

source:
  source_type: vendor-monitoring
  source_id: VRM-MON-2026-Q2-Atlas-001
  # regulator omitted; not examiner-issued

date_identified: 2026-04-25
period_start: 2025-04-01
period_end: 2026-03-31

condition: |
  The SOC 2 Type II report for fraud-screening vendor [vendor codename Atlas] covering
  2025-04-01 through 2026-03-31 carries a qualified opinion on Trust Services Criterion CC6.1
  (logical access). The qualifying paragraph notes that during the audit period the vendor's
  privileged-access reviews were not performed at the contractually committed quarterly cadence
  on Q3 2025 and Q1 2026. The firm has reviewed the qualified opinion and confirmed with the
  vendor's customer-success team that the cadence gap occurred. The firm has no documented
  compensating control on its side: there is no firm-performed review of the vendor's privileged-
  access roster, no firm-side requirement that the vendor evidence quarterly review prior to
  contract renewal, and no firm-side detective control to flag missed reviews between SOC report
  cycles.

criteria: |
  Interagency Guidance on Third-Party Relationships: Risk Management (OCC / FRB / FDIC, June
  2023) §III.D ongoing monitoring — the firm should monitor critical third parties' performance
  against contractual and risk-management expectations on a basis commensurate with the criticality
  of the relationship. NYDFS 23 NYCRR §500.11(a) — third-party service-provider security policy,
  including periodic assessment based on the risk presented and the continued adequacy of the
  third party's cybersecurity practices. Firm Third-Party Risk Management Policy v3.5 §4.3
  (critical-vendor monitoring) and §4.7 (compensating-control matrix for critical vendors with
  qualified or adverse SOC opinions).
criteria_source_anchor: "references/source-anchors.md#interagency-tprm-2023, references/cross-cutting/cyber.md#nydfs-500, references/firm-overlay.md#tprm-policy-v35"

cause: |
  The firm-side ongoing-monitoring control (C-VRM-007) requires review of received SOC 2 reports
  for qualified opinions, but the control's design does not include a downstream step to compare
  the qualified opinion against a firm-side compensating-control matrix and trigger a remediation
  workflow when no compensating control is documented. The control's review step ends at
  receipt-and-noting; the gap is the missing trigger from "qualified opinion received" to
  "compensating control evaluated, documented, or scheduled." The vendor's own privileged-access
  review cadence is the vendor's control, not the firm's; the firm's control is the monitoring
  workflow that should have surfaced the absence of a compensating response.

impact: |
  Operational and cyber: residual risk on customer-data access at the vendor for the period the
  vendor's privileged-access review cadence slipped, with no firm-side detective or compensating
  control mitigating the residual risk. Customer: the vendor screens 100% of new account openings
  and a sample of high-risk transactions; nonpublic customer information is in scope of the
  vendor's privileged access. No identified customer-data exposure event during the period; the
  vendor reports no incident, but the firm has limited visibility absent the compensating control.
  Regulatory: NYDFS continuous-supervisory expectation on §500.11 third-party programs; SEC OCIE
  attention on broker-dealer vendor oversight via Reg S-P (customer-information safeguards) is
  in scope. Reputational: low; no public-facing event identified.

severity: high
severity_rationale: |
  High because the vendor is critical (100% of new account openings; high-risk transaction
  screening), nonpublic customer information is in the vendor's privileged-access scope, the
  cadence slip persisted across two of four quarters of the SOC audit period, and there is no
  firm-side compensating control. Not critical because no customer-data exposure event has been
  identified and the vendor has now committed to and evidenced corrective action on cadence;
  the firm-side control gap is the structural weakness, not a confirmed harm event.
compensating_controls: []

# mra_mria_classification omitted; source is vendor-monitoring, not examiner-letter.
# The cyber cross-cutting overlay is loaded; see references/cross-cutting/cyber.md.

# population/sample fields omitted; this is not a sample-based test
linked_obligation_ids: [OBL-TPRM-IIID-OngoingMon, OBL-NYDFS-500-11]
linked_control_ids: [C-VRM-007]
linked_evidence_ids: [EV-2026-VRM-Atlas-Q2-A, EV-2026-VRM-Atlas-Q2-B]

recommendation: |
  The Head of Vendor Risk Management must (1) document a compensating control for the period
  the vendor's cadence slipped and for any future periods where vendor SOC reports carry a
  qualified or adverse opinion on logical-access criteria, (2) redesign control C-VRM-007 to
  include a downstream trigger from qualified-opinion-noted to compensating-control-evaluated,
  with a named approver and documented decision, and (3) initiate a vendor remediation tracking
  record for Atlas covering the cadence slip and the firm's expectation of evidenced quarterly
  reviews going forward.

remediation: |
  Three-part remediation: compensating-control documentation, control redesign, and vendor
  remediation tracking. The control redesign is the structural fix that prevents recurrence
  across the vendor portfolio; the compensating-control documentation closes the specific Atlas
  exposure; the vendor remediation tracking is the firm's leverage on the vendor.

owner: "Head of Vendor Risk Management"
target_date: 2026-07-31
remediation_milestones:
  - {date: 2026-05-15, milestone: "Compensating control for Atlas documented and approved by Vendor Risk Committee", owner: "Head of Vendor Risk Management"}
  - {date: 2026-06-30, milestone: "Control C-VRM-007 redesign signed off by Head of Operational Risk", owner: "Head of Vendor Risk Management"}
  - {date: 2026-07-31, milestone: "Vendor remediation tracking record opened with Atlas; first cadence-evidence cycle delivered by vendor", owner: "Head of Vendor Risk Management"}

closure_evidence:
  - "Compensating-control documentation for Atlas with named approver, retained in GRC platform vendor record"
  - "Updated control documentation for C-VRM-007 with downstream qualified-opinion trigger workflow"
  - "Two consecutive quarters of vendor-evidenced privileged-access reviews from Atlas, retained in vendor monitoring record"
  - "Vendor remediation tracking record with status, owner, and target dates, retained in GRC platform"

interim_mitigation: |
  Firm-side ad-hoc privileged-access roster review against vendor-provided current-state list,
  performed by Vendor Risk Analyst with named approver, until the structural redesign is signed
  off. Evidenced by analyst sign-off log retained in the GRC platform. The interim check is the
  mitigation while the redesign and the vendor's evidenced cadence land.

evidence_gap: true
evidence_gap_note: |
  Vendor has not yet provided firm-side visibility into the privileged-access roster as of the
  cadence slip period; the firm cannot independently verify the slip's customer-data exposure
  scope. Routed to engagement issue log as item ENG-2026-VRM-Q2-IL-003.

confidence_label: medium

reviewer_questions:
  - "Should the redesigned C-VRM-007 trigger workflow apply to all vendor SOC report qualified opinions across logical-access, change-management, and incident-response criteria, or only to logical-access? Scope expansion adds work but covers more failure modes."
  - "Is the 2026-07-31 target date acceptable to the Vendor Risk Committee given the customer-data exposure scope, or should the compensating-control documentation milestone (2026-05-15) move forward?"
  - "Does the firm need to refresh its NYDFS §500.11 third-party annual assessment of Atlas to reflect the qualified opinion, or does the SOC report itself satisfy the assessment requirement until the next annual cycle?"
  - "Should the firm's broker-dealer Reg S-P safeguards-rule program incorporate this finding into the next safeguards-program review, or is the TPRM track sufficient?"

human_review_required: true

revisions:
  - {date: 2026-04-28, reason: initial write-up, delta: created from VRM-MON-2026-Q2-Atlas-001, approved_by: "Head of Vendor Risk Management"}
```

## What the write-up surfaces

- The condition names the specific Trust Services Criterion (CC6.1), the qualified-opinion period (2025-04-01 through 2026-03-31), the cadence slip (Q3 2025 and Q1 2026), and the absence of a compensating control. The firm's confirmation step with the vendor's customer-success team is named, so the reviewer can trace the confirmation pathway.
- Criteria pulls from three sources: Interagency TPRM Guidance §III.D, NYDFS §500.11(a), and the firm's TPRM policy. Each is named with section. The criteria_source_anchor field points at the source-anchors entry, the cyber cross-cutting overlay (because §500.11 is a cyber criterion), and the firm-overlay. The reviewer can read all three.
- The cause names the specific control attribute that failed: control C-VRM-007 ends at receipt-and-noting and lacks the downstream trigger to compensating-control evaluation. The cause is not "vendor failed" or "monitoring weakness". The vendor's failure is named separately as the upstream condition that the firm-side control should have caught.
- The effect identifies operational, cyber, customer, regulatory, and reputational impact distinctly. Customer impact is "no identified exposure event" rather than "no impact" because the firm has limited visibility absent the compensating control; the honesty matters for severity defensibility.
- Severity rationale references vendor criticality, customer-data exposure scope, frequency (two of four quarters), and the absence of compensating controls. The "not critical" reasoning ties to the absence of a confirmed harm event; that is the boundary the firm will defend if the severity is challenged at the Vendor Risk Committee.
- Compensating controls field is the empty array. The empty array carries the signal explicitly; it is not omission.
- Evidence gap is yes: the vendor has not yet provided privileged-access roster visibility for the slip period. The gap routes to the engagement issue log with a specific item ID.
- Closure evidence is the artifact across all three remediation lines: documentation, redesigned control, evidenced quarters from the vendor, opened remediation record. None of the closure evidence reads as the verb.
- Reviewer questions tie to specific decision points (scope of redesign, target-date defensibility, NYDFS §500.11 assessment cycle, Reg S-P seam) rather than generic "is this complete?" prompts.

## Downstream uses

- `compliance-testing` consumes `severity`, `linked_control_ids`, and `closure_evidence` to schedule a focused test of C-VRM-007 once the redesign is evidenced.
- `risk-committee-pack` for the next Vendor Risk Committee and Operational Risk Committee references this issue's `severity`, `evidence_gap`, and `target_date` in the open-critical-vendor-issues section.
- `control-matrix` reads `linked_control_ids` to surface ISS-2026-VRM-Vendor-Atlas-014 against the C-VRM-007 row in the vendor-lifecycle matrix; the open issue's severity drops the control's operating-effectiveness rating to partially-effective until closure.
- `vendor-diligence` (when the firm runs an Atlas re-diligence) consumes the issue and the closure evidence as a precondition for vendor re-tier or contract renewal decisions.
- The cyber cross-cutting overlay is loaded; the next CISO-led continuous-monitoring readout reads this issue as a cyber-tagged finding via the cross-cutting overlay path.
