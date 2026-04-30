#!/usr/bin/env python3
# AI-Slop Check
# author: emasoft
# license: MIT
"""amw-ai-slop-check.py — mechanical enforcement of `amw-design-principles/ai-slop-avoid.md`.

Replaces the LLM-based "re-read the 237-line checklist" loop that four agents
ran independently every Phase B run. Each rule below maps to one numbered
entry in `skills/amw-design-principles/ai-slop-avoid.md`; the rationale lives
in the reference file, the gate lives here.

Detected rules:
    1. Rule 1 (linear-gradient on backgrounds)               severity=high
    2. Rule 2 (border-radius + colored border-left)          severity=medium
    3. Rule 4 (emoji density >3 per hero/h1/h2/cta block)    severity=medium
    4. Rule 7 (banned default fonts)                         severity=high
    5. Rule 23 (saturation at the ceiling — raw primaries)   severity=low
    6. Rule 26 (scrollIntoView)                              severity=high
    7. Rule 1 specialization (mauve-teal / purple-cyan duo)  severity=high
    8. Rule 3 (AI-drawn SVG faces / eyes pair)               severity=medium

Usage:
    python3 bin/amw-ai-slop-check.py <html-or-svg-file> [--severity-threshold high|medium|low]

Exit codes:
    0  no violations at or above the severity threshold (default: high)
    1  violations at or above threshold — caller should treat as FAIL
    2  file unreadable / parse error

Output: JSON to stdout. See `--help` for the full schema.

Rationale: `ai-slop-avoid.md` documents 26 rules with examples and rationale.
This script enforces the eight rules that are reliably mechanical (regex on
raw HTML or pure-Python HSL math). The other 18 rules (e.g. "trust-marker
carpet", "filler paragraphs", "weight soup") require semantic judgment and
remain in the reference file as documentation for human + LLM review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2}

# Rule 1 — linear-gradient on backgrounds. Two hex stops, no oklch fallback in vicinity.
LINEAR_GRADIENT_RE = re.compile(
    r"linear-gradient\s*\(\s*[0-9]+deg\s*,\s*(#[0-9a-fA-F]{3,8})\s*,\s*(#[0-9a-fA-F]{3,8})\s*\)"
)

# Rule 2 — border-radius + colored border-left in same declaration block. Either order.
BORDER_RADIUS_LEFT_A = re.compile(
    r"border-radius\s*:[^;]+;[^}]*border-left\s*:\s*\d+px\s+solid\s+#[0-9a-fA-F]{3,8}",
    re.IGNORECASE,
)
BORDER_RADIUS_LEFT_B = re.compile(
    r"border-left\s*:\s*\d+px\s+solid\s+#[0-9a-fA-F]{3,8}[^}]*;[^}]*border-radius\s*:",
    re.IGNORECASE,
)

# Rule 4 — emoji density. Unicode ranges per the task spec.
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F000-\U0001F02F"
    "]"
)
HERO_BLOCK_RE = re.compile(
    r"<(h1|h2)\b[^>]*>(.*?)</\1>|"
    r"<[^>]*class\s*=\s*[\"'][^\"']*\b(hero|cta)\b[^\"']*[\"'][^>]*>(.*?)</[a-zA-Z0-9]+>",
    re.IGNORECASE | re.DOTALL,
)

# Rule 7 — banned default fonts. Case-insensitive, must be a font-family declaration.
BANNED_FONT_RE = re.compile(
    r"font-family\s*:\s*['\"]?\s*(Inter|Roboto|Arial|Poppins|Fraunces|system-ui)\b",
    re.IGNORECASE,
)

# Rule 23 — raw screen primaries: #FF0000, #00FF00, #0000FF, #FFFFFF, #000000.
RAW_PRIMARY_RE = re.compile(
    r"#(?:[Ff]{2}0{4}|0{2}[Ff]{2}0{2}|0{4}[Ff]{2}|[Ff]{6}|0{6})\b"
)

# Rule 26 — scrollIntoView. Always banned in this plugin.
SCROLL_INTO_VIEW_RE = re.compile(r"\.scrollIntoView\s*\(")

# Rule 3 — AI-drawn SVG eyes/face heuristic. Two <circle> in a small <svg>.
SVG_BLOCK_RE = re.compile(r"<svg\b[^>]*>(.*?)</svg>", re.IGNORECASE | re.DOTALL)
SVG_VIEWBOX_RE = re.compile(
    r"viewBox\s*=\s*[\"']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)\s*[\"']", re.IGNORECASE
)
SVG_WIDTH_HEIGHT_RE = re.compile(
    r"\bwidth\s*=\s*[\"']?(\d+)[\"']?\s+(?:[^>]*?)\bheight\s*=\s*[\"']?(\d+)", re.IGNORECASE
)
SVG_CIRCLE_RE = re.compile(
    r"<circle\b[^>]*\bcx\s*=\s*[\"']?([-\d.]+)[\"']?[^>]*\br\s*=\s*[\"']?([-\d.]+)",
    re.IGNORECASE,
)


def hex_to_hsl(hex_color: str) -> tuple[float, float, float]:
    """Convert #RGB / #RRGGBB to HSL. Returns (h_deg, s_pct, l_pct).

    Pure-stdlib, no colorsys dependency, ~10 LOC. Used by the mauve-teal
    gradient detector to flag the Stripe-2018-cliché color pair.
    """
    s = hex_color.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) < 6:
        return (0.0, 0.0, 0.0)
    r = int(s[0:2], 16) / 255.0
    g = int(s[2:4], 16) / 255.0
    b = int(s[4:6], 16) / 255.0
    cmax, cmin = max(r, g, b), min(r, g, b)
    delta = cmax - cmin
    lightness = (cmax + cmin) / 2.0
    if delta == 0:
        h = 0.0
        sat = 0.0
    else:
        sat = delta / (1.0 - abs(2.0 * lightness - 1.0)) if lightness not in (0.0, 1.0) else 0.0
        if cmax == r:
            h = ((g - b) / delta) % 6.0
        elif cmax == g:
            h = ((b - r) / delta) + 2.0
        else:
            h = ((r - g) / delta) + 4.0
        h *= 60.0
    return (h, sat * 100.0, lightness * 100.0)


def line_of_offset(text: str, offset: int) -> int:
    """Return 1-indexed line number of a string offset."""
    return text.count("\n", 0, offset) + 1


def snippet(text: str, offset: int, length: int = 100) -> str:
    """Return a single-line snippet around the offset, trimmed to `length`."""
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    raw = text[start:end].strip()
    return raw[:length] + ("..." if len(raw) > length else "")


def check_linear_gradient(text: str) -> list[dict]:
    """Rule 1 + mauve-teal specialization."""
    out: list[dict] = []
    for m in LINEAR_GRADIENT_RE.finditer(text):
        # Skip if the same declaration also has oklch( in the surrounding 200 chars.
        ctx = text[max(0, m.start() - 200) : min(len(text), m.end() + 200)]
        if "oklch(" in ctx:
            continue
        c1, c2 = m.group(1), m.group(2)
        out.append(
            {
                "rule": "Rule 1: linear-gradient on backgrounds",
                "severity": "high",
                "line": line_of_offset(text, m.start()),
                "snippet": snippet(text, m.start()),
            }
        )
        # Mauve-teal specialization: both stops in [240-300] (mauve/purple) or [160-200] (teal/cyan).
        h1, _, _ = hex_to_hsl(c1)
        h2, _, _ = hex_to_hsl(c2)

        def in_band(h: float) -> bool:
            return (240.0 <= h <= 300.0) or (160.0 <= h <= 200.0)

        if in_band(h1) and in_band(h2):
            out.append(
                {
                    "rule": "Rule 1 specialization: mauve-teal / purple-cyan gradient",
                    "severity": "high",
                    "line": line_of_offset(text, m.start()),
                    "snippet": snippet(text, m.start()),
                }
            )
    return out


def check_border_radius_left(text: str) -> list[dict]:
    """Rule 2: rounded-card + colored left-accent."""
    out: list[dict] = []
    for regex in (BORDER_RADIUS_LEFT_A, BORDER_RADIUS_LEFT_B):
        for m in regex.finditer(text):
            out.append(
                {
                    "rule": "Rule 2: border-radius + colored border-left",
                    "severity": "medium",
                    "line": line_of_offset(text, m.start()),
                    "snippet": snippet(text, m.start()),
                }
            )
    return out


def check_emoji_density(text: str) -> list[dict]:
    """Rule 4: >3 emoji in any single h1 / h2 / .hero / .cta block."""
    out: list[dict] = []
    for m in HERO_BLOCK_RE.finditer(text):
        body = m.group(2) or m.group(4) or ""
        count = len(EMOJI_RE.findall(body))
        if count > 3:
            out.append(
                {
                    "rule": "Rule 4: emoji density >3 in hero/headline block",
                    "severity": "medium",
                    "line": line_of_offset(text, m.start()),
                    "snippet": snippet(text, m.start()),
                }
            )
    return out


def check_banned_fonts(text: str) -> list[dict]:
    """Rule 7: default fonts (Inter / Roboto / Arial / Poppins / Fraunces / system-ui)."""
    return [
        {
            "rule": "Rule 7: banned default font",
            "severity": "high",
            "line": line_of_offset(text, m.start()),
            "snippet": snippet(text, m.start()),
        }
        for m in BANNED_FONT_RE.finditer(text)
    ]


def check_raw_primaries(text: str) -> list[dict]:
    """Rule 23: raw screen primaries #FF0000 / #00FF00 / #0000FF / #FFFFFF / #000000."""
    return [
        {
            "rule": "Rule 23: raw screen primary (use oklch instead)",
            "severity": "low",
            "line": line_of_offset(text, m.start()),
            "snippet": snippet(text, m.start()),
        }
        for m in RAW_PRIMARY_RE.finditer(text)
    ]


