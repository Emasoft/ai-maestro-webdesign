#!/usr/bin/env python3
"""amw-validate-ascii.py — ASCII diagram validator.

Checks ASCII + Unicode inputs; offers box-diagram-master's group-detection
refinement for more precise error messages on multi-structure diagrams.
Requires only Python 3.8+ stdlib — no Perl dependency needed.

Checks (mirror of the Perl validator):
  1. Line-width consistency, per *box group* (group-aware — a diagram with
     multiple independent structures is evaluated group by group rather than
     by global most-common width).
  2. Vertical line continuity ('│' and junctions must align across rows).
  3. Nested box corner alignment (top-left / top-right / bottom-left /
     bottom-right at matching columns, with left/right walls aligned).
  4. Horizontal connections at corners (e.g. '┌' must be followed by '─'
     or another box char, never by an unrelated printable char).
  5. Wide-character detection (CJK, emoji → 2 display columns).
  6. Forbidden characters (long arrows '⟶ ⇒', variable-width triangles
     '▼ ▲ ▶ ◀') that render at variable width and break alignment.
  7. Tab characters (use spaces only).

Exit codes: 0 = all files pass, 1 = at least one file failed.

Usage:
  python3 bin/amw-validate-ascii.py file1.txt [file2.txt ...]
  python3 bin/amw-validate-ascii.py diagrams/*.txt

Format of each finding:
  <N>. Line LLL, Col CCC: [TYPE] <message>. FIX: <actionable hint>
"""
from __future__ import annotations

import sys
import unicodedata
from pathlib import Path
from typing import Iterable

# ─── ANSI color codes ──────────────────────────────────────────────────────
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ─── Box-drawing character sets (ASCII + Unicode) ──────────────────────────
# Corners
CORNERS_TL = set("┌╭┏╔")   # top-left
CORNERS_TR = set("┐╮┓╗")   # top-right
CORNERS_BL = set("└╰┗╚")   # bottom-left
CORNERS_BR = set("┘╯┛╝")   # bottom-right
CORNERS_UNICODE = CORNERS_TL | CORNERS_TR | CORNERS_BL | CORNERS_BR
CORNERS_ASCII = {"+"}
CORNERS = CORNERS_UNICODE | CORNERS_ASCII

# Verticals
VERT_PURE_UNICODE = set("│┃║")               # pure vertical lines
VERT_DASHED_UNICODE = set("┆┊╎")             # dashed vertical lines
VERT_UNICODE = VERT_PURE_UNICODE | VERT_DASHED_UNICODE
VERT_ASCII = {"|"}
VERT = VERT_UNICODE | VERT_ASCII

# Left-side / right-side verticals (for wall-alignment checks)
LEFT_VERT = set("│║┃┆┊╎├╠┣")
RIGHT_VERT = set("│║┃┆┊╎┤╣┫")

# Horizontals
HORIZ_UNICODE_SOLID = set("─━═")
HORIZ_UNICODE_DASHED = set("┄┈╌")
HORIZ_UNICODE = HORIZ_UNICODE_SOLID | HORIZ_UNICODE_DASHED
HORIZ_ASCII = set("-=")
HORIZ = HORIZ_UNICODE | HORIZ_ASCII

# Junctions (Ts + crosses)
T_DOWN = set("┬╦┳")
T_UP = set("┴╩┻")
T_RIGHT = set("├╠┣")
T_LEFT = set("┤╣┫")
CROSS = set("┼╬╋")
JUNCTIONS = T_DOWN | T_UP | T_RIGHT | T_LEFT | CROSS

# Broad categories used below
BOX_CHARS_UNICODE = CORNERS_UNICODE | VERT_UNICODE | HORIZ_UNICODE | JUNCTIONS
BOX_CHARS = CORNERS | VERT  # chars that indicate a "box line" for grouping
BOX_CHAR_FILL = HORIZ | JUNCTIONS | {" "}  # what can go between two corners

