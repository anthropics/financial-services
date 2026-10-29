# Troubleshooting: scoping

The scope record is the bootstrapping primitive. When downstream skills produce wrong outputs (wrong regulator, wrong tone, evidence asks the engagement cannot satisfy, review gates that do not exist), the root cause is almost always a defect in the scope. This file walks the recurring defects and how to resolve them.

## 1. The charter becomes a one-time deliverable

**Symptom**: Three weeks into the engagement, the institution profile, regulator list, or out-of-scope items are stale. Downstream skills are still consuming the original record.

**Why it happens**: The engagement was scoped on day one and never revisited. New facts surfaced (an MRIA was added, a connector came online, a new regulator engaged) and the charter did not update.

**Resolution**:
- Treat scope as a status, not a fixed truth. Mid-flight scope is the version that exists today.
- Use the revision log. Every shift gets a dated row with reason and delta. Append-only.
- Make scope review a standing item in the engagement steering cadence (weekly for sprints, monthly for ongoing programs).
- Re-emit the scope record after any material change so downstream skills receive the updated version.

## 2. The out-of-scope list is empty or generic

**Symptom**: Mid-engagement steering committee or partner review challenges scope creep. The engagement has no written firewall to point at.

**Why it happens**: Practitioners are reluctant to write down what they will not do. The instinct is to leave room. The cost is later contestation.

**Resolution**:
- Force the practitioner to name three to five exclusions, even when the engagement feels well-bounded.
- Each exclusion is a sentence, not a noun. "Model risk" is not enough. "Model risk, including SR 11-7 validation work and model performance monitoring, which sits with the existing model validation engagement under SOW-2025-09" is a sentence.
- When scope creep arrives, point at the list. If the request is legitimate, log a revision and update the list.
- Advisory engagements: the out-of-scope list is the contractual defense. Internal engagements: it is the defence against priority drift.

## 3. The persona defaults to "compliance"

**Symptom**: Downstream skills produce CCO-flavored deliverables when the engagement is actually CRO-led, or AI-governance-flavored when it is BSA-led. Review gates are wrong. Tone is wrong.

**Why it happens**: The skill was invoked without explicit persona, or the practitioner reflexively wrote "compliance" because that is the default the broader industry uses.

**Resolution**:
- The persona role is enumerated for a reason. Pick the right one. CRO, head of model risk, head of TPRM, BSA officer, CCO, AI Governance Lead, engagement partner, embedded business risk officer (1.5-line), and so on are different functions with different review machinery.
- 1.5-line and 2-line are different. A regional risk officer embedded in a business unit (1.5-line) has different review authority from a corporate risk officer (2-line). Capture the lens.
- Review gates are named, not generic. "Committee review" alone is insufficient. Which committee? With what criteria?

## 4. The primary-regulator list has too many entries

**Symptom**: Every regulator that could conceivably apply is listed as primary. Downstream skills cite a confused regulator constellation. Citations are unfocused.

**Why it happens**: Practitioner anxiety about omitting a regulator. Also a misread of the field as "regulators with any relationship to this institution" rather than "regulators this engagement is addressing."

**Resolution**:
- Primary regulators is the list this engagement is actually addressing. Three is normal, five is a stretch, eight is broken.
- Conceivable-but-secondary regulators belong in `assumptions_and_dependencies` ("we assume the FRB consolidated supervisor will not request involvement in this exam scope").
- Fix the list before downstream skills consume it. A wrong regulator at the top distorts every citation choice the skill makes.

## 5. Source posture is over-claimed

**Symptom**: Posture is set to `connector-aware`, but downstream skills repeatedly ask for evidence the engagement cannot produce. Or posture is `public-plus-firm-policy-plus-evidence` and the firm policy library is not actually accessible.

**Why it happens**: The aspirational posture (what the firm wishes were available) was captured rather than the actual posture (what the engagement can pull today).

**Resolution**:
- Set source posture at the level the engagement actually has, today. Roadmap items go in `assumptions_and_dependencies` with target dates.
- `connectors_enabled` is the truth-test. If the list is empty, posture is at most `public-plus-firm-policy`.
- Update posture when a connector or evidence pathway actually opens. Log it as a revision.
- For advisory engagements, posture is also a contractual question. Confirm with the engagement letter.

## 6. Firm-specific facts encoded in the institution profile

**Symptom**: The institution profile includes firm-specific risk taxonomy lines, internal policy references, internal committee names, or proprietary review machinery. The charter does not survive being lifted to a peer engagement at a similar institution.

**Why it happens**: Firm-specific content leaked into the public-shaped institution profile because there was no `references/firm-overlay.md` to absorb it.

**Resolution**:
- Institution profile is descriptive of the institution as the regulator and the public would describe it. Type, charter, registrations, geographic footprint, primary regulators, public supervisory posture.
- Firm-specific content (firm risk taxonomy, internal policy library, firm review gates beyond the regulatory baseline, internal committee charters) belongs in `references/firm-overlay.md`. Set `risk_taxonomy_reference` to point at it.
- The charter should be readable by an external reviewer (advisory partner, regulator, auditor) without needing the firm-overlay file. The firm-overlay file is the customization layer.

## 7. Risk lens is too narrow or too wide

**Symptom**: Downstream skills load the wrong cross-cutting overlays. Cyber-relevant work omits cyber. Or the lens lists every risk type and downstream skills load every overlay, producing bloated outputs.

**Why it happens**: The practitioner did not check the lens against the engagement type.

**Resolution**:
- Match `risk_lens` to the engagement type and to the deliverable. An exam-readiness sprint for credit-risk and BSA is `[credit, financial-crime, operational]`, not `[credit]` and not `[credit, market, liquidity, operational, strategic, reputational, model, climate, cyber, conduct, financial-crime, consumer-compliance, third-party, ICT]`.
- Cross-cutting overlay set follows from risk lens. If `cyber` is in the lens, `cyber` overlay loads. If conduct is not in the lens but the engagement touches consumer-facing work, add it explicitly.
- When in doubt, ask the engagement sponsor. Do not guess.

## 8. The skill is invoked when it should not be

**Symptom**: Scoping is run on a one-off question or on a skill invocation that already has a scope on file. Output is wasted; the scope record drifts from the canonical one.

**Why it happens**: The downstream skill default-invoked scoping rather than checking for an existing scope.

**Resolution**:
- Downstream skills check for an existing scope record before invoking this skill.
- If a scope exists, consume it. If it is stale or contested, run a revision (not a fresh scope).
- For one-off questions (a quick obligation lookup, a single citation check), scoping is overkill. Skip it; use the public posture default.
- The "Not the right tool when" section of the activation description is the contract; the downstream skill respects it.
