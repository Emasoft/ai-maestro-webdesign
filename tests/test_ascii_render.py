"""Unit tests for bin/amw-ascii-render.py — the JSON -> ASCII renderer.

The renderer reads a JSON spec on stdin and prints ASCII to stdout. Its public
contract (module main()):

  - the top-level JSON must contain exactly one of the keys
    "diagram" | "table" | "layers" | "sequence";
  - it enforces a hard 78-column max and exits 1 if any line is wider;
  - invalid JSON or a missing mode-key exits 1 with an "Error:" message.

Schemas were discovered by reading render_diagram / render_table /
render_layers / render_sequence:
  diagram  -> {"boxes":[{"id","label"}], "grid":[[id...]], "connectors":[...]}
  table    -> {"headers":[[cell...]], "rows":[[cell...]]}   (lists of ROWS)
  layers   -> {"title", "levels":[{"label","boxes":[str...]}]}
  sequence -> {"actors":[str...], "messages":[{"from","to","label"}]}

Every successful render is then fed through the real bin/amw-validate-ascii.py
so the test proves the output is genuinely well-formed ASCII (<=78 cols,
aligned, no wide/forbidden chars), not merely non-empty.

No mocks: real renderer subprocess + real validator subprocess.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
RENDER = BIN / "amw-ascii-render.py"
VALIDATE = BIN / "amw-validate-ascii.py"
MAX_WIDTH = 78
TIMEOUT = 30


def _render(spec: dict) -> subprocess.CompletedProcess:
    """Run the renderer with `spec` as JSON stdin."""
    return subprocess.run(
        [sys.executable, str(RENDER)],
        input=json.dumps(spec),
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def _assert_renders_valid_ascii(spec: dict, tmp_path: Path) -> str:
    """Render spec, assert exit 0 + <=78 cols + validator PASS. Return output."""
    proc = _render(spec)
    assert proc.returncode == 0, f"render failed exit {proc.returncode}\n{proc.stderr}"
    out = proc.stdout
    assert out.strip(), "renderer produced empty output"
    widths = [len(line) for line in out.split("\n")]
    assert max(widths) <= MAX_WIDTH, f"line exceeds {MAX_WIDTH} cols: max={max(widths)}\n{out}"

    # Round-trip through the real validator: it must PASS.
    target = tmp_path / "rendered.txt"
    target.write_text(out if out.endswith("\n") else out + "\n", encoding="utf-8")
    vproc = subprocess.run(
        [sys.executable, str(VALIDATE), str(target)],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert vproc.returncode == 0, f"rendered ASCII failed validator:\n{vproc.stdout}\n{out}"
    return out


def test_diagram_mode_renders_and_validates(tmp_path: Path) -> None:
    """diagram-mode spec renders boxes+connector that pass the validator."""
    spec = {
        "diagram": {
            "boxes": [{"id": "a", "label": "Alpha"}, {"id": "b", "label": "Beta"}],
            "grid": [["a", "b"]],
            "connectors": [{"from": "a", "to": "b"}],
        }
    }
    out = _assert_renders_valid_ascii(spec, tmp_path)
    assert "Alpha" in out and "Beta" in out


def test_table_mode_renders_and_validates(tmp_path: Path) -> None:
    """table-mode spec renders an aligned grid that passes the validator."""
    spec = {
        "table": {
            "headers": [["Name", "Role"]],
            "rows": [["Ann", "Dev"], ["Bob", "PM"]],
        }
    }
    out = _assert_renders_valid_ascii(spec, tmp_path)
    assert "Name" in out and "Ann" in out


def test_layers_mode_renders_and_validates(tmp_path: Path) -> None:
    """layers-mode spec renders stacked layers that pass the validator."""
    spec = {
        "layers": {
            "title": "Stack",
            "levels": [
                {"label": "UI", "boxes": ["Button", "Form"]},
                {"label": "API", "boxes": ["REST"]},
            ],
        }
    }
    out = _assert_renders_valid_ascii(spec, tmp_path)
    assert "Button" in out and "REST" in out


def test_sequence_mode_renders_and_validates(tmp_path: Path) -> None:
    """sequence-mode spec renders actors+message arrow that pass the validator."""
    spec = {
        "sequence": {
            "actors": ["User", "Server"],
            "messages": [{"from": "User", "to": "Server", "label": "GET"}],
        }
    }
    out = _assert_renders_valid_ascii(spec, tmp_path)
    assert "User" in out and "Server" in out


def test_missing_mode_key_errors() -> None:
    """A JSON object with no diagram/table/layers/sequence key exits 1."""
    proc = _render({"unknown": 1})
    assert proc.returncode == 1
    assert "Error" in proc.stderr


def test_invalid_json_errors() -> None:
    """Non-JSON stdin exits 1 with an invalid-JSON message."""
    proc = subprocess.run(
        [sys.executable, str(RENDER)],
        input="this is not json",
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert proc.returncode == 1
    assert "Invalid JSON" in proc.stderr
