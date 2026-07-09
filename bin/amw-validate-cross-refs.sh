#!/usr/bin/env bash
# author: emasoft
# license: MIT
#
# amw-validate-cross-refs.sh — verify every cited path inside the
# `Cross-references` section of `skills/**/SKILL.md` and `agents/*.md` files
# resolves on disk. Catches orphan-link rot before it reaches users.
#
# Usage:
#   bash bin/amw-validate-cross-refs.sh           # report broken refs, always exit 0
#   bash bin/amw-validate-cross-refs.sh --strict  # exit 1 if any refs are broken
#
# Behavior:
#   - Walks every `*.md` under `skills/` (recursive) and `agents/`.
#   - Locates a `## Cross-references` (or `### Cross-references`) heading and
#     scans the block until the next top-level heading or EOF.
#   - Within that block, extracts every backtick-quoted relative path AND every
#     `[label](relative/path)` markdown link target.
#   - Skips URLs (http://, https://) and slash-command tokens (/amw-…).
#   - Resolves each remaining path relative to the source file's directory.
#   - Reports any non-existent path as `MISSING: <source>:<line> -> <path>`.
#   - Always emits a final summary line.
#
# Exit codes:
#   0 — clean run (or non-strict mode regardless of findings)
#   1 — broken refs found AND --strict was passed
#   2 — invocation error

set -u

STRICT=0
if [ "$#" -gt 0 ]; then
  case "$1" in
    --strict) STRICT=1; shift ;;
    -h|--help)
      sed -n '4,21p' "$0" >&2
      exit 2
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
fi

# Find the plugin root by walking up from this script.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ ! -d "$PLUGIN_ROOT/skills" ] && [ ! -d "$PLUGIN_ROOT/agents" ]; then
  printf 'ERROR: cannot find skills/ or agents/ under %s\n' "$PLUGIN_ROOT" >&2
  exit 2
fi

CHECKED=0
BROKEN=0

# Process one markdown file: emit MISSING lines for any unresolvable cross-ref.
process_file() {
  local file="$1"
  CHECKED=$((CHECKED + 1))

  local source_dir
  source_dir="$(dirname "$file")"

  # Use awk to extract the cross-reference block (line numbers + content).
  # The block starts at a heading whose text contains "Cross-references" /
  # "Cross-Reference" / "References" (case-insensitive, allowing leading "##" or
  # "###") and ends at the next "^# " or "^## " heading.
  awk '
    BEGIN { in_block = 0 }
    /^#{2,3}[[:space:]]+([Cc]ross[-[:space:]]?[Rr]eference|[Cc]ross[-[:space:]]?[Rr]eferences)[[:space:]]*$/ {
      in_block = 1
      next
    }
    in_block && /^#{1,3}[[:space:]]/ { in_block = 0 }
    in_block { printf "%d\t%s\n", NR, $0 }
  ' "$file" | while IFS=$'\t' read -r lineno content; do
    [ -z "$content" ] && continue

    # Blockquote annotation lines (`>`-prefixed) are auto-generated doc-TOC
    # mirrors (e.g. "> What it does · … · Paths (configurable in
    # `hyperframes.json`) · …"), NOT the authoritative cross-reference list. A
    # backtick-wrapped word inside one is prose (often a runtime filename like
    # `hyperframes.json`), not a repo ref — extracting it produces a false
    # MISSING. Real refs live in the `-` / `[label](target)` bullets, so skip
    # ONLY the backtick scan on `>` lines; the markdown-link scan below still
    # runs on every line and would still catch a genuine broken link there.
    stripped_lead="$(printf '%s' "$content" | sed -E 's/^[[:space:]]+//')"
    case "$stripped_lead" in
      '>'*) ;;  # blockquote annotation — skip backtick extraction
      *)
        # Extract backtick-quoted paths (Python-free, portable grep -oE).
        # The single-quoted regex / sed scripts contain LITERAL backticks;
        # shellcheck disable=SC2016
        printf '%s\n' "$content" | \
          grep -oE '`[^`]+`' 2>/dev/null | \
          sed 's/^`//; s/`$//' | \
          while IFS= read -r ref; do
            emit_check "$file" "$lineno" "$source_dir" "$ref"
          done
        ;;
    esac

    # Then the markdown link targets [label](target).
    printf '%s\n' "$content" | \
      grep -oE '\[[^]]*\]\([^)]+\)' 2>/dev/null | \
      sed -E 's/^\[[^]]*\]\(([^)]+)\)/\1/' | \
      while IFS= read -r ref; do
        emit_check "$file" "$lineno" "$source_dir" "$ref"
      done
  done
}

