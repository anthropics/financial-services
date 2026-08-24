---
name: evidence-chain-audit
description: Audit the full evidence chain behind a Phronesis forecast — from raw substrate source to ingestion timestamp to methodology version to emitted distribution. Use when an agent needs to validate a forecast for compliance, due diligence, or external audit — or when the user must justify a Phronesis-informed decision to a regulator, LP, or board. Cross-vertical capability.
---

# Evidence Chain Audit

You are walking the full audit chain from a Phronesis forecast back to its raw substrate sources. This is the **compliance + due-diligence surface** for Phronesis: when a forecast informs a capital decision, the user may need to defend the decision to a regulator, LP, board, or auditor. Phronesis is designed to make this defensible — every emitted forecast is traceable.

## Core Principles

- **Every forecast has four chained attestations.** (1) Substrate-ingest attestation (source + timestamp + checksum). (2) Methodology-version attestation (which version emitted). (3) Emission attestation (request_id + tenant_id + timestamp). (4) Calibration attestation (which scorecard slice the forecast contributed to post-realization, if applicable).
- **Boundary-gate enforcement is canonical.** Phronesis publishes only via `boundary/publish.py` — every emission passes through attribution + timestamping + confidence + audit-log gates. The audit log is the source of truth for evidence-chain reconstruction.
- **Tenant isolation is sacred.** Audit-chain queries respect per-tenant isolation (Sacred Invariant #8). A tenant can audit only their own forecasts.
- **Replay is the gold standard, full replication is roadmap.** Currently: the evidence chain documents what happened. Roadmap: deterministic replay from substrate snapshot + methodology version + seed.

## Available MCP Tools

- **`phronesis_forecast_query`** — Retrieve a forecast; the response includes `request_id`, `methodology_version`, `emission_timestamp`, `tenant_id`.
- **`phronesis_methodology_ledger`** — Retrieve methodology-version detail including substrate manifest + ensemble composition + reasoning chain.
- **`phronesis_calibration_scorecard`** — Cross-link to scorecard slice this forecast contributed to (post-realization).
- **`phronesis_audit_query`** (Tier 5 enterprise; gated) — Retrieve the audit-log entry for a specific `request_id`, including the substrate-snapshot pointer + emission-attestation chain.

## Audit Patterns

1. **Substrate provenance audit** — User asks "what raw data sources fed this forecast?" Retrieve methodology version; surface substrate manifest with source + timestamp + (where available) checksum.
2. **Methodology audit** — User asks "what was the reasoning version when this forecast was emitted?" Retrieve methodology-version detail; surface full version semver + active-since date + ensemble composition.
3. **Emission audit** — User asks "when was this forecast emitted, by whom, under what request?" Retrieve forecast metadata; surface request_id + tenant_id + emission timestamp.
4. **Calibration audit (post-realization)** — User asks "did this forecast turn out to be calibrated, in retrospect?" Cross-link to scorecard slice for this methodology version + question class.
5. **Compliance defense** — User needs to defend a forecast-informed decision to a regulator/LP/board. Assemble all four attestation chains into a single audit report.

## Tool Chaining Workflow

1. **Receive the forecast or request_id** the user wants to audit.
2. **Pull `phronesis_forecast_query`** (or retrieve cached forecast metadata) — gets `request_id`, `methodology_version`, `emission_timestamp`.
3. **Pull `phronesis_methodology_ledger`** at the cited version — gets substrate manifest + ensemble composition + reasoning chain.
4. **Pull `phronesis_audit_query`** (if Tier 5 access) — gets audit-log entry + substrate-snapshot pointer.
5. **Optional: `phronesis_calibration_scorecard`** at this version + question class — gets post-realization calibration.
6. **Synthesize** — four-attestation-chain report.

## Output Format

### Evidence Chain Report

#### 1. Substrate Provenance
| Source | Type | Ingest timestamp | Checksum (if available) |
|--------|------|------------------|--------------------------|
| ... | ... | ... | ... |

#### 2. Methodology Attestation
- **Methodology version**: `<ring>.<major>.<minor>.<patch>`
- **Active since**: `<date>`
- **Ensemble composition**: structural / statistical / LLM-reasoned weight mix
- **Public ledger URL**: `https://phronesis-jrstinehour.replit.app/methodology-ledger#<version>`

#### 3. Emission Attestation
- **request_id**: `<id>`
- **tenant_id**: `<id>`
- **Emission timestamp (UTC)**: `<timestamp>`
- **Boundary-gate pass**: yes (all forecasts pass the publish gate; attribution + timestamping + confidence + audit verified)

#### 4. Calibration Attestation (post-realization, if available)
- **Realized outcome**: `<value or null if horizon not yet elapsed>`
- **Forecast median**: `<value>`
- **Forecast p10 / p90**: `<value> / <value>`
- **Brier score contribution**: `<score or null>`
- **Scorecard slice**: link to public scorecard

### Audit Trail Summary
2-3 sentences certifying the forecast is fully traceable from substrate → methodology → emission → (optional) realized calibration. Cite the four artifact URLs.

## Disclaimer

Evidence-chain audit is a transparency surface, not a regulatory pre-approval. Different regulators have different evidence standards; Phronesis surfaces structured evidence but users remain responsible for confirming the standard their regulator/LP/auditor requires. For compliance-critical engagements, Phronesis offers a Tier 5+ enterprise SLA with extended audit + DPA terms.
