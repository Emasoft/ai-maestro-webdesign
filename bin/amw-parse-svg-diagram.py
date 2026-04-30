#!/usr/bin/env python3
"""parse-svg-diagram.py — parse a standalone SVG document into diagram-IR JSON.

This is the Phase 1b SVG parser for the `ai-maestro-webdesign` plugin. It
consumes an SVG document (file or stdin) and emits an IR object whose shape
is defined by `skills/amw-diagram-formats/schema.json` (`diagram-ir/1.0`).

Replaces the `annotations:["raw-source"]` MVP stub that `bin/diagram-ir.py`
currently emits for SVG inputs. A separate wire-up agent will integrate the
call inside `diagram-ir.py::parse_path`; this script does NOT modify that
module.

Parse strategy
--------------
Stdlib only (`xml.etree.ElementTree`). Namespace handling is explicit: the
SVG namespace is `http://www.w3.org/2000/svg` and ElementTree tags are
therefore clark-notation strings like `{http://www.w3.org/2000/svg}rect`.
A local helper `_lname()` strips the namespace so comparisons stay readable.

Node extraction:
- `<rect>`, `<circle>`, `<ellipse>`, `<polygon>` (or a `<g>` whose sole
  geometric child is one of those) become IR nodes.
- Bounding box `{x, y, w, h}` is derived from the SVG attributes of the
  underlying shape (see `_shape_bbox()`). For `<circle>` / `<ellipse>` we
  use centre ± radius/rx/ry. For `<polygon>` we compute the axis-aligned
  bbox over the points.
- Label: the nearest `<text>` element either inside the node's `<g>`
  parent OR whose origin `(x, y)` falls inside the node bbox. If multiple
  candidates, nearest centre wins. Empty labels get the node id.
- `style.shape` is `rect|circle|ellipse|polygon` — mirrors the SVG tag.

Edge extraction:
- `<line>` gives two endpoints directly.
- `<path>` with `d="M x y L x2 y2"` (2-point simple form) — we parse both
  coordinates via a small regex. Curves (`C`, `Q`, `A`, etc.) are NOT
  followed in MVP; the path is skipped with a comment in `metadata.notes`.
- For each endpoint we snap to the nearest node whose bbox centre is
  within `SNAP_RADIUS` units (default 60). Snapping to the node whose
  bbox actually CONTAINS the endpoint wins over pure-distance snapping.
- Arrow direction: if the line/path has `marker-end` and no
  `marker-start`, the direction is (from -> to) as drawn. If both, we
  keep the as-drawn direction and tag `style.head = "triangle"`. If
  neither, `style.head = "none"`.
- Edge label: `<text>` element whose origin is within `LABEL_RADIUS` of
  the edge midpoint.

Kind / layout inference:
- If all node bbox centres share either the same column (std-dev of x <
  30 units) OR same row (std-dev of y < 30 units), `kind = "flowchart"`;
  otherwise `kind = "arch"`.
- If y-coordinates cluster into ≥ 2 horizontal bands and every node in a
  lower band is reached from a node in a higher band,
  `layout = "layered"`. Otherwise `layout = "freeform"`.

Fallback:
- If NO shapes qualify as nodes (e.g. a pure-icon SVG with only `<path>`
  strokes), the IR is emitted with `kind = "freeform"`, `layout =
  "freeform"`, and a single node whose label is
  "Untyped SVG (N elements)". No edges.

Metadata:
- `metadata.title` <- `<title>` element text (first one wins)
- `metadata.description` <- `<desc>` element text (first one wins)

CLI
---
    parse-svg-diagram.py [--in <path>|-] [--out <path>]

`--in -` or omitted `--in` reads stdin. Omitted `--out` writes to stdout.
JSON output uses `indent=2, ensure_ascii=False`.

Exit codes
----------
  0 — success
  1 — XML parse error or SVG structural error
  2 — internal IR validation failed (should not happen; indicates a parser
      bug — the emitted IR is still written to stderr for diagnosis)

Known limitations (MVP)
-----------------------
- Curved `<path>` with `C/Q/A/S/T` commands is not traced; the path is
  skipped and recorded in metadata.
- CSS classes (`<style>` or `class="..."`) are ignored — shape classification
  is by tag only.
- Nested `<g transform="..."/>` is NOT flattened; transforms are ignored.
  Authors who want reliable IR should emit absolute coordinates.
- `<use href="#id">` references are not dereferenced.
- Multi-segment polylines are not emitted as edges (only `<line>` and
  2-point `<path>` are).
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

IR_VERSION = "diagram-ir/1.0"
SVG_NS = "http://www.w3.org/2000/svg"
SNAP_RADIUS = 60.0
LABEL_RADIUS = 80.0
COLUMN_STDDEV_THRESHOLD = 30.0
RANK_BAND_TOLERANCE = 40.0


# ---------------------------------------------------------------------------
# ID sanitizer — IR ids must match ^[A-Za-z0-9_\-]+$
# ---------------------------------------------------------------------------

_ID_SAFE_RE = re.compile(r"[^A-Za-z0-9_\-]")


def _safe_id(raw: str, fallback: str) -> str:
    """Return an IR-safe id. Falls back if sanitization leaves empty."""
    cleaned = _ID_SAFE_RE.sub("_", raw or "")
    cleaned = cleaned.strip("_-")
    return cleaned or fallback


# ---------------------------------------------------------------------------
# Namespace-agnostic local-name helper. ElementTree uses clark notation
# ("{http://www.w3.org/2000/svg}rect") when a default namespace is set.
# ---------------------------------------------------------------------------

def _lname(tag: str) -> str:
    """Strip a `{namespace}` prefix from a clark-notation tag."""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


# ---------------------------------------------------------------------------
# Numeric attribute parsing — SVG allows unit suffixes on some attrs. For
# diagram inputs we expect unitless user-space numbers, but we tolerate
# `px` / trailing whitespace.
# ---------------------------------------------------------------------------

_NUM_RE = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _attr_float(elem: ET.Element, name: str, default: float = 0.0) -> float:
    raw = elem.get(name)
    if raw is None:
        return default
    m = _NUM_RE.match(raw.strip())
    if not m:
        raise ValueError(
            f"attribute {name!r}={raw!r} on <{_lname(elem.tag)}> is not a number"
        )
    return float(m.group(0))


def _parse_points(raw: str) -> List[Tuple[float, float]]:
    """Parse a polygon/polyline `points` attribute into (x, y) tuples."""
    nums = [float(m.group(0)) for m in _NUM_RE.finditer(raw)]
    if len(nums) % 2 != 0:
        raise ValueError(f"points attribute has odd number of values: {raw!r}")
    return list(zip(nums[0::2], nums[1::2]))


# ---------------------------------------------------------------------------
# Shape bbox — axis-aligned bounding box for each supported primitive.
# Returns None if the primitive is unsupported or malformed.
# ---------------------------------------------------------------------------

def _shape_bbox(elem: ET.Element) -> Optional[Dict[str, float]]:
    tag = _lname(elem.tag)
    if tag == "rect":
        x = _attr_float(elem, "x", 0.0)
        y = _attr_float(elem, "y", 0.0)
        w = _attr_float(elem, "width", 0.0)
        h = _attr_float(elem, "height", 0.0)
        if w <= 0 or h <= 0:
            return None
        return {"x": x, "y": y, "w": w, "h": h}
    if tag == "circle":
        cx = _attr_float(elem, "cx", 0.0)
        cy = _attr_float(elem, "cy", 0.0)
        r = _attr_float(elem, "r", 0.0)
        if r <= 0:
            return None
        return {"x": cx - r, "y": cy - r, "w": 2 * r, "h": 2 * r}
    if tag == "ellipse":
        cx = _attr_float(elem, "cx", 0.0)
        cy = _attr_float(elem, "cy", 0.0)
        rx = _attr_float(elem, "rx", 0.0)
        ry = _attr_float(elem, "ry", 0.0)
        if rx <= 0 or ry <= 0:
            return None
        return {"x": cx - rx, "y": cy - ry, "w": 2 * rx, "h": 2 * ry}
    if tag == "polygon":
        pts = elem.get("points")
        if not pts:
            return None
        points = _parse_points(pts)
        if not points:
            return None
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return {"x": min(xs), "y": min(ys), "w": max(xs) - min(xs), "h": max(ys) - min(ys)}
    return None


def _bbox_center(bbox: Dict[str, float]) -> Tuple[float, float]:
    return (bbox["x"] + bbox["w"] / 2.0, bbox["y"] + bbox["h"] / 2.0)


def _bbox_contains(bbox: Dict[str, float], px: float, py: float) -> bool:
    return bbox["x"] <= px <= bbox["x"] + bbox["w"] and bbox["y"] <= py <= bbox["y"] + bbox["h"]


# ---------------------------------------------------------------------------
# Path 'd' attribute — extract first M command + first L command. Returns
# None if the path is not a simple 2-point line.
# ---------------------------------------------------------------------------

_PATH_CMD_RE = re.compile(
    r"([MmLl])\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)[ ,]+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
)


def _simple_path_endpoints(d: str) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Return ((x1,y1),(x2,y2)) if `d` is a 2-point M...L... path. Else None.

    The forbidden curve commands (`C H V Q A S T Z`) cause None so the edge
    is skipped — this is a hard MVP limit documented in the module header.
    """
    cmds = _PATH_CMD_RE.findall(d)
    if len(cmds) != 2:
        return None
    first_op, x1, y1 = cmds[0]
    second_op, x2, y2 = cmds[1]
    if first_op.upper() != "M" or second_op.upper() != "L":
        return None
    # Reject anything else in the string (curves would also match other letters).
    forbidden = re.search(r"[CcSsQqTtAaHhVvZz]", d)
    if forbidden:
        return None
    # Relative `l` means offset from previous point.
    ax = float(x1)
    ay = float(y1)
    if second_op == "l":
        bx = ax + float(x2)
        by = ay + float(y2)
    else:
        bx = float(x2)
        by = float(y2)
    return ((ax, ay), (bx, by))


