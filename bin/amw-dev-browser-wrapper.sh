#!/usr/bin/env bash
# amw-dev-browser-wrapper.sh — thin wrapper over the `dev-browser` CLI.
#
# Used by: skills/amw-dev-browser, /amw-preview, /amw-extract-style,
# bin/amw-design-md-from-url.sh, bin/amw-page-to-ascii-layout.py, and any skill
# that needs interactive browser automation or page capture.
#
# This is the ONLY sanctioned path for browser automation INPUT in
# ai-maestro-webdesign. Rendering pipelines (bin/amw-html-export.py,
# skills/amw-infographics/) use Playwright internally — that is output emission,
# not interactive automation, and is NOT a substitute for this wrapper.
#
# dev-browser runs scripts in a QuickJS sandbox whose pages are full Playwright
# Page objects (goto/screenshot/evaluate/…). The sandbox can only write under
# ~/.dev-browser/tmp via saveScreenshot()/writeFile(); each subcommand below
# reads the saved tmp path off stdout and copies it to the requested output.
# (The older `dev-browser screenshot --url …` / `dev-browser eval --script …`
# subcommands no longer exist in the installed CLI — this wrapper targets the
# current script-based API.)
#
# Subcommands
# -----------
#   shot    <url> [out.png]   — full-page desktop screenshot (DB_VIEWPORT)
#   mobile  <url> [out.png]   — full-page mobile (375×812) screenshot
#   dom     <url> [out.json]  — capture DOM + computed styles (design-extract subset)
#   open    <url>             — navigate a persistent named page ("amw-open")
#   <any-other>              — passes args straight to `dev-browser` (run/status/…)
#
# Each capture subcommand echoes the OUTPUT PATH as its last stdout line —
# consumers rely on this.
#
# Environment overrides
# ---------------------
#   DB_OUT_DIR     output directory (default: $TMPDIR/ai-maestro-webdesign-browser)
#   DB_VIEWPORT    desktop viewport WxH (default: 1440x900)
#   DB_TIMEOUT_MS  page-load (networkidle) timeout in ms (default: 15000)
#   HEADFUL=1      run the browser visibly (default: headless)

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

# Headless by default; HEADFUL=1 opts into a visible browser (per the
# always-headless test rule). Script-execution cap = page timeout + 30s.
HEADLESS_FLAGS=(--headless)
[[ "${HEADFUL:-}" == "1" ]] && HEADLESS_FLAGS=()
SCRIPT_TIMEOUT_S=$(( TIMEOUT_MS / 1000 + 30 ))

slugify() {
  echo "$1" | sed -E 's#^https?://##; s#[^a-zA-Z0-9._-]+#-#g; s#^-+|-+$##g' | cut -c1-60
}

# Run a generated dev-browser script file; stdout flows to the caller.
run_db_script() { # script_text
  local script; script="$(mktemp "$OUT_DIR/db-script-XXXXXX.js")"
  printf '%s' "$1" > "$script"
  local rc=0
  dev-browser "${HEADLESS_FLAGS[@]}" --timeout "$SCRIPT_TIMEOUT_S" run "$script" || rc=$?
  rm -f "$script"
  return "$rc"
}

# Screenshot helper shared by shot/mobile. page.screenshot({fullPage:true})
# preserves the documented full-page semantics. (The parity harness renders
# fixed-viewport via its own bin/amw-verify-parity.sh, not this path.)
capture_shot() { # url, w, h, out
  local url="$1" w="$2" h="$3" out="$4" saved
  saved="$(run_db_script "
const page = await browser.newPage();
await page.setViewportSize({ width: $w, height: $h });
await page.goto(\"$url\", { waitUntil: \"networkidle\", timeout: $TIMEOUT_MS });
try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}
await new Promise((r) => setTimeout(r, 500));
const p = await saveScreenshot(await page.screenshot({ fullPage: true }), \"amw-shot-$$.png\");
console.log(p);
" 2>/dev/null | tail -1)"
  [[ -n "$saved" && -f "$saved" ]] || { echo "ERROR: screenshot failed for $url" >&2; exit 2; }
  cp "$saved" "$out"
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
    VP_W="${VIEWPORT%x*}"; VP_H="${VIEWPORT#*x}"
    echo "→ screenshot  $url  @  ${VP_W}x${VP_H} (full-page)  →  $out" >&2
    capture_shot "$url" "$VP_W" "$VP_H" "$out"
    echo "$out"
    ;;

  mobile)
    url="${1:?URL required}"
    out="${2:-$OUT_DIR/$(slugify "$url")-mobile.png}"
    echo "→ mobile screenshot  $url  @  375x812 (full-page)  →  $out" >&2
    capture_shot "$url" 375 812 "$out"
    echo "$out"
    ;;

  dom)
    url="${1:?URL required}"
    out="${2:-$OUT_DIR/$(slugify "$url")-dom.json}"
    echo "→ capture DOM + computed styles  $url  →  $out" >&2
    # The capture callback runs in the browser (page.evaluate) as plain JS.
    saved="$(run_db_script "
const page = await browser.newPage();
await page.goto(\"$url\", { waitUntil: \"networkidle\", timeout: $TIMEOUT_MS });
try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}
const data = await page.evaluate(() => {
  const get = (el) => ({
    tag: el.tagName.toLowerCase(),
    text: (el.innerText || '').slice(0, 200),
    computed: (() => {
      const s = window.getComputedStyle(el);
      return {
        color: s.color, background: s.backgroundColor, fontFamily: s.fontFamily,
        fontSize: s.fontSize, fontWeight: s.fontWeight, lineHeight: s.lineHeight,
        padding: s.padding, margin: s.margin, borderRadius: s.borderRadius,
        boxShadow: s.boxShadow,
      };
    })(),
  });
  const samples = {};
  ['h1', 'h2', 'h3', 'p', 'a', 'button'].forEach((sel) => {
    samples[sel] = Array.from(document.querySelectorAll(sel)).slice(0, 3).map(get);
  });
  return {
    title: document.title, url: window.location.href,
    viewport: { w: window.innerWidth, h: window.innerHeight },
    scroll: { w: document.body.scrollWidth, h: document.body.scrollHeight },
    bodyBg: window.getComputedStyle(document.body).backgroundColor,
    bodyFont: window.getComputedStyle(document.body).fontFamily,
    samples,
  };
});
const p = await writeFile(\"amw-dom-$$.json\", JSON.stringify(data, null, 2));
console.log(p);
" 2>/dev/null | tail -1)"
    [[ -n "$saved" && -f "$saved" ]] || { echo "ERROR: DOM capture failed for $url" >&2; exit 2; }
    cp "$saved" "$out"
    echo "$out"
    ;;

  open)
    url="${1:?URL required}"
    echo "→ open persistent page 'amw-open'  $url" >&2
    run_db_script "
const page = await browser.getPage(\"amw-open\");
await page.goto(\"$url\", { waitUntil: \"networkidle\", timeout: $TIMEOUT_MS });
console.log(\"opened: \" + page.url());
"
    ;;

  *)
    # Pass-through to raw dev-browser (run/status/browsers/stop/…)
    exec dev-browser "$cmd" "$@"
    ;;
esac
