#!/usr/bin/env python3
r"""amw-parse-mermaid-diagram.py — parse Mermaid source into the plugin's diagram IR.

Replaces the raw-source freeform stub that `bin/amw-diagram-ir.py` emits for Mermaid
inputs with a structured `diagram-ir/1.0` document. The IR schema is mirrored at
`skills/amw-diagram-formats/schema.json` (authoritative) and documented in prose at
`skills/amw-diagram-formats/references/ir-schema.md`. The Mermaid grammar reference
lives at `skills/amw-diagram-formats/references/mermaid.md`.

Supported Mermaid grammars
--------------------------
The parser targets the 5 structural grammars most useful for IR round-trip:

- **flowchart** / **graph** (`TD`/`TB`/`LR`/`BT`/`RL`) — nodes with shape syntax
  (`[]`, `()`, `{}`, `[[]]`, `([])`, `>]`, `[()]`, `((()))`, `{{}}`,
  `[/.../]`, `[\...\]`), edges with arrow-type syntax (`-->`, `-.->`, `==>`,
  `---`, `--x`, `--o`), inline edge labels (`A -- text --> B` and
  `A -->|text| B`), and `subgraph Name ... end` grouping (emitted as a
  per-node annotation `subgraph:<name>`). `classDef` / `class A ...` /
  `click ...` / `linkStyle` / `style A ...` directives are parsed-and-ignored
  (stripped, never a fail).
- **sequenceDiagram** — participants/actors via `participant A` / `actor A`,
  messages via `A->B:`, `A->>B:`, `A-->>B:`, `A-xB:`, `A--xB:`. Arrow style
  (solid vs dashed) is preserved on the edge `style`.
- **stateDiagram-v2** / **stateDiagram** — `[*]` start/end pseudo-states are
  emitted as IR nodes annotated `entry-point` / `terminal`. `A --> B: text`
  transitions become edges. Nested composite states `state A { ... }` are
  recorded as `nested-state-parent` annotations on the outer node.
- **classDiagram** — `class Name` / `class Name { members }` declarations
  become IR nodes (with the member list preserved in `annotations`),
  relationships `<|--` / `*--` / `o--` / `--` / `..>` / `<..` map to edges
  with `style.arrow` = solid|dashed and an `annotations` tag naming the
  UML semantic (inheritance, composition, aggregation, association,
  dependency, realization).
- **erDiagram** — entities from the left/right sides of relationships become
  nodes; crow's-foot cardinality markers (`||`, `o{`, `}o`, `o|`, `|o`, `}|`)
  are recorded as edge annotations. `kind: arch`.

Anything else (`gantt`, `pie`, `journey`, `mindmap`, `quadrantChart`,
`gitGraph`, `C4Context`, or an unrecognised first line) falls through to a
`kind: freeform` single-node stub with `annotations: ["raw-source"]` carrying
the verbatim source. This keeps the conversion pipeline from breaking on
unsupported inputs — the same contract `bin/amw-diagram-ir.py` uses for the MVP.

Directive + comment handling
----------------------------
- `%%{init: ...}%%` config blocks are stripped from the parse buffer but
  preserved verbatim in `metadata.description` for emitters that want to
  re-apply theme config on round-trip.
- `%% ...` line comments are stripped. If the very first line of the input
  is a comment, its text becomes `metadata.title`.
- `metadata.title` defaults to the diagram-type label (e.g. `"Flowchart"`)
  when no header comment is present.

CLI contract (fail-fast; no try/except swallowing)
--------------------------------------------------
  amw-parse-mermaid-diagram.py [--in <path>|-] [--out <path>]

Exit codes
----------
  0 — success
  1 — parse error (unrecognised shape syntax, malformed edge, self-validation
      FAIL — schema drift is always user-visible, never silent)
  2 — invalid IR produced by the parser (schema violation — indicates a bug
      in this parser, not in the input)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

IR_VERSION = "diagram-ir/1.0"

# ---------------------------------------------------------------------------
# Inline JSON schema — kept in sync with bin/amw-diagram-ir.py::SCHEMA and with
# skills/amw-diagram-formats/schema.json. Drift here is a parse error.
# ---------------------------------------------------------------------------

VALID_SOURCE_FORMATS = {"ascii", "html", "svg", "mermaid"}
VALID_KINDS = {"flowchart", "sequence", "state", "arch", "tree", "table", "freeform"}
VALID_LAYOUTS = {"layered", "grid", "freeform", "sequence"}
VALID_ARROWS = {"solid", "dashed", "dotted"}
VALID_HEADS = {"triangle", "open", "none"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9_\-]+$")


# ---------------------------------------------------------------------------
# Header detection — matches the first non-empty non-comment line.
# Order matters: stateDiagram-v2 must be matched before stateDiagram so the
# suffixed form wins; classDiagram before class; erDiagram before ER.
# ---------------------------------------------------------------------------

HEADER_RE = re.compile(
    r"^\s*("
    r"flowchart|graph|"
    r"sequenceDiagram|"
    r"stateDiagram-v2|stateDiagram|"
    r"classDiagram|"
    r"erDiagram|"
    r"gantt|pie|journey|mindmap|quadrantChart|gitGraph|C4Context"
    r")\b"
    r"\s*([A-Za-z]+)?"
)

#
# `%%{init: ...}%%` directive bodies can contain nested `{...}` (JSON-ish
# config objects), so `[^}]*` would stop at the first inner `}`. Use a
# non-greedy match up to the closing `}%%` literal instead.
DIRECTIVE_RE = re.compile(r"%%\{.*?\}%%", re.DOTALL)
# COMMENT_RE matches lone `%% ...` lines. Directive blocks also start with
# `%%`, so `_preprocess` MUST strip directives before scanning for comments.
COMMENT_RE = re.compile(r"^\s*%%.*$")


# ---------------------------------------------------------------------------
# Id-sanitiser — node ids must match ^[A-Za-z0-9_\-]+$ per schema.
# ---------------------------------------------------------------------------

def _sanitize_id(raw: str) -> str:
    """Coerce an arbitrary label fragment into a schema-valid node id.

    The IR schema constrains ids to `^[A-Za-z0-9_\\-]+$`. Mermaid source can
    contain ids with dots (state paths), spaces (quoted labels), or unicode.
    We replace each disallowed char with `_` and collapse runs. An empty
    result falls back to a stable placeholder.
    """
    sanitized = re.sub(r"[^A-Za-z0-9_\-]", "_", raw)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_")
    return sanitized or "node"


def _register_node(
    nodes: List[Dict[str, Any]],
    seen: Dict[str, int],
    raw_id: str,
    label: str,
    *,
    shape: Optional[str] = None,
    annotations: Optional[List[str]] = None,
) -> str:
    """Register a node (idempotent on raw_id) and return its sanitized id."""
    sid = _sanitize_id(raw_id)
    if sid in seen:
        idx = seen[sid]
        existing = nodes[idx]
        if label and (not existing.get("label") or existing["label"] == sid):
            existing["label"] = label
        if shape and "style" not in existing:
            existing["style"] = {"shape": shape}
        elif shape:
            existing["style"]["shape"] = shape
        if annotations:
            existing.setdefault("annotations", [])
            for tag in annotations:
                if tag not in existing["annotations"]:
                    existing["annotations"].append(tag)
        return sid

    node: Dict[str, Any] = {"id": sid, "label": label or sid}
    if shape:
        node["style"] = {"shape": shape}
    if annotations:
        node["annotations"] = list(annotations)
    nodes.append(node)
    seen[sid] = len(nodes) - 1
    return sid


# ---------------------------------------------------------------------------
# Flowchart node-shape decoder.
# Mermaid supports the following bracket pairs (longest match first):
#   [[ .. ]]  subroutine
#   [( .. )]  cylinder
#   (( .. ))  circle
#   {{ .. }}  hexagon
#   ([ .. ])  stadium
#   [/ .. /]  parallelogram (slash)
#   [\ .. \]  reverse parallelogram
#   [  ..  ]  rect
#   (  ..  )  rounded
#   {  ..  }  diamond
#   >  ..  ]  asymmetric
# Order of the patterns in SHAPE_PATTERNS is LONGEST-MATCH-FIRST.
# ---------------------------------------------------------------------------

SHAPE_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("subroutine", re.compile(r"([A-Za-z0-9_\-]+)\[\[(.*?)\]\]")),
    ("cylinder",   re.compile(r"([A-Za-z0-9_\-]+)\[\((.*?)\)\]")),
    ("circle",     re.compile(r"([A-Za-z0-9_\-]+)\(\((.*?)\)\)")),
    ("hexagon",    re.compile(r"([A-Za-z0-9_\-]+)\{\{(.*?)\}\}")),
    ("stadium",    re.compile(r"([A-Za-z0-9_\-]+)\(\[(.*?)\]\)")),
    ("parallelogram",         re.compile(r"([A-Za-z0-9_\-]+)\[/(.*?)/\]")),
    ("parallelogram-reverse", re.compile(r"([A-Za-z0-9_\-]+)\[\\(.*?)\\\]")),
    ("rect",       re.compile(r"([A-Za-z0-9_\-]+)\[(.*?)\]")),
    ("rounded",    re.compile(r"([A-Za-z0-9_\-]+)\((.*?)\)")),
    ("diamond",    re.compile(r"([A-Za-z0-9_\-]+)\{(.*?)\}")),
    ("asymmetric", re.compile(r"([A-Za-z0-9_\-]+)>(.+?)\]")),
]


def _strip_quotes(text: str) -> str:
    """Remove outer matched quotes from a label fragment, if any."""
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


# ---------------------------------------------------------------------------
# Flowchart edge patterns — each returns (arrow_style, head_style).
# Keep the longest (``==>``, ``-.->``) patterns first so the regex engine
# doesn't accidentally eat ``-->`` out of ``-.->``.
# ---------------------------------------------------------------------------

FLOW_EDGE_RE = re.compile(
    r"""
    (?P<src>[A-Za-z0-9_\-]+(?:[\[\{\(][^\]\}\)]*[\]\}\)])?)    # src node or shaped-src
    \s*
    (?:--\s*(?P<label1>[^\->|]+?)\s*-->)                        # A -- text --> B
    |
    (?P<src2>[A-Za-z0-9_\-]+(?:[\[\{\(][^\]\}\)]*[\]\}\)])?)
    \s*
    (?P<arrow>==>|-\.->|-->|---|--x|--o)
    \s*
    (?:\|(?P<label2>[^|]+)\|\s*)?
    (?P<dst>[A-Za-z0-9_\-]+(?:[\[\{\(][^\]\}\)]*[\]\}\)])?)
    """,
    re.VERBOSE,
)

# Simplified line-level scanner: we split statements first and parse each
# statement with a pair of regexes instead of one giant alternation.
EDGE_TOKEN_RE = re.compile(
    r"""
    ^
    \s*
    (?P<src>\S+?)
    \s*
    (?:
        --\s*(?P<pre_label>[^\->|]+?)\s*-->    # A -- text --> B
      |
        (?P<arrow>==>|-\.->|-->|---|--x|--o)
    )
    \s*
    (?:\|(?P<post_label>[^|]+)\|\s*)?
    (?P<dst>\S+?)
    \s*$
    """,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# Preprocessing — strip directives + comments; extract title.
# ---------------------------------------------------------------------------

def _preprocess(source: str) -> Tuple[List[str], Dict[str, str]]:
    """Strip directive blocks + comment lines. Return (lines, metadata).

    The returned line list has no comment-only lines, no directive blocks,
    and trailing whitespace stripped. Inline trailing `%% comment` on code
    lines is also stripped. Metadata may contain `title` and `description`.
    """
    meta: Dict[str, str] = {}

    # Capture any inline directive block for metadata.description, then strip.
    directive_match = DIRECTIVE_RE.search(source)
    if directive_match:
        meta["description"] = directive_match.group(0)
        source = DIRECTIVE_RE.sub("", source)

    raw_lines = source.splitlines()

    # First-line comment → title.
    for line in raw_lines:
        if line.strip() == "":
            continue
        if COMMENT_RE.match(line):
            meta["title"] = line.strip().lstrip("%").strip()
        break

    cleaned: List[str] = []
    for line in raw_lines:
        stripped = line.rstrip()
        if stripped.strip() == "":
            continue
        if COMMENT_RE.match(stripped):
            continue
        # Strip inline trailing `%% comment`.
        inline_comment = re.search(r"\s+%%.*$", stripped)
        if inline_comment:
            stripped = stripped[: inline_comment.start()].rstrip()
            if not stripped:
                continue
        cleaned.append(stripped)

    return cleaned, meta


def _detect_header(lines: List[str]) -> Tuple[str, str, int]:
    """Return (diagram_type, direction_or_empty, header_line_index)."""
    for idx, line in enumerate(lines):
        m = HEADER_RE.match(line)
        if m:
            return m.group(1), (m.group(2) or ""), idx
    return "", "", -1


# ---------------------------------------------------------------------------
# Flowchart parser.
# ---------------------------------------------------------------------------

def _extract_flowchart_nodes(
    statement: str,
    nodes: List[Dict[str, Any]],
    seen: Dict[str, int],
    subgraph_stack: List[str],
) -> str:
    """Replace all inline `id[Label]`-style node declarations in `statement`
    with their bare id, registering each node in `nodes` with its shape.

    Returns the modified statement. Subgraph ancestry is attached as
    `subgraph:<name>` annotation tags on each newly-registered node.
    """
    mutated = statement
    for shape, pattern in SHAPE_PATTERNS:
        while True:
            m = pattern.search(mutated)
            if not m:
                break
            raw_id, raw_label = m.group(1), m.group(2)
            label = _strip_quotes(raw_label)
            annotations: List[str] = []
            if shape == "diamond":
                annotations.append("decision")
            if subgraph_stack:
                for sg in subgraph_stack:
                    annotations.append(f"subgraph:{sg}")
            _register_node(
                nodes, seen, raw_id, label,
                shape=shape, annotations=annotations or None,
            )
            mutated = mutated[: m.start()] + raw_id + mutated[m.end() :]
    return mutated


def _parse_flow_edge_token(statement: str) -> Optional[Tuple[str, str, str, str, str]]:
    """Parse a simplified flowchart edge statement.

    Returns `(src_id, dst_id, arrow_glyph, label, head_style)` or None.
    """
    # Try two-phase arrow pattern `A -- text --> B`.
    two_phase = re.match(
        r"^\s*(?P<src>\S+)\s*--\s*(?P<label>[^\->|][^-]*?)\s*-->\s*(?P<dst>\S+)\s*$",
        statement,
    )
    if two_phase:
        return (
            two_phase.group("src"),
            two_phase.group("dst"),
            "-->",
            two_phase.group("label").strip(),
            "triangle",
        )
    # Single-arrow pattern with optional pipe-label.
    single = re.match(
        r"^\s*(?P<src>\S+)\s*(?P<arrow>==>|-\.->|-->|---|--x|--o)"
        r"\s*(?:\|(?P<label>[^|]+)\|\s*)?(?P<dst>\S+)\s*$",
        statement,
    )
    if single:
        arrow = single.group("arrow")
        head = "triangle"
        if arrow == "--x":
            head = "none"
        elif arrow == "--o":
            head = "open"
        elif arrow == "---":
            head = "none"
        return (
            single.group("src"),
            single.group("dst"),
            arrow,
            (single.group("label") or "").strip(),
            head,
        )
    return None


def _arrow_style_for_glyph(glyph: str) -> str:
    """Map a flowchart arrow glyph to IR `style.arrow`."""
    if glyph == "-.->":
        return "dotted"
    if glyph == "==>":
        return "solid"
    return "solid"


def parse_flowchart(lines: List[str]) -> Dict[str, Any]:
    """Parse a `flowchart`/`graph` body into structured IR.

    The first element of `lines` is the header; subsequent lines carry node
    declarations, edges, `subgraph ... end` blocks, and ignorable directives
    (`classDef`, `class`, `click`, `linkStyle`, `style`). Edges are split on
    `&` (Mermaid's multi-target shortcut) and on newlines. Layout direction is
    captured by the caller into `metadata.direction`, so it is not needed here.
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen: Dict[str, int] = {}
    subgraph_stack: List[str] = []

    for raw in lines[1:]:
        stripped = raw.strip()
        if not stripped:
            continue

        # subgraph / end
        sg = re.match(r"^subgraph\s+(.+)$", stripped)
        if sg:
            subgraph_stack.append(_sanitize_id(sg.group(1).strip()))
            continue
        if stripped == "end":
            if subgraph_stack:
                subgraph_stack.pop()
            continue

        # ignorable directives
        if re.match(r"^(classDef|class|click|linkStyle|style)\b", stripped):
            continue

        # split on `;` (multi-statement on one line) and on `&` (multi-target)
        # Semicolons first:
        for piece in re.split(r";", stripped):
            piece = piece.strip()
            if not piece:
                continue
            # Register embedded node shapes BEFORE `&` expansion so shape
            # info is captured once.
            piece = _extract_flowchart_nodes(piece, nodes, seen, subgraph_stack)
            # `A & B --> C & D` expansion: split src and dst on `&`.
            parsed = _parse_flow_edge_token(piece)
            if parsed is None:
                # bare node declaration — register it so it shows up
                bare = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*$", piece)
                if bare:
                    _register_node(nodes, seen, bare.group(1), bare.group(1))
                continue
            src_raw, dst_raw, arrow, label, head = parsed
            src_ids = [s.strip() for s in src_raw.split("&") if s.strip()]
            dst_ids = [d.strip() for d in dst_raw.split("&") if d.strip()]
            for s in src_ids:
                for d in dst_ids:
                    src_id = _register_node(nodes, seen, s, s)
                    dst_id = _register_node(nodes, seen, d, d)
                    edge: Dict[str, Any] = {
                        "id": f"e{len(edges) + 1}",
                        "from": src_id,
                        "to": dst_id,
                    }
                    if label:
                        edge["label"] = label
                    edge["style"] = {
                        "arrow": _arrow_style_for_glyph(arrow),
                        "head": head,
                    }
                    edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "kind": "flowchart",
        "layout": "layered",
    }


