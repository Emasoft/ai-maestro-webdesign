#!/usr/bin/env python3
"""parse-html-diagram.py — HTML (and HTML + inline SVG) → diagram-ir/1.0 JSON.

CLI
---
    parse-html-diagram.py [--in <path>|-] [--out <path>]

    --in  <path>   Input HTML file. Use `-` to read from stdin. Default: stdin.
    --out <path>   Output JSON file. Omitted = stdout.

Exit codes
----------
    0  Success — IR emitted and internally validated.
    1  Parse error (unreadable input, malformed HTML beyond our tolerance).
    2  Invalid IR produced (internal bug — should never happen).

Parse strategy (three branches, checked in order)
-------------------------------------------------
1. INLINE-SVG branch. If the HTML contains an inline `<svg>` element,
   treat the SVG's children as diagram primitives:
     - `<rect>`          → IR node. `id` from the `id` attribute if present,
                          else synthesized (`n0`, `n1`, ...). Label from
                          `data-label`, the nearest `<text>` element whose
                          position overlaps the rect, or the rect's `id`.
     - `<line>` / `<path>` with an arrow marker (`marker-end`, `marker-start`,
       or a path `d` that forms a line/arrow) → IR edge. `from` / `to` resolve
       to the rect nodes whose centers are closest to each endpoint.
     - `<text>` not geometrically inside any rect → attached as a trailing
       `annotation` node labeled with the text content.
   Result: `kind: "arch"` when >=3 rects are stacked vertically (layered),
   else `kind: "flowchart"` with `layout: "freeform"`.

2. SEMANTIC-LANDMARK branch. No inline SVG found. Extract HTML5 semantic
   landmarks as IR nodes:
     - `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`,
       `<aside>` each become a node with `kind: "arch"`.
     - Internal `href="#id"` links between sections become IR edges.
     - `data-*` attribute overrides: `data-diagram-id` wins over the element's
       own `id`; `data-diagram-label` wins over the element's heading text;
       `data-diagram-edge-to="<id>,<id>"` adds edges irrespective of anchors.
   Result: always `kind: "arch"`, `layout: "layered"`.

3. FREEFORM FALLBACK. No inline SVG AND no semantic landmarks. Emit a
   single-node IR with `kind: "freeform"`, `layout: "freeform"`, and a
   one-line summary of the HTML (title + first text snippet) as the node
   label. `style.shape` set to `"rect"` per spec. This is the documented
   fail-safe for arbitrary non-semantic HTML (e.g. a `<div>` soup).

Metadata
--------
    metadata.title        = <title>…</title> text when present.
    metadata.description  = <meta name="description" content="…"> when present.
    metadata.source       = input path (or "<stdin>").
    source_format         = "html" (always — this parser writes HTML IRs).

Implementation notes
--------------------
- Primary parser: `html.parser.HTMLParser` from the stdlib. A minimal
  subclass is used for the semantic-landmark and freeform branches.
- Optional: `lxml` and `beautifulsoup4` are detected at import time; when
  available they're used for the inline-SVG branch because SVG geometry
  extraction is significantly more reliable with a real XML parser.
- No hard dependency on lxml / bs4. The stdlib path produces valid IR for
  all three branches.
- Fail-fast. No broad `except`. Only the FREEFORM FALLBACK is a "fallback",
  and it's documented above — not an error recovery.

Limitations (known, acceptable for MVP)
---------------------------------------
- SVG endpoint resolution uses rect-center nearest-neighbor. Overlapping
  rects with very close centers may resolve the wrong edge target; an
  author who relies on precise endpoints should use `data-diagram-edge-to`.
- `<path>` parsing is minimal — we extract the first `M` and last point of
  the `d` attribute. Complex curves are treated as straight lines for
  endpoint purposes.
- Nested semantic landmarks (e.g. a `<section>` inside another `<section>`)
  are both emitted as separate nodes; no implicit parent-child edge is
  synthesized.
- `<text>`-inside-rect detection uses bbox-overlap, not transform-aware
  projection. SVGs that rely on `transform="translate(...)"` to position
  text over rects may miss the association.
- PNG, external CSS / JS, base64 images, iframes, and responsive
  breakpoints are all ignored per the HTML-lossy-parse table in
  references/ir-schema.md §5.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

# Optional dependencies — detected at import time, never required.
# We only check availability (parser uses the stdlib HTMLParser on this path),
# so import the module itself instead of a symbol — keeps ruff F401 clean
# while still surfacing _HAS_BS4 to downstream branches that may want to
# delegate to a richer parser when bs4 is present.
try:
    import bs4  # type: ignore  # noqa: F401

    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

try:
    import lxml.etree  # type: ignore  # noqa: F401

    _HAS_LXML = True
except ImportError:
    _HAS_LXML = False


IR_VERSION = "diagram-ir/1.0"
SOURCE_FORMAT = "html"

SEMANTIC_TAGS = {"header", "nav", "main", "section", "article", "footer", "aside"}

ID_SAFE_RE = re.compile(r"[^A-Za-z0-9_\-]+")


# ---------------------------------------------------------------------------
# IR validation (minimal, self-contained — mirrors schema.json invariants).
# Kept local so this script has zero runtime dependency on diagram-ir.py.
# ---------------------------------------------------------------------------


def _validate_ir(ir: Dict[str, Any]) -> List[str]:
    """Return a list of error strings. Empty list = PASS.

    Enforces the rules from schema.json + ir-schema.md §8:
      - format == "diagram-ir/1.0"
      - source_format in allowed set
      - kind / layout in allowed sets
      - node.id matches [A-Za-z0-9_\\-]+
      - every edge.from / edge.to references an existing node.id
    """
    errors: List[str] = []
    if not isinstance(ir, dict):
        return ["ir: not a dict"]

    if ir.get("format") != IR_VERSION:
        errors.append(f"format: expected '{IR_VERSION}', got {ir.get('format')!r}")
    if ir.get("source_format") not in {"ascii", "html", "svg", "mermaid"}:
        errors.append(f"source_format: invalid value {ir.get('source_format')!r}")
    if ir.get("kind") not in {
        "flowchart",
        "sequence",
        "state",
        "arch",
        "tree",
        "table",
        "freeform",
    }:
        errors.append(f"kind: invalid value {ir.get('kind')!r}")
    if ir.get("layout") not in {"layered", "grid", "freeform", "sequence"}:
        errors.append(f"layout: invalid value {ir.get('layout')!r}")

    nodes = ir.get("nodes")
    if not isinstance(nodes, list):
        errors.append("nodes: not a list")
        return errors
    edges = ir.get("edges")
    if not isinstance(edges, list):
        errors.append("edges: not a list")
        return errors

    node_ids: set = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{i}]: not a dict")
            continue
        nid = node.get("id")
        if not isinstance(nid, str) or not re.fullmatch(r"[A-Za-z0-9_\-]+", nid):
            errors.append(f"nodes[{i}].id: invalid {nid!r}")
        else:
            node_ids.add(nid)
        if not isinstance(node.get("label"), str):
            errors.append(f"nodes[{i}].label: not a string")

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{i}]: not a dict")
            continue
        eid = edge.get("id")
        if not isinstance(eid, str) or not re.fullmatch(r"[A-Za-z0-9_\-]+", eid):
            errors.append(f"edges[{i}].id: invalid {eid!r}")
        frm, to = edge.get("from"), edge.get("to")
        if frm not in node_ids:
            errors.append(f"edges[{i}].from: dangling reference {frm!r}")
        if to not in node_ids:
            errors.append(f"edges[{i}].to: dangling reference {to!r}")

    return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_id(raw: str, fallback: str) -> str:
    """Coerce any string into schema-valid id chars. Empty -> fallback."""
    cleaned = ID_SAFE_RE.sub("-", raw).strip("-")
    return cleaned or fallback


def _unique_id(base: str, used: set) -> str:
    """Return `base` if unused, else base-2, base-3, ..."""
    if base not in used:
        used.add(base)
        return base
    i = 2
    while f"{base}-{i}" in used:
        i += 1
    chosen = f"{base}-{i}"
    used.add(chosen)
    return chosen


def _parse_float(val: Optional[str], default: float = 0.0) -> float:
    """Parse an SVG coordinate string to float. Non-numeric -> default."""
    if val is None:
        return default
    try:
        return float(val.strip().rstrip("px"))
    except ValueError:
        return default


# ---------------------------------------------------------------------------
# HTML parser — collects everything we need in a single pass.
# ---------------------------------------------------------------------------


class _HTMLCollector(HTMLParser):
    """Single-pass HTML collector.

    Tracks:
      - <title> text
      - <meta name="description" content="...">
      - <svg>...</svg> raw source (captured verbatim for the inline-SVG branch)
      - Top-level semantic landmarks with their id / data-* attrs and
        first visible text (used as label fallback).
      - Anchor references `<a href="#id">` grouped by the enclosing landmark.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: List[str] = []
        self.meta_description: Optional[str] = None
        # SVG capture
        self.svg_depth = 0
        self._svg_buffer: List[str] = []
        self.svg_sources: List[str] = []
        # Semantic landmark stack
        self.landmarks: List[Dict[str, Any]] = []
        self._landmark_stack: List[Dict[str, Any]] = []
        # Flag stacks
        self._in_title = False
        self._heading_depth = 0
        self._heading_text: List[str] = []

    # -- tag handling -------------------------------------------------------

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attr_map = {k: (v or "") for k, v in attrs}

        # SVG capture — once we enter an <svg>, capture raw source until close.
        if tag == "svg" or self.svg_depth > 0:
            self._svg_buffer.append(self.get_starttag_text() or f"<{tag}>")
            if tag == "svg":
                self.svg_depth += 1
            return

        if tag == "title":
            self._in_title = True
            return

        if tag == "meta":
            name = attr_map.get("name", "").lower()
            if name == "description":
                self.meta_description = attr_map.get("content") or None
            return

        if tag in SEMANTIC_TAGS:
            landmark = {
                "tag": tag,
                "attrs": attr_map,
                "heading": "",
                "anchors": [],
                "_first_text_chunks": [],
            }
            self.landmarks.append(landmark)
            self._landmark_stack.append(landmark)
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self._landmark_stack:
            self._heading_depth += 1
            self._heading_text = []
            return

        if tag == "a" and self._landmark_stack:
            href = attr_map.get("href", "")
            if href.startswith("#") and len(href) > 1:
                self._landmark_stack[-1]["anchors"].append(href[1:])
            return

    def handle_endtag(self, tag: str) -> None:
        # SVG close — write end tag, decrement depth, flush on exit.
        if self.svg_depth > 0:
            self._svg_buffer.append(f"</{tag}>")
            if tag == "svg":
                self.svg_depth -= 1
                if self.svg_depth == 0:
                    self.svg_sources.append("".join(self._svg_buffer))
                    self._svg_buffer = []
            return

        if tag == "title":
            self._in_title = False
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self._heading_depth > 0:
            if self._landmark_stack and not self._landmark_stack[-1]["heading"]:
                joined = "".join(self._heading_text).strip()
                if joined:
                    self._landmark_stack[-1]["heading"] = joined
            self._heading_depth -= 1
            self._heading_text = []
            return

        if tag in SEMANTIC_TAGS and self._landmark_stack:
            self._landmark_stack.pop()
            return

    def handle_startendtag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        # Handle self-closing tags (e.g. <meta />, <br />) exactly like start.
        self.handle_starttag(tag, attrs)
        # Only truly void elements don't need a matching end — but we still
        # emit one into the SVG buffer to keep the capture balanced.
        if self.svg_depth > 0 and tag not in {"meta", "br", "hr", "img", "input"}:
            if self._svg_buffer and self._svg_buffer[-1].endswith("/>"):
                return  # already self-closed in the starttag text
            self._svg_buffer.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self.svg_depth > 0:
            self._svg_buffer.append(data)
            return
        if self._in_title:
            self.title_parts.append(data)
            return
        if self._heading_depth > 0:
            self._heading_text.append(data)
        if self._landmark_stack and len(self._landmark_stack[-1]["_first_text_chunks"]) < 5:
            stripped = data.strip()
            if stripped:
                self._landmark_stack[-1]["_first_text_chunks"].append(stripped)


