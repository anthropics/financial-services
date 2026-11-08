<#
.SYNOPSIS
  Export a copy of the Claude Office add-in's local data on Windows -- chat
  history, uploaded skills, MCP registrations, memory, and settings.

.DESCRIPTION
  READ ONLY. This script never writes to, moves, or deletes anything in
  Office. It reads the add-in's storage and copies it to a folder you name.
  Run it with no arguments and it only prints what it found.

  IndexedDB (chat history, skills, MCP registrations, memory) is per-origin,
  so only Claude's stores are copied -- other add-ins' stores are detected and
  skipped, and the script reports how many it ignored.

  localStorage (settings, inference config, onboarding + terms flags) is NOT
  per-origin: Chromium keeps one LevelDB per profile shared by every origin.
  It cannot be split, so it is copied WHOLE, once per Office account, and that
  copy therefore also contains other add-ins' and other sites' settings. The
  run prints its size, in list mode too, so this is never a surprise. If that
  is unacceptable for your data policy, delete the "Local Storage" folder from
  the export -- everything else is Claude-only.

  SEE IT YOURSELF -- you do not need this script to look
    The data is a plain, unencrypted folder. Paste into File Explorer:

      %LOCALAPPDATA%\Microsoft\Office\16.0\Wef\webview2

    Or list every store, read-only:

      Get-ChildItem -Recurse -Depth 8 -Directory `
        "$env:LOCALAPPDATA\Microsoft\Office\16.0\Wef\webview2" |
        Where-Object Name -like 'https_*.indexeddb.*' |
        Select-Object -Expand FullName

    Folders are named after the website that owns them, e.g.
    https_pivot.claude.ai_0.indexeddb.leveldb. The trailing _0 is the port.

  NOTES
    * The path includes the signed-in Office account:
      webview2\<account>\2\[n]\EBWebView\... . A GUID ending _ADAL is a
      work or school account; one ending _LiveId is a personal Microsoft
      account. Signing Office into a different account means a different
      folder -- so if history looks missing, check the account before
      anything else. This exports every folder found and labels each one.
    * On Windows the add-in's storage lives INSIDE the Wef folder, so the
      commonly circulated "delete %LOCALAPPDATA%\Microsoft\Office\16.0\Wef"
      fix deletes chat history along with the manifest cache. Export first.
    * Sign-in tokens are deliberately NOT exported. The export does contain
      conversation text -- handle it under your normal data policy.
    * You do NOT need this to change add-ins. Storage is keyed by the origin
      the add-in is served from, not by add-in ID, so replacing the manifest,
      reinstalling, or moving to the store listing leaves the data in place.
      Export before a machine is rebuilt or wiped.

.EXAMPLE
  export-addin-data.ps1                  # list what is on this PC, copy nothing
  export-addin-data.ps1 -Out C:\claude-export
#>
[CmdletBinding()]
param(
  [string]$Out,
  # Export every IndexedDB store, skipping the "is this Claude's?" check. Use
  # when the add-in has clearly been used but its store is not recognised --
  # LevelDB compaction can hide the database names from a plaintext search.
  [switch]$IncludeAll
)

$ErrorActionPreference = 'Stop'
$wef = Join-Path $env:LOCALAPPDATA 'Microsoft\Office\16.0\Wef\webview2'

if (-not (Test-Path $wef)) {
  Write-Host "No add-in storage at $wef -- the add-in has not run on this PC."
  return
}

# Unlike SQLite on macOS, LevelDB has no consistent online snapshot. Copying
# while Office is open can catch a store mid-write -- that only affects the
# fidelity of the COPY, never the original, so warn instead of blocking.
$live = Get-Process EXCEL, WINWORD, POWERPNT, OUTLOOK -ErrorAction SilentlyContinue
if ($Out -and $live) {
  Write-Warning ("Office is open (" + (($live | Select-Object -Expand Name | Sort-Object -Unique) -join ', ') +
                 "). Close it for a clean copy. Your existing data is not affected either way.")
}

# "https_pivot.claude.ai_0.indexeddb.leveldb" -> "pivot.claude.ai"
# Chromium names each store <scheme>_<host>_<port>.indexeddb.leveldb, using 0
# for the scheme's default port. Keep a non-default port in the label: storage
# is per-origin and an origin includes the port, so https://addins.contoso.com
# and https://addins.contoso.com:8443 are genuinely separate stores and must
# not read as one.
function Get-OriginHost([string]$name) {
  if ($name -match '^https?_(.+?)_(\d+)\.indexeddb\.(leveldb|blob)$') {
    if ($Matches[2] -in '0', '443') { return $Matches[1] }
    return "$($Matches[1]):$($Matches[2])"
  }
  return $null
}

# ...\<account>\2\[n]\EBWebView -> "<account>__2[__n]", a readable label.
function Get-AccountLabel([string]$ebWebViewPath) {
  $rel = $ebWebViewPath.Substring($wef.Length).Trim('\')
  return ($rel -replace '\\EBWebView.*$', '') -replace '\\', '__'
}

function Get-AccountKind([string]$label) {
  if ($label -match '_ADAL')   { return 'work or school account' }
  if ($label -match '_LiveId') { return 'personal Microsoft account' }
  return 'not signed in'
}

# Only export stores that actually belong to the Claude add-in.
#
# Office keeps one store per website, and other add-ins -- Microsoft's own
# included -- get their own stores in the same folder. A LevelDB store packs
# every database for its website into one set of files, so we cannot copy
# just our databases out of a store; what we CAN do is skip any store that
# is not ours. This checks whether our database names appear in the bytes,
# which works whatever host the add-in is served from (production, a
# government cloud, or a customer-specific deployment).
$claudeDbs = @('claude-chat-history', 'claude-local-skills', 'claude-mcp-gateways',
               'claude-memory', 'claude-office-snipped-results')
# Search the raw bytes. Decoding as ASCII is a byte search for our purposes:
# the names are pure ASCII so those bytes round-trip exactly, the NUL bytes of
# the UTF-16LE form round-trip too, and any byte above 127 becomes '?' which
# cannot accidentally spell a database name. ASCII is built into every .NET,
# unlike the code-page encodings, so this works on Windows PowerShell 5.1 and
# PowerShell 7 alike.
$ascii = [System.Text.Encoding]::ASCII
$needles = foreach ($db in $claudeDbs) {
  $db                                                              # written as ASCII
  $ascii.GetString([System.Text.Encoding]::Unicode.GetBytes($db))  # written as UTF-16LE
}

# Read in chunks rather than slurping whole files: a heavy user's store can be
# hundreds of MB, and skipping big files would silently drop exactly the
# largest history from the export. The overlap keeps a name that straddles a
# chunk boundary from being missed.
function Test-IsClaudeStore([string]$dir) {
  $chunk = 4MB
  $overlap = 256          # comfortably longer than any name, in UTF-16 bytes
  # Order matters for speed AND for hit rate. LevelDB keeps recent writes in the
  # uncompressed write-ahead log and MANIFEST; only compacted .ldb blocks are
  # Snappy-compressed, where a plaintext name may not appear at all. Read the
  # cheap uncompressed files first, smallest to largest, so the common case
  # answers in milliseconds instead of scanning hundreds of MB per store.
  $files = Get-ChildItem -File $dir -ErrorAction SilentlyContinue |
    Sort-Object @{ Expression = { if ($_.Extension -eq '.ldb') { 1 } else { 0 } } }, Length
  foreach ($f in $files) {
    if ($f.Length -eq 0) { continue }
    $fs = [System.IO.File]::OpenRead($f.FullName)
    try {
      $buf = New-Object byte[] $chunk
      $carry = ''
      while (($read = $fs.Read($buf, 0, $chunk)) -gt 0) {
        $hay = $carry + $ascii.GetString($buf, 0, $read)
        foreach ($n in $needles) { if ($hay.Contains($n)) { return $true } }
        $carry = if ($hay.Length -gt $overlap) { $hay.Substring($hay.Length - $overlap) } else { $hay }
      }
    } finally { $fs.Dispose() }
  }
  return $false
}

$allStores = Get-ChildItem -Directory -Recurse -Depth 8 $wef -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -like 'https_*.indexeddb.leveldb' }

$stores = @($allStores | Where-Object { $IncludeAll -or (Test-IsClaudeStore $_.FullName) })
$skipped = @($allStores).Count - $stores.Count

if (-not $stores) {
  Write-Host "No Claude add-in storage found under $wef."
  if ($skipped) {
    # Detection is a plaintext search, and LevelDB compaction can Snappy-compress
    # the database names out of reach. So "none matched" is not proof of absence
    # when stores DO exist -- name them and let the admin decide.
    Write-Host "`n$skipped IndexedDB store(s) are present but were not recognised as Claude's:"
    foreach ($s in $allStores) { Write-Host ("    {0}" -f $s.Name) }
    Write-Host "`nIf one of those is the add-in, re-run with -IncludeAll to export them all."
    Write-Host "(-IncludeAll also copies other add-ins' data -- handle it accordingly.)"
    exit 1
  }
  # Asked to export and exported nothing: never let that read as success, or
  # `export -Out ... ; wipe` treats an empty backup as a green light.
  if ($Out) {
    Write-Host "`nNOTHING WAS EXPORTED to $Out. Do not wipe anything based on this run."
    Write-Host "Check that Office is signed into the expected account, then re-run."
    exit 1
  }
  return
}

