#!/bin/sh
# amw-mjml-render.sh — validate and compile an MJML source file to email HTML.
# Wraps `mjml` (https://mjml.io). Uses `npx --yes mjml` so users do not need
# to globally install — npx will fetch and run on first invocation.
#
# Output contract (unified):
#   PASS: <input.mjml> -> <output.html>
# OR
#   FAIL: <line>: <message> [FIX: <hint>]
#   (one line per finding; exit 1. Prints at most 5 findings to keep output sane.)
#
# Modes:
#   --validate   Only validate (no HTML emit). Output: PASS or FAIL lines.
#   --render     Compile to HTML. Default mode.
#
# Exit codes:
#   0 — PASS (validation passed; HTML emitted if --render)
#   1 — FAIL (MJML errors)
#   2 — CLI misuse / missing input / missing tool

set -eu

usage() {
  cat <<EOF >&2
Usage: $0 [--validate|--render] <input.mjml> [<output.html>]

Modes:
  --validate    Validate only (no HTML output). Default <output.html> ignored.
  --render      Validate AND compile to HTML. (Default.)

If <output.html> is omitted in render mode, output goes to <input>.html
alongside the input. \`npx --yes mjml\` is used to invoke MJML; first run
will download the package.
EOF
  exit 2
}

mode=render
case "${1:-}" in
  --validate) mode=validate; shift ;;
  --render)   mode=render;   shift ;;
  -h|--help)  usage ;;
esac

[ $# -ge 1 ] && [ $# -le 2 ] || usage
input="$1"
[ -r "$input" ] || { echo "ERROR: cannot read: $input" >&2; exit 2; }

# Determine output path for render mode
if [ "$mode" = "render" ]; then
  if [ $# -eq 2 ]; then
    output="$2"
  else
    output="${input%.mjml}.html"
  fi
fi

command -v npx >/dev/null 2>&1 || {
  echo "ERROR: npx not found on PATH. Install Node.js (>=22) per /amw-init." >&2
  exit 2
}

tmp_err=$(mktemp -t amw-mjmlr.XXXXXX)
trap 'rm -f "$tmp_err"' EXIT INT TERM

if [ "$mode" = "validate" ]; then
  # mjml --validate <input> exits non-zero on validation errors.
  # We pipe stderr to capture errors.
  set +e
  npx --yes mjml --validate strict "$input" 2>"$tmp_err" >/dev/null
  mjml_exit=$?
  set -e

  if [ "$mjml_exit" -eq 0 ]; then
    printf 'PASS: %s\n' "$input"
    exit 0
  fi
else
  # render mode
  set +e
  npx --yes mjml "$input" -o "$output" --validate strict 2>"$tmp_err"
  mjml_exit=$?
  set -e

  if [ "$mjml_exit" -eq 0 ] && [ -s "$output" ]; then
    printf 'PASS: %s -> %s\n' "$input" "$output"
    exit 0
  fi
fi

# Parse MJML errors. mjml prints lines like:
# "Line 14 of <stdin> (mj-text) — mj-text expects parent mj-column"
count=0
while IFS= read -r line; do
  case "$line" in
    "")
      continue
      ;;
    *"Line"*"of"*|*"ValidationError"*|*"error"*|*"Error"*)
      count=$((count + 1))
      lineno="$(printf '%s' "$line" | sed -nE 's/.*Line ([0-9]+).*/\1/p' | head -n 1)"
      [ -n "$lineno" ] || lineno=0
      printf 'FAIL: %s: %s [FIX: review MJML 4 component nesting / attribute spelling]\n' "$lineno" "$line"
      [ "$count" -ge 5 ] && break
      ;;
  esac
done <"$tmp_err"

if [ "$count" -eq 0 ]; then
  # mjml exited non-zero but no parseable error — emit a generic fail.
  # The literal backticks inside the FIX hint are intentional (Markdown-style
  # code spans the user reads); shellcheck SC2016 is a false positive here.
  # shellcheck disable=SC2016
  printf 'FAIL: 0: mjml exited with status %s; see stderr for details [FIX: run `npx --yes mjml --validate strict %s` manually]\n' \
    "$mjml_exit" "$input"
fi
exit 1