# ---------------------------------------------------------------------------
# Inline-SVG branch
# ---------------------------------------------------------------------------


def _parse_svg_to_ir(
    svg_source: str,
    title: Optional[str],
    description: Optional[str],
    source_path: str,
) -> Optional[Dict[str, Any]]:
    """Parse a single inline SVG string into IR.

    Returns None if the SVG contains no rects — caller falls through to the
    semantic-landmark branch.
    """
    # Use ElementTree from stdlib. Strip the default SVG namespace so our
    # xpath-ish `.findall('rect')` actually matches.
    import xml.etree.ElementTree as ET

    # Strip namespace declarations — ET's namespace handling is awkward.
    source_clean = re.sub(r'\sxmlns(:[a-zA-Z0-9_-]+)?="[^"]*"', "", svg_source)
    # Strip namespace prefixes on tags (e.g. `<svg:rect>` -> `<rect>`).
    source_clean = re.sub(r"<(/?)([a-zA-Z0-9_-]+:)", r"<\1", source_clean)

    try:
        root = ET.fromstring(source_clean)
    except ET.ParseError as exc:
        print(f"parse-html-diagram: SVG parse error: {exc}", file=sys.stderr)
        return None

    rects: List[Dict[str, Any]] = []
    lines: List[Dict[str, Any]] = []
    paths: List[Dict[str, Any]] = []
    texts: List[Dict[str, Any]] = []

    def _walk(elem: ET.Element) -> None:
        tag = elem.tag.lower()
        if tag == "rect":
            rects.append(
                {
                    "x": _parse_float(elem.get("x"), 0.0),
                    "y": _parse_float(elem.get("y"), 0.0),
                    "w": _parse_float(elem.get("width"), 0.0),
                    "h": _parse_float(elem.get("height"), 0.0),
                    "id": elem.get("id") or "",
                    "label": elem.get("data-label") or "",
                }
            )
        elif tag == "line":
            lines.append(
                {
                    "x1": _parse_float(elem.get("x1"), 0.0),
                    "y1": _parse_float(elem.get("y1"), 0.0),
                    "x2": _parse_float(elem.get("x2"), 0.0),
                    "y2": _parse_float(elem.get("y2"), 0.0),
                    "id": elem.get("id") or "",
                    "has_arrow": bool(
                        elem.get("marker-end") or elem.get("marker-start")
                    ),
                }
            )
        elif tag == "path":
            d_attr = elem.get("d", "")
            endpoints = _path_endpoints(d_attr)
            if endpoints is not None:
                paths.append(
                    {
                        "x1": endpoints[0],
                        "y1": endpoints[1],
                        "x2": endpoints[2],
                        "y2": endpoints[3],
                        "id": elem.get("id") or "",
                        "has_arrow": bool(
                            elem.get("marker-end") or elem.get("marker-start")
                        ),
                    }
                )
        elif tag == "text":
            # ET concatenates only the immediate .text; include tail'd tspans.
            content_parts: List[str] = []
            if elem.text:
                content_parts.append(elem.text)
            for child in elem:
                if child.text:
                    content_parts.append(child.text)
                if child.tail:
                    content_parts.append(child.tail)
            content = " ".join(p.strip() for p in content_parts if p.strip())
            texts.append(
                {
                    "x": _parse_float(elem.get("x"), 0.0),
                    "y": _parse_float(elem.get("y"), 0.0),
                    "text": content,
                }
            )
        for child in elem:
            _walk(child)

    _walk(root)

    if not rects:
        return None

    # Build nodes.
    used_ids: set = set()
    nodes: List[Dict[str, Any]] = []
    for i, rect in enumerate(rects):
        raw_id = rect["id"] or f"n{i}"
        node_id = _unique_id(_safe_id(raw_id, f"n{i}"), used_ids)
        label = rect["label"]
        if not label:
            # Find any text whose point lies inside this rect's bbox.
            for t in texts:
                if (
                    rect["x"] <= t["x"] <= rect["x"] + rect["w"]
                    and rect["y"] <= t["y"] <= rect["y"] + rect["h"]
                    and t["text"]
                ):
                    label = t["text"]
                    t["consumed"] = True
                    break
        if not label:
            label = node_id
        node = {
            "id": node_id,
            "label": label,
            "bbox": {
                "x": rect["x"],
                "y": rect["y"],
                "w": rect["w"],
                "h": rect["h"],
            },
            "style": {"shape": "rect"},
        }
        nodes.append(node)

    # Annotations: unconsumed <text> elements become a single appended node.
    loose_texts = [t["text"] for t in texts if t.get("text") and not t.get("consumed")]
    if loose_texts:
        annot_id = _unique_id("annotations", used_ids)
        nodes.append(
            {
                "id": annot_id,
                "label": " | ".join(loose_texts),
                "style": {"shape": "rect"},
                "annotations": ["annotation"],
            }
        )

    # Build edges from <line> and arrow-bearing <path>.
    edges: List[Dict[str, Any]] = []
    used_edge_ids: set = set()
    edge_candidates = [
        *({**ln, "kind": "line"} for ln in lines if ln["has_arrow"]),
        *({**p, "kind": "path"} for p in paths if p["has_arrow"]),
    ]
    if not edge_candidates:
        # Also consider non-arrow lines — an author may have forgotten the
        # marker. Better an edge than a silent drop.
        edge_candidates = [
            *({**ln, "kind": "line"} for ln in lines),
            *({**p, "kind": "path"} for p in paths),
        ]

    for i, candidate in enumerate(edge_candidates):
        src = _closest_rect(candidate["x1"], candidate["y1"], rects, nodes)
        dst = _closest_rect(candidate["x2"], candidate["y2"], rects, nodes)
        if src is None or dst is None or src == dst:
            continue
        raw_eid = candidate.get("id") or f"e{i}"
        eid = _unique_id(_safe_id(raw_eid, f"e{i}"), used_edge_ids)
        edges.append(
            {
                "id": eid,
                "from": src,
                "to": dst,
                "style": {"arrow": "solid", "head": "triangle"},
            }
        )

    # Choose kind / layout.
    stacked = _looks_stacked_vertically(rects)
    kind = "arch" if stacked else "flowchart"
    layout = "layered" if stacked else "freeform"

    metadata: Dict[str, Any] = {"source": source_path}
    if title:
        metadata["title"] = title
    if description:
        metadata["description"] = description

    return {
        "format": IR_VERSION,
        "source_format": SOURCE_FORMAT,
        "kind": kind,
        "layout": layout,
        "nodes": nodes,
        "edges": edges,
        "metadata": metadata,
    }


