# Example: CFPB Section 1071 obligation register for a community bank

## Input

A community bank subject to the CFPB Section 1071 small-business lending data collection rule is mapping its obligations from the rule and the final-rule preamble. The bank originates roughly 1,200 covered small-business credit transactions per year, putting it above the **§1071 revised final rule (May 1, 2026)** single 1,000-transaction threshold (which supersedes the 2023 tiered schedule of 2,500 / 500 / 100). Source posture is public-only: 12 CFR 1002.107, 12 CFR 1002.105 (covered financial institution), 12 CFR 1002.110 (reporting), 12 CFR 1002.111 (recordkeeping), the May 2026 revised final rule, and the original CFPB final-rule preamble. The bank's CCO is the engagement sponsor; legal counsel reviews open questions.

## Why this scenario matters

Section 1071 is the canonical mid-complexity register a community bank stands up: the rule has lifecycle-stage obligations, an applicability threshold that needs explicit reasoning, and at least one design obligation (the firewall) that requires legal review. Under the May 2026 revised final rule, the threshold is a single 1,000-covered-transactions trigger (effective June 30, 2026; compliance January 1, 2028) and the older tier-by-tier compliance-date schedule is gone. The register has to be honest about the threshold and effective-date posture under the revised rule, and has to push the firewall obligation to legal in `open-question` status rather than guessing. It tests the skill's discipline on threshold reasoning, effective-date capture under a recently-amended rule, and routing of design obligations.

## Output sketch

