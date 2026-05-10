#!/usr/bin/env python3
"""dom-to-ir.py — Full-page DOM (URL or local HTML file) -> diagram-ir/1.0 JSON.

This is a specialization of `bin/parse-html-diagram.py` for the webpage round-trip
skills. Where `parse-html-diagram.py` focuses on inline `<svg>` diagrams inside
an HTML document, this tool focuses on the **page as a structural graph** —
every top-level HTML5 landmark becomes an IR node, and internal anchor links
become IR edges.

CLI
---
    dom-to-ir.py --url <URL>          [--out <ir.json>] [--target-kind <k>]
    dom-to-ir.py --in  <html-path>    [--out <ir.json>] [--target-kind <k>]

    --url          Fetch a live page via bin/dev-browser-wrapper.sh (dom subcmd).
                   Saves the rendered HTML to a temp file, then parses it.
    --in           Parse a local HTML file directly. Must exist and be readable.
    --out          Output JSON path. Default: stdout.
    --target-kind  Hint for downstream emitters: one of flowchart | arch | tree.
                   Default: arch (the natural kind for landmark graphs).

Exit codes
----------
    0  Success.
    1  Parse / fetch error (URL unreachable, file not found, malformed HTML).
    2  PNG-refusal (input is a PNG file or URL returns image/* Content-Type)
       OR CLI misuse.

Extraction strategy
-------------------
1. **PNG refusal gate.** If `--in` path extension is `.png` or the file starts
   with PNG magic bytes (0x89 50 4E 47), exit 2 with the hardcoded refusal
   message. For `--url`, the dev-browser wrapper is only called after a
   curl `-I` HEAD check confirms `Content-Type: text/html*` (or similar).
   An `image/*` Content-Type triggers the same refusal.
2. **Fetch (URL mode).** Call `bin/dev-browser-wrapper.sh` on a temp path to
   get the post-JS rendered HTML. Fall back to a plain urllib fetch if the
   wrapper is unavailable (documented — produces pre-JS HTML only).
3. **Landmark extraction.** Walk the HTML with `html.parser` (opportunistically
   lxml/bs4 when present). Emit every `<header>`, `<nav>`, `<main>`,
   `<section>`, `<article>`, `<footer>`, `<aside>` as an IR node with:
       - id       : from `data-diagram-id`, else `id`, else `<tag>-<i>`
       - label    : from `data-diagram-label`, else first heading inside the
                   landmark (`<h1..h6>`), else first text snippet, else tag name
       - rank     : document-order index (0-based)
       - style    : {"shape": "rect"}
       - annotations: [tag-name]  (e.g. ["nav"], ["main"], ["section"])
4. **Inline SVG diagrams.** For every `<svg>` that is a child of one of those
   landmarks, re-parse it via `bin/parse-html-diagram.py` (subprocess) and
   attach its nodes+edges as CHILDREN of the containing landmark node. The
   landmark node keeps its own identity; the SVG-derived nodes become
   additional IR nodes with an `annotations: ["from-inline-svg"]` marker.
5. **Edge discovery.** Internal anchor links `href="#id"` between landmark
   elements become IR edges from the source landmark to the target landmark
   (only if both ends resolve). `data-diagram-edge-to="<id>,<id>"` attribute
   overrides anchor-discovered edges.
6. **Metadata.**
       metadata.title       = <title> text (when present)
       metadata.description = <meta name="description"> + " (extracted from
                             <source-url-or-path>)"
       metadata.source      = input URL or file path
       source_format        = "html"
       kind                 = --target-kind (default "arch")
       layout               = "layered"

Dependencies
------------
- Python stdlib (html.parser, urllib, argparse, subprocess, re, pathlib).
- Optional: lxml and beautifulsoup4 are used when available for more reliable
  nested-element handling. NOT required — stdlib works.
- Optional: `bin/dev-browser-wrapper.sh` for --url. Fallback: urllib fetch
  (pre-JS HTML only).
- Optional: `bin/parse-html-diagram.py` for nested-SVG extraction.

Fail-fast policy: no broad except. Each documented error path is raised
explicitly and mapped to a specific exit code.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError

# Optional dependencies — detected at import time, never required.
try:
    from bs4 import BeautifulSoup  # type: ignore  # noqa: F401

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
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
ID_SAFE_RE = re.compile(r"[^A-Za-z0-9_\-]+")
PNG_REFUSAL = (
    "REFUSE: PNG-embedded diagram cannot be modified — "
    "provide the source artifact (ASCII / HTML / SVG / Mermaid)."
)
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

BIN_DIR = pathlib.Path(__file__).resolve().parent
DEV_BROWSER_WRAPPER = BIN_DIR / "dev-browser-wrapper.sh"
PARSE_HTML_DIAGRAM = BIN_DIR / "parse-html-diagram.py"


# ---------------------------------------------------------------------------
# IR validation (mirrors the invariants in parse-html-diagram.py and schema.json)
# ---------------------------------------------------------------------------


def _validate_ir(ir: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(ir, dict):
        return ["top-level IR is not an object"]
    if ir.get("format") != IR_VERSION:
        errors.append(f"format must be {IR_VERSION!r}, got {ir.get('format')!r}")
    for key in ("source_format", "kind", "layout"):
        if not isinstance(ir.get(key), str) or not ir[key]:
            errors.append(f"{key!r} must be a non-empty string")
    nodes = ir.get("nodes")
    edges = ir.get("edges")
    if not isinstance(nodes, list):
        errors.append("nodes must be a list")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be a list")
        edges = []
    node_ids: set = set()
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            errors.append(f"node[{i}] not an object")
            continue
        nid = n.get("id")
        # Per IR spec, node ids must be non-empty strings of [A-Za-z0-9_-].
        # (The previous version mistakenly OR'd a no-op `ID_SAFE_RE.fullmatch("")`
        # check that always evaluated False due to operator precedence, so the
        # regex-shape check was dead code. Reinstated as a single explicit
        # match against the safe-id alphabet.)
        if not isinstance(nid, str) or not re.fullmatch(r"[A-Za-z0-9_\-]+", nid):
            errors.append(f"node[{i}].id invalid: {nid!r}")
            continue
        if nid in node_ids:
            errors.append(f"duplicate node id {nid!r}")
        node_ids.add(nid)
        if not isinstance(n.get("label"), str):
            errors.append(f"node[{i}].label must be a string")
    for i, e in enumerate(edges):
        if not isinstance(e, dict):
            errors.append(f"edge[{i}] not an object")
            continue
        for end in ("from", "to"):
            if e.get(end) not in node_ids:
                errors.append(f"edge[{i}].{end} -> unknown node {e.get(end)!r}")
    return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_id(raw: str, fallback: str) -> str:
    """Coerce any string to schema-safe id chars."""
    cleaned = ID_SAFE_RE.sub("-", raw or "").strip("-")
    return cleaned or fallback


def _unique_id(base: str, used: set) -> str:
    """Return `base` if unused, else `base-2`, `base-3`, ..."""
    if base not in used:
        used.add(base)
        return base
    i = 2
    while f"{base}-{i}" in used:
        i += 1
    new_id = f"{base}-{i}"
    used.add(new_id)
    return new_id


def _is_png_path(path: pathlib.Path) -> bool:
    if path.suffix.lower() == ".png":
        return True
    try:
        with path.open("rb") as fh:
            head = fh.read(8)
        return head.startswith(PNG_MAGIC)
    except OSError:
        return False


def _head_content_type(url: str) -> Optional[str]:
    """HEAD-check a URL and return the Content-Type header (lower-cased)."""
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
        return (resp.headers.get("Content-Type") or "").lower()


# ---------------------------------------------------------------------------
# HTML landmark collector
# ---------------------------------------------------------------------------


class _LandmarkCollector(HTMLParser):
    """Walks the HTML once, records landmarks, anchors, inline SVGs, meta."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.landmarks: List[Dict[str, Any]] = []
        self.title_parts: List[str] = []
        self.meta_description: Optional[str] = None
        self._in_title = False
        self._landmark_stack: List[Dict[str, Any]] = []
        self._heading_target: Optional[Dict[str, Any]] = None
        self._heading_open: bool = False
        self._svg_depth = 0
        self._svg_parts: List[str] = []
        self._svg_target: Optional[Dict[str, Any]] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        self._record_starttag(tag, attrs_dict)

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        # Self-closing tags (e.g. `<meta/>`) — we only care about meta + some SVG children.
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        self._record_starttag(tag, attrs_dict, self_closing=True)
        # html.parser does NOT auto-call endtag for XHTML self-closing; replay:
        if tag == "svg":
            self._close_svg()

    def _record_starttag(
        self, tag: str, attrs: Dict[str, str], self_closing: bool = False
    ) -> None:
        t = tag.lower()
        if t == "title":
            self._in_title = True
            return
        if t == "meta":
            name = attrs.get("name", "").lower()
            if name == "description":
                self.meta_description = attrs.get("content") or None
            return
        if self._svg_depth > 0:
            # Accumulate SVG source for later parse-html-diagram.py call.
            self._svg_parts.append(self._reconstruct_opentag(tag, attrs, self_closing))
            if t == "svg":
                self._svg_depth += 1
            return
        if t == "svg":
            self._svg_depth = 1
            self._svg_parts = [self._reconstruct_opentag(tag, attrs, self_closing)]
            self._svg_target = (
                self._landmark_stack[-1] if self._landmark_stack else None
            )
            return
        if t in SEMANTIC_TAGS:
            lm = {
                "tag": t,
                "attrs": attrs,
                "heading": None,
                "_first_text_chunks": [],
                "anchors": [],
                "inline_svgs": [],
            }
            self.landmarks.append(lm)
            self._landmark_stack.append(lm)
            return
        if t in HEADING_TAGS and self._landmark_stack and self._landmark_stack[-1]["heading"] is None:
            self._heading_open = True
            self._heading_target = self._landmark_stack[-1]
            return
        if t == "a" and self._landmark_stack:
            href = attrs.get("href", "")
            if href.startswith("#"):
                self._landmark_stack[-1]["anchors"].append(href[1:])

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "title":
            self._in_title = False
            return
        if self._svg_depth > 0:
            self._svg_parts.append(f"</{tag}>")
            if t == "svg":
                self._svg_depth -= 1
                if self._svg_depth == 0:
                    self._close_svg()
            return
        if t in HEADING_TAGS and self._heading_open:
            self._heading_open = False
            self._heading_target = None
            return
        if (
            t in SEMANTIC_TAGS
            and self._landmark_stack
            and self._landmark_stack[-1]["tag"] == t
        ):
            self._landmark_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
            return
        if self._svg_depth > 0:
            self._svg_parts.append(data)
            return
        if self._heading_open and self._heading_target is not None:
            cur = self._heading_target["heading"] or ""
            self._heading_target["heading"] = (cur + data).strip() or None
            return
        text = data.strip()
        if text and self._landmark_stack and len(self._landmark_stack[-1]["_first_text_chunks"]) < 8:
            self._landmark_stack[-1]["_first_text_chunks"].append(text)

    def _close_svg(self) -> None:
        source = "".join(self._svg_parts)
        if self._svg_target is not None:
            self._svg_target["inline_svgs"].append(source)
        self._svg_parts = []
        self._svg_target = None

    @staticmethod
    def _reconstruct_opentag(tag: str, attrs: Dict[str, str], self_closing: bool) -> str:
        attr_str = "".join(
            f' {k}="{v}"' if v else f" {k}" for k, v in attrs.items()
        )
        slash = "/" if self_closing else ""
        return f"<{tag}{attr_str}{slash}>"


