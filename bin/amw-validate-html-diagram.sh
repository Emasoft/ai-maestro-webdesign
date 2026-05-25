#!/bin/sh
# amw-validate-html-diagram.sh — HTML validator for diagrams (editorial / infographic
# HTML+SVG output). Wraps:
#   1. xmllint --html --noout --nonet  (XML-ish well-formedness for HTML5)
#   2. tidy -e -q -errors              (HTML-specific linting; optional)
#
# Output contract (unified):
#   PASS: <path>
# OR
#   FAIL: <line>: <message> [FIX: <hint>]
#   (one line per finding; exit 1)
#
# Exit codes:
#   0 — PASS
#   1 — FAIL
#   2 — CLI misuse / missing tool
#
# Notes:
#   - xmllint --html is lenient about HTML5 (it uses an HTML4-era parser); we
#     treat its findings as warnings unless they would break parsing.
#   - tidy is optional. If it isn't on PATH we skip it. /amw-init installs it.

set -eu

usage() {
  cat <<EOF >&2
Usage: $0 <path.html>
Validates HTML via xmllint --html (well-formedness) and tidy (if available).
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

tmp_err=$(mktemp -t wd-html-xmllint.XXXXXX)
tmp_tidy=$(mktemp -t wd-html-tidy.XXXXXX)
trap 'rm -f "$tmp_err" "$tmp_tidy"' EXIT INT TERM

# 1) xmllint --html
if ! xmllint --html --noout --nonet "$input" 2>"$tmp_err"; then
  had_fail=1
fi
# Even on exit 0, xmllint emits warnings to stderr. We surface them all.
while IFS= read -r line; do
  case "$line" in
    "$input":*)
      lineno="${line#"$input":}"
      lineno="${lineno%%:*}"
      msg="${line#"$input":"$lineno":}"
      printf 'FAIL: %s: %s [FIX: fix HTML structure (check tags / attrs / nesting)]\n' \
        "$lineno" "${msg# }"
      had_fail=1
      ;;
  esac
done <"$tmp_err"

# 2) tidy (optional)
if command -v tidy >/dev/null 2>&1; then
  # tidy writes errors/warnings to stderr; exit code:
  #   0 — no errors / warnings
  #   1 — warnings
  #   2 — errors
  tidy -e -q -errors "$input" >/dev/null 2>"$tmp_tidy" || true
  while IFS= read -r line; do
    # tidy error format: "line N column M - {Error|Warning}: <msg>"
    case "$line" in
      line\ *)
        lineno="$(printf '%s' "$line" | awk '{print $2}')"
        msg="$(printf '%s' "$line" | sed -E 's/^line [0-9]+ column [0-9]+ - //')"
        case "$msg" in
          Error:*|error:*)
            printf 'FAIL: %s: tidy %s [FIX: fix HTML error before shipping]\n' \
              "$lineno" "$msg"
            had_fail=1
            ;;
          Warning:*|warning:*)
            printf 'FAIL: %s: tidy %s [FIX: resolve or suppress the warning]\n' \
              "$lineno" "$msg"
            had_fail=1
            ;;
        esac
        ;;
    esac
  done <"$tmp_tidy"
fi

if [ "$had_fail" -eq 0 ]; then
  printf 'PASS: %s\n' "$input"
  exit 0
fi
exit 1
