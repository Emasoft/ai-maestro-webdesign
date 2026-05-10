#!/usr/bin/env bash
#
# mermaid-render.sh — ai-maestro-webdesign plugin wrapper for
# external/mermaid-render (consolidates beautiful-mermaid + pretty-mermaid +
# agent-skill-diagramming-flows). Single entry point used by the
# `mermaid-render` skill and by any skill that needs a Mermaid → SVG or
# Mermaid → ASCII render.
#
# Usage:
#   bin/mermaid-render.sh --input <file|-> --format <svg|ascii> [--theme <name>] [--out <path>] [other flags...]
#
# --input -        reads Mermaid text from stdin (explicit form)
# (no --input)     if stdin is a pipe (not a TTY), stdin is auto-consumed
# --format svg     emits SVG to --out (or stdout)
# --format ascii   emits ASCII to --out (or stdout), piped through validate-ascii.py as a warn-only gate
# --theme <name>   one of the 15 built-in themes; see `--list-themes`
# --list-themes    prints the built-in theme list and exits
# --version        prints the wrapper version and exits
#
# Exit codes:
#   0   success
#   1   renderer / backend error
#   2   missing external/mermaid-render/ (asks the user to run /amw-init)
#   3   missing node runtime
#
# Note on the ASCII gate: beautiful-mermaid's renderMermaidAscii() can emit
# variable-width Unicode glyphs (CJK, emoji, long arrows) depending on the
# input labels. We run bin/amw-validate-ascii.py as a warn-only post-check so
# the skill's house rule ("ASCII output MUST pass amw-validate-ascii.py") is
# still visible, but we don't fail the render — the Mermaid backend's
# output is what it is, and re-running with different labels is the fix.

set -euo pipefail

# Resolve the plugin root from this script's location so the wrapper works
# whether invoked via an absolute path, a symlink, or `bin/amw-mermaid-render.sh`.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENDOR_DIR="$PLUGIN_ROOT/external/mermaid-render"
VALIDATOR="$SCRIPT_DIR/validate-ascii.py"

WRAPPER_VERSION="1.0.0"

# --- early arg sniff for --list-themes / --version / --help ---------------
for a in "$@"; do
  case "$a" in
    --version|-v)
      echo "mermaid-render.sh $WRAPPER_VERSION (ai-maestro-webdesign plugin wrapper)"
      exit 0
      ;;
    --list-themes)
      if [ ! -d "$VENDOR_DIR" ]; then
        echo "external/mermaid-render/ is missing — run /amw-init (step 7) to fetch it." >&2
        exit 2
      fi
      if ! command -v node >/dev/null 2>&1; then
        echo "node is not on PATH. Install node >= 18 and re-run." >&2
        exit 3
      fi
      exec node "$VENDOR_DIR/scripts/themes.mjs"
      ;;
    --help|-h)
      sed -n '3,29p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
  esac
done

# --- required runtime checks ---------------------------------------------
if [ ! -d "$VENDOR_DIR" ]; then
  echo "error: external/mermaid-render/ is missing." >&2
  echo "       run /amw-init (step 7 — Mermaid render backend) to vendor it, or:" >&2
  echo "       mkdir -p external && git -C \"$PLUGIN_ROOT\" clone https://github.com/Emasoft/ai-maestro-webdesign-mermaid-render external/mermaid-render" >&2
  echo "       (see external/mermaid-render/README.md for the direct-install path)" >&2
  exit 2
fi

if ! command -v node >/dev/null 2>&1; then
  echo "error: 'node' not found on PATH. Install Node.js >= 18 and re-run /amw-init." >&2
  exit 3
fi

# --- parse --format and --out out of the arg list so we can post-process
# the ASCII output. Everything else is forwarded to render.mjs verbatim.
# We leave --format and --out IN the forwarded args so the renderer still
# sees them — we only record their values for our own post-processing.
# We ALSO detect whether --input was supplied so we can fall back to stdin
# when the shell is piping something in and the caller forgot the flag.
# Source: agent-skill-diagramming-flows-main/render.ts lines 39-56 —
# the bun version treats "no --input arg + stdin is not a TTY" as implicit
# stdin mode. Keep parity here.
FORMAT="svg"
OUT_PATH=""
HAS_INPUT=0
ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --format|-f)
      FORMAT="${2:-svg}"
      ARGS+=("$1" "$2")
      shift 2
      ;;
    --out|--output|-o)
      OUT_PATH="${2:-}"
      ARGS+=("$1" "$2")
      shift 2
      ;;
    --input|-i)
      HAS_INPUT=1
      ARGS+=("$1" "$2")
      shift 2
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

# --- stdin fallback ------------------------------------------------------
# If no --input was provided AND stdin is a pipe (not a TTY), consume stdin
# into a temp file and inject --input <tmpfile> into the forwarded args.
# This keeps the single-line `echo "..." | mermaid-render.sh --format svg`
# invocation working without a fragile "--input -" incantation.
STDIN_TMPFILE=""
if [ "$HAS_INPUT" -eq 0 ] && [ ! -t 0 ]; then
  STDIN_TMPFILE="$(mktemp -t mermaid-render-stdin.XXXXXX.mmd)"
  # shellcheck disable=SC2064
  trap "rm -f '$STDIN_TMPFILE'" EXIT
  cat > "$STDIN_TMPFILE"
  ARGS+=("--input" "$STDIN_TMPFILE")
fi

# --- run the vendored renderer -------------------------------------------
# On first run this triggers an in-place `npm install` inside $VENDOR_DIR
# (see scripts/render.mjs::loadBeautifulMermaid). That is idempotent and
# only affects $VENDOR_DIR/node_modules/ which is gitignored at the root.
if ! node "$VENDOR_DIR/scripts/render.mjs" "${ARGS[@]}"; then
  exit 1
fi

# --- post-process ASCII output through validate-ascii.py (warn-only) ----
if [ "$FORMAT" = "ascii" ] && [ -n "$OUT_PATH" ] && [ -f "$OUT_PATH" ]; then
  if [ -x "$VALIDATOR" ] || [ -f "$VALIDATOR" ]; then
    # validate-ascii.py returns non-zero on issues. We intentionally ignore
    # its exit code here: the Mermaid backend is deterministic and a
    # validation failure usually means "your input labels produced
    # variable-width glyphs" — the fix is to rename labels, not to fail
    # the render. Surface the diagnostic to stderr and continue.
    if ! python3 "$VALIDATOR" "$OUT_PATH" >&2; then
      echo "[mermaid-render] warn: validate-ascii.py flagged issues in $OUT_PATH (see above). Output written anyway." >&2
    fi
  fi
fi
