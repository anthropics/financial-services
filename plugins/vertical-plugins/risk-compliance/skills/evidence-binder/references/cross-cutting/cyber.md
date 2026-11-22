# Cyber cross-cutting overlay — evidence-binder

Loads when the scope `cross_cutting_overlay_set` includes `cyber`, or whenever the binder carries cyber-program evidence (NYDFS Part 500 attestations, IR workpapers, vulnerability-scan extracts, SOC 2 evidence supporting a control test, vendor cyber assessments cited by a critical-vendor binder, SEC cyber-disclosure-readiness evidence). The overlay does not change the binder's spine; it sharpens provenance, custodian, and sensitivity treatment for cyber-program rows so the binder survives review by the firm's CISO function and by examiners reading the cyber file.

## Why cyber belongs in the binder

Three patterns recur. A regulator exam binder routinely includes the firm's NYDFS Part 500 §500.4 program documentation, §500.7 access-controls evidence, §500.16 IR plan and tabletop output, §500.17(a) and (b) notice files. A model-validation binder for an in-perimeter AML or fraud system carries the serving-environment cyber evidence (logging, access controls, change controls) the validator references. A critical-vendor binder reconciles to the vendor's SOC 2 Type II, pen-test summary, and IR-clock posture. The binder needs to handle this evidence with the right custodian, the right sensitivity, and provenance that survives a CISO-side challenge — not as `internal` rows the binder author treats as ordinary.

## Operative anchors

- **NYDFS 23 NYCRR Part 500** — §500.4 (cybersecurity program governance and the CISO designation), §500.6 (audit-trail retention; relevant where the binder cites system-of-record extracts of access logs, change logs, security-event logs), §500.7 (access privileges), §500.11 (third-party service-provider security policy; cited where the binder includes vendor cyber attestations), §500.16 (incident-response plan and BCDR), §500.17(a) (72-hour notice to superintendent of a cybersecurity event), §500.17(b) (annual certification of compliance). The October 2024 NYDFS AI cybersecurity Industry Letter applies where AI-system cyber evidence is in the binder.
- **Banking computer-security incident notification rule** — 12 CFR Part 53 (OCC), 12 CFR Part 225 (FRB), 12 CFR Part 304 (FDIC) — 36-hour notification clock for "computer-security incidents" meeting the rule's criteria. Where the binder supports an exam at a covered banking organisation, the IR-evidence rows must reconcile to this clock (and to the bank service provider notification obligation on third parties).
- **SEC cyber-disclosure rule** — Form 8-K Item 1.05 and Reg S-K Item 106 — for public registrants, the binder rows tied to materiality determinations, 8-K filings, and Reg S-K Item 106 annual-disclosure governance carry confidential or restricted classification by default.
- **GLBA Safeguards Rule** — 16 CFR Part 314 (FTC scope) and the interagency Safeguards rule for banks — §314.4 program elements and §314.5(d) notification-event reporting (FTC) where the binder carries unauthorised-acquisition-of-unencrypted-customer-information evidence.
- **FFIEC IT Examination Handbook — Information Security booklet** [verify current edition] — examiner-facing detail on cyber-program documentation, complementary user entity controls, and audit evidence.
- **SR 11-7 / OCC 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026 (April 17, 2026)** — for in-perimeter models with cyber-relevant serving environments, the validation evidence chain includes serving-environment cyber controls; the binder treats those rows as cyber-tagged.

## Implications for binder construction

- **Custodian role on cyber rows.** A CISO-function role (CISO, Deputy CISO, Head of Security Operations, Head of IR, Head of Identity and Access, Head of Vulnerability Management) is named as custodian on cyber-tagged rows, alongside or instead of the operational owner. "IT" is not a custodian; "Information Security" is not a custodian. Examiners and validators read the custodian field as a routing column.
- **Sensitivity classification on cyber rows.** IR workpapers, vulnerability-scan extracts, pen-test reports, SIEM-derived audit-trail extracts, and §500.17 notice files are `restricted` by default. Marketing-grade summaries (board cyber-risk paper, public-disclosure language) may be `confidential`; the row classification is honest, not defaulted.
- **Provenance on screenshot-of-cyber-evidence rows.** A screenshot of a SIEM dashboard taken on a personal device is a cyber-evidence-handling concern in addition to a provenance concern. The provenance fields record `extract_method` (SIEM query ID, dashboard share-link, vendor-portal export), `extracted_by_role` (named CISO-function role), the device class for `restricted` rows, and the system-of-record link back to the underlying record. Pen-test PDFs from the testing partner: capture the partner identity and the report ID, not just the file path.
- **Reproducibility on audit-trail rows.** §500.6 audit-trail evidence must be reproducible: the SIEM query, the time window, the filter set. A screenshot dated yesterday with no query reference cannot be re-pulled six months later and is `[evidence needed]` until the query reference is captured.
- **Period coverage and the BSA five-year floor.** Where cyber-evidence rows support BSA-touching control tests (transaction-monitoring system access logs, screening-engine change logs), the recordkeeping floor extends past the engagement window. The row's `period_end` respects the floor.
- **Vendor cyber rows reconcile to the third-party file.** SOC 2 Type II, ISO 27001 SoA, pen-test summary, and the BCDR test report from a critical vendor are binder rows; the vendor identity, report period, scope, and exceptions are recorded at the row, not abstracted into "vendor SOC 2".
- **§500.17 notice files as binder rows.** A 72-hour notice to NYDFS, a 36-hour banking notice, an 8-K Item 1.05 filing, a §314.5(d) FTC notification: each is a binder row with the filing reference, the date, the submitting role, and the underlying-incident pointer. A binder that holds the filing as an attachment without the row-level metadata fails the request-list reconciliation.
- **Regulator-correspondence rows are confidential at minimum.** Examiner letters, MRA / MRIA correspondence on cyber-program findings, and cyber-disclosure follow-up correspondence are not `internal`. The sensitivity column drives downstream handling.

## What the cyber overlay does not do

The overlay does not turn the binder into a cyber-program assessment. The binder indexes evidence; the cyber-program assessment lives in `compliance-testing` (for control testing), in `third-party-operational-resilience/skills/resilience-testing-pack` (for cyber and operational-resilience testing), and in `risk-reporting/skills/cyber-disclosure-readiness` (for the SEC disclosure file). The overlay sharpens how cyber-tagged evidence is indexed; it does not substitute for the upstream artifact that produced it.

## Common pitfalls when cyber-tagged evidence is in the binder

- Custodian set to "IT" or "InfoSec" as a function rather than a CISO-function role.
- Sensitivity defaulted to `internal` on IR workpapers, pen-test PDFs, SIEM extracts, and §500.17 notice files.
- Audit-trail extract rows without the query reference; they are screen states, not reproducible evidence.
- Vendor SOC 2 Type II row collapsed into one cell without the period covered, the trust-services criteria scope, and the exceptions noted.
- §500.17 notice files held as attachments with no row-level metadata reconciling to the underlying-incident evidence.
- Treating an SEC 8-K Item 1.05 filing as a public-source obligation row when the binder also holds the firm's materiality-assessment workpaper, which is restricted firm-internal evidence.
- Missing the device-class field on `restricted` cyber-evidence rows that originated as screenshots.
