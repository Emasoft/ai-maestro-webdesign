#!/usr/bin/env bash
# author: emasoft
# license: MIT (direct-port from design-specialist-agent's audit recipe)
#
# amw-html-design-grep-audit.sh — fast, grep-only design-system + a11y audit
# for HTML/JSX/TSX/Astro/Vue files. Six rule checks:
#
#   [DSP-001] Hardcoded color literals — hex (#abc, #aabbcc) or rgb(...)
#             outside of CSS custom properties or theme tokens.
#             Why: design tokens should be variables, not literals; literals
#             survive theme switches and produce stale palettes.
#
#   [DSP-002] Naked px spacing values — any `padding:` / `margin:` / `gap:`
#             with a literal Npx that does NOT come from a token / variable.
#             Why: spacing should snap to the 8pt grid via tokens, not be
#             freely typed.
#
#   [DSP-003] z-index > 100 — z-index values larger than two digits typically
#             mean the author is fighting stacking-context wars. Flag for
#             review (often fixable by re-rooting the layer in DOM order).
#
#   [A11Y-001] <img> without alt — every <img> must have an alt attribute
#              (even alt="" for decorative). Missing alt is a hard WCAG fail.
#
#   [A11Y-002] onClick / handler without keyboard equivalent — div / span /
#              other non-button elements with onClick but no onKeyDown or
#              role=button + tabIndex.
#              Why: keyboard users cannot reach mouse-only handlers.
#
#   [MOTION-001] No prefers-reduced-motion query — the file uses @keyframes
#                or transition: but does NOT include a
#                `@media (prefers-reduced-motion: reduce)` block.
#                Why: WCAG 2.3.3 (Animation from Interactions).
#
# Each violation is one line: `file:line — [rule-id] message`.
#
# Usage:
#   bash bin/amw-html-design-grep-audit.sh                   # scan src/ + app/ + components/ + public/
#   bash bin/amw-html-design-grep-audit.sh <path> [<path>]   # explicit paths
#   bash bin/amw-html-design-grep-audit.sh --rule DSP-001    # restrict to a single rule
#   bash bin/amw-html-design-grep-audit.sh --strict          # exit 1 on first violation
#   bash bin/amw-html-design-grep-audit.sh --help
#
# Exit codes:
#   0 — clean run; zero violations
#   1 — at least one violation found
#   2 — invocation error

set -u

ONLY_RULE=""
STRICT=0
PATHS=()

usage() {
  sed -n '4,49p' "$0" >&2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --rule)   ONLY_RULE="${2:-}"; shift 2 ;;
    --strict) STRICT=1; shift ;;
    -h|--help) usage; exit 2 ;;
    --) shift; while [ "$#" -gt 0 ]; do PATHS+=("$1"); shift; done ;;
    -*) printf 'Unknown flag: %s\n' "$1" >&2; usage; exit 2 ;;
    *)  PATHS+=("$1"); shift ;;
  esac
done

if [ "${#PATHS[@]}" -eq 0 ]; then
  for d in src app components public pages; do
    if [ -d "$d" ]; then PATHS+=("$d"); fi
  done
fi

if [ "${#PATHS[@]}" -eq 0 ]; then
  printf 'No scan paths and no default directories found.\n' >&2
  exit 2
fi

# Counter file (used instead of a shell var because each
# `grep | while read` pipeline runs in a subshell on macOS bash 3.x —
# incrementing a variable inside the subshell would be lost when the
# subshell exits).  Each violation appends one line.
COUNTER_FILE="$(mktemp -t amw-audit-counter-XXXXXX)"

# Helper: should we run this rule?
should_run() {
  if [ -z "$ONLY_RULE" ]; then return 0; fi
  if [ "$ONLY_RULE" = "$1" ]; then return 0; fi
  return 1
}

# Helper: record a violation (called from inside subshell loops).
record() {
  printf '1\n' >> "$COUNTER_FILE"
}

# Find all candidate files first.
FILES_TMP="$(mktemp -t amw-audit-files-XXXXXX)"
trap 'rm -f "$FILES_TMP" "$COUNTER_FILE"' EXIT
for p in "${PATHS[@]}"; do
  [ -e "$p" ] || continue
  find "$p" \( -name '*.html' -o -name '*.htm' -o -name '*.tsx' -o -name '*.jsx' \
              -o -name '*.ts' -o -name '*.js' -o -name '*.astro' -o -name '*.vue' \
              -o -name '*.css' -o -name '*.scss' -o -name '*.sass' \) \
            -type f -print 2>/dev/null
done > "$FILES_TMP"

# DSP-001: hex / rgb literals outside of token-variable form.
# We allow `var(--...)` and `theme(...)` wrappers; literals not enclosed
# in those are flagged.
if should_run "DSP-001"; then
  while IFS= read -r file; do
    grep -nE '(#[0-9a-fA-F]{3,8}\b|rgb\(|rgba\()' "$file" 2>/dev/null \
      | grep -vE '(var\(--|theme\(|hsl\(var|--[a-z]+:)' \
      | while IFS=: read -r ln rest; do
          # Skip CSS variable definitions (--color-primary: #abc) — those ARE tokens.
          if echo "$rest" | grep -qE '^\s*--[a-z]'; then continue; fi
          printf '%s:%s — [DSP-001] hardcoded color literal: %s\n' "$file" "$ln" "$(echo "$rest" | sed 's/^[[:space:]]*//' | cut -c1-80)"
          record
          if [ "$STRICT" -eq 1 ]; then exit 1; fi
        done
  done < "$FILES_TMP"
