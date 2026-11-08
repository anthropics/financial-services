<#
.SYNOPSIS
  Remove a sideloaded Office add-in's dev registration on Windows.

.DESCRIPTION
  On Windows, sideloaded (developer) add-ins are NOT files in a Wef folder --
  office-addin-dev-settings registers them as registry values under
  HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer. Each value's name is
  either the add-in <Id> or the manifest path; its data is the manifest path.
  Per-add-in settings live in a subkey Developer\<Id>.

  This removes ONLY the registration(s) matching one add-in ID (the Developer
  value whose name == ID or whose manifest data has that <Id>, plus the
  Developer\<Id> settings subkey). Other add-ins are untouched.

  NOTE: This targets the developer/sideload registry -- the analog of the
  macOS Documents/wef files. It does NOT touch the centrally-deployed
  manifest cache (%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\<guid>\...),
  which Microsoft says must be cleared as a whole folder, never per-file
  ("deleting individual manifest files can stop all add-ins from loading").

  That restraint is also what protects the user's data. This script only ever
  writes to HKCU -- it touches no file on disk. The add-in's chat history,
  skills, MCP registrations and memory live UNDER that same Wef folder
  (%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\webview2\...), so the widely
  circulated "just delete the Wef folder" fix destroys them. Run
  export-addin-data.ps1 before anyone does that.

.EXAMPLE
  clear-addin-cache.ps1                       # list every sideloaded add-in, do nothing
  clear-addin-cache.ps1 -Id <GUID>            # dry-run: show what would be removed
  clear-addin-cache.ps1 -Manifest C:\m.xml    # dry-run, read <Id> from the manifest
  clear-addin-cache.ps1 -Id <GUID> -Apply     # actually remove the registration
#>
[CmdletBinding()]
param(
  [string]$Id,
  [string]$Manifest,
  [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$devKey = 'HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer'

if (-not (Test-Path $devKey)) {
  Write-Host "No developer key at $devKey -- nothing is sideloaded on Windows."
  # Asked to clear a specific ID and there was nothing to clear it from: same
  # miss-reads-as-success shape guarded below, so use the same exit code. With
  # no -Id this is just an empty listing, which is a legitimate 0.
  if ($Id -or $Manifest) {
    Write-Host "`nNOT cleared. If the add-in was deployed centrally rather than"
    Write-Host "sideloaded, this script is not the tool -- see the debug command."
    exit 1
  }
  return
}

function Get-Registrations {
  $props = Get-ItemProperty -Path $devKey
  $props.PSObject.Properties |
    Where-Object { $_.Name -notmatch '^PS' -and $_.Name -ne 'RefreshAddins' } |
    ForEach-Object { [pscustomobject]@{ Name = $_.Name; Data = $_.Value } }
}

# Resolve the add-in <Id> from a manifest if -Id wasn't given.
if (-not $Id -and $Manifest) {
  if (-not (Test-Path $Manifest)) { throw "manifest not found: $Manifest" }
  $Id = ([xml](Get-Content $Manifest)).OfficeApp.Id
}

# No ID at all -> list what's registered and exit (no deletion).
if (-not $Id) {
  Write-Host "Sideloaded add-ins registered under Developer (name  ->  manifest):"
  $regs = Get-Registrations
  if (-not $regs) { Write-Host "  (none)" }
  foreach ($r in $regs) {
    $guid = ''
    if (Test-Path $r.Data) { try { $guid = ([xml](Get-Content $r.Data)).OfficeApp.Id } catch {} }
    "  {0}  ->  {1}{2}" -f $r.Name, $r.Data, $(if ($guid) { "  [<Id> $guid]" } else { '' })
  }
  Write-Host "`nRe-run with -Id <GUID> (or -Manifest <path>) to remove one (add -Apply to delete)."
  return
}

# $Id becomes part of a registry path below, and Remove-Item -Path expands
# wildcards: an -Id of '*' would resolve to every Developer\<Id> subkey rather
# than one. Require a real GUID so the blast radius stays at a single add-in.
if ($Id -notmatch '^\{?[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\}?$') {
  throw "not a GUID: '$Id'. Pass the add-in <Id>, e.g. -Id 12345678-1234-1234-1234-123456789abc"
}

# Match a Developer value whose name IS the ID, or whose manifest data has that <Id>.
$toRemove = @()
foreach ($r in (Get-Registrations)) {
  if ($r.Name -ieq $Id) { $toRemove += $r; continue }
  if (Test-Path $r.Data) {
    try { if ((([xml](Get-Content $r.Data)).OfficeApp.Id) -ieq $Id) { $toRemove += $r } } catch {}
  }
}
$settingsSubkey = Join-Path $devKey $Id
$hasSubkey = Test-Path -LiteralPath $settingsSubkey

if ($Apply) { Write-Host "Removing sideload registration for add-in $Id" }
else        { Write-Host "DRY RUN -- would remove (re-run with -Apply to delete):" }

if (-not $toRemove -and -not $hasSubkey) {
  # A miss is a dead end, not a success. Read as "already clear" it sends the
  # admin off to restart Office, still see the stale add-in, and reach for the
  # Wef folder wipe -- which takes the user's chat history with it.
  Write-Host "  (nothing registered for $Id)"
  Write-Host "`nNOT cleared. Either it was already removed, or the ID is wrong."
  Write-Host "Re-run with no arguments to list what is actually registered."
  exit 1
} else {
  foreach ($r in $toRemove) {
    # -Name is wildcard-matched, and a value name is often a manifest PATH
    # (see .DESCRIPTION). A path like C:\...\[archive]\manifest.xml would parse
    # as a character class, match nothing, and -Force would swallow the error --
    # printing "removed" for a registration that is still there.
    if ($Apply) { Remove-ItemProperty -Path $devKey -Name ([WildcardPattern]::Escape($r.Name)) -Force; Write-Host "  removed value: $($r.Name) -> $($r.Data)" }
    else        { Write-Host "  would remove value: $($r.Name) -> $($r.Data)" }
  }
  if ($hasSubkey) {
    if ($Apply) { Remove-Item -LiteralPath $settingsSubkey -Recurse -Force; Write-Host "  removed settings subkey: $settingsSubkey" }
    else        { Write-Host "  would remove settings subkey: $settingsSubkey" }
  }
}
Write-Host "Quit and reopen the Office apps so they re-read the registry."
