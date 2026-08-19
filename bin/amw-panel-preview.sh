#!/usr/bin/env bash
# author: emasoft
# license: MIT
#
# amw-panel-preview.sh — push a live HTML preview into the AI Maestro
# dashboard side panel (the human's web browser panel), via the frozen
# aimaestro-panel.sh CLI (the spec-mandated integration surface: plugins
# call SCRIPTS only, never the HTTP API — design/specs/aimaestro-scripts-spec.md).
#
# This is the webdesign plugin's ONLY call-site for the panel: skills and
# commands go through this wrapper so availability gating and agent-name
# resolution live in one place (same pattern as amw-dev-browser-wrapper.sh).
#
# Usage:
#   amw-panel-preview.sh show    (--html-file <path> | --url <https-url>) [--agent <name-or-uuid>]
#   amw-panel-preview.sh refresh [--agent <name-or-uuid>]
#   amw-panel-preview.sh close   [--agent <name-or-uuid>]
#   amw-panel-preview.sh feedback [--agent <name-or-uuid>]
#   amw-panel-preview.sh status  [--agent <name-or-uuid>]
#
# Agent resolution: --agent wins; else $AIMAESTRO_AGENT; else $AID; else fail.
# Auth: aimaestro-panel.sh reads AID_AUTH itself — nothing handled here.
#
# AUTH SHAPE (verified by the hub's authed e2e, 2026-08-19): `show` is
# set+open = TWO strict POSTs. An AGENT caller (AID_AUTH + governance title)
# is authorized for both. A USER caller's AIMAESTRO_SUDO_TOKEN is one-shot /
# one-op, so the second POST 403s (sudo_required) — USER callers must use the
# per-op verbs (set via the CLI, then `open`) minting a fresh token right
# before each op; the USER sudo quota is 2 outstanding tokens, so two failed
# calls 429 (sudo_token_quota_exceeded) for 60 s.
#
# NOTE: the panel is a LIVE surface, not a queue. "delivered" counts connected
# panel CHANNELS = dashboards currently showing THIS agent — not "panel
# visible". A set after close re-opens the panel (delivered 1); "delivered": 0
# means no dashboard has this agent active and the push was DROPPED — callers
# must surface that, not report success.

set -euo pipefail

PANEL_CLI="$(command -v aimaestro-panel.sh || true)"
if [ -z "$PANEL_CLI" ]; then
  echo "amw-panel-preview: aimaestro-panel.sh not found on PATH — not an AI Maestro" >&2
  echo "environment (or the server CLIs are not installed). Fall back to /amw-preview's" >&2
  echo "dev-browser flow instead." >&2
  exit 3
fi

verb="${1:-}"; shift || true
agent="${AIMAESTRO_AGENT:-${AID:-}}"
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    --agent) agent="$2"; shift 2 ;;
    *) args+=("$1"); shift ;;
  esac
done

if [ -z "$agent" ]; then
  echo "amw-panel-preview: no agent id — pass --agent or export AIMAESTRO_AGENT / AID" >&2
  exit 2
fi

case "$verb" in
  show)
    # set the content, then open the panel so the human actually sees it.
    # ${args[@]+…} not "${args[@]}": under `set -u` on the system /bin/bash
    # (3.2.57) an EMPTY array expansion is "unbound variable" — every no-flag
    # verb died before reaching the CLI (hub e2e report 20260819_150341).
    "$PANEL_CLI" set "$agent" ${args[@]+"${args[@]}"}
    "$PANEL_CLI" open "$agent"
    ;;
  refresh|close|status|feedback)
    "$PANEL_CLI" "$verb" "$agent" ${args[@]+"${args[@]}"}
    ;;
  *)
    echo "amw-panel-preview: unknown verb '$verb' (show|refresh|close|status|feedback)" >&2
    exit 2
    ;;
esac
