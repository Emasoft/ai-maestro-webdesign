#!/usr/bin/env bash
# amw-self-review-screenshot.sh — render an HTML file (or URL) via
# bin/amw-dev-browser-wrapper.sh and capture desktop (and optionally mobile)
# screenshots for downstream slop-audit consumption.
#
# Used by: amw-slop-verifier-agent, ai-maestro-webdesign-main-agent (Phase B
# self-review loop before delivery), any workflow that needs a rendered PNG
# of a local HTML artifact to feed into a visual audit.
#
# The script delegates ALL browser interaction to bin/amw-dev-browser-wrapper.sh
# (the ONLY sanctioned browser-automation primitive in this plugin). It does not
# run Playwright, Puppeteer, Chrome DevTools MCP, or any other stack.
#
# Usage:
#   amw-self-review-screenshot.sh <url-or-html> [--mobile] [--out DIR] [--label LABEL]
#
#   <url-or-html>   file:// URL, http(s):// URL, or absolute path to an HTML
#                   file (the script auto-prefixes file://)
#   --mobile        also capture a mobile (375x812) screenshot in addition to
#                   the desktop shot; both are saved to --out DIR
#   --out DIR       output directory; default:
#                     $MAIN_ROOT/reports/batch9-slop-review/<ts±tz>/<label>/
#                   where MAIN_ROOT is derived from git worktree list
#   --label LABEL   slug used in directory and filename; default: inferred from
#                   the input basename with non-alnum chars replaced by dashes
#
# Exit codes:
#   0  PASS — desktop screenshot produced; --mobile screenshot produced if requested
#   1  FAIL — dev-browser wrapper missing or screenshot call failed
#   2  BAD ARGS — unrecognized option or missing required argument
#
# Output:
#   Writes PNGs to <out-dir>/<label>-desktop.png (always) and
#   <out-dir>/<label>-mobile.png (when --mobile is passed).
#   Emits ONE line to stdout: the absolute path of the desktop screenshot.
#   All diagnostic messages go to stderr.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  sed -n '2,34p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

# Fail fast if dev-browser wrapper is missing.
WRAPPER="$SCRIPT_DIR/amw-dev-browser-wrapper.sh"
if [[ ! -f "$WRAPPER" ]]; then
  echo "ERROR: bin/amw-dev-browser-wrapper.sh not found at: $WRAPPER" >&2
  echo "  The dev-browser wrapper is required. Install the plugin dependencies with /amw-init." >&2
  exit 1
fi

# Resolve the main-repo root (works from worktrees and main checkout).
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  MAIN_ROOT="$(git worktree list | head -n1 | awk '{print $1}')"
else
  MAIN_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
fi

# ── Argument parsing ──────────────────────────────────────────────────────────

INPUT_URL=""
DO_MOBILE=0
LABEL=""
OUT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mobile)   DO_MOBILE=1; shift ;;
    --out)      OUT_DIR="${2:?--out requires a directory argument}"; shift 2 ;;
    --label)    LABEL="${2:?--label requires a value}"; shift 2 ;;
    -h|--help)  usage; exit 0 ;;
    -*)         echo "ERROR: unknown option: $1" >&2; usage; exit 2 ;;
    *)
      if [[ -z "$INPUT_URL" ]]; then
        INPUT_URL="$1"
      else
        echo "ERROR: unexpected positional argument: $1" >&2
        exit 2
      fi
      shift ;;
  esac
done

if [[ -z "$INPUT_URL" ]]; then
  echo "ERROR: <url-or-html> is required." >&2
  usage
  exit 2
fi

# Normalise to a URL: absolute file paths become file:// URLs.
if [[ "$INPUT_URL" != file://* && "$INPUT_URL" != http://* && "$INPUT_URL" != https://* ]]; then
  if [[ -f "$INPUT_URL" ]]; then
    INPUT_URL="file://$(realpath "$INPUT_URL")"
  else
    echo "ERROR: '$INPUT_URL' is not a valid URL and does not exist as a file." >&2
    exit 2
  fi
fi

# Derive default LABEL from URL (basename, lowercase, non-alnum → dash).
if [[ -z "$LABEL" ]]; then
  LABEL="$(basename "${INPUT_URL##*/}" .html | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]/-/g; s/-\{2,\}/-/g; s/^-*//; s/-*$//' | cut -c1-60)"
  [[ -z "$LABEL" ]] && LABEL="artifact"
fi

# Derive default OUT_DIR if not supplied.
if [[ -z "$OUT_DIR" ]]; then
  TIMESTAMP="$(date +%Y%m%d_%H%M%S%z)"
  OUT_DIR="$MAIN_ROOT/reports/batch9-slop-review/$TIMESTAMP/$LABEL"
fi

mkdir -p "$OUT_DIR"

# ── Desktop screenshot ────────────────────────────────────────────────────────

DESKTOP_OUT="$OUT_DIR/$LABEL-desktop.png"
echo "→ capturing desktop screenshot: $INPUT_URL" >&2
echo "  output: $DESKTOP_OUT" >&2

# Suppress the wrapper's own stdout (it echoes the path) so this script's
# final stdout line is the only path-bearing line the caller sees.
bash "$WRAPPER" shot "$INPUT_URL" "$DESKTOP_OUT" >/dev/null

# Confirm a PNG was actually produced (magic bytes 89 50 4E 47).
if [[ ! -f "$DESKTOP_OUT" ]]; then
  echo "ERROR: desktop screenshot not produced at $DESKTOP_OUT" >&2
  exit 1
fi
MAGIC="$(head -c 4 "$DESKTOP_OUT" | od -An -tx1 | tr -d ' \n' | cut -c1-8)"
if [[ "$MAGIC" != "89504e47" ]]; then
  echo "ERROR: $DESKTOP_OUT does not appear to be a PNG (magic bytes: $MAGIC)" >&2
  exit 1
fi
echo "  desktop PNG verified (magic bytes OK)" >&2

# ── Mobile screenshot (optional) ─────────────────────────────────────────────

if [[ "$DO_MOBILE" -eq 1 ]]; then
  MOBILE_OUT="$OUT_DIR/$LABEL-mobile.png"
  echo "→ capturing mobile screenshot (375x812): $INPUT_URL" >&2
  echo "  output: $MOBILE_OUT" >&2

  bash "$WRAPPER" mobile "$INPUT_URL" "$MOBILE_OUT" >/dev/null

  if [[ ! -f "$MOBILE_OUT" ]]; then
    echo "ERROR: mobile screenshot not produced at $MOBILE_OUT" >&2
    exit 1
  fi
  MAGIC_M="$(head -c 4 "$MOBILE_OUT" | od -An -tx1 | tr -d ' \n' | cut -c1-8)"
  if [[ "$MAGIC_M" != "89504e47" ]]; then
    echo "ERROR: $MOBILE_OUT does not appear to be a PNG (magic bytes: $MAGIC_M)" >&2
    exit 1
  fi
  echo "  mobile PNG verified (magic bytes OK)" >&2
fi

# ── Emit the single stdout line expected by callers ──────────────────────────
# Callers (including amw-slop-verifier-agent) rely on this LAST line being the
# absolute path of the desktop screenshot — nothing else should be on stdout.
echo "$DESKTOP_OUT"
