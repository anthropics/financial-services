#!/usr/bin/env bash
# Clear a single Office add-in's cached / sideloaded manifest on macOS.
#
# The Wef cache holds every add-in side by side, each file named
# <addin-id>.manifest-*.xml. This removes ONLY the files matching one
# add-in ID across Excel/Word/PowerPoint -- it never wipes the folder.
#
# It does NOT touch the add-in's stored data. On macOS chat history, skills,
# MCP registrations and memory live in a different subtree entirely --
# Data/Library/WebKit/WebsiteData -- while manifests live in Data/Documents/wef.
# Clearing the manifest cannot reach the storage. (Windows is not so tidy: see
# the note in clear-addin-cache.ps1.)
#
# Usage:
#   clear-addin-cache.sh                       # list every add-in found, do nothing
#   clear-addin-cache.sh /path/to/manifest.xml # dry-run: show what would be removed
#   clear-addin-cache.sh --id <GUID>           # dry-run by ID (no manifest needed)
#   clear-addin-cache.sh /path/manifest.xml --apply   # actually delete
set -euo pipefail

# Office writes the wef filename using whatever casing the manifest's <Id> had,
# so a lowercase GUID from the admin will not match an uppercase file on disk.
# Without this the script reports "already clear" and the admin escalates to a
# folder-wide wipe. Characters that arrive from a quoted expansion (i.e. the ID
# itself) still stay literal, so `--id '*'` remains inert.
shopt -s nocaseglob

# Outlook included: it has its own container and its own wef folder. Scanning
# only three apps would report "NOT cleared" for a correct ID that simply lives
# in the fourth -- the exact wrong-turn that sends admins to a folder-wide wipe.
APPS=(Excel Word Powerpoint Outlook)
wef_dir() { echo "$HOME/Library/Containers/com.microsoft.$1/Data/Documents/wef"; }

MANIFEST="" ADDIN_ID="" APPLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    # Guard the value: a bare `--id` would otherwise make `shift 2` fail under
    # `set -e` and exit 1 with no output at all.
    --id) [ $# -ge 2 ] || { echo "ERROR: --id requires a GUID" >&2; exit 1; }
          ADDIN_ID="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    # Only the header block, so the shebang and internal comments stay out.
    -h|--help) sed -n '2,/^set -euo/p' "$0" | grep '^#' | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) MANIFEST="$1"; shift ;;
  esac
done

# No args -> just list what's cached, then exit.
if [ -z "$MANIFEST" ] && [ -z "$ADDIN_ID" ]; then
  echo "Add-ins currently cached in wef (id  <-  filename):"
  for app in "${APPS[@]}"; do
    d="$(wef_dir "$app")"; [ -d "$d" ] || continue
    echo "  [$app]"
    for f in "$d"/*.xml; do
      [ -f "$f" ] || continue
      b="$(basename "$f")"; printf "    %s  <-  %s\n" "${b%%.*}" "$b"
    done
  done
  echo
  echo "Re-run with the manifest path or --id <GUID> to clear one (add --apply to delete)."
  exit 0
fi

# Resolve the add-in ID from the manifest if not given explicitly.
if [ -z "$ADDIN_ID" ]; then
  [ -f "$MANIFEST" ] || { echo "ERROR: manifest not found: $MANIFEST" >&2; exit 1; }
  ADDIN_ID="$(xmllint --xpath 'string(/*[local-name()="OfficeApp"]/*[local-name()="Id"])' "$MANIFEST" 2>/dev/null \
    || grep -oE '<Id>[^<]+</Id>' "$MANIFEST" | head -1 | sed -E 's#</?Id>##g')"
fi
[ -n "$ADDIN_ID" ] || { echo "ERROR: could not determine add-in ID" >&2; exit 1; }

[ "$APPLY" -eq 1 ] && echo "Removing cached/sideloaded manifests for add-in $ADDIN_ID" \
                    || echo "DRY RUN -- would remove these (re-run with --apply to delete):"

found=0
for app in "${APPS[@]}"; do
  d="$(wef_dir "$app")"; [ -d "$d" ] || continue
  for f in "$d/$ADDIN_ID."*.xml "$d/$ADDIN_ID.xml"; do
    [ -f "$f" ] || continue
    found=1
    if [ "$APPLY" -eq 1 ]; then rm -f "$f" && echo "  removed $f"
    else echo "  would remove $f"; fi
  done
done

# A miss is a dead end, not a success. Reported as "already clear" it sends the
# admin off to restart Office, still see the stale add-in, and reach for the
# folder-wide wipe -- which on Windows takes the user's chat history with it.
if [ "$found" -eq 0 ]; then
  echo "  (no manifest matched $ADDIN_ID)"
  echo
  echo "NOT cleared. Either it was already removed, or the ID is wrong."
  echo "Re-run with no arguments to list the IDs actually on this Mac."
  exit 1
fi

echo "Quit and reopen the Office apps so they re-fetch the manifest."
