#!/usr/bin/env bash
# amw-design-md-from-url.sh — Extract a Variant 1 DESIGN.md from a live URL.
#
# Delegates DOM and computed-style extraction to the plugin's existing
# amw-dev-browser primitive (via bin/amw-dev-browser-wrapper.sh), then
# post-processes the JSON snapshot into a Variant 1 DESIGN.md.
#
# Usage:
#   bash bin/amw-design-md-from-url.sh <URL> [-o OUT] [-n NAME]
#
# Required deps already present in the plugin:
#   - bin/amw-dev-browser-wrapper.sh (wrapping the dev-browser CLI)
#   - python3 (>= 3.8) for the post-processor

set -euo pipefail

usage() {
  cat <<USAGE
Usage: bash bin/amw-design-md-from-url.sh <URL> [-o OUT] [-n NAME] [--summary-only]
       [--mode <dev-browser|curl|auto|manual>]
       [--wait-for-selector SEL] [--screenshot OUT.png] [--from-snapshot PATH]
       [--extract-states]

Extract a Variant 1 DESIGN.md from a live URL.

Options:
  -o OUT                   Output path. Default: ./DESIGN.md
  -n NAME                  Design system name. Default: from <title> or domain
  --summary-only           Probe the page and emit a JSON summary to stdout instead of
                           writing a full DESIGN.md. Useful for detecting gradient-heavy
                           heroes and noisy pages before committing to full extraction.
                           Always exits 0 (the summary is informational).
  --mode <tier>            Extraction tier. Default: dev-browser (backward-compatible).
                             dev-browser  Use the dev-browser wrapper (default).
                             curl         Fast curl + stdlib HTML parse (SSR sites).
                                          Exits 3 if result is too sparse.
                             auto         Try curl first; escalate to dev-browser on
                                          poor result; print manual instructions if
                                          both fail.
                             manual       Print a browser DevTools console snippet and
                                          exit 0. No DESIGN.md is written.
  --wait-for-selector SEL  CSS selector to wait for after page.goto() before extracting.
                           Passed to dev-browser tier only; ignored by curl tier.
  --screenshot OUT.png     Also capture a desktop screenshot to OUT.png.
                           Uses bin/amw-self-review-screenshot.sh when present.
                           Independent of --mode.
  --from-snapshot PATH     Skip dev-browser invocation and feed PATH (JSON) directly to
                           the post-processor. Closes the --mode manual loop.
  --extract-states         After the resting-state extraction, run a second pass that
                           probes pseudo-element styles (:hover / :focus / :active /
                           :disabled) for each landmark via dev-browser CDP input
                           events. Writes the captured state deltas to
                           extensions.states in the DESIGN.md frontmatter. Requires
                           --mode dev-browser (default) or --mode auto. Adds ~2-4s
                           per extraction. See TECH-extractor-pseudo-element-extraction.
  -h, --help               Show this help and exit.

Pipeline (full extraction, dev-browser mode):
  1. dev-browser eval <URL> — captures DOM landmarks + computed styles + CSS vars
  2. post-process JSON → cluster colors, infer typography, spacing, radius
  3. emit Variant 1 DESIGN.md
  4. validate via amw-design-md-lint.sh + amw-design-md-contrast.py

Pipeline (--summary-only):
  1. tier extraction <URL> — captures DOM landmarks + computed styles + CSS vars
  2. post-process JSON → count colors, fonts, radii, spacing steps
  3. emit JSON summary to stdout with warnings for problematic extraction signals

Exit codes:
  0  DESIGN.md written and passes lint  (full mode)
  0  JSON summary emitted                (--summary-only mode)
  0  Manual instructions emitted         (--mode manual)
  1  validation failed (DESIGN.md still written; see warnings)  (full mode)
  2  invocation / network error
  3  curl tier returned poor result (auto mode: triggers escalation)
USAGE
  exit 2
}

if [ $# -lt 1 ]; then usage; fi

URL=""
OUT="./DESIGN.md"
NAME=""
SUMMARY_ONLY=0
MODE="dev-browser"
WAIT_FOR_SELECTOR=""
SCREENSHOT_OUT=""
FROM_SNAPSHOT=""
EXTRACT_STATES=0

while [ $# -gt 0 ]; do
  case "$1" in
    -o) OUT="$2"; shift 2 ;;
    -n) NAME="$2"; shift 2 ;;
    --summary-only) SUMMARY_ONLY=1; shift ;;
    --mode) MODE="$2"; shift 2 ;;
    --wait-for-selector) WAIT_FOR_SELECTOR="$2"; shift 2 ;;
    --screenshot) SCREENSHOT_OUT="$2"; shift 2 ;;
    --from-snapshot) FROM_SNAPSHOT="$2"; shift 2 ;;
    --extract-states) EXTRACT_STATES=1; shift ;;
    -h|--help) usage ;;
    *)
      if [ -z "$URL" ]; then URL="$1"; shift
      else echo "Unknown argument: $1" >&2; usage; fi
      ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Error: URL is required." >&2
  usage
