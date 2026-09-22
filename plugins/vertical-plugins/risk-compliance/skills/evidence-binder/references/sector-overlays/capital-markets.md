# Capital-markets sector overlay — evidence-binder

Loads when the scope `sector_overlay_set` includes `capital-markets`. Binds evidence-binder content to SEC, FINRA, and CFTC examination expectations for broker-dealers, investment advisers, registered funds, and futures-market participants.

## Supervisory frame

SEC Division of Examinations (formerly OCIE) and FINRA Member Supervision issue examination request lists at exam open. The binder reconciles each item.

For investment advisers, SEC Rule 206(4)-7 (compliance-program rule) sets the annual-review frame; the binder for an annual-review evidence pack carries the testing workpapers, deficiencies log, and remediation evidence.

For broker-dealers, FINRA Rule 3110 (supervision) and the Books and Records rules (SEA §17(a), Rules 17a-3 / 17a-4) drive evidence-list shape.

## Recordkeeping and retention

The binding rules are sharp here:

- **SEC Rule 17a-4** — broker-dealer recordkeeping: most records retained six years (first two years in an easily accessible place); some categories (e.g., partnership articles) for the life of the enterprise plus three years. Electronic records since 2022 amendment may be stored on a write-once or audit-trail basis.
- **FINRA Rule 4511** — books-and-records general retention: six years unless a specific rule is shorter or longer.
- **SEC Investment Advisers Act Rule 204-2** — adviser recordkeeping: most records five years (first two years on premises). Performance-presentation records carry their own retention periods.
- **CFTC Regulation 1.31** — futures-market recordkeeping: five years from creation, with electronic-storage standards.

Binder rows that touch records under these rules carry a period_start that respects the retention window, not just the examination window.

## Common request-list shapes

SEC EXAMS request lists typically cover: governance (Form ADV, code of ethics, policies and procedures), conflicts (related-party trades, soft dollars, gifts and entertainment), portfolio management (trade blotter, allocation policy, IPO allocations), best execution (broker reviews, transaction-cost analysis), valuation (pricing policies, hard-to-value asset evidence), custody (Rule 206(4)-2 evidence for advisers), marketing (Rule 206(4)-1 evidence), cybersecurity (Reg S-P, Reg S-ID, the cybersecurity risk management program), and compliance (annual-review documentation, testing workpapers).

FINRA examination requests typically cover: supervisory structure (3110 evidence), books-and-records (4511 evidence), AML (3310 evidence), customer accounts (NASD 3010 / FINRA 3110 supervisory evidence), trade reporting, communications with the public (2210 evidence), and cybersecurity.

## Sign-off and review-gate norms

Adviser binders are signed by the chief compliance officer (named under Rule 206(4)-7). Broker-dealer binders are signed by the principal-supervisor under FINRA 3110 or by the chief compliance officer. Fund binders are signed by the fund CCO under Rule 38a-1; board materials are signed by the fund secretary.

The binder's `sign_off` field carries the role.

## Anchors used by this overlay

- 17 CFR §240.17a-3 and §240.17a-4 — broker-dealer recordkeeping.
- FINRA Rule 4511 — books and records, general retention.
- 17 CFR §275.204-2 — Investment Advisers Act recordkeeping.
- 17 CFR §275.206(4)-7 — Investment Advisers Act compliance-program rule.
- 17 CFR §270.38a-1 — Investment Company Act fund compliance-program rule.
- FINRA Rule 3110 — supervision.
- FINRA Rule 3310 — anti-money-laundering compliance program.
- 17 CFR §1.31 — CFTC recordkeeping requirements.
