# Privacy cross-cutting overlay — evidence-binder

Loads when the scope `cross_cutting_overlay_set` includes `privacy`, or when the binder carries evidence touching NPI, PHI, PCI, or other regulated personal data. The overlay sets the privacy posture on individual rows and on the binder as a whole.

## Why privacy belongs in the binder

Evidence frequently is personal data. Sample claim files carry NPI and may carry PHI. Customer-prompts to AI systems carry whatever the customer typed. Adverse-action notice samples carry NPI. Complaint logs carry NPI and sometimes PHI. The binder cannot move that evidence without applying the firm's privacy controls, and the binder must be able to evidence its own handling for downstream regulator scrutiny.

The discipline is: classify each row's `sensitivity` honestly, name the lawful basis for collecting and processing the evidence in this binder context, redact at the row level where redaction is the firm's standard and the regulator does not require unredacted form, and segregate restricted rows from lower-classification rows in shared review folders.

## Specific regimes

- **GLBA Safeguards Rule** — 16 CFR Part 314 (FTC) for non-bank financial institutions; functional regulator equivalents for banks (interagency Safeguards rule). The binder's privacy posture cites the firm's Safeguards program where NPI is in scope.
- **HIPAA** — 45 CFR Part 160 and Part 164. Where PHI may appear in narratives or files (medical-pay claims, life and health underwriting, certain disability evidence), the binder evidences the firm's BAA chain and the minimum-necessary handling. Restricted classification by default.
- **State privacy laws** — California (CCPA/CPRA), Virginia (VCDPA), Colorado (CPA), Connecticut (CTDPA), Texas, Florida, and others as adopted. Right-to-delete and right-to-correct request fulfilment is itself often binder-worthy evidence.
- **FCRA / FACTA** — when consumer-report data appears in evidence (adverse-action samples, fraud-investigation files), FCRA disposal rules (16 CFR Part 682) and the FTC Red Flags Rule apply.
- **Reg S-P / Reg S-ID** — for SEC-registered entities, customer-information handling.
- **GDPR / UK GDPR** — for binders involving EU/EEA data subjects, Article 5 principles (purpose limitation, data minimisation, storage limitation) bear on what evidence the binder may retain after the review closes; Article 28 governs processor relationships when third-party reviewers handle the evidence.

## Implications for binder construction

- **Row-level sensitivity classification is mandatory.** A binder that defaults every row to `internal` is not honest.
- **Redaction is a row attribute, not a binder attribute.** Some rows may need redaction for some audiences (e.g., shared with external counsel) but not others (e.g., regulator-direct).
- **Source-of-record provenance bears on privacy.** A screenshot of NPI taken on a personal device is a privacy incident, not just a provenance concern. The provenance fields should record the device class for restricted-sensitivity rows.
- **Retention after review.** When a regulator review or audit closes, the binder may itself become a privacy retention question. The firm's records-retention schedule controls; the binder's `revision_log` is the audit trail.
- **Privacy custodian.** Where the binder carries restricted-classification rows, the custodian register names a privacy role (privacy officer, data protection officer, HIPAA privacy officer) for those rows in addition to the operational owner.

## Anchors used by this overlay

- 16 CFR Part 314 — FTC Safeguards Rule.
- 45 CFR Parts 160 and 164 — HIPAA Privacy and Security Rules.
- 16 CFR Part 682 — FCRA disposal rule.
- CCPA / CPRA — Cal. Civ. Code §1798.100 et seq.
- Reg S-P — 17 CFR §248.30.
- GDPR — Regulation (EU) 2016/679, Articles 5 and 28.
- UK GDPR — Data Protection Act 2018.
