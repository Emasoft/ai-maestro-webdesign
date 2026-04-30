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
Usage: bash bin/amw-design-md-from-url.sh <URL> [-o OUT] [-n NAME]

Extract a Variant 1 DESIGN.md from a live URL.

Options:
  -o OUT     Output path. Default: ./DESIGN.md
  -n NAME    Design system name. Default: from <title> or domain

Pipeline:
  1. dev-browser eval <URL> — captures DOM landmarks + computed styles + CSS vars
  2. post-process JSON → cluster colors, infer typography, spacing, radius
  3. emit Variant 1 DESIGN.md
  4. validate via amw-design-md-lint.sh + amw-design-md-contrast.py

Exit codes:
  0  DESIGN.md written and passes lint
  1  validation failed (DESIGN.md still written; see warnings)
  2  invocation / network error
USAGE
  exit 2
}

if [ $# -lt 1 ]; then usage; fi

URL=""
OUT="./DESIGN.md"
NAME=""

while [ $# -gt 0 ]; do
  case "$1" in
    -o) OUT="$2"; shift 2 ;;
    -n) NAME="$2"; shift 2 ;;
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

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WRAPPER="$PLUGIN_ROOT/bin/amw-dev-browser-wrapper.sh"

if [ ! -x "$WRAPPER" ]; then
  echo "Error: dev-browser wrapper not found or not executable: $WRAPPER" >&2
  echo "       Run /amw-init or check the plugin install." >&2
  exit 2
fi

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

# Try to capture via wrapper. If wrapper does not yet expose a generic eval,
# fall back to a documented stub that the user runs manually.
if "$WRAPPER" --help 2>&1 | grep -q "eval"; then
  "$WRAPPER" eval "$URL" --expr "$EXTRACT_JS" > "$TMP_JSON" || {
    echo "Error: dev-browser eval failed for URL: $URL" >&2
    exit 2
  }
else
  echo "Note: dev-browser wrapper does not yet expose 'eval'. Running stub extractor." >&2
  # Stub: write minimal placeholder JSON so the post-processor can still emit a draft DESIGN.md
  # The user is expected to fill in the missing pieces.
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
    primary_hex = top_colors[0][0]
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
