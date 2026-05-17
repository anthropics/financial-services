#!/usr/bin/env bash
# Clear a single Office add-in's cached / sideloaded manifest on macOS.
#
# The Wef cache holds every add-in side by side, each file named
# <addin-id>.manifest-*.xml. This removes ONLY the files matching one
# add-in ID across Excel/Word/PowerPoint -- it never wipes the folder.
#
# Usage:
#   clear-addin-cache.sh                       # list every add-in found, do nothing
#   clear-addin-cache.sh /path/to/manifest.xml # dry-run: show what would be removed
#   clear-addin-cache.sh --id <GUID>           # dry-run by ID (no manifest needed)
#   clear-addin-cache.sh /path/manifest.xml --apply   # actually delete
set -euo pipefail

APPS=(Excel Word Powerpoint)
wef_dir() { echo "$HOME/Library/Containers/com.microsoft.$1/Data/Documents/wef"; }

MANIFEST="" ADDIN_ID="" APPLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --id) ADDIN_ID="${2:-}"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
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

[ "$found" -eq 0 ] && echo "  (nothing found for $ADDIN_ID -- already clear)"
echo "Quit and reopen the Office apps so they re-fetch the manifest."