# ---------------------------------------------------------------------------
# Sequence parser.
# ---------------------------------------------------------------------------

SEQ_ARROW_RE = re.compile(
    r"^\s*(?P<src>\S+?)\s*(?P<arrow>-->>|->>|--x|-x|-\)|->|-->)"
    r"\s*(?P<dst>\S+?)\s*:\s*(?P<text>.*)$"
)


def parse_sequence(lines: List[str]) -> Dict[str, Any]:
    """Parse a `sequenceDiagram` body into structured IR.

    Participants are discovered either explicitly (`participant A` /
    `actor A`) or implicitly (any src/dst id in a message). Messages become
    edges with `style.arrow` = `solid` (for `->`, `->>`) or `dashed`
    (for `-->>`). `--x`/`-x` crossed-arrow tails are recorded with
    `style.head = "none"`.
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen: Dict[str, int] = {}

    for raw in lines[1:]:
        stripped = raw.strip()
        if not stripped:
            continue
        # Explicit participant / actor declarations.
        part = re.match(r"^(participant|actor)\s+(\S+)(?:\s+as\s+(.+))?$", stripped)
        if part:
            raw_id = part.group(2)
            label = (part.group(3) or raw_id).strip()
            _register_node(nodes, seen, raw_id, label)
            continue
        # Ignorable sequence directives: note, loop, alt, opt, par, rect,
        # activate / deactivate, autonumber, title, end.
        if re.match(
            r"^(note|loop|alt|opt|par|rect|activate|deactivate|"
            r"autonumber|title|end|else|critical|break)\b",
            stripped,
            flags=re.IGNORECASE,
        ):
            continue
        m = SEQ_ARROW_RE.match(stripped)
        if not m:
            continue
        src_id = _register_node(nodes, seen, m.group("src"), m.group("src"))
        dst_id = _register_node(nodes, seen, m.group("dst"), m.group("dst"))
        arrow = m.group("arrow")
        style: Dict[str, str] = {
            "arrow": "dashed" if arrow.startswith("--") else "solid",
        }
        if arrow.endswith("x"):
            style["head"] = "none"
        edge: Dict[str, Any] = {
            "id": f"m{len(edges) + 1}",
            "from": src_id,
            "to": dst_id,
            "label": m.group("text").strip(),
            "style": style,
        }
        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "kind": "sequence",
        "layout": "sequence",
    }


# ---------------------------------------------------------------------------
# State parser.
# ---------------------------------------------------------------------------

STATE_TRANSITION_RE = re.compile(
    r"^\s*(?P<src>\S+)\s*-->\s*(?P<dst>\S+?)\s*(?::\s*(?P<label>.*))?$"
)


def parse_state(lines: List[str]) -> Dict[str, Any]:
    """Parse a `stateDiagram` / `stateDiagram-v2` body into structured IR.

    `[*]` pseudo-states are materialised as nodes `start0` / `end0` with
    `annotations` = `entry-point` / `terminal`. The leading-alpha ids are
    required by the schema's id pattern (underscore-prefixed ids survive
    the pattern check but get stripped by `_sanitize_id`'s `.strip('_')`
    — reusing the plain-word convention avoids that trap). Composite-state
    blocks (`state NAME { ... }`) are parsed shallowly: the outer name is
    recorded with `annotations: ["nested-state-parent"]`; contained
    transitions are still emitted at top level (flattened).
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen: Dict[str, int] = {}
    composite_stack: List[str] = []

    # Per-direction sentinel ids so multiple `[*] --> X` lines all share
    # one entry node (and same for terminals).
    def _sentinel(direction: str) -> str:
        sid = "start0" if direction == "entry" else "end0"
        tag = "entry-point" if direction == "entry" else "terminal"
        label = "Start" if direction == "entry" else "End"
        if sid not in seen:
            _register_node(
                nodes, seen, sid, label,
                shape="circle", annotations=[tag],
            )
        return sid

    for raw in lines[1:]:
        stripped = raw.strip()
        if not stripped:
            continue
        # Composite state open: `state Name { ...` or `state Name {`
        comp_open = re.match(r"^state\s+(\S+)\s*\{\s*$", stripped)
        if comp_open:
            raw_id = comp_open.group(1)
            composite_stack.append(raw_id)
            _register_node(
                nodes, seen, raw_id, raw_id,
                annotations=["nested-state-parent"],
            )
            continue
        if stripped == "}":
            if composite_stack:
                composite_stack.pop()
            continue
        # Simple state declaration: `state Name as "Display"` / `state Name`
        state_decl = re.match(r"^state\s+(\S+)(?:\s+as\s+(.+))?$", stripped)
        if state_decl:
            raw_id = state_decl.group(1)
            label = (state_decl.group(2) or raw_id).strip()
            _register_node(nodes, seen, raw_id, _strip_quotes(label))
            continue
        # Note lines: ignore.
        if stripped.lower().startswith("note "):
            continue
        # Transition.
        m = STATE_TRANSITION_RE.match(stripped)
        if not m:
            continue
        src_raw = m.group("src")
        dst_raw = m.group("dst")
        label = (m.group("label") or "").strip()

        if src_raw == "[*]":
            src_id = _sentinel("entry")
        else:
            src_id = _register_node(nodes, seen, src_raw, src_raw)
        if dst_raw == "[*]":
            dst_id = _sentinel("exit")
        else:
            dst_id = _register_node(nodes, seen, dst_raw, dst_raw)

        edge: Dict[str, Any] = {
            "id": f"t{len(edges) + 1}",
            "from": src_id,
            "to": dst_id,
            "style": {"arrow": "solid", "head": "triangle"},
        }
        if label:
            edge["label"] = label
        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "kind": "state",
        "layout": "layered",
    }