# ─── Forbidden characters: the same table as the Perl script ───────────────
# severity, width, recommended_replacement, recommended_alt
FORBIDDEN_CHARS: dict[str, dict[str, str]] = {
    # CRITICAL: Long arrows (render 3-4x width) — these WILL break alignment
    "⟶": {"severity": "CRITICAL", "width": "3-4x", "replacement": "──→", "alt": "-->"},
    "⟵": {"severity": "CRITICAL", "width": "3-4x", "replacement": "←──", "alt": "<--"},
    "⟹": {"severity": "CRITICAL", "width": "3-4x", "replacement": "══→", "alt": "==>"},
    "⟸": {"severity": "CRITICAL", "width": "3-4x", "replacement": "←══", "alt": "<=="},
    "⟷": {"severity": "CRITICAL", "width": "4-5x", "replacement": "←─→", "alt": "<->"},
    "⟺": {"severity": "CRITICAL", "width": "4-5x", "replacement": "←═→", "alt": "<=>"},
    # HIGH: Double-stroke arrows (render 1.5-2x width)
    "⇒": {"severity": "HIGH", "width": "1.5-2x", "replacement": "=>", "alt": "→"},
    "⇐": {"severity": "HIGH", "width": "1.5-2x", "replacement": "<=", "alt": "←"},
    "⇔": {"severity": "HIGH", "width": "2x", "replacement": "<=>", "alt": "↔"},
    "⇑": {"severity": "HIGH", "width": "1.5x", "replacement": "^", "alt": "↑"},
    "⇓": {"severity": "HIGH", "width": "1.5x", "replacement": "v", "alt": "↓"},
    "⇕": {"severity": "HIGH", "width": "1.5x", "replacement": "↕", "alt": "^v"},
    # MEDIUM: Triangle/filled arrows (render 1.2-1.5x width)
    "▶": {"severity": "MEDIUM", "width": "1.2-1.5x", "replacement": ">", "alt": "→"},
    "◀": {"severity": "MEDIUM", "width": "1.2-1.5x", "replacement": "<", "alt": "←"},
    "▲": {"severity": "MEDIUM", "width": "variable", "replacement": "^", "alt": "↑"},
    "▼": {"severity": "MEDIUM", "width": "variable", "replacement": "v", "alt": "↓"},
    # MEDIUM: Other problematic symbols
    "⇆": {"severity": "MEDIUM", "width": "2x", "replacement": "<>", "alt": "←→"},
    "⇄": {"severity": "MEDIUM", "width": "2x", "replacement": "><", "alt": "→←"},
}


# ─── Display width ─────────────────────────────────────────────────────────
# The Perl validator's custom range table is the source of truth: the
# unicodedata.east_asian_width ("W"/"F") call covers almost all of these,
# but we supplement with ranges that Unicode classifies as "N"/"A"
# (neutral / ambiguous) but render wide in most terminals — specifically
# emoji blocks, which are the common slipup in ASCII diagrams.
_SUPPLEMENTARY_WIDE_RANGES: tuple[tuple[int, int], ...] = (
    # Most emoji are wide even though some are Ambiguous/Neutral in UCD
    (0x1F300, 0x1F9FF),   # Misc Symbols and Pictographs, Emoticons, Transport, etc.
    (0x1FA00, 0x1FA6F),   # Chess Symbols
    (0x1FA70, 0x1FAFF),   # Symbols and Pictographs Extended-A
)

_ZERO_WIDTH_CODEPOINTS: frozenset[int] = frozenset({
    0x200B, 0x200C, 0x200D, 0xFEFF,
})