def _path_endpoints(d_attr: str) -> Optional[Tuple[float, float, float, float]]:
    """Extract start + end point of an SVG path `d`.

    Minimal — handles the common `M x y L x y ... ` and `M x y H x V y` forms.
    Returns None if we can't find at least a start and an end.
    """
    # Tokenize: command letters + numbers.
    tokens = re.findall(r"([MLHVCQZAmlhvcqza])|(-?\d+(?:\.\d+)?)", d_attr)
    cmd: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    start: Optional[Tuple[float, float]] = None
    numbers: List[float] = []

    def _flush() -> None:
        nonlocal x, y, start, numbers
        if cmd in {"M", "m", "L", "l"} and len(numbers) >= 2:
            nx, ny = numbers[0], numbers[1]
            if cmd in {"m", "l"} and x is not None and y is not None:
                nx += x
                ny += y
            x, y = nx, ny
            if start is None:
                start = (nx, ny)
        elif cmd in {"H", "h"} and numbers:
            nx = numbers[0]
            if cmd == "h" and x is not None:
                nx += x
            x = nx
        elif cmd in {"V", "v"} and numbers:
            ny = numbers[0]
            if cmd == "v" and y is not None:
                ny += y
            y = ny
        numbers = []

    for letter, number in tokens:
        if letter:
            _flush()
            cmd = letter
        elif number:
            numbers.append(float(number))
    _flush()

    if start is None or x is None or y is None:
        return None
    return (start[0], start[1], x, y)