if ($Out) { Write-Host "Exporting to $Out" }
else      { Write-Host "Claude add-in data on this PC (pass -Out <dir> to copy it):" }
if ($skipped) { Write-Host "Ignoring $skipped store(s) belonging to other add-ins." }
Write-Host ""

$n = 0
foreach ($store in $stores) {
  $originHost = Get-OriginHost $store.Name
  if (-not $originHost) { continue }

  # ...\EBWebView\Default\IndexedDB\<store> -> ...\EBWebView
  $ebWebView = Split-Path (Split-Path (Split-Path $store.FullName -Parent) -Parent) -Parent
  $acct = Get-AccountLabel $ebWebView

  # NB: .BaseName is NOT extension-stripped for a directory -- swap the
  # suffix explicitly or the attachment folder is missed.
  $blob = Join-Path $store.Parent.FullName ($store.Name -replace '\.leveldb$', '.blob')
  $hasBlob = Test-Path $blob

  $size = (Get-ChildItem -Recurse -File $store.FullName | Measure-Object Length -Sum).Sum
  Write-Host ("https://{0}   [{1}]" -f $originHost, (Get-AccountKind $acct))
  Write-Host ("    data         {0,10:N0} bytes" -f $size)
  if ($hasBlob) {
    $bs = (Get-ChildItem -Recurse -File $blob | Measure-Object Length -Sum).Sum
    Write-Host ("    attachments  {0,10:N0} bytes" -f $bs)
  }

  if ($Out) {
    # ':' is illegal in a Windows path, so a ported origin becomes host_port.
    $dest = Join-Path (Join-Path $Out $acct) ($originHost -replace ':', '_')
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    # Copy-Item -Recurse into an EXISTING directory nests it (dest\store\store)
    # rather than refreshing it, so a re-run would hide the good copy one level
    # down and leave the first, possibly torn, copy on top. Clear it first.
    foreach ($leaf in @($store.Name) + @(if ($hasBlob) { Split-Path $blob -Leaf })) {
      $target = Join-Path $dest $leaf
      if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
    }
    Copy-Item -Recurse -Force -LiteralPath $store.FullName -Destination (Join-Path $dest $store.Name)
    if ($hasBlob) { Copy-Item -Recurse -Force -LiteralPath $blob -Destination (Join-Path $dest (Split-Path $blob -Leaf)) }
    $n++
    Write-Host "    -> $dest"
  }
  Write-Host ""
}

