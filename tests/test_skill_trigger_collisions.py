"""Ratchet gate: skill-trigger collisions must not GROW (TRDD-NN3X00Q6).

bin/amw-skill-trigger-collision.py worked but was wired into no gate — CLAUDE.md
called it "CI-time gate" while nothing (CI, pytest, /amw-doctor) ever ran it, so
37 HIGH collisions accumulated invisibly (Phase-1 audit, axis 4 / CONFIRMED-2).

This is a RATCHET, not a zero-gate: the 37 pre-existing HIGH collisions are
unadjudicated debt (possibly partly detector noise), so asserting high == 0
would red CI on day one without fixing anything. Instead the baseline is frozen
at the measured count; any NEW collision pushes `high` above it and fails here.
Lowering the baseline as debt is paid down is encouraged; raising it requires
its own TRDD. No mocks: runs the real tool over the real skills/ tree.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "bin" / "amw-skill-trigger-collision.py"

# Measured 2026-08-18 (summary: total=105 high=37 medium=0 low=68). Frozen debt —
# ratchet DOWN only; raising this number needs its own TRDD.
HIGH_BASELINE = 37


def _run() -> dict:
    proc = subprocess.run(
        [sys.executable, str(TOOL)], capture_output=True, text=True, cwd=ROOT
    )
    return json.loads(proc.stdout)


def test_high_collisions_do_not_exceed_baseline() -> None:
    """The tool's HIGH collision count stays at or below the frozen baseline."""
    summary = _run()["summary"]
    assert summary["high"] <= HIGH_BASELINE, (
        f"HIGH skill-trigger collisions grew: {summary['high']} > baseline "
        f"{HIGH_BASELINE}. A new skill description re-claims another skill's "
        "trigger phrase — narrow it (see CLAUDE.md 'orchestrator priority'), "
        "or adjudicate and lower/justify the baseline in its own TRDD."
    )


def test_tool_actually_detects_collisions() -> None:
    """Positive control: the tool is not a no-op — it finds the known debt."""
    summary = _run()["summary"]
    # If detection silently broke (regex drift, empty scan), high would drop to
    # 0 and the ratchet above would pass vacuously. Guard the instrument itself.
    assert summary["total"] > 0, "tool found zero collisions — detector broken?"
    assert summary["high"] > 0, "known HIGH debt vanished without a baseline lower"