fi

# Validate --mode
case "$MODE" in
  dev-browser|curl|auto|manual) ;;
  *)
    echo "Error: invalid --mode value '${MODE}'. Accepted: dev-browser, curl, auto, manual." >&2
    exit 2
    ;;
esac

# Validate --extract-states is compatible with the chosen mode.
# State probing requires CDP input events, which only the dev-browser tier
# exposes. curl and manual tiers cannot drive interaction state.
if [ "$EXTRACT_STATES" = "1" ]; then
  case "$MODE" in
    curl|manual)
      echo "Error: --extract-states requires --mode dev-browser or --mode auto." >&2
      echo "       The curl and manual tiers cannot drive pseudo-element states." >&2
      exit 2
      ;;
  esac
  if [ "$SUMMARY_ONLY" = "1" ]; then
    echo "Note: --extract-states has no effect with --summary-only (no DESIGN.md is emitted)." >&2
    EXTRACT_STATES=0
  fi
fi

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WRAPPER="$PLUGIN_ROOT/bin/amw-dev-browser-wrapper.sh"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 not found on PATH." >&2
  exit 2
fi

# Step 1 — capture DOM + computed styles via dev-browser
TMP_JSON="$(mktemp -t amw-design-md-extract-XXXXXX.json)"
trap 'rm -f "$TMP_JSON"' EXIT

# The dev-browser eval expression: extract DOM landmarks + computed styles + CSS variables.
# The expression is intentionally compact; the extractor JS is embedded here.
EXTRACT_JS='
(() => {
  const pickStyle = (el) => {
    if (!el) return null;
    const cs = getComputedStyle(el);
    return {
      color: cs.color,
      backgroundColor: cs.backgroundColor,
      fontFamily: cs.fontFamily,
      fontSize: cs.fontSize,
      fontWeight: cs.fontWeight,
      lineHeight: cs.lineHeight,
      letterSpacing: cs.letterSpacing,
      borderRadius: cs.borderRadius,
      padding: cs.padding,
      margin: cs.margin,
    };
  };
  const cssVars = {};
  const root = getComputedStyle(document.documentElement);
  for (const [k, v] of Object.entries(root)) {
    if (typeof k === "string" && k.startsWith("--")) cssVars[k] = v;
  }
  const sample = (sel) => Array.from(document.querySelectorAll(sel)).slice(0, 5).map(pickStyle);
  return JSON.stringify({
    title: document.title,
    h1: sample("h1"),
    h2: sample("h2"),
    body: sample("p"),
    button: sample("button, a.btn, [role=button]"),
    input: sample("input, textarea"),
    link: sample("a"),
    nav: pickStyle(document.querySelector("nav")),
    header: pickStyle(document.querySelector("header")),
    footer: pickStyle(document.querySelector("footer")),
    cssVars,
    metaDescription: (document.querySelector("meta[name=description]") || {}).content || "",
    ogTitle: (document.querySelector("meta[property=og:title]") || {}).content || "",
  });
})()
'

# ── Tier helpers ──────────────────────────────────────────────────────────────

# run_dev_browser_tier: invoke dev-browser and write JSON to TMP_JSON.
# Returns 0 on success, 2 on failure.
run_dev_browser_tier() {
  if [ ! -x "$WRAPPER" ]; then
    echo "Error: dev-browser wrapper not found or not executable: $WRAPPER" >&2
    echo "       Run /amw-init or check the plugin install." >&2
    return 2
  fi

  # Build wait-selector prefix if requested
  local WAIT_PREFIX=""
  if [ -n "$WAIT_FOR_SELECTOR" ]; then
    WAIT_PREFIX="await page.waitForSelector(\"${WAIT_FOR_SELECTOR}\", { timeout: 10000 });"
  fi

  if "$WRAPPER" --help 2>&1 | grep -q "eval"; then
    if [ -n "$WAIT_FOR_SELECTOR" ]; then
      # Inject wait-selector into a wrapper async expression
      local FULL_JS="(async () => { ${WAIT_PREFIX} return ${EXTRACT_JS} })()"
      "$WRAPPER" eval "$URL" --expr "$FULL_JS" > "$TMP_JSON" || {
        echo "Error: dev-browser eval failed for URL: $URL" >&2
        return 2
      }
    else
      "$WRAPPER" eval "$URL" --expr "$EXTRACT_JS" > "$TMP_JSON" || {
        echo "Error: dev-browser eval failed for URL: $URL" >&2
        return 2
      }
    fi
  else
    echo "Note: dev-browser wrapper does not yet expose 'eval'. Running stub extractor." >&2
    # Stub: write minimal placeholder JSON so the post-processor can still emit a draft DESIGN.md
    cat > "$TMP_JSON" <<JSONSTUB
{
  "title": "$URL",
  "h1": [], "h2": [], "body": [], "button": [], "input": [], "link": [],
  "nav": null, "header": null, "footer": null,
  "cssVars": {},
  "metaDescription": "",
  "ogTitle": ""
}
JSONSTUB
  fi
  return 0
}

