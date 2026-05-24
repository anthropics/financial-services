<#
.SYNOPSIS
  Remove a sideloaded Office add-in's dev registration on Windows.

.DESCRIPTION
  On Windows, sideloaded (developer) add-ins are NOT files in a Wef folder —
  office-addin-dev-settings registers them as registry values under
  HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer. Each value's name is
  either the add-in <Id> or the manifest path; its data is the manifest path.
  Per-add-in settings live in a subkey Developer\<Id>.

  This removes ONLY the registration(s) matching one add-in ID (the Developer
  value whose name == ID or whose manifest data has that <Id>, plus the
  Developer\<Id> settings subkey). Other add-ins are untouched.

  NOTE: This targets the developer/sideload registry — the analog of the
  macOS Documents/wef files. It does NOT touch the centrally-deployed
  manifest cache (%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\<guid>\...),
  which Microsoft says must be cleared as a whole folder, never per-file
  ("deleting individual manifest files can stop all add-ins from loading").

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
  Write-Host "No developer key at $devKey — nothing is sideloaded on Windows."
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

# Match a Developer value whose name IS the ID, or whose manifest data has that <Id>.
$toRemove = @()
foreach ($r in (Get-Registrations)) {
  if ($r.Name -ieq $Id) { $toRemove += $r; continue }
  if (Test-Path $r.Data) {
    try { if ((([xml](Get-Content $r.Data)).OfficeApp.Id) -ieq $Id) { $toRemove += $r } } catch {}
  }
}
$settingsSubkey = Join-Path $devKey $Id
$hasSubkey = Test-Path $settingsSubkey

if ($Apply) { Write-Host "Removing sideload registration for add-in $Id" }
else        { Write-Host "DRY RUN — would remove (re-run with -Apply to delete):" }

if (-not $toRemove -and -not $hasSubkey) {
  Write-Host "  (nothing registered for $Id — already clear)"
} else {
  foreach ($r in $toRemove) {
    if ($Apply) { Remove-ItemProperty -Path $devKey -Name $r.Name -Force; Write-Host "  removed value: $($r.Name) -> $($r.Data)" }
    else        { Write-Host "  would remove value: $($r.Name) -> $($r.Data)" }
  }
  if ($hasSubkey) {
    if ($Apply) { Remove-Item -Path $settingsSubkey -Recurse -Force; Write-Host "  removed settings subkey: $settingsSubkey" }
    else        { Write-Host "  would remove settings subkey: $settingsSubkey" }
  }
}
Write-Host "Quit and reopen the Office apps so they re-read the registry."
