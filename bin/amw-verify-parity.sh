#!/usr/bin/env bash
# amw-verify-parity.sh — screenshot-parity verification harness.
#
# The per-item orchestrator for the batch9 acceptance test: render the SOURCE
# sample and MY reimplementation at identical fixed viewports, then compare
# each pair with fcvvdp (CVVDP perceptual JOD) via amw-screenshot-compare.sh.
# Writes a per-item report under reports/batch9-verification/<ts>/<id>/.
#
# Renders use a FIXED viewport (NOT --full-page) so both images share exact
# dimensions — fcvvdp errors on dimension mismatch. Source/mine may be a URL,
# an absolute path, or a relative path (turned into a file:// URL).
#
# For INTERACTIVE (I-class) items, run this twice with distinct render targets:
# once for the "before" state and once for the "after" state (e.g. a URL that
# auto-applies the interaction, or a pre-captured snapshot). Same for themes:
# call once per theme with light/dark variants of the targets.
#
# Usage:
#   amw-verify-parity.sh --id <item-id> --source <url|path> --mine <url|path> \
#       [--threshold JOD] [--viewports "1440x900,375x812"] [--out DIR] [--label TAG]
#
# Exit: 0 = all viewport pairs PASS · 1 = at least one FAIL ·
#       2 = bad args · 3 = dev-browser missing.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPARE="$SCRIPT_DIR/amw-screenshot-compare.sh"

ID="item"
SOURCE=""
MINE=""
THRESHOLD="9.0"
VIEWPORTS="1440x900,375x812"
OUT_DIR=""
LABEL=""

usage() { sed -n '2,28p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)        ID="${2:?}"; shift 2 ;;
    --source)    SOURCE="${2:?}"; shift 2 ;;
    --mine)      MINE="${2:?}"; shift 2 ;;
    --threshold) THRESHOLD="${2:?}"; shift 2 ;;
    --viewports) VIEWPORTS="${2:?}"; shift 2 ;;
    --out)       OUT_DIR="${2:?}"; shift 2 ;;
    --label)     LABEL="${2:?}"; shift 2 ;;
    -h|--help)   usage; exit 0 ;;
    *) echo "ERROR: unknown arg: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$SOURCE" && -n "$MINE" ]] || { usage; exit 2; }

if ! command -v dev-browser >/dev/null 2>&1; then
  cat >&2 <<EOF
ERROR: dev-browser CLI not found on PATH.
  Install with:  /amw-init   (the manual equivalent is a global npm install of
  the dev-browser package, then its one-time install sub-command).
EOF
  exit 3
fi

# Resolve the main-repo root (worktree-safe) for the report path.
MAIN_ROOT="$(git -C "$REPO_ROOT" worktree list 2>/dev/null | head -n1 | awk '{print $1}')"
[[ -n "$MAIN_ROOT" ]] || MAIN_ROOT="$REPO_ROOT"
TS="$(date +%Y%m%d_%H%M%S%z)"
OUT_DIR="${OUT_DIR:-$MAIN_ROOT/reports/batch9-verification/$TS/$ID}"
mkdir -p "$OUT_DIR"

# Turn a URL / abs path / rel path into a URL dev-browser accepts.
to_url() {
  local t="$1"
  case "$t" in
    http://*|https://*|file://*) printf '%s' "$t" ;;
    /*) printf 'file://%s' "$t" ;;
    *) printf 'file://%s/%s' "$(cd "$(dirname "$t")" && pwd)" "$(basename "$t")" ;;
  esac
}

render() { # url, w, h, outpng
  # dev-browser runs QuickJS sandbox scripts whose pages are full Playwright
  # objects. page.screenshot() defaults to viewport-only (fixed W×H), which is
  # exactly what fcvvdp needs (it errors on dimension mismatch). The sandbox can
  # only write under ~/.dev-browser/tmp via saveScreenshot(); we read the saved
  # path off stdout and copy it to the requested output.
  local url="$1" w="$2" h="$3" out="$4"
  local name="amw-parity-$$-${RANDOM}.png"
  local script; script="$(mktemp -t amw-render-XXXXXX.js)"
  cat > "$script" <<JS
const page = await browser.newPage();
await page.setViewportSize({ width: $w, height: $h });
await page.goto("$url", { waitUntil: "networkidle", timeout: ${DB_TIMEOUT_MS:-15000} });
try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}
await new Promise((r) => setTimeout(r, 500));
const p = await saveScreenshot(await page.screenshot(), "$name");
console.log(p);
JS
  local saved
  saved="$(dev-browser --headless --timeout 60 run "$script" 2>/dev/null | tail -1)"
  rm -f "$script"
  [[ -n "$saved" && -f "$saved" ]] || { echo "ERROR: render failed for $url" >&2; return 1; }
  cp "$saved" "$out"
}

src_url="$(to_url "$SOURCE")"
mine_url="$(to_url "$MINE")"

verdict="$OUT_DIR/verdict.md"
{
  echo "# Parity verdict — $ID${LABEL:+ ($LABEL)}"
  echo ""
  echo "- source: \`$SOURCE\`"
  echo "- mine:   \`$MINE\`"
  echo "- threshold: JOD ≥ $THRESHOLD"
  echo ""
  echo "| viewport | JOD | result |"
  echo "|---|---|---|"
} > "$verdict"

overall=0
IFS=',' read -ra VPS <<< "$VIEWPORTS"
for vp in "${VPS[@]}"; do
  w="${vp%x*}"; h="${vp#*x}"
  s="$OUT_DIR/source-$vp.png"
  m="$OUT_DIR/mine-$vp.png"
  render "$src_url" "$w" "$h" "$s"
  render "$mine_url" "$w" "$h" "$m"

  vpdir="$OUT_DIR/$vp"
  if line="$("$COMPARE" "$s" "$m" --threshold "$THRESHOLD" --out "$vpdir" 2>&1)"; then
    res="PASS"
  else
    rc=$?
    if [[ "$rc" == "1" ]]; then res="FAIL"; else res="ERROR"; fi
    overall=1
  fi
  jod="$(printf '%s' "$line" | grep -oE 'JOD [0-9.]+' | awk '{print $2}' | head -1)"
  # printf with %s placeholders (not echo interpolation): tool-derived values are
  # individually quoted arguments — no word-splitting/glob risk, and no echo
  # flag/escape ambiguity if a value ever starts with '-' or contains '\'.
  printf '| %s | %s | %s |\n' "$vp" "${jod:-?}" "$res" >> "$verdict"
  echo "→ $ID $vp: ${jod:-?} ($res)" >&2
done

echo "report: $verdict"
exit "$overall"