# run_curl_tier: fetch URL with curl, parse with stdlib html.parser, write JSON to TMP_JSON.
# Returns 0 on usable result, 3 on poor result (few colors, empty meta, bare domain title).
run_curl_tier() {
  local HTML_TMP
  HTML_TMP="$(mktemp -t amw-curl-html-XXXXXX.html)"
  # shellcheck disable=SC2064
  trap "rm -f '${HTML_TMP}'; rm -f '$TMP_JSON'" EXIT

  if ! command -v curl >/dev/null 2>&1; then
    echo "Error: curl not found on PATH — cannot use curl tier." >&2
    return 2
  fi

  curl -sSL --max-time 15 -A "Mozilla/5.0 (compatible; amw-design-md/0.1)" \
    "$URL" -o "$HTML_TMP" 2>/dev/null || {
    echo "Error: curl fetch failed for URL: $URL" >&2
    return 2
  }

  python3 - "$HTML_TMP" "$TMP_JSON" "$URL" <<'PYCURL'
import sys
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

html_path = sys.argv[1]
out_path  = sys.argv[2]
src_url   = sys.argv[3]

html_text = Path(html_path).read_text(errors="replace")

class DesignExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.og_title = ""
        self._in_title = False
        self._in_style = False
        self._style_buf = []
        self.inline_colors = []
        self.inline_fonts = []
        self.inline_radii = []

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "style":
            self._in_style = True
            self._style_buf = []
        elif tag == "meta":
            name = (attrs_d.get("name") or "").lower()
            prop = (attrs_d.get("property") or "").lower()
            content = attrs_d.get("content") or ""
            if name == "description":
                self.meta_description = content
            elif prop == "og:title":
                self.og_title = content
        # Parse inline style attribute
        style = attrs_d.get("style") or ""
        if style:
            for m in re.finditer(
                r"(?:background(?:-color)?|color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgb\([^)]+\))",
                style, re.I
            ):
                self.inline_colors.append(m.group(1))
            for m in re.finditer(r"font-family\s*:\s*([^;\"']+)", style, re.I):
                ff = m.group(1).strip().split(",")[0].strip().strip("\"'")
                if ff:
                    self.inline_fonts.append(ff)
            for m in re.finditer(r"border-radius\s*:\s*(\d+(?:\.\d+)?)px", style, re.I):
                self.inline_radii.append(float(m.group(1)))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "style":
            self._in_style = False
            self._style_buf = []

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_style:
            self._style_buf.append(data)

extractor = DesignExtractor()
extractor.feed(html_text)

# Collect CSS-block colors from <style> blocks via regex (minimal, no external deps)
css_colors = []
for m in re.finditer(
    r"(?:background(?:-color)?|color)\s*:\s*(#[0-9a-fA-F]{3,6})",
    html_text, re.I
):
    css_colors.append(m.group(1))

all_colors = extractor.inline_colors + css_colors

# Deduplicate colors (case-insensitive), keep order of first occurrence
seen_colors = {}
for c in all_colors:
    cl = c.lower()
    if cl not in seen_colors:
        seen_colors[cl] = c

unique_colors = list(seen_colors.values())[:20]

# Build cssVars-compatible dict from CSS variables in <style> blocks
css_vars = {}
for m in re.finditer(r"(-{2}[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})", html_text):
    css_vars[m.group(1)] = m.group(2)

# Assess quality
title_clean = extractor.title.strip()
domain = urlparse(src_url).netloc or ""
title_is_bare_domain = title_clean.lower() in ("", domain.lower(), domain.lower().lstrip("www."))
meta_empty = extractor.meta_description.strip() == ""
color_count = len(unique_colors)

poor_result = (color_count < 3) and meta_empty and title_is_bare_domain

# Build a JSON snapshot in the same shape that the dev-browser tier emits.
# curl cannot capture computed styles, so element-role arrays contain None entries.
snapshot = {
    "title": title_clean or src_url,
    "h1": [],
    "h2": [],
    "body": [],
    "button": [],
    "input": [],
    "link": [],
    "nav": None,
    "header": None,
    "footer": None,
    "cssVars": css_vars,
    "metaDescription": extractor.meta_description,
    "ogTitle": extractor.og_title,
    # Extra keys used by the quality check only — post-processor ignores them.
    "_curl_colors": unique_colors,
    "_curl_fonts": list(dict.fromkeys(extractor.inline_fonts)),
    "_curl_radii": sorted(set(extractor.inline_radii)),
    "_curl_poor_result": poor_result,
}

# Inject inline colors into cssVars so the post-processor picks them up.
for i, c in enumerate(unique_colors[:8]):
    key = f"--amw-curl-color-{i}"
    snapshot["cssVars"][key] = c

Path(out_path).write_text(json.dumps(snapshot, indent=2))

if poor_result:
    sys.exit(3)
sys.exit(0)
PYCURL

  local PYEXIT=$?
  rm -f "$HTML_TMP"
  return $PYEXIT
}

