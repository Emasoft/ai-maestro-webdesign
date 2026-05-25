"""Unit tests for bin/amw-diagram-ir.py — parse / emit / validate / diff the IR.

The IR (diagram-ir/1.0) is the pivot format for cross-format diagram
conversion. This suite drives the real CLI (module docstring contract):

  validate --in IR        exit 0 PASS / 1 FAIL
  emit     --in IR --format <ascii|html|svg|mermaid>  exit 0 / 1 on invalid IR
  parse    --in PATH [--format FMT]                   exit 0 / 1|2

Verified-real behavior notes:

* `emit --format ascii` on a raw-source freeform IR returns the carried label
  verbatim (the raw-source fast-path), so a one-node freeform IR emits
  byte-for-byte.

* `parse --format ascii` delegates to bin/amw-ascii-parse.py and reaches the
  structured `kind:"flowchart"` branch — it extracts one node per detected box.
  Box LABELS and connector EDGES are not yet recovered by amw-ascii-parse.py
  (a known parser limitation, separate from IR delegation), so a structured
  emit->parse round-trip preserves node COUNT but not labels/edges.

* `parse --format mermaid` delegates to bin/amw-parse-mermaid-diagram.py and
  returns a structured flowchart IR (nodes, edges, metadata).

These notes match the on-disk `amw-`prefixed delegation targets wired in
amw-diagram-ir.py (parse_ascii -> amw-ascii-parse.py, _parse_via_subprocess ->
amw-parse-<fmt>-diagram.py, emit ascii fallback -> amw-ascii-render.py).

No mocks: every assertion runs the real CLI in a subprocess.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "amw-diagram-ir.py"
TIMEOUT = 30

VALID_IR = {
    "format": "diagram-ir/1.0",
    "source_format": "ascii",
    "kind": "flowchart",
    "layout": "grid",
    "nodes": [{"id": "a", "label": "Alpha"}, {"id": "b", "label": "Beta"}],
    "edges": [{"id": "e1", "from": "a", "to": "b"}],
}

RAW_SOURCE_IR = {
    "format": "diagram-ir/1.0",
    "source_format": "ascii",
    "kind": "freeform",
    "layout": "freeform",
    "nodes": [{"id": "raw", "label": "+---+\n| X |\n+---+", "annotations": ["raw-source"]}],
    "edges": [],
}


def _run(*args: str, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        **kw,
    )


def _write_json(obj: dict, path: Path) -> Path:
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


def test_validate_accepts_minimal_valid_ir(tmp_path: Path) -> None:
    """A minimal schema-complete IR validates as PASS (exit 0)."""
    ir = _write_json(VALID_IR, tmp_path / "ok.json")
    result = _run("validate", "--in", str(ir))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_validate_rejects_missing_required_field(tmp_path: Path) -> None:
    """An IR missing the required 'edges' array is rejected (exit 1, FAIL)."""
    bad = dict(VALID_IR)
    del bad["edges"]
    path = _write_json(bad, tmp_path / "bad.json")
    result = _run("validate", "--in", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "FAIL" in result.stdout
    assert "edges" in result.stdout


def test_validate_rejects_edge_referencing_unknown_node(tmp_path: Path) -> None:
    """A semantic check flags an edge whose 'to' matches no node id (FAIL)."""
    bad = {
        "format": "diagram-ir/1.0",
        "source_format": "ascii",
        "kind": "flowchart",
        "layout": "grid",
        "nodes": [{"id": "a", "label": "A"}],
        "edges": [{"id": "e1", "from": "a", "to": "ghost"}],
    }
    path = _write_json(bad, tmp_path / "dangling.json")
    result = _run("validate", "--in", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ghost" in result.stdout


def test_emit_ascii_raw_source_round_trips_byte_for_byte(tmp_path: Path) -> None:
    """emit ascii on a raw-source freeform IR returns its label verbatim."""
    ir = _write_json(RAW_SOURCE_IR, tmp_path / "raw.json")
    result = _run("emit", "--in", str(ir), "--format", "ascii")
    assert result.returncode == 0, result.stdout + result.stderr
    # _write_out appends a trailing newline; the carried label has none.
    assert result.stdout.rstrip("\n") == RAW_SOURCE_IR["nodes"][0]["label"]


def test_emit_then_parse_ascii_preserves_node_count(tmp_path: Path) -> None:
    """emit ascii (2-node flowchart) -> parse --format ascii recovers 2 boxes.

    amw-ascii-parse.py extracts one node per detected box but does not yet
    recover box labels or connector edges, so this asserts node COUNT round-trips
    through the structured path (label/edge recovery is a known parser gap).
    """
    ir = _write_json(VALID_IR, tmp_path / "ok.json")
    emit1 = _run("emit", "--in", str(ir), "--format", "ascii")
    assert emit1.returncode == 0, emit1.stderr
    ascii_file = tmp_path / "round.txt"
    ascii_file.write_text(emit1.stdout, encoding="utf-8")

    parsed = _run("parse", "--in", str(ascii_file), "--format", "ascii")
    assert parsed.returncode == 0, parsed.stderr
    parsed_ir = json.loads(parsed.stdout)
    assert parsed_ir["kind"] == "flowchart"
    assert parsed_ir["source_format"] == "ascii"
    assert len(parsed_ir["nodes"]) == len(VALID_IR["nodes"])

    # The structured IR recovered from ASCII is itself schema-valid.
    parsed_ir_file = _write_json(parsed_ir, tmp_path / "parsed.json")
    val = _run("validate", "--in", str(parsed_ir_file))
    assert val.returncode == 0, val.stdout


def test_emit_mermaid_produces_flowchart(tmp_path: Path) -> None:
    """emit mermaid on a structured IR yields a flowchart TD with nodes+edge."""
    ir = _write_json(VALID_IR, tmp_path / "ok.json")
    result = _run("emit", "--in", str(ir), "--format", "mermaid")
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("flowchart TD")
    assert 'a["Alpha"]' in result.stdout
    assert "a --> b" in result.stdout


def test_parse_ascii_returns_structured_flowchart(tmp_path: Path) -> None:
    """parse --format ascii on a box diagram returns a structured flowchart IR.

    The structured branch delegates to bin/amw-ascii-parse.py (diagram mode):
    each detected box becomes one node. The returned IR is schema-valid.
    """
    box = tmp_path / "box.txt"
    box.write_text("+-----+\n|  A  |\n+-----+\n", encoding="utf-8")
    result = _run("parse", "--in", str(box), "--format", "ascii")
    assert result.returncode == 0, result.stderr
    ir = json.loads(result.stdout)
    assert ir["source_format"] == "ascii"
    assert ir["kind"] == "flowchart"
    assert len(ir["nodes"]) >= 1
    # And the produced IR is itself schema-valid.
    ir_file = _write_json(ir, tmp_path / "parsed.json")
    val = _run("validate", "--in", str(ir_file))
    assert val.returncode == 0, val.stdout


def test_parse_mermaid_returns_structured_flowchart(tmp_path: Path) -> None:
    """parse --format mermaid returns a structured flowchart IR (exit 0).

    Delegates to bin/amw-parse-mermaid-diagram.py: recovers both nodes and the
    a->b edge, with mermaid as the source_format. The IR is schema-valid.
    """
    mmd = tmp_path / "g.mmd"
    mmd.write_text("flowchart TD\n  a[\"Alpha\"]\n  b[\"Beta\"]\n  a --> b\n", encoding="utf-8")
    result = _run("parse", "--in", str(mmd), "--format", "mermaid")
    assert result.returncode == 0, result.stderr
    ir = json.loads(result.stdout)
    assert ir["source_format"] == "mermaid"
    assert ir["kind"] == "flowchart"
    node_ids = {n["id"] for n in ir["nodes"]}
    assert {"a", "b"} <= node_ids
    assert any(e["from"] == "a" and e["to"] == "b" for e in ir["edges"])
    ir_file = _write_json(ir, tmp_path / "parsed.json")
    val = _run("validate", "--in", str(ir_file))
    assert val.returncode == 0, val.stdout


def test_diff_reports_added_node(tmp_path: Path) -> None:
    """diff between two IRs flags an added node and exits 1 (diff present)."""
    a = _write_json(VALID_IR, tmp_path / "a.json")
    bigger = json.loads(json.dumps(VALID_IR))
    bigger["nodes"].append({"id": "c", "label": "Gamma"})
    b = _write_json(bigger, tmp_path / "b.json")
    result = _run("diff", "--a", str(a), "--b", str(b))
    assert result.returncode == 1, result.stdout + result.stderr
    ops = json.loads(result.stdout)
    assert any(op["op"] == "add-node" and op["node"]["id"] == "c" for op in ops)


def test_parse_missing_input_path_exits_2(tmp_path: Path) -> None:
    """parse on a nonexistent --in path exits 2 (CLI/IO misuse per contract)."""
    missing = tmp_path / "nope.txt"
    result = _run("parse", "--in", str(missing), "--format", "ascii")
    assert result.returncode == 2
    assert "does not exist" in result.stderr
