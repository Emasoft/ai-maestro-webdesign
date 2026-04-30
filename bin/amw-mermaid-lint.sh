#!/bin/sh
# mermaid-lint.sh — lint a Mermaid source file via mmdc dry-render.
# mmdc has no standalone "lint" command; the canonical idiom is to render to a
# throwaway SVG and read stderr. Exit 0 = valid grammar; non-zero = parse error.
#
# Output contract (unified):
#   PASS: <path>
# OR
#   FAIL: <line>: <message> [FIX: <hint>]
#   (one line per finding; exit 1. Prints at most 3 findings to keep output sane.)
#
# Exit codes:
#   0 — PASS
#   1 — FAIL
#   2 — CLI misuse / missing tool

set -eu

usage() {
  cat <<EOF >&2
Usage: $0 <path.mmd>
Runs mmdc dry-render and reports grammar errors.
EOF
  exit 2
}

[ $# -eq 1 ] || usage
input="$1"
[ -r "$input" ] || { echo "ERROR: cannot read: $input" >&2; exit 2; }

command -v mmdc >/dev/null 2>&1 || {
  echo "ERROR: mmdc (mermaid-cli) not found on PATH. Install via /amw-init." >&2
  exit 2
}

tmp_svg=$(mktemp -t wd-mmdlint.XXXXXX).svg
tmp_err=$(mktemp -t wd-mmdlint.XXXXXX)
trap 'rm -f "$tmp_svg" "$tmp_err"' EXIT INT TERM

# mmdc writes a Puppeteer deprecation banner to stderr on many installs; we
# have to filter it out before scoring PASS/FAIL. The real errors start with
# "Error" or "SyntaxError" or "at Parser.parse".
set +e
mmdc -i "$input" -o "$tmp_svg" -q >/dev/null 2>"$tmp_err"
mmdc_exit=$?
set -e

if [ "$mmdc_exit" -eq 0 ] && [ -s "$tmp_svg" ]; then
  printf 'PASS: %s\n' "$input"
  exit 0
fi

# Collect up to 3 error lines, strip warnings/banners.
count=0
while IFS= read -r line; do
  case "$line" in
    ""|[Dd]eprecation*|\[WARNING\]*|warn\ *)
      continue
      ;;
    *Error*|*error*|*SyntaxError*|*"Parse error"*|*"Unknown diagram"*)
      count=$((count + 1))
      # Try to find a "Parse error on line N:" pattern for the line number.
      lineno="$(printf '%s' "$line" | sed -nE 's/.*line ([0-9]+).*/\1/p' | head -n 1)"
      [ -n "$lineno" ] || lineno=0
      printf 'FAIL: %s: %s [FIX: fix Mermaid grammar (diagram type / node syntax / arrow style)]\n' \
        "$lineno" "$line"
      [ "$count" -ge 3 ] && break
      ;;
  esac
done <"$tmp_err"

if [ "$count" -eq 0 ]; then
  # mmdc exited non-zero but we couldn't parse the error — emit a generic fail.
  printf 'FAIL: 0: mmdc exited with status %s; see stderr for details [FIX: run mmdc -i %s -o /tmp/x.svg manually]\n' \
    "$mmdc_exit" "$input"
fi
exit 1
