---
description: Build the access_policies value — the granular, IAM-shaped way to allow or deny add-in features
---

# Configure access_policies

`access_policies` is the add-in's access-control mechanism going forward: a JSON
list of allow/deny **statements** — IAM-shaped — that decide which
features are available and under what conditions. Where `disabled_features` is a
single flat list — a feature is on or off for everyone — `access_policies` gives
you the same off switch *plus* conditions and effects:

| Want | `disabled_features` | `access_policies` |
|---|---|---|
| Turn a feature off for everyone | ✔ `disabled_features='skills.authoring'` | ✔ a resource-less `deny` statement (same effect) |
| Turn a feature off only on certain documents | ✗ | ✔ add a `resource` (e.g. a sensitivity label) |
| Turn a feature off *except* for approved documents (allowlist) | ✗ | ✔ `"effect": "allow"` |
| Attribute the block in UI copy / telemetry | limited | ✔ per-statement `description` and source |

A statement with **no `resource`** is exactly `disabled_features` — so anything
you'd put there, you can put here. The `resource` is what adds granularity, and its
`type` is the extension point: today the resource is a document identified by its
**Microsoft Purview sensitivity label** (`open_file`, `uploaded_file`); further
resource types plug into the same shape without a new config key. New deployments
should start here; `disabled_features` remains supported for the simple flat case.

Two label-conditioned controls ship today:

- **Whether the add-in runs at all on an open document** (the `addin.access` kill
  switch), keyed off the open document's label.
- **Whether a file may be attached as an upload** (`file.upload`), keyed off the
  *attached* file's own label — Office files and PDFs.

Walk the admin through the four steps below, then hand the finished JSON to
[manifest](manifest.md#access_policies) as one more key.

## 1. Get the label GUIDs

Statements match on the label's **GUID** (`mip_label_guid`) — stable across
renames and locales. Have the admin pull their taxonomy once with the Purview
compliance PowerShell module (no app registration needed; it uses Microsoft's
first-party sign-in):

```powershell
# One-time: Install-Module ExchangeOnlineManagement
Connect-IPPSSession -UserPrincipalName admin@theirtenant.com
Get-Label | Sort-Object Priority | Format-Table Priority, DisplayName, Name, Guid, ParentId
```

Ask them to paste the table. From it, note for each label they care about:
`Guid` (what you'll match), `DisplayName`, and `ParentId` (non-empty means it's
a *sublabel* — see the parent-label rule below).

If they can't run PowerShell, GUIDs are also visible in the Purview compliance
portal URL when a label is opened for editing, or via Microsoft Graph Explorer
(`GET /security/informationProtection/sensitivityLabels`).

## 2. Choose the statements

Ask which of these shapes they need — most tenants want the first, second, or
both. Then substitute their GUIDs.

**Block the add-in on documents with a given label** (the common ask —
"Claude must not run on our top-secret files"):

```json
{
  "effect": "deny",
  "action": "addin.access",
  "resource": {
    "type": "open_file",
    "identifiers": [{ "type": "mip_label_guid", "equals": "<guid>" }],
    "description": "Highly Confidential"
  }
}
```

**Refuse uploading files that carry a given label** ("users may not attach
restricted files"):

```json
{
  "effect": "deny",
  "action": "file.upload",
  "resource": {
    "type": "uploaded_file",
    "identifiers": [{ "type": "mip_label_guid", "equals": "<guid>" }],
    "description": "Confidential - Restricted"
  }
}
```

**Turn a feature off for everyone** (the `disabled_features` equivalent — no
`resource`, so it applies everywhere; here, no user may author skills):

```json
{ "effect": "deny", "action": "skills.authoring" }
```

**Allowlist — the add-in runs only on approved labels.** The first `allow`
written for an `(action, resource type)` flips that scope to default-deny:
only files matching an `allow`'s identifiers pass, and unlabeled files no
longer pass either. A matching `deny` still wins over a matching `allow`.

```json
{
  "effect": "allow",
  "action": "addin.access",
  "resource": {
    "type": "open_file",
    "identifiers": [
      { "type": "mip_label_guid", "equals": "<general-guid>" },
      { "type": "mip_label_guid", "equals": "<public-guid>" }
    ]
  }
}
```

Combine as needed — the value is one JSON array of statements:

```json
[
  { "effect": "deny", "action": "addin.access", "resource": { ... } },
  { "effect": "deny", "action": "file.upload", "resource": { ... } }
```

## 3. Rules to explain before they ship it

Tell the admin these five things before they ship; each is a common surprise.

**A statement does exactly what it says — nothing is implied.** Blocking the
add-in on a label (`addin.access` on `open_file`) does *not* also stop that
document from being uploaded into a *different* document, and vice versa. A
label blocked "in all its forms" is **two statements** — one on `open_file`,
one on `uploaded_file`. Statements, and the identifiers within each, OR
together.

**Parent labels have no GUID inside a file — only sublabels do.** A document
carries its sublabel's GUID (the row with a `ParentId`). To block a whole
parent group ("everything under *Confidential*"), either list each sublabel's
GUID, or match on the composed display name, which Office writes as
`"Parent - Sublabel"`:

```json
{ "type": "mip_label_name", "startsWith": "Confidential" }
```

**Name matching is exact and rename-hazardous.** `mip_label_name` compares the
label's display name character-for-character — case-sensitive, whitespace
included — as the labeling client wrote it, in that user's locale. `equals`,
`startsWith`, and `endsWith` are available. Prefer GUIDs; use names only for the
parent-group case above, and tell the admin a rename breaks the match.

**A label the add-in can't read fails closed.** When any statement targets
`uploaded_file`, an attachment whose label is unreadable — a Purview-*encrypted*
package, or legacy `.xls` / `.ppt` / `.doc` — is refused rather than let
through. If their sensitive labels apply encryption, that's the behavior they
want; if they must upload legacy formats, they'll need to convert them.

**"Only classified documents"** — to make the add-in refuse *unlabeled* files,
match on presence rather than a GUID:

```json
{ "type": "mip_label_guid", "exists": false }
```

On `uploaded_file` this also matches formats that can't carry a label at all
(images, CSV, plain text) — say so, so they aren't surprised when a screenshot
is refused.

## 4. Validate and hand off

Read the finished array back to the admin as a table (effect / action /
resource / identifiers) before generating anything. Then pass it to
[manifest](manifest.md#access_policies) as the `access_policies` key — the build
script checks it's a JSON array. Malformed statements aren't fatal on the
add-in side (they're skipped and reported), but validate now so the admin isn't
surprised by a rule that silently didn't apply.

`access_policies` is manifest / bootstrap only — it does **not** fit in Entra
extension attributes (256-char cap). If they use per-user
[bootstrap](bootstrap.md), the same array goes there as a native JSON value
rather than a string.
