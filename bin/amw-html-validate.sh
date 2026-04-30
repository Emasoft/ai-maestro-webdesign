#!/bin/sh
# amw-html-validate.sh — validate an HTML file's syntax via tidy (if installed)
# or via a regex sanity-check fallback. Exit 0 = PASS; non-zero = FAIL.
#
# Output contract (unified):
#   PASS: <path>
# OR
#   FAIL: <line>: <message> [FIX: <hint>]
#   (one line per finding; exit 1. Prints at most 5 findings to keep output sane.)
#
# Exit codes:
#   0 — PASS
#   1 — FAIL (validation errors found)
#   2 — CLI misuse / missing input

set -eu

usage() {
  cat <<EOF >&2
Usage: $0 <path.html>
Validates HTML syntax. Prefers \`tidy\` (BSD/GNU); falls back to
regex sanity-check when tidy is unavailable.
EOF
  exit 2
}

[ $# -eq 1 ] || usage
input="$1"
[ -r "$input" ] || { echo "ERROR: cannot read: $input" >&2; exit 2; }

# Prefer tidy if installed — most thorough validator
if command -v tidy >/dev/null 2>&1; then
  tmp_err=$(mktemp -t amw-htmlv.XXXXXX)
  trap 'rm -f "$tmp_err"' EXIT INT TERM

  # tidy -e -q prints errors to stderr (and exits non-zero on errors)
  # -e = errors only (no auto-fix output)
  # -q = quiet (suppress info messages)
  set +e
  tidy -e -q "$input" 2>"$tmp_err" >/dev/null
  tidy_exit=$?
  set -e

  # tidy exits: 0=clean, 1=warnings-only, 2=errors
  if [ "$tidy_exit" -eq 0 ]; then
    printf 'PASS: %s\n' "$input"
    exit 0
  fi

  # Parse tidy output. tidy emits lines like:
  # "line 42 column 5 - Error: <element> is not recognized!"
  count=0
  while IFS= read -r line; do
    case "$line" in
      *"Error:"*|*"error:"*)
        count=$((count + 1))
        lineno="$(printf '%s' "$line" | sed -nE 's/.*line ([0-9]+).*/\1/p' | head -n 1)"
        [ -n "$lineno" ] || lineno=0
        msg="$(printf '%s' "$line" | sed -E 's/^line [0-9]+ column [0-9]+ - //')"
        printf 'FAIL: %s: %s [FIX: fix HTML syntax error per tidy report]\n' "$lineno" "$msg"
        [ "$count" -ge 5 ] && break
        ;;
    esac
  done <"$tmp_err"

  if [ "$count" -eq 0 ] && [ "$tidy_exit" -ne 1 ]; then
    # tidy exit 2 but no Error: lines parsed — emit a generic fail
    printf 'FAIL: 0: tidy exited with status %s; see stderr for details [FIX: run tidy -e -q %s manually]\n' \
      "$tidy_exit" "$input"
    exit 1
  fi

  if [ "$tidy_exit" -eq 1 ]; then
    # warnings only — pass with a note
    printf 'PASS: %s (with warnings; run tidy -e -q manually for details)\n' "$input"
    exit 0
  fi

  exit 1
fi

# Fallback: regex sanity check (no tidy available)
# This is a coarse check — catches structural problems but not all HTML errors.
echo "WARN: tidy not found; running regex sanity-check fallback. Install tidy for full validation." >&2

count=0

# Check for unclosed common tags
for tag in html head body header main footer nav section article div span p ul ol li table tr td form; do
  open_count=$(grep -oiE "<${tag}\\b[^>]*>" "$input" | grep -ovE "<${tag}\\b[^>]*/>" | wc -l)
  close_count=$(grep -oiE "</${tag}>" "$input" | wc -l)
  # Trim whitespace
  open_count=$(printf '%s' "$open_count" | tr -d ' ')
  close_count=$(printf '%s' "$close_count" | tr -d ' ')
  if [ "$open_count" -ne "$close_count" ]; then
    count=$((count + 1))
    printf 'FAIL: 0: <%s> open/close mismatch (%s open, %s close) [FIX: check for unclosed <%s> tags]\n' \
      "$tag" "$open_count" "$close_count" "$tag"
    [ "$count" -ge 5 ] && break
  fi
done

# Check for missing DOCTYPE
if ! grep -qiE '^<!DOCTYPE' "$input"; then
  count=$((count + 1))
  printf 'FAIL: 1: missing <!DOCTYPE html> declaration [FIX: add <!DOCTYPE html> as first line]\n'
fi

# Check for missing <html lang>
if grep -qiE '<html\\b' "$input" && ! grep -qiE '<html\\b[^>]*\\blang=' "$input"; then
  count=$((count + 1))
  printf 'FAIL: 0: <html> missing lang attribute [FIX: add lang="en" or appropriate locale]\n'
fi

# Check for missing <title>
if ! grep -qiE '<title>[^<]+</title>' "$input"; then
  count=$((count + 1))
  printf 'FAIL: 0: missing or empty <title> element [FIX: add <title>Page title</title> in <head>]\n'
fi

# Check for missing viewport meta
if ! grep -qiE '<meta\\b[^>]*name=["'"'"']viewport["'"'"']' "$input"; then
  count=$((count + 1))
  printf 'FAIL: 0: missing <meta name="viewport"> [FIX: add <meta name="viewport" content="width=device-width, initial-scale=1">]\n'
fi

if [ "$count" -eq 0 ]; then
  printf 'PASS: %s (regex fallback; install tidy for full validation)\n' "$input"
  exit 0
fi

exit 1