def check_scroll_into_view(text: str) -> list[dict]:
    """Rule 26: scrollIntoView is banned plugin-wide."""
    return [
        {
            "rule": "Rule 26: scrollIntoView is banned (use window.scrollTo)",
            "severity": "high",
            "line": line_of_offset(text, m.start()),
            "snippet": snippet(text, m.start()),
        }
        for m in SCROLL_INTO_VIEW_RE.finditer(text)
    ]


def check_svg_eye_pair(text: str) -> list[dict]:
    """Rule 3: AI-drawn faces / eyes — heuristic pair of <circle> in a small <svg>."""
    out: list[dict] = []
    for m in SVG_BLOCK_RE.finditer(text):
        svg_body = m.group(1)
        # Determine canvas size from viewBox first; fall back to width/height attributes.
        canvas_w = canvas_h = None
        vb = SVG_VIEWBOX_RE.search(m.group(0))
        if vb:
            canvas_w, canvas_h = float(vb.group(1)), float(vb.group(2))
        else:
            wh = SVG_WIDTH_HEIGHT_RE.search(m.group(0))
            if wh:
                canvas_w, canvas_h = float(wh.group(1)), float(wh.group(2))
        if canvas_w is None or canvas_w >= 100 or (canvas_h is not None and canvas_h >= 100):
            continue
        circles = [
            (float(c.group(1)), float(c.group(2))) for c in SVG_CIRCLE_RE.finditer(svg_body)
        ]
        if len(circles) < 2:
            continue
        # Eye-pair heuristic: any two circles with similar radii (within 20%) and
        # cx distance between 10% and 60% of canvas width.
        for i, (cx_i, r_i) in enumerate(circles):
            for cx_j, r_j in circles[i + 1 :]:
                if r_i <= 0 or r_j <= 0:
                    continue
                ratio = min(r_i, r_j) / max(r_i, r_j)
                dx = abs(cx_i - cx_j)
                if ratio >= 0.8 and 0.10 * canvas_w <= dx <= 0.60 * canvas_w:
                    out.append(
                        {
                            "rule": "Rule 3: AI-drawn SVG eye-pair pattern (heuristic)",
                            "severity": "medium",
                            "line": line_of_offset(text, m.start()),
                            "snippet": snippet(text, m.start()),
                        }
                    )
                    break
            else:
                continue
            break
    return out