# ---------------------------------------------------------------------------
# Label resolution — find the best <text> for a node bbox or an edge midpoint.
# ---------------------------------------------------------------------------

def _text_origin(text_elem: ET.Element) -> Tuple[float, float]:
    return (_attr_float(text_elem, "x", 0.0), _attr_float(text_elem, "y", 0.0))


def _text_content(text_elem: ET.Element) -> str:
    """Concatenate <text> and all descendant <tspan> text."""
    parts: List[str] = []
    if text_elem.text:
        parts.append(text_elem.text)
    for child in text_elem.iter():
        if child is text_elem:
            continue
        if child.text:
            parts.append(child.text)
        if child.tail:
            parts.append(child.tail)
    return " ".join(p.strip() for p in parts if p.strip())


def _find_node_label(
    bbox: Dict[str, float],
    group_texts: List[ET.Element],
    all_texts: List[ET.Element],
) -> str:
    # First: any <text> inside the same <g>.
    for t in group_texts:
        content = _text_content(t)
        if content:
            return content
    # Fallback: nearest <text> whose origin is inside the bbox.
    inside: List[Tuple[float, str]] = []
    cx, cy = _bbox_center(bbox)
    for t in all_texts:
        tx, ty = _text_origin(t)
        if _bbox_contains(bbox, tx, ty):
            content = _text_content(t)
            if content:
                dist = math.hypot(tx - cx, ty - cy)
                inside.append((dist, content))
    if inside:
        inside.sort(key=lambda pair: pair[0])
        return inside[0][1]
    return ""


