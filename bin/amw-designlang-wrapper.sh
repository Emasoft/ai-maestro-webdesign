#!/usr/bin/env bash
# designlang-wrapper.sh — thin wrapper over `npx designlang`.
#
# Used by: skills/amw-design-extract, /amw-extract-style.
#
# Standardizes output format and location so downstream skills (amw-design-principles,
# amw-ui-ux-reasoning, amw-ascii-to-html) can find the emitted tokens without
# hard-coding paths.
#
# Subcommands
# -----------
#   tokens <url> [out-dir]        — full multi-format token dump (default)
#   colors <url>                  — JSON palette only
#   fonts  <url>                  — JSON font stack only
#   css    <url> [out.css]        — CSS custom properties only
#
# The default output directory is $TMPDIR/ai-maestro-webdesign-tokens/<slug>/
# and contains:
#   report.md               design-principles-ready summary
#   tokens.w3c.json         W3C Design Tokens
#   tailwind.theme.css      Tailwind v4 @theme block
#   shadcn.theme.css        shadcn/ui theme CSS
#   react.theme.ts          React theme object
#   figma.variables.json    Figma variables
#   css-vars.css            plain :root { --* } block
#   preview.html            static HTML preview of the palette

set -euo pipefail

OUT_BASE="${DL_OUT_DIR:-${TMPDIR:-/tmp}/ai-maestro-webdesign-tokens}"
mkdir -p "$OUT_BASE"

# Preflight
if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx not found on PATH. Install Node.js ≥ 22 first." >&2
  exit 1
fi

# Quick detection — designlang is lazy-installed by npx on first use.
if ! npx --no-install designlang --version >/dev/null 2>&1; then
  echo "note: designlang not yet cached by npx — first call will download it" >&2
fi

slugify() {
  echo "$1" | sed -E 's#^https?://##; s#[^a-zA-Z0-9._-]+#-#g; s#^-+|-+$##g' | cut -c1-60
}

cmd="${1:-}"
if [[ -z "$cmd" ]]; then
  cat <<EOF
Usage:
  $0 tokens <url> [out-dir]
  $0 colors <url>
  $0 fonts  <url>
  $0 css    <url> [out.css]
EOF
  exit 0
fi
shift

case "$cmd" in
  tokens)
    url="${1:?URL required}"
    out_dir="${2:-$OUT_BASE/$(slugify "$url")}"
    mkdir -p "$out_dir"
    echo "→ designlang tokens  $url  →  $out_dir" >&2
    # Use the documented flag surface. Fail loudly if it doesn't work so the
    # user knows to pin designlang in /amw-init instead of silently getting a
    # reduced-output fallback (fail-fast rule — no silent workarounds).
    if ! npx designlang "$url" --out "$out_dir" --format all >/dev/null 2>&1; then
      echo "ERROR: 'npx designlang \"$url\" --out \"$out_dir\" --format all' failed." >&2
      echo "       Run 'npx designlang --help' to verify the current flag surface." >&2
      echo "       If it has changed, pin a known-good version in /amw-init." >&2
      exit 1
    fi
    echo "$out_dir"
    ;;

  colors)
    url="${1:?URL required}"
    echo "→ designlang colors  $url" >&2
    npx designlang "$url" --format json --only colors
    ;;

  fonts)
    url="${1:?URL required}"
    echo "→ designlang fonts  $url" >&2
    npx designlang "$url" --format json --only typography
    ;;

  css)
    url="${1:?URL required}"
    out="${2:-$OUT_BASE/$(slugify "$url").css}"
    echo "→ designlang css  $url  →  $out" >&2
    npx designlang "$url" --format css > "$out"
    echo "$out"
    ;;

  *)
    # Raw pass-through
    exec npx designlang "$cmd" "$@"
    ;;
esac