# emit_manual_instructions: print browser DevTools console snippet and exit 0.
emit_manual_instructions() {
  cat <<MANUAL
MANUAL_TIER_INSTRUCTIONS_EMITTED
Open ${URL} in any browser, open DevTools (F12) → Console, and paste:

${EXTRACT_JS}

Copy the printed JSON, save to a file (e.g., /tmp/extract.json), then re-run:

  bash bin/amw-design-md-from-url.sh ${URL} --from-snapshot /tmp/extract.json -o ${OUT}

(The --from-snapshot flag skips the dev-browser invocation and reads the
snapshot from disk directly, feeding it straight to the post-processor.)
MANUAL
  exit 0
}

# ── Tier dispatch ─────────────────────────────────────────────────────────────

if [ -n "$FROM_SNAPSHOT" ]; then
  # --from-snapshot: skip all tier invocation, feed snapshot directly to post-processor
  if [ ! -f "$FROM_SNAPSHOT" ]; then
    echo "Error: --from-snapshot path not found: $FROM_SNAPSHOT" >&2
    exit 2
  fi
  cp "$FROM_SNAPSHOT" "$TMP_JSON"
else
  case "$MODE" in
    manual)
      emit_manual_instructions
      ;;

    curl)
      run_curl_tier
      CURL_EXIT=$?
      if [ "$CURL_EXIT" -eq 3 ]; then
        echo "Note: curl tier returned poor result (CURL_TIER_POOR_RESULT)." >&2
        echo "CURL_TIER_POOR_RESULT" >&2
        exit 3
      elif [ "$CURL_EXIT" -ne 0 ]; then
        exit "$CURL_EXIT"
      fi
      ;;

    dev-browser)
      run_dev_browser_tier || exit $?
      ;;

    auto)
      # Stage 1: curl tier
      CURL_POOR=0
      if run_curl_tier; then
        CURL_POOR=0
      else
        CURL_EXIT_CODE=$?
        if [ "$CURL_EXIT_CODE" -eq 3 ] || [ -n "$WAIT_FOR_SELECTOR" ]; then
          CURL_POOR=1
        else
          exit "$CURL_EXIT_CODE"
        fi
      fi

      if [ "$CURL_POOR" -eq 1 ]; then
        echo "Note: curl tier poor result — escalating to dev-browser tier." >&2
        # Stage 2: dev-browser tier
        if ! run_dev_browser_tier; then
          # dev-browser failed — check if result is near-empty
          emit_manual_instructions
        fi
        # Verify dev-browser result is not near-empty (< 2 colors post-processing)
        DEV_COLOR_COUNT="$(python3 - "$TMP_JSON" <<'PYCOUNT'
import json, re, sys
from pathlib import Path
snap = json.loads(Path(sys.argv[1]).read_text())
def hex_re(s):
    if not s: return None
    s = str(s).strip()
    m = re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", s)
    if m: return "#" + m.group(1).lower()
    m = re.match(r"^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if m:
        r,g,b = int(m.group(1)),int(m.group(2)),int(m.group(3))
        return "#%02x%02x%02x" % (r,g,b)
    return None
colors = set()
for key in ("h1","h2","body","button","input","link"):
    for s in snap.get(key,[]) or []:
        if not s: continue
        for f in ("color","backgroundColor"):
            h = hex_re(s.get(f))
            if h: colors.add(h)
for lk in ("nav","header","footer"):
    s = snap.get(lk)
    if s:
        for f in ("color","backgroundColor"):
            h = hex_re(s.get(f))
            if h: colors.add(h)
for v in (snap.get("cssVars") or {}).values():
    h = hex_re(str(v))
    if h: colors.add(h)
print(len(colors))
PYCOUNT
)"
        if [ "${DEV_COLOR_COUNT:-0}" -lt 2 ]; then
          echo "Note: dev-browser tier near-empty result — falling back to manual instructions." >&2
          emit_manual_instructions
        fi
      fi
      ;;
  esac