def char_display_width(ch: str) -> int:
    """Return the display width of a character in a monospace font.

    0 for control/zero-width, 1 for typical ASCII/Latin, 2 for CJK/fullwidth/
    most emoji. Mirrors the Perl validator's `get_display_width` so alignment
    counts match across both validators.
    """
    if not ch:
        return 0
    cp = ord(ch)
    # Control + private-use zero-width
    if cp < 0x20:
        return 0
    if 0x7F <= cp < 0xA0:
        return 0
    if cp in _ZERO_WIDTH_CODEPOINTS:
        return 0
    # Supplementary ranges the UCD doesn't classify as W/F
    for lo, hi in _SUPPLEMENTARY_WIDE_RANGES:
        if lo <= cp <= hi:
            return 2
    # Unicode east-asian-width: W (Wide) and F (Fullwidth) are 2 columns
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("W", "F"):
        return 2
    return 1


def line_display_width(line: str) -> int:
    """Total display width of a string."""
    return sum(char_display_width(c) for c in line)


def find_display_columns(line: str, chars: Iterable[str]) -> list[int]:
    """Return the display-column positions of characters in `chars`."""
    match = set(chars)
    cols: list[int] = []
    col = 0
    for c in line:
        if c in match:
            cols.append(col)
        col += char_display_width(c)
    return cols


def char_at_display_col(line: str, target_col: int) -> str | None:
    """Character that occupies a given display column (start column)."""
    col = 0
    for c in line:
        if col == target_col:
            return c
        w = char_display_width(c)
        if col + w > target_col:
            # target is inside a wide char; return the char
            return c
        col += w
    return None


# ─── Group-detection: box-diagram-master's refinement ──────────────────────
def group_box_lines(lines: list[str]) -> list[list[int]]:
    """Group consecutive lines that share box-char column positions.

    Lines with box chars at different columns are separate structural groups
    (e.g. a box-border row at cols [0,15,19,34] vs a branch connector at
    cols [8,27,46]). This avoids false positives in diagrams with multiple
    independent sub-structures — the "most-common width" heuristic would
    pick one group's width as global expected, which is wrong.

    Source: box-diagram-master/validate.py lines 86-105.
    """
    groups: list[list[int]] = []
    current: list[int] = []

    def box_cols(line: str) -> set[int]:
        return set(find_display_columns(line, BOX_CHARS))

    for i, line in enumerate(lines):
        cols = box_cols(line)
        if len(cols) >= 2:
            if current:
                prev_cols = box_cols(lines[current[-1]])
                if cols & prev_cols:  # shared columns → same structure
                    current.append(i)
                else:  # different columns → new group
                    groups.append(current)
                    current = [i]
            else:
                current = [i]
        else:
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)
    return groups


# ─── Issue record ──────────────────────────────────────────────────────────
class Issue(dict):
    """A single validation finding. Dict-like for easy printing."""

    def __init__(
        self,
        *,
        line: int,
        col: int,
        type: str,
        msg: str,
        char: str | None = None,
    ):
        super().__init__(line=line, col=col, type=type, msg=msg, char=char)


# ─── Individual checks ─────────────────────────────────────────────────────
def check_forbidden_chars(lines: list[str]) -> list[Issue]:
    """Flag forbidden glyphs (long arrows, filled triangles, double arrows)."""
    issues: list[Issue] = []
    for i, line in enumerate(lines):
        col = 0
        for c in line:
            if c in FORBIDDEN_CHARS:
                info = FORBIDDEN_CHARS[c]
                codepoint = f"U+{ord(c):04X}"
                issues.append(
                    Issue(
                        line=i + 1,
                        col=col + 1,
                        type=f"FORBIDDEN_CHAR_{info['severity']}",
                        char=c,
                        msg=(
                            f"Forbidden character '{c}' ({codepoint}) renders "
                            f"at {info['width']} normal width. "
                            f"FIX: Replace with '{info['replacement']}' or "
                            f"'{info['alt']}'"
                        ),
                    )
                )
            col += 1  # NB: Perl script uses char index, not display col, for
                      # the reported column — mirror that for parity.
    return issues


