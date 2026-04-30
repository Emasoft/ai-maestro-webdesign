#!/usr/bin/env bash
# amw-design-md-diff.sh — Wrapper around `npx @google/design.md diff`.
#
# Reports added/removed/changed tokens, section reorderings, and prose changes
# between two DESIGN.md revisions.
#
# Usage:
#   bash bin/amw-design-md-diff.sh <a.md> <b.md> [--json]
#
# Exit codes:
#   0  — diff produced (regardless of whether differences exist)
#   2  — invocation error (file not found, npx not available)

set -euo pipefail

usage() {
  cat <<USAGE
Usage: bash bin/amw-design-md-diff.sh <a.md> <b.md> [--json]

Wraps \`npx @google/design.md diff\`. Pure-Node, no API key.

Options:
  --json           Structured JSON output

Exit codes:
  0  diff produced
  2  invocation error
USAGE
  exit 2
}

if [ $# -lt 2 ]; then
  usage
fi

LEFT="$1"
RIGHT="$2"
shift 2

EXTRA_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --json) EXTRA_ARGS+=("--json"); shift ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

if [ ! -f "$LEFT" ];  then echo "Error: file not found: $LEFT"  >&2; exit 2; fi
if [ ! -f "$RIGHT" ]; then echo "Error: file not found: $RIGHT" >&2; exit 2; fi

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx not found on PATH. Install Node.js (>= 18)." >&2
  exit 2
fi

exec npx --yes "@google/design.md" diff "$LEFT" "$RIGHT" "${EXTRA_ARGS[@]}"