fi

# ── Optional state-probe pass (--extract-states) ──────────────────────────────
# Runs a second dev-browser eval that walks the candidate landmarks
# (button / link / input / nav-a) and samples their computed style at rest
# plus under :hover / :focus / :active / :disabled. The state-delta map is
# merged back into TMP_JSON under the "_states" key, which the Python
# post-processor consumes to emit the extensions.states block.
# See: skills/amw-design-md/references/TECH-extractor-pseudo-element-extraction.md
if [ "$EXTRACT_STATES" = "1" ] && [ -z "$FROM_SNAPSHOT" ]; then
  if [ ! -x "$WRAPPER" ]; then
    echo "Warning: dev-browser wrapper unavailable — skipping state extraction." >&2
  elif ! "$WRAPPER" --help 2>&1 | grep -q "eval"; then
    echo "Warning: dev-browser wrapper does not expose 'eval' — skipping state extraction." >&2
  else
    STATE_PROBE_JS='
(async () => {
  const FIELDS = ["color","backgroundColor","borderColor","borderWidth",
                  "borderStyle","boxShadow","outline","outlineColor",
                  "outlineOffset","textDecoration","transform","opacity","cursor"];
  const pick = (el) => {
    const cs = getComputedStyle(el);
    const o = {};
    for (const f of FIELDS) o[f] = cs[f];
    return o;
  };
  const diff = (a, b) => {
    const d = {};
    for (const k of Object.keys(b)) if (a[k] !== b[k]) d[k] = b[k];
    return d;
  };
  const rafWait = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  const candidates = [
    { role: "button-primary", sel: "button, a[role=button], [type=button], [type=submit]" },
    { role: "link",           sel: "a:not([role=button])" },
    { role: "input-default",  sel: "input:not([type=hidden]), textarea, select" },
    { role: "nav-link",       sel: "nav a, nav button" },
  ];
  const out = {};
  for (const { role, sel } of candidates) {
    const el = document.querySelector(sel);
    if (!el) continue;
    const resting = pick(el);
    const states = {};
    el.dispatchEvent(new MouseEvent("mouseover", { bubbles: true }));
    el.dispatchEvent(new MouseEvent("mouseenter", { bubbles: false }));
    await rafWait();
    states.hover = diff(resting, pick(el));
    el.dispatchEvent(new MouseEvent("mouseout", { bubbles: true }));
    el.dispatchEvent(new MouseEvent("mouseleave", { bubbles: false }));
    await rafWait();
    if (typeof el.focus === "function") {
      el.focus();
      await rafWait();
      states.focus = diff(resting, pick(el));
      if (typeof el.blur === "function") el.blur();
      await rafWait();
    }
    el.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, button: 0 }));
    await rafWait();
    states.active = diff(resting, pick(el));
    el.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, button: 0 }));
    await rafWait();
    const hadDisabled = el.hasAttribute("disabled");
    if (!hadDisabled) {
      el.setAttribute("disabled", "");
      await rafWait();
      states.disabled = diff(resting, pick(el));
      el.removeAttribute("disabled");
      await rafWait();
    }
    out[role] = { resting, states };
  }
  return JSON.stringify(out);
})()
'
    STATE_JSON="$(mktemp -t amw-design-md-states-XXXXXX.json)"
    if "$WRAPPER" eval "$URL" --expr "$STATE_PROBE_JS" > "$STATE_JSON" 2>/dev/null; then
      python3 - "$TMP_JSON" "$STATE_JSON" <<'PYMERGE'
import json
import sys
from pathlib import Path

snap_path = sys.argv[1]
state_path = sys.argv[2]
try:
    snap = json.loads(Path(snap_path).read_text())
    states_raw = Path(state_path).read_text().strip()
    try:
        parsed = json.loads(states_raw)
    except json.JSONDecodeError:
        parsed = {}
    if isinstance(parsed, str):
        try:
            parsed = json.loads(parsed)
        except json.JSONDecodeError:
            parsed = {}
    snap["_states"] = parsed if isinstance(parsed, dict) else {}
    Path(snap_path).write_text(json.dumps(snap, indent=2))
except Exception as exc:
    print(f"Warning: state-merge failed: {exc}", file=sys.stderr)
PYMERGE
      STATE_COUNT="$(python3 -c "
