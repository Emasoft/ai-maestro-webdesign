"""Unit tests for bin/amw-validate-ascii.py — the ASCII diagram validator.

Each test invokes the validator through its real CLI (a fresh subprocess) on a
temp file written with tmp_path. The validator's public contract (from its
module docstring) is:

  exit 0  — every file PASSES
  exit 1  — at least one file FAILED (or ERROR / EMPTY)
  stdout  — human report containing "Status: PASS" or "Status: FAIL" plus,
            on failure, one "[TYPE] message" line per finding.

No mocks: the real check functions (check_group_widths, check_wide_chars,
check_forbidden_chars, check_vertical_continuity, …) run against real input.

Reproducibility: pure stdlib, no randomness, no network, no timestamps. The
validator is platform-independent (Python 3.8+ stdlib only), so no skipif
guards are needed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "amw-validate-ascii.py"
TIMEOUT = 30

# The validator decorates its report with ANSI color escapes (e.g.
# "Status: \x1b[32mPASS\x1b[0m"). Strip them so substring assertions on the
# human-readable status text are color-agnostic and CI/terminal-independent.
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(s: str) -> str:
    return _ANSI_RE.sub("", s)


def _run(ascii_text: str, tmp_path: Path) -> subprocess.CompletedProcess:
    """Write ascii_text to a temp file and run the validator CLI on it."""
    target = tmp_path / "diagram.txt"
    target.write_text(ascii_text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(target)],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def test_aligned_box_under_78_cols_passes(tmp_path: Path) -> None:
    """A well-aligned ASCII box <=78 cols validates as PASS (exit 0)."""
    box = "+-------+\n|  OK   |\n+-------+\n"
    result = _run(box, tmp_path)
    assert result.returncode == 0, f"expected PASS exit 0, got {result.returncode}\n{result.stdout}"
    assert "Status: PASS" in _strip_ansi(result.stdout)


def test_aligned_unicode_box_passes(tmp_path: Path) -> None:
    """A rounded-corner Unicode box with aligned walls validates as PASS."""
    box = "╭─────╮\n│ hi  │\n╰─────╯\n"
    result = _run(box, tmp_path)
    assert result.returncode == 0, f"expected PASS exit 0, got {result.returncode}\n{result.stdout}"
    assert "Status: PASS" in _strip_ansi(result.stdout)


def test_over_width_line_fails(tmp_path: Path) -> None:
    """A line wider than 78 display columns is reported as a FAIL (exit 1)."""
    # 90 dashes between two corners => 92 cols, well over the 78 limit. A second
    # short box line is added so the group-width check has a baseline to flag.
    wide = "+" + ("-" * 90) + "+\n+--+\n"
    result = _run(wide, tmp_path)
    assert result.returncode == 1, f"expected FAIL exit 1, got {result.returncode}\n{result.stdout}"
    assert "Status: FAIL" in _strip_ansi(result.stdout)


def test_misaligned_vertical_border_fails(tmp_path: Path) -> None:
    """A vertical border that shifts column between rows is flagged as FAIL."""
    # Top/bottom corners at col 0 and 8, but the middle wall's right '|' is at
    # col 7 instead of 8 — a vertical-continuity / corner-alignment violation.
    misaligned = "+------+\n|  x  |\n+------+\n"
    result = _run(misaligned, tmp_path)
    assert result.returncode == 1, f"expected FAIL exit 1, got {result.returncode}\n{result.stdout}"
    assert "Status: FAIL" in _strip_ansi(result.stdout)


def test_emoji_wide_char_fails(tmp_path: Path) -> None:
    """An emoji (2 display columns) trips the wide-character check (FAIL)."""
    # The rocket emoji renders 2 cols wide and breaks monospace alignment.
    box = "+-------+\n| \U0001F680 hi |\n+-------+\n"
    result = _run(box, tmp_path)
    assert result.returncode == 1, f"expected FAIL exit 1, got {result.returncode}\n{result.stdout}"
    # The wide-char check tags findings with a WIDE_CHAR type.
    assert "WIDE_CHAR" in _strip_ansi(result.stdout)


def test_forbidden_long_arrow_fails(tmp_path: Path) -> None:
    """A forbidden long-arrow glyph (U+27F6) is reported as a FAIL."""
    # '⟶' (⟶) renders 3-4x width — explicitly forbidden by the validator.
    text = "A ⟶ B\n"
    result = _run(text, tmp_path)
    assert result.returncode == 1, f"expected FAIL exit 1, got {result.returncode}\n{result.stdout}"
    # The forbidden-char check tags findings FORBIDDEN_CHAR_CRITICAL/HIGH/MEDIUM.
    assert "FORBIDDEN_CHAR" in _strip_ansi(result.stdout)


def test_missing_file_reports_error(tmp_path: Path) -> None:
    """A nonexistent input path yields a non-zero exit and an error report."""
    missing = tmp_path / "does-not-exist.txt"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(missing)],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert result.returncode == 1
    # validate_file returns status ERROR with a "Cannot open file" message.
    clean = _strip_ansi(result.stdout)
    assert "ERROR" in clean or "Cannot open" in clean
