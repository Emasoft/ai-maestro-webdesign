#!/usr/bin/env bash
# amw-design-md-lint.sh — Wrapper around `npx @google/design.md lint`.
#
# Pure-Node, no API key, no remote calls beyond the npm registry on first run.
#
# Usage:
#   bash bin/amw-design-md-lint.sh <path-to-DESIGN.md> [--json]
#
# Exit codes:
#   0  — lint passes
#   1  — lint reports errors
#   2  — invocation error (file not found, npx not available, etc.)

set -euo pipefail

usage() {
  cat <<USAGE
Usage: bash bin/amw-design-md-lint.sh <path-to-DESIGN.md> [--json]

Wraps \`npx @google/design.md lint\`. The first run fetches the package via npx;
subsequent runs use the cached version. No API key required.

Options:
  --json           Pass --json to the linter for structured output

Exit codes:
  0  lint passes (no errors)
  1  lint errors reported
  2  invocation error
USAGE
  exit 2
}

if [ $# -lt 1 ]; then
  usage
fi

INPUT="$1"
shift

EXTRA_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --json)
      EXTRA_ARGS+=("--json")
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      ;;
  esac
done

if [ ! -f "$INPUT" ]; then
  echo "Error: file not found: $INPUT" >&2
  exit 2
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx not found on PATH. Install Node.js (>= 18) and try again." >&2
  echo "       The official linter requires Node + npx." >&2
  echo "       For an offline alternative, use: python3 bin/amw-design-md-validate.py" >&2
  exit 2
fi

# The official package is "@google/design.md".
# Quote the package name because of the @scoped form.
exec npx --yes "@google/design.md" lint "$INPUT" "${EXTRA_ARGS[@]}"