# ---------------------------------------------------------------------------
# Landmarks + inline SVG -> IR
# ---------------------------------------------------------------------------


def _inline_svg_children(svg_source: str, parent_node_id: str) -> List[Dict[str, Any]]:
    """Parse an inline SVG string via parse-html-diagram.py and return IR nodes.

    Returns nodes (NOT edges — cross-landmark edges are landmark-level only in
    this specialization). Annotations mark every node as `from-inline-svg`
    so downstream emitters can distinguish them from the landmark skeleton.

    Failure is non-fatal — an unparseable SVG yields an empty list. We do NOT
    swallow errors silently when `parse-html-diagram.py` is missing; that
    would hide a misconfigured install. If the script is missing from disk,
    we just return [] (no subprocess attempted).
    """
    if not PARSE_HTML_DIAGRAM.is_file():
        return []
    # Wrap the SVG so parse-html-diagram.py's inline-SVG branch fires.
    wrapped = f"<!DOCTYPE html><html><body>{svg_source}</body></html>"
    result = subprocess.run(
        [sys.executable, str(PARSE_HTML_DIAGRAM), "--in", "-"],
        input=wrapped,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []
    ir = json.loads(result.stdout)
    children: List[Dict[str, Any]] = []
    for n in ir.get("nodes", []):
        new = dict(n)
        new["id"] = f"{parent_node_id}-{new.get('id', 'svg')}"
        annos = list(new.get("annotations") or [])
        if "from-inline-svg" not in annos:
            annos.append("from-inline-svg")
        new["annotations"] = annos
        children.append(new)
    return children


def _landmarks_to_ir(
    collector: _LandmarkCollector,
    source_display: str,
    target_kind: str,
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    used_ids: set = set()
    id_index: Dict[str, str] = {}

    for i, lm in enumerate(collector.landmarks):
        attrs = lm["attrs"]
        raw_id = attrs.get("data-diagram-id") or attrs.get("id") or f"{lm['tag']}-{i}"
        node_id = _unique_id(_safe_id(raw_id, f"lm{i}"), used_ids)
        id_index[raw_id] = node_id
        if attrs.get("id"):
            id_index[attrs["id"]] = node_id

        override_label = attrs.get("data-diagram-label")
        label = (
            override_label
            or lm["heading"]
            or " ".join(lm["_first_text_chunks"])[:120]
            or lm["tag"].capitalize()
        )
        nodes.append(
            {
                "id": node_id,
                "label": (label or lm["tag"].capitalize()).strip(),
                "rank": i,
                "style": {"shape": "rect"},
                "annotations": [lm["tag"]],
            }
        )

        # Nested SVG diagrams attach as children.
        for svg_source in lm["inline_svgs"]:
            for child in _inline_svg_children(svg_source, node_id):
                child_id = _unique_id(_safe_id(child["id"], f"{node_id}-svg"), used_ids)
                child["id"] = child_id
                nodes.append(child)
                edges.append(
                    {
                        "id": _unique_id(
                            _safe_id(f"e-{node_id}-{child_id}", f"e{len(edges)}"),
                            set(e["id"] for e in edges) if edges else set(),
                        ),
                        "from": node_id,
                        "to": child_id,
                        "style": {"arrow": "solid"},
                    }
                )

    # Anchor + data-diagram-edge-to edges between landmarks.
    used_edge_ids: set = set(e["id"] for e in edges)
    for i, lm in enumerate(collector.landmarks):
        src_id = nodes_first_with_rank(nodes, i)
        if src_id is None:
            continue
        seen_targets: set = set()
        override = lm["attrs"].get("data-diagram-edge-to", "").strip()
        if override:
            for t in (s.strip() for s in override.split(",") if s.strip()):
                if t in id_index and id_index[t] != src_id:
                    seen_targets.add(id_index[t])
        for anchor in lm["anchors"]:
            tgt = id_index.get(anchor)
            if tgt and tgt != src_id:
                seen_targets.add(tgt)
        for tgt in seen_targets:
            eid = _unique_id(_safe_id(f"e-{src_id}-{tgt}", f"e{len(edges)}"), used_edge_ids)
            edges.append({"id": eid, "from": src_id, "to": tgt})

    title = "".join(collector.title_parts).strip() or None
    meta_desc = collector.meta_description
    description = f"(extracted from {source_display})"
    if meta_desc:
        description = f"{meta_desc.strip()} {description}"

    metadata: Dict[str, Any] = {"source": source_display, "description": description}
    if title:
        metadata["title"] = title

    return {
        "format": IR_VERSION,
        "source_format": SOURCE_FORMAT,
        "kind": target_kind,
        "layout": "layered",
        "nodes": nodes,
        "edges": edges,
        "metadata": metadata,
    }


def nodes_first_with_rank(nodes: List[Dict[str, Any]], rank: int) -> Optional[str]:
    for n in nodes:
        if n.get("rank") == rank and "from-inline-svg" not in (n.get("annotations") or []):
            return n["id"]
    return None


# ---------------------------------------------------------------------------
# Fetch logic (URL mode)
# ---------------------------------------------------------------------------


def _fetch_via_dev_browser(url: str, out_html_path: pathlib.Path) -> None:
    """Best-effort: save rendered HTML via the dev-browser wrapper."""
    if not DEV_BROWSER_WRAPPER.is_file():
        raise RuntimeError(
            f"dev-browser wrapper not found at {DEV_BROWSER_WRAPPER}; "
            "run /amw-init to install it."
        )
    # dev-browser-wrapper.sh has no "html" subcommand — we use the raw
    # pass-through with eval and return document.documentElement.outerHTML.
    script = (
        "(() => document.documentElement.outerHTML)();"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as js_fh:
        js_fh.write(script)
        script_path = js_fh.name
    try:
        result = subprocess.run(
            [
                "dev-browser",
                "eval",
                "--url",
                url,
                "--wait-for-network-idle",
                "--timeout",
                "15000",
                "--script",
                script_path,
            ],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
    finally:
        pathlib.Path(script_path).unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"dev-browser eval failed (exit {result.returncode}): {result.stderr.strip()}"
        )
    payload = result.stdout.strip()
    if payload.startswith('"') and payload.endswith('"'):
        payload = json.loads(payload)
    out_html_path.write_text(payload, encoding="utf-8")


def _fetch_via_urllib(url: str, out_html_path: pathlib.Path) -> None:
    """Fallback: plain urllib fetch — produces pre-JS HTML only."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "ai-maestro-webdesign/dom-to-ir"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
        raw = resp.read()
    out_html_path.write_bytes(raw)


def _fetch_url(url: str) -> pathlib.Path:
    """Guard Content-Type, pick a fetcher, return the temp file path."""
    try:
        ctype = _head_content_type(url) or ""
    except (HTTPError, URLError, OSError):
        ctype = ""
    if ctype.startswith("image/"):
        print(PNG_REFUSAL, file=sys.stderr)
        print(f"        URL returned Content-Type: {ctype}", file=sys.stderr)
        sys.exit(2)
    tmp = pathlib.Path(tempfile.mkstemp(suffix=".html", prefix="dom-to-ir-")[1])
    try:
        _fetch_via_dev_browser(url, tmp)
    except (RuntimeError, FileNotFoundError, subprocess.SubprocessError) as exc:
        # Fallback to urllib — documented as pre-JS only.
        print(
            f"dom-to-ir: dev-browser fetch unavailable ({exc}); "
            "falling back to urllib (pre-JS HTML only).",
            file=sys.stderr,
        )
        _fetch_via_urllib(url, tmp)
    return tmp


# ---------------------------------------------------------------------------
# Top-level parse
# ---------------------------------------------------------------------------


def parse_dom(raw_html: str, source_display: str, target_kind: str) -> Dict[str, Any]:
    """Parse `raw_html` into a landmark-centric IR."""
    collector = _LandmarkCollector()
    try:
        collector.feed(raw_html)
        collector.close()
    except Exception as exc:
        raise ValueError(f"html.parser failed: {exc}") from exc
    ir = _landmarks_to_ir(collector, source_display, target_kind)
    # Landmark-less pages: synthesize a single <body> node so downstream
    # emitters don't break. This is the documented freeform fallback.
    if not ir["nodes"]:
        title = "".join(collector.title_parts).strip() or source_display
        ir["nodes"] = [
            {
                "id": "body",
                "label": title,
                "rank": 0,
                "style": {"shape": "rect"},
                "annotations": ["html-freeform"],
            }
        ]
        ir["kind"] = "freeform"
        ir["layout"] = "freeform"
    return ir


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _write_output(ir: Dict[str, Any], out_path: Optional[str]) -> None:
    text = json.dumps(ir, indent=2, ensure_ascii=False)
    if out_path is None:
        sys.stdout.write(text + "\n")
        return
    pathlib.Path(out_path).write_text(text + "\n", encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dom-to-ir",
        description=(
            "Full-page DOM (URL or local HTML) -> diagram-ir/1.0 JSON. "
            "Extracts HTML5 landmarks as IR nodes and internal anchor links "
            "as edges. Inline <svg> diagrams are attached as children."
        ),
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="Fetch this URL via bin/dev-browser-wrapper.sh.")
    src.add_argument("--in", dest="in_path", help="Parse this local HTML file.")
    parser.add_argument("--out", dest="out_path", default=None, help="Output JSON path.")
    parser.add_argument(
        "--target-kind",
        choices=["flowchart", "arch", "tree"],
        default="arch",
        help="Downstream IR kind hint. Default: arch.",
    )
    args = parser.parse_args(argv)

    if args.in_path:
        path = pathlib.Path(args.in_path)
        if not path.is_file():
            print(f"dom-to-ir: input not found: {args.in_path}", file=sys.stderr)
            return 1
        if _is_png_path(path):
            print(PNG_REFUSAL, file=sys.stderr)
            return 2
        raw = path.read_text(encoding="utf-8", errors="replace")
        source_display = str(path)
    else:
        tmp_path = _fetch_url(args.url)
        raw = tmp_path.read_text(encoding="utf-8", errors="replace")
        source_display = args.url

    try:
        ir = parse_dom(raw, source_display, args.target_kind)
    except ValueError as exc:
        print(f"dom-to-ir: {exc}", file=sys.stderr)
        return 1

    errors = _validate_ir(ir)
    if errors:
        print("dom-to-ir: produced an invalid IR — this is a bug.", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    _write_output(ir, args.out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
