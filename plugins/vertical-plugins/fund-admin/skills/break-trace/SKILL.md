---
name: break-trace
description: Root-cause a reconciliation break to its source transaction or posting — follow the audit trail from the break row back to the originating entry on each side and state what differs and why. Use after gl-recon has classified a break.
---

# Root-cause a break

Given a single break row (key, GL values, subledger values, bucket, likely cause), trace it to source and produce a root-cause statement.

## Trace path

1. **Pull the GL side** — via the internal-gl MCP, fetch the journal entry or posting that produced this GL line: entry id, posting date, source system, batch id, preparer.
2. **Pull the subledger side** — via the subledger MCP, fetch the matching transaction: trade id, trade/settle dates, counterparty, source feed, FX rate used.
3. **Diff the attributes** — line up posting date, FX rate/date, account mapping, quantity sign, amount sign. The differing attribute is usually the cause.

## Cause → statement

Write the root cause as a single sentence in the form **"⟨side⟩ ⟨did what⟩ because ⟨reason⟩"**, e.g.:

- "GL posted on settle date (T+2) while subledger posted on trade date — timing break, will clear on 2026-05-07."
- "Subledger used WM/R 4pm rate; GL used Bloomberg close — FX break of 12 bps on the base amount."
- "Security ABC123 maps to GL account 11420 in the mapping table but the subledger fed 11410 — mapping break, raise to reference-data."
- "Subledger posted the trade twice (trade ids 88412 and 88419 are duplicates) — duplicate post, suppress 88419."

## Output

For each traced break, return:

```json
{
  "key": "...",
  "root_cause": "one sentence as above",
  "owner": "ops | reference-data | accounting | upstream-system",
  "expected_clear_date": "YYYY-MM-DD or null",
  "action": "monitor | adjust | raise-ticket | suppress"
}
```

Only the resolver writes adjustments — this skill diagnoses, it does not post.
