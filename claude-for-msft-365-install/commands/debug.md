---
description: Diagnose deployment issues (stale config, connect failures, missing add-in)
---

# Debug a Claude Office deployment

You are helping an enterprise admin diagnose why the deployed add-in isn't
working right. Start by asking **what's wrong**, then route.

## Triage

Ask the admin to describe the symptom. Route by answer:

| Symptom | Section |
|---|---|
| Updated the manifest but users still see old config | [Stale config after update](#stale-config-after-update) |
| Add-in shows "Connection failed" | [Read the error paste](#read-the-error-paste) |
| Add-in doesn't appear in Excel/PowerPoint at all | [Add-in not visible](#add-in-not-visible) |
| Want to test/iterate a manifest locally before deploying | [Sideload a manifest for local debugging](#sideload-a-manifest-for-local-debugging) |
| Sign-in popup fails or loops | [Admin consent](#admin-consent) |
| Need to see the browser console | [Opening browser devtools](#opening-browser-devtools-on-the-add-in) |

If they have an error paste from the add-in (the **Copy error details** button
on the connect-failed screen), always start there. It carries everything.

---

## Read the error paste

Paste structure:

```
Claude for Office connection failed (<Provider>)
Build: <sha>

<friendly message>

Request:
  <key>: <value actually sent>
  ...

Manifest params:
  <key>: <value the deployed manifest carries>
  ...

Raw error:
<SDK/HTTP error>
```

**What to check:**

- `Request:` vs `Manifest params:` delta. Keys are the same snake_case names
  in both blocks, so diff directly. If they differ, the user typed override
  values into the form. If they match, the manifest values went through
  unchanged.
- `Manifest params:` `m` key is the version tag (e.g. `unified-1.0.0.11`). If
  it's below what you last uploaded, the user is on a stale manifest. Go to
  [Stale config](#stale-config-after-update).
- `Raw error:` is the ground truth. Common patterns:
  - `invalid_client` (401, Google) → wrong `google_client_secret` for that
    `google_client_id`. Verify in GCP Console → Credentials.
  - `Load failed (<host>)` → network blocked at the WebView layer. Firewall
    needs to allow that host.
  - `STS AssumeRoleWithWebIdentity failed` → AWS IAM OIDC provider
    misconfigured or role trust policy wrong.
  - `HTTP 401/403` (gateway) → bad token or gateway rejected the key.

---

## Stale config after update

Two caches, two clocks:

| Layer | Who holds it | TTL | How to clear |
|---|---|---|---|
| Service | M365 Admin Center → Exchange Online → client | Up to **72h** for updates (24h for fresh deploys) | Wait, or redeploy with a fresh `<Id>` |
| Client | Office app's Wef folder on each machine | Until app restart, sometimes longer | Clear the cached manifests (see below) |

Microsoft's own FAQ:
> It can take up to 72 hours for add-in updates, changes from turn on or turn off to reflect for users.
> https://learn.microsoft.com/en-us/microsoft-365/admin/manage/centralized-deployment-faq

### Confirm what Admin Center is serving

Admin Center silently ignores re-uploads with the same `<Version>`. If you
uploaded a fix without bumping the fourth segment, it never took. Open M365
Admin Center → Integrated apps → your add-in → check the listed version.

### Force a client-side refresh

A stale **sideloaded** manifest is stored differently per platform:

- **macOS** — a file `<addin-id>.manifest-*.xml` in each app's
  `Documents/wef` folder, alongside every other add-in.
- **Windows** — a **registry** value under
  `HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer` (there is no
  per-add-in file to delete; clearing the `Wef` *folder* is a different,
  blunter operation — see the caveat below).

Use the helper scripts. They target **only** your add-in's `<Id>` and do
direct `rm`/registry edits — they do **not** shell out to
`office-addin-dev-settings` (its removal path has burned us on customer
calls):

- macOS: [`scripts/clear-addin-cache.sh`](../scripts/clear-addin-cache.sh)
- Windows: [`scripts/clear-addin-cache.ps1`](../scripts/clear-addin-cache.ps1)

Quit Excel/Word/PowerPoint first. The scripts are **ID-first** — pass the
add-in `<Id>` directly (handy when iterating across new/multiple IDs); the
manifest path is an optional convenience that just reads `<Id>` for you.

```bash
# macOS — list everything, do nothing:
./scripts/clear-addin-cache.sh

# Dry-run by ID (preferred), or via the manifest:
./scripts/clear-addin-cache.sh --id <GUID>
./scripts/clear-addin-cache.sh ~/path/to/manifest.xml

# Actually remove (only this ID's files):
./scripts/clear-addin-cache.sh --id <GUID> --apply
```

```powershell
# Windows — same flow, registry-scoped:
.\scripts\clear-addin-cache.ps1                  # list, do nothing
.\scripts\clear-addin-cache.ps1 -Id <GUID>       # dry-run
.\scripts\clear-addin-cache.ps1 -Id <GUID> -Apply
```

Both **dry-run by default** — nothing is removed without `--apply` /
`-Apply`. No-args lists every registered add-in so you confirm the ID
first. Other add-ins are never affected.

**You must fully restart the Office app after clearing.** Removing the
file/registry entry does nothing until the app re-reads it on launch — and
a *backgrounded* app counts as still running. Quit **and reopen** Excel /
Word / PowerPoint, confirming no lingering process first:
`pkill -f "Microsoft Excel"` (macOS) / check Task Manager (Windows). The
script also prints this reminder when it finishes.

**Deleting local/sideloaded manifests by ID is safe and works.** In
practice, removing just the one add-in's file (macOS) or registry value
(Windows) cleanly drops that add-in and leaves the rest loading normally —
we do this routinely. Microsoft's "don't delete individual files" warning
is about a *different* cache (below), not these local dev/sideload entries;
don't let it scare you off the surgical path here.

> **Centrally-deployed (Admin Center) staleness on Windows** is a
> *different* cache: `%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\<guid>\…`,
> stored under opaque hashes, **not** by add-in ID. Microsoft's official
> guidance is conservative — clear that folder's contents as a whole
> because *"deleting individual manifest files can cause all add-ins to
> stop loading."* In practice targeted deletion there can work too, but
> the filenames aren't ID-mapped so it's hard to be surgical — which is
> why these scripts deliberately do **not** touch it. If a
> centrally-deployed update is
> stale, prefer waiting out the service TTL or redeploying with a fresh
> `<Id>` (below) over hand-deleting that cache.

If it's still stale after the restart, the service-side cache hasn't caught
up. Wait, or use a fresh `<Id>` (below).

Microsoft's cache-clear doc: https://learn.microsoft.com/en-us/office/dev/add-ins/testing/clear-cache

### Nuclear option: redeploy with a fresh Id

If 72h is unacceptable, a fresh `<Id>` UUID forces Admin Center and every
client to treat it as a brand-new add-in (24h fresh-deploy SLA, usually much
faster). Edit `manifest.xml`, replace the text inside `<Id>` with a new UUID
(`uuidgen` on mac/linux, `[guid]::NewGuid()` in PowerShell), re-upload.

---

## Add-in not visible

- **Not in the ribbon:** Check M365 Admin Center → Integrated apps → your
  add-in → Users tab. Is the user (or their group) assigned? Nested groups
  aren't supported.
- **Shows "My Add-ins" but not the ribbon button:** The manifest's `<Hosts>`
  may not include this app. Check both `<Hosts>` lists (top-level and under
  `<VersionOverrides>`).
- **Fresh deploy, been <24h:** Normal. Microsoft's SLA is 24h for first-time
  deployment visibility.

---

## Sideload a manifest for local debugging

For iterating on a manifest **without going through Admin Center deployment**
(no 24–72h cache wait), point Office at a local manifest file directly. The
manifest stays wherever it is on disk; you just tell Office where to find it.
Pick the recipe for the customer's OS.

Use the helper scripts — they read the `<Id>` from the manifest and
install it the right way per platform (macOS: a `<Id>.manifest.xml` file in
each app's `Documents/wef`; Windows: a registry value under
`HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer` named by the `<Id>`).
Both do direct file/registry writes — **not** `office-addin-dev-settings`.

- macOS install: [`scripts/sideload-addin.sh`](../scripts/sideload-addin.sh)
- Windows install: [`scripts/sideload-addin.ps1`](../scripts/sideload-addin.ps1)
- Remove (either OS): `clear-addin-cache.{sh,ps1}` — see
  [Force a client-side refresh](#force-a-client-side-refresh)

```bash
# macOS — installs directly:
./scripts/sideload-addin.sh ~/path/to/manifest.xml
```

```powershell
# Windows — installs directly:
.\scripts\sideload-addin.ps1 C:\path\to\manifest.xml
```

Sideloading is additive and idempotent, so it installs directly — **no
dry-run** (unlike the destructive `clear-addin-cache`, which stays dry-run
by default). The install names the entry by the add-in `<Id>`, so removal
later is the exact inverse: `clear-addin-cache.{sh,ps1} --id <GUID>
--apply` (the sideload script prints the precise remove command on
completion).

Then **fully quit and reopen** Excel / Word / PowerPoint — check Task
Manager (Windows) / `pkill -f "Microsoft Excel"` (macOS) first; a
backgrounded app won't re-read the registry or rescan the folder. The
add-in appears under **Insert → My Add-ins** (Windows also shows it on the
**Home** tab / **Shared Folder** group); pin it.

**Notes (both platforms):**
- This is per-user and per-machine — it doesn't touch tenant deployment. It's
  purely for the customer to debug/iterate on their own box.
- A locally sideloaded manifest **wins over** a centrally deployed one with
  the same `<Id>`, so this is also a fast way to test a manifest fix before
  re-uploading to Admin Center.
- Pair this with [browser devtools](#opening-browser-devtools-on-the-add-in)
  to see console/network while iterating.
- If a stale copy keeps loading, also clear the cache — see
  [Force a client-side refresh](#force-a-client-side-refresh).

Microsoft's sideloading references:
- Windows: https://learn.microsoft.com/en-us/office/dev/add-ins/testing/create-a-network-shared-folder-catalog-for-task-pane-and-content-add-ins
- macOS: https://learn.microsoft.com/en-us/office/dev/add-ins/testing/sideload-an-office-add-in-on-mac

---

## Admin consent

If the user sees a sign-in popup that closes immediately or loops, the tenant
hasn't granted admin consent to the Claude app. Run
[`:consent`](consent.md) to generate the consent URL for a Global Admin to
approve. The symptom in error pastes: `user_canceled` in the raw error (the
broker maps any unclassifiable close to that).

---

## Silent SSO / Entra token failures

- **`AADSTS50194: …not configured as a multi-tenant application` /
  `Use a tenant-specific endpoint`** — your `graph_client_id` (or the
  `entra_scope` resource app) is a single-tenant app, and the add-in build is
  old enough to still request tokens against the `/common` authority. Newer
  builds resolve a tenant-specific authority automatically when
  `graph_client_id` is set. Fix: have users update to the latest add-in
  version. There is no manifest workaround on an old build.
- **`entra_scope requires graph_client_id`** — `entra_scope` was set without
  `graph_client_id`. Custom-scope access tokens must be issued by your own
  Entra app, not the default; set both. The build script also rejects this
  pairing.
- **Silent SSO fails, then an interactive popup works** — expected on first
  run before a service principal exists in the tenant. Once admin consent is
  granted (see above) the silent path succeeds.

---

## Opening browser devtools on the add-in

When you need the WebView's console — JS errors, network tab, the add-in's
debug logs — you have to attach the host OS's browser devtools. The add-in runs
in an embedded WebView with no address bar and no built-in F12, so each OS
has its own recipe.

### macOS (Safari Web Inspector)

Three gates. **Gate 3 is the one everyone misses.**

1. **Office developer extras** — quit the app first, then:
   ```bash
   defaults write com.microsoft.Excel OfficeWebAddinDeveloperExtras -bool true
   defaults write com.microsoft.Powerpoint OfficeWebAddinDeveloperExtras -bool true
   defaults write com.microsoft.Word OfficeWebAddinDeveloperExtras -bool true
   ```
   Makes right-click → **Inspect Element** appear inside the task pane.

2. **Safari Develop menu** — Safari → Settings → Advanced → check *Show
   features for web developers*.

3. **macOS Developer Tools allowlist** (Sonoma and later) — System Settings
   → Privacy & Security → Developer Tools → toggle **Terminal** on. Without
   this, Safari's Develop menu shows *"No Inspectable Applications"* even
   with gates 1 and 2 open.

With the task pane open, either right-click inside it → **Inspect Element**,
or go to Safari → Develop → *[your machine name]* → find the add-in host
(`pivot.claude.ai` in prod, your configured domain otherwise).

**Gotchas:**
- **Office updates silently reset gate 1.** If inspection worked last week
  and doesn't now, re-run the `defaults write`.
- *"No Inspectable Applications"* = gate 3 missing, or the Office app wasn't
  fully quit before `defaults write`. `pkill -f "Microsoft Excel"` then
  relaunch.
- The task pane has to be **open** (not just the app) for it to appear under
  Safari's Develop menu.

### Windows (Edge DevTools)

Depends on which WebView engine Office is using. Current M365 on Win10/11
with the WebView2 runtime gets Chromium; older perpetual Office or machines
without the runtime may still be on IE11/Trident.

**WebView2 (Chromium — the common case):**

Right-click inside the task pane → **Inspect**. That's it, no gates. If
right-click doesn't show Inspect, install **Microsoft Edge DevTools
Preview** from the Microsoft Store — it lists all attachable WebView2
targets including Office add-ins. Launch it, find the add-in's URL in the
target list, click to attach.

**IE11/Trident (legacy Office 2019/2021 perpetual):**

Run the IEChooser from an admin PowerShell:
```powershell
& "C:\Windows\SysWOW64\F12\IEChooser.exe"
```
Pick the add-in's page from the list. If the list is empty, the task pane
isn't open yet — open it first, then refresh IEChooser.

Microsoft's walkthrough: https://learn.microsoft.com/en-us/office/dev/add-ins/testing/debug-add-ins-using-devtools-edge-chromium
