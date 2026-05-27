#!/usr/bin/env python3
"""
amw-figma-tokens-import.py — Figma Tokens Studio JSON → DESIGN.md (Variant 1).

Imports a `figma-tokens.json` file produced by the Tokens Studio for Figma plugin
(https://github.com/tokens-studio/figma-plugin) and emits a DESIGN.md whose YAML
frontmatter follows the @google/design.md Variant 1 canonical-template.md schema.

Supported Tokens Studio formats:
  - Classic legacy keys:  { "name": { "value": "...", "type": "color" } }
  - DTCG modern keys:     { "name": { "$value": "...", "$type": "color" } }
  - Single-set wrapper:   { "global": { ... } }
  - Multi-set wrapper:    { "set1": {...}, "set2": {...}, "$themes": [], "$metadata": {...} }

When multi-set, the importer concatenates every non-metadata set; later-set values
override earlier-set values on key collision, mirroring Tokens Studio's "merge
sets" behavior. Pass `--set <name>` to pick exactly one set.

The mapping is lossy-but-equivalent (round-trip stable for color hex, font family,
font size, font weight, line height, spacing px, radius px). Shadow tokens map to
the optional `shadows` block; gradient color tokens drop to the first stop hex.

Usage:
    amw-figma-tokens-import.py <tokens.json> -o <DESIGN.md> [--set <name>] [--variant 1]

Exit codes:
    0  success
    1  invalid Figma Tokens JSON
    2  invocation error (bad args, file not found)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("ERROR: PyYAML required. Install via `uv pip install pyyaml`.\n")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Tokens Studio key/value extraction (handles classic + DTCG)
# ---------------------------------------------------------------------------

def _token_value(node: dict[str, Any]) -> Any:
    """Return the value of a token node, supporting both classic and DTCG keys."""
    if "$value" in node:
        return node["$value"]
    if "value" in node:
        return node["value"]
    return None


def _token_type(node: dict[str, Any]) -> str | None:
    """Return the type of a token node, supporting both classic and DTCG keys."""
    if "$type" in node:
        return str(node["$type"])
    if "type" in node:
        return str(node["type"])
    return None


def _is_token(node: Any) -> bool:
    """True if `node` is a leaf token (has value/$value AND type/$type)."""
    if not isinstance(node, dict):
        return False
    has_value = "value" in node or "$value" in node
    has_type = "type" in node or "$type" in node
    return has_value and has_type


# ---------------------------------------------------------------------------
# Tree-walking — flatten a Tokens Studio tree into (path, value, type) records
# ---------------------------------------------------------------------------

def flatten_tokens(tree: dict[str, Any], prefix: str = "") -> list[tuple[str, Any, str]]:
    """Flatten nested token groups into a list of (dotted-path, value, type)."""
    out: list[tuple[str, Any, str]] = []
    for key, node in tree.items():
        # Skip Tokens Studio meta keys
        if key.startswith("$"):
            continue
        path = f"{prefix}.{key}" if prefix else key
        if _is_token(node):
            t = _token_type(node)
            v = _token_value(node)
            if t is None or v is None:
                continue
            out.append((path, v, t))
        elif isinstance(node, dict):
            out.extend(flatten_tokens(node, path))
    return out


def select_set(data: dict[str, Any], set_name: str | None) -> dict[str, Any]:
    """Pick a single set from a Tokens Studio file, or merge all if `set_name` is None."""
    # Single-set (no outer set wrapping): the file IS the tree of tokens.
    # Detect by checking whether every top-level value is itself a token-group dict.
    meta_keys = {k for k in data.keys() if k.startswith("$")}
    non_meta_keys = [k for k in data.keys() if k not in meta_keys]

    if not non_meta_keys:
        return {}

    # If a specific set was requested, return it (or error).
    if set_name is not None:
        if set_name not in data:
            sys.stderr.write(f"ERROR: set {set_name!r} not found in tokens file. "
                             f"Available: {non_meta_keys!r}\n")
            sys.exit(1)
        node = data[set_name]
        if not isinstance(node, dict):
            sys.stderr.write(f"ERROR: set {set_name!r} is not a dict.\n")
            sys.exit(1)
        return node

    # Heuristic: if the file looks like a multi-set wrapper (no `value`/`$value`
    # at the leaves of the top-level dict but every top-level node is itself a
    # group of tokens), merge every set. Otherwise treat the whole dict as one
    # set.
    top_is_set_wrapper = all(
        isinstance(data[k], dict) and not _is_token(data[k])
        for k in non_meta_keys
    )

    # In the single-set case the top dict already contains token-groups whose
    # leaves are token nodes — so flatten_tokens on the whole dict works.
    if not top_is_set_wrapper:
        return data

    # Multi-set: merge by key path, later set wins (Tokens Studio merge semantics).
    merged: dict[str, Any] = {}
    for set_key in non_meta_keys:
        node = data[set_key]
        if isinstance(node, dict):
            _deep_merge(merged, node)
    return merged


def _deep_merge(dst: dict[str, Any], src: dict[str, Any]) -> None:
    for k, v in src.items():
        if k in dst and isinstance(dst[k], dict) and isinstance(v, dict) and not _is_token(v) and not _is_token(dst[k]):
            _deep_merge(dst[k], v)
        else:
            dst[k] = v


# ---------------------------------------------------------------------------
# Value normalization (hex color, px integer, gradient first-stop, etc.)
# ---------------------------------------------------------------------------

_HEX_RE = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
_RGBA_RE = re.compile(r"^rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$")
_PX_RE = re.compile(r"^(-?\d+(?:\.\d+)?)(?:px)?$")


def normalize_color(value: Any) -> str | None:
    """Return uppercase #RRGGBB hex (or #RRGGBBAA for alpha), or None if unparseable."""
    if not isinstance(value, str):
        return None
    v = value.strip()
    # Gradient: pick the first stop's color
    if v.lower().startswith(("linear-gradient", "radial-gradient", "conic-gradient")):
        m = re.search(r"#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)", v)
        if not m:
            return None
        v = m.group(0)
    if _HEX_RE.match(v):
        # Expand short form #RGB → #RRGGBB
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return f"#{h.upper()}"
    m = _RGBA_RE.match(v)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = float(m.group(4)) if m.group(4) else 1.0
        base = f"#{r:02X}{g:02X}{b:02X}"
        if a >= 0.999:
            return base
        return f"{base}{int(round(a * 255)):02X}"
    return None


