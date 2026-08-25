# Example: FFIEC BSA/AML CDD obligation register for a payments fintech bank-sponsor partnership

## Input

A consumer-payments fintech operates under a bank-sponsor partnership. The fintech provides the user-facing product; the sponsor bank holds the deposit relationship and bears the BSA/AML obligation as the covered financial institution. The fintech is refreshing its CDD obligation register against the FFIEC BSA/AML Examination Manual (current edition, 2024 update), 31 CFR 1010.230 (beneficial ownership), 31 CFR 1020 (CDD for banks), and the bank-sponsor agreement allocating CDD activities. Source posture is public-plus-firm-policy: the public regulatory anchors plus the executed sponsor agreement and the fintech's CDD policy. The engagement sponsor is the fintech's BSA Officer; legal counsel for the sponsor bank is engaged for cross-party allocation questions.

## Why this scenario matters

This is the canonical mapping where obligations have to extract on both sides of a third-party relationship. The bank carries the regulatory obligation under 31 CFR 1020 and 1010.230; the fintech carries the operational obligation under the sponsor agreement; the BSA Officer at the bank ultimately attests. The register has to extract the bank-side and fintech-side obligations as separate rows, has to anchor the fintech-side rows in the sponsor agreement (a contractual source) rather than the rule (which addresses the bank), and has to surface the allocation language as the obligation text. It tests the skill's discipline on multi-party source labelling and on the rule-anchored discipline (a fintech-side row whose only source is fintech policy, with no sponsor-agreement clause underneath, fails the discipline).

## Output sketch

