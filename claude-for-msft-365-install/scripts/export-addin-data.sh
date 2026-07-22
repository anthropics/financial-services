#!/usr/bin/env bash
# Export a copy of the Claude Office add-in's local data on macOS -- chat
# history, uploaded skills, MCP registrations, and memory.
#
# READ ONLY. This script never writes to, moves, or deletes anything in Office.
# It reads the add-in's storage and copies it to a folder you name. Run it with
# no arguments and it only prints what it found.
#
# SEE IT YOURSELF -- you do not need this script to look
#   The data is a plain, unencrypted folder. Open it in Finder:
#
#     open ~/Library/Containers/com.microsoft.Excel/Data/Library/WebKit/WebsiteData/Default
#
#   Each subfolder there is one website's storage, named with a salted hash.
#   Print which is which:
#
#     for d in ~/Library/Containers/com.microsoft.Excel/Data/Library/WebKit/\
# WebsiteData/Default/*/; do echo "$(strings "$d$(basename "$d")/origin" | \
# head -2 | tr '\n' ' ')  <- $(basename "$d")"; done
#
#   Chat history is IndexedDB/<uppercase SHA-256 of "claude-chat-history">.
#   Check that hash yourself: printf 'claude-chat-history' | shasum -a 256
#   Swap "Excel" for "Word" / "Powerpoint" / "Outlook" for the other apps.
#
# NOTES
#   * Each Office app has its own storage, so Excel / Word / PowerPoint each
#     keep separate chat history. That is expected.
#   * Unlike Windows, the path has no per-Office-account segment -- storage
#     belongs to the macOS user account, and Office accounts signed in within
#     it share one store. So there is nothing to pick between: this exports
#     everything under the current macOS user.
#   * Sign-in tokens are deliberately NOT exported. The export does contain
#     conversation text -- handle it under your normal data policy.
#   * Office can stay open. The data is SQLite and this takes a consistent
#     snapshot of an open database.
#   * Precisely: no conversation, skill, MCP or memory record is altered, and
#     no file is moved or deleted. Opening a SQLite database does update the
#     mtime of its -shm shared-memory index, so a byte-level before/after audit
#     will show those (size unchanged). Nothing else in Office is touched.
#   * You do NOT need this to change add-ins. Storage is keyed by the origin
#     the add-in is served from, not by add-in ID, so replacing the manifest,
#     reinstalling, or moving to the store listing leaves the data in place.
#     Export before a machine is rebuilt or wiped.
#
# Usage:
#   export-addin-data.sh              # list what is on this Mac, copy nothing
#   export-addin-data.sh --out DIR    # copy it to DIR
set -euo pipefail

APPS=(Excel Word Powerpoint Outlook)
DBS=(claude-chat-history claude-local-skills claude-mcp-gateways claude-memory claude-office-snipped-results)

OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    # Guard the value: a bare `--out` would otherwise make `shift 2` fail under
    # `set -e` and exit 1 with no output at all.
    --out) [ $# -ge 2 ] || { echo "ERROR: --out requires a directory" >&2; exit 1; }
           OUT="$2"; shift 2 ;;
    -h|--help) sed -n '2,/^set -euo/p' "$0" | grep '^#' | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "ERROR: unknown argument: $1 (see --help)" >&2; exit 1 ;;
  esac
done

command -v sqlite3 >/dev/null || { echo "ERROR: sqlite3 not found on PATH" >&2; exit 1; }
# xxd ships with macOS, but a trimmed PATH would otherwise fail per-origin with
# a confusing "no stores found" rather than a real error.
command -v xxd >/dev/null || { echo "ERROR: xxd not found on PATH" >&2; exit 1; }

website_data() { echo "$HOME/Library/Containers/com.microsoft.$1/Data/Library/WebKit/WebsiteData/Default"; }

# A database's folder name is the uppercase SHA-256 of its name.
db_hash() { printf '%s' "$1" | shasum -a 256 | cut -d' ' -f1 | tr 'a-z' 'A-Z'; }