def check_wide_chars(lines: list[str]) -> list[Issue]:
    """Flag characters whose display width is > 1 (CJK, emoji, fullwidth)."""
    issues: list[Issue] = []
    for i, line in enumerate(lines):
        pos = 0
        for c in line:
            if char_display_width(c) > 1 and c not in FORBIDDEN_CHARS:
                # Forbidden chars already reported with a more specific type.
                codepoint = f"U+{ord(c):04X}"
                issues.append(
                    Issue(
                        line=i + 1,
                        col=pos + 1,
                        type="WIDE_CHAR",
                        char=c,
                        msg=(
                            f"Wide character '{c}' ({codepoint}) occupies 2 "
                            f"columns but counts as 1 character. "
                            f"FIX: Replace with ASCII equivalent or account "
                            f"for double-width in alignment"
                        ),
                    )
                )
            pos += 1
    return issues


def check_tabs(lines: list[str]) -> list[Issue]:
    """Flag tab characters."""
    return [
        Issue(
            line=i + 1,
            col=line.index("\t") + 1,
            type="TAB_CHAR",
            msg="Contains tab character (use spaces only). "
                "FIX: Replace tabs with spaces",
        )
        for i, line in enumerate(lines)
        if "\t" in line
    ]


def check_group_widths(lines: list[str]) -> list[Issue]:
    """Group-aware line-width consistency check.

    Uses box-diagram-master's group-detection: consecutive lines sharing
    box-char column positions are treated as one structural group, and
    width inconsistency is reported per group. This is MORE PRECISE than
    the Perl script's global "most-common width" approach for diagrams
    with multiple independent sub-structures.
    """
    widths = [line_display_width(ln) for ln in lines]
    groups = group_box_lines(lines)
    issues: list[Issue] = []

    for group in groups:
        group_widths = {widths[i] for i in group}
        if len(group_widths) <= 1:
            continue
        # Most common width within the group is the expected one
        counts: dict[int, int] = {}
        for idx in group:
            counts[widths[idx]] = counts.get(widths[idx], 0) + 1
        expected = max(counts.items(), key=lambda kv: (kv[1], -kv[0]))[0]
        start, end = group[0] + 1, group[-1] + 1
        for idx in group:
            if widths[idx] != expected:
                diff = widths[idx] - expected
                fix = (
                    f"FIX: Remove {diff} character(s) from this line"
                    if diff > 0
                    else f"FIX: Add {abs(diff)} space(s) to pad this line "
                    f"to width {expected}"
                )
                issues.append(
                    Issue(
                        line=idx + 1,
                        col=widths[idx] + 1,
                        type="WIDTH_MISMATCH",
                        msg=(
                            f"Line has width {widths[idx]}, expected "
                            f"{expected} (off by {diff}) in box group "
                            f"lines {start}-{end}. {fix}"
                        ),
                    )
                )
    return issues


