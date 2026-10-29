# Insurance sector overlay — evidence-binder

Loads when the scope `sector_overlay_set` includes `insurance`. Binds evidence-binder content to state-DOI and NAIC-framework expectations.

## Supervisory frame

State Departments of Insurance run market-conduct and financial examinations under state law and the NAIC handbooks. The Market Conduct Examiners Handbook frames evidence asks for claims-handling, complaint-handling, underwriting, rating, marketing, and producer-licensing programs; the Financial Condition Examiners Handbook frames evidence asks for solvency, reserves, reinsurance, and corporate governance. The binder's `request_list` reconciles the examiner's RFIs.

NAIC accreditation drives a baseline of standards across states; state-specific amendments are common, and the binder carries the binding-state version where the two diverge.

## Recordkeeping and retention

- NAIC Model Audit Rule (Model #205), §16: internal control over financial reporting expectations for insurers above the premium threshold. Audit-binder rows cite §16 for ICFR scope; reproducibility of the underlying control evidence is the supervisory test.
- State retention rules vary; common pattern is the longer of seven years or the policy life plus a tail. Binder rows for policy-administration evidence respect the longer window.
- ORSA (Own Risk and Solvency Assessment): annual filing in adopting states. Evidence binder for ORSA review carries the ORSA Summary Report, the supporting risk-and-capital analysis, and the governance evidence (board approval, risk-appetite statement). NAIC Risk Management and ORSA Model Act §4 [verify].

## Common request-list shapes

State-DOI market-conduct RFIs typically cover: claims-handling timeliness and unfair-claims-settlement practices, complaint logs and responses, producer licensing and appointment, underwriting and rating sample files, marketing materials, advertising approvals, replacement and suitability evidence (life and annuities), privacy notices (NAIC Model #672 / GLBA-aligned).

Financial examinations typically cover: corporate-governance evidence, board and committee minutes, audited statutory financials, reserve adequacy, reinsurance ceded and assumed, asset valuation, related-party transactions, and ORSA where adopted.

## Sign-off and review-gate norms

Market-conduct binders are signed by the chief compliance officer; financial-exam binders by the chief financial officer or chief risk officer. The binder's `sign_off` field carries the role.

## Anchors used by this overlay

- NAIC Model Audit Rule (Model #205) §16 — internal control over financial reporting [verify section].
- NAIC Market Conduct Examiners Handbook — claims-handling examination standards [verify section].
- NAIC Financial Condition Examiners Handbook — financial examination standards [verify section].
- NAIC Risk Management and ORSA Model Act (Model #505) §4 [verify section].
- NAIC Model Unfair Claims Settlement Practices Act (Model #900) [verify state-specific adoption].
- State recordkeeping statutes — verify per state.
