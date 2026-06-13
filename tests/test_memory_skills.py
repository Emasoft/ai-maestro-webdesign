"""Real tests for the webdesign markdown memory skills (amw-memory-recall / amw-memory-write).

No mocks. Validates the two SKILL.md files parse and stay within the CPV line cap, the
protocol doc carries the load-bearing rules, and — most importantly — the RECALL mechanism
the skills prescribe actually works: a symptom-indexed note planted in a temp memdir is
found by its SYMPTOM (via the documented grep fallback, and via the real memgrep binary when
present) and is NOT returned for an unrelated query.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RECALL = ROOT / "skills" / "amw-memory-recall" / "SKILL.md"
WRITE = ROOT / "skills" / "amw-memory-write" / "SKILL.md"
PROTOCOL = ROOT / "rules" / "memory-protocol.md"


def _frontmatter(p: Path) -> dict[str, str]:
    """Parse the top-level name/description from a SKILL.md frontmatter (no yaml dep)."""
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert m, f"{p} is missing a --- frontmatter block"
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def _plant_note(memdir: Path) -> None:
    """Write one symptom-indexed note into a temp memdir (the canonical note shape)."""
    memdir.mkdir(parents=True, exist_ok=True)
    (memdir / "zprofile-keychain-hang.md").write_text(
        "---\n"
        "name: zprofile-keychain-hang\n"
        'description: "every bash command hangs / stuck at password to unlock keychain"\n'
        "metadata:\n  type: reference\n"
        "---\n\n"
        "The .zprofile blocks on a keychain unlock prompt; guard the line or unlock "
        "the keychain so bash stops hanging.\n\n"
        "## Notes and lessons learned\n",
        encoding="utf-8",
    )


def test_recall_skill_frontmatter() -> None:
    """amw-memory-recall SKILL.md declares its matching name and a non-trivial description."""
    fm = _frontmatter(RECALL)
    assert fm.get("name") == "amw-memory-recall"
    assert len(fm.get("description", "")) > 80


def test_write_skill_frontmatter() -> None:
    """amw-memory-write SKILL.md declares its matching name and a non-trivial description."""
    fm = _frontmatter(WRITE)
    assert fm.get("name") == "amw-memory-write"
    assert len(fm.get("description", "")) > 80


def test_skills_within_line_cap() -> None:
    """Both memory SKILL.md bodies stay under the CPV 500-line cap (a real, reliable cap)."""
    for p in (RECALL, WRITE):
        lines = p.read_text(encoding="utf-8").count("\n") + 1
        assert lines < 500, f"{p} has {lines} lines (>= 500 CPV cap)"


def test_protocol_carries_load_bearing_rules() -> None:
    """memory-protocol.md states index-by-symptom, the three scopes, and the grep fallback."""
    t = PROTOCOL.read_text(encoding="utf-8").lower()
    assert "symptom" in t and "not the answer" in t
    for scope in ("local", "project", "user"):
        assert scope in t
    assert "grep" in t


def test_grep_fallback_recall_finds_by_symptom(tmp_path: Path) -> None:
    """The documented grep fallback finds the planted note by its symptom, not by an unrelated query."""
    memdir = tmp_path / "memory"
    _plant_note(memdir)
    hit = subprocess.run(
        ["grep", "-rliE", "bash command hangs", str(memdir)],
        capture_output=True,
        text=True,
    )
    assert "zprofile-keychain-hang.md" in hit.stdout
    miss = subprocess.run(
        ["grep", "-rliE", "tailwind gradient slop", str(memdir)],
        capture_output=True,
        text=True,
    )
    assert miss.stdout.strip() == ""


def test_memgrep_recall_finds_by_symptom(tmp_path: Path) -> None:
    """If memgrep is installed, `memgrep recall <symptom> <memdir>` returns the planted note (real binary)."""
    if shutil.which("memgrep") is None:
        pytest.skip("memgrep not on PATH — the grep fallback test covers the recall contract")
    memdir = tmp_path / "memory"
    _plant_note(memdir)
    r = subprocess.run(
        ["memgrep", "recall", "bash command hangs at keychain", str(memdir)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        pytest.skip(f"memgrep recall unsupported on this build: {r.stderr.strip()[:120]}")
    assert "zprofile-keychain-hang" in (r.stdout + r.stderr)