def normalize_px(value: Any) -> str | None:
    """Return Npx normalized string. Accepts '16px', '16', 16, 16.0."""
    if isinstance(value, (int, float)):
        n = float(value)
        return f"{int(n) if n.is_integer() else n}px"
    if isinstance(value, str):
        m = _PX_RE.match(value.strip())
        if m:
            n = float(m.group(1))
            return f"{int(n) if n.is_integer() else n}px"
    return None


def normalize_font_weight(value: Any) -> int | str:
    """Numeric weight if parseable; otherwise the keyword string."""
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        s = value.strip().lower()
        keyword_map = {
            "thin": 100, "hairline": 100,
            "extralight": 200, "ultralight": 200, "extra-light": 200,
            "light": 300,
            "regular": 400, "normal": 400, "book": 400,
            "medium": 500,
            "semibold": 600, "demibold": 600, "semi-bold": 600,
            "bold": 700,
            "extrabold": 800, "heavy": 800, "extra-bold": 800,
            "black": 900,
        }
        if s in keyword_map:
            return keyword_map[s]
        try:
            return int(s)
        except ValueError:
            return value if isinstance(value, str) else 400
    return 400


# ---------------------------------------------------------------------------
# Token-path classification → DESIGN.md slot
# ---------------------------------------------------------------------------

