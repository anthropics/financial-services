---
name: deal-sourcing
description: PE deal sourcing workflow — discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails. Use when sourcing new deals, prospecting companies in a sector, or reaching out to founders. Triggers on "find companies", "source deals", "draft founder email", "check if we've seen this company", or "outreach to founder".
---

# Deal Sourcing

## Workflow

This skill follows a 3-step sourcing pipeline:

### Step 1: Discover Companies

Research and identify potential target companies based on the user's criteria:

- **Sector/industry focus**: Ask the user what space they're looking in (e.g., "B2B SaaS in healthcare", "industrial services in the Southeast")
- **Deal parameters**: Revenue range, EBITDA range, growth profile, geography, ownership type (founder-owned, PE-backed, corporate carve-out)
- **Sources**: Use web search to find companies matching criteria. Look at industry reports, conference attendee lists, trade publications, and competitor landscapes
- **Output**: A shortlist of companies with: name, description, estimated revenue/size, location, founder/CEO name, website, and why they fit the thesis

### Step 2: CRM Check

Before outreach, check if the company or founder already exists in the firm's CRM:

- Search the user's email (Gmail) for prior correspondence with the company or founder
- Search Slack for any internal mentions or prior discussions about the target
- Ask the user: "Have you or your team had any prior contact with [Company]?"
- Flag any existing relationships, prior passes, or known context
- **Output**: For each company, note: "New" (no prior contact), "Existing" (prior correspondence found — summarize), or "Previously Passed" (if evidence of a prior pass)

### Step 3: Draft Founder Outreach

Draft personalized cold emails to founders/CEOs:

- **Tone**: Professional but warm. Not overly formal — founders respond better to genuine, concise outreach
- **Structure**:
  1. Brief intro — who you are and your firm (ask user for their firm intro if not known)
  2. Why this company caught your attention — reference something specific (product, market position, growth)
  3. What you're looking for — partnership, not just a transaction
  4. Soft ask — "Would you be open to a brief conversation?"
- **Personalization**: Reference the company's specific product, recent news, or market position. Never use generic templates
- **Length**: 4-6 sentences max. Founders are busy
- **Voice matching**: If the user has sent prior outreach emails, study them to match their tone and style. Search Gmail for "sent" emails with keywords like "reaching out", "introduction", "partnership" to find examples

### Email Draft Guidelines

- Subject line: Keep it short and specific. Reference the company or sector, not "Investment Opportunity"
- No attachments on first touch
- Include a clear but low-pressure CTA
- Draft in Gmail if available, otherwise output as text for the user to copy

## Example Interaction

**User**: "Find me founder-owned industrial services companies in Texas doing $10-50M revenue"

**Assistant**:
1. Searches web for industrial services companies in Texas matching the criteria
2. Presents a shortlist of 5-8 companies with key details
3. For each, checks Gmail/Slack for prior contact
4. Drafts personalized outreach emails for the ones marked "New"
5. Presents drafts for user review before sending

## Important Notes

- Always present the shortlist for user review before drafting emails
- Never send emails without explicit user approval
- If the user's firm intro or investment criteria aren't clear, ask before drafting
- Prioritize quality over quantity — 5 well-researched targets beat 20 generic ones
