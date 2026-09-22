# Insurance sector overlay — human-review-gates

Loads when the scope `sector_overlay_set` includes `insurance`. The overlay shapes the decision-authority block, the independence requirements, the documentation conventions, and the board-oversight expectations for gate matrices at US insurance companies (life, P&C, health insurers, plus reinsurers and insurance holding companies regulated by state DOIs and coordinated through the NAIC).

## Why the insurance overlay matters

State insurance regulators coordinate via the NAIC, which publishes Model Acts and Model Regulations the states adopt with variation. The governance architecture is distinct from federal banking governance: insurance commissioners, not federal banking supervisors, are the primary regulators; ORSA (Own Risk and Solvency Assessment) is the enterprise-risk artifact rather than the bank-style risk-appetite-statement; the audit committee requirement under most state insurance-holding-company statutes is statutory rather than supervisory. A gate matrix for an insurer that uses bank governance vocabulary will read as misaligned to a state insurance examiner.

## Source basis

- **NAIC Risk Management and Own Risk and Solvency Assessment (ORSA) Model Act (MDL-505)**. ORSA is the insurer's enterprise risk-management framework and capital-assessment artifact; the ORSA process is itself a gated set of decisions, and gate matrices for insurer enterprise risk reference the ORSA framework. Operative for insurance groups at the states' premium thresholds (typically $500M individual or $1B group, with state variation).
- **NAIC Corporate Governance Annual Disclosure Model Act (MDL-305) and Model Regulation (MDL-306)**. Annual disclosure to the domiciliary state of the insurer's corporate governance practices, including board composition, committee structure, and policies on senior officer oversight. The disclosure framing informs how gates are documented and how the board-committee structure is named.
- **NAIC Model Audit Rule — Annual Financial Reporting Model Regulation (MDL-205)**. Audit committee independence requirements; the audit committee is a statutory committee under most state insurance laws, with named independence requirements that flow into gate matrices for finance, audit, and internal-control-related decisions.
- **NAIC Insurance Holding Company System Regulatory Act (MDL-440) and Regulation (MDL-450)**. Group-supervision framework; Form B annual filing requirements include governance disclosures.
- **NAIC AI Bulletin (2023)**. State insurance regulator expectations on AI governance for insurer use cases (underwriting, claims, fraud detection); the Bulletin's governance-framework language informs AI-related gate construction at insurers.
- **State DOI bulletins** (varies by state). Specific governance and committee-charter expectations from individual state insurance commissioners; California, New York DFS (which regulates insurers as well as banks), and Texas tend to publish the most-cited state-specific guidance.

## What the overlay adds to the matrix

### Decision authority — board and audit committee

The insurer's matrix names the board of directors as the ultimate adopting body, with the audit committee as the named statutory body for finance, audit, and internal-control-related gates (Model Audit Rule). Risk-related governance gates flow through a risk committee or a combined risk-and-audit committee depending on the firm's structure (NAIC Corporate Governance Annual Disclosure framework documents the structure annually). For insurance groups under the NAIC Holding Company framework, the holding-company board has additional oversight on group-level gates.

### ORSA-anchored governance gates

For insurers above the ORSA threshold (state-by-state, typically $500M individual or $1B group), the ORSA framework is itself the source for enterprise-risk gates. The matrix references ORSA for: enterprise risk identification gates, capital assessment gates, prospective solvency assessment gates, and the annual ORSA Summary Report sign-off gate. The ORSA Summary Report sign-off is itself a high-stakes gate; the documentation requirement names the report, the named attesters (typically the CRO and the CEO with board concurrence), the date, and the regulator submission.

### Audit committee independence

