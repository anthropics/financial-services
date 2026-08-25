# Insurance sector overlay — issue-writeup

Loads when the scope `sector_overlay_set` includes `insurance`. The overlay shapes the criteria block, the severity calibration, and the closure-evidence framing for issues at US insurance companies (P&C, life, health, reinsurance) supervised by state DOIs and coordinated through the NAIC.

## Why the insurance overlay matters

Insurance supervision in the US is state-led with NAIC coordination, which produces a different finding shape than the federal banking framework. State DOIs issue findings via market-conduct examination reports, financial examination reports, and supervisory letters; remediation is often documented through Memoranda of Understanding (MOUs), consent orders, or corrective action plans (CAPs). The criteria block, the severity calibration, and the closure-evidence framing all need to fit the state-DOI / NAIC convention, not the federal banking convention.

## Source basis

- **NAIC Financial Condition Examiners Handbook** — convention for financial-examination findings. The handbook structures findings around significant deficiencies, control weaknesses, and recommendations; severity calibration is anchored on the audit-risk-model concepts the handbook adopts from AICPA AU-C 265.
- **NAIC Market Regulation Handbook** — convention for market-conduct examination findings. Findings track to standards on policy forms, claims handling, producer licensing, advertising, complaint handling, and unfair trade practices.
- **NAIC Model Audit Rule (MAR; Annual Financial Reporting Model Regulation, MDL-205)** — internal control over financial reporting framework adopted in most states. Findings on insurer internal control over financial reporting cite MAR §16 (notification of unremediated material weakness).
- **NAIC ORSA Guidance Manual** — Own Risk and Solvency Assessment framework. Enterprise-risk findings at ORSA-eligible insurers cite the relevant ORSA component (risk identification, risk-management framework, risk-appetite-and-tolerance, capital adequacy).
- **State DOI MOU and consent-order language conventions** — varies by state but most state DOIs publish enforcement actions; the language patterns in posted MOUs and consent orders inform the criteria-citation discipline. [verify specific state references against the state's actual language; New York DFS, California DOI, Texas DOI, and Florida OIR are frequently cited examples.]
- **NAIC AI Bulletin (Model Bulletin on the Use of Artificial Intelligence Systems by Insurers, December 2023)** — AI-system findings at insurers cite the bulletin's governance framework expectations.

## What the overlay adds to the write-up

### Examination finding format

When the source type is examiner-letter and the regulator is a state DOI, the criteria block follows the state DOI's examination-report format. State DOI examination reports typically structure findings as:
- **Comment** (an observation that does not rise to the level of a deficiency)
- **Recommendation** (a deficiency in policies, procedures, or controls that should be corrected)
- **Citation / violation** (a confirmed violation of statute, regulation, or department rule)

The firm's internal issue write-up mirrors this structure: a finding labelled as a recommendation in the DOI's report is typically severity moderate or high in the firm's calibration; a citation/violation is high or critical. The `mra_mria_classification` field is set to `n/a` because the federal banking MRA / MRIA / MRBA framework does not apply.

### Severity calibration

Insurance severity calibration weighs (1) policyholder impact, (2) financial solvency impact, (3) market-conduct violation dimension, and (4) producer / distribution channel implications. Findings that touch financial reporting under MAR carry severity tied to the materiality framework AICPA AU-C 265 sets. Market-conduct findings carry severity tied to consumer-harm scope, repeated-pattern frequency, and unfair-trade-practice exposure.

### Closure-evidence framing

State DOIs typically follow up via the next examination cycle (financial exams every three to five years; market-conduct exams on a state-by-state cadence). Closure evidence for state-DOI-issued findings names:
- The artifact (board minutes, committee minutes, system-of-record output, sign-off log).
- The retention location (insurer's GRC platform, board-portal, regulatory-filings system).
- The DOI's expected re-inspection touchpoint (next exam cycle, mid-cycle continuous-monitoring touchpoint, or specific follow-up letter).

When the finding has been remediated through an MOU or consent order, the closure evidence references the MOU / consent-order satisfaction terms specifically.

### MAR §16 material-weakness pathway

For insurers subject to MAR (most insurers above the state-defined threshold), unremediated material weaknesses in internal control over financial reporting trigger §16 notification to the state DOI. An issue write-up on a control deficiency that is heading toward material-weakness classification carries the §16 implication in the severity rationale; the criteria block cites MAR §16 directly.

### ORSA-driven enterprise-risk findings

For ORSA-eligible insurers, findings on the enterprise-risk-management framework, risk-appetite-and-tolerance, or capital-adequacy assessment carry severity weight tied to the ORSA component implicated. The criteria block cites the relevant ORSA Guidance Manual section.

## Common patterns

- **Multi-state market-conduct finding**. A market-conduct finding identified by one state often replicates across other states where the insurer is licensed; the issue write-up names the state of identification and flags the other-state implication in the impact section.
- **MOU resolution shape**. Many state DOI findings are resolved via MOU rather than via consent order; the MOU is the closure-evidence anchor. The MOU specifies the corrective action, the milestone schedule, and the DOI's re-inspection terms.
- **NAIC accreditation continuity**. Findings on the state DOI's own performance against NAIC accreditation standards do not appear in firm-side issue write-ups, but findings on the insurer that affect the DOI's accreditation evaluation can carry an indirect severity weight; flag in the severity rationale where applicable.

## Implications for the CCCE

- **Criteria** for insurance-overlay issues cite the state insurance code section first (or NAIC Model Law section if the state has adopted the model), then NAIC handbook section second, then firm policy third. State-specific deviation from the NAIC model carries a separate criteria entry where applicable.
- **Cause** for market-conduct findings ties to the specific operational control that failed (claims-handling timeliness control, producer-licensing-verification control, complaint-handling-tracking control). For financial-reporting findings, the cause maps to a COSO component or principle as MAR adopts the COSO framework.
- **Effect** for insurance issues quantifies policyholder impact distinctly from financial impact distinctly from market-conduct violation impact. Consumer-harm scope is typically named in policyholder-count terms and dollar-restitution terms.
- **Closure evidence** for state-DOI-issued findings references the DOI's expected re-inspection touchpoint, not just the firm-internal sign-off cadence.

## Anchors used by this overlay

- NAIC Financial Condition Examiners Handbook (current edition). https://content.naic.org/cmte_e_fcrr.htm [verify current edition section labels.]
- NAIC Market Regulation Handbook (current edition). https://content.naic.org/cmte_d_mar.htm [verify current edition section labels.]
- NAIC Annual Financial Reporting Model Regulation (Model 205) — MAR. https://content.naic.org/cmte_d.htm [verify current model regulation section labels.]
- NAIC ORSA Guidance Manual. https://content.naic.org/cmte_e_orsa.htm [verify current edition section labels.]
- NAIC Model Bulletin on the Use of Artificial Intelligence Systems by Insurers (December 2023). [verify current state adoption status; bulletin adoption varies by state.]
- State-specific examination report and consent-order language patterns vary by state DOI; the firm-overlay names the state-specific anchors that apply to the insurer.