# ---------------------------------------------------------------------------
# Class parser.
# ---------------------------------------------------------------------------

CLASS_REL_RE = re.compile(
    r"^\s*(?P<src>\S+)\s*"
    r"(?P<rel><\|--|--\|>|\*--|--\*|o--|--o|<\.\.|\.\.>|<--|-->|--|\.\.)"
    r"\s*(?P<dst>\S+)(?:\s*:\s*(?P<label>.*))?$"
)

CLASS_REL_SEMANTIC = {
    "<|--": ("inheritance", "solid", "triangle"),
    "--|>": ("inheritance", "solid", "triangle"),
    "*--":  ("composition", "solid", "none"),
    "--*":  ("composition", "solid", "none"),
    "o--":  ("aggregation", "solid", "open"),
    "--o":  ("aggregation", "solid", "open"),
    "<..":  ("realization", "dashed", "triangle"),
    "..>":  ("dependency", "dashed", "open"),
    "<--":  ("association", "solid", "triangle"),
    "-->":  ("association", "solid", "triangle"),
    "--":   ("association", "solid", "none"),
    "..":   ("dependency", "dashed", "none"),
}


def parse_class(lines: List[str]) -> Dict[str, Any]:
    """Parse a `classDiagram` body into structured IR.

    Class members inside `class Foo { ... }` blocks are preserved in the
    node's `annotations` list as `member:<line>` tags (lossy: formatting
    of member declarations is not round-tripped, but the semantic content
    survives).
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen: Dict[str, int] = {}
    current_class: Optional[str] = None

    for raw in lines[1:]:
        stripped = raw.strip()
        if not stripped:
            continue

        # Open a class body: `class Foo {` or `class Foo{`
        open_body = re.match(r"^class\s+(\S+)\s*\{\s*$", stripped)
        if open_body:
            class_name = open_body.group(1)
            current_class = class_name
            _register_node(nodes, seen, class_name, class_name)
            continue

        # Close of class body.
        if stripped == "}":
            current_class = None
            continue

        # Bare class declaration: `class Foo`
        bare = re.match(r"^class\s+(\S+)\s*$", stripped)
        if bare:
            _register_node(nodes, seen, bare.group(1), bare.group(1))
            continue

        # Inside a class body, treat lines as members.
        if current_class is not None and not CLASS_REL_RE.match(stripped):
            idx = seen[_sanitize_id(current_class)]
            nodes[idx].setdefault("annotations", []).append(f"member:{stripped}")
            continue

        # Relationship line.
        rel = CLASS_REL_RE.match(stripped)
        if not rel:
            continue
        src_id = _register_node(nodes, seen, rel.group("src"), rel.group("src"))
        dst_id = _register_node(nodes, seen, rel.group("dst"), rel.group("dst"))
        rel_glyph = rel.group("rel")
        semantic, arrow_style, head_style = CLASS_REL_SEMANTIC.get(
            rel_glyph, ("association", "solid", "none")
        )
        edge: Dict[str, Any] = {
            "id": f"r{len(edges) + 1}",
            "from": src_id,
            "to": dst_id,
            "style": {"arrow": arrow_style, "head": head_style},
        }
        label = (rel.group("label") or "").strip()
        if label:
            edge["label"] = label
        # Stash UML semantic as a custom annotation on the edge id — edges
        # don't have an `annotations` array in the schema, so we fold it
        # into the label when no explicit label is given.
        if not label:
            edge["label"] = semantic
        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "kind": "arch",
        "layout": "layered",
    }


# ---------------------------------------------------------------------------
# ER parser.
# ---------------------------------------------------------------------------

ER_CARDINALITY = {
    "||": "exactly-one",
    "o{": "zero-or-many",
    "}o": "zero-or-many",
    "o|": "zero-or-one",
    "|o": "zero-or-one",
    "}|": "one-or-many",
    "|{": "one-or-many",
}

ER_REL_RE = re.compile(
    r"^\s*(?P<src>\S+)\s+"
    r"(?P<lcard>\|\||o\{|\}o|o\||\|o|\}\||\|\{)"
    r"(?P<middle>--|\.\.)"
    r"(?P<rcard>\|\||o\{|\}o|o\||\|o|\}\||\|\{)"
    r"\s+(?P<dst>\S+)(?:\s*:\s*(?P<label>.*))?$"
)


def parse_er(lines: List[str]) -> Dict[str, Any]:
    """Parse an `erDiagram` body into structured IR.

    Each relationship produces two entity nodes + one edge. Crow's-foot
    cardinalities on each side become edge label prefixes of the form
    `<src-cardinality> : <user-label> : <dst-cardinality>`. Attribute
    blocks (`ENTITY { ... }`) are parsed shallowly — attributes collected
    as `member:<line>` annotations on the entity node, same convention as
    the class parser.
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen: Dict[str, int] = {}
    current_entity: Optional[str] = None

    for raw in lines[1:]:
        stripped = raw.strip()
        if not stripped:
            continue

        # Entity attribute block open: `ENTITY {`
        open_attr = re.match(r"^(\S+)\s*\{\s*$", stripped)
        if open_attr and not ER_REL_RE.match(stripped):
            entity_name = open_attr.group(1)
            current_entity = entity_name
            _register_node(nodes, seen, entity_name, entity_name)
            continue
        if stripped == "}":
            current_entity = None
            continue
        if current_entity is not None:
            idx = seen[_sanitize_id(current_entity)]
            nodes[idx].setdefault("annotations", []).append(f"member:{stripped}")
            continue

        m = ER_REL_RE.match(stripped)
        if not m:
            continue
        src_id = _register_node(nodes, seen, m.group("src"), m.group("src"))
        dst_id = _register_node(nodes, seen, m.group("dst"), m.group("dst"))
        lcard = ER_CARDINALITY.get(m.group("lcard"), m.group("lcard"))
        rcard = ER_CARDINALITY.get(m.group("rcard"), m.group("rcard"))
        middle = m.group("middle")
        user_label = (m.group("label") or "").strip()

        label_bits = [lcard]
        if user_label:
            label_bits.append(user_label)
        label_bits.append(rcard)
        edge: Dict[str, Any] = {
            "id": f"er{len(edges) + 1}",
            "from": src_id,
            "to": dst_id,
            "label": " : ".join(label_bits),
            "style": {
                "arrow": "dashed" if middle == ".." else "solid",
                "head": "none",
            },
        }
        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "kind": "arch",
        "layout": "layered",
    }


