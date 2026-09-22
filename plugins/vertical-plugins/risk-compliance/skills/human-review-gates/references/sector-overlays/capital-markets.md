# Capital markets sector overlay — human-review-gates

Loads when the scope `sector_overlay_set` includes `capital-markets`. The overlay shapes the decision-authority block, the supervision and compliance-program gate framing, and the documentation conventions for gate matrices at SEC- and FINRA-regulated firms (broker-dealers, investment advisers, fund complexes, CFTC-registered swap dealers and FCMs, and exchange-traded-product issuers).

## Why the capital-markets overlay matters

The supervision concept is central to broker-dealer governance under FINRA Rule 3110; the compliance-program concept is central to investment adviser governance under SEC Rule 206(4)-7. Both concepts are directly anchored in the firm's gate architecture: supervision is itself a continuous gate function, and the annual compliance-program review under Rule 206(4)-7 is itself an annual gate. A gate matrix at a broker-dealer or investment adviser that does not name supervision or the annual compliance review correctly will not align with the SEC EXAMS or FINRA examination posture.

## Source basis

- **FINRA Rule 3110 — Supervision**. The supervision system requirement: written supervisory procedures, supervision of registered persons by qualified principals, supervision of customer accounts and transactions, supervision of correspondence and internal communications, and the supervision-of-supervisors requirement.
- **FINRA Rule 3120 — Supervisory Control System**. The supervisory control system requirement, distinct from but layered onto Rule 3110: testing and verification of the firm's supervisory procedures, with the chief executive officer's annual certification.
- **SEC Rule 206(4)-7 — Compliance Programs of Investment Advisers (17 CFR §275.206(4)-7)**. The requirement that registered investment advisers adopt and implement written compliance policies and procedures reasonably designed to prevent violations, designate a chief compliance officer, and conduct an annual review of the adequacy of the policies and procedures and the effectiveness of their implementation.
- **SEC Rule 38a-1 — Compliance Procedures and Practices of Investment Companies (17 CFR §270.38a-1)**. The fund-complex parallel to Rule 206(4)-7: written compliance policies, designated CCO, annual board approval and review.
- **SEC Rule 17a-3 and 17a-4 — Broker-dealer recordkeeping (17 CFR §240.17a-3 and §240.17a-4)**. The records the broker-dealer must make and preserve, with named retention periods. The recordkeeping rule is itself a gate-decision evidence anchor.
- **SEC Rule 204-2 — Investment Adviser recordkeeping (17 CFR §275.204-2)**. The investment-adviser parallel.
- **SEC Rule 15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access (17 CFR §240.15c3-5)**. Pre-trade risk-management controls and the CEO certification of effectiveness of those controls; named pre-trade gates with documented criteria.
- **FINRA Rule 4511 — General Recordkeeping**. Books-and-records retention requirements layered onto SEC 17a-3 / 17a-4.
- **FINRA Rule 3170 — Tape Recording of Registered Persons (taping rule)**. Specific firms; named gate where applicable.
- **CFTC Part 3 — Registration and CFTC Part 23 — Swap Dealers** and the CFTC's compliance-program requirements for swap dealers.

## What the overlay adds to the matrix

### Decision authority — supervision and CCO functions

The capital-markets matrix names two distinct decision-authority structures:

- **For broker-dealers**: the supervision system under Rule 3110, with named principals (Series 24 General Securities Principal, Series 9/10 Branch Office Manager, Series 4 Registered Options Principal, Series 27/28 Financial and Operations Principal, etc.) carrying gate-decision authority for the activities they supervise. The supervisory control system under Rule 3120 names the senior officer (often the President or CEO) who certifies the supervisory system annually. Branch-office gates flow through branch managers; firm-level gates flow through the senior principal in the relevant function.
- **For investment advisers**: the chief compliance officer designated under Rule 206(4)-7 as the named decision-holder for compliance-program gates. The annual compliance review is itself a gate; the documentation requirement names the annual review report and the CCO sign-off.

For dual-registrant firms (broker-dealer and adviser), both structures exist; the matrix names the structure relevant to each gate's subject matter.

### Annual compliance review as a gate

Rule 206(4)-7 explicitly requires registered investment advisers to review their compliance program annually. This is itself a gate: the trigger is annual; the required reviewer is the CCO; the required inputs are the firm's compliance policies, the year's compliance monitoring outputs, and the year's exception log; the decision criteria are adequacy and effectiveness; the documentation requirement is the annual review report, retained per Rule 204-2. Funds under Rule 38a-1 carry the same gate with board-approval framing.

### Pre-trade risk-management gates (Rule 15c3-5)

