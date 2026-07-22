---
description: Export a copy of a user's add-in chat history, skills, MCP registrations, and settings before a machine is rebuilt
---

# Export add-in data

Chat history, uploaded skills, MCP registrations, memory, and settings live in browser
storage **on the user's own machine**. There is no server-side copy. These
scripts make a copy of it.

| Platform | Script |
|---|---|
| macOS | `scripts/export-addin-data.sh` |
| Windows | `scripts/export-addin-data.ps1` |

**Read only.** They read Office's storage and write only to the folder you
name. They never modify, move, or delete anything in Office. Run with no
arguments and they just print what they found.

```bash
./scripts/export-addin-data.sh                      # macOS: list
./scripts/export-addin-data.sh --out ~/claude-export
```
```powershell
.\scripts\export-addin-data.ps1                     # Windows: list
.\scripts\export-addin-data.ps1 -Out C:\claude-export
```

## Why reinstalling the add-in doesn't lose anything

The manifest is a **pointer, not a container**. It holds an `<Id>`, a
`<Version>`, and a `<SourceLocation>` URL — and no data. Office reads it,
then opens that URL in an embedded browser (WKWebView on macOS, WebView2 on
Windows). From there the ordinary web rules apply: that browser gives
IndexedDB to the page's **origin** — `scheme://host:port` — exactly as Chrome
or Safari would.

So the ID and the storage live on two different keys:

```
  manifest.xml                       the WebView                storage bucket
  ┌──────────────────────┐           ┌───────────────┐          ┌─────────────┐
  │ <Id>  3499c065-…     │──ignored─╳│               │          │             │
  │ <Version> 1.0.0.11   │──ignored─╳│  loads  URL   │──origin─▶│ IndexedDB   │
  │ <SourceLocation>     │──────────▶│               │          │  for that   │
  │   https://host/…     │           └───────────────┘          │   origin    │
  └──────────────────────┘                                      └─────────────┘
         ▲                                                             ▲
         │ replaced / deleted / re-ID'd / version-bumped               │
         └──── none of this reaches ───────────────────────────────────┘
```

Deleting a manifest is like deleting a bookmark: the site's cookies don't go
with it. Put a new manifest in place pointing at the same URL and the same
bucket is waiting — the ID it carries is irrelevant to the lookup.

You can see this directly: a pilot manifest and a production manifest with
**different `<Id>`s** that both point at `https://pivot.claude.ai` share one
store, because the origin is the same. The add-in ID appears nowhere in the
storage path.

So all of these keep the history in place, with nothing to do:

- replacing the manifest with a new one
- deleting the manifest, or uninstalling and reinstalling
- moving between a sideloaded manifest and the store listing
- a version bump, or a fresh `<Id>` to dodge the Admin Center cache

What **does** move the data is a change to the origin or to the profile
holding it:

| Change | Effect |
|---|---|
| Add-in served from a new host, or `https`→`http`, or a different port | New origin → new empty bucket. The old one still exists but nothing reads it. |
| Machine rebuilt, or the browser profile wiped | Gone; nothing is stored server-side. |
| Windows: Office signed into a different account | Different profile path → different bucket. Reversible — sign back in. |

## When you need this

Export when the machine or the storage location is about to change:

| Situation | Why |
|---|---|
| A PC or Mac is being rebuilt, reimaged, or handed to someone else | Nothing is stored server-side. |
| Clearing the Office add-in cache on **Windows** | The add-in's storage lives inside the `Wef` folder, so "delete the Wef folder" removes chat history too. On macOS these are separate trees and clearing the cache is harmless. |
| Roaming-profile / FSLogix cleanup, or Edge policies like `ClearBrowsingDataOnExit` | Wipes the browser profile the add-in stores into. |
| Old conversations matter | History keeps the 50 most recent chats per app, and drops the oldest automatically when storage runs low. |

## What is in the export

A plain folder tree, grouped by Office app (macOS) or signed-in account
(Windows), then by website:

```
claude-export/
└── Excel/                            macOS groups by app — each Office app has
    ├── pivot.claude.ai/              its own sandbox, so each keeps separate history
    │   ├── claude-chat-history/
    │   ├── claude-local-skills/
    │   ├── claude-mcp-gateways/
    │   ├── claude-memory/
    │   └── local-storage/            settings, inference config, onboarding + terms
    └── addins.contoso.com_8443/      a non-default port is kept in the name:
        └── …                         :8443 is a different origin, so a different store
```

Windows groups by signed-in Office account instead of by app, and its
localStorage is one store shared by every origin on that profile, so it is
copied whole and sits beside the origin folders:

```
claude-export\
└── <guid>_ADAL__2\                    the Office account (see "Putting data back")
    ├── pivot.claude.ai\
    │   └── https_pivot.claude.ai_0.indexeddb.leveldb\
    ├── addins.contoso.com_8443\
    └── Local Storage\                 ⚠ whole profile store — ALL origins, not
        └── leveldb\                     just Claude's. Chromium cannot split it.
```

That last folder is the one exception to "only Claude's data". localStorage —
settings, the inference config, the onboarding and terms-accepted flags — is a
single LevelDB per profile shared by every origin, so it cannot be filtered
down to one add-in. It is copied whole rather than dropped, and its size is
printed on every run, including the argument-less preview. If that is
unacceptable under your data policy, delete `Local Storage` from the export;
everything else is Claude-only. On macOS localStorage *is* per-origin, so there
it appears as a `local-storage/` folder inside each origin with nothing extra.

Both layouts are **relabelled for readability, not a path mirror** — the real
locations are nested under salted hashes (macOS) or `…\2\[n]\EBWebView\Default\`
(Windows). Copying the export back over those paths will not work; see
[Putting data back](#putting-data-back).

Sign-in tokens are deliberately **not** included — a rebuilt machine signs in
again, which is the safer default. The export **does** contain conversation
text, and on Windows the `Local Storage` folder carries other add-ins' settings
too; handle it under the same policy as any other copy of that content.

### Checking an export is complete

On macOS the stores are SQLite, so compare the copy against the original:

```bash
sqlite3 <path>/IndexedDB.sqlite3 'SELECT sum(length(value)) FROM Records;'
```

Matching totals means the copy is whole. Note that `PRAGMA integrity_check`
and `SELECT count(*)` both fail with **`no such collation sequence: IDBKEY`**
— WebKit registers that collation at runtime and the `sqlite3` CLI has no way
to. That error says nothing about the copy; it appears on the *original* file
too. Don't read it as corruption.

## Putting data back

The scripts do not do this, on purpose. Writing into Office's storage risks
damaging a working setup, and the right move depends on why the data went
missing. Keep the export and raise it with Anthropic support — the folder is
everything needed to recover.

One case worth checking first, because it needs no recovery at all: on
Windows the storage path includes the **signed-in Office account** —

```
%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\webview2\<account>\2\[n]\EBWebView\
```

A GUID ending `_ADAL` is a work or school account; one ending `_LiveId` is a
personal Microsoft account. If Office is signed into a different account than
the one the chats were created under, the add-in reads a different folder and
the history looks gone. **Signing back into the original account brings it
back on its own — no copying needed.** Run the export script with no arguments
to see which account folders exist on the machine; it labels each one.

## Where the data lives

Point a skeptical admin at the folder — it is plain and readable without
running anything. Both scripts print these paths in their `--help` /
`Get-Help` output too.

**Windows** — paste into File Explorer:

```
%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\webview2
```

Then `<account>\2\[n]\EBWebView\Default\IndexedDB\`, where folders are named
after the origin, e.g. `https_pivot.claude.ai_0.indexeddb.leveldb`.

**macOS** — per-app sandbox container, so each app has its own history:

```
~/Library/Containers/com.microsoft.Excel/Data/Library/WebKit/WebsiteData/Default
```

Each subfolder is one origin, named with a salted hash — read the plaintext
`origin` file inside to see which. Chat history is
`IndexedDB/<uppercase SHA-256 of "claude-chat-history">`; check that hash with
`printf 'claude-chat-history' | shasum -a 256`.