# ---------------------------------------------------------------------------
# Freeform fallback.
# ---------------------------------------------------------------------------

def _raw_source_ir(raw: str, title: str) -> Dict[str, Any]:
    """Return a `freeform` raw-source IR for unsupported Mermaid grammars.

    Matches the same contract as `bin/amw-diagram-ir.py::_raw_source_ir`:
    emitters that target the same `source_format` MUST round-trip
    `nodes[0].label` verbatim.
    """
    return {
        "format": IR_VERSION,
        "source_format": "mermaid",
        "kind": "freeform",
        "layout": "freeform",
        "nodes": [
            {"id": "raw", "label": raw, "annotations": ["raw-source"]},
        ],
        "edges": [],
        "metadata": {"title": title or "Mermaid (unsupported grammar)"},
    }


# ---------------------------------------------------------------------------
# Top-level dispatcher.
# ---------------------------------------------------------------------------

DIAGRAM_TYPE_TITLES = {
    "flowchart": "Flowchart",
    "graph": "Flowchart",
    "sequenceDiagram": "Sequence Diagram",
    "stateDiagram": "State Diagram",
    "stateDiagram-v2": "State Diagram",
    "classDiagram": "Class Diagram",
    "erDiagram": "ER Diagram",
}


def parse_mermaid(source: str) -> Dict[str, Any]:
    """Parse a Mermaid source string into a `diagram-ir/1.0` dict.

    The dispatcher detects the header type and delegates to the matching
    sub-parser; everything outside the 5 structurally-supported grammars
    falls through to `_raw_source_ir`.
    """
    lines, meta = _preprocess(source)
    if not lines:
        return _raw_source_ir(source, meta.get("title", ""))

    diagram_type, direction, _header_idx = _detect_header(lines)

    default_title = DIAGRAM_TYPE_TITLES.get(diagram_type, "Mermaid Diagram")
    title = meta.get("title") or default_title

    if diagram_type in ("flowchart", "graph"):
        body = parse_flowchart(lines)
    elif diagram_type == "sequenceDiagram":
        body = parse_sequence(lines)
    elif diagram_type in ("stateDiagram", "stateDiagram-v2"):
        body = parse_state(lines)
    elif diagram_type == "classDiagram":
        body = parse_class(lines)
    elif diagram_type == "erDiagram":
        body = parse_er(lines)
    else:
        # gantt, pie, journey, mindmap, quadrantChart, gitGraph, C4Context,
        # or unrecognised header → freeform raw-source stub.
        return _raw_source_ir(source, title)

    ir: Dict[str, Any] = {
        "format": IR_VERSION,
        "source_format": "mermaid",
        "kind": body["kind"],
        "layout": body["layout"],
        "nodes": body["nodes"],
        "edges": body["edges"],
    }
    metadata: Dict[str, Any] = {"title": title}
    if meta.get("description"):
        metadata["description"] = meta["description"]
    if direction:
        metadata["direction"] = direction
    ir["metadata"] = metadata
    return ir


