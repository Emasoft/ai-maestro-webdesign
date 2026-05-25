"""Unit tests for bin/amw-page-to-ascii-layout.py — webpage -> ASCII wireframe.

Driven through the real CLI with `--no-browser` (the deterministic static-HTML
fallback — no dev-browser, no network, fully reproducible). Contract from the
module docstring:

  exit 0  ASCII emitted and PASSES bin/amw-validate-ascii.py
  exit 1  capture failed AND fallback produced nothing usable (e.g. empty page)
  exit 2  PNG refusal OR CLI misuse (non-.html local input, missing file)

Verified-real width nuance (tested explicitly below): the BODY (box-drawing
wireframe) respects the hard 78-column cap, but the prepended header-comment
block (lines starting with '#') may exceed 78 and may contain a non-ASCII
em-dash in the fallback note. The validator passes the whole file anyway
because comment lines aren't part of any box group. So this suite asserts the
78-col cap on the box-drawing lines specifically, and asserts the whole output
passes the real validator (which is the script's own self-validation gate).

Fixtures live in tests/fixtures/ (sample-page.html, empty.html) — committed,
tracked sample inputs, well under the fixture size budget.

No mocks: real CLI subprocess + real validator subprocess.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "amw-page-to-ascii-layout.py"
VALIDATE = ROOT / "bin" / "amw-validate-ascii.py"
SAMPLE = ROOT / "tests" / "fixtures" / "sample-page.html"
EMPTY = ROOT / "tests" / "fixtures" / "empty.html"
MAX_WIDTH = 78
TIMEOUT = 60

# A box-drawing line is one made of the wireframe glyphs the renderer uses
# ('+', '-', '|', space). Header-comment lines start with '#'.
_BOX_CHARS = set("+-| ")


def _box_lines(text: str) -> list[str]:
    """Return the wireframe (non-comment, non-blank) box-drawing lines."""
    out = []
    for line in text.split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        if set(line) <= _BOX_CHARS or "|" in line or "+" in line:
            out.append(line)
    return out


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def test_sample_page_static_fallback_exits_zero(tmp_path: Path) -> None:
    """--no-browser on sample-page.html emits a wireframe and exits 0."""
    out = tmp_path / "layout.txt"
    result = _run(str(SAMPLE), "--no-browser", "--out", str(out))
    assert result.returncode == 0, result.stderr
    assert out.exists()
    assert out.read_text(encoding="utf-8").strip(), "wrote an empty wireframe"


def test_sample_page_box_lines_within_78_cols(tmp_path: Path) -> None:
    """Every box-drawing line of the wireframe is <=78 columns wide."""
    out = tmp_path / "layout.txt"
    result = _run(str(SAMPLE), "--no-browser", "--out", str(out))
    assert result.returncode == 0, result.stderr
    box_lines = _box_lines(out.read_text(encoding="utf-8"))
    assert box_lines, "no box-drawing lines found in output"
    widest = max(len(line) for line in box_lines)
    assert widest <= MAX_WIDTH, f"box line exceeds {MAX_WIDTH}: width {widest}"


def test_sample_page_contains_landmark_labels(tmp_path: Path) -> None:
    """The wireframe labels the header, main, and footer landmarks."""
    out = tmp_path / "layout.txt"
    result = _run(str(SAMPLE), "--no-browser", "--out", str(out))
    assert result.returncode == 0, result.stderr
    text = out.read_text(encoding="utf-8")
    for landmark in ("header", "main", "footer"):
        assert f"| {landmark}" in text, f"missing landmark label '{landmark}'\n{text}"


def test_sample_page_output_passes_validator(tmp_path: Path) -> None:
    """The emitted wireframe file passes the real amw-validate-ascii.py."""
    out = tmp_path / "layout.txt"
    result = _run(str(SAMPLE), "--no-browser", "--out", str(out))
    assert result.returncode == 0, result.stderr
    vproc = subprocess.run(
        [sys.executable, str(VALIDATE), str(out)],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert vproc.returncode == 0, f"wireframe failed validator:\n{vproc.stdout}"


def test_png_input_refused_with_exit_2(tmp_path: Path) -> None:
    """A PNG input is refused with exit code 2 (output-only directive)."""
    png = tmp_path / "shot.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)
    result = _run(str(png), "--no-browser")
    assert result.returncode == 2
    assert "REFUSE" in result.stderr


def test_empty_page_exits_1() -> None:
    """An HTML page with no significant layout blocks exits 1."""
    result = _run(str(EMPTY), "--no-browser")
    assert result.returncode == 1
    assert "no significant layout blocks" in result.stderr


def test_non_html_local_input_exits_2(tmp_path: Path) -> None:
    """A local input that isn't .html/.htm is rejected with exit 2."""
    txt = tmp_path / "notes.txt"
    txt.write_text("just text, not html\n", encoding="utf-8")
    result = _run(str(txt), "--no-browser")
    assert result.returncode == 2
    assert ".html" in result.stderr