def _closest_rect(
    x: float, y: float, rects: List[Dict[str, Any]], nodes: List[Dict[str, Any]]
) -> Optional[str]:
    """Return the id of the rect whose center is nearest (x, y)."""
    best: Optional[Tuple[float, str]] = None
    for rect, node in zip(rects, nodes):
        cx = rect["x"] + rect["w"] / 2.0
        cy = rect["y"] + rect["h"] / 2.0
        dist = (cx - x) ** 2 + (cy - y) ** 2
        if best is None or dist < best[0]:
            best = (dist, node["id"])
    return best[1] if best else None


def _looks_stacked_vertically(rects: List[Dict[str, Any]]) -> bool:
    """Return True if at least 3 rects are arranged top-to-bottom."""
    if len(rects) < 3:
        return False
    # Sort by y. If the horizontal span of centers is narrow (<40% of widest
    # rect width), we treat it as a layered stack.
    if not rects:
        return False
    max_w = max(r["w"] for r in rects) or 1.0
    centers_x = [r["x"] + r["w"] / 2.0 for r in rects]
    span = max(centers_x) - min(centers_x)
    return span < 0.4 * max_w


# ---------------------------------------------------------------------------
# Semantic-landmark branch
# ---------------------------------------------------------------------------


def _parse_landmarks_to_ir(
    landmarks: List[Dict[str, Any]],
    title: Optional[str],
    description: Optional[str],
    source_path: str,
) -> Optional[Dict[str, Any]]:
    """Convert collected landmarks into IR. Returns None if list is empty."""
    if not landmarks:
        return None

    used_ids: set = set()
    id_index: Dict[str, str] = {}  # html id -> node id
    nodes: List[Dict[str, Any]] = []

    for i, lm in enumerate(landmarks):
        attrs = lm["attrs"]
        raw_id = attrs.get("data-diagram-id") or attrs.get("id") or f"{lm['tag']}-{i}"
        node_id = _unique_id(_safe_id(raw_id, f"lm{i}"), used_ids)
        id_index[raw_id] = node_id
        if attrs.get("id"):
            id_index[attrs["id"]] = node_id

        override_label = attrs.get("data-diagram-label")
        label_source = (
            override_label
            or lm["heading"]
            or " ".join(lm["_first_text_chunks"])[:120]
            or lm["tag"].capitalize()
        )
        nodes.append(
            {
                "id": node_id,
                "label": label_source.strip() or lm["tag"].capitalize(),
                "rank": i,
                "style": {"shape": "rect"},
                "annotations": [lm["tag"]],
            }
        )

    # Build edges: anchor hrefs + data-diagram-edge-to overrides.
    used_edge_ids: set = set()
    edges: List[Dict[str, Any]] = []
    for i, lm in enumerate(landmarks):
        src_id = nodes[i]["id"]
        seen_targets: set = set()

        override = lm["attrs"].get("data-diagram-edge-to", "").strip()
        if override:
            for target in (t.strip() for t in override.split(",") if t.strip()):
                if target in id_index and id_index[target] != src_id:
                    seen_targets.add(id_index[target])

        for anchor in lm["anchors"]:
            target_node = id_index.get(anchor)
            if target_node and target_node != src_id:
                seen_targets.add(target_node)

        for target_id in seen_targets:
            eid = _unique_id(
                _safe_id(f"e-{src_id}-{target_id}", f"e{len(edges)}"), used_edge_ids
            )
            edges.append({"id": eid, "from": src_id, "to": target_id})

    metadata: Dict[str, Any] = {"source": source_path}
    if title:
        metadata["title"] = title
    if description:
        metadata["description"] = description

    return {
        "format": IR_VERSION,
        "source_format": SOURCE_FORMAT,
        "kind": "arch",
        "layout": "layered",
        "nodes": nodes,
        "edges": edges,
        "metadata": metadata,
    }


