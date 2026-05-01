#!/usr/bin/env bash
# amw-freeze-phase-a.sh — Aggregate Phase A artifacts into a canonical
# phase-a-frozen-spec.json that every Phase B sub-agent reads.
#
# Implements P1-1 from reports/audit/architecture-deep-audit/CONSOLIDATED-fix-plan.md.
# The "Phase A.5 Spec Freeze" replaces "main-agent paraphrases YAML headers
# in 9 input contracts" with "9 sub-agents read 1 small JSON". Saves ~30K
# orchestrator tokens per multi-artifact workflow.
#
# Producer: ai-maestro-webdesign-main-agent (only).
# Consumers: every Phase B sub-agent (each reads only the keys it needs).
#
# Usage:
#   bash bin/amw-freeze-phase-a.sh \
#     --approved-ascii  <abs-path>     [REQUIRED]
#     --brand-tokens    <abs-path>     [REQUIRED]
#     --design-md       <abs-path>     [REQUIRED]
#     --ia              <abs-path>     [REQUIRED]
#     --copy            <abs-path>     [optional — skip when single-locale]
#     --legal           <abs-path>     [optional — skip when no regulatory reqs]
#     --seo-head        <abs-path>     [optional — skip when SEO not in scope]
#     --personas        <abs-path>     [optional — skip when no user-research]
#     --target-stack    <string>       [REQUIRED]
#     --locales         <comma-list>   [REQUIRED]
#     --output-dir      <abs-path>     [REQUIRED]
#     --wcag-target     <AA|AAA>       [REQUIRED]
#     --out             <abs-path>     [REQUIRED — destination JSON path]
#
# Exit codes:
#   0  spec written
#   1  missing required input file (path does not exist)
#   2  invocation / argument error
#
# Header conventions: pure bash + standard utilities (shasum, python3 for
# realpath portability, date with %z). No Python script files. macOS + Linux.
#
# author: emasoft
# license: MIT

set -euo pipefail

usage() {
  cat <<USAGE
Usage: bash bin/amw-freeze-phase-a.sh [REQUIRED FLAGS] [OPTIONAL FLAGS]

Required:
  --approved-ascii <path>   ASCII variant the user approved at the satisfaction gate
  --brand-tokens <path>     Token JSON from amw-brand-researcher-agent
  --design-md <path>        DESIGN.md from author/extractor agents (or user-supplied)
  --ia <path>               IA / page-structure JSON
  --target-stack <string>   e.g. "shadcn+next", "vanilla-html", "astro"
  --locales <comma-list>    e.g. "en" or "en,fr,de"
  --output-dir <path>       Directory where Phase B agents write their artifacts
  --wcag-target <AA|AAA>    Accessibility target
  --out <path>              Where to write the frozen-spec JSON

Optional (omit when domain not in scope):
  --copy <path>       copy_blocks JSON (skip when single-locale or copy is inline)
  --legal <path>      legal mandatory-elements HTML/JSON (skip when no regulatory reqs)
  --seo-head <path>   SEO head fragments JSON (skip when SEO not in scope)
  --personas <path>   user-research personas markdown (skip when no research provided)

Behavior:
  1. Validate every passed --<x> <path> flag points to an existing file/dir.
  2. Compute sha256 of the approved-ascii file.
  3. Compose JSON with absolute paths and ISO-8601 frozen_at timestamp.
  4. Write to --out (mkdir -p the parent).
  5. Echo the absolute output path on stdout for the orchestrator.
USAGE
  exit 2
}

if [ $# -eq 0 ]; then usage; fi

APPROVED_ASCII=""
BRAND_TOKENS=""
DESIGN_MD=""
IA=""
COPY=""
LEGAL=""
SEO_HEAD=""
PERSONAS=""
TARGET_STACK=""
LOCALES=""
OUTPUT_DIR=""
WCAG_TARGET=""
OUT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --approved-ascii) APPROVED_ASCII="$2"; shift 2 ;;
    --brand-tokens)   BRAND_TOKENS="$2";   shift 2 ;;
    --design-md)      DESIGN_MD="$2";      shift 2 ;;
    --ia)             IA="$2";             shift 2 ;;
    --copy)           COPY="$2";           shift 2 ;;
    --legal)          LEGAL="$2";          shift 2 ;;
    --seo-head)       SEO_HEAD="$2";       shift 2 ;;
    --personas)       PERSONAS="$2";       shift 2 ;;
    --target-stack)   TARGET_STACK="$2";   shift 2 ;;
    --locales)        LOCALES="$2";        shift 2 ;;
    --output-dir)     OUTPUT_DIR="$2";     shift 2 ;;
    --wcag-target)    WCAG_TARGET="$2";    shift 2 ;;
    --out)            OUT="$2";            shift 2 ;;
    -h|--help)        usage ;;
    *) echo "ERROR: unknown flag: $1" >&2; usage ;;
  esac
done

