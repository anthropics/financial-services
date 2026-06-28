#!/usr/bin/env bash
# Sideload an Office add-in manifest for local debugging on macOS.
#
# Copies the manifest into each app's Documents/wef folder named
# <addin-id>.manifest.xml, so it (a) loads in Excel/Word/PowerPoint and
# (b) is later removable by ID with clear-addin-cache.sh.
#
# This does direct file copies — it does NOT use office-addin-dev-settings.
#
# Sideloading is additive and idempotent — it installs directly (no
# dry-run). Reverse it any time with clear-addin-cache.sh --id <GUID> --apply.
#
# Usage:
#   sideload-addin.sh /path/to/manifest.xml
set -euo pipefail

APPS=(Excel Word Powerpoint)
wef_dir() { echo "$HOME/Library/Containers/com.microsoft.$1/Data/Documents/wef"; }

MANIFEST=""
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) MANIFEST="$1"; shift ;;
  esac
done

[ -n "$MANIFEST" ] || { echo "usage: sideload-addin.sh /path/to/manifest.xml" >&2; exit 1; }
[ -f "$MANIFEST" ] || { echo "ERROR: manifest not found: $MANIFEST" >&2; exit 1; }

ADDIN_ID="$(xmllint --xpath 'string(/*[local-name()="OfficeApp"]/*[local-name()="Id"])' "$MANIFEST" 2>/dev/null \
  || grep -oE '<Id>[^<]+</Id>' "$MANIFEST" | head -1 | sed -E 's#</?Id>##g')"
[ -n "$ADDIN_ID" ] || { echo "ERROR: could not read <Id> from manifest" >&2; exit 1; }

DEST_NAME="$ADDIN_ID.manifest.xml"
echo "Sideloading add-in $ADDIN_ID"

for app in "${APPS[@]}"; do
  d="$(wef_dir "$app")"
  mkdir -p "$d"
  cp "$MANIFEST" "$d/$DEST_NAME"
  echo "  installed $d/$DEST_NAME"
done

echo "Quit and reopen Excel/Word/PowerPoint. The add-in appears under"
echo "Insert -> My Add-ins. Remove later with:"
echo "  ./clear-addin-cache.sh --id $ADDIN_ID --apply"
