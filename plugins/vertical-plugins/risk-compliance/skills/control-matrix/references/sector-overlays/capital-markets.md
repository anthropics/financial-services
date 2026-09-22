# Capital-markets sector overlay — control-matrix

Loads when the scope `sector_overlay_set` includes `capital-markets`. Binds matrix construction to SEC, FINRA, and CFTC examination expectations for broker-dealers, investment advisers, registered funds, and futures-market participants.

## Supervisory frame

SEC Division of Examinations and FINRA Member Supervision examine against named rule references; the matrix is read against the rule, not against a paraphrase. The rule citation in the obligation-source column is the navigation device for both the firm and the examiner. CFTC and NFA examinations follow a similar pattern for futures and swaps participants.

The character of the matrix differs by registration:

- **Broker-dealer matrices** anchor on FINRA supervision (Rule 3110), books-and-records (SEA §17(a) / Rules 17a-3 / 17a-4 / FINRA 4511), AML (FINRA 3310), communications (FINRA 2210), and the suitability and best-interest framework (FINRA 2111 / Reg BI).
- **Investment adviser matrices** anchor on the Advisers Act compliance program rule (Rule 206(4)-7) and its annual-review evidence, the custody rule (206(4)-2), the marketing rule (206(4)-1), and recordkeeping (Rule 204-2).
- **Registered fund matrices** anchor on the Investment Company Act compliance program rule (Rule 38a-1) and the fund's CCO report to the board.
- **CFTC-registrant matrices** anchor on the relevant Part 23 (swap dealers), Part 30 (foreign futures intermediaries), and Part 4 (commodity pool operators) controls.

## Annual-review machinery (advisers and funds)

Adviser matrices are bound to the annual-review cycle under Rule 206(4)-7. The matrix supports the CCO's annual-review report; testing rows in the matrix document the CCO-led testing for the year, the deficiencies identified, and the remediation evidence. Fund matrices serve the same function under Rule 38a-1, with the CCO reporting to the fund board at least annually.

The annual-review character drives matrix cadence: a broker-dealer matrix may be refreshed only on supervisory or material-change triggers, while an adviser matrix is expected to refresh annually with documented testing.

## Books-and-records controls

The recordkeeping rules are sharp and the matrix cites them precisely:

- 17 CFR §240.17a-3 — record creation requirements (broker-dealers).
- 17 CFR §240.17a-4 — record retention; most categories six years (first two readily accessible). The 2022 amendment introduced an electronic-recordkeeping audit-trail option as an alternative to write-once-read-many storage.
- FINRA Rule 4511 — general books-and-records retention, six years unless a specific rule sets a different period.
- 17 CFR §275.204-2 — Investment Advisers Act recordkeeping; most records five years (first two on-premises).
- 17 CFR §1.31 — CFTC recordkeeping; five years from creation, with electronic-storage standards.

Matrices for processes touching records under these rules carry retention-control rows; the evidence pointer's expected retention window respects the rule, not the firm's policy summary of the rule.

## Marketing and communications controls

Broker-dealer matrices for communications-with-the-public processes carry FINRA 2210 controls (principal review, filing requirements for member-firm-prepared retail communications, recordkeeping). Adviser matrices carry Rule 206(4)-1 (the marketing rule) controls: testimonial and endorsement evidence, performance-presentation controls (gross-and-net, time-period, hypothetical-performance disclosures), and review-and-recordkeeping controls.

## Best-interest and suitability controls

Broker-dealer matrices for retail-account processes carry Reg BI (17 CFR §240.15l-1) controls: care, disclosure, conflict-of-interest, and compliance obligations. Adviser matrices for retail-account processes carry the fiduciary-duty framework (SEC Interpretation Regarding Standard of Conduct for Investment Advisers, June 2019) and Form CRS controls.

## AML controls

FINRA 3310 sets the broker-dealer AML program elements; the matrix carries rows for the four pillars and for the FinCEN CDD Rule (31 CFR §1010.230) integration. Where the broker-dealer is part of a bank holding company, the matrix may inherit transaction-monitoring controls from the bank's BSA program; the inheritance and the firewall between the two are themselves matrix-recordable.

## Sign-off and review-gate norms

Adviser matrices are signed by the CCO (named under Rule 206(4)-7); fund matrices by the fund CCO under Rule 38a-1. Broker-dealer matrices for supervisory-program processes are signed by the principal-supervisor designated under FINRA 3110; broker-dealer AML matrices by the AML compliance officer designated under FINRA 3310. CFTC-registrant matrices are signed by the chief compliance officer designated under the relevant Part regulation.

## Anchors used by this overlay

- 17 CFR §240.15l-1 — Regulation Best Interest.
- 17 CFR §240.17a-3 and §240.17a-4 — broker-dealer recordkeeping.
- 17 CFR §275.204-2 — Investment Advisers Act recordkeeping.
- 17 CFR §275.206(4)-7 — Advisers Act compliance program rule.
- 17 CFR §275.206(4)-1 — Advisers Act marketing rule.
- 17 CFR §275.206(4)-2 — Advisers Act custody rule.
- 17 CFR §270.38a-1 — Investment Company Act fund compliance program rule.
- 17 CFR §1.31 — CFTC recordkeeping.
- FINRA Rule 2111 — suitability.
- FINRA Rule 2210 — communications with the public.
- FINRA Rule 3110 — supervision.
- FINRA Rule 3310 — AML compliance program.
- FINRA Rule 4511 — books and records, general retention.
- 31 CFR §1010.230 — FinCEN Customer Due Diligence Rule (applies to broker-dealers as covered financial institutions).