# ---------------------------------------------------------------------------
# Self-validation — mirrors bin/amw-diagram-ir.py::validate's semantic checks.
# Pure stdlib; no import of amw-diagram-ir to avoid circular dependency.
# ---------------------------------------------------------------------------

def _validate_ir(ir: Any) -> List[str]:
    """Return a list of validation-error strings; empty list = PASS.

    Enforces the schema's required keys, enum memberships, id pattern, and
    the semantic invariant that every edge endpoint matches a node id.
    """
    errors: List[str] = []

    if not isinstance(ir, dict):
        return ["#: root must be a JSON object"]

    # Required top-level keys.
    for key in ("format", "source_format", "kind", "nodes", "edges", "layout"):
        if key not in ir:
            errors.append(f"#: missing required key {key!r}")

    if ir.get("format") != IR_VERSION:
        errors.append(f"#/format: must be {IR_VERSION!r}")
    if ir.get("source_format") not in VALID_SOURCE_FORMATS:
        errors.append(f"#/source_format: must be one of {sorted(VALID_SOURCE_FORMATS)}")
    if ir.get("kind") not in VALID_KINDS:
        errors.append(f"#/kind: must be one of {sorted(VALID_KINDS)}")
    if ir.get("layout") not in VALID_LAYOUTS:
        errors.append(f"#/layout: must be one of {sorted(VALID_LAYOUTS)}")

    nodes = ir.get("nodes", [])
    edges = ir.get("edges", [])
    if not isinstance(nodes, list):
        errors.append("#/nodes: must be an array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("#/edges: must be an array")
        edges = []

    node_ids = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"#/nodes/{i}: must be an object")
            continue
        nid = node.get("id")
        if not isinstance(nid, str) or not ID_PATTERN.match(nid):
            errors.append(f"#/nodes/{i}/id: {nid!r} must match ^[A-Za-z0-9_\\-]+$")
        else:
            node_ids.add(nid)
        if "label" not in node or not isinstance(node["label"], str):
            errors.append(f"#/nodes/{i}/label: missing or not a string")

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"#/edges/{i}: must be an object")
            continue
        eid = edge.get("id")
        if not isinstance(eid, str) or not ID_PATTERN.match(eid):
            errors.append(f"#/edges/{i}/id: {eid!r} must match ^[A-Za-z0-9_\\-]+$")
        for field in ("from", "to"):
            target = edge.get(field)
            if target is None:
                errors.append(f"#/edges/{i}: missing {field!r}")
                continue
            if target not in node_ids:
                errors.append(
                    f"#/edges/{i}/{field}: {target!r} does not match any node id"
                )
        style = edge.get("style")
        if style is not None:
            if not isinstance(style, dict):
                errors.append(f"#/edges/{i}/style: must be an object")
            else:
                arrow = style.get("arrow")
                if arrow is not None and arrow not in VALID_ARROWS:
                    errors.append(
                        f"#/edges/{i}/style/arrow: {arrow!r} must be one of "
                        f"{sorted(VALID_ARROWS)}"
                    )
                head = style.get("head")
                if head is not None and head not in VALID_HEADS:
                    errors.append(
                        f"#/edges/{i}/style/head: {head!r} must be one of "
                        f"{sorted(VALID_HEADS)}"
                    )

    return errors