# emit_check: decide whether `ref` should be checked, and if so, whether it
# resolves on disk. Output a MISSING line if not.
emit_check() {
  local file="$1"
  local lineno="$2"
  local source_dir="$3"
  local ref="$4"

  # Strip a trailing fragment / anchor / query.
  ref="${ref%%#*}"
  ref="${ref%%\?*}"

  # Strip surrounding whitespace.
  ref="$(printf '%s' "$ref" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
  [ -z "$ref" ] && return

  # Skip URLs.
  case "$ref" in
    http://*|https://*|mailto:*|ftp://*) return ;;
  esac

  # Skip slash-command tokens.
  case "$ref" in
    /amw-*) return ;;
  esac

  # Skip template-placeholder paths — refs containing `{…}` (or `<…>`) are
  # documentation templates (e.g. `.infographic/{project}.json`,
  # `out/{slug}.svg`), not concrete on-disk paths, so a literal existence
  # check is meaningless and always reports a false "MISSING".
  case "$ref" in
    *'{'*|*'}'*|*'<'*|*'>'*) return ;;
  esac

  # Skip PROVENANCE references into the build-time distillation dirs. Skills
  # carry `source:` frontmatter and "distilled from" cross-refs pointing at the
  # gitignored `reports_dev/…` / `reports/batch…` inputs they were harvested
  # from (the amw-skill-drift-audit skill consumes these pins to audit drift
  # against upstream). Those inputs are intentionally NOT shipped in the plugin,
  # so an on-disk existence check always false-reports them as MISSING.
  case "$ref" in
    reports_dev/*|*/reports_dev/*|reports/batch*|*/reports/batch*) return ;;
  esac

  # Skip glob-pattern refs (e.g. `brand-*.md`) — a literal existence check on a
  # wildcard path is meaningless; the `*` marks a documented FAMILY of files,
  # not one concrete path.
  case "$ref" in
    *'*'*) return ;;
  esac

  # Skip refs that look like inline-code language tokens or shell flags
  # (`bash`, `python3`, `--strict`, etc.). Heuristic: must contain '/' or '.' or
  # start with '~'.
  # NOTE: `*/*` already covers the home-relative `~/*` case (any path with a
  # slash matches `*/*` first), so we drop the redundant `~/*` glob — keeps
  # the linter (SC2221/SC2222) clean. Tilde-prefixed paths still match via
  # the leading `*/*` because they all contain at least one slash.
  case "$ref" in
    */*|*.md|*.py|*.sh|*.mjs|*.ts|*.tsx|*.html|*.json|*.yaml|*.css|*.svg|*.png|*.jpg|*.txt|*.pdf|*.mmd) ;;
    *) return ;;
  esac

  # Resolve. Allow leading `./`, `../`, or absolute.
  #
  # Relative refs may be written EITHER relative to the source file's own
  # directory OR relative to the plugin root. The plugin-root convention is
  # the dominant one in this repo for citing `bin/…`, `tests/…`, `skills/…`,
  # and `agents/…` paths from deeply-nested reference files (≈1083 root-
  # relative refs vs ≈43 `../`-style). Accept either: try the source dir
  # first, then fall back to the plugin root before declaring a ref MISSING.
  # Without this, every root-relative `bin/…` ref cited from a nested file is
  # a false positive (it resolves at the root but not beside its citing file).
  local resolved
  case "$ref" in
    /*) resolved="$ref" ;;
    ~/*) resolved="$HOME/${ref#~/}" ;;
    *)
      if [ -e "$source_dir/$ref" ]; then
        resolved="$source_dir/$ref"
      else
        resolved="$PLUGIN_ROOT/$ref"
      fi
      ;;
  esac

  if [ ! -e "$resolved" ]; then
    # Path is recorded relative to plugin root for legibility.
    # Quote the parameter expansion so glob-pattern matching (the default
    # behaviour of `${var#pattern}`) does not accidentally treat magic
    # characters in $PLUGIN_ROOT as wildcards (SC2295).
    local rel_source="${file#"$PLUGIN_ROOT"/}"
    printf 'MISSING: %s:%s -> %s\n' "$rel_source" "$lineno" "$ref"
    BROKEN=$((BROKEN + 1))
    # Persist BROKEN across the subshell via a temp file.
    printf '1\n' >>"$BROKEN_FILE"
  fi
}

# A subshell is created by the `while IFS=` pipeline above, so we have to
# persist the BROKEN counter via a temp file.
BROKEN_FILE="$(mktemp -t amw-xref-broken.XXXXXX)"
trap 'rm -f "$BROKEN_FILE"' EXIT INT TERM
: >"$BROKEN_FILE"

# Walk the markdown files.
if [ -d "$PLUGIN_ROOT/skills" ]; then
  while IFS= read -r f; do
    process_file "$f"
  done < <(find "$PLUGIN_ROOT/skills" -type f -name '*.md' -print)
fi

if [ -d "$PLUGIN_ROOT/agents" ]; then
  while IFS= read -r f; do
    process_file "$f"
  done < <(find "$PLUGIN_ROOT/agents" -type f -name '*.md' -print)
fi

# Count broken refs from the temp file.
if [ -s "$BROKEN_FILE" ]; then
  BROKEN="$(wc -l <"$BROKEN_FILE" | tr -d ' ')"
else
  BROKEN=0
fi

printf 'Checked %s files, found %s broken references.\n' "$CHECKED" "$BROKEN"

if [ "$BROKEN" -gt 0 ] && [ "$STRICT" -eq 1 ]; then
  exit 1
fi
exit 0
