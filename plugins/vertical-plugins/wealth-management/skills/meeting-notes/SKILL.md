---
name: meeting-notes
description: Turn raw client-meeting notes into a documented recap — a structured summary, decisions and IPS changes, action items with owners and dates, a client follow-up email, and a compliance file note. Use after a client review or planning meeting to write up what happened and what's next. Triggers on "write up my meeting", "meeting recap", "client meeting notes", "follow-up email after meeting", "document the meeting", or "what did we agree".
---

# Meeting Notes

The post-meeting counterpart to `client-review`: that skill prepares the meeting, this one documents it. Takes the advisor's raw notes (typed, dictated, or bullet fragments) and turns them into a clean, file-ready recap plus the follow-ups. It records what was discussed and decided — it does not give advice or execute anything.

## Workflow

### Step 1: Capture What Happened

Gather the raw inputs and normalize them:

- **Meeting basics**: client/household name, date, attendees (advisor, client, spouse, other professionals), meeting type (annual review, planning, ad hoc)
- **Raw notes**: paste, dictation, or fragments — whatever the advisor has
- **Context**: pull last meeting's action items if available, to check what closed
- If the notes are thin, ask targeted questions rather than inventing detail. Mark anything uncertain as `[CONFIRM]`.

### Step 2: Structure the Recap

Produce a clean internal recap:

- **Summary** — 3-5 sentences: what the meeting covered and the overall tone/outcome
- **Topics discussed** — grouped bullets (performance, planning, life changes, taxes, estate, concerns raised)
- **Decisions made** — what was actually agreed (e.g., "increase monthly contribution to $2,000", "revisit allocation after home sale")
- **Changes to the plan / IPS** — any change to objectives, risk tolerance, constraints, or allocation, flagged for the IPS change log
- **Open questions** — items raised but not resolved

### Step 3: Action Items

Extract a clear action table — owner and due date on every row:

| Action | Owner | Due | Notes |
|--------|-------|-----|-------|
| | | | |

- Separate **advisor** actions from **client** actions
- Carry forward any prior action items that are still open
- Where the client owes something (documents, decisions), note it for the follow-up email

### Step 4: Client Follow-Up Email

Draft a short, warm follow-up for the advisor to review and send:

- Thank them for their time; recap the 2-3 things that mattered most to *them*
- List what the advisor will do next and by when
- List clearly (but lightly) what you need from the client
- **No performance figures, projections, or recommendations in the email** unless the advisor explicitly adds them — keep it a recap, not advice
- Match the advisor's prior voice if earlier emails are available

### Step 5: Compliance File Note

Produce a concise, factual file note suitable for the CRM / compliance record:

- Date, attendees, topics, decisions, and any suitability-relevant changes (risk tolerance, objectives, time horizon, liquidity needs)
- Factual and neutral — record what was said and decided, not opinion
- Flag any item that may need supervisory review (e.g., a change in risk profile, a concentrated-position decision, a complaint)

## Example Interaction

**User**: "Just met with the Hendersons for their annual review — write it up. Notes: markets discussion, Bob retiring in 18 months not 3 years, wants more conservative, Sue asked about gifting to grandkids, need updated beneficiary form."

**Assistant**:
1. Builds the recap: retirement timeline moved up, shift toward conservative, gifting interest, beneficiary update
2. Flags the IPS change — **shorter time horizon + lower risk tolerance** — for the change log and supervisory review
3. Action table: advisor to model the 18-month retirement and propose a glide path (due date); client to return the beneficiary form
4. Drafts a warm follow-up email recapping the retirement timeline and gifting question, asking for the signed beneficiary form
5. Writes a neutral compliance file note recording the risk-profile change

## Important Notes

- **Documentation, not advice.** This skill records the meeting; it does not recommend products or allocations. Any recommendation is the advisor's, added on review.
- **Nothing is sent or filed automatically.** All output — email, file note, CRM entry — is staged for the advisor to review, edit, and submit.
- **Don't invent.** If a detail isn't in the notes, ask or mark `[CONFIRM]`; never fabricate what a client said or agreed to.
- **Flag suitability-relevant changes.** Changes to risk tolerance, objectives, time horizon, or liquidity needs should be surfaced for the IPS and any required supervisory review.
- **Compliance**: documentation and recordkeeping must follow firm policy and the regulations that apply to your firm.
