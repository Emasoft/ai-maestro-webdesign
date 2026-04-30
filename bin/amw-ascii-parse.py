#!/usr/bin/env python3
"""
ascii-parse.py — tokenize ASCII box-drawing / wireframe text into structured JSON.

Used by: ascii-to-svg, ascii-to-html, wd-ascii-to-svg, wd-ascii-to-html.

This is a MECHANICAL tokenizer — it classifies each character of the input grid
into one of {corner, h-edge, v-edge, intersection, arrow, text, space}, and
does light node/edge discovery for diagrams. It is NOT a full semantic parser.
The calling skill (ascii-to-svg / ascii-to-html) does semantic reasoning on
top of the JSON the parser emits.

Input formats recognized
------------------------
  1. Unicode box-drawing  — ┌─┐│└┘├┤┬┴┼  (recommended)
     Arrows:  → ↓ ← ↑
  2. ASCII art boxes      — +---+ | | +---+
     Arrows:  -> <- v ^ | -
  3. Wireframe markers (active only with --mode wireframe):
       [ text ]         → button
       [__placeholder__] → input
       [x] text         → checkbox on
       [ ] text         → checkbox off
       (o) text         → radio
       IMG / PICTURE    → image placeholder

Usage
-----
  ascii-parse.py --in file.txt [--mode diagram|wireframe|auto] [--out out.json]
  cat file.txt | ascii-parse.py --mode diagram
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Unicode box-drawing character classes
U_CORNERS_DOUBLE = set("╔╗╚╝╤╧╢╟╫╪")
U_CORNERS = set("┌┐└┘╔╗╚╝") | U_CORNERS_DOUBLE
U_H_EDGE = set("─━═")
U_V_EDGE = set("│┃║")
U_T_JUNCTION = set("├┤┬┴┼╠╣╦╩╬")
U_ARROWS = set("→↓←↑⇒⇓⇐⇑▶▼◀▲⬇⬆⬅➡")
U_BOX_CHARS = U_CORNERS | U_H_EDGE | U_V_EDGE | U_T_JUNCTION

A_CORNER = {"+"}
A_H_EDGE = {"-", "="}
A_V_EDGE = {"|"}
A_ARROWS = set()  # ASCII arrows are two-char tokens handled by regex below
A_BOX_CHARS = A_CORNER | A_H_EDGE | A_V_EDGE

# Anchored to non-word boundaries so `^^` and `vv` don't match inside prose
# ("savvy", "^^^^^" ASCII borders). The directional arrows (-->, <-, etc.)
# are safe without anchors but we anchor them uniformly for consistency.
ASCII_ARROW_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])(-->|<--|->|<-|=>|<=|\^\^|vv)(?![A-Za-z0-9_])"
)


def classify(ch: str) -> str:
    """Return a single classification token for a character."""
    if ch in U_CORNERS:
        return "corner"
    if ch in U_H_EDGE:
        return "h-edge"
    if ch in U_V_EDGE:
        return "v-edge"
    if ch in U_T_JUNCTION:
        return "junction"
    if ch in U_ARROWS:
        return "arrow"
    if ch in A_CORNER:
        return "corner"
    if ch in A_H_EDGE:
        return "h-edge"
    if ch in A_V_EDGE:
        return "v-edge"
    if ch == " ":
        return "space"
    if ch == "\t":
        return "space"
    return "text"


def detect_format(text: str) -> str:
    """unicode | ascii | mixed"""
    has_u = any(c in U_BOX_CHARS for c in text)
    has_a = "+" in text and ("-" in text or "|" in text)
    if has_u and not has_a:
        return "unicode"
    if has_a and not has_u:
        return "ascii"
    if has_u and has_a:
        return "mixed"
    return "unicode"  # default when no box chars detected at all


# Hard cap for grid dimensions. find_boxes is O(rows*cols*rows*cols); a
# 300x300 all-plus input hangs for minutes. 500x500 = 6.25e10 ops worst-case
# but typical ASCII wireframes are <100x100 and complete instantly.
MAX_GRID_DIM = 500


def to_grid(text: str) -> list[list[str]]:
    """Expand tabs, pad to rectangular grid. Caps dimensions at MAX_GRID_DIM.

    MIN-D2: use `str.expandtabs(4)` per line so tab-stop math is correct.
    A plain text.replace("\\t", "    ") overcounts when a tab is preceded
    by a non-multiple-of-4 number of characters — ASCII wireframes pasted
    from an editor then lose visual alignment.
    """
    lines = [ln.expandtabs(4) for ln in text.splitlines()]
    if not lines:
        return []
    if len(lines) > MAX_GRID_DIM:
        raise ValueError(
            f"Input has {len(lines)} rows; max is {MAX_GRID_DIM}. "
            f"Split into smaller chunks."
        )
    max_w = max(len(ln) for ln in lines)
    if max_w > MAX_GRID_DIM:
        raise ValueError(
            f"Input has {max_w}-char-wide rows; max is {MAX_GRID_DIM}. "
            f"Trim long lines."
        )
    return [list(ln.ljust(max_w)) for ln in lines]


def find_boxes(grid: list[list[str]], fmt: str) -> list[dict]:
    """Find rectangular boxes. Returns list of {x, y, w, h, text}.

    Uses the corner-walking heuristic: for each corner char, look for a
    matching right corner on the same row, then a matching bottom on the
    column, then verify the rectangle is closed.
    """
    if not grid:
        return []
    rows, cols = len(grid), len(grid[0])

    corner_chars = U_CORNERS if fmt != "ascii" else A_CORNER
    # Unicode top-left indicator
    tl_u = {"┌", "╔"}
    tl_a = {"+"}
    tl = tl_u if fmt != "ascii" else tl_a

    # Accept junctions on edges so divider rows (├──┤) don't break box detection.
    h_edge_ok = U_H_EDGE | A_H_EDGE | {"┬", "┴", "╤", "╧"}
    v_edge_ok = U_V_EDGE | A_V_EDGE | {"├", "┤", "╟", "╢"}

    boxes = []
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] not in tl:
                continue
            # Look for top-right corner on same row
            for x2 in range(x + 2, cols):
                if grid[y][x2] in corner_chars:
                    # Verify top edge is all h-edges (or horizontal junctions)
                    row_segment = grid[y][x + 1 : x2]
                    if not all(c in h_edge_ok for c in row_segment):
                        continue
                    # Look for bottom-left corner in column x
                    for y2 in range(y + 2, rows):
                        if grid[y2][x] in corner_chars:
                            # Verify left edge (allow T-junctions for dividers)
                            col_segment = [grid[yy][x] for yy in range(y + 1, y2)]
                            if not all(c in v_edge_ok for c in col_segment):
                                continue
                            # Verify bottom edge
                            bottom_segment = grid[y2][x + 1 : x2]
                            if not all(c in h_edge_ok for c in bottom_segment):
                                continue
                            # Verify right edge
                            right_segment = [grid[yy][x2] for yy in range(y + 1, y2)]
                            if not all(c in v_edge_ok for c in right_segment):
                                continue
                            if grid[y2][x2] not in corner_chars:
                                continue
                            inner_lines = []
                            for yy in range(y + 1, y2):
                                row_text = "".join(grid[yy][x + 1 : x2]).strip()
                                if row_text:
                                    inner_lines.append(row_text)
                            boxes.append(
                                {
                                    "x": x,
                                    "y": y,
                                    "w": x2 - x + 1,
                                    "h": y2 - y + 1,
                                    "text": "\n".join(inner_lines),
                                }
                            )
                            break
                    break
    return boxes


def find_arrows(text: str) -> list[dict]:
    """Return list of {row, col, symbol, direction}. Handles both Unicode and ASCII arrows."""
    arrows = []
    for y, line in enumerate(text.splitlines()):
        # Unicode single-character arrows
        for x, ch in enumerate(line):
            if ch in U_ARROWS:
                direction = {
                    "→": "right",
                    "⇒": "right",
                    "▶": "right",
                    "➡": "right",
                    "←": "left",
                    "⇐": "left",
                    "◀": "left",
                    "⬅": "left",
                    "↓": "down",
                    "⇓": "down",
                    "▼": "down",
                    "⬇": "down",
                    "↑": "up",
                    "⇑": "up",
                    "▲": "up",
                    "⬆": "up",
                }.get(ch, "unknown")
                arrows.append({"row": y, "col": x, "symbol": ch, "direction": direction})
        # ASCII two-char arrows
        for m in ASCII_ARROW_PATTERN.finditer(line):
            sym = m.group(0)
            direction = {
                "->": "right",
                "-->": "right",
                "=>": "right",
                "<-": "left",
                "<--": "left",
                "<=": "left",
            }.get(sym, "unknown")
            arrows.append({"row": y, "col": m.start(), "symbol": sym, "direction": direction})
    return arrows


def classify_grid(grid: list[list[str]]) -> list[list[str]]:
    """Produce a parallel grid of classification tokens."""
    return [[classify(ch) for ch in row] for row in grid]


# ---------- Wireframe-specific primitives ----------

WF_BUTTON = re.compile(r"\[\s*([^\[\]_\n]{1,80}?)\s*\]")
WF_INPUT = re.compile(r"\[\s*__+\s*([^\[\]]*?)\s*__+\s*\]|\[_+\s*([^\[\]]*?)\s*_+\]")
WF_CHECKBOX = re.compile(r"\[([ xX])\]\s*([^\n]+)")
WF_RADIO = re.compile(r"\(([ oO])\)\s*([^\n]+)")
# Require square-bracket markers so prose like "the logo in the picture" doesn't
# get flagged as two image components and flip auto-mode to wireframe spuriously.
WF_IMG = re.compile(r"\[\s*(IMG|IMAGE|PICTURE|PIC|LOGO)\s*\]", re.IGNORECASE)


def find_wireframe_components(text: str) -> list[dict]:
    comps = []
    for y, line in enumerate(text.splitlines()):
        for m in WF_INPUT.finditer(line):
            label = m.group(1) or m.group(2) or ""
            comps.append(
                {"kind": "input", "row": y, "col": m.start(), "label": label.strip()}
            )
        # Subtract inputs from button scan (inputs also match [ ... ])
        # Preserve match length — fixed-length substitution shifted every
        # subsequent button's reported column by the cumulative delta.
        stripped = WF_INPUT.sub(lambda m: " " * len(m.group(0)), line)
        for m in WF_BUTTON.finditer(stripped):
            text_in = m.group(1).strip()
            # Filter out checkbox/radio matches
            if re.fullmatch(r"[ xXoO]", text_in):
                continue
            comps.append(
                {"kind": "button", "row": y, "col": m.start(), "label": text_in}
            )
        for m in WF_CHECKBOX.finditer(line):
            comps.append(
                {
                    "kind": "checkbox",
                    "row": y,
                    "col": m.start(),
                    "checked": m.group(1).strip().lower() == "x",
                    "label": m.group(2).strip(),
                }
            )
        for m in WF_RADIO.finditer(line):
            comps.append(
                {
                    "kind": "radio",
                    "row": y,
                    "col": m.start(),
                    "selected": m.group(1).strip().lower() == "o",
                    "label": m.group(2).strip(),
                }
            )
        for m in WF_IMG.finditer(line):
            comps.append(
                {"kind": "image", "row": y, "col": m.start(), "label": m.group(1)}
            )
    return comps


def main():
    p = argparse.ArgumentParser(
        description="Tokenize ASCII box-drawing / wireframe text into JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    # NIT: dest="input_path" (was dest="input") so args.input_path doesn't
    # shadow Python's builtin input() semantically inside this function.
    p.add_argument("--in", dest="input_path", help="Input file (default: stdin).")
    p.add_argument("--out", dest="output", help="Output JSON file (default: stdout).")
    p.add_argument(
        "--mode",
        choices=["diagram", "wireframe", "auto"],
        default="auto",
        help="Parse mode. auto = infer from content.",
    )
    p.add_argument(
        "--no-grid",
        action="store_true",
        help="Omit the classified-grid payload from output (saves space).",
    )
    args = p.parse_args()

    if args.input_path:
        # MIN-D7: utf-8-sig transparently strips a leading BOM that Windows
        # editors (old VS Code, Notepad) prepend. Without this, the BOM
        # counted as column 0 and every box on the first line was offset
        # by 1 character.
        raw = Path(args.input_path).read_text(encoding="utf-8-sig")
    else:
        raw = sys.stdin.read()

    # MIN-D1: normalize line endings BEFORE the fence regex. Windows-style
    # `\r\n```\r\n` didn't match the `\n```\s*$` pattern, so the trailing
    # fence leaked into the grid as a literal row of backticks.
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")

    # Strip fenced code block wrappers if present
    stripped = re.sub(r"^```[a-z]*\n", "", raw, flags=re.MULTILINE)
    stripped = re.sub(r"\n```\s*$", "", stripped)

    fmt = detect_format(stripped)
    grid = to_grid(stripped)

    # Infer mode when requested.
    # MIN-D3: auto-mode used to flip to "wireframe" on any single [x]/[ ]/[...]
    # marker — prose like a docstring example or JSON arrays in a pasted
    # snippet would spuriously trigger wireframe parsing. We now require
    # DISTINCT marker locations (de-duped by row+col so [x] isn't
    # double-counted by WF_BUTTON and WF_CHECKBOX) AND at least 3 of them
    # (OR more if the doc is large — 1 per ~150 non-empty lines). A real
    # wireframe always has several independent markers; a single docstring
    # `[x]` ref cannot cross that bar.
    if args.mode == "auto":
        marker_spots: set[tuple[int, int]] = set()
        for y, line in enumerate(stripped.splitlines()):
            for rx in (WF_BUTTON, WF_INPUT, WF_CHECKBOX):
                for m in rx.finditer(line):
                    marker_spots.add((y, m.start()))
        non_empty_lines = sum(1 for ln in stripped.splitlines() if ln.strip())
        density_threshold = max(3, non_empty_lines // 150)
        mode = "wireframe" if len(marker_spots) >= density_threshold else "diagram"
    else:
        mode = args.mode

    boxes = find_boxes(grid, fmt)
    arrows = find_arrows(stripped)

    payload = {
        "meta": {
            "format": fmt,
            "mode": mode,
            "rows": len(grid),
            "cols": len(grid[0]) if grid else 0,
        },
        "boxes": boxes,
        "arrows": arrows,
    }

    if mode == "wireframe":
        payload["components"] = find_wireframe_components(stripped)

    if not args.no_grid:
        payload["grid_classified"] = classify_grid(grid)

    out = json.dumps(payload, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Parsed → {args.output}")
        print(f"  format: {fmt}   mode: {mode}")
        print(f"  boxes:  {len(boxes)}   arrows: {len(arrows)}")
        if mode == "wireframe":
            print(f"  components: {len(payload['components'])}")
    else:
        print(out)


if __name__ == "__main__":
    main()