# --- localStorage: one shared LevelDB per PROFILE, not per origin ------------
# Settings, the inference/customer config, and the onboarding + terms flags all
# live here rather than in IndexedDB. Chromium gives every origin on a profile
# the same store, so it cannot be split per add-in -- it is copied whole.
#
# Driven off the profile list rather than the store loop: a profile whose only
# store fails the origin-name parse would otherwise lose its settings silently.
$lsFailed = 0
$profiles = $stores |
  ForEach-Object { Split-Path (Split-Path (Split-Path $_.FullName -Parent) -Parent) -Parent } |
  Select-Object -Unique

foreach ($prof in $profiles) {
  $ls = Join-Path $prof 'Default\Local Storage'
  if (-not (Test-Path -LiteralPath $ls)) { continue }
  $acct = Get-AccountLabel $prof
  $lsSize = (Get-ChildItem -Recurse -File $ls -ErrorAction SilentlyContinue |
             Measure-Object Length -Sum).Sum
  Write-Host ("local storage  [{0}]  {1:N0} bytes  -- WHOLE profile store, all origins" -f (Get-AccountKind $acct), $lsSize)

  if ($Out) {
    $lsDest = Join-Path (Join-Path $Out $acct) 'Local Storage'
    $tmp = "$lsDest.partial"
    # Copy to a scratch name and swap only on success. Deleting the old copy
    # first would mean a locked LOCK file (Office still running) leaves the
    # export with neither the new copy nor the previous good one.
    try {
      if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
      New-Item -ItemType Directory -Force -Path (Split-Path $lsDest -Parent) | Out-Null
      Copy-Item -Recurse -Force -LiteralPath $ls -Destination $tmp
      if (Test-Path -LiteralPath $lsDest) { Remove-Item -LiteralPath $lsDest -Recurse -Force }
      Rename-Item -LiteralPath $tmp -NewName 'Local Storage'
      Write-Host "    -> $lsDest"
    } catch {
      $lsFailed++
      Write-Host "    !! could not copy Local Storage for $acct -- skipped ($($_.Exception.Message))"
      if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue }
    }
  }
  Write-Host ""
}

if ($Out) {
  # $n can still be 0 here if every store's folder name failed to parse, so
  # check the count rather than assuming the loop above copied something.
  if ($n -eq 0) {
    Write-Host "NOTHING WAS EXPORTED to $Out. Do not wipe anything based on this run."
    exit 1
  }
  Write-Host "Done. $n location(s) exported to $Out"
  Write-Host "Nothing in Office was modified."
  if ($lsFailed) {
    Write-Host ""
    Write-Host "WARNING: Local Storage for $lsFailed profile(s) could not be copied --"
    Write-Host "settings are MISSING from this export. Close Office and re-run."
    exit 1
  }
}
