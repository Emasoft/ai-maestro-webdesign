#!/bin/sh
# amw-validate-diagram.sh — top-level validator dispatcher.
#
# Usage:
#   bin/amw-validate-diagram.sh <path>
#
# Auto-detects format via bin/amw-diagram-detect-format.sh and routes to:
#   ascii    -> bin/amw-validate-ascii.py
#   svg      -> bin/amw-validate-svg-diagram.sh
#   html     -> bin/amw-validate-html-diagram.sh
#   mermaid  -> bin/amw-mermaid-lint.sh
#   png      -> hardcoded refusal (PNG is output-only by plugin directive)
#   unknown  -> exit 2 with a hint
#
# Output contract (unified across all validators):
#   PASS: <path>
# OR
#   FAIL: <line>: <message> [FIX: <hint>]
#
# Exit codes:
#   0 — PASS
#   1 — FAIL
#   2 — PNG-input refusal OR unknown-format
#   3 — CLI misuse / missing tool

set -eu

SELF_DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"

usage() {
  cat <<EOF >&2
Usage: $0 <path>
Dispatches to the format-specific validator for ASCII / SVG / HTML / Mermaid.
PNG inputs are refused per plugin directive (PNG is output-only).
EOF
  exit 3
}

[ $# -eq 1 ] || usage
input="$1"
[ -r "$input" ] || { echo "ERROR: cannot read: $input" >&2; exit 3; }

detect="$SELF_DIR/amw-diagram-detect-format.sh"
[ -x "$detect" ] || { echo "ERROR: missing $detect" >&2; exit 3; }

fmt="$("$detect" "$input")"

case "$fmt" in
  ascii)
    if command -v python3 >/dev/null 2>&1 && [ -x "$SELF_DIR/amw-validate-ascii.py" ]; then
      exec python3 "$SELF_DIR/amw-validate-ascii.py" "$input"
    else
      echo "ERROR: no ASCII validator available (need python3)." >&2
      exit 3
    fi
    ;;
  svg)
    exec "$SELF_DIR/amw-validate-svg-diagram.sh" "$input"
    ;;
  html)
    exec "$SELF_DIR/amw-validate-html-diagram.sh" "$input"
    ;;
  mermaid)
    exec "$SELF_DIR/amw-mermaid-lint.sh" "$input"
    ;;
  png)
    echo "REFUSE: PNG is output-only by plugin directive; validate the source artifact instead."
    echo "        Provide the ASCII / HTML / SVG / Mermaid source that produced this PNG."
    exit 2
    ;;
  unknown|*)
    echo "UNKNOWN: could not detect diagram format for $input"
    echo "         If the file is a diagram, pass a recognized extension"
    echo "         (.txt, .md, .html, .svg, .mmd, .mermaid) or add a format marker"
    echo "         (e.g. 'flowchart TD' on the first line of a Mermaid file)."
    exit 2
    ;;
esac
