# Insurance sector overlay: obligation-mapping

Loaded when the scope includes `insurance` in `sector_overlay_set`. Adds insurance-specific source labels and obligation patterns the practitioner expects to find when the register scopes an insurance process. Does not change the row spine.

The federal-state interplay is the dominant feature: most insurance obligations live in state insurance code, with NAIC model laws as the starting point and state adoptions varying. The register must name the state of domicile and any host states with material business when applicability turns on state-specific rules.

## Sources the register may cite

### NAIC model laws as starting point

NAIC models do not bind directly; state-by-state adoption does. The register cites the NAIC model and the state adoption together where the state has adopted, and notes the state has not adopted where it has not.

- NAIC Model Audit Rule (Model #205 — Annual Financial Reporting Model Regulation). [verify section labels against current NAIC version.]
  - Use for: financial-reporting and internal-control-over-financial-reporting (ICFR-equivalent) obligations on insurers. Section references vary by state adoption.
  - Link: https://content.naic.org/

- NAIC Risk Management and Own Risk and Solvency Assessment (ORSA) Model Act (Model #505).
  - Use for: ORSA filing obligations, risk-management framework obligations, group-level risk obligations on insurance holding companies.

- NAIC Insurance Holding Company System Regulatory Act (Model #440) and the related Form B / Form F obligations.
  - Use for: holding-company-level reporting and intercompany-transaction obligations.

- NAIC Insurance Data Security Model Law (Model #668).
  - Use for: cybersecurity-program obligations in states that have adopted; cross-load with the cyber overlay.

- NAIC AI Bulletin (2023) and emerging NAIC AI model regulation work.
  - Use for: AI-system obligations on insurers (use-case inventories, governance, third-party AI model expectations); cross-load with AI overlays from `ai-governance-model-risk` references when the engagement also touches AI.

### ORSA and group capital

- ORSA Guidance Manual (NAIC) — the operational guidance behind Model #505. [verify section labels and current edition.]
  - Use for: ORSA Summary Report content obligations (sections 1, 2, 3 of the Manual).
  - Link: https://content.naic.org/cipr-topics/own-risk-and-solvency-assessment-orsa

### State-specific anchors (sample; the register names the actual state)

- New York Insurance Law and 11 NYCRR (DFS regulations). NYDFS Insurance Regulation 187 (suitability and best interests in life insurance and annuity transactions) §224.4, §224.6. [verify subsection labels.]
  - Use for: market-conduct obligations on life and annuity products sold in New York.
  - Link: https://www.dfs.ny.gov/

- California Insurance Code §790 et seq. (Unfair Insurance Practices Act).
  - Use for: market-conduct obligations on California-domiciled or California-licensed insurers.

- Texas Insurance Code Chapter 4001 et seq. (Licensing of Insurance Agents).
  - Use for: producer-licensing obligations.

### Federal hooks

- Gramm-Leach-Bliley Act privacy (15 U.S.C. §6801 et seq.) as implemented through state insurance privacy regulations modeled on NAIC Model #672 (Privacy of Consumer Financial and Health Information).
  - Use for: privacy obligations on insurers; cross-load with the privacy cross-cutting overlay.

- Federal Insurance Office Act provisions and federal preemption questions where federal action interacts with state insurance authority.
  - Use sparingly; FIO does not directly impose obligations on insurers in most contexts.

- Health Insurance Portability and Accountability Act for health insurers (45 CFR Parts 160, 162, 164).
  - Use for: PHI-handling obligations on health insurers.

## Obligation patterns the practitioner expects to find

- **State-by-state extraction with a domicile anchor.** For multi-state insurers, the register extracts obligations at the state level where the rule is state-specific, with the domicile state as primary and material host states as secondary. Identical or near-identical obligations across states roll up only when the substance is genuinely identical and the difference is form.
- **Holding-company and operating-company split.** Holding-company obligations under Model #440 and ORSA under Model #505 extract on the holding-company tier; operating-company obligations extract at the licensed-entity tier. The register names the entity each row applies to.
- **Producer (agent) and broker obligations.** Producer-licensing, suitability, and supervision obligations extract as their own cluster when the register scopes distribution.
- **Reinsurance and ceded-business obligations.** State reinsurance credit rules and NAIC Credit for Reinsurance Model Regulation (#786) extract when the register scopes reinsurance, including the ceded-business reporting obligations.
- **NAIC accreditation and model adoption status.** Where the register cites a NAIC model that the relevant state has adopted with modifications, the row notes the adoption form and any deviation; where the state has not adopted, the row reads `not-applicable` with the rationale.

## What does not belong here

- Bank-side obligations even where a financial-holding company owns both a bank and an insurer. Run a separate register on the bank with `banking` overlay.
- Federal securities-law obligations on the insurer's investment management or affiliated broker-dealer. Run a separate register or extend with the `capital-markets` overlay if the same engagement covers it.
- Internal firm policy and taxonomy. That goes in `references/firm-overlay.md`.