def _find_edge_label(
    midpoint: Tuple[float, float],
    all_texts: List[ET.Element],
    consumed_text_ids: set,
) -> str:
    mx, my = midpoint
    candidates: List[Tuple[float, str, int]] = []
    for i, t in enumerate(all_texts):
        if i in consumed_text_ids:
            continue
        tx, ty = _text_origin(t)
        dist = math.hypot(tx - mx, ty - my)
        if dist <= LABEL_RADIUS:
            content = _text_content(t)
            if content:
                candidates.append((dist, content, i))
    if not candidates:
        return ""
    candidates.sort(key=lambda triple: triple[0])
    dist, content, idx = candidates[0]
    consumed_text_ids.add(idx)
    return content


# ---------------------------------------------------------------------------
# Node discovery — walk the tree, emit one node per shape / group-with-shape.
# ---------------------------------------------------------------------------

_NODE_SHAPES = {"rect", "circle", "ellipse", "polygon"}
# Elements whose subtree is a rendering definition, NOT diagram content.
# Shapes inside these are excluded from node discovery (e.g. the <polygon>
# inside a <marker> is the arrow-head geometry, not a diagram node).
_DEFS_CONTAINERS = {"defs", "marker", "symbol", "clipPath", "mask", "pattern", "filter"}


def _collect_defs_descendants(root: ET.Element) -> set:
    """Return a set of id()s for every element inside a defs/marker/... subtree."""
    excluded: set = set()
    for container in root.iter():
        if _lname(container.tag) in _DEFS_CONTAINERS:
            for descendant in container.iter():
                if descendant is container:
                    continue
                excluded.add(id(descendant))
    return excluded