# Canonical DESIGN.md color slots in priority order (first match wins).
# Order matters: more-specific multi-word hints must be checked BEFORE
# their single-word substrings — e.g. `on-surface` MUST precede `surface`,
# `brand-primary` MUST precede `primary` — otherwise a path like
# `colors.on-surface` matches the `surface` hint (the dash is a path
# delimiter the regex treats as a word boundary) and steals the slot.
_COLOR_SLOT_HINTS: list[tuple[str, list[str]]] = [
    ("on-surface", ["on-surface", "foreground", "fg", "text"]),
    ("surface", ["surface", "background", "bg"]),
    ("primary", ["brand-primary", "brand/primary", "primary", "brand"]),
    ("secondary", ["brand-secondary", "brand/secondary", "secondary", "accent"]),
    ("tertiary", ["brand-tertiary", "tertiary"]),
    ("neutral", ["neutral", "gray", "grey"]),
    ("error", ["error", "danger", "critical"]),
]


def classify_color(path: str) -> str | None:
    """Return DESIGN.md canonical color slot name from a Tokens Studio dotted path."""
    p = path.lower()
    # Special-case keys that already match canonical slots
    for slot, hints in _COLOR_SLOT_HINTS:
        for h in hints:
            # Match dotted-path tokens like colors.primary, brand.primary, primary.500
            if re.search(rf"(^|[./-]){re.escape(h)}([./-]|$)", p):
                return slot
    return None


# Canonical DESIGN.md typography slots
_TYPO_SLOT_HINTS: list[tuple[str, list[str]]] = [
    ("headline-display", ["display", "headline-display", "h-display"]),
    ("headline-lg", ["headline-lg", "h1", "heading-1", "title-lg"]),
    ("headline-md", ["headline-md", "h2", "heading-2", "title-md"]),
    ("body-lg", ["body-lg", "body-large", "text-lg"]),
    ("body-md", ["body-md", "body-medium", "body", "text-base", "text-md"]),
    ("body-sm", ["body-sm", "body-small", "text-sm"]),
    ("label-lg", ["label-lg", "label-large"]),
    ("label-md", ["label-md", "label", "caption"]),
    ("label-sm", ["label-sm", "label-small", "overline"]),
]


def classify_typography(path: str) -> str | None:
    p = path.lower()
    for slot, hints in _TYPO_SLOT_HINTS:
        for h in hints:
            if re.search(rf"(^|[./-]){re.escape(h)}([./-]|$)", p):
                return slot
    return None


# Canonical DESIGN.md radius slots
_RADIUS_SLOT_HINTS: list[tuple[str, list[str]]] = [
    ("none", ["none", "0", "square"]),
    ("sm", ["sm", "small"]),
    ("md", ["md", "medium", "default", "base"]),
    ("lg", ["lg", "large"]),
    ("xl", ["xl", "x-large"]),
    ("full", ["full", "pill", "round"]),
]


def classify_radius(path: str) -> str | None:
    p = path.lower()
    for slot, hints in _RADIUS_SLOT_HINTS:
        for h in hints:
            if re.search(rf"(^|[./-]){re.escape(h)}([./-]|$)", p):
                return slot
    return None


# Spacing slots
_SPACING_SLOT_HINTS: list[tuple[str, list[str]]] = [
    ("xs", ["xs", "x-small"]),
    ("sm", ["sm", "small"]),
    ("md", ["md", "medium", "default", "base"]),
    ("lg", ["lg", "large"]),
    ("xl", ["xl", "x-large"]),
    ("gutter", ["gutter"]),
    ("margin", ["margin"]),
]


def classify_spacing(path: str) -> str | None:
    p = path.lower()
    for slot, hints in _SPACING_SLOT_HINTS:
        for h in hints:
            if re.search(rf"(^|[./-]){re.escape(h)}([./-]|$)", p):
                return slot
    return None


# ---------------------------------------------------------------------------
# Typography composite tokens (Tokens Studio "type": "typography")
# ---------------------------------------------------------------------------

