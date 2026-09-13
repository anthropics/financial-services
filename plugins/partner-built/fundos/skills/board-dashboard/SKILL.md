---
name: board-dashboard
description: Turn a completed variance analysis into a board-ready one-page pack — KPI tiles with provenance, a gross-to-net bridge (waterfall), a management message, and line detail underneath. Use after variance commentary, when preparing an IC or board pack, or when someone asks for a dashboard, a one-pager, or a visual summary of the numbers. Triggers on "board pack", "board deck", "dashboard", "one-pager", "IC pack", "waterfall chart", "bridge chart", "KPI tiles", or "make this presentable".
---

# Board Dashboard

You turn a finished analysis into something a board can read in ten seconds. This skill is the second half of a pair: **variance-commentary** produces the analysis, this presents it.

## Do not rebuild the numbers

Take the figures from the analysis that already ran. Do not re-derive, re-total, or re-bucket them here, and do not "tidy" a number so a chart looks better.

FundOS builds the tiles and the bridge in Python (`flux_pack.build_pack`) and foots the bridge in code before rendering. If you are working from a FundOS pack, the arithmetic is already checked — your job is layout and language. If you are assembling a pack by hand from figures a user pasted, say plainly that nothing has been footed, because the reader cannot tell the difference from the page.

## Available FundOS MCP Tools

- **`fundos_list_fund_accounts`** — pick the vehicle
- **`fundos_call_tool`** — invoke `cfo.flux` for the computed table and pack spec
- **`fundos_compute_pnl`** — surrounding P&L context when the pack needs it

## Layout

Top to bottom, in this order. The order is the point: a reader who stops after the first line should still have the answer.

### 1. Management message
One sentence stating the so-what — what happened, what drove it, what to pressure-test. Not a summary of the page below it.

### 2. KPI tiles
One tile per headline metric. Each tile carries:
- the **value**,
- the **change** in amount and percent,
- the **basis** — "vs budget" or "vs prior", never left implied,
- a **Source** line naming the fund, the period and the basis.

The source line is not decoration. A tile without provenance is a number with no way to check it, and board packs get forwarded.

### 3. Gross-to-net bridge
Opening basis → one bar per material mover, largest first → closing actual. Collapse the immaterial tail into a single "Other" bar rather than showing twenty slivers.

### 4. Line detail
The full table underneath, as the drill-in. Material lines carry their driver sentence.

## The footing verdict is part of the design

State it on the page, every time.

- **Foots** — show the check quietly: components, stated total, residual.
- **Does not foot** — banner it at the top, and render the gap as **its own labelled "Unexplained" bar**. Never fold a residual into "Other" to make the waterfall close. A bridge that closes because you hid the gap is worse than one that visibly doesn't, because it has stopped being evidence.

## Mark it a draft

Put **DRAFT FOR HUMAN REVIEW** on the pack until a human has signed it off. Board packs are forwarded, screenshotted and quoted; the badge travels with the file and is the difference between a working document and an apparent management assertion.

## If the management message is missing

Say so, name the reason, and add that the figures are unaffected because they are computed in code. Do not write a substitute so-what — a message the model invented is indistinguishable, on the page, from one the CFO wrote.

## Output format

Prefer a **single self-contained file** — inline CSS, inline SVG for the waterfall, no external scripts or CDN references. A pack that needs the network to display its own numbers will render blank from a data room, an email attachment, or a laptop on a plane.

FundOS publishes exactly this shape (`/fundos/cfo/flux/pack/<run_id>` → Publish to room) as XLSX, PDF and self-contained HTML, all three rendered from the same footed spec, filed into the fund's reporting room with an audit trail.

## Related

- **variance-commentary** — produces the analysis this skill presents.
- **lp-communications** — for LP-facing letters rather than board packs.