def _collect_text_elements(root: ET.Element) -> List[ET.Element]:
    defs_excluded = _collect_defs_descendants(root)
    return [
        e for e in root.iter()
        if _lname(e.tag) == "text" and id(e) not in defs_excluded
    ]


def _discover_nodes(
    root: ET.Element, all_texts: List[ET.Element]
) -> Tuple[List[Dict[str, Any]], Dict[int, str]]:
    """Find top-level shape nodes. Return (nodes, element_id->node_id map).

    The element_id map lets edge resolution know which shapes are nodes
    without re-iterating the tree.

    Shapes inside `<defs>`, `<marker>`, `<symbol>`, `<clipPath>`, `<mask>`,
    `<pattern>`, `<filter>` are excluded — they are rendering definitions,
    not diagram content.
    """
    defs_excluded = _collect_defs_descendants(root)
    nodes: List[Dict[str, Any]] = []
    shape_to_node: Dict[int, str] = {}
    seen_ids: set = set()

    def _unique_id(raw: str, fallback: str) -> str:
        base = _safe_id(raw, fallback)
        candidate = base
        counter = 1
        while candidate in seen_ids:
            counter += 1
            candidate = f"{base}_{counter}"
        seen_ids.add(candidate)
        return candidate

    # Pass 1: <g> groups that wrap a single node-shape.
    for g in root.iter():
        if _lname(g.tag) != "g":
            continue
        if id(g) in defs_excluded:
            continue
        shape_children = [c for c in list(g) if _lname(c.tag) in _NODE_SHAPES]
        if len(shape_children) != 1:
            continue
        shape = shape_children[0]
        bbox = _shape_bbox(shape)
        if bbox is None:
            continue
        g_id = g.get("id", "")
        node_id = _unique_id(g_id, f"node_{len(nodes) + 1}")
        texts_in_group = [c for c in list(g) if _lname(c.tag) == "text"]
        label = _find_node_label(bbox, texts_in_group, all_texts) or node_id
        nodes.append({
            "id": node_id,
            "label": label,
            "bbox": bbox,
            "style": {"shape": _lname(shape.tag)},
        })
        shape_to_node[id(shape)] = node_id
        # Mark the group so we don't re-emit the shape below.
        shape_to_node[id(g)] = node_id

    # Pass 2: standalone shapes at any depth NOT already claimed by a group.
    for elem in root.iter():
        tag = _lname(elem.tag)
        if tag not in _NODE_SHAPES:
            continue
        if id(elem) in shape_to_node:
            continue
        if id(elem) in defs_excluded:
            continue
        bbox = _shape_bbox(elem)
        if bbox is None:
            continue
        elem_id = elem.get("id", "")
        node_id = _unique_id(elem_id, f"node_{len(nodes) + 1}")
        label = _find_node_label(bbox, [], all_texts) or node_id
        nodes.append({
            "id": node_id,
            "label": label,
            "bbox": bbox,
            "style": {"shape": tag},
        })
        shape_to_node[id(elem)] = node_id

    return nodes, shape_to_node