The Model Audit Rule sets named independence requirements for the audit committee that flow into gate matrices for finance and internal-control-related decisions. Audit committee members must meet specific independence criteria (no material relationship with the insurer; no compensation other than committee fees and equity-based compensation under the Model Audit Rule's framing). The matrix's `independence_basis` for audit-committee-anchored gates cites the Model Audit Rule.

### Statutory accounting and reserving gates

Gates touching statutory accounting decisions (reserves, asset valuation, capital classification under risk-based capital rules) are statutory under state insurance law. The matrix references the relevant SAP (Statutory Accounting Principles) standard; reserving gates name the appointed actuary as the independent reviewer (the appointed actuary is a state-statutory role with named independence from management on actuarial opinion).

### NAIC AI Bulletin governance for AI use cases

For insurers deploying AI in underwriting, claims, fraud detection, or pricing, the NAIC AI Bulletin (2023) frames the governance expectations. The matrix references the Bulletin's governance-framework language for AI-related gates: senior management oversight, board awareness, governance committee structure, third-party AI vendor oversight, and consumer-impact assessment. For New York-regulated insurers, the NYDFS AI Industry Letter (2024) layers onto the NAIC framework with state-specific language on insurer AI use.

### State DOI variation

Gates at multi-state insurers reflect the domiciliary state's specific governance expectations, with secondary-state extensions where licensed-state requirements add to (rather than replace) domiciliary requirements. The matrix's `scope_notes` block names the domiciliary state and the multi-state footprint; the `firm-overlay.md` lists the state-specific bulletins the firm has implemented.

## Common patterns

- **Audit committee under-staffed for material-control gates**. Audit committee composition under the Model Audit Rule requires independence and financial literacy; smaller insurers often staff the audit committee at minimum statutory requirements, which is fine until a material-control gate (Sarbanes-Oxley-equivalent for filers, or material reserving change for any insurer) puts strain on the committee. The matrix surfaces this in the gap section when the audit-committee gate count is high relative to committee capacity.
- **ORSA Summary Report sign-off as a single annual gate**. For insurers above the ORSA threshold, the ORSA Summary Report is filed annually with the lead state. The sign-off gate is annual; the upstream gates (ERM framework refresh, capital-assessment refresh, prospective-solvency-assessment refresh) feed it. The matrix sequences these.
- **Appointed-actuary independence**. The appointed actuary's independence on reserving-decision gates is statutory; the matrix carries the independence flag with the specific state-statutory citation (varies by state).
- **NAIC AI Bulletin gap on legacy use cases**. Insurers with AI in production from before the 2023 NAIC AI Bulletin sometimes have governance gates that pre-date the Bulletin's expectations. The matrix's gap section flags the specific Bulletin sections not yet reflected.

## Implications for gate construction

- Decision authority for insurer matrices typically names: board of directors, audit committee (statutory), risk committee or combined risk/audit committee, governance/nominating committee, and enterprise risk management committee at the management level. The board overrides at the top; specific gate types route to specific committees based on subject matter.
- Independence on insurer gates is grounded in the Model Audit Rule for audit-committee-anchored gates, the Holding Company framework for group-level gates, and state-statutory citations for reserving and actuarial opinion gates.
- Documentation requirement on insurer gates names the system of record (typically the GRC platform plus the board-portal), the retention (state-by-state; California is among the longest at 5+ years for board minutes), and the regulator-submission cadence where the gate's record is filed (Form B, ORSA Summary Report, Corporate Governance Annual Disclosure).
- The gap section explicitly checks for: missing audit-committee independence on Model-Audit-Rule-anchored gates; missing appointed-actuary independence on reserving gates; missing ORSA Summary Report sign-off gate for above-threshold insurers; missing NAIC AI Bulletin alignment for AI-using insurers.

## Anchors used by this overlay

- NAIC Risk Management and Own Risk and Solvency Assessment (ORSA) Model Act (MDL-505). https://content.naic.org/sites/default/files/MO505.pdf
- NAIC Corporate Governance Annual Disclosure Model Act (MDL-305). https://content.naic.org/sites/default/files/inline-files/MDL-305.pdf
- NAIC Corporate Governance Annual Disclosure Model Regulation (MDL-306). https://content.naic.org/sites/default/files/inline-files/MDL-306.pdf
- NAIC Annual Financial Reporting Model Regulation (Model Audit Rule, MDL-205). https://content.naic.org/sites/default/files/inline-files/MDL-205.pdf
- NAIC Insurance Holding Company System Regulatory Act (MDL-440). https://content.naic.org/sites/default/files/inline-files/MDL-440.pdf
- NAIC AI Bulletin — Use of Artificial Intelligence Systems by Insurers (2023). https://content.naic.org/sites/default/files/inline-files/2023-12-04%20Model%20Bulletin_Adopted_0.pdf
- NYDFS AI Industry Letter (2024) — Use of AI in Underwriting and Pricing. https://www.dfs.ny.gov/industry_guidance/circular_letters
- State DOI bulletins — varies by state; firm-overlay names the state-specific bulletins the firm has implemented.
