# Capital markets and asset management sector overlay: obligation-mapping

Loaded when the scope includes `capital-markets` in `sector_overlay_set`. Adds capital-markets-specific source labels and obligation patterns the practitioner expects to find when the register scopes a broker-dealer, investment adviser, or registered fund process. Does not change the row spine.

The two regulators are SEC and FINRA (with the CFTC and NFA layered in for futures and swaps). Investment Advisers Act and Investment Company Act govern the buy-side; Securities Exchange Act and FINRA rules govern the sell-side; the Securities Act is mostly issuer-side. The register names the regulatory regime that imposes each row.

## Sources the register may cite

### Investment adviser obligations

- Investment Advisers Act of 1940 and rules thereunder (17 CFR Part 275).
  - Rule 206(4)-7 (compliance program rule) — the foundational compliance-program obligation. [verify subsection labels.]
  - Rule 206(4)-1 (marketing rule, as amended 2020). §275.206(4)-1(a) through (e).
  - Rule 204A-1 (code of ethics). §275.204A-1.
  - Rule 204-2 (recordkeeping). §275.204-2.
  - Rule 206(4)-2 (custody). §275.206(4)-2.
  - Use for: adviser-side obligations across compliance program, marketing, code of ethics, recordkeeping, custody. SEC Division of Examinations priorities are scoping input rather than rule-text source.
  - Link: https://www.ecfr.gov/current/title-17/chapter-II/part-275

### Broker-dealer obligations

- Securities Exchange Act of 1934 and rules thereunder (17 CFR Part 240).
  - Rule 15c3-1 (net capital). §240.15c3-1.
  - Rule 15c3-3 (customer protection). §240.15c3-3.
  - Rule 17a-3 and Rule 17a-4 (recordkeeping). §240.17a-3 and §240.17a-4 (note 2022 amendments to electronic recordkeeping).
  - Rule 15c3-5 (market access). §240.15c3-5.
  - Reg BI (Best Interest, 17 CFR §240.15l-1).
  - Use for: broker-dealer obligations across capital, customer protection, recordkeeping, market access, retail-investor conduct.
  - Link: https://www.sec.gov/divisions/marketreg/

- FINRA rule book.
  - FINRA Rule 3110 (supervision).
  - FINRA Rule 4511 (general books-and-records retention).
  - FINRA Rule 4530 (reporting requirements, including disciplinary and customer-complaint reporting).
  - FINRA Rule 2010 (standards of commercial honor and just and equitable principles of trade).
  - Use for: FINRA-imposed supervision, recordkeeping, reporting, and conduct obligations on member firms.
  - Link: https://www.finra.org/rules-guidance

### Registered investment company obligations

- Investment Company Act of 1940 and rules thereunder (17 CFR Part 270).
  - Rule 38a-1 (compliance program rule). §270.38a-1.
  - Rule 17a-7, 17a-8, 17a-9 (affiliated transactions and cross-trades).
  - Rule 18f-4 (derivatives and limits).
  - Rule 22c-2 (redemption fees, recordkeeping for trading activity).
  - Use for: fund-board, fund-CCO, and affiliated-transaction obligations on registered open-end and closed-end funds.
  - Link: https://www.ecfr.gov/current/title-17/chapter-II/part-270

### Securities-issuer obligations (when the engagement covers issuer reporting)

- Securities Exchange Act of 1934 §§13, 15(d) and Reg S-K. Item 106 (cybersecurity) for cyber-related disclosures, Item 402 for executive compensation, Form 8-K Item 1.05 for material cybersecurity incident disclosure.
  - Use for: issuer-disclosure obligations when the register scopes issuer-reporting processes.

### CFTC and NFA hooks

- Commodity Exchange Act and CFTC regulations (17 CFR Chapter I).
  - 17 CFR §23.600 (risk management program for swap dealers).
  - 17 CFR §1.31 (recordkeeping for futures commission merchants).
  - Use for: swap-dealer and FCM obligations when the register scopes derivatives activity.

- NFA Compliance Rules (NFA member firms).
  - Use for: NFA-side obligations on commodity pool operators, commodity trading advisors, and FCMs.

## Obligation patterns the practitioner expects to find

- **CCO-anchored compliance-program obligations.** Both Rule 206(4)-7 (advisers) and Rule 38a-1 (funds) impose compliance-program obligations and a CCO-attestation cycle. The register surfaces the program elements (annual review, written policies, designated CCO) as discrete rows.
- **Recordkeeping obligations with retention windows.** SEC Rule 17a-4, IAA Rule 204-2, FINRA Rule 4511. The register's evidence-required column reflects the retention window that the rule names; firm policy summaries are not the source.
- **Board-anchored fund obligations.** Fund-board approval obligations for advisory contracts (§15(c)), distribution arrangements (Rule 12b-1), valuation (Rule 2a-5), and affiliated transactions (Rule 17a-7). The owner column on these rows is the fund board, not the adviser CCO.
- **Reg BI and Form CRS for retail-facing brokers and dual-registrants.** The register splits the Reg BI care, conflicts, and disclosure obligations from the Form CRS delivery obligations because the test posture differs.
- **SEC Division of Examinations priorities as scoping input, not source.** When a SEC EXAMS priority letter highlights a topic, the register may note it as scoping rationale in `applicability_notes`, but the obligations still extract from the underlying rule.

## What does not belong here

- Bank-side obligations even where the broker-dealer is part of a bank-holding company. Run a separate register with `banking` overlay if relevant.
- Insurance-side obligations on a variable-annuity sponsor's insurance company. Run a separate register with `insurance` overlay; the SEC-side obligations on the registered separate account stay here.
- Internal firm policy and taxonomy. That goes in `references/firm-overlay.md`.
