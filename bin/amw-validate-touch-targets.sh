#!/usr/bin/env bash
# author: emasoft
# license: MIT
#
# amw-validate-touch-targets.sh — CI gate that scans TSX/JSX/TS/JS files for
# touch-target dimensions smaller than the platform minimums:
#   - iOS Human Interface Guidelines:    44 pt minimum (any axis)
#   - Android Material Design (M3):      48 dp minimum (any axis)
#   - WCAG 2.5.5 Target Size (AAA):      44 CSS px minimum
#   - WCAG 2.5.8 Target Size Minimum:    24 CSS px hard floor (warn only)
#
# Detection is GREP-based, not AST-based — fast, no browser, no deps.
# It catches the common authoring mistakes:
#   - inline-style `width: 32px` / `height: 32px`
#   - Tailwind `w-8` / `h-8` (= 32px) on interactive elements
#   - `<button>` / `<a>` / `[role=button]` / `[onClick]` near small-size classes
#
# Usage:
#   bash bin/amw-validate-touch-targets.sh                       # scan src/ + app/ + components/ (auto-detect), exit 0/1
#   bash bin/amw-validate-touch-targets.sh <path> [<path> ...]   # scan explicit paths
#   bash bin/amw-validate-touch-targets.sh --strict              # exit 1 on first violation (CI mode)
#   bash bin/amw-validate-touch-targets.sh --json                # emit JSON findings to stdout
#   bash bin/amw-validate-touch-targets.sh --help                # this help
#
# Output format (default human-readable):
#   file:line — <pattern> (suggested fix: <suggestion>)
#
# Exit codes:
#   0 — clean run; zero violations
#   1 — at least one violation found
#   2 — invocation error (bad arguments, no scan paths)

set -u

STRICT=0
JSON=0
PATHS=()

usage() {
  sed -n '4,33p' "$0" >&2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --strict) STRICT=1; shift ;;
    --json)   JSON=1; shift ;;
    -h|--help) usage; exit 2 ;;
    --) shift; while [ "$#" -gt 0 ]; do PATHS+=("$1"); shift; done ;;
    -*) printf 'Unknown flag: %s\n' "$1" >&2; usage; exit 2 ;;
    *)  PATHS+=("$1"); shift ;;
  esac
done

# Auto-detect default scan paths if none supplied.
if [ "${#PATHS[@]}" -eq 0 ]; then
  for d in src app components; do
    if [ -d "$d" ]; then PATHS+=("$d"); fi
  done
fi

if [ "${#PATHS[@]}" -eq 0 ]; then
  printf 'No scan paths and no src/, app/, or components/ directory found.\n' >&2
  exit 2
fi

# Patterns to catch. Each line is: <regex>|<dimension>|<unit>|<suggestion>
# Numeric extraction is done in awk after grep matches.
# We look at sizes below 44 for iOS / WCAG 2.5.5 and 48 for Android (M3).
# A hit on any size <44px on a button/link/role=button is a violation;
# a hit on 24–43px is a WARN (still flagged); <24px is a hard error.
#
# We grep for:
#   1. inline-style width/height in px
#   2. Tailwind w-N / h-N where N corresponds to <44px (w-1..w-10 = 4..40px)
#   3. CSS rules `width: Npx` / `height: Npx` within style props
#   4. min-width / min-height with same numeric ranges

VIOLATIONS=0
TMP="$(mktemp -t amw-touch-targets-XXXXXX)"
trap 'rm -f "$TMP"' EXIT

# Helper: emit one finding line.
emit() {
  # args: file line pattern suggestion
  if [ "$JSON" -eq 1 ]; then
    printf '{"file":"%s","line":%s,"pattern":"%s","suggestion":"%s"}\n' \
      "$1" "$2" "$3" "$4" >>"$TMP"
  else
    printf '%s:%s — %s (suggested fix: %s)\n' "$1" "$2" "$3" "$4" >>"$TMP"
  fi
  VIOLATIONS=$((VIOLATIONS + 1))
}