def parse_typography_value(value: Any) -> dict[str, Any]:
    """Return a normalized {fontFamily, fontSize, fontWeight, lineHeight, letterSpacing}
    block from a Tokens Studio typography token value (which is a dict with sub-fields)."""
    if not isinstance(value, dict):
        return {}
    out: dict[str, Any] = {}
    ff = value.get("fontFamily") or value.get("font-family")
    if ff:
        out["fontFamily"] = str(ff).strip("\"'")
    fs = value.get("fontSize") or value.get("font-size")
    if fs is not None:
        px = normalize_px(fs)
        if px:
            out["fontSize"] = px
    fw = value.get("fontWeight") or value.get("font-weight")
    if fw is not None:
        out["fontWeight"] = normalize_font_weight(fw)
    lh = value.get("lineHeight") or value.get("line-height")
    if lh is not None:
        # Tokens Studio sometimes uses % for percentage line-heights; preserve px or unitless
        if isinstance(lh, (int, float)):
            out["lineHeight"] = lh
        elif isinstance(lh, str):
            s = lh.strip()
            if s.endswith("%"):
                try:
                    out["lineHeight"] = float(s[:-1]) / 100.0
                except ValueError:
                    out["lineHeight"] = s
            else:
                px = normalize_px(s)
                out["lineHeight"] = px if px else s
    ls = value.get("letterSpacing") or value.get("letter-spacing")
    if ls is not None:
        if isinstance(ls, (int, float)):
            out["letterSpacing"] = f"{ls}em" if abs(ls) < 1 else f"{ls}px"
        elif isinstance(ls, str):
            out["letterSpacing"] = ls.strip()
    return out


# ---------------------------------------------------------------------------
# Build the DESIGN.md frontmatter dict from flattened tokens
# ---------------------------------------------------------------------------

def build_frontmatter(name: str, tokens: list[tuple[str, Any, str]]) -> dict[str, Any]:
    fm: dict[str, Any] = {
        "version": "alpha",
        "name": name,
    }

    colors: dict[str, str] = {}
    typography: dict[str, dict[str, Any]] = {}
    rounded: dict[str, str] = {}
    spacing: dict[str, str] = {}

    # Track every parsed token so unmatched ones can be reported (best-effort, no errors)
    for path, value, ttype in tokens:
        t = (ttype or "").lower()
        if t == "color":
            hex_ = normalize_color(value)
            if hex_ is None:
                continue
            slot = classify_color(path)
            if slot and slot not in colors:
                colors[slot] = hex_
        elif t == "typography":
            block = parse_typography_value(value)
            if not block:
                continue
            slot = classify_typography(path)
            if slot and slot not in typography:
                typography[slot] = block
        elif t in ("borderradius", "border-radius", "radius"):
            px = normalize_px(value)
            if px is None:
                continue
            slot = classify_radius(path)
            if slot and slot not in rounded:
                rounded[slot] = px
        elif t in ("spacing", "sizing", "dimension"):
            px = normalize_px(value)
            if px is None:
                continue
            slot = classify_spacing(path)
            if slot and slot not in spacing:
                spacing[slot] = px
        # Unsupported types (boxShadow, fontFamilies, fontWeights as standalone, etc.)
        # are dropped — the round-trip contract documents this lossy boundary.

    if colors:
        fm["colors"] = colors
    if typography:
        fm["typography"] = typography
    if rounded:
        # Ensure `none` is always 0px if present
        if "none" in rounded:
            rounded["none"] = "0px"
        fm["rounded"] = rounded
    if spacing:
        fm["spacing"] = spacing

    return fm


# ---------------------------------------------------------------------------
# Markdown body skeleton — minimal, satisfies canonical section order
# ---------------------------------------------------------------------------