def check_vertical_continuity(lines: list[str]) -> list[Issue]:
    """Pure-vertical lines must align across consecutive rows.

    Mirrors Perl `validate_vertical_continuity`. Only pure '│┃║' are checked
    (junctions are excluded to avoid false positives at converging points).
    """
    issues: list[Issue] = []
    for i in range(len(lines) - 1):
        line, next_line = lines[i], lines[i + 1]
        display_col = 0
        for c in line:
            if c in VERT_PURE_UNICODE or c == "|":
                below = char_at_display_col(next_line, display_col)
                if below == " ":
                    # Look for a misaligned vertical nearby
                    for offset in (-2, -1, 1, 2):
                        nearby = char_at_display_col(
                            next_line, display_col + offset
                        )
                        if nearby and (
                            nearby in VERT_PURE_UNICODE or nearby == "|"
                        ):
                            fix = (
                                f"FIX: Move '│' on line {i + 2} left by "
                                f"{offset} position(s) to column "
                                f"{display_col + 1}"
                                if offset > 0
                                else f"FIX: Move '│' on line {i + 2} right "
                                f"by {abs(offset)} position(s) to column "
                                f"{display_col + 1}"
                            )
                            issues.append(
                                Issue(
                                    line=i + 2,
                                    col=display_col + offset + 1,
                                    type="VERTICAL_MISALIGNED",
                                    msg=(
                                        f"Vertical '│' at column "
                                        f"{display_col + offset + 1} should "
                                        f"align with '│' above (line "
                                        f"{i + 1}, column "
                                        f"{display_col + 1}). {fix}"
                                    ),
                                )
                            )
                            break
            elif c in T_DOWN:
                # Perl validator flags T-down joints whose junction below is
                # misaligned. Mirror that logic to keep parity.
                below = char_at_display_col(next_line, display_col)
                if below and below in HORIZ:
                    for offset in (-2, -1, 1, 2):
                        nearby = char_at_display_col(
                            next_line, display_col + offset
                        )
                        if nearby and nearby in (CROSS | T_UP):
                            fix = (
                                f"FIX: Move '{nearby}' left by {offset} "
                                f"position(s) to column {display_col + 1}"
                                if offset > 0
                                else f"FIX: Move '{nearby}' right by "
                                f"{abs(offset)} position(s) to column "
                                f"{display_col + 1}"
                            )
                            issues.append(
                                Issue(
                                    line=i + 2,
                                    col=display_col + offset + 1,
                                    type="VERTICAL_MISALIGNED",
                                    msg=(
                                        f"Junction '{nearby}' at column "
                                        f"{display_col + offset + 1} should "
                                        f"align with '┬' above (line "
                                        f"{i + 1}, column "
                                        f"{display_col + 1}). {fix}"
                                    ),
                                )
                            )
                            break
            display_col += char_display_width(c)
    return issues


def check_box_border_integrity(lines: list[str]) -> list[Issue]:
    """Between two corners on the same line, only horizontal or junction
    chars (plus space) may appear."""
    issues: list[Issue] = []
    for i, line in enumerate(lines):
        positions = [j for j, c in enumerate(line) if c in CORNERS]
        if len(positions) < 2:
            continue
        # Pair adjacent corners
        k = 0
        while k < len(positions) - 1:
            start, end = positions[k], positions[k + 1]
            between = line[start + 1 : end]
            if between and not all(c in BOX_CHAR_FILL for c in between):
                issues.append(
                    Issue(
                        line=i + 1,
                        col=start + 1,
                        type="BROKEN_CONNECTION",
                        msg=(
                            f"Broken box border between col {start + 1} and "
                            f"{end + 1}: {between!r}. "
                            f"FIX: Replace non-horizontal characters with "
                            f"'─', '═', or whitespace"
                        ),
                    )
                )
            k += 2
    return issues


def check_corner_neighbors(lines: list[str]) -> list[Issue]:
    """At each corner, check the adjacent character on the expected side.

    ┌/╭/┏/╔ : horizontal (or box/space) to the RIGHT
    ┐/╮/┓/╗ : horizontal (or box/space) to the LEFT
    └/╰/┗/╚ : horizontal (or box/space) to the RIGHT
    ┘/╯/┛/╝ : horizontal (or box/space) to the LEFT
    """
    issues: list[Issue] = []
    valid_neighbor = HORIZ | BOX_CHARS_UNICODE | {" ", "+"}
    for i, line in enumerate(lines):
        chars = list(line)
        for j, c in enumerate(chars):
            if c in CORNERS_TL or c in CORNERS_BL:
                if j < len(chars) - 1:
                    nxt = chars[j + 1]
                    if nxt not in valid_neighbor:
                        issues.append(
                            Issue(
                                line=i + 1,
                                col=j + 1,
                                char=c,
                                type="BROKEN_CONNECTION",
                                msg=(
                                    f"Corner '{c}' has unexpected char "
                                    f"'{nxt}' to the right. "
                                    f"FIX: The character to the right of a "
                                    f"top-left or bottom-left corner must be "
                                    f"a horizontal line, another box char, "
                                    f"or a space"
                                ),
                            )
                        )
            if c in CORNERS_TR or c in CORNERS_BR:
                if j > 0:
                    prv = chars[j - 1]
                    if prv not in valid_neighbor:
                        issues.append(
                            Issue(
                                line=i + 1,
                                col=j + 1,
                                char=c,
                                type="BROKEN_CONNECTION",
                                msg=(
                                    f"Corner '{c}' has unexpected char "
                                    f"'{prv}' to the left. "
                                    f"FIX: The character to the left of a "
                                    f"top-right or bottom-right corner must "
                                    f"be a horizontal line, another box "
                                    f"char, or a space"
                                ),
                            )
                        )
    return issues


