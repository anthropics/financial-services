# Banking sector overlay — human-review-gates

Loads when the scope `sector_overlay_set` includes `banking`. The overlay shapes the decision-authority block, the independence requirements, the documentation conventions, and the board-oversight expectations for gate matrices at federally regulated US banks (national, state-member, state-non-member, savings, holding companies, and US IHCs of foreign banking organizations).

## Why the banking overlay matters

The federal banking supervisors (FRB, OCC, FDIC) have specific, published expectations on risk governance, three-lines-of-defense architecture, board risk-committee oversight, and senior-management challenge. A gate matrix that does not reflect those expectations reads as misaligned with the firm's continuous-monitoring posture and is harder to defend in the next examination cycle. The overlay is the contract between the gate matrix and the supervisor's expected governance architecture.

## Source basis

- **12 CFR Part 30, Appendix D — OCC Heightened Standards for Large Insured National Banks**. Standards I–V on the risk governance framework, three-lines-of-defense, independent risk management, front-line-unit responsibilities, and the board's oversight responsibility. Threshold for application: covered banks at the OCC's asset-size population (currently $50B+ at the OCC's discretion).
- **Reg YY (12 CFR Part 252) — Enhanced Prudential Standards for large bank holding companies**. Risk-management and risk-committee requirements that frame governance gates, including the requirement that BHCs at $50B+ maintain a risk committee of the board with at least one risk-management expert and an independent CRO with stature in the organization.
- **Federal Reserve SR 11-7 / OCC Bulletin 2011-12**. Validation independence as the ground for independence in model-risk gates; effective challenge as the source for the dissent-path discipline.
- **OCC Bulletin 2026-13**. Refreshed effective-challenge gate language, human oversight for AI-extended models, third-party model gates.
- **Federal Reserve SR 16-11**. Risk-management-framework expectations for sub-$100B FRB-supervised institutions.
- **Federal Reserve SR 13-13 / CA 13-10**. MRA / MRIA framework and the firm-side expectation that issues are tracked through closure with named-reviewer documentation.
- **FDIC Risk Management Manual of Examination Policies and FDIC Compliance Examination Manual**. MRBA framing; FDIC convention that significant findings address the board rather than management alone.
- **FFIEC Uniform Rating System (CAMELS for banks; ROCA for FBOs)**. Composite-rating framing that informs gate-criticality calibration; gates touching CAMELS components carry higher-stakes rationale.

## What the overlay adds to the matrix

### Decision authority — board oversight

For Heightened-Standards-covered banks and Reg YY-covered BHCs, the matrix's decision-authority block names the board risk committee as the ultimate adopting body for material gate-architecture changes. The board reporting cadence is named (typically quarterly to the risk committee, with an annual report on the gate-architecture refresh to the full board). For BHCs covered by Reg YY, the risk committee charter is itself a regulatory document; gate-architecture changes flow through risk-committee adoption with a documented decision.

### Three-lines-of-defense independence

The Heightened Standards' three-lines-of-defense architecture is the primary source for independence on banking-overlay gates:
- **Front-line unit (line 1)** — the business sponsor. Owns the risk-taking and the artifact under review.
- **Independent risk management (line 2)** — the independent reviewer. Owns the challenge function. Independence is structural: line-2 reviewers report to the CRO, not to the front-line unit.
- **Internal audit (line 3)** — the audit reviewer where the gate is one that internal audit certifies (e.g., the annual review of the gate matrix itself; the validation of effective-challenge implementation).

The matrix's `required_reviewers` block carries primary and backup roles per line; the `independence_required` flag is true for line-2 and line-3 reviewers; the `independence_basis` cites 12 CFR Part 30 Appendix D Standard II (risk governance framework) and Standard IV (front-line-unit responsibilities).

### Senior-management challenge

For sub-$100B FRB-supervised institutions, SR 16-11 frames the senior-management-challenge expectation. The matrix typically names a "senior management committee" gate distinct from the board risk committee gate; the senior management committee is the operational decision-holder, and the board risk committee is the oversight body that reviews the senior management committee's record on a periodic cadence.

### Reg YY risk-committee gates

For BHCs at $50B+ under Reg YY enhanced prudential standards, gates touching enterprise-wide risk-management framework refresh, risk-appetite-statement updates, or material change to the CRO function flow through the board risk committee with a documented decision. The matrix names the risk committee as the primary committee for these gates; the documentation requirement names the board risk-committee minutes as the system of record.

### Heightened Standards severity flavour

For OCC-Heightened-Standards-covered banks, gate-design issues (a missing independence requirement, an absent escalation path, a documentation requirement that does not retain attesters) carry severity weight tied to the specific Heightened Standard they impair. A missing line-1 / line-2 separation impairs Standard II; a missing front-line-unit accountability impairs Standard IV; a missing board-oversight cadence impairs Standard V. The gap section of the matrix names the specific Standard.

### CAMELS / ROCA component implications

Gates that govern decisions touching CAMELS components (Capital, Asset quality, Management, Earnings, Liquidity, Sensitivity) carry severity weight tied to the component. A gate-design weakness on the M (Management) component is itself a Management-rating consideration; the gap is sourced to the FFIEC Uniform Rating System framing.

## Common patterns

- **One-committee monoculture**. A bank where the same committee owns AI use-case approval, model-risk approval, vendor onboarding, issue rating, and customer-impact action does not have a gate matrix; it has one committee. Heightened Standards Standard II expects independent risk management with stature; one-committee monoculture fails the independence test. The gap section names this and recommends a committee-charter refresh.
- **MRA-driven gate refresh**. An MRA on governance prompts a gate-architecture refresh; the recommended charter language and the gap section frame the refresh against the MRA's specific finding.
- **Pre-emptive Heightened Standards readiness**. Banks approaching the $50B Heightened Standards threshold typically refresh gate architecture in advance of the threshold trigger. The matrix's `recommended_charter_language` block frames the readiness posture.
- **Validator-as-developer failure**. A model-risk gate where the named validator is also the named developer (or reports to the developer's chain) fails SR 11-7. The matrix's gap section flags this with the specific section reference.

## Implications for gate construction

- Independence is named explicitly per reviewer, with the source anchor in `independence_basis`. Banking overlay matrices typically have independence flagged on the line-2 reviewer slot for every gate that touches risk-taking, risk-control, or regulatory-disclosure decisions.
- Decision criteria for banking gates often cite the specific Heightened Standard, Reg YY section, or SR letter; the criteria block carries the source anchor.
- Documentation requirement names the system of record at granularity: GRC platform record ID type, board-portal location, board-minutes retention period (typically 7-year retention for federal banking exam files; firm-overlay specifies the firm's actual cadence).
- The gap section explicitly checks for: missing independent reviewer slot, missing board-oversight cadence (for Heightened Standards / Reg YY firms), missing escalation path to the risk committee, missing dissent-path discipline.

## Anchors used by this overlay

- 12 CFR Part 30, Appendix D — OCC Heightened Standards (Standards I–V). https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20D%20to%20Part%2030
- 12 CFR Part 252 (Reg YY) — Enhanced prudential standards for large BHCs. [verify current section labels for risk committee and risk-management requirements.] https://www.federalreserve.gov/supervisionreg/reglisting.htm
- Federal Reserve SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management. §V (validation independence), §VI (governance). https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm
- OCC Bulletin 2026-13 — Revised Interagency Model Risk Management Guidance. §III.E (independent challenge), §III.F (human oversight). [verify section labels] https://www.occ.gov/news-issuances/bulletins/
- Federal Reserve SR 16-11 — Risk-management framework for sub-$100B institutions. https://www.federalreserve.gov/supervisionreg/srletters/sr1611.htm
- Federal Reserve SR 13-13 / CA 13-10 — Communication of Supervisory Findings (MRA / MRIA). https://www.federalreserve.gov/supervisionreg/srletters/sr1313.htm
- FDIC Risk Management Manual of Examination Policies. https://www.fdic.gov/regulations/safety/manual/
- FDIC Compliance Examination Manual. https://www.fdic.gov/resources/supervision-and-examinations/consumer-compliance-examination-manual/
- FFIEC Uniform Rating System (CAMELS / ROCA). [verify current edition.]
