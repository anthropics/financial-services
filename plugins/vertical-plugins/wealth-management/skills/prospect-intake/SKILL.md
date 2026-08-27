---
name: prospect-intake
description: Wealth-management prospect intake and qualification. Capture an inbound lead (referral, seminar sign-up, web form, or COI introduction), enrich it from public sources, qualify against the advisor's ideal-client profile and account minimum, dedupe against the CRM, and draft a compliant first-touch email plus a first-meeting agenda — all staged for advisor review. Use when a new lead comes in and you need to decide whether and how to pursue it. Triggers on "new prospect", "qualify this lead", "intake a referral", "should I take this client", "draft intro to prospect", or "got a referral from".
---

# Prospect Intake

Turns an inbound lead into a qualified, deduped, advisor-ready next step. This skill helps decide *whether* to pursue and drafts *how* to reach out — it does not give investment advice, make a suitability determination, or send anything on its own.

## Workflow

This skill follows a 5-step intake pipeline. Stop and surface for advisor review at Step 3 (the qualify call) and again before any outreach leaves.

### Step 1: Capture the Lead

Normalize whatever came in — a referral text, a seminar sign-up row, a website form, a LinkedIn message — into one structured prospect record:

- **Name and household**: prospect name, spouse/partner, dependents if mentioned
- **Source**: referral (and *who* referred — a client, a center of influence/COI, an attorney/CPA), seminar, web form, inbound call, networking
- **Stated need / trigger event**: what prompted the inquiry (retirement, liquidity event, job change, inheritance, dissatisfaction with current advisor)
- **Estimated investable assets**: as stated or implied — never invented
- **Location**: state/region (matters for licensing)
- **Contact**: email, phone, preferred channel
- **Output**: a clean prospect card. Mark any field you couldn't fill as `[MISSING]` and list what to ask the referrer or prospect.

### Step 2: Enrich (Public Sources Only)

Build light context from **publicly available** information — company/role, LinkedIn headline, public bios, press mentions:

- Use only public sources. **Do not scrape behind logins, buy data lists, or pull anything the prospect hasn't made public.**
- The goal is enough context to qualify and personalize — not a dossier.
- **Output**: 3-5 context bullets. Mark anything not directly confirmed as `[UNVERIFIED]`.

### Step 3: Qualify

Score the prospect against the advisor's **ideal-client profile (ICP)** and **account minimum**. If these aren't known, ask before scoring — don't assume a number.

- **Fit signals**: assets vs. minimum, complexity that matches the firm's strength (equity comp, business owner, multigenerational), location within licensed states, healthy referral source
- **Friction signals**: below minimum, out-of-state licensing gap, conflict with an existing client, services the firm doesn't offer, do-not-contact status
- **Output — a single recommendation** with a one-line reason:
  - **Pursue** — strong fit, move to outreach
  - **Nurture** — promising but early (e.g., liquidity event 12+ months out); set a follow-up date
  - **Refer out** — better served elsewhere; suggest a graceful referral
  - **Decline** — politely close the loop with the referrer

### Step 4: CRM & Relationship Dedupe

Before any outreach, check whether the prospect or referrer is already known:

- Search Gmail/Slack/CRM for prior correspondence with the prospect or household
- Check for an existing relationship with the **referrer** (a referral from a top client is handled differently than a cold web form)
- **Output**: label each prospect **New** (no prior contact), **Existing** (prior contact — summarize), or **Previously Passed** (evidence of a prior decline — surface the context before re-engaging)

### Step 5: Draft First-Touch + Meeting Agenda

For prospects marked **Pursue**, draft — for advisor review, never to send automatically:

- **First-touch email**:
  - **Tone**: warm, concise, professional. Reference the **referral source by name** when there is one ("Jane Doe suggested I reach out") — referral warmth is the whole point.
  - **Structure**: brief intro → why you're reaching out (tie to their trigger event) → what a first conversation looks like (no obligation) → soft ask for a short call
  - **Length**: 4-6 sentences. **No attachments, no performance figures, no product pitch** on first touch.
  - **Voice matching**: if the advisor has sent prior intro emails, study them (search Gmail "sent" for "reaching out", "introduction", "great connecting") and match their voice.
- **First-meeting agenda**: a short discovery-focused agenda (goals, current situation, what prompted the call, how the firm works, mutual next step) — discovery, not a pitch.

## Example Interaction

**User**: "Got a referral from my client Tom — his colleague Dana just sold her company and needs help. Should I take her on?"

**Assistant**:
1. Captures Dana into a prospect card (source: referral from client Tom; trigger: business sale/liquidity event; flags `[MISSING]` assets, location, contact)
2. Asks Tom or Dana for the missing pieces; enriches role/background from public sources, marking unverified items
3. Qualifies against the firm's ICP and minimum → recommends **Pursue** (liquidity event + warm top-client referral), noting to confirm the state for licensing
4. Searches Gmail/CRM → labels Dana **New**, confirms Tom is an existing client
5. Drafts a 5-sentence first-touch that names Tom as the referrer and a discovery-focused first-meeting agenda — and presents both for the advisor to review and send

## Important Notes

- **Stage everything for advisor review.** Never send an email, log a CRM contact, or contact a prospect without explicit advisor approval.
- **No advice, no suitability call.** This skill qualifies *fit and process*; it does not recommend products, allocations, or make a suitability/Reg BI determination — that happens after discovery, with the advisor.
- **Honor do-not-contact and prior passes.** If a prospect previously asked not to be contacted or was passed on, surface that and stop.
- **Respect the referrer.** A referral is a loan of trust from the person who made it — close the loop with them whatever the outcome.
- **Quality over volume.** A few well-qualified, well-researched prospects beat a long unfiltered list.
- **Compliance**: ensure all outreach and materials follow firm policy, advertising/testimonial rules, and the regulations that apply to your firm.
