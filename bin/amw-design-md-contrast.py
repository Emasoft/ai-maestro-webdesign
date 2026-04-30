#!/usr/bin/env python3
"""
amw-design-md-contrast.py — WCAG-AA contrast checker for DESIGN.md.

Parses the YAML frontmatter, extracts every `colors.*` token, identifies semantic pairs
(by canonical naming: `X` + `on-X`, `X` + `X-foreground`, `X` + `text-on-X`), computes
the WCAG luminance contrast ratio, and reports each pair with WCAG class.

Usage:
    python3 bin/amw-design-md-contrast.py <DESIGN.md> [--threshold 4.5] [--json] [--all-pairs]

Exit codes:
    0  all pairs pass threshold (or no pairs to check)
    1  one or more pairs fail threshold
    2  invocation error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def hex_to_rgb(h: str) -> tuple[int, int, int] | None:
    m = HEX_RE.match(h.strip())
    if not m:
        return None
    s = m.group(1)
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def relative_luminance(r: int, g: int, b: int) -> float:
    def chan(c: int) -> float:
        cs = c / 255.0
        return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(hex_a: str, hex_b: str) -> float | None:
    rgb_a = hex_to_rgb(hex_a)
    rgb_b = hex_to_rgb(hex_b)
    if rgb_a is None or rgb_b is None:
        return None
    la = relative_luminance(*rgb_a)
    lb = relative_luminance(*rgb_b)
    lighter = max(la, lb)
    darker = min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_class(ratio: float) -> str:
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3.0:
        return "AA-large only"
    return "FAIL"


def parse_frontmatter_colors(content: str) -> dict[str, str]:
    """Extract colors.* from YAML frontmatter. Returns {token-name: hex}."""
    if not content.startswith("---"):
        return {}
    lines = content.splitlines()
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}
    fm_text = "\n".join(lines[1:end_idx])

    out: dict[str, str] = {}
    if HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            return {}
        colors = data.get("colors", {}) if isinstance(data, dict) else {}
        if isinstance(colors, dict):
            for k, v in colors.items():
                if isinstance(v, str) and HEX_RE.match(v):
                    out[str(k)] = v
        return out

    # Fallback: regex-based extraction of `colors:` block
    in_colors = False
    for raw_line in fm_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("colors:"):
            in_colors = True
            continue
        if in_colors:
            if not line.startswith(" "):  # back to top-level
                in_colors = False
                continue
            m = re.match(r"^\s+([A-Za-z0-9._-]+)\s*:\s*\"?(#[0-9a-fA-F]{3,8})\"?", line)
            if m:
                out[m.group(1)] = m.group(2)
    return out


def find_pairs(colors: dict[str, str]) -> list[tuple[str, str, str]]:
    """Detect canonical pairs. Returns list of (label, fg-name, bg-name)."""
    pairs = []
    seen = set()

    for k in colors:
        # X + on-X
        if not k.startswith("on-"):
            on_key = f"on-{k}"
            if on_key in colors and (k, on_key) not in seen:
                pairs.append((f"on-{k} on {k}", on_key, k))
                seen.add((k, on_key))
        # X + X-foreground
        fg_key = f"{k}-foreground"
        if fg_key in colors and (k, fg_key) not in seen:
            pairs.append((f"{fg_key} on {k}", fg_key, k))
            seen.add((k, fg_key))
        # X + text-on-X
        text_key = f"text-on-{k}"
        if text_key in colors and (k, text_key) not in seen:
            pairs.append((f"{text_key} on {k}", text_key, k))
            seen.add((k, text_key))

    # Standard convention: text-* on surface
    if "surface" in colors:
        for tname in ("text-primary", "text-secondary", "on-surface", "text", "foreground"):
            if tname in colors and ("surface", tname) not in seen:
                pairs.append((f"{tname} on surface", tname, "surface"))
                seen.add(("surface", tname))

    return pairs


def find_all_pairs(colors: dict[str, str]) -> list[tuple[str, str, str]]:
    """Generate all distinct color pairs (n*(n-1)/2)."""
    keys = list(colors.keys())
    pairs = []
    for i, a in enumerate(keys):
        for b in keys[i + 1 :]:
            pairs.append((f"{a} vs {b}", a, b))
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description="WCAG-AA contrast checker for DESIGN.md.")
    parser.add_argument("path", help="Path to DESIGN.md")
    parser.add_argument("--threshold", type=float, default=4.5, help="Pass threshold (default 4.5 for AA normal text)")
    parser.add_argument("--all-pairs", action="store_true", help="Check all distinct color pairs (verbose)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    p = Path(args.path)
    if not p.is_file():
        print(f"Error: file not found: {p}", file=sys.stderr)
        return 2

    content = p.read_text(encoding="utf-8")
    colors = parse_frontmatter_colors(content)

    if not colors:
        msg = "No colors.* tokens found in frontmatter"
        if args.json:
            print(json.dumps({"file": str(p), "verdict": "PASS", "results": [], "note": msg}))
        else:
            print(msg)
        return 0

    pairs = find_all_pairs(colors) if args.all_pairs else find_pairs(colors)
    if not pairs:
        msg = "No semantic color pairs detected (no on-X / X-foreground patterns)"
        if args.json:
            print(json.dumps({"file": str(p), "verdict": "PASS", "results": [], "note": msg}))
        else:
            print(msg)
        return 0

    results = []
    failures = 0
    for label, fg, bg in pairs:
        ratio = contrast_ratio(colors[fg], colors[bg])
        if ratio is None:
            results.append({"pair": label, "fg": fg, "bg": bg, "fg_value": colors[fg], "bg_value": colors[bg], "ratio": None, "wcag": "INVALID"})
            failures += 1
            continue
        cls = wcag_class(ratio)
        passed = ratio >= args.threshold
        if not passed:
            failures += 1
        results.append({
            "pair": label,
            "fg": fg, "bg": bg,
            "fg_value": colors[fg], "bg_value": colors[bg],
            "ratio": round(ratio, 2),
            "wcag": cls,
            "pass": passed,
        })

    if args.json:
        out = {
            "file": str(p),
            "threshold": args.threshold,
            "verdict": "FAIL" if failures else "PASS",
            "total_pairs": len(results),
            "failed": failures,
            "results": results,
        }
        print(json.dumps(out, indent=2))
    else:
        print(f"File: {p}")
        print(f"Threshold: {args.threshold}:1 (WCAG-AA normal text)")
        print(f"Pairs checked: {len(results)}")
        print()
        for r in results:
            check = "✓" if r.get("pass") else "✗"
            ratio_str = f"{r['ratio']}:1" if r["ratio"] is not None else "INVALID"
            print(f"  {check} {r['pair']}: {r['fg_value']} on {r['bg_value']} = {ratio_str} ({r['wcag']})")
        print()
        if failures:
            print(f"FAIL — {failures}/{len(results)} pair(s) below threshold")
        else:
            print("PASS — all pairs meet threshold")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