# The `origin` file is length-prefixed binary: for each of scheme and host a
# u32 LE length, a 1-byte flag, then the string; then a 1-byte "has port" flag
# and, if set, a u16 LE port.
#
# The port has to be parsed, not skipped. Storage is per-origin and an origin
# includes the port, so https://addins.contoso.com and
# https://addins.contoso.com:8443 are two separate stores -- labelling both
# "addins.contoso.com" would land them in one export folder, silently
# overwriting the first. Self-hosted deployments hit this.
read_origin() {
  local hex off len s h
  hex="$(xxd -p -c 1000000 "$1" 2>/dev/null | tr -d '\n')" || return 1
  [ ${#hex} -ge 20 ] || return 1
  u32() { printf '%d' "$((16#${hex:$(($1*2+6)):2}${hex:$(($1*2+4)):2}${hex:$(($1*2+2)):2}${hex:$(($1*2)):2}))"; }
  u16() { printf '%d' "$((16#${hex:$(($1*2+2)):2}${hex:$(($1*2)):2}))"; }
  str() { printf '%s' "${hex:$(($1*2)):$(($2*2))}" | xxd -r -p; }

  len=$(u32 0);      s=$(str 5 "$len");            off=$((5 + len))
  len=$(u32 "$off"); h=$(str $((off + 5)) "$len"); off=$((off + 5 + len))
  [ -n "$s" ] && [ -n "$h" ] || return 1
  if [ "$((16#${hex:$((off * 2)):2}))" -eq 1 ]; then echo "$s://$h:$(u16 $((off + 1)))"
  else echo "$s://$h"; fi
}

# `.backup` is a sqlite3 dot-command, not SQL, and its own quoting has no
# escape for an embedded apostrophe -- so /Users/o'brien/export would break.
# Sidestep it: run from the destination directory and pass a bare filename,
# which is always IndexedDB.sqlite3 or localstorage.sqlite3. The SOURCE path is
# an ordinary argv entry, so it needs no special handling.
#
# One unreadable store must not abort the run and strand a half-finished export
# -- record it and keep going, then report at the end.
FAILED=0
backup_db() {
  if ( cd "$(dirname "$2")" && sqlite3 "$1" ".backup '$(basename "$2")'" ) 2>/dev/null; then
    return 0
  fi
  echo "    !! could not copy $(basename "$(dirname "$1")") -- skipped" >&2
  FAILED=$((FAILED + 1))
  return 0
}

if [ -n "$OUT" ]; then echo "Exporting to $OUT"
else echo "Add-in data on this Mac (pass --out DIR to copy it):"; fi
echo

found=0
for app in "${APPS[@]}"; do
  base="$(website_data "$app")"; [ -d "$base" ] || continue

  for od in "$base"/*/; do
    oh="$(basename "$od")"; [ "$oh" = "salt" ] && continue
    inner="$od$oh"; [ -d "$inner/IndexedDB" ] || continue

    origin="$(read_origin "$inner/origin" || true)"
    [ -n "${origin:-}" ] || continue

    present=()
    for db in "${DBS[@]}"; do
      [ -d "$inner/IndexedDB/$(db_hash "$db")" ] && present+=("$db")
    done
    [ "${#present[@]}" -eq 0 ] && continue
    found=$((found + 1))

    # localStorage sits beside IndexedDB in the same per-origin folder. It is
    # small but not redundant: settings, the inference/customer config, and the
    # onboarding + terms-accepted flags live here, not in IndexedDB.
    lstore="$inner/LocalStorage/localstorage.sqlite3"

    echo "[$app] $origin"
    for db in "${present[@]}"; do
      printf '    %-32s %s\n' "$db" "$(du -sh "$inner/IndexedDB/$(db_hash "$db")" 2>/dev/null | cut -f1 | tr -d ' ')"
    done
    [ -f "$lstore" ] && printf '    %-32s %s\n' "local-storage (settings)" \
      "$(du -sh "$inner/LocalStorage" 2>/dev/null | cut -f1 | tr -d ' ')"

    if [ -n "$OUT" ]; then
      # Name the destination after the app and host so the export is readable
      # without knowing anything about salted hashes. ':' would show up as '/'
      # in Finder, so a non-default port becomes host_port.
      dest="$OUT/$app/$(printf '%s' "${origin#*://}" | tr ':' '_')"
      mkdir -p "$dest"
      for db in "${present[@]}"; do
        mkdir -p "$dest/$db"
        # `.backup` rather than cp: a consistent snapshot even with Office
        # open, and it folds in the write-ahead log.
        backup_db "$inner/IndexedDB/$(db_hash "$db")/IndexedDB.sqlite3" "$dest/$db/IndexedDB.sqlite3"
        # Any out-of-line attachment files sit beside the SQLite file.
        find "$inner/IndexedDB/$(db_hash "$db")" -maxdepth 1 -type f \
          ! -name 'IndexedDB.sqlite3*' -exec cp {} "$dest/$db/" \;
      done
      if [ -f "$lstore" ]; then
        mkdir -p "$dest/local-storage"
        backup_db "$lstore" "$dest/local-storage/localstorage.sqlite3"
      fi
      echo "    -> $dest"
    fi
    echo
  done
done

if [ "$found" -eq 0 ]; then
  echo "  (nothing found -- has the add-in been used on this Mac?)"
  # Listing nothing is a fine answer. Being ASKED to export and exporting
  # nothing is not: `export --out DIR && rm -rf ...` would treat an empty
  # export as a green light and destroy the only copy. Fail so it can't.
  [ -z "$OUT" ] && exit 0
  echo
  echo "NOTHING WAS EXPORTED to $OUT. Do not wipe anything on the strength of"
  echo "this run. On a machine where the add-in has been used, check that Office"
  echo "is signed into the expected account, then re-run."
  exit 1
fi

if [ -n "$OUT" ]; then
  echo "Done. $found location(s) exported to $OUT"
  echo "Nothing in Office was modified."
  if [ "$FAILED" -gt 0 ]; then
    echo
    echo "WARNING: $FAILED database(s) could not be copied -- this export is INCOMPLETE."
    exit 1
  fi
fi
