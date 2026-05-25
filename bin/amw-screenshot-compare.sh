#!/usr/bin/env bash
# amw-screenshot-compare.sh — perceptual image comparison via fcvvdp (CVVDP JOD).
#
# Used by: the batch9 screenshot-parity verification harness
# (bin/amw-verify-parity.sh) and any phase that must prove a reimplementation
# matches its source render.
#
# Wraps the `fcvvdp` binary (halidecx/fcvvdp, Apache-2.0 — a fast C/Zig
# implementation of Cambridge's CVVDP/ColorVideoVDP perceptual metric). fcvvdp
# reads two PNGs and emits a JOD (Just-Objectionable-Difference) score:
#
#   10.0       images are identical
#   9.0 – 10.0 barely visible difference
#   8.0 –  9.0 slight visible difference
#   7.0 –  8.0 noticeable but acceptable
#
# Strict-parity bars used by the harness: JOD ≥ 9.5 (token-identical style
# tests) · JOD ≥ 9.0 (technique reimplementations).
#
# NOTE: fcvvdp errors out if the two images differ in dimensions, so callers
# must render both at the SAME fixed viewport (not full-page). fcvvdp prints
# its JSON to stderr, so we capture 2>&1 and isolate the JSON object.
#
# Usage:
#   amw-screenshot-compare.sh <reference.png> <distorted.png> \
#       [--threshold JOD] [--model fhd] [--out DIR]
#
#   reference  = the source-side render (ground truth)
#   distorted  = my reimplementation's render
#   --threshold default 9.0; --model default fhd; --out writes score.json
#
# Exit: 0 = PASS (JOD ≥ threshold) · 1 = FAIL · 2 = bad args ·
#       3 = fcvvdp binary missing · 4 = fcvvdp run/parse error.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FCVVDP="${AMW_FCVVDP_BIN:-$REPO_ROOT/libs_dev/fcvvdp/zig-out/bin/fcvvdp}"

THRESHOLD="9.0"
MODEL="fhd"
OUT_DIR=""
REF=""
DIST=""

usage() {
  sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --threshold) THRESHOLD="${2:?--threshold needs a value}"; shift 2 ;;
    --model|-m)  MODEL="${2:?--model needs a value}"; shift 2 ;;
    --out)       OUT_DIR="${2:?--out needs a value}"; shift 2 ;;
    -h|--help)   usage; exit 0 ;;
    -*)          echo "ERROR: unknown option: $1" >&2; exit 2 ;;
    *)
      if [[ -z "$REF" ]]; then REF="$1"
      elif [[ -z "$DIST" ]]; then DIST="$1"
      else echo "ERROR: too many positional args" >&2; exit 2; fi
      shift ;;
  esac
done

[[ -n "$REF" && -n "$DIST" ]] || { usage; exit 2; }

if [[ ! -x "$FCVVDP" ]]; then
  cat >&2 <<EOF
ERROR: fcvvdp binary not found at: $FCVVDP
Build it (Apache-2.0, requires Zig 0.16.x):
  git clone --depth 1 --branch 0.3.0 https://github.com/halidecx/fcvvdp.git "$REPO_ROOT/libs_dev/fcvvdp"
  ( cd "$REPO_ROOT/libs_dev/fcvvdp" && zig build --release=fast )
Or point AMW_FCVVDP_BIN at an existing fcvvdp binary.
EOF
  exit 3
fi

for f in "$REF" "$DIST"; do
  [[ -f "$f" ]] || { echo "ERROR: file not found: $f" >&2; exit 2; }
done

# fcvvdp writes the banner AND the -j JSON to stderr; merge and isolate the JSON.
raw="$("$FCVVDP" -j -m "$MODEL" "$REF" "$DIST" 2>&1)" || {
  printf '%s\n' "$raw" >&2
  echo "ERROR: fcvvdp failed (dimension mismatch is the usual cause)." >&2
  exit 4
}

jod="$(printf '%s' "$raw" | python3 -c "import sys,json,re; t=sys.stdin.read(); m=re.search(r'\{.*\}', t, re.S); print(json.loads(m.group(0))['jod'])")" || {
  echo "ERROR: could not parse fcvvdp output:" >&2
  printf '%s\n' "$raw" >&2
  exit 4
}

if [[ -n "$OUT_DIR" ]]; then
  mkdir -p "$OUT_DIR"
  printf '%s' "$raw" | python3 -c "import sys,re; t=sys.stdin.read(); m=re.search(r'\{.*\}', t, re.S); sys.stdout.write(m.group(0) if m else '{}')" > "$OUT_DIR/score.json"
fi

verdict="$(awk -v j="$jod" -v t="$THRESHOLD" 'BEGIN{print (j>=t)?"PASS":"FAIL"}')"
printf 'JOD %.4f  threshold %.2f  → %s\n' "$jod" "$THRESHOLD" "$verdict"
[[ "$verdict" == "PASS" ]]