import json, sys
from pathlib import Path
s = json.loads(Path('${TMP_JSON}').read_text())
print(len(s.get('_states') or {}))
")"
      echo "State extraction: probed ${STATE_COUNT} landmark(s)."
    else
      echo "Warning: state-probe eval failed — proceeding without states." >&2
    fi
    rm -f "$STATE_JSON"
  fi
fi

# ── Optional screenshot ────────────────────────────────────────────────────────
if [ -n "$SCREENSHOT_OUT" ]; then
  SCREENSHOT_SCRIPT="$PLUGIN_ROOT/bin/amw-self-review-screenshot.sh"
  if [ -x "$SCREENSHOT_SCRIPT" ]; then
    SCREENSHOT_DIR="$(dirname "$SCREENSHOT_OUT")"
    SCREENSHOT_LABEL="$(basename "$SCREENSHOT_OUT" .png)"
    bash "$SCREENSHOT_SCRIPT" "$URL" --out "$SCREENSHOT_DIR" --label "$SCREENSHOT_LABEL" || \
      echo "Warning: screenshot capture failed (non-fatal)." >&2
  else
    echo "Warning: amw-self-review-screenshot.sh not found or not executable — skipping screenshot." >&2
  fi
fi

# --summary-only: probe page and emit JSON summary, then exit 0
if [ "$SUMMARY_ONLY" = "1" ]; then
  if [ "$MODE" = "manual" ]; then
    echo '{"mode":"manual","summary":"manual tier — no automated snapshot"}'
    exit 0
  fi
  python3 - "$TMP_JSON" "$URL" <<'PYSUMMARY'
import json
import re
import sys
from collections import Counter
from pathlib import Path