For broker-dealers with market access, Rule 15c3-5 names a specific class of gates: pre-trade risk-management controls, with the CEO's annual certification of effectiveness. The matrix carries these as a distinct gate cluster, with the CEO as the named attester for the annual certification gate.

### Recordkeeping framing

The recordkeeping rules (17a-3, 17a-4, 204-2, 4511) frame the documentation requirement on every capital-markets gate. The retention period is rule-specific (typically 3 to 6 years depending on the record type, with the first 2 years in an easily accessible location); the storage standard is rule-specific (the 2022 SEC amendment to 17a-4 changed the electronic-storage standard from WORM to a more flexible audit-trail-based standard). The matrix's documentation requirement column names the rule and the retention period.

### CFTC-regulated activity

For swap dealers and FCMs, the CFTC's compliance-program requirements layer onto the matrix. The chief compliance officer for a swap dealer carries specific duties under CFTC rules; the annual CCO report to the CFTC is itself a gate-anchored deliverable.

## Common patterns

- **Supervision is not a gate; supervision is the continuous function**. A common confusion: practitioners name "supervision" as a gate. Supervision under Rule 3110 is the continuous oversight function performed by qualified principals; the gate is the decision point inside the supervision function (account approval, transaction review threshold, correspondence escalation). The matrix names the gates within the supervisory function, not "supervision" as a gate itself.
- **Annual compliance review treated as administrative**. The annual review under Rule 206(4)-7 is sometimes treated as an administrative box-check; the SEC EXAMS staff treat it as a substantive gate. The matrix elevates the annual review to a named gate with criteria, stop conditions (e.g., "no sign-off if material deficiencies are not remediated or scheduled"), and documentation discipline.
- **Dual-registrant ambiguity**. Firms registered as both broker-dealer and investment adviser sometimes have unclear gate boundaries between supervision (Rule 3110) and compliance-program (Rule 206(4)-7). The matrix names both structures and assigns each gate to the structure relevant to its subject matter.
- **CEO certification under-evidenced**. The Rule 3120 supervisory-control-system certification and the Rule 15c3-5 pre-trade-risk certification are CEO-level attestations; the documentation requirement on these gates names the certification record retained per Rule 17a-4.

## Implications for gate construction

- Decision authority for capital-markets matrices typically names: the supervision system (broker-dealer side), the CCO function (adviser/fund side), the senior officer carrying Rule 3120 / Rule 15c3-5 certifications, and the board (for fund advisers under Rule 38a-1).
- Independence on capital-markets gates is grounded in SEC Rule 206(4)-7's framing that the CCO has "competence and knowledge" and "sufficient authority to develop and enforce appropriate policies and procedures"; firms sometimes also flag CCO independence from front-office reporting lines, though the rule does not explicitly require it.
- Documentation requirement on capital-markets gates names the recordkeeping rule (17a-3, 17a-4, 204-2, 4511) and the retention period; the system of record is the firm's books-and-records system per SEC and FINRA expectations.
- The gap section explicitly checks for: supervision-named-as-gate confusion (correct it); annual review under Rule 206(4)-7 missing or under-evidenced; CEO certification gates (Rule 3120, Rule 15c3-5) missing or with no clear attester; correspondence and internal communications supervision gates missing under Rule 3110.

## Anchors used by this overlay

- FINRA Rule 3110 — Supervision. https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110
- FINRA Rule 3120 — Supervisory Control System. https://www.finra.org/rules-guidance/rulebooks/finra-rules/3120
- FINRA Rule 4511 — General Recordkeeping. https://www.finra.org/rules-guidance/rulebooks/finra-rules/4511
- FINRA Rule 3170 — Tape Recording of Registered Persons. https://www.finra.org/rules-guidance/rulebooks/finra-rules/3170
- 17 CFR §275.206(4)-7 — SEC Rule 206(4)-7, Compliance Programs of Investment Advisers. https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.206(4)-7
- 17 CFR §270.38a-1 — SEC Rule 38a-1, Compliance Procedures and Practices of Investment Companies. https://www.ecfr.gov/current/title-17/chapter-II/part-270/section-270.38a-1
- 17 CFR §240.17a-3 — Records to be made by certain exchange members, brokers, and dealers. https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.17a-3
- 17 CFR §240.17a-4 — Records to be preserved by certain exchange members, brokers, and dealers. https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.17a-4
- 17 CFR §275.204-2 — Investment Adviser recordkeeping. https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.204-2
- 17 CFR §240.15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access. https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.15c3-5
- CFTC Part 3 (Registration) and Part 23 (Swap Dealers). https://www.ecfr.gov/current/title-17/chapter-I