def check_box_alignment(lines: list[str]) -> list[Issue]:
    """Nested-box corner alignment and wall verticals.

    For every top-left corner, locate its mate top-right on the same line,
    the matching bottom-left in the same column below, and the bottom-right
    on the same line as the BL and same column as the TR. If any of those
    are off by ≤3 cols, flag with a FIX that includes the direction and
    distance. If they are not found but a nearby corner exists, flag a
    misalignment.
    """
    # Build a list of all corners with their display column and type
    corner_type: dict[int, list[tuple[int, int, str, str]]] = {}
    # key = line idx, value = list of (display_col, char_idx, char, type)
    for i, line in enumerate(lines):
        col = 0
        for j, c in enumerate(line):
            kind = ""
            if c in CORNERS_TL:
                kind = "top_left"
            elif c in CORNERS_TR:
                kind = "top_right"
            elif c in CORNERS_BL:
                kind = "bottom_left"
            elif c in CORNERS_BR:
                kind = "bottom_right"
            if kind:
                corner_type.setdefault(i, []).append((col, j, c, kind))
            col += char_display_width(c)

    # Flatten for easy iteration
    all_corners: list[tuple[int, int, int, str, str]] = []
    # (line_idx, display_col, char_idx, char, type)
    for li, lst in corner_type.items():
        for col, ci, c, kind in lst:
            all_corners.append((li, col, ci, c, kind))

    issues: list[Issue] = []

    def find_first_right(line_idx: int, col: int, kind: str) -> tuple[int, int, str] | None:
        best: tuple[int, int, str] | None = None
        for li, dc, _, ch, k in all_corners:
            if li == line_idx and k == kind and dc > col:
                if best is None or dc < best[0]:
                    best = (dc, li, ch)
        return best

    def find_first_below_at_col(col: int, line_idx: int, kind: str) -> tuple[int, str] | None:
        best: tuple[int, str] | None = None
        for li, dc, _, ch, k in all_corners:
            if k == kind and dc == col and li > line_idx:
                if best is None or li < best[0]:
                    best = (li, ch)
        return best

    for li, col, _, ch, kind in all_corners:
        if kind != "top_left":
            continue
        tl_line = li
        tl_col = col
        # Find matching TR on the same line to the right
        tr = find_first_right(tl_line, tl_col, "top_right")
        if not tr:
            continue
        tr_col = tr[0]
        # Find BL in the same column as TL, below
        bl = find_first_below_at_col(tl_col, tl_line, "bottom_left")
        # Find BR in the same column as TR, below
        br_at_tr = find_first_below_at_col(tr_col, tl_line, "bottom_right")

        # Case 1: BL not exactly aligned — is there a nearby BL within 3 cols?
        if bl is None:
            for li2, dc, _, ch2, k in all_corners:
                if k == "bottom_left" and li2 > tl_line:
                    diff = dc - tl_col
                    if 0 < abs(diff) <= 3:
                        fix = (
                            f"FIX: Move '{ch2}' left by {diff} position(s) "
                            f"to column {tl_col + 1}"
                            if diff > 0
                            else f"FIX: Move '{ch2}' right by {abs(diff)} "
                            f"position(s) to column {tl_col + 1}"
                        )
                        issues.append(
                            Issue(
                                line=li2 + 1,
                                col=dc + 1,
                                type="BOX_CORNER_MISALIGNED",
                                msg=(
                                    f"Bottom-left corner '{ch2}' at column "
                                    f"{dc + 1} should align with top-left "
                                    f"'{ch}' at line {tl_line + 1}, column "
                                    f"{tl_col + 1}. {fix}"
                                ),
                            )
                        )
                        break

        # Case 2: BL found but BR not at TR column — is there a BR nearby?
        if bl is not None and br_at_tr is None:
            bl_line = bl[0]
            for li2, dc, _, ch2, k in all_corners:
                if k == "bottom_right" and li2 == bl_line:
                    diff = dc - tr_col
                    if 0 < abs(diff) <= 3:
                        fix = (
                            f"FIX: Move '{ch2}' left by {diff} position(s) "
                            f"to column {tr_col + 1}"
                            if diff > 0
                            else f"FIX: Move '{ch2}' right by {abs(diff)} "
                            f"position(s) to column {tr_col + 1}"
                        )
                        issues.append(
                            Issue(
                                line=li2 + 1,
                                col=dc + 1,
                                type="BOX_CORNER_MISALIGNED",
                                msg=(
                                    f"Bottom-right corner '{ch2}' at column "
                                    f"{dc + 1} should align with top-right "
                                    f"'{tr[2]}' "
                                    f"at line {tl_line + 1}, column "
                                    f"{tr_col + 1}. {fix}"
                                ),
                            )
                        )
                        break

        # Case 3: All four corners exist — check walls
        if bl is not None and br_at_tr is not None:
            bl_line = bl[0]
            for check_line in range(tl_line + 1, bl_line):
                # Left wall
                cc = char_at_display_col(lines[check_line], tl_col)
                if cc and cc not in LEFT_VERT and cc != " ":
                    for offset in (-2, -1, 1, 2):
                        nb = char_at_display_col(
                            lines[check_line], tl_col + offset
                        )
                        if nb and nb in LEFT_VERT:
                            fix = (
                                f"FIX: Move '│' left by {offset} position(s) "
                                f"to column {tl_col + 1}"
                                if offset > 0
                                else f"FIX: Move '│' right by {abs(offset)} "
                                f"position(s) to column {tl_col + 1}"
                            )
                            issues.append(
                                Issue(
                                    line=check_line + 1,
                                    col=tl_col + offset + 1,
                                    type="BOX_WALL_MISALIGNED",
                                    msg=(
                                        f"Left wall '│' at column "
                                        f"{tl_col + offset + 1} should "
                                        f"align with box corner at column "
                                        f"{tl_col + 1}. {fix}"
                                    ),
                                )
                            )
                            break
                # Right wall
                cc = char_at_display_col(lines[check_line], tr_col)
                if cc and cc not in RIGHT_VERT and cc != " ":
                    for offset in (-2, -1, 1, 2):
                        nb = char_at_display_col(
                            lines[check_line], tr_col + offset
                        )
                        if nb and nb in RIGHT_VERT:
                            fix = (
                                f"FIX: Move '│' left by {offset} position(s) "
                                f"to column {tr_col + 1}"
                                if offset > 0
                                else f"FIX: Move '│' right by {abs(offset)} "
                                f"position(s) to column {tr_col + 1}"
                            )
                            issues.append(
                                Issue(
                                    line=check_line + 1,
                                    col=tr_col + offset + 1,
                                    type="BOX_WALL_MISALIGNED",
                                    msg=(
                                        f"Right wall '│' at column "
                                        f"{tr_col + offset + 1} should "
                                        f"align with box corner at column "
                                        f"{tr_col + 1}. {fix}"
                                    ),
                                )
                            )
                            break
    return issues