# ---------------------------------------------------------------------------
# Edge discovery — <line> and simple 2-point <path>.
# ---------------------------------------------------------------------------

def _nearest_node_id(
    point: Tuple[float, float], nodes: List[Dict[str, Any]]
) -> Optional[str]:
    """Snap a point to a node. Containment wins; else distance within radius."""
    px, py = point
    # Containment priority.
    for n in nodes:
        bbox = n.get("bbox")
        if bbox and _bbox_contains(bbox, px, py):
            return n["id"]
    # Distance fallback.
    best: Optional[Tuple[float, str]] = None
    for n in nodes:
        bbox = n.get("bbox")
        if not bbox:
            continue
        cx, cy = _bbox_center(bbox)
        dist = math.hypot(cx - px, cy - py)
        if best is None or dist < best[0]:
            best = (dist, n["id"])
    if best and best[0] <= SNAP_RADIUS:
        return best[1]
    return None


def _arrow_head(elem: ET.Element) -> str:
    marker_end = elem.get("marker-end")
    marker_start = elem.get("marker-start")
    if marker_end or marker_start:
        return "triangle"
    return "none"


def _discover_edges(
    root: ET.Element,
    nodes: List[Dict[str, Any]],
    all_texts: List[ET.Element],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    defs_excluded = _collect_defs_descendants(root)
    edges: List[Dict[str, Any]] = []
    skipped: List[str] = []
    consumed_text_ids: set = set()
    counter = 0

    def _emit_edge(
        a: Tuple[float, float],
        b: Tuple[float, float],
        elem: ET.Element,
    ) -> None:
        nonlocal counter
        from_id = _nearest_node_id(a, nodes)
        to_id = _nearest_node_id(b, nodes)
        if from_id is None or to_id is None or from_id == to_id:
            skipped.append(
                f"<{_lname(elem.tag)}> endpoints did not snap to distinct nodes"
            )
            return
        counter += 1
        edge_id = _safe_id(elem.get("id", ""), f"edge_{counter}")
        midpoint = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        label = _find_edge_label(midpoint, all_texts, consumed_text_ids)
        edge: Dict[str, Any] = {
            "id": edge_id,
            "from": from_id,
            "to": to_id,
            "style": {"arrow": "solid", "head": _arrow_head(elem)},
        }
        if label:
            edge["label"] = label
        edges.append(edge)

    for elem in root.iter():
        if id(elem) in defs_excluded:
            continue
        tag = _lname(elem.tag)
        if tag == "line":
            x1 = _attr_float(elem, "x1", 0.0)
            y1 = _attr_float(elem, "y1", 0.0)
            x2 = _attr_float(elem, "x2", 0.0)
            y2 = _attr_float(elem, "y2", 0.0)
            _emit_edge((x1, y1), (x2, y2), elem)
        elif tag == "path":
            d = elem.get("d", "")
            endpoints = _simple_path_endpoints(d)
            if endpoints is None:
                skipped.append(f"<path> d={d!r} not a simple 2-point line")
                continue
            _emit_edge(endpoints[0], endpoints[1], elem)

    return edges, skipped


# ---------------------------------------------------------------------------
# Kind + layout inference.
# ---------------------------------------------------------------------------

def _infer_kind(nodes: List[Dict[str, Any]]) -> str:
    if not nodes:
        return "freeform"
    centres = [_bbox_center(n["bbox"]) for n in nodes if n.get("bbox")]
    if len(centres) < 2:
        return "flowchart"
    xs = [c[0] for c in centres]
    ys = [c[1] for c in centres]
    sx = statistics.pstdev(xs) if len(xs) > 1 else 0.0
    sy = statistics.pstdev(ys) if len(ys) > 1 else 0.0
    if sx < COLUMN_STDDEV_THRESHOLD or sy < COLUMN_STDDEV_THRESHOLD:
        return "flowchart"
    return "arch"


def _infer_layout_and_ranks(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> str:
    """Assign ranks in-place if the y-coordinates form clear bands."""
    if not nodes:
        return "freeform"
    with_bbox = [n for n in nodes if n.get("bbox")]
    if len(with_bbox) < 2:
        return "freeform"
    centres = sorted(
        [(_bbox_center(n["bbox"])[1], n) for n in with_bbox], key=lambda pair: pair[0]
    )
    # Cluster by y into bands.
    bands: List[List[Dict[str, Any]]] = [[centres[0][1]]]
    last_y = centres[0][0]
    for y, node in centres[1:]:
        if y - last_y > RANK_BAND_TOLERANCE:
            bands.append([node])
        else:
            bands[-1].append(node)
        last_y = y
    if len(bands) < 2:
        return "freeform"
    for rank, band in enumerate(bands):
        for node in band:
            node["rank"] = rank
    return "layered"


# ---------------------------------------------------------------------------
# Metadata extraction.
# ---------------------------------------------------------------------------

def _first_text(root: ET.Element, local_name: str) -> Optional[str]:
    for elem in root.iter():
        if _lname(elem.tag) == local_name:
            content = _text_content(elem)
            if content:
                return content
    return None


# ---------------------------------------------------------------------------
# Lightweight IR validator — duplicates the schema rules from
# skills/amw-diagram-formats/schema.json just enough to self-check output.
# This is a local belt-and-braces check; bin/diagram-ir.py's full
# validator will run downstream.
# ---------------------------------------------------------------------------

_ID_RE = re.compile(r"^[A-Za-z0-9_\-]+$")


def _validate_ir(ir: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if ir.get("format") != IR_VERSION:
        errors.append(f"format must be {IR_VERSION!r}, got {ir.get('format')!r}")
    if ir.get("source_format") not in {"ascii", "html", "svg", "mermaid"}:
        errors.append(f"invalid source_format: {ir.get('source_format')!r}")
    if ir.get("kind") not in {"flowchart", "sequence", "state", "arch", "tree", "table", "freeform"}:
        errors.append(f"invalid kind: {ir.get('kind')!r}")
    if ir.get("layout") not in {"layered", "grid", "freeform", "sequence"}:
        errors.append(f"invalid layout: {ir.get('layout')!r}")
    nodes = ir.get("nodes", [])
    if not isinstance(nodes, list):
        errors.append("nodes must be a list")
        return errors
    node_ids: set = set()
    for i, n in enumerate(nodes):
        nid = n.get("id", "")
        if not _ID_RE.match(nid):
            errors.append(f"nodes[{i}].id {nid!r} not matching ^[A-Za-z0-9_\\-]+$")
        if "label" not in n:
            errors.append(f"nodes[{i}] missing label")
        node_ids.add(nid)
    edges = ir.get("edges", [])
    if not isinstance(edges, list):
        errors.append("edges must be a list")
        return errors
    for i, e in enumerate(edges):
        eid = e.get("id", "")
        if not _ID_RE.match(eid):
            errors.append(f"edges[{i}].id {eid!r} not matching ^[A-Za-z0-9_\\-]+$")
        if e.get("from") not in node_ids:
            errors.append(f"edges[{i}].from {e.get('from')!r} is not a node id")
        if e.get("to") not in node_ids:
            errors.append(f"edges[{i}].to {e.get('to')!r} is not a node id")
    return errors


# ---------------------------------------------------------------------------
# Top-level parse.
# ---------------------------------------------------------------------------

def parse_svg(svg_text: str) -> Dict[str, Any]:
    """Parse SVG source text into a diagram-IR dict."""
    root = ET.fromstring(svg_text)
    if _lname(root.tag) != "svg":
        raise ValueError(f"root element is <{_lname(root.tag)}>, expected <svg>")

    all_texts = _collect_text_elements(root)
    nodes, _shape_map = _discover_nodes(root, all_texts)
    edges: List[Dict[str, Any]]
    skipped: List[str]

    if not nodes:
        # Fallback: no structural shapes found. Emit a single freeform node
        # whose label reports the element count so downstream tooling sees
        # SOMETHING rather than an empty diagram.
        element_count = sum(1 for _ in root.iter()) - 1  # exclude root itself
        ir: Dict[str, Any] = {
            "format": IR_VERSION,
            "source_format": "svg",
            "kind": "freeform",
            "layout": "freeform",
            "nodes": [{
                "id": "raw",
                "label": f"Untyped SVG ({element_count} elements)",
                "annotations": ["raw-source"],
            }],
            "edges": [],
        }
    else:
        edges, skipped = _discover_edges(root, nodes, all_texts)
        kind = _infer_kind(nodes)
        layout = _infer_layout_and_ranks(nodes, edges)
        ir = {
            "format": IR_VERSION,
            "source_format": "svg",
            "kind": kind,
            "layout": layout,
            "nodes": nodes,
            "edges": edges,
        }
        if skipped:
            ir.setdefault("metadata", {})["notes"] = skipped

    title = _first_text(root, "title")
    desc = _first_text(root, "desc")
    if title or desc:
        meta = ir.setdefault("metadata", {})
        if title:
            meta["title"] = title
        if desc:
            meta["description"] = desc

    return ir


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _read_input(in_arg: Optional[str]) -> str:
    if in_arg is None or in_arg == "-":
        return sys.stdin.read()
    path = pathlib.Path(in_arg)
    if not path.is_file():
        raise FileNotFoundError(f"--in path does not exist: {in_arg}")
    return path.read_text(encoding="utf-8")


def _write_output(text: str, out_arg: Optional[str]) -> None:
    if out_arg is None:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
        return
    pathlib.Path(out_arg).write_text(
        text if text.endswith("\n") else text + "\n", encoding="utf-8"
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="parse-svg-diagram.py",
        description="Parse a standalone SVG document into diagram-IR JSON (diagram-ir/1.0).",
    )
    parser.add_argument("--in", dest="in_arg", default=None,
                        help="path to an SVG file, or '-' for stdin (default: stdin)")
    parser.add_argument("--out", dest="out_arg", default=None,
                        help="path to write IR JSON to (default: stdout)")
    args = parser.parse_args(argv)

    try:
        svg_text = _read_input(args.in_arg)
    except (FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        ir = parse_svg(svg_text)
    except (ET.ParseError, ValueError) as exc:
        print(f"ERROR: SVG parse failed: {exc}", file=sys.stderr)
        return 1

    errors = _validate_ir(ir)
    if errors:
        print("ERROR: emitted IR failed self-validation:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        # Still dump the broken IR to stderr so a human can see what went
        # wrong; stdout stays clean.
        print("\n--- invalid IR follows ---", file=sys.stderr)
        json.dump(ir, sys.stderr, indent=2, ensure_ascii=False)
        sys.stderr.write("\n")
        return 2

    output = json.dumps(ir, indent=2, ensure_ascii=False)
    _write_output(output, args.out_arg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