fi

# DSP-002: naked px spacing values in margin/padding/gap.
if should_run "DSP-002"; then
  while IFS= read -r file; do
    grep -nE '(padding|margin|gap)[[:space:]]*:[[:space:]]*[0-9]+px' "$file" 2>/dev/null \
      | grep -vE '(var\(--|theme\(|calc\()' \
      | while IFS=: read -r ln rest; do
          printf '%s:%s — [DSP-002] naked px spacing (not a token): %s\n' "$file" "$ln" "$(echo "$rest" | sed 's/^[[:space:]]*//' | cut -c1-80)"
          record
          if [ "$STRICT" -eq 1 ]; then exit 1; fi
        done
  done < "$FILES_TMP"
fi

# DSP-003: z-index > 100.
if should_run "DSP-003"; then
  while IFS= read -r file; do
    grep -nE 'z-index[[:space:]]*:[[:space:]]*[0-9]+' "$file" 2>/dev/null \
      | while IFS=: read -r ln rest; do
          val="$(echo "$rest" | grep -oE 'z-index[[:space:]]*:[[:space:]]*[0-9]+' | grep -oE '[0-9]+')"
          if [ -n "$val" ] && [ "$val" -gt 100 ]; then
            printf '%s:%s — [DSP-003] z-index > 100 (=%s): re-root the stacking context\n' "$file" "$ln" "$val"
            record
            if [ "$STRICT" -eq 1 ]; then exit 1; fi
          fi
        done
  done < "$FILES_TMP"
fi

# A11Y-001: <img> without alt.
if should_run "A11Y-001"; then
  while IFS= read -r file; do
    # Match <img ... > tags that do NOT contain alt= (case-insensitive).
    grep -nE '<img\b' "$file" 2>/dev/null \
      | while IFS=: read -r ln rest; do
          if ! echo "$rest" | grep -qiE '\balt[[:space:]]*='; then
            printf '%s:%s — [A11Y-001] <img> without alt attribute: %s\n' "$file" "$ln" "$(echo "$rest" | sed 's/^[[:space:]]*//' | cut -c1-80)"
            record
            if [ "$STRICT" -eq 1 ]; then exit 1; fi
          fi
        done
  done < "$FILES_TMP"
fi

# A11Y-002: onClick without keyboard equivalent on non-button elements.
if should_run "A11Y-002"; then
  while IFS= read -r file; do
    # Match lines with onClick (JSX) or onclick (HTML).
    grep -nE '(onClick|onclick)[[:space:]]*=' "$file" 2>/dev/null \
      | while IFS=: read -r ln rest; do
          # Skip if the line/element is a <button> or <a> or has role=button.
          if echo "$rest" | grep -qiE '(<button|<a[[:space:]]|<a$|role=("|.)button)'; then continue; fi
          # Skip if same line has onKeyDown / onKeyPress / onKeyUp.
          if echo "$rest" | grep -qiE 'onKey(Down|Press|Up)'; then continue; fi
          printf '%s:%s — [A11Y-002] onClick on non-button without keyboard handler: %s\n' "$file" "$ln" "$(echo "$rest" | sed 's/^[[:space:]]*//' | cut -c1-80)"
          record
          if [ "$STRICT" -eq 1 ]; then exit 1; fi
        done
  done < "$FILES_TMP"
fi

# MOTION-001: animation/transition without prefers-reduced-motion.
if should_run "MOTION-001"; then
  while IFS= read -r file; do
    # Only check files likely to contain motion (CSS-like or styled).
    case "$file" in
      *.css|*.scss|*.sass|*.html|*.htm|*.astro|*.vue|*.tsx|*.jsx) ;;
      *) continue ;;
    esac
    # Does the file use animation primitives?
    if grep -qE '@keyframes|transition[[:space:]]*:|animation[[:space:]]*:' "$file" 2>/dev/null; then
      # Does it ALSO have a prefers-reduced-motion query?
      if ! grep -qE 'prefers-reduced-motion' "$file" 2>/dev/null; then
        # Find first line with motion to report.
        ln="$(grep -nE '@keyframes|transition[[:space:]]*:|animation[[:space:]]*:' "$file" 2>/dev/null | head -n1 | cut -d: -f1)"
        if [ -z "$ln" ]; then ln=1; fi
        printf '%s:%s — [MOTION-001] motion primitives but no @media (prefers-reduced-motion: reduce) block\n' "$file" "$ln"
        record
        if [ "$STRICT" -eq 1 ]; then exit 1; fi
      fi
    fi
  done < "$FILES_TMP"
fi

VIOLATIONS=0
if [ -s "$COUNTER_FILE" ]; then
  VIOLATIONS="$(wc -l < "$COUNTER_FILE" | tr -d ' ')"
fi
if [ "$VIOLATIONS" -gt 0 ]; then
  printf '\n%d design/a11y violation(s) found.\n' "$VIOLATIONS" >&2
  exit 1
fi
printf 'OK: zero design/a11y violations across %d scan path(s).\n' "${#PATHS[@]}" >&2
exit 0