# ─── Per-file validation + reporting ────────────────────────────────────────
class FileResult(dict):
    def __init__(
        self,
        filename: str,
        status: str,
        *,
        line_count: int = 0,
        expected_width: int = 0,
        issues: list[Issue] | None = None,
        message: str | None = None,
    ):
        super().__init__(
            filename=filename,
            status=status,
            line_count=line_count,
            expected_width=expected_width,
            issues=issues or [],
            message=message,
        )


def validate_file(filename: str) -> FileResult:
    path = Path(filename)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return FileResult(
            filename, "ERROR", message=f"Cannot open file: {filename}"
        )
    except OSError as e:
        return FileResult(filename, "ERROR", message=f"Cannot open file: {e}")
    except UnicodeDecodeError as e:
        return FileResult(
            filename, "ERROR", message=f"File is not valid UTF-8: {e}"
        )

    lines = text.splitlines()
    if not lines:
        return FileResult(filename, "EMPTY", message="File is empty")

    issues: list[Issue] = []
    issues += check_group_widths(lines)
    issues += check_vertical_continuity(lines)
    issues += check_box_border_integrity(lines)
    issues += check_corner_neighbors(lines)
    issues += check_wide_chars(lines)
    issues += check_forbidden_chars(lines)
    issues += check_box_alignment(lines)
    issues += check_tabs(lines)

    # Sort issues for stable output: by line, col, type
    issues.sort(key=lambda it: (it["line"], it["col"], it["type"]))

    # Compute an expected width for the status line: max line width is
    # more informative here than the Perl script's global mode because
    # this validator is group-aware.
    widths = [line_display_width(ln) for ln in lines]
    max_w = max(widths) if widths else 0

    status = "PASS" if not issues else "FAIL"
    return FileResult(
        filename,
        status,
        line_count=len(lines),
        expected_width=max_w,
        issues=issues,
    )


