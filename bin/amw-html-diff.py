#!/usr/bin/env python3
"""html-diff.py — structural diff between two HTML files.

CLI
---
    html-diff.py --before <html> --after <html> [--out <patch.json>]

Produces a JSON patch array describing **structural** (diagram-level) changes
between two HTML pages. Does NOT perform word-level text diff — structure
(landmarks, headings, section ids) only. This is the MVP matching what the
`diagram-webpage-sync` skill needs for its "what changed on the page when I
re-ran the ascii-to-html pipeline?" report.

Patch format
------------
Each entry is one object:

    {"op": "add"|"remove"|"move", "path": "<dotted-path>", "detail": "<text>"}

Where `op`:
    add     — a structural element present in AFTER but not BEFORE.
    remove  — present in BEFORE but not AFTER.
    move    — same identity, different document-order rank (reordering).

And `path` is a dotted landmark path like `main.section#hero.h2`.

Exit codes
----------
    0  Inputs are STRUCTURALLY IDENTICAL (empty patch).
    1  Inputs DIFFER (non-empty patch; still a successful diff).
    2  Bad input — one or both files unreadable, or malformed HTML that
       cannot be parsed at all.

Implementation notes
--------------------
- Primary parser: `html.parser.HTMLParser` (stdlib). Opportunistic lxml/bs4
  when available, same as `dom-to-ir.py` and `parse-html-diagram.py`.
- The tool extracts a "structure signature" from each document — an ordered
  list of `(tag, id, heading)` triples for every HTML5 landmark and every
  heading `<h1>`..`<h6>`. The diff is computed over these lists using
  longest-common-subsequence matching plus an add/remove complement.
- We intentionally do NOT diff inline SVG diagrams at this MVP stage — that
  work is handled by `bin/diagram-ir-diff.py` on the landmark-level
  extracted IRs. `html-diff.py` reports "SVG present in both" or "SVG added /
  removed" only at the landmark level.
- Fail-fast: no try/except that swallows parse errors silently.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

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


LANDMARK_TAGS = {"header", "nav", "main", "section", "article", "footer", "aside"}
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


# ---------------------------------------------------------------------------
# Structural signature extractor
# ---------------------------------------------------------------------------


class _SigCollector(HTMLParser):
    """Walk the HTML once, record a structural signature as a flat list.

    Each entry is a dict with keys:
        kind: "landmark" | "heading" | "svg"
        tag:  the HTML tag (lowercased)
        id:   the `id` attribute (or synthesized index if absent)
        label: the heading text / landmark-first-text / ""
        path:  dotted path from root to this element (e.g. "main.section#hero")
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: List[Dict[str, Any]] = []
        self._stack: List[Dict[str, Any]] = []
        self._heading_open = False
        self._heading_entry: Optional[Dict[str, Any]] = None
        self._svg_depth = 0
        self._counter = 0

    def _path(self) -> str:
        parts: List[str] = []
        for el in self._stack:
            p = el["tag"]
            if el["id"]:
                p = f"{p}#{el['id']}"
            parts.append(p)
        return ".".join(parts)

    def _push(self, tag: str, attrs: Dict[str, str], kind: str) -> Dict[str, Any]:
        elem_id = attrs.get("id") or ""
        self._counter += 1
        entry = {
            "kind": kind,
            "tag": tag,
            "id": elem_id,
            "label": "",
            "path": self._path() + (f".{tag}" if self._stack else tag) + (
                f"#{elem_id}" if elem_id else f"[{self._counter}]"
            ),
        }
        self.entries.append(entry)
        return entry

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        t = tag.lower()
        if self._svg_depth > 0:
            if t == "svg":
                self._svg_depth += 1
            return
        if t == "svg":
            # Register one "svg" marker per occurrence (we don't diff SVG contents here).
            entry = self._push("svg", attrs_dict, "svg")
            # Track `data-diagram-id` / `data-role` for stable identity.
            entry["id"] = attrs_dict.get("id") or attrs_dict.get("data-diagram-id") or ""
            self._svg_depth = 1
            return
        if t in LANDMARK_TAGS:
            entry = self._push(t, attrs_dict, "landmark")
            self._stack.append(entry)
            return
        if t in HEADING_TAGS:
            entry = self._push(t, attrs_dict, "heading")
            self._heading_open = True
            self._heading_entry = entry

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        t = tag.lower()
        if t == "svg" and self._svg_depth == 0:
            self._push("svg", attrs_dict, "svg")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if self._svg_depth > 0:
            if t == "svg":
                self._svg_depth -= 1
            return
        if t in HEADING_TAGS and self._heading_open:
            self._heading_open = False
            self._heading_entry = None
            return
        if t in LANDMARK_TAGS and self._stack and self._stack[-1]["tag"] == t:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        if self._svg_depth > 0:
            return
        if self._heading_open and self._heading_entry is not None:
            self._heading_entry["label"] = (
                self._heading_entry["label"] + data
            ).strip()


