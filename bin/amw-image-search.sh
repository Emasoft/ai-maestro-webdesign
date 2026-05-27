#!/usr/bin/env bash
# author: emasoft
# license: MIT
#
# amw-image-search.sh — clean-room wrapper around the Lummi free-stock-photo
# public API (https://www.lummi.ai). Resolves placeholder-image slots from an
# approved ASCII sketch BEFORE wireframe-builder renders production HTML, so
# Lorem-Picsum / placehold.co / placeholder.com URLs never ship.
#
# Lummi exposes a JSON search endpoint that returns CC0-licensed photographs
# matched by query string. The wrapper handles:
#   - URL-safe query encoding
#   - optional orientation, image type, luminance, and per-page filters
#   - optional API key (LUMMI_API_KEY env var) for higher rate limits
#   - --format=urls (default) | --format=json (raw API response)
#   - --count N to limit result set
#
# This is a thin wrapper — no caching, no de-duplication, no download. The
# consumer (wireframe-builder, infographic-builder, asset-generator) decides
# how to use the URLs.
#
# Usage:
#   bash bin/amw-image-search.sh "modern office workspace"
#   bash bin/amw-image-search.sh "coffee cup" --orientation portrait --count 5
#   bash bin/amw-image-search.sh "city skyline" --type photo --luminance dark --json
#   bash bin/amw-image-search.sh --help
#
# Filters:
#   --orientation landscape|portrait|square
#   --type photo|illustration|3d                (Lummi supports these three)
#   --luminance light|dark                      (broad luminance filter)
#   --count N                                   (max results, default 10)
#   --json                                      (emit raw JSON response)
#   --api-key KEY                               (overrides LUMMI_API_KEY env var)
#
# Exit codes:
#   0 — success
#   1 — API returned an error or zero results
#   2 — invocation error (bad args)
#   3 — curl/jq/network failure
#
# Dependencies: curl (required), jq (required for --format=urls; optional for --json).
#
# API key handling:
#   The Lummi public API may work without a key for low-volume use. For higher
#   rate limits, set:
#       export LUMMI_API_KEY="your-key-here"
#   or pass --api-key on the command line. The key is sent via Authorization
#   header per Lummi's documented contract.

set -u

API_ENDPOINT="${LUMMI_API_ENDPOINT:-https://api.lummi.ai/v1/images/search}"
API_KEY="${LUMMI_API_KEY:-}"
QUERY=""
ORIENTATION=""
IMG_TYPE=""
LUMINANCE=""
COUNT=10
FORMAT="urls"

usage() {
  sed -n '4,42p' "$0" >&2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --orientation) ORIENTATION="${2:-}"; shift 2 ;;
    --type)        IMG_TYPE="${2:-}"; shift 2 ;;
    --luminance)   LUMINANCE="${2:-}"; shift 2 ;;
    --count)       COUNT="${2:-10}"; shift 2 ;;
    --json)        FORMAT="json"; shift ;;
    --api-key)     API_KEY="${2:-}"; shift 2 ;;
    -h|--help)     usage; exit 2 ;;
    --)            shift; QUERY="${QUERY:+$QUERY }$*"; break ;;
    -*)            printf 'Unknown flag: %s\n' "$1" >&2; usage; exit 2 ;;
    *)             QUERY="${QUERY:+$QUERY }$1"; shift ;;
  esac
done

if [ -z "$QUERY" ]; then
  printf 'ERROR: query string required\n' >&2
  usage
  exit 2
fi

# Dependency checks.
if ! command -v curl >/dev/null 2>&1; then
  printf 'ERROR: curl not found on PATH\n' >&2
  exit 3
fi
HAS_JQ=0
if command -v jq >/dev/null 2>&1; then HAS_JQ=1; fi
if [ "$FORMAT" = "urls" ] && [ "$HAS_JQ" -eq 0 ]; then
  printf 'ERROR: --format=urls requires jq on PATH\n' >&2
  exit 3
fi

# URL-encode the query.
url_encode() {
  local s="$1"
  local out=""
  local i ch
  for ((i = 0; i < ${#s}; i++)); do
    ch="${s:$i:1}"
    case "$ch" in
      [A-Za-z0-9._~-]) out+="$ch" ;;
      ' ') out+="+" ;;
      *) out+=$(printf '%%%02X' "'$ch") ;;
    esac
  done
  printf '%s' "$out"
}

Q="$(url_encode "$QUERY")"

# Assemble URL.
URL="${API_ENDPOINT}?query=${Q}&limit=${COUNT}"
if [ -n "$ORIENTATION" ]; then URL+="&orientation=${ORIENTATION}"; fi
if [ -n "$IMG_TYPE" ];    then URL+="&type=${IMG_TYPE}"; fi
if [ -n "$LUMINANCE" ];   then URL+="&luminance=${LUMINANCE}"; fi

# Make the request.
TMP="$(mktemp -t amw-image-search-XXXXXX)"
trap 'rm -f "$TMP"' EXIT

CURL_OPTS=(--silent --show-error --max-time 30 --user-agent "amw-image-search/1.0")
if [ -n "$API_KEY" ]; then
  CURL_OPTS+=(--header "Authorization: Bearer ${API_KEY}")
fi

if ! curl "${CURL_OPTS[@]}" --output "$TMP" --write-out '%{http_code}' "$URL" > "${TMP}.code" 2>&1; then
  printf 'ERROR: network failure invoking %s\n' "$URL" >&2
  exit 3
fi

HTTP_CODE="$(cat "${TMP}.code" 2>/dev/null || echo 0)"
rm -f "${TMP}.code"

if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
  printf 'ERROR: API returned HTTP %s\n' "$HTTP_CODE" >&2
  cat "$TMP" >&2
  exit 1
fi

case "$FORMAT" in
  json)
    cat "$TMP"
    ;;
  urls)
    # Extract download/full-size URLs. Lummi's response shape: { "data": [ { "url": "...", "urls": { "regular": "..." } } ] }
    # Try several shapes; emit one URL per line.
    EXTRACTED="$(jq -r '
      ( .data // .results // .images // .photos // [] ) as $arr
      | $arr[]
      | ( .urls.regular // .urls.full // .url // .src // empty )
    ' "$TMP" 2>/dev/null || true)"
    if [ -z "$EXTRACTED" ]; then
      printf 'ERROR: zero results extracted from API response (use --json to inspect)\n' >&2
      exit 1
    fi
    printf '%s\n' "$EXTRACTED"
    ;;
  *)
    printf 'ERROR: unknown format: %s\n' "$FORMAT" >&2
    exit 2
    ;;
esac

exit 0
