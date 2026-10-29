# Banking sector overlay — evidence-binder

Loads when the scope `sector_overlay_set` includes `banking`. Binds evidence-binder content to bank-supervisory expectations.

## Supervisory frame

US bank examiners (OCC, FRB, FDIC) work from request lists (RFIs) typically issued at exam open and supplemented during fieldwork. The binder's `request_list` is the canonical reconciliation surface for these RFIs. State DFIs follow a similar pattern; for state-member banks, the FRB and the state share supervision and the binder may carry items from both.

The FFIEC IT Examination Handbook (Audit booklet, April 2012) frames evidence sufficiency for IT and third-party audit programs. Audit evidence is read against the program's design and the institution's risk profile; the binder cites the booklet section by reference, not by excerpt.

For OCC large-bank populations, 12 CFR Part 30 Appendix D (Heightened Standards) sets framework-level expectations that bear on what the binder must support: independent risk management evidence, board-level oversight evidence, risk-appetite-statement evidence, and chief-risk-executive evidence.

## Recordkeeping and retention

- Bank Service Company Act, 12 USC §1867(c): examiner-access expectations for third-party-provided services. Vendor-evidence rows in the binder reference the contract clause that gives the examiner access; if the clause is missing, the binder surfaces a gap.
- 12 CFR §1010 (FinCEN BSA recordkeeping): five-year retention floor for BSA records. Binder rows for BSA evidence carry a period_start that respects the five-year window even when the examination period is shorter, because the underlying records must be available.
- FFIEC IT Audit booklet: retention expectations for audit workpapers vary by program; a typical floor is the longer of the firm's internal policy or the supervisory cycle (commonly seven years for federally regulated institutions).

## Common request-list shapes

Federal exam RFIs typically cluster around: governance and oversight (board minutes, committee minutes, charter, policy versions), risk management (risk-appetite statement, KRI dashboards, KRI breach log), controls (control inventory, testing results, exception register), audit (internal-audit plan, prior-period workpapers, follow-up status), data and reporting (BCBS 239 conformance evidence for the relevant institutions, data-quality metrics, lineage documentation), and third-party (TPRM inventory, criticality determinations, vendor diligence packs, SOC reports, exit plans).

The binder reconciles each cluster against the evidence index. Cluster-level gaps appear in the gaps section even when individual requests within the cluster are met.

## BCBS 239 traceability

For G-SIBs and D-SIBs, BCBS 239 Principles 3 (accuracy and integrity), 4 (completeness), and 7 (accuracy of risk reporting) bear on the binder when risk-data evidence is in scope. Binder rows for risk-data extracts cite the BCBS 239 principle they support and the firm's data-lineage record where one exists.

## Sign-off and review-gate norms

A bank-exam binder is signed by the chief compliance officer or chief risk officer (depending on the exam type) before it is presented to the examiner-in-charge. Internal-audit fieldwork binders are signed by the audit director and the in-charge auditor. The binder's `sign_off` field carries the role.

## Anchors used by this overlay

- 12 CFR Part 30 Appendix D — OCC Heightened Standards [verify section labels].
- Bank Service Company Act, 12 USC §1867(c).
- FFIEC IT Examination Handbook, Audit booklet (April 2012) §§III, IV.B [verify section labels].
- FinCEN BSA recordkeeping, 31 CFR §1010.430 (general), 31 CFR §1020 series (banks).
- BCBS 239, January 2013, Principles 3, 4, 7.
- SR 11-7 / OCC Bulletin 2011-12 §V (model documentation) for model-validation binders within bank scope.