# ---------------------------------------------------------------------------
# Freeform fallback
# ---------------------------------------------------------------------------


def _freeform_ir(
    raw_html: str,
    title: Optional[str],
    description: Optional[str],
    source_path: str,
) -> Dict[str, Any]:
    """Build the documented freeform stub IR.

    Per the spec at top: a single node whose label is a one-line summary
    of the HTML (title + first text) and style.shape == "rect".
    """
    summary_bits: List[str] = []
    if title:
        summary_bits.append(title.strip())
    # Extract the first non-empty text node for a flavor snippet.
    text_only = re.sub(r"<[^>]+>", " ", raw_html)
    text_only = re.sub(r"\s+", " ", text_only).strip()
    if text_only:
        summary_bits.append(text_only[:140])
    summary = " — ".join(b for b in summary_bits if b) or "HTML document (no text)"

    metadata: Dict[str, Any] = {"source": source_path}
    if title:
        metadata["title"] = title
    if description:
        metadata["description"] = description

    return {
        "format": IR_VERSION,
        "source_format": SOURCE_FORMAT,
        "kind": "freeform",
        "layout": "freeform",
        "nodes": [
            {
                "id": "root",
                "label": summary,
                "style": {"shape": "rect"},
                "annotations": ["html-freeform"],
            }
        ],
        "edges": [],
        "metadata": metadata,
    }