# Scan for inline-style width:Npx or height:Npx where N < 44.
# Limitation: pure grep cannot evaluate "N < 44" numerically; we use awk on
# the matched lines and extract the value.
scan_inline_px() {
  local file="$1"
  # Use grep to find candidate lines (faster than reading the whole file in awk).
  # Match: width:Npx, width: Npx, height:Npx, height: Npx (case-insensitive).
  grep -nE '(width|height)[[:space:]]*:[[:space:]]*[0-9]+px' "$file" 2>/dev/null \
    | while IFS=: read -r linenum rest; do
        # Extract every "(width|height): Npx" occurrence in the line.
        # Use awk to evaluate the numeric value.
        echo "$rest" | awk -v F="$file" -v L="$linenum" '
          {
            # Walk the line and find all width/height:Npx occurrences.
            # Use a regex sub-loop via match() with a saved index.
            line = $0
            while (match(line, /(width|height)[[:space:]]*:[[:space:]]*([0-9]+)px/)) {
              # Save outer match bounds BEFORE calling inner match() which would clobber
              # RSTART and RLENGTH.
              outer_rstart = RSTART
              outer_rlen   = RLENGTH
              dim = substr(line, outer_rstart, outer_rlen)
              # Parse the numeric value out of the matched substring.
              numstart = match(dim, /[0-9]+/)
              if (numstart > 0) {
                numlen = RLENGTH
                n = substr(dim, numstart, numlen) + 0
                if (n < 44) {
                  if (n < 24) {
                    printf "EMIT|%s|%s|inline %s|enlarge to at least 44px (24px hard floor; WCAG 2.5.8)\n", F, L, dim
                  } else {
                    printf "EMIT|%s|%s|inline %s|enlarge to at least 44px (iOS HIG / WCAG 2.5.5 AAA)\n", F, L, dim
                  }
                }
              }
              # Advance past this match using the saved outer bounds.
              line = substr(line, outer_rstart + outer_rlen)
            }
          }
        '
      done
}

# Scan for Tailwind w-N / h-N classes where N corresponds to < 11 (= 44px).
# Tailwind unit: 1 = 4px, 2 = 8px, ... 10 = 40px, 11 = 44px, 12 = 48px.
# We flag w-1..w-10 and h-1..h-10 occurring on the same line as button|link|onClick|role=button.
scan_tailwind() {
  local file="$1"
  # Find lines containing both an interactive element and a small w-N/h-N class.
  grep -nE 'w-([1-9]|10)[^0-9]|h-([1-9]|10)[^0-9]' "$file" 2>/dev/null \
    | while IFS=: read -r linenum rest; do
        # Check if the line also looks interactive.
        if echo "$rest" | grep -qiE '(<button|<a |role=("|.)button|onClick|<input|<select|<textarea)'; then
          # Extract the offending class.
          match="$(echo "$rest" | grep -oE '[wh]-([1-9]|10)' | head -n1)"
          if [ -z "$match" ]; then match="w-?"; fi
          # Compute pixel size for the suggestion.
          n="$(echo "$match" | grep -oE '[0-9]+')"
          px=$((n * 4))
          if [ "$px" -lt 24 ]; then
            echo "EMIT|$file|$linenum|tailwind $match (= ${px}px) on interactive element|use w-11/h-11 (44px) minimum; WCAG 2.5.8 24px hard floor"
          else
            echo "EMIT|$file|$linenum|tailwind $match (= ${px}px) on interactive element|use w-11/h-11 (44px) minimum; iOS HIG / WCAG 2.5.5 AAA"
          fi
        fi
      done
}

# Walk the scan paths.
for p in "${PATHS[@]}"; do
  if [ ! -e "$p" ]; then
    printf 'Path does not exist, skipping: %s\n' "$p" >&2
    continue
  fi
  # Find candidate files.
  while IFS= read -r -d '' f; do
    # Inline px scan.
    while IFS='|' read -r tag fname fline fpat fsugg; do
      [ "$tag" = "EMIT" ] || continue
      emit "$fname" "$fline" "$fpat" "$fsugg"
      if [ "$STRICT" -eq 1 ]; then break 3; fi
    done < <(scan_inline_px "$f")
    # Tailwind class scan.
    while IFS='|' read -r tag fname fline fpat fsugg; do
      [ "$tag" = "EMIT" ] || continue
      emit "$fname" "$fline" "$fpat" "$fsugg"
      if [ "$STRICT" -eq 1 ]; then break 3; fi
    done < <(scan_tailwind "$f")
  done < <(find "$p" \( -name '*.tsx' -o -name '*.jsx' -o -name '*.ts' -o -name '*.js' \) -type f -print0 2>/dev/null)
done

# Emit findings.
if [ "$JSON" -eq 1 ]; then
  printf '[\n'
  if [ -s "$TMP" ]; then
    # Comma-separate the JSON lines (each is a complete object).
    awk 'NR>1{printf ",\n"} {printf "  %s", $0}' "$TMP"
    printf '\n'
  fi
  printf ']\n'
else
  if [ "$VIOLATIONS" -gt 0 ]; then
    cat "$TMP"
    printf '\n%d touch-target violation(s) found.\n' "$VIOLATIONS" >&2
  else
    printf 'OK: zero touch-target violations across %d scan path(s).\n' "${#PATHS[@]}" >&2
  fi
fi

if [ "$VIOLATIONS" -gt 0 ]; then
  exit 1
fi
exit 0
