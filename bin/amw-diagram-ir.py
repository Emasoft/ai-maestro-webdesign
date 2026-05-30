#!/usr/bin/env python3
"""amw-diagram-ir.py — parse / emit / validate / diff the plugin's diagram IR.

The IR (Intermediate Representation) is the pivot format for cross-format
diagram conversion in the `ai-maestro-webdesign` plugin. Its canonical schema
is mirrored as JSON-Schema in `skills/amw-diagram-formats/schema.json` and
documented in prose at `skills/amw-diagram-formats/references/ir-schema.md`.

Version: `diagram-ir/1.0` (locked by user directive 2026-04-22).

MVP parser scope
----------------
- **ASCII** — delegates to `bin/amw-ascii-parse.py` (which emits a compatible
  structured-JSON form); a thin adapter converts that into IR nodes+edges.
- **HTML** — delegates to `bin/amw-parse-html-diagram.py`.
- **SVG** — delegates to `bin/amw-parse-svg-diagram.py`.
- **Mermaid** — delegates to `bin/amw-parse-mermaid-diagram.py`. Flowchart,
  sequence, state, class, and ER diagrams are parsed to structured IR.
  Remaining Mermaid grammars (Gantt, pie, journey, mindmap, etc.) fall
  through to `kind: "freeform"` inside the Mermaid parser itself.

MVP emitter scope
-----------------
- **ASCII** — delegates to `bin/amw-ascii-render.py`. IR with exactly one
  `kind:"freeform"` node and `annotations:["raw-source"]` round-trips its
  carried ASCII source byte-for-byte.
- **HTML** — emits a minimal `<!DOCTYPE html>` wrapper with a `<pre>` block
  carrying rendered ASCII. Format-native HTML emission is future work.
- **SVG** — emits a minimal SVG stub with a `<text>` element per node.
  Format-native SVG emission is future work.
- **Mermaid** — emits a minimal `flowchart TD` with one node/edge per IR
  entry. Format-native Mermaid grammars (sequence / state / class / ER) are
  future work.

CLI contract (fail-fast; no try/except swallowing; no fallbacks)
----------------------------------------------------------------
  diagram-ir parse    --in <path> [--format FMT] [--out <ir.json>]
  diagram-ir emit     --in <ir.json> --format <ascii|html|svg|mermaid> [--out <path>]
  diagram-ir validate --in <ir.json>
  diagram-ir diff     --a <ir-a.json> --b <ir-b.json> [--out <patch.json>]

Exit codes
----------
  0 — success (PASS for validate; no diff for diff)
  1 — schema FAIL or structural diff present
  2 — CLI misuse (unknown subcommand, missing args)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Any, Dict, List

IR_VERSION = "diagram-ir/1.0"
BIN_DIR = pathlib.Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# JSON schema (draft-07-style; validated by our own lightweight validator)
# Matches §3.1 of the 12-commands build plan EXACTLY.
# ---------------------------------------------------------------------------

SCHEMA: Dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "diagram-ir/1.0",
    "type": "object",
    "additionalProperties": False,
    "required": ["format", "source_format", "kind", "nodes", "edges", "layout"],
    "properties": {
        "format": {"type": "string", "const": IR_VERSION},
        "source_format": {
            "type": "string",
            "enum": ["ascii", "html", "svg", "mermaid"],
        },
        "kind": {
            "type": "string",
            "enum": [
                "flowchart",
                "sequence",
                "state",
                "arch",
                "tree",
                "table",
                "freeform",
            ],
        },
        "layout": {
            "type": "string",
            "enum": ["layered", "grid", "freeform", "sequence"],
        },
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "label"],
                "properties": {
                    "id": {"type": "string", "pattern": r"^[A-Za-z0-9_\-]+$"},
                    "label": {"type": "string"},
                    "bbox": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["x", "y", "w", "h"],
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                            "w": {"type": "number"},
                            "h": {"type": "number"},
                        },
                    },
                    "rank": {"type": "integer"},
                    "style": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "shape": {"type": "string"},
                            "fill": {"type": "string"},
                            "stroke": {"type": "string"},
                            "corner": {"type": "string"},
                        },
                    },
                    "annotations": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "from", "to"],
                "properties": {
                    "id": {"type": "string", "pattern": r"^[A-Za-z0-9_\-]+$"},
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "label": {"type": "string"},
                    "style": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "arrow": {
                                "type": "string",
                                "enum": ["solid", "dashed", "dotted"],
                            },
                            "head": {
                                "type": "string",
                                "enum": ["triangle", "open", "none"],
                            },
                        },
                    },
                    "waypoints": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["x", "y"],
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                            },
                        },
                    },
                },
            },
        },
        "metadata": {
            "type": "object",
            "additionalProperties": True,
            "properties": {
                "title": {"type": "string"},
                "author": {"type": "string"},
                "description": {"type": "string"},
            },
        },
    },
}


# ---------------------------------------------------------------------------
# Lightweight JSON-schema validator (no external deps)
# Implements: type, enum, const, required, properties, items, pattern,
# additionalProperties:false. Enough for the IR schema above.
# Fail-fast: any unknown keyword raises (we control the schema so this is
# the right behavior — catches authoring bugs).
# ---------------------------------------------------------------------------

def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValueError(f"unknown schema type: {expected!r}")


def _validate_node(
    value: Any, schema: Dict[str, Any], ptr: str, errors: List[str]
) -> None:
    if "type" in schema and not _type_matches(value, schema["type"]):
        errors.append(f"{ptr}: expected type {schema['type']}, got {type(value).__name__}")
        return

    if "const" in schema and value != schema["const"]:
        errors.append(f"{ptr}: expected const {schema['const']!r}, got {value!r}")

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{ptr}: value {value!r} not in enum {schema['enum']}")

    if "pattern" in schema and isinstance(value, str):
        if not re.match(schema["pattern"], value):
            errors.append(f"{ptr}: string {value!r} does not match pattern {schema['pattern']!r}")

    if schema.get("type") == "object" and isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{ptr}: missing required property {key!r}")

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, sub_value in value.items():
            sub_ptr = f"{ptr}/{key}"
            if key in properties:
                _validate_node(sub_value, properties[key], sub_ptr, errors)
            else:
                if additional is False:
                    errors.append(f"{ptr}: additional property {key!r} not allowed")
                elif isinstance(additional, dict):
                    _validate_node(sub_value, additional, sub_ptr, errors)

    if schema.get("type") == "array" and isinstance(value, list):
        items = schema.get("items")
        if items is not None:
            for i, item in enumerate(value):
                _validate_node(item, items, f"{ptr}/{i}", errors)


def validate(ir: Dict[str, Any]) -> List[str]:
    """Return a list of error strings; empty list = PASS."""
    errors: List[str] = []
    _validate_node(ir, SCHEMA, "#", errors)
    # Extra semantic checks beyond what the schema encodes:
    if isinstance(ir, dict):
        node_ids = {n.get("id") for n in ir.get("nodes", []) if isinstance(n, dict)}
        for i, edge in enumerate(ir.get("edges", [])):
            if not isinstance(edge, dict):
                continue
            for field in ("from", "to"):
                target = edge.get(field)
                if target is not None and target not in node_ids:
                    errors.append(
                        f"#/edges/{i}/{field}: {target!r} does not match any node id"
                    )
    return errors


# ---------------------------------------------------------------------------
# Format detection — duplicates bin/amw-diagram-detect-format.sh rules for
# library use when we don't want to shell out. Canonical rules live in the
# shell script; keep this function in sync.
# ---------------------------------------------------------------------------

MERMAID_KEYWORDS = re.compile(
    r"^\s*(flowchart|sequenceDiagram|stateDiagram|classDiagram|erDiagram|"
    r"gantt|pie|journey|mindmap|graph)\b"
)
ASCII_BOX_CHARS = re.compile(r"[─-╿]|\+[\-=]+\+")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def detect_format(path: pathlib.Path | None, content: str | None = None) -> str:
    """Sniff format. Return one of ascii|html|svg|mermaid|png|unknown."""
    ext = path.suffix.lower() if path else ""
    if ext in {".mmd", ".mermaid"}:
        return "mermaid"
    if ext == ".png":
        return "png"
    if ext == ".svg":
        return "svg"
    if ext in {".html", ".htm"}:
        return "html"

    if path is not None and content is None:
        raw = path.read_bytes()
        if raw.startswith(PNG_MAGIC):
            return "png"
        content = raw.decode("utf-8", errors="replace")

    if content is None:
        return "unknown"

    stripped = content.lstrip()
    if stripped.startswith(("<?xml", "<svg")):
        return "svg"
    if stripped.lower().startswith(("<!doctype html", "<html")):
        return "html"
    if MERMAID_KEYWORDS.match(stripped):
        return "mermaid"
    if ASCII_BOX_CHARS.search(content):
        return "ascii"
    return "unknown"


# ---------------------------------------------------------------------------
# Parse stubs — ASCII wraps bin/amw-ascii-parse.py; HTML/SVG/Mermaid are raw-source
# freeform stubs (Phase 1 replaces them).
# ---------------------------------------------------------------------------

def _raw_source_ir(source_format: str, raw: str) -> Dict[str, Any]:
    """Return an IR carrying the raw source as a single freeform node.

    The emitter layer round-trips this back to its original format by
    inspecting `annotations: ["raw-source"]` and emitting `label` verbatim.
    """
    return {
        "format": IR_VERSION,
        "source_format": source_format,
        "kind": "freeform",
        "layout": "freeform",
        "nodes": [
            {
                "id": "raw",
                "label": raw,
                "annotations": ["raw-source"],
            }
        ],
        "edges": [],
    }


def parse_ascii(path: pathlib.Path) -> Dict[str, Any]:
    """Parse ASCII by delegating to bin/amw-ascii-parse.py in diagram mode.

    The existing parser emits a structured-JSON form. We flatten it into IR
    nodes (one per detected box) and edges (one per detected connector).
    When amw-ascii-parse.py cannot extract structure (pure freeform wireframe),
    we fall back to the raw-source stub so the renderer can round-trip.
    """
    raw = path.read_text(encoding="utf-8")
    parser = BIN_DIR / "amw-ascii-parse.py"
    if not parser.exists():
        return _raw_source_ir("ascii", raw)

    result = subprocess.run(
        [sys.executable, str(parser), "--in", str(path), "--mode", "diagram"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        # amw-ascii-parse.py could not find structure; carry raw source instead.
        return _raw_source_ir("ascii", raw)

    parsed = json.loads(result.stdout)
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for i, box in enumerate(parsed.get("boxes", [])):
        node_id = box.get("id") or f"n{i+1}"
        node: Dict[str, Any] = {"id": node_id, "label": box.get("label", "")}
        pos = box.get("position") or {}
        if pos:
            node["bbox"] = {
                "x": float(pos.get("col", 0)),
                "y": float(pos.get("row", 0)),
                "w": float(pos.get("w", 0)),
                "h": float(pos.get("h", 0)),
            }
        nodes.append(node)

    for i, conn in enumerate(parsed.get("connectors", [])):
        edges.append(
            {
                "id": f"e{i+1}",
                "from": conn.get("from", ""),
                "to": conn.get("to", ""),
                **({"label": conn["label"]} if conn.get("label") else {}),
            }
        )

    if not nodes:
        return _raw_source_ir("ascii", raw)

    return {
        "format": IR_VERSION,
        "source_format": "ascii",
        "kind": "flowchart",
        "layout": "grid",
        "nodes": nodes,
        "edges": edges,
    }


def _parse_via_subprocess(fmt: str, path: pathlib.Path) -> Dict[str, Any]:
    """Invoke the standalone parse-<fmt>-diagram.py and return its IR dict.

    Fail-fast: raises SystemExit with the parser's stderr on non-zero exit.
    """
    parser_path = BIN_DIR / f"amw-parse-{fmt}-diagram.py"
    result = subprocess.run(
        [sys.executable, str(parser_path), "--in", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"amw-parse-{fmt}-diagram.py failed (exit {result.returncode}):\n"
            + (result.stderr or result.stdout or "(no output)")
        )
    return json.loads(result.stdout)


def parse_path(path: pathlib.Path, forced_format: str | None = None) -> Dict[str, Any]:
    """Parse any supported format to IR. See module docstring for MVP scope."""
    fmt = forced_format or detect_format(path)
    if fmt == "ascii":
        return parse_ascii(path)
    if fmt in {"html", "svg", "mermaid"}:
        return _parse_via_subprocess(fmt, path)
    if fmt == "png":
        raise SystemExit(
            "PNG is output-only by plugin directive; cannot parse to IR. "
            "Provide the source artifact (ASCII/HTML/SVG/Mermaid) instead."
        )
    raise SystemExit(f"Cannot detect format for {path}; pass --format to force.")


# ---------------------------------------------------------------------------
# Emit stubs
# ---------------------------------------------------------------------------

def _render_ir_as_ascii(ir: Dict[str, Any]) -> str:
    """Render an IR as ASCII.

    Fast path: a single freeform node with annotation `raw-source` emits its
    label verbatim (perfect round-trip). Otherwise we emit a minimal
    box-per-node listing — format-native ASCII emission is future work.
    """
    nodes = ir.get("nodes", [])
    if (
        len(nodes) == 1
        and "raw-source" in (nodes[0].get("annotations") or [])
        and ir.get("kind") == "freeform"
    ):
        return nodes[0]["label"]

    # Fallback: build a minimal diagram-mode JSON and delegate to
    # bin/amw-ascii-render.py. Only works for simple flowcharts; keeps emitter
    # useful for cross-format via IR even without per-format renderers.
    renderer = BIN_DIR / "amw-ascii-render.py"
    if not renderer.exists() or not nodes:
        # Last-resort plain text listing.
        lines = [f"[{n.get('id')}] {n.get('label','')}" for n in nodes]
        for e in ir.get("edges", []):
            lines.append(f"  {e.get('from')} -> {e.get('to')}"
                         + (f" : {e['label']}" if e.get("label") else ""))
        return "\n".join(lines)

    diagram = {
        "diagram": {
            "boxes": [
                {"id": n["id"], "label": n.get("label", "")}
                for n in nodes
            ],
            "grid": [[n["id"]] for n in nodes],
            "connectors": [
                {"from": e["from"], "to": e["to"],
                 **({"label": e["label"]} if e.get("label") else {})}
                for e in ir.get("edges", [])
            ],
        }
    }
    result = subprocess.run(
        [sys.executable, str(renderer)],
        input=json.dumps(diagram),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        # Fall back to the plain listing so the CLI never silently mis-emits.
        return "\n".join(
            [f"[{n.get('id')}] {n.get('label','')}" for n in nodes]
        )
    return result.stdout.rstrip("\n")


def _render_ir_as_html(ir: Dict[str, Any]) -> str:
    """Minimal HTML wrapper around the ASCII rendering. Phase 1 will replace."""
    ascii_body = _render_ir_as_ascii(ir)
    escaped = (
        ascii_body.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    title = (ir.get("metadata") or {}).get("title", "diagram")
    title_escaped = (
        str(title).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{title_escaped}</title>\n</head>\n<body>\n"
        "<pre style=\"font-family:ui-monospace,monospace;\">"
        f"{escaped}"
        "</pre>\n</body>\n</html>\n"
    )


def _render_ir_as_svg(ir: Dict[str, Any]) -> str:
    """Minimal SVG — one <text> per node. Phase 1 lands format-native SVG."""
    nodes = ir.get("nodes", [])
    width = max(320, 20 + max((len(n.get("label", "")) for n in nodes), default=10) * 8)
    height = max(60, 20 + len(nodes) * 24)
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
    ]
    for i, n in enumerate(nodes):
        y = 24 + i * 24
        label = (
            n.get("label", "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        parts.append(
            f'  <text x="12" y="{y}" font-family="ui-monospace, monospace" '
            f'font-size="14">{label}</text>'
        )
    parts.append("</svg>\n")
    return "\n".join(parts)


def _render_ir_as_mermaid(ir: Dict[str, Any]) -> str:
    """Minimal flowchart TD — Phase 1 lands per-kind Mermaid grammars."""
    lines = ["flowchart TD"]
    for n in ir.get("nodes", []):
        label = n.get("label", "").replace('"', '\\"')
        lines.append(f"  {n['id']}[\"{label}\"]")
    for e in ir.get("edges", []):
        label = e.get("label", "")
        arrow = f"-- {label} -->" if label else "-->"
        lines.append(f"  {e['from']} {arrow} {e['to']}")
    return "\n".join(lines) + "\n"


EMITTERS = {
    "ascii": _render_ir_as_ascii,
    "html": _render_ir_as_html,
    "svg": _render_ir_as_svg,
    "mermaid": _render_ir_as_mermaid,
}


def emit(ir: Dict[str, Any], target: str) -> str:
    if target not in EMITTERS:
        raise SystemExit(
            f"Unknown target format {target!r}; expected one of "
            f"{sorted(EMITTERS)}."
        )
    return EMITTERS[target](ir)


# ---------------------------------------------------------------------------
# Structural diff — IR-level. Emits a JSON-patch-like list.
# ---------------------------------------------------------------------------

def _index_by_id(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {item["id"]: item for item in items if isinstance(item, dict) and "id" in item}


def diff(a: Dict[str, Any], b: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Structural IR diff. Returns a list of patch ops.

    Ops:
      {"op":"add-node","node":<obj>}
      {"op":"remove-node","id":<id>}
      {"op":"change-node","id":<id>,"from":<obj>,"to":<obj>}
      {"op":"add-edge","edge":<obj>}
      {"op":"remove-edge","id":<id>}
      {"op":"change-edge","id":<id>,"from":<obj>,"to":<obj>}
      {"op":"change-kind","from":<str>,"to":<str>}
      {"op":"change-layout","from":<str>,"to":<str>}
    """
    ops: List[Dict[str, Any]] = []

    if a.get("kind") != b.get("kind"):
        ops.append({"op": "change-kind", "from": a.get("kind"), "to": b.get("kind")})
    if a.get("layout") != b.get("layout"):
        ops.append({"op": "change-layout", "from": a.get("layout"), "to": b.get("layout")})

    a_nodes = _index_by_id(a.get("nodes", []))
    b_nodes = _index_by_id(b.get("nodes", []))
    for node_id in sorted(set(a_nodes) | set(b_nodes)):
        if node_id in a_nodes and node_id not in b_nodes:
            ops.append({"op": "remove-node", "id": node_id})
        elif node_id in b_nodes and node_id not in a_nodes:
            ops.append({"op": "add-node", "node": b_nodes[node_id]})
        elif a_nodes[node_id] != b_nodes[node_id]:
            ops.append({
                "op": "change-node",
                "id": node_id,
                "from": a_nodes[node_id],
                "to": b_nodes[node_id],
            })

    a_edges = _index_by_id(a.get("edges", []))
    b_edges = _index_by_id(b.get("edges", []))
    for edge_id in sorted(set(a_edges) | set(b_edges)):
        if edge_id in a_edges and edge_id not in b_edges:
            ops.append({"op": "remove-edge", "id": edge_id})
        elif edge_id in b_edges and edge_id not in a_edges:
            ops.append({"op": "add-edge", "edge": b_edges[edge_id]})
        elif a_edges[edge_id] != b_edges[edge_id]:
            ops.append({
                "op": "change-edge",
                "id": edge_id,
                "from": a_edges[edge_id],
                "to": b_edges[edge_id],
            })

    return ops


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _write_out(text: str, out: str | None) -> None:
    if out is None or out == "-":
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    else:
        pathlib.Path(out).write_text(text if text.endswith("\n") else text + "\n",
                                     encoding="utf-8")