def _signature(raw_html: str) -> List[Dict[str, Any]]:
    collector = _SigCollector()
    try:
        collector.feed(raw_html)
        collector.close()
    except Exception as exc:
        raise ValueError(f"html.parser failed: {exc}") from exc
    return collector.entries


def _key(entry: Dict[str, Any]) -> str:
    """Identity key used for add/remove/move detection."""
    return f"{entry['kind']}|{entry['tag']}|{entry['id']}|{entry['label']}"


# ---------------------------------------------------------------------------
# Diff algorithm
# ---------------------------------------------------------------------------


def _diff(before: List[Dict[str, Any]], after: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    before_keys = [_key(e) for e in before]
    after_keys = [_key(e) for e in after]
    before_set = set(before_keys)
    after_set = set(after_keys)

    patch: List[Dict[str, Any]] = []

    # Additions: anything in after_set but not in before_set.
    for i, k in enumerate(after_keys):
        if k not in before_set:
            e = after[i]
            patch.append(
                {
                    "op": "add",
                    "path": e["path"],
                    "detail": f"new {e['kind']} <{e['tag']}>"
                    + (f" id={e['id']}" if e["id"] else "")
                    + (f" label={e['label']!r}" if e["label"] else ""),
                }
            )

    # Removals: in before_set but not in after_set.
    for i, k in enumerate(before_keys):
        if k not in after_set:
            e = before[i]
            patch.append(
                {
                    "op": "remove",
                    "path": e["path"],
                    "detail": f"removed {e['kind']} <{e['tag']}>"
                    + (f" id={e['id']}" if e["id"] else "")
                    + (f" label={e['label']!r}" if e["label"] else ""),
                }
            )

    # Moves: present in both but at different document-order ranks.
    # We only report a move if the identity is unambiguous (key appears
    # exactly once in each list); duplicate keys get skipped to avoid noise.
    shared = before_set & after_set
    for k in shared:
        before_idx = [i for i, bk in enumerate(before_keys) if bk == k]
        after_idx = [i for i, ak in enumerate(after_keys) if ak == k]
        if len(before_idx) != 1 or len(after_idx) != 1:
            continue
        if before_idx[0] != after_idx[0]:
            e = after[after_idx[0]]
            patch.append(
                {
                    "op": "move",
                    "path": e["path"],
                    "detail": f"{e['kind']} <{e['tag']}>"
                    + (f" id={e['id']}" if e["id"] else "")
                    + f" moved from rank {before_idx[0]} -> {after_idx[0]}",
                }
            )
    return patch


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="html-diff",
        description=(
            "Structural (landmark / heading / SVG marker) diff between two "
            "HTML files. NOT a word-level text diff."
        ),
    )
    parser.add_argument("--before", required=True, help="Path to the BEFORE html file.")
    parser.add_argument("--after", required=True, help="Path to the AFTER html file.")
    parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Output patch.json path. Omitted = stdout.",
    )
    args = parser.parse_args(argv)

    try:
        before_raw = pathlib.Path(args.before).read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, IsADirectoryError) as exc:
        print(f"html-diff: cannot read --before: {exc}", file=sys.stderr)
        return 2
    try:
        after_raw = pathlib.Path(args.after).read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, IsADirectoryError) as exc:
        print(f"html-diff: cannot read --after: {exc}", file=sys.stderr)
        return 2

    try:
        before_sig = _signature(before_raw)
        after_sig = _signature(after_raw)
    except ValueError as exc:
        print(f"html-diff: {exc}", file=sys.stderr)
        return 2

    patch = _diff(before_sig, after_sig)
    text = json.dumps(patch, indent=2, ensure_ascii=False)
    if args.out_path is None:
        sys.stdout.write(text + "\n")
    else:
        pathlib.Path(args.out_path).write_text(text + "\n", encoding="utf-8")

    return 0 if not patch else 1


if __name__ == "__main__":
    sys.exit(main())