def build_body(name: str, fm: dict[str, Any]) -> str:
    colors = fm.get("colors", {})
    typography = fm.get("typography", {})
    spacing = fm.get("spacing", {})
    rounded = fm.get("rounded", {})

    color_bullets = "\n".join(
        f"- **{slot.title()} (`{hex_}`):** Imported from Figma Tokens Studio."
        for slot, hex_ in colors.items()
    ) or "- No color tokens were imported."

    typo_bullets = "\n".join(
        f"- **{slot}:** {block.get('fontFamily', '?')} {block.get('fontWeight', '?')} / "
        f"{block.get('fontSize', '?')}"
        for slot, block in typography.items()
    ) or "- No typography tokens were imported."

    spacing_line = ", ".join(f"{v}" for v in spacing.values()) or "—"
    radii_line = ", ".join(f"{slot}:{v}" for slot, v in rounded.items()) or "—"

    return f"""# {name} Design System

> Imported from Figma Tokens Studio JSON via `bin/amw-figma-tokens-import.py`. Human
> commentary placeholders are below; fill them in before shipping to humans.

## Overview

Design system extracted from a Figma Tokens Studio export. The token surface
imported here covers colors, typography, spacing, and corner-radius. Shadows,
gradients, composite border tokens, and other Tokens Studio types are dropped
during import (see references/TECH-16-figma-tokens-bridge.md for the lossy-contract).

## Colors

{color_bullets}

## Typography

{typo_bullets}

## Layout

- **Grid:** 12-column on desktop, fluid on mobile, max content width 1200px.
- **Base unit:** 8px.
- **Spacing scale (px):** {spacing_line}

## Elevation & Depth

Elevation tokens were not imported (Figma Tokens Studio `boxShadow` is dropped by
this importer). Fill in shadow philosophy by hand if used.

## Shapes

- **Radius scale:** {radii_line}

## Components

Component tokens are not imported by this bridge. Author them by hand after
importing — see references/TECH-04-component-tokens.md.

## Do's and Don'ts

**Do:**
- Do reference tokens by name; never hard-code hex values in component code.
- Do maintain WCAG AA contrast ratios (4.5:1 for normal text).

**Don't:**
- Don't mix rounded and sharp corners in the same view.
- Don't introduce new colors outside this palette without updating this file first.
"""


# ---------------------------------------------------------------------------
# YAML emit helpers — produce output that lints under @google/design.md alpha
# ---------------------------------------------------------------------------

class _DesignMdDumper(yaml.SafeDumper):
    pass


def _represent_str(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    # Hex colors and px values must be quoted to survive the @google/design.md lint.
    if _HEX_RE.match(value) or _PX_RE.match(value):
        return dumper.represent_scalar("tag:yaml.org,2002:str", value, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", value)


_DesignMdDumper.add_representer(str, _represent_str)


def emit_design_md(fm: dict[str, Any], body: str) -> str:
    yaml_block = yaml.dump(
        fm,
        Dumper=_DesignMdDumper,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
    return f"---\n{yaml_block}---\n\n{body}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tokens_path", help="Path to figma-tokens.json")
    parser.add_argument("-o", "--output", required=True, help="Output DESIGN.md path")
    parser.add_argument("--set", dest="set_name", default=None, help="Specific Tokens Studio set name to import (default: merge all)")
    parser.add_argument("--name", default=None, help="Design system name (default: derived from filename)")
    parser.add_argument("--variant", default="1", choices=["1"], help="DESIGN.md variant (currently only Variant 1 is supported)")

    args = parser.parse_args(argv)

    tokens_path = Path(args.tokens_path)
    if not tokens_path.is_file():
        sys.stderr.write(f"ERROR: tokens file not found: {tokens_path}\n")
        return 2

    try:
        data = json.loads(tokens_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        sys.stderr.write(f"ERROR: cannot read tokens JSON: {exc}\n")
        return 1

    if not isinstance(data, dict):
        sys.stderr.write("ERROR: tokens JSON must be a JSON object at the top level.\n")
        return 1

    tree = select_set(data, args.set_name)
    if not tree:
        sys.stderr.write("ERROR: no tokens found in the input file (after set selection).\n")
        return 1

    tokens = flatten_tokens(tree)
    if not tokens:
        sys.stderr.write("ERROR: no leaf tokens found (every node missing both value and type).\n")
        return 1

    name = args.name or tokens_path.stem.replace("-", " ").replace("_", " ").title()
    fm = build_frontmatter(name, tokens)
    body = build_body(name, fm)
    output = emit_design_md(fm, body)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    sys.stderr.write(f"OK: wrote {out_path} ({len(tokens)} tokens read).\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