# ---------------------------------------------------------------------------
# Top-level parse
# ---------------------------------------------------------------------------


def parse_html(raw_html: str, source_path: str) -> Dict[str, Any]:
    """Parse `raw_html` and return a validated IR dict.

    Raises ValueError on parse failure (caller maps to exit 1).
    """
    collector = _HTMLCollector()
    try:
        collector.feed(raw_html)
        collector.close()
    except Exception as exc:  # HTMLParser raises various — we narrow to msg.
        raise ValueError(f"html.parser failed: {exc}") from exc

    title = "".join(collector.title_parts).strip() or None
    description = collector.meta_description

    # Branch 1: inline SVG.
    for svg in collector.svg_sources:
        ir = _parse_svg_to_ir(svg, title, description, source_path)
        if ir is not None:
            return ir

    # Branch 2: semantic landmarks.
    ir = _parse_landmarks_to_ir(collector.landmarks, title, description, source_path)
    if ir is not None:
        return ir

    # Branch 3: freeform fallback.
    return _freeform_ir(raw_html, title, description, source_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _read_input(path: str) -> Tuple[str, str]:
    """Return (raw, display-path)."""
    if path == "-":
        return sys.stdin.read(), "<stdin>"
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"input not found: {path}")
    return p.read_text(encoding="utf-8"), str(p)


def _write_output(ir: Dict[str, Any], out_path: Optional[str]) -> None:
    text = json.dumps(ir, indent=2, ensure_ascii=False)
    if out_path is None:
        sys.stdout.write(text + "\n")
        return
    pathlib.Path(out_path).write_text(text + "\n", encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="parse-html-diagram",
        description="Parse HTML (+ optional inline SVG) to diagram-ir/1.0 JSON.",
    )
    parser.add_argument(
        "--in",
        dest="in_path",
        default="-",
        help="Input path. Use '-' for stdin (default).",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Output path. Omitted = stdout.",
    )
    args = parser.parse_args(argv)

    try:
        raw, display_path = _read_input(args.in_path)
    except (FileNotFoundError, OSError) as exc:
        print(f"parse-html-diagram: {exc}", file=sys.stderr)
        return 1

    try:
        ir = parse_html(raw, display_path)
    except ValueError as exc:
        print(f"parse-html-diagram: {exc}", file=sys.stderr)
        return 1

    errors = _validate_ir(ir)
    if errors:
        print("parse-html-diagram: produced invalid IR:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 2

    _write_output(ir, args.out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