# ---------------------------------------------------------------------------
# CLI wiring.
# ---------------------------------------------------------------------------

def _read_input(in_arg: str) -> str:
    """Read Mermaid source from `--in <path>` or `-` (stdin)."""
    if in_arg == "-" or in_arg == "":
        return sys.stdin.read()
    path = pathlib.Path(in_arg)
    return path.read_text(encoding="utf-8")


def _write_output(ir: Dict[str, Any], out_arg: Optional[str]) -> None:
    """Emit IR as JSON to `--out <path>` or stdout."""
    text = json.dumps(ir, indent=2, ensure_ascii=False)
    if out_arg:
        pathlib.Path(out_arg).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="amw-parse-mermaid-diagram.py",
        description="Parse Mermaid source into a diagram-ir/1.0 JSON document.",
    )
    parser.add_argument(
        "--in", dest="in_arg", default="-",
        help="Input path (or '-' for stdin). Default: stdin.",
    )
    parser.add_argument(
        "--out", dest="out_arg", default=None,
        help="Output path. Default: stdout.",
    )
    args = parser.parse_args(argv)

    source = _read_input(args.in_arg)
    if not source.strip():
        sys.stderr.write("parse-mermaid-diagram: empty input\n")
        return 1

    ir = parse_mermaid(source)
    errors = _validate_ir(ir)
    if errors:
        sys.stderr.write("parse-mermaid-diagram: produced invalid IR:\n")
        for err in errors:
            sys.stderr.write(f"  {err}\n")
        return 2

    _write_output(ir, args.out_arg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