def hex_re(s):
    if not s: return None
    s = s.strip()
    m = re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c*2 for c in h)
        return "#" + h.lower()
    m = re.match(r"^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if m:
        r, g, b = (int(m.group(i)) for i in (1, 2, 3))
        return "#%02x%02x%02x" % (r, g, b)
    return None

snapshot_path = sys.argv[1]
src_url = sys.argv[2]

snap = json.loads(Path(snapshot_path).read_text())

# Collect colors
colors = Counter()
for key in ("h1", "h2", "body", "button", "input", "link"):
    for s in snap.get(key, []) or []:
        if not s: continue
        for f in ("color", "backgroundColor"):
            h = hex_re(s.get(f))
            if h: colors[h] += 1
for lk in ("nav", "header", "footer"):
    s = snap.get(lk)
    if s:
        for f in ("color", "backgroundColor"):
            h = hex_re(s.get(f))
            if h: colors[h] += 1
for v in (snap.get("cssVars") or {}).values():
    h = hex_re(str(v))
    if h: colors[h] += 1

# Collect fonts
fonts = Counter()
for key in ("h1", "h2", "body", "button", "input", "link"):
    for s in snap.get(key, []) or []:
        if not s: continue
        ff = s.get("fontFamily", "")
        if ff:
            primary = ff.split(",")[0].strip().strip('"\'')
            if primary:
                fonts[primary] += 1

# Collect radii
radii = Counter()
for key in ("button", "input"):
    for s in snap.get(key, []) or []:
        if not s: continue
        br = s.get("borderRadius", "")
        if br:
            m = re.match(r"^(\d+(?:\.\d+)?)px", br.strip())
            if m:
                radii[int(round(float(m.group(1))))] += 1

# Collect spacing (padding values from body/button as a proxy)
spacing_vals = Counter()
for key in ("body", "button", "input"):
    for s in snap.get(key, []) or []:
        if not s: continue
        for fld in ("padding", "margin"):
            val = s.get(fld, "")
            if val:
                for part in val.split():
                    m = re.match(r"^(\d+)px$", part.strip())
                    if m:
                        v = int(m.group(1))
                        if v > 0:
                            spacing_vals[f"{v}px"] += 1

top_colors = colors.most_common(12)
top_fonts = fonts.most_common(4)
top_radii = sorted(radii.keys())[:4]
top_spacing = sorted(spacing_vals.keys(), key=lambda x: int(x[:-2]))[:8]

warnings = []
if len(top_colors) > 10:
    warnings.append("may be a gradient-heavy hero — consider --wait-for-selector for the main content")
if len(top_fonts) > 4:
    warnings.append("many font families detected — page may be using third-party widgets")
if len(top_spacing) > 8:
    warnings.append("noisy spacing — page may not have a coherent design system")

summary = {
    "url": src_url,
    "color_count": len(top_colors),
    "color_preview": [h for h, _ in top_colors[:3]],
    "font_count": len(top_fonts),
    "font_preview": [f for f, _ in top_fonts[:2]],
    "radius_count": len(top_radii),
    "radius_preview": [f"{r}px" for r in top_radii[:3]],
    "spacing_step_count": len(top_spacing),
    "spacing_preview": top_spacing[:4],
    "warnings": warnings,
}
print(json.dumps(summary, indent=2))
PYSUMMARY
  exit 0
fi

# Step 2-3 — post-process JSON → Variant 1 DESIGN.md (delegated to inline Python)
NAME_ARG="${NAME:-Auto-extracted Design System}"

python3 - "$TMP_JSON" "$OUT" "$NAME_ARG" "$URL" <<'PYEOF'
import json
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

def hex_re(s):
    if not s: return None
    s = s.strip()
    m = re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c*2 for c in h)
        return "#" + h.lower()
    m = re.match(r"^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if m:
        r, g, b = (int(m.group(i)) for i in (1, 2, 3))
        return "#%02x%02x%02x" % (r, g, b)
    return None

def collect_colors(snapshot):
    colors = Counter()
    for key in ("h1", "h2", "body", "button", "input", "link"):
        for s in snapshot.get(key, []) or []:
            if not s: continue
            for f in ("color", "backgroundColor"):
                h = hex_re(s.get(f))
                if h: colors[h] += 1
    for landmark_key in ("nav", "header", "footer"):
        s = snapshot.get(landmark_key)
        if s:
            for f in ("color", "backgroundColor"):
                h = hex_re(s.get(f))
                if h: colors[h] += 1
    # Also inspect cssVars for hex values.
    for v in (snapshot.get("cssVars") or {}).values():
        h = hex_re(str(v))
        if h: colors[h] += 1
    return colors

def collect_fonts(snapshot):
    fonts = Counter()
    for key in ("h1", "h2", "body", "button", "input", "link"):
        for s in snapshot.get(key, []) or []:
            if not s: continue
            ff = s.get("fontFamily", "")
            if ff:
                primary = ff.split(",")[0].strip().strip('"\'')
                if primary:
                    fonts[primary] += 1
    return fonts

def collect_radii(snapshot):
    radii = Counter()
    for key in ("button", "input"):
        for s in snapshot.get(key, []) or []:
            if not s: continue
            br = s.get("borderRadius", "")
            if br:
                m = re.match(r"^(\d+(?:\.\d+)?)px", br.strip())
                if m:
                    radii[int(round(float(m.group(1))))] += 1
    return radii

snapshot_path = sys.argv[1]
out_path = sys.argv[2]
name = sys.argv[3]
src_url = sys.argv[4]

snap = json.loads(Path(snapshot_path).read_text())

colors = collect_colors(snap)
top_colors = colors.most_common(8)

fonts = collect_fonts(snap)
top_fonts = fonts.most_common(3)

radii = collect_radii(snap)
top_radii = sorted(radii.keys()) if radii else [4, 8, 12]

now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

lines = []
lines.append("---")
lines.append("version: alpha")
lines.append(f'name: "{name}"')
lines.append(f'description: "Auto-extracted from {src_url} on {now}"')
lines.append("")

# Colors
if top_colors:
    lines.append("colors:")
    semantic_names = ["primary", "secondary", "tertiary", "neutral", "surface", "on-surface", "border-subtle", "accent"]
    for i, (hex_v, _count) in enumerate(top_colors):
        slug = semantic_names[i] if i < len(semantic_names) else f"discovered-{i}"
        lines.append(f'  {slug}: "{hex_v}"')
    lines.append("")

# Typography
if top_fonts:
    lines.append("typography:")
    levels = [
        ("headline-display", 48, 700, 1.1),
        ("headline-lg", 36, 600, 1.15),
        ("headline-md", 28, 600, 1.2),
        ("body-lg", 18, 400, 1.6),
        ("body-md", 16, 400, 1.6),
        ("body-sm", 14, 400, 1.5),
        ("label-md", 14, 500, 1.4),
    ]
    primary_font = top_fonts[0][0]
    for slug, size, weight, lh in levels:
        lines.append(f"  {slug}:")
        lines.append(f'    fontFamily: "{primary_font}"')
        lines.append(f'    fontSize: "{size}px"')
        lines.append(f'    fontWeight: {weight}')
        lines.append(f'    lineHeight: {lh}')
    lines.append("")

# Rounded
if top_radii:
    lines.append("rounded:")
    radii_names = ["sm", "md", "lg", "xl"]
    for i, r in enumerate(top_radii[:4]):
        slug = radii_names[i] if i < len(radii_names) else f"step-{i}"
        lines.append(f'  {slug}: "{r}px"')
    lines.append('  full: "9999px"')
    lines.append("")

# Spacing — default 8px scale
lines.append("spacing:")
lines.append('  base: "16px"')
lines.append('  xs: "4px"')
lines.append('  sm: "8px"')
lines.append('  md: "16px"')
lines.append('  lg: "32px"')
lines.append('  xl: "64px"')
lines.append("")

# Components — derive button-primary if a primary color was extracted
if top_colors:
    lines.append("components:")
    lines.append("  button-primary:")
    lines.append('    backgroundColor: "{colors.primary}"')
    if len(top_colors) >= 6:
        lines.append('    textColor: "{colors.surface}"')
    lines.append('    typography: "{typography.label-md}"')
    if top_radii:
        lines.append('    rounded: "{rounded.md}"')
    lines.append('    padding: "12px"')
    lines.append("")

# Extensions — interaction-state deltas (emitted only when --extract-states ran)
states_map = snap.get("_states") or {}
if states_map:
    lines.append("extensions:")
    lines.append("  states:")
    for role_name in sorted(states_map.keys()):
        entry = states_map.get(role_name) or {}
        if not isinstance(entry, dict):
            continue
        lines.append(f"    {role_name}:")
        resting = entry.get("resting") or {}
        if resting:
            lines.append("      resting:")
            for prop, val in sorted(resting.items()):
                if val:
                    val_str = str(val).replace('"', '\\"')
                    lines.append(f'        {prop}: "{val_str}"')
        states_block = entry.get("states") or {}
        for state_name in ("hover", "focus", "active", "disabled"):
            delta = states_block.get(state_name) or {}
            if not delta:
                continue
            lines.append(f"      {state_name}:")
            for prop, val in sorted(delta.items()):
                if val:
                    val_str = str(val).replace('"', '\\"')
                    lines.append(f'        {prop}: "{val_str}"')
    lines.append("")

lines.append("---")
lines.append("")
lines.append(f"# {name}")
lines.append("")
lines.append(f"> Auto-extracted from {src_url}. Refine prose before treating as canonical.")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"This design system was extracted from `{src_url}` on {now}. The brand uses {len(top_colors)} primary colors, {len(top_fonts)} font family/families, and a {top_radii[0] if top_radii else 8}px-base radius scale. The auto-extraction is starting input — review every token, reword the prose, and iterate.")
lines.append("")
lines.append("## Colors")
lines.append("")
if top_colors:
    semantic_names = ["primary", "secondary", "tertiary", "neutral", "surface", "on-surface", "border-subtle", "accent"]
    for i, (hex_v, count) in enumerate(top_colors):
        slug = semantic_names[i] if i < len(semantic_names) else f"discovered-{i}"
        lines.append(f"- **{slug.title()} (`{hex_v}`):** Used in {count} computed-style observations. (Auto-classified — verify role.)")
