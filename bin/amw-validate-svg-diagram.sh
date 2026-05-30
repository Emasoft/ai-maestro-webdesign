#!/bin/sh
# amw-validate-svg-diagram.sh — SVG validator.
# Uses xmllint for XML well-formedness + a grep sanity check for the SVG namespace.
#
# Output contract (unified across plugin validators):
#   PASS: <path>
# OR
#   FAIL: <line>: <message> [FIX: <hint>]
#   (one line per finding; exit 1)
#
# Exit codes:
#   0 — PASS
#   1 — FAIL
#   2 — CLI misuse or missing tool

set -eu

usage() {
  cat <<EOF >&2
Usage: $0 <path.svg>
Validates XML well-formedness via xmllint and checks for the SVG namespace.
EOF
  exit 2
}

[ $# -eq 1 ] || usage
input="$1"
[ -r "$input" ] || { echo "ERROR: cannot read: $input" >&2; exit 2; }

command -v xmllint >/dev/null 2>&1 || {
  echo "ERROR: xmllint not found on PATH. Install via /amw-init." >&2
  exit 2
}

had_fail=0

# 1) XML well-formedness via xmllint --noout --nonet
tmp_err=$(mktemp -t wd-svg-lint.XXXXXX)
trap 'rm -f "$tmp_err"' EXIT INT TERM
if ! xmllint --noout --nonet "$input" 2>"$tmp_err"; then
  # xmllint's error format: "<path>:<line>: <category>: <message>"
  # Re-emit each line in the unified format.
  while IFS= read -r line; do
    # Extract line number if present (xmllint path:line: prefix).
    case "$line" in
      "$input":*)
        lineno="${line#"$input":}"
        lineno="${lineno%%:*}"
        msg="${line#"$input":"$lineno":}"
        printf 'FAIL: %s: %s [FIX: fix XML well-formedness (check tags/attrs/quoting)]\n' \
          "$lineno" "${msg# }"
        ;;
      *)
        # xmllint sometimes emits context lines without the path prefix.
        case "$line" in
          *[!\ ]*) printf 'FAIL: 0: %s [FIX: fix XML well-formedness]\n' "$line" ;;
        esac
        ;;
    esac
  done <"$tmp_err"
  had_fail=1
fi

# 2) SVG namespace check — first 500 bytes must contain xmlns="http://www.w3.org/2000/svg"
head_bytes="$(dd if="$input" bs=1 count=500 2>/dev/null)"
case "$head_bytes" in
  *'xmlns="http://www.w3.org/2000/svg"'*|*"xmlns='http://www.w3.org/2000/svg'"*)
    : # OK
    ;;
  *)
    printf 'FAIL: 1: SVG namespace declaration missing in first 500 bytes [FIX: add xmlns="http://www.w3.org/2000/svg" to the root <svg> element]\n'
    had_fail=1
    ;;
esac

if [ "$had_fail" -eq 0 ]; then
  printf 'PASS: %s\n' "$input"
  exit 0
fi
exit 1