# Validate required scalar arguments
for pair in \
    "approved-ascii:$APPROVED_ASCII" \
    "brand-tokens:$BRAND_TOKENS" \
    "design-md:$DESIGN_MD" \
    "ia:$IA" \
    "target-stack:$TARGET_STACK" \
    "locales:$LOCALES" \
    "output-dir:$OUTPUT_DIR" \
    "wcag-target:$WCAG_TARGET" \
    "out:$OUT"; do
  flag="${pair%%:*}"
  val="${pair#*:}"
  if [ -z "$val" ]; then
    echo "ERROR: --$flag is required" >&2
    exit 2
  fi
done

if [ "$WCAG_TARGET" != "AA" ] && [ "$WCAG_TARGET" != "AAA" ]; then
  echo "ERROR: --wcag-target must be AA or AAA (got '$WCAG_TARGET')" >&2
  exit 2
fi

# Validate file/dir existence for every passed path
check_path_exists() {
  local flag="$1"; local val="$2"; local kind="$3"  # kind=file|dir
  if [ -z "$val" ]; then return 0; fi
  if [ "$kind" = "dir" ]; then
    if [ ! -d "$val" ]; then echo "MISSING: --$flag $val" >&2; exit 1; fi
  else
    if [ ! -f "$val" ]; then echo "MISSING: --$flag $val" >&2; exit 1; fi
  fi
}

check_path_exists "approved-ascii" "$APPROVED_ASCII" "file"
check_path_exists "brand-tokens"   "$BRAND_TOKENS"   "file"
check_path_exists "design-md"      "$DESIGN_MD"      "file"
check_path_exists "ia"             "$IA"             "file"
# output-dir is the directory where Phase B will write; create it if absent
mkdir -p "$OUTPUT_DIR"
check_path_exists "output-dir"     "$OUTPUT_DIR"     "dir"
check_path_exists "copy"           "$COPY"           "file"
check_path_exists "legal"          "$LEGAL"          "file"
check_path_exists "seo-head"       "$SEO_HEAD"       "file"
check_path_exists "personas"       "$PERSONAS"       "file"

# Portable absolute-path resolution (macOS lacks GNU realpath out of the box)
abs() {
  local p="$1"
  if [ -z "$p" ]; then echo ""; return 0; fi
  python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$p"
}

APPROVED_ASCII_ABS="$(abs "$APPROVED_ASCII")"
BRAND_TOKENS_ABS="$(abs "$BRAND_TOKENS")"
DESIGN_MD_ABS="$(abs "$DESIGN_MD")"
IA_ABS="$(abs "$IA")"
COPY_ABS="$(abs "$COPY")"
LEGAL_ABS="$(abs "$LEGAL")"
SEO_HEAD_ABS="$(abs "$SEO_HEAD")"
PERSONAS_ABS="$(abs "$PERSONAS")"
OUTPUT_DIR_ABS="$(abs "$OUTPUT_DIR")"
OUT_ABS="$(abs "$OUT")"

# Compute sha256 of approved ASCII file
ASCII_SHA="$(shasum -a 256 "$APPROVED_ASCII_ABS" | awk '{print $1}')"

# Format ISO-8601 timestamp with offset (e.g. 2026-04-30T18:30:12+0200)
FROZEN_AT="$(date "+%Y-%m-%dT%H:%M:%S%z")"

# Convert comma-separated locales to a JSON array via python3 (handles
# trimming, quoting, and escapes correctly)
LOCALES_JSON="$(python3 -c '
import json, sys
parts = [p.strip() for p in sys.argv[1].split(",") if p.strip()]
print(json.dumps(parts))
' "$LOCALES")"

# Compose the JSON via python3 to ensure correct quoting / null handling.
# Optional fields become JSON null when not provided; required are strings.
mkdir -p "$(dirname "$OUT_ABS")"

python3 - "$OUT_ABS" <<PYEOF
import json, sys

out_path = sys.argv[1]

def opt(s):
    return s if s else None

spec = {
    "frozen_at": "${FROZEN_AT}",
    "frozen_spec_version": "1",
    "approved_ascii_path": "${APPROVED_ASCII_ABS}",
    "approved_ascii_sha256": "${ASCII_SHA}",
    "brand_tokens_path": "${BRAND_TOKENS_ABS}",
    "design_md_path": "${DESIGN_MD_ABS}",
    "ia_structure_path": "${IA_ABS}",
    "copy_blocks_path": opt("${COPY_ABS}"),
    "legal_mandatory_elements_path": opt("${LEGAL_ABS}"),
    "seo_head_path": opt("${SEO_HEAD_ABS}"),
    "personas_path": opt("${PERSONAS_ABS}"),
    "target_stack": "${TARGET_STACK}",
    "locales": ${LOCALES_JSON},
    "output_dir": "${OUTPUT_DIR_ABS}",
    "wcag_target": "${WCAG_TARGET}",
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)
    f.write("\n")
PYEOF

# Echo absolute output path on stdout for orchestrator capture
echo "$OUT_ABS"
exit 0