lines.append("")
lines.append("## Typography")
lines.append("")
if top_fonts:
    for f, c in top_fonts:
        lines.append(f"- `{f}` — observed {c} times.")
lines.append("")
lines.append("## Layout")
lines.append("")
lines.append("Auto-extraction defaults to an 8px base spacing scale. Verify against the live site's actual spacing usage.")
lines.append("")
lines.append("## Elevation & Depth")
lines.append("")
lines.append("Not extracted automatically — review the live site's shadow usage and document here.")
lines.append("")
lines.append("## Shapes")
lines.append("")
if top_radii:
    lines.append(f"Border-radius scale extracted: {', '.join(str(r) + 'px' for r in top_radii[:4])}.")
lines.append("")
lines.append("## Components")
lines.append("")
lines.append("- **Button (primary):** Auto-extracted backgroundColor and rounded. Review actual button styles on the live site to refine padding, hover state, and focus ring.")
lines.append("")
lines.append("## Do's and Don'ts")
lines.append("")
lines.append("- Do reference tokens by name in component code; never inline hex.")
lines.append("- Do maintain WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text).")
lines.append("- Do respect the 8px grid for every spatial value.")
lines.append("- Do use the primary color only for the single most important action per screen.")
lines.append("- Don't introduce new colors outside this palette without updating this file first.")
lines.append("- Don't use more than two font weights on a single screen.")
lines.append("- Don't mix rounded and sharp corners in the same view.")
lines.append("")

Path(out_path).write_text("\n".join(lines))
print(f"Wrote {out_path}")
PYEOF

# Step 4 — validate (best-effort)
echo "Validating $OUT ..."
if bash "$PLUGIN_ROOT/bin/amw-design-md-lint.sh" "$OUT" 2>/dev/null; then
  echo "Lint: PASS"
else
  echo "Lint: warnings or errors (see output above)" >&2
fi

if [ -x "$PLUGIN_ROOT/bin/amw-design-md-contrast.py" ]; then
  python3 "$PLUGIN_ROOT/bin/amw-design-md-contrast.py" "$OUT" || true
fi

echo "Done. Review and edit: $OUT"
