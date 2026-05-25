#!/usr/bin/env bash
# amw-dev-browser-wrapper.sh — thin wrapper over the `dev-browser` CLI.
#
# Used by: skills/amw-dev-browser, /amw-preview, /amw-extract-style, and any skill
# that needs interactive browser automation.
#
# This is the ONLY sanctioned path for browser automation input in
# ai-maestro-webdesign. Rendering pipelines (bin/amw-html-export.py,
# skills/amw-infographics/) use Playwright internally — that is output emission,
# not interactive automation, and is NOT a substitute for this wrapper.
#
# Plugin-standard defaults applied here:
#   - Desktop viewport 1440×900 (override with DB_VIEWPORT="WxH")
#   - Mobile viewport 375×812 (via `mobile` subcommand)
#   - Outputs default to $TMPDIR/ai-maestro-webdesign-browser/
#   - Realistic user-agent (dev-browser default is fine; override with DB_UA)
#
# Subcommands (documented conveniences on top of the raw CLI)
# -----------------------------------------------------------
#   shot    <url> [out.png]        — full-page desktop screenshot
#   mobile  <url> [out.png]        — full-page mobile (375px) screenshot
#   dom     <url> [out.json]       — capture DOM + computed styles
#   open    <url>                  — interactive session (passes through)
#   <any-other>                    — passes args straight to `dev-browser`
#
# Environment overrides
# ---------------------
#   DB_OUT_DIR     output directory (default: $TMPDIR/ai-maestro-webdesign-browser)
#   DB_VIEWPORT    viewport WxH (default: 1440x900)
#   DB_UA          user agent (default: dev-browser built-in)
#   DB_TIMEOUT_MS  network-idle timeout in ms (default: 15000)

set -euo pipefail

OUT_DIR="${DB_OUT_DIR:-${TMPDIR:-/tmp}/ai-maestro-webdesign-browser}"
VIEWPORT="${DB_VIEWPORT:-1440x900}"
TIMEOUT_MS="${DB_TIMEOUT_MS:-15000}"
mkdir -p "$OUT_DIR"

# Preflight
if ! command -v dev-browser >/dev/null 2>&1; then
  cat >&2 <<EOF
ERROR: dev-browser CLI not found on PATH.
  Install with:   /amw-init
  Or manually:    npm install -g dev-browser && dev-browser install
EOF
  exit 1
fi

# Slug helper
slugify() {
  echo "$1" | sed -E 's#^https?://##; s#[^a-zA-Z0-9._-]+#-#g; s#^-+|-+$##g' | cut -c1-60
}

cmd="${1:-}"
if [[ -z "$cmd" ]]; then
  cat <<EOF
Usage:
  $0 shot    <url> [out.png]
  $0 mobile  <url> [out.png]
  $0 dom     <url> [out.json]
  $0 open    <url>
  $0 <raw dev-browser args...>
EOF
  exit 0
fi
shift

case "$cmd" in
  shot)
    url="${1:?URL required}"
    out="${2:-$OUT_DIR/$(slugify "$url")-desktop.png}"
    VP_W="${VIEWPORT%x*}"
    VP_H="${VIEWPORT#*x}"
    echo "→ screenshot  $url  @  ${VP_W}x${VP_H}  →  $out" >&2
    dev-browser screenshot \
      --url "$url" \
      --width "$VP_W" --height "$VP_H" \
      --full-page \
      --wait-for-network-idle \
      --timeout "$TIMEOUT_MS" \
      --output "$out"
    echo "$out"
    ;;

  mobile)
    url="${1:?URL required}"
    out="${2:-$OUT_DIR/$(slugify "$url")-mobile.png}"
    echo "→ mobile screenshot  $url  @  375x812  →  $out" >&2
    dev-browser screenshot \
      --url "$url" \
      --width 375 --height 812 \
      --full-page \
      --wait-for-network-idle \
      --timeout "$TIMEOUT_MS" \
      --output "$out"
    echo "$out"
    ;;

  dom)
    url="${1:?URL required}"
    out="${2:-$OUT_DIR/$(slugify "$url")-dom.json}"
    echo "→ capture DOM + computed styles  $url  →  $out" >&2
    # Sandboxed JS to capture the subset we need for design-extract.
    # Encoded as a here-doc; dev-browser pipes it with --script.
    SCRIPT_FILE="$(mktemp "$OUT_DIR/dom-script-XXXXXX.js")"
    cat > "$SCRIPT_FILE" <<'JS'
(() => {
  const get = (el) => ({
    tag: el.tagName.toLowerCase(),
    text: (el.innerText || '').slice(0, 200),
    computed: (() => {
      const s = window.getComputedStyle(el);
      return {
        color: s.color,
        background: s.backgroundColor,
        fontFamily: s.fontFamily,
        fontSize: s.fontSize,
        fontWeight: s.fontWeight,
        lineHeight: s.lineHeight,
        padding: s.padding,
        margin: s.margin,
        borderRadius: s.borderRadius,
        boxShadow: s.boxShadow,
      };
    })(),
  });
  const samples = {};
  ['h1', 'h2', 'h3', 'p', 'a', 'button'].forEach((sel) => {
    samples[sel] = Array.from(document.querySelectorAll(sel)).slice(0, 3).map(get);
  });
  return {
    title: document.title,
    url: window.location.href,
    viewport: { w: window.innerWidth, h: window.innerHeight },
    scroll: { w: document.body.scrollWidth, h: document.body.scrollHeight },
    bodyBg: window.getComputedStyle(document.body).backgroundColor,
    bodyFont: window.getComputedStyle(document.body).fontFamily,
    samples,
  };
})();
JS
    dev-browser eval \
      --url "$url" \
      --wait-for-network-idle \
      --timeout "$TIMEOUT_MS" \
      --script "$SCRIPT_FILE" \
      > "$out"
    rm -f "$SCRIPT_FILE"
    echo "$out"
    ;;

  open)
    url="${1:?URL required}"
    echo "→ interactive session  $url" >&2
    exec dev-browser open --url "$url"
    ;;

  *)
    # Pass-through to raw dev-browser
    exec dev-browser "$cmd" "$@"
    ;;
esac