def print_result(result: FileResult) -> None:
    status = result["status"]
    color = GREEN if status == "PASS" else RED if status == "FAIL" else YELLOW
    print()
    print(f"{BOLD}File: {result['filename']}{RESET}")
    print("=" * 78)
    print(f"Status: {color}{status}{RESET}")

    if status == "PASS":
        print(f"{GREEN}All checks passed.{RESET}")
        print(
            f"Lines: {result['line_count']}, "
            f"Max width: {result['expected_width']} characters"
        )
    elif status in ("ERROR", "EMPTY"):
        print(f"{YELLOW}{result['message']}{RESET}")
    else:
        print(
            f"Lines: {result['line_count']}, "
            f"Max width: {result['expected_width']} characters"
        )
        print()
        print(f"{CYAN}Issues Found:{RESET}")
        print("-" * 78)
        for idx, issue in enumerate(result["issues"], start=1):
            print(
                f"  {idx:3d}. Line {issue['line']:3d}, "
                f"Col {issue['col']:3d}: [{issue['type']}] {issue['msg']}"
            )
    print()


# ─── CLI entry point ───────────────────────────────────────────────────────
def main(argv: list[str]) -> int:
    if not argv:
        print(f"Usage: {Path(sys.argv[0]).name} <file1> [file2] [...]")
        print("       python3 bin/amw-validate-ascii.py diagrams/*.txt")
        return 1

    print()
    print(f"{BOLD}ASCII Diagram Validator (Python){RESET}")
    print("=" * 78)
    print(f"Checking {len(argv)} file(s)...")

    pass_count = 0
    fail_count = 0
    for file in argv:
        result = validate_file(file)
        print_result(result)
        if result["status"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1

    print()
    print(f"{BOLD}Summary{RESET}")
    print("=" * 78)
    print(f"Total files: {len(argv)}")
    print(f"{GREEN}Passed: {pass_count}{RESET}")
    if fail_count:
        print(f"{RED}Failed: {fail_count}{RESET}")
    print()
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