```yaml
register_id: REG-2026-1071-CB-01
as_of_date: 2026-05-06
scope_ref: ENG-2026-CB-1071-01

scope:
  process: small-business credit application intake, underwriting, recordkeeping, and reporting
  business_unit: small-business lending
  jurisdiction: federal (CFPB)
  period_start: 2026-05-06
  register_type: fresh-build

source_posture: public-only

sources:
  - source_name: CFPB Section 1071 Revised Final Rule
    issuer: CFPB
    edition: Revised final rule, May 1, 2026 (1,000-transaction threshold; effective June 30, 2026; compliance January 1, 2028)
    date: 2026-05-01
    url: https://www.consumerfinance.gov/rules-policy/final-rules/small-business-lending-under-the-equal-credit-opportunity-act-regulation-b/
    source_type: rule-text
  - source_name: CFPB Section 1071 Final Rule (2023, as codified — superseded compliance-date schedule)
    issuer: CFPB
    edition: Final, March 30, 2023, as codified
    date: 2023-03-30
    url: https://www.ecfr.gov/current/title-12/chapter-X/part-1002/subpart-B
    source_type: rule-text

obligations:
  - obligation_id: OBL-001
    source_citation: CFPB, 12 CFR 1002.105
    source_section: §1002.105(b)
    source_url: https://www.ecfr.gov/current/title-12/chapter-X/part-1002/subpart-B/section-1002.105
    regulator: CFPB
    requirement_summary: >
      A covered financial institution that originated at least 1,000 covered originations
      in each of the two preceding calendar years must comply with the data-collection,
      reporting, and recordkeeping requirements of Subpart B (§1002.105(b) under the
      May 2026 revised final rule; supersedes the 2023 100-origination threshold).
    applicability: >
      Community bank originating roughly 1,200 covered small-business credit transactions
      per year; meets the §1002.105(b) revised 1,000-transaction threshold.
    applicability_thresholds:
      covered_origination_threshold: 1000
      notes: bank originated ~1,200 covered transactions in each of 2024 and 2025
    effective_date: 2026-06-30
    effective_date_phase_in: >
      §1071 revised final rule (May 1, 2026): rule effective June 30, 2026; compliance
      date January 1, 2028. The 2023 tiered (high / moderate / low volume) schedule is
      superseded.
    impacted_process: small-business credit application intake
    control_objective: >
      The bank correctly identifies itself as a covered financial institution under §1002.105
      and applies the data-collection regime to all covered applications.
    evidence_required:
      - Annual covered-origination tally with supporting loan-system extract
      - Compliance committee acknowledgement of covered-FI status
    owner: Chief Compliance Officer
    status: in-review
    confidence: high
    tags: [consumer-compliance, fair-lending, banking]

  - obligation_id: OBL-002
    source_citation: CFPB, 12 CFR 1002.107
    source_section: §1002.107(a)
    source_url: https://www.ecfr.gov/current/title-12/chapter-X/part-1002/subpart-B/section-1002.107
    regulator: CFPB
    requirement_summary: >
      The bank must collect and report specified data points for each covered application
      from a small business, including application date, credit type, amount applied for,
      action taken, and the demographic data points listed in §1002.107(a).
    applicability: >
      Community bank, all covered applications from small businesses (as defined in
      §1002.106(b)); compliance begins on §1002.114 compliance date under the May 2026
      revised final rule.
    effective_date: 2028-01-01 [compliance date; rule effective 2026-06-30]
    impacted_process: application intake and underwriting
    control_objective: >
      Every covered application produces a complete §1002.107(a) data record before the
      reporting cycle closes for the year.
    evidence_required:
      - LOS extract showing §1002.107(a) field-by-field completeness
      - QA sample demonstrating 100% of covered applications populated
    owner: Head of Small Business Lending Operations
    status: draft
    confidence: high
    open_questions:
      - "Whether prequalification inquiries that do not become applications need any §1002.107 capture for §1002.103 covered-application boundary purposes"
    tags: [consumer-compliance, fair-lending]

  - obligation_id: OBL-003
    source_citation: CFPB, 12 CFR 1002.108 (firewall)
    source_section: §1002.108(b) [verify subsection labels]
    source_url: https://www.ecfr.gov/current/title-12/chapter-X/part-1002/subpart-B/section-1002.108
    regulator: CFPB
    requirement_summary: >
      Employees and officers involved in making any determination concerning a covered
      application must not have access to the applicant's responses to the §1002.107(a)
      demographic information unless a feasibility determination supports an exception.
    applicability: >
      Covered financial institution; design obligation on the firewall between intake
      capture of demographic data and underwriting decisioning.
    effective_date: 2028-01-01 [compliance date under May 2026 revised final rule]
    impacted_process: application intake and underwriting
    control_objective: >
      Demographic responses captured at intake are not accessible to underwriting
      decision-makers, or a documented feasibility determination supports the exception.
    evidence_required:
      - Firewall design document and access-control walkthrough
      - Feasibility-exception memo if dual-role staffing is being relied on
    owner: Chief Compliance Officer
    status: open-question
    confidence: low
    open_questions:
      - "Whether the bank's loan officers can perform both intake and underwriting under §1002.108 where staffing constraints make full segregation impractical, and what the feasibility-determination evidence has to show. Routes to legal."
    tags: [consumer-compliance, fair-lending, design-obligation]

  - obligation_id: OBL-004
    source_citation: CFPB, 12 CFR 1002.110
    source_section: §1002.110(a)
    source_url: https://www.ecfr.gov/current/title-12/chapter-X/part-1002/subpart-B/section-1002.110
    regulator: CFPB
    requirement_summary: >
      The bank must submit the small-business lending application register to the CFPB
      annually by June 1 of the year following the calendar year covered by the data.
    applicability: covered financial institution; annual federal filing
    effective_date: first filing under §1002.110 falls in the year following the bank's first compliance year; [verify against CFPB filing-instructions guide]
    impacted_process: regulatory reporting
    control_objective: >
      The annual register is filed by June 1 with the §1002.110(b) data fields, and the
      filing acknowledgement is retained.
    evidence_required:
      - Annual CFPB filing acknowledgement
      - Filing-readiness sign-off log from CCO
    owner: Chief Compliance Officer
    status: draft
    confidence: high
    tags: [consumer-compliance, regulatory-reporting]

open_question_summary:
  - obligation_ids: [OBL-003]
    question: "Firewall design where loan officers perform both intake and underwriting; what feasibility-determination evidence is sufficient under §1002.108"
    reviewer: legal
    target_resolution_date: 2026-06-01
  - obligation_ids: [OBL-002]
    question: "Treatment of prequalification inquiries that do not become applications under §1002.103 covered-application definition"
    reviewer: compliance
    target_resolution_date: 2026-06-15

applicability_notes: >
  Bank originated ~1,200 covered transactions in each of 2024 and 2025, meeting the
  §1002.105(b) 1,000-transaction threshold under the May 2026 revised final rule; rule
  effective June 30, 2026 with January 1, 2028 compliance date. Threshold reasoning sits
  in OBL-001's applicability column; open-question on prequalification inquiries depends
  on the §1002.103 covered-application interpretation.

confidence_label: mixed
human_review_required: true

reviewer:
  role: Chief Compliance Officer
  review_status: pending

revisions:
  - date: 2026-05-06
    reason: initial register
    delta: created
    approved_by: Chief Compliance Officer
```

## Why the register shape matters downstream

- `control-matrix` will anchor its rows on `OBL-001` through `OBL-004`; the firewall row (`OBL-003`) will not move past `open-question` until legal returns the feasibility determination, so the matrix will not yet attempt to map controls against it.
- `policy-gap-review` reads the register against the bank's existing fair-lending policy; the firewall obligation surfaces as a likely policy gap regardless of legal's eventual answer.
- `evidence-binder` reads `OBL-002.evidence_required` and scopes its evidence ask against the LOS extract and the QA sample.
- `exam-brief` reads the register when CFPB exam staff cite §1002.107 or §1002.108; the open-question summary is what the bank shows the examiner if the firewall design is challenged.