def collect_violations(text: str) -> list[dict]:
    """Run every rule against the file text. Order is stable for deterministic output."""
    violations: list[dict] = []
    violations.extend(check_linear_gradient(text))
    violations.extend(check_border_radius_left(text))
    violations.extend(check_emoji_density(text))
    violations.extend(check_banned_fonts(text))
    violations.extend(check_raw_primaries(text))
    violations.extend(check_scroll_into_view(text))
    violations.extend(check_svg_eye_pair(text))
    return violations


def summarise(violations: list[dict]) -> dict:
    out = {"high": 0, "medium": 0, "low": 0, "total": len(violations)}
    for v in violations:
        sev = v.get("severity", "low")
        if sev in out:
            out[sev] += 1
    return out


def main() -> int:
    p = argparse.ArgumentParser(
        description="Mechanical enforcement of skills/amw-design-principles/ai-slop-avoid.md."
    )
    p.add_argument("file", help="HTML or SVG file to check")
    p.add_argument(
        "--severity-threshold",
        choices=["low", "medium", "high"],
        default="high",
        help="Exit 1 only when a violation at or above this severity is found (default: high).",
    )
    args = p.parse_args()

    path = Path(args.file)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        json.dump(
            {"file": str(path.resolve()), "error": f"unreadable: {exc}"},
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
        return 2

    violations = collect_violations(text)
    summary = summarise(violations)
    json.dump(
        {"file": str(path.resolve()), "violations": violations, "summary": summary},
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")

    threshold = SEVERITY_RANK[args.severity_threshold]
    if any(SEVERITY_RANK.get(v.get("severity", "low"), 0) >= threshold for v in violations):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
