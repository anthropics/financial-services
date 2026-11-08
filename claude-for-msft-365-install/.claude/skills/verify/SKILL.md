---
name: verify
description: Verify changes to the claude-for-msft-365-install admin scripts and commands by driving them against an isolated fake $HOME.
---

# Verifying claude-for-msft-365-install

This plugin is **admin CLI tooling**, not an app. There is nothing to build and
no server to boot. The surface is the terminal: `scripts/*.sh` on macOS,
`scripts/*.ps1` on Windows.

## Lint gate

```bash
python3 scripts/check.py           # from the REPO ROOT, not the plugin dir
bash -n claude-for-msft-365-install/scripts/<script>.sh
```

`check.py` lints every manifest and self-installs the pre-commit hook that
patch-bumps `.claude-plugin/plugin.json`. Run it before committing.

## Drive the scripts against a fake $HOME

Every macOS script resolves Office paths from `$HOME`, so overriding it gives a
throwaway sandbox — you can exercise the destructive `--apply` paths without
touching real Office data.

```bash
S=<scratchpad>/sandbox
for app in Excel Word Powerpoint; do
  mkdir -p "$S/Library/Containers/com.microsoft.$app/Data/Documents/wef"
done
printf '<x/>' > "$S/Library/Containers/com.microsoft.Excel/Data/Documents/wef/aaaaaaaa-1111-1111-1111-111111111111.manifest-a.xml"

HOME=$S ./scripts/clear-addin-cache.sh                      # list
HOME=$S ./scripts/clear-addin-cache.sh --id <GUID>          # dry-run
HOME=$S ./scripts/clear-addin-cache.sh --id <GUID> --apply  # destructive
```

Seed at least **two IDs across two apps**, with **mixed upper/lowercase**. Both
properties have caught real bugs: cross-app blast radius, and a case-sensitive
glob that reported "already clear" and sent admins to a folder-wide wipe.

## Prove storage is retained

The load-bearing claim of this plugin is that clearing a manifest never touches
the user's chat history. Verify it by snapshot-diffing both trees around the
operation, against the **real** `$HOME`:

```bash
snap() {
  for app in Excel Word Powerpoint; do
    find "$HOME/Library/Containers/com.microsoft.$app/Data/Library/WebKit/WebsiteData" \
         -type f -exec stat -f '%N %z %m' {} \; 2>/dev/null
    find "$HOME/Library/Containers/com.microsoft.$app/Data/Documents/wef" \
         -type f -exec stat -f 'WEF %N %z' {} \; 2>/dev/null
  done | sort
}
snap > before.txt;  <run the script>;  snap > after.txt;  diff before.txt after.txt
```

Manifests live in `Data/Documents/wef`; storage lives in
`Data/Library/WebKit/WebsiteData`. Different subtrees — the diff should show
only the manifest you removed. **Restore any planted files and re-diff to
confirm you left the machine as you found it.**

## Gotchas

- **The Bash tool runs zsh.** Scripts are `#!/usr/bin/env bash`; test bash-only
  behaviour (`shopt`, glob semantics) inside `bash <<'EOF' … EOF`, not inline.
- **`PRAGMA integrity_check` and `SELECT count(*)` fail on exported IndexedDB
  files** with `no such collation sequence: IDBKEY`. That is WebKit's custom
  collation, not corruption — it fails on the source file too. Verify
  completeness with `SELECT sum(length(value)) FROM Records;` on both sides.
- **Never claim the `.ps1` scripts work without running them on Windows.**
  macOS has no PowerShell, so a `.ps1` change verified only here is unverified.
  Run it on a real Windows host against Windows PowerShell 5.1, and always
  include a **parse check** before the behavioural ones:

  ```powershell
  $e = $null
  [System.Management.Automation.PSParser]::Tokenize(
    (Get-Content -Raw .\clear-addin-cache.ps1), [ref]$e) | Out-Null
  if ($e.Count) { $e | ForEach-Object { $_.Message } } else { 'parse ok' }
  ```

  A file can be perfectly fine on macOS and fail to parse outright on Windows
  (see the ASCII note below), so parsing is the first thing to establish.

- **`.ps1` files must be pure ASCII** (enforced by `scripts/check.py`).
  Windows PowerShell 5.1 reads a BOM-less `.ps1` as ANSI, so an em dash decodes
  to mojibake containing `"`, which terminates a string and breaks the parse.
  `clear-addin-cache.ps1` shipped broken this way and no macOS check caught it.
- Probe the arg parser. `--flag` as the final argument makes `shift 2` fail
  under `set -e` and exits 1 with **no output**; each flag needs a
  `[ $# -ge 2 ]` guard.
