"""Unit tests for bin/amw-ascii-parse.py — ASCII -> structured-JSON tokenizer.

Driven through the real CLI (reads stdin or --in, writes JSON to stdout or
--out). Public payload shape, confirmed by reading find_boxes / find_arrows /
find_wireframe_components and main():

  {
    "meta": {"format": "unicode|ascii|mixed", "mode": ..., "rows": N, "cols": N},
    "boxes":  [{"x", "y", "w", "h", "text"} ...],
    "arrows": [{"row", "col", "symbol", "direction"} ...],
    "components": [...]            # only in --mode wireframe
    "grid_classified": [[...]]     # omitted with --no-grid
  }

Documented contract this suite pins:
  * It is a MECHANICAL tokenizer: text with no boxes returns boxes:[] and
    exits 0 — "no structure" is a valid result, NOT an error.
  * Empty input returns rows:0/cols:0, empty boxes/arrows, exit 0.
  * Fenced ``` code-block wrappers are stripped before parsing.
  * Unicode and ASCII box styles are both detected; format is reported in meta.

No mocks: real CLI subprocess against real input.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "amw-ascii-parse.py"
TIMEOUT = 30


def _parse(text: str, *extra: str) -> dict:
    """Run the parser on `text` via stdin; return the parsed JSON payload."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--mode", "diagram", "--no-grid", *extra],
        input=text,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert result.returncode == 0, f"parser exited {result.returncode}\n{result.stderr}"
    return json.loads(result.stdout)


def test_ascii_box_parses_to_single_node() -> None:
    """An ASCII +--+ box is tokenized into one box with its inner text."""
    payload = _parse("+-----+\n|  A  |\n+-----+\n")
    assert payload["meta"]["format"] == "ascii"
    assert len(payload["boxes"]) == 1
    box = payload["boxes"][0]
    assert box["text"] == "A"
    assert (box["x"], box["y"]) == (0, 0)
    assert box["w"] == 7 and box["h"] == 3


def test_two_boxes_and_arrow_between_them() -> None:
    """Two ASCII boxes joined by '->' yield 2 boxes and 1 right-arrow."""
    diagram = "+-----+      +-----+\n|  A  |  ->  |  B  |\n+-----+      +-----+\n"
    payload = _parse(diagram)
    assert len(payload["boxes"]) == 2
    texts = sorted(b["text"] for b in payload["boxes"])
    assert texts == ["A", "B"]
    assert len(payload["arrows"]) == 1
    arrow = payload["arrows"][0]
    assert arrow["symbol"] == "->"
    assert arrow["direction"] == "right"


def test_unicode_box_is_detected() -> None:
    """A Unicode box-drawing box parses to one node and meta.format unicode."""
    payload = _parse("┌─────┐\n"
                     "│  A  │\n"
                     "└─────┘\n")
    assert payload["meta"]["format"] == "unicode"
    assert len(payload["boxes"]) == 1
    assert payload["boxes"][0]["text"] == "A"


def test_empty_input_returns_empty_structure() -> None:
    """Empty stdin yields rows:0/cols:0 and empty boxes/arrows, exit 0."""
    payload = _parse("")
    assert payload["meta"]["rows"] == 0
    assert payload["meta"]["cols"] == 0
    assert payload["boxes"] == []
    assert payload["arrows"] == []


def test_prose_without_boxes_returns_no_boxes() -> None:
    """Plain prose (no box chars) tokenizes to zero boxes, exit 0 (not error)."""
    payload = _parse("just some prose here\nno boxes at all\n")
    assert payload["boxes"] == []


def test_fenced_code_block_wrapper_is_stripped() -> None:
    """A ```-fenced box is parsed as if the fences weren't there."""
    payload = _parse("```\n+---+\n| Y |\n+---+\n```\n")
    assert len(payload["boxes"]) == 1
    assert payload["boxes"][0]["text"] == "Y"
    # The trailing fence must not leak in as a row of backticks.
    assert payload["meta"]["rows"] == 3


def test_out_flag_writes_json_file(tmp_path: Path) -> None:
    """--out writes the JSON payload to disk and prints a summary line."""
    src = tmp_path / "diagram.txt"
    src.write_text("+-----+\n|  A  |\n+-----+\n", encoding="utf-8")
    out = tmp_path / "parsed.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--in", str(src), "--out", str(out),
         "--mode", "diagram", "--no-grid"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert result.returncode == 0, result.stderr
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert len(payload["boxes"]) == 1
    assert "Parsed" in result.stdout  # summary line on stdout


def test_wireframe_mode_extracts_components() -> None:
    """--mode wireframe extracts button/checkbox/input/radio components."""
    wf = "[ Submit ]\n[x] Remember me\n[____ email ____]\n( ) Option A\n"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--mode", "wireframe", "--no-grid"],
        input=wf,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    kinds = {c["kind"] for c in payload["components"]}
    assert {"button", "checkbox", "input", "radio"} <= kinds
