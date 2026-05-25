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

Content-layer rules (T-030 — run on a code-masked copy so CSS/JS do not
false-positive; see mask_code_blocks):
    9.  em-dash density (3+ as prose punctuation)            severity=low
    10. "not just X but Y" construction                      severity=medium
    11. corporate filler (leverage/utilize/seamless/robust)  severity=low
    12. "In <year>," opener                                  severity=low
    13. fake persona / testimonial byline                    severity=medium
    14. "//"-kicker eyebrow label                            severity=medium
    15. mono-caps filler subtitle (heuristic)                severity=low
    16. unicode-glyph used as decoration                     severity=low
    17. passive voice >=25% of sentences (document-level)    severity=low

Usage:
    python3 bin/amw-ai-slop-check.py <html-or-svg-file> [--severity-threshold high|medium|low]

Exit codes:
    0  no violations at or above the severity threshold (default: high)
    1  violations at or above threshold — caller should treat as FAIL
    2  file unreadable / parse error

Output: JSON to stdout. See `--help` for the full schema.

Rationale: `ai-slop-avoid.md` documents the visual + content rules with examples
and rationale. This script enforces the subset that is reliably mechanical:
the eight visual rules (regex on raw HTML or pure-Python HSL math) plus nine
content-layer rules (T-030, regex on code-masked prose). The content rules are
mostly low/medium severity, so they surface for review without failing the
default `high` gate. Rules that require semantic judgment (e.g. "trust-marker
carpet", "weight soup") remain in the reference file for human + LLM review.
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

# --- Content-layer anti-slop (T-030) -----------------------------------------
# These scan the PROSE, not the CSS/JS. To keep line numbers accurate while
# avoiding false positives inside <script>/<style>, collect_violations runs them
# against a "masked" copy of the file where those blocks are blanked with spaces
# of equal length (offsets and newlines preserved). See mask_code_blocks().
CODE_BLOCK_RE = re.compile(r"(<(script|style)\b[^>]*>)(.*?)(</\2>)", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")

# Em-dash used as prose punctuation. Three or more in a document is an AI tell.
EM_DASH_RE = re.compile("—")
# "not just X but Y" rhetorical construction.
NOT_JUST_BUT_RE = re.compile(r"\bnot\s+just\b[^.?!<]{1,60}?\bbut\b", re.IGNORECASE)
# Corporate filler verbs/adjectives.
FILLER_WORD_RE = re.compile(
    r"\b(leverage|leveraging|utilize|utilizing|seamless|seamlessly|robust)\b", re.IGNORECASE
)
# "In <year>, ..." sentence opener (start of line, after sentence punctuation, or after a tag).
YEAR_OPENER_RE = re.compile(r"(?:^|[.!?]\s+|>\s*)In\s+20\d{2}\b\s*,", re.MULTILINE)
# Fake persona / testimonial byline: "Sarah J. — CEO at TechCorp" etc.
FAKE_PERSONA_RE = re.compile(
    r"[A-Z][a-z]+(?:\s+[A-Z]\.?)?\s*[—,\-]\s*"
    r"(?:CEO|CTO|CFO|COO|Founder|Co-?founder|Director|VP|Head\s+of|Manager|Lead)\b"
)
# "//"-kicker eyebrow label: `// SOLUTION` (not part of a URL).
SLASH_KICKER_RE = re.compile(r"(?<![:/\w])//\s+[A-Z][A-Za-z]{2,}")
# Mono-caps filler: 3+ all-caps words (>=3 letters) chained by punctuation/space.
MONOCAPS_FILLER_RE = re.compile(r"\b[A-Z]{3,}\b(?:[\s.·•|]+\b[A-Z]{3,}\b){2,}")
# Decorative arrow/diamond glyph used as a lead-in (bullet/eyebrow), not inline.
GLYPH_DECOR_RE = re.compile(
    "(?:^|>)\\s*[→➡➜➔⟶⇒✦✧◆◇▸]\\s+\\S",
    re.MULTILINE,
)
# Passive-voice approximation: be-verb + past participle.
PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ed|written|made|done|built|given|taken|"
    r"seen|known|shown|held|kept|sent|chosen|driven|grown|found|told|left|brought)\b",
    re.IGNORECASE,
)
SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")


def mask_code_blocks(text: str) -> str:
    """Blank <script>/<style> contents with equal-length spaces (offsets + newlines kept)."""

    def repl(m: re.Match[str]) -> str:
        masked_inner = re.sub(r"[^\n]", " ", m.group(3))
        return m.group(1) + masked_inner + m.group(4)

    return CODE_BLOCK_RE.sub(repl, text)


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


def _content_hits(masked: str, regex: re.Pattern[str], rule: str, severity: str) -> list[dict]:
    """Emit one violation per regex match in code-masked prose."""
    return [
        {
            "rule": rule,
            "severity": severity,
            "line": line_of_offset(masked, m.start()),
            "snippet": snippet(masked, m.start()),
        }
        for m in regex.finditer(masked)
    ]


def check_em_dash_density(masked: str) -> list[dict]:
    """T-030: 3+ em-dashes used as prose punctuation is an AI tell (one finding, document-level)."""
    hits = list(EM_DASH_RE.finditer(masked))
    if len(hits) < 3:
        return []
    first = hits[0]
    return [
        {
            "rule": f"T-030 content: {len(hits)} em-dashes as punctuation (use commas/parens/periods)",
            "severity": "low",
            "line": line_of_offset(masked, first.start()),
            "snippet": snippet(masked, first.start()),
        }
    ]


def check_not_just_but(masked: str) -> list[dict]:
    """T-030: the 'not just X but Y' rhetorical construction."""
    return _content_hits(masked, NOT_JUST_BUT_RE, "T-030 content: 'not just X but Y' AI construction", "medium")


def check_filler_words(masked: str) -> list[dict]:
    """T-030: corporate filler (leverage / utilize / seamless / robust)."""
    return _content_hits(masked, FILLER_WORD_RE, "T-030 content: corporate filler word", "low")


def check_year_opener(masked: str) -> list[dict]:
    """T-030: 'In <year>, ...' sentence opener."""
    return _content_hits(masked, YEAR_OPENER_RE, "T-030 content: 'In <year>,' opener", "low")


def check_fake_persona(masked: str) -> list[dict]:
    """T-030: fake persona / testimonial byline as demo data."""
    return _content_hits(masked, FAKE_PERSONA_RE, "T-030 content: fake persona byline (use real or clearly-placeholder data)", "medium")


def check_slash_kicker(masked: str) -> list[dict]:
    """T-030: '//'-kicker eyebrow label."""
    return _content_hits(masked, SLASH_KICKER_RE, "T-030 content: '//'-kicker eyebrow label", "medium")


def check_monocaps_filler(masked: str) -> list[dict]:
    """T-030: mono-caps filler subtitle (heuristic: 3+ all-caps words chained)."""
    return _content_hits(masked, MONOCAPS_FILLER_RE, "T-030 content: mono-caps filler subtitle (heuristic)", "low")


def check_glyph_decoration(masked: str) -> list[dict]:
    """T-030: decorative arrow/diamond glyph used as a lead-in bullet."""
    return _content_hits(masked, GLYPH_DECOR_RE, "T-030 content: unicode-glyph used as decoration", "low")


def check_passive_voice(masked: str) -> list[dict]:
    """T-030: passive-voice density >=25% of sentences (document-level heuristic)."""
    prose = TAG_RE.sub(" ", masked)
    sentences = [s for s in SENTENCE_SPLIT_RE.split(prose) if s.strip()]
    passives = PASSIVE_RE.findall(prose)
    if len(sentences) < 4 or not passives:
        return []
    if len(passives) / len(sentences) < 0.25:
        return []
    loc = PASSIVE_RE.search(masked)
    start = loc.start() if loc else 0
    pct = round(100 * len(passives) / len(sentences))
    return [
        {
            "rule": f"T-030 content: passive voice ~{pct}% of sentences (prefer active voice)",
            "severity": "low",
            "line": line_of_offset(masked, start),
            "snippet": snippet(masked, start),
        }
    ]


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
    # Content-layer checks (T-030) run on a code-masked copy so CSS/JS never
    # false-positive while line numbers stay accurate.
    masked = mask_code_blocks(text)
    violations.extend(check_em_dash_density(masked))
    violations.extend(check_not_just_but(masked))
    violations.extend(check_filler_words(masked))
    violations.extend(check_year_opener(masked))
    violations.extend(check_fake_persona(masked))
    violations.extend(check_slash_kicker(masked))
    violations.extend(check_monocaps_filler(masked))
    violations.extend(check_glyph_decoration(masked))
    violations.extend(check_passive_voice(masked))
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
