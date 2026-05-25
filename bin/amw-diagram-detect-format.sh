#!/bin/sh
# amw-diagram-detect-format.sh — sniff a diagram file (or stdin) and print exactly
# one of: ascii, html, svg, mermaid, png, unknown — to stdout.
#
# Canonical detection rules (per §3.2 of the 12-commands build plan):
#   1. Extension dispatch:
#        .mmd | .mermaid          -> mermaid
#        .png                     -> png  (then verify magic bytes below)
#        .svg                     -> svg
#        .html | .htm             -> html
#        .txt | .md               -> fall through to content sniffing
#        anything else            -> fall through to content sniffing
#   2. Magic / first-line sniff (POSIX shell; no bashisms):
#        starts with PNG magic (\x89PNG)       -> png
#        starts with <?xml or <svg             -> svg
#        starts with <!DOCTYPE html / <html    -> html (case-insensitive)
#        first non-empty line matches
#          flowchart|sequenceDiagram|
#          stateDiagram|classDiagram|erDiagram|
#          gantt|pie|journey|mindmap|graph    -> mermaid
#        contains box-drawing chars (─│┌┐└┘├┤┬┴┼)
#          or "+---+" / "| |" ASCII grid       -> ascii
#        otherwise                              -> unknown
#
# Exit codes:
#   0 — recognized format (stdout = single word)
#   1 — unknown (stdout = "unknown")
#   2 — CLI misuse (missing arg, unreadable path)
#
# Usage:
#   bin/amw-diagram-detect-format.sh <path>
#   cat foo.txt | bin/amw-diagram-detect-format.sh -

set -eu

usage() {
  cat <<EOF >&2
Usage: $0 <path-to-file>     # detect format by path
       $0 -                  # detect format from stdin (no extension hint)
EOF
  exit 2
}

[ $# -eq 1 ] || usage

input="$1"

case "$input" in
  -|/dev/stdin)
    path_ext=""
    # Read up to 4 KB of stdin once; use it for all content checks below.
    # dd is POSIX; head -c isn't (portability — macOS head accepts -c but
    # BusyBox variants differ). We use `dd` with a conservative count.
    content="$(dd bs=1 count=4096 2>/dev/null || true)"
    ;;
  *)
    [ -r "$input" ] || { echo "ERROR: cannot read: $input" >&2; exit 2; }
    # Normalize the extension to lowercase the POSIX way (tr).
    path_ext="$(printf '%s' "$input" | awk -F. 'NF>1 {print tolower($NF)}')"
    # Read the first 4 KB only (magic + shebang + first-line keyword fit here).
    content="$(dd if="$input" bs=1 count=4096 2>/dev/null || true)"
    ;;
esac

# Rule 1a — unambiguous extension dispatch
case "$path_ext" in
  mmd|mermaid)
    echo "mermaid"
    exit 0
    ;;
  svg)
    # Verify it looks like SVG before committing (avoid misnamed files).
    case "$content" in
      "<?xml"*|"<svg"*|*"<svg "*)
        echo "svg"; exit 0 ;;
    esac
    # Fall through — extension says svg but content doesn't; try other rules.
    ;;
  html|htm)
    # Case-insensitive check for DOCTYPE / <html
    lowered="$(printf '%s' "$content" | tr '[:upper:]' '[:lower:]')"
    case "$lowered" in
      "<!doctype html"*|"<html"*|*"<!doctype html"*|*"<html "*|*"<html>"*)
        echo "html"; exit 0 ;;
    esac
    # Fall through — extension says html but content doesn't.
    ;;
esac

# Rule 2a — PNG magic bytes (0x89 50 4E 47 0D 0A 1A 0A)
# We can't use $content for magic-byte comparison reliably because shell
# variable assignment drops NUL. Instead: read the first 8 bytes with od.
if [ "$input" != "-" ] && [ -r "$input" ]; then
  magic="$(od -An -c -N 8 "$input" 2>/dev/null | tr -s ' ' ' ' | sed 's/^ //')"
  case "$magic" in
    "211   P   N   G"*|*"P   N   G"*)
      # Verified PNG magic — this is a real PNG
      echo "png"
      exit 0
      ;;
  esac
  # Also trust the extension if the magic check couldn't be decisive:
  if [ "$path_ext" = "png" ]; then
    echo "png"
    exit 0
  fi
fi

# Rule 2b — XML / SVG sniff (content-only)
case "$content" in
  "<?xml"*|"<svg"*|*"<svg "*|*"<svg>"*)
    echo "svg"
    exit 0
    ;;
esac

# Rule 2c — HTML sniff (case-insensitive)
lowered="$(printf '%s' "$content" | tr '[:upper:]' '[:lower:]')"
case "$lowered" in
  "<!doctype html"*|"<html"*|*"<!doctype html"*|*"<html "*|*"<html>"*)
    echo "html"
    exit 0
    ;;
esac

# Rule 2d — Mermaid keyword on first non-empty line
first_non_empty="$(printf '%s' "$content" | awk 'NF {print; exit}')"
case "$first_non_empty" in
  flowchart*|sequenceDiagram*|stateDiagram*|classDiagram*|erDiagram*|gantt*|pie*|journey*|mindmap*|graph*)
    echo "mermaid"
    exit 0
    ;;
esac

# Rule 2e — ASCII box-drawing or +---+ style
# grep -q: portable across BSD and GNU. -l/--binary-files unsupported on some
# BusyBox builds, so we pipe $content in.
if printf '%s' "$content" | grep -q -E '─|│|┌|┐|└|┘|├|┤|┬|┴|┼|\+-+\+' ; then
  echo "ascii"
  exit 0
fi

# Last chance — extension-only fallback for ambiguous text files.
case "$path_ext" in
  txt|md)
    # A .txt without any box chars and without a mermaid keyword isn't a diagram.
    echo "unknown"
    exit 1
    ;;
esac

echo "unknown"
exit 1