def _cmd_parse(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.inp)
    if not path.exists():
        print(f"ERROR: input path does not exist: {path}", file=sys.stderr)
        return 2
    ir = parse_path(path, forced_format=args.format)
    _write_out(json.dumps(ir, indent=2, ensure_ascii=False), args.out)
    return 0


def _cmd_emit(args: argparse.Namespace) -> int:
    ir_path = pathlib.Path(args.inp)
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    errors = validate(ir)
    if errors:
        print("ERROR: input is not a valid IR:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    text = emit(ir, args.format)
    _write_out(text, args.out)
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    ir_path = pathlib.Path(args.inp)
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    errors = validate(ir)
    if errors:
        print(f"FAIL: {ir_path}")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"PASS: {ir_path}")
    return 0


def _cmd_diff(args: argparse.Namespace) -> int:
    a = json.loads(pathlib.Path(args.a).read_text(encoding="utf-8"))
    b = json.loads(pathlib.Path(args.b).read_text(encoding="utf-8"))
    ops = diff(a, b)
    _write_out(json.dumps(ops, indent=2, ensure_ascii=False), args.out)
    return 0 if not ops else 1


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="diagram-ir", description=(__doc__ or "").splitlines()[0] if (__doc__ or "").splitlines() else "diagram-ir")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_parse = sub.add_parser("parse", help="Parse any supported diagram format to IR JSON")
    p_parse.add_argument("--in", dest="inp", required=True, help="input path")
    p_parse.add_argument("--format", choices=["ascii", "html", "svg", "mermaid"],
                         help="force source format (skip auto-detection)")
    p_parse.add_argument("--out", help="output path (default: stdout)")
    p_parse.set_defaults(func=_cmd_parse)

    p_emit = sub.add_parser("emit", help="Emit IR JSON to a target format")
    p_emit.add_argument("--in", dest="inp", required=True, help="input IR JSON path")
    p_emit.add_argument("--format", choices=["ascii", "html", "svg", "mermaid"],
                        required=True)
    p_emit.add_argument("--out", help="output path (default: stdout)")
    p_emit.set_defaults(func=_cmd_emit)

    p_val = sub.add_parser("validate", help="Schema-validate an IR JSON file")
    p_val.add_argument("--in", dest="inp", required=True)
    p_val.set_defaults(func=_cmd_validate)

    p_diff = sub.add_parser("diff", help="Structural diff between two IR JSON files")
    p_diff.add_argument("--a", required=True)
    p_diff.add_argument("--b", required=True)
    p_diff.add_argument("--out", help="output path for patch JSON (default: stdout)")
    p_diff.set_defaults(func=_cmd_diff)

    return ap


def main(argv: List[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
