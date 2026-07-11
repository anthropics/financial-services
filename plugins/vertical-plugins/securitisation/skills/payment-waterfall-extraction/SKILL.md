---
name: payment-waterfall-extraction
description: >-
  Extract the priority of payments (waterfall) from an ABS prospectus, a CLO indenture, or
  a 10-D investor report, and render it as an ordered, condition-aware sequence, handling
  sequential-versus-pro-rata logic, turbo and OC build, trigger switches, and pre- and
  post-event-of-default variants. Use when the user wants the waterfall, application of
  funds, or priority of payments laid out clearly, with the triggers that reorder it.
---

# Payment Waterfall Extraction

> EDGAR access in this skill uses the bundled `securitisation-edgar` connector. If its tools are missing or erroring, see [CONNECTOR.md](../../CONNECTOR.md) — do not substitute web search for filings.

Locate the **"Priority of Payments" / "Application of Available Funds" / "Distribution"**
section and reconstruct it as an **ordered list of steps, each with its condition**.
For registered ABS, fetch the 424B or 10-D with **`get_filing_document`**; for CLOs and
private deals, use the supplied document.

## Standard ABS / consumer waterfall (typical order)
1. **Fees & expenses** — servicing fee; trustee, owner-trustee, asset-rep-reviewer,
   and administrative fees (often capped before, uncapped after an EOD).
2. **Senior note interest** — by seniority (Class A pro-rata, then B, then C, …).
3. **Principal** — the *First Priority / Required Principal Distribution Amount* to
   cure undercollateralization, then per the principal rules (often **sequential**
   to the senior class until retired, then down the stack; sometimes **pro-rata**
   among Class A while a step-down test passes).
4. **Reserve account** — top up to its required amount/floor.
5. **Subordinate interest then principal** (Class B/C/D) as available.
6. **Overcollateralization build** — apply excess spread to reach the **OC target**
   (a **turbo** feature).
7. **Other** — indemnities, additional fees.
8. **Residual** — to the certificateholder / equity / depositor.

## Trigger logic that REORDERS the waterfall
- **Sequential vs pro-rata switch:** pro-rata among senior notes only while a
  cumulative-loss / delinquency / OC **step-down test** passes; on breach it reverts
  to strict **sequential**.
- **Cumulative net loss / delinquency triggers:** breach typically **traps cash**,
  **accelerates OC build**, and stops releases to equity.
- **Events of default / acceleration:** switch to a **post-EOD** waterfall — usually
  strict sequential senior-first, fees may become uncapped.

## CLO specifics
Capture the **interest waterfall** and **principal waterfall** separately. Mark each
**coverage-test (OC/IC) diversion** point where failure redirects cash to delever the
senior notes, and the **interest-diversion / par-flush** step. Note the
**reinvestment** treatment of principal during the reinvestment period.

## Method
1. Find the section; read it fully (page with `offset` if long).
2. Capture every step **in order**, preserving its **condition** verbatim in plain words.
3. If the document defines **pre- and post-trigger** (or **pre-/post-EOD**) waterfalls,
   extract **both** and label them.
4. Identify any **turbo**, **step-down**, and **trigger** definitions and link them to
   the steps they affect.

## Output
A numbered waterfall (one per regime), each step annotated with its condition, plus a
short **triggers** note explaining what changes the order and when. Where helpful, add
a simple top-to-bottom diagram. Cite the source section/URL. Mark unstated mechanics as
**"not specified in this document"**.