```yaml
register_id: REG-2026-BSA-CDD-FT-01
as_of_date: 2026-05-06
scope_ref: ENG-2026-FT-BSA-01

scope:
  process: customer onboarding, customer due diligence, beneficial ownership identification, ongoing monitoring
  product: consumer payments product under bank-sponsor partnership
  business_unit: payments operations and BSA/AML
  jurisdiction: federal (FinCEN, OCC for sponsor bank)
  period_start: 2026-05-06
  register_type: refresh

source_posture: public-plus-firm-policy

sources:
  - source_name: FFIEC BSA/AML Examination Manual
    issuer: FFIEC
    edition: current online edition, 2024 update referenced
    date: 2024-08-01 [verify update-cycle date]
    url: https://bsaexaminationmanual.ffiec.gov/
    source_type: exam-manual
  - source_name: FinCEN beneficial ownership rule
    issuer: FinCEN
    date: 2018-05-11
    url: https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010/subpart-D/section-1010.230
    source_type: rule-text
  - source_name: CDD for banks
    issuer: FinCEN / OCC / FRB / FDIC
    date: as currently codified
    url: https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1020
    source_type: rule-text
  - source_name: Bank-sponsor agreement, fintech and sponsor bank
    issuer: sponsor bank and fintech (private contract)
    edition: as amended through 2025-Q4
    date: 2025-12-15
    url: internal contract repository, document ID PARTNERSHIP-AGR-2024-001
    source_type: third-party-sla

obligations:
  - obligation_id: OBL-001
    source_citation: FFIEC BSA/AML Examination Manual, Customer Due Diligence section
    source_section: CDD core elements [verify chapter labels in current online edition]
    source_url: https://bsaexaminationmanual.ffiec.gov/
    regulator: FFIEC (bank-sponsor exam authority)
    requirement_summary: >
      The covered financial institution must develop a customer risk profile for each
      customer, including the nature and purpose of the customer relationship, sufficient
      to inform suspicious activity monitoring.
    applicability: >
      Sponsor bank as covered financial institution under 31 CFR 1020; obligation runs
      to the bank, with operational support from the fintech under the sponsor agreement.
    effective_date: in force
    impacted_process: customer onboarding and ongoing monitoring
    control_objective: >
      Every customer record carries a documented customer risk profile reviewed at
      onboarding and refreshed on a risk-based cadence.
    evidence_required:
      - Customer risk profile records in the sponsor bank's BSA system of record
      - Risk-rating refresh cadence sign-off log
    owner: Sponsor bank BSA Officer
    status: approved
    confidence: high
    tags: [financial-crime, bank-side]

  - obligation_id: OBL-002
    source_citation: FinCEN, 31 CFR 1010.230
    source_section: §1010.230(b)(1) (identification) and §1010.230(b)(2) (verification)
    source_url: https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010/subpart-D/section-1010.230
    regulator: FinCEN
    requirement_summary: >
      The covered financial institution must identify and verify the identity of each
      beneficial owner of a legal-entity customer at account opening using the
      certification-form mechanism or its substantive equivalent.
    applicability: >
      Sponsor bank as covered financial institution; legal-entity customers opened
      through the fintech-sponsored product flow; not applicable to consumer accounts
      since the rule addresses legal-entity customers.
    effective_date: in force since 2018-05-11
    impacted_process: legal-entity customer onboarding
    control_objective: >
      Every legal-entity customer record contains a §1010.230 certification (or
      substantive equivalent) and verification documentation retained per §1010.230(i).
    evidence_required:
      - §1010.230 certification forms or substantive equivalents in onboarding records
      - Verification documentation (government-issued ID copies, control-prong evidence)
      - Recordkeeping retention proof per §1010.230(i)
    owner: Sponsor bank BSA Officer
    status: approved
    confidence: high
    tags: [financial-crime, bank-side]

  - obligation_id: OBL-003
    source_citation: Bank-sponsor agreement, CDD allocation
    source_section: §4.2 (CDD operational responsibilities of the fintech)
    source_url: internal contract repository, PARTNERSHIP-AGR-2024-001
    regulator: contractual; flows back to the bank's regulatory obligation under 31 CFR 1020
    requirement_summary: >
      The fintech must collect, verify, and transmit CIP and CDD information for each
      customer to the sponsor bank within the timeframes specified in §4.2(c) of the
      sponsor agreement, using the data fields and verification standards the bank's
      written CDD program requires.
    applicability: >
      Fintech onboarding flow for the consumer-payments product; runs only as long as
      the sponsor agreement is in effect.
    effective_date: as of sponsor-agreement execution; current amendment effective 2025-12-15
    impacted_process: customer onboarding (fintech-side)
    control_objective: >
      The fintech delivers CIP and CDD data to the sponsor bank in the §4.2(c) format
      and within the §4.2(c) timeframe, with no incomplete records advancing to the
      bank's BSA system of record.
    evidence_required:
      - Onboarding-flow sample showing field-by-field CIP/CDD capture
      - Daily reconciliation log between fintech onboarding system and bank BSA system
      - Exception report for records that failed verification
    owner: Fintech BSA Lead (operational); sponsor bank BSA Officer (regulatory accountability)
    status: in-review
    confidence: medium
    open_questions:
      - "Whether the §4.2(c) reconciliation cadence (daily) is sufficient if the bank's CDD program later requires near-real-time reconciliation; depends on the bank's program update."
    tags: [financial-crime, fintech-side, third-party-allocation]

  - obligation_id: OBL-004
    source_citation: Bank-sponsor agreement, beneficial-ownership allocation
    source_section: §4.4 (BO collection and verification responsibilities)
    source_url: internal contract repository, PARTNERSHIP-AGR-2024-001
    regulator: contractual; flows to the bank's §1010.230 obligation
    requirement_summary: >
      The fintech must collect and verify §1010.230 beneficial-owner information for
      legal-entity customers it onboards and transmit the certification record to the
      sponsor bank for retention; the sponsor bank retains regulatory accountability.
    applicability: legal-entity customer onboarding through the fintech-sponsored flow
    effective_date: as of sponsor-agreement execution
    impacted_process: legal-entity customer onboarding (fintech-side)
    control_objective: >
      Every legal-entity customer onboarded via the fintech reaches the bank's BSA
      system of record with a §1010.230-compliant certification and verification
      package, or is rejected at the fintech intake gate.
    evidence_required:
      - §1010.230 certification records flowing fintech to bank with timestamped handoff
      - Rejection log for legal-entity customers that failed BO verification at intake
    owner: Fintech BSA Lead (operational); sponsor bank BSA Officer (regulatory accountability)
    status: open-question
    confidence: medium
    open_questions:
      - "Whether the fintech can rely on the sponsor bank's §1010.230 control-prong verification rather than performing its own; depends on bank's written program and the §4.4 carve-out language. Routes to sponsor bank legal."
    tags: [financial-crime, fintech-side, third-party-allocation]

open_question_summary:
  - obligation_ids: [OBL-004]
    question: "Whether fintech can rely on sponsor bank for §1010.230 control-prong verification, or must perform its own; depends on §4.4 sponsor-agreement carve-out and bank's written CDD program"
    reviewer: external-counsel
    target_resolution_date: 2026-06-01
  - obligation_ids: [OBL-003]
    question: "Whether daily reconciliation cadence is sufficient if bank's CDD program later moves to near-real-time"
    reviewer: function-head
    target_resolution_date: 2026-07-01

applicability_notes: >
  Bank-side obligations (OBL-001, OBL-002) flow to the sponsor bank as the covered
  financial institution; the bank's BSA Officer attests these. Fintech-side obligations
  (OBL-003, OBL-004) are contractual and flow back to the bank's regulatory obligation
  through the sponsor agreement; the fintech's BSA Lead is the operational owner, the
  bank's BSA Officer remains regulatorily accountable. The obligation pair-up is the
  point of the register and is explicit in the owner column.

confidence_label: mixed
human_review_required: true

reviewer:
  role: Sponsor bank BSA Officer; fintech BSA Lead countersigns operational rows
  review_status: pending

revisions:
  - date: 2026-05-06
    reason: refresh against 2024 manual update and amended sponsor agreement
    delta: added OBL-003 and OBL-004 to reflect §4.2 and §4.4 amendment language
    approved_by: fintech BSA Lead
```

## Why the register shape matters downstream

- `control-matrix` builds bank-side rows and fintech-side rows distinctly; the same control objective on both sides will not collapse to one row because the source is different.
- `policy-gap-review` triangulates the fintech's CDD policy against the sponsor agreement and the bank's written CDD program, flagging gaps where the fintech policy does not cover the §4.2 or §4.4 obligations.
- `evidence-binder` reads `OBL-003.evidence_required` and scopes the daily-reconciliation evidence ask, which is the test most likely to surface defects.
- `exam-brief` reads the register if the OCC examiner asks the bank "how do you discharge §1010.230 when the customer was onboarded via the fintech"; OBL-002, OBL-004, and the open-question on §4.4 carve-out are the answer chain.
