#!/usr/bin/env python3
"""
amw-figma-tokens-export.py — DESIGN.md (Variant 1) → Figma Tokens Studio JSON.

Reads a DESIGN.md file, parses its YAML frontmatter (Variant 1 canonical-template
schema), and emits a Tokens Studio JSON ready for import into the
"Tokens Studio for Figma" plugin (https://github.com/tokens-studio/figma-plugin).

The output schema is the classic Tokens Studio "single-set" form (the format the
plugin offers as its default JSON-file export):

    {
      "global": {
        "colors": {
          "primary": { "value": "#hex", "type": "color" },
          ...
        },
        "typography": {
          "body-md": {
            "value": {
              "fontFamily": "...",
              "fontSize": "16px",
              "fontWeight": 400,
              "lineHeight": 1.5,
              "letterSpacing": "0em"
            },
            "type": "typography"
          }
        },
        "spacing": { ... },
        "borderRadius": { ... }
      },
      "$themes": [],
      "$metadata": { "tokenSetOrder": ["global"] }
    }

Pass `--dtcg` to emit the modern W3C DTCG ($type/$value) form instead. The
plugin accepts both on import.

Usage:
    amw-figma-tokens-export.py <DESIGN.md> -o <figma-tokens.json> [--dtcg]

Exit codes:
    0  success
    1  invalid DESIGN.md frontmatter
    2  invocation error
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


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.+?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, Any]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        sys.stderr.write("ERROR: DESIGN.md is missing the YAML frontmatter block (--- ... ---).\n")
        sys.exit(1)
    block = m.group(1)
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        sys.stderr.write(f"ERROR: frontmatter is not valid YAML: {exc}\n")
        sys.exit(1)
    if not isinstance(data, dict):
        sys.stderr.write("ERROR: frontmatter must be a YAML mapping.\n")
        sys.exit(1)
    return data


def _kv(value: Any, ttype: str, dtcg: bool) -> dict[str, Any]:
    """Build a single token node in either DTCG or classic shape."""
    if dtcg:
        return {"$value": value, "$type": ttype}
    return {"value": value, "type": ttype}


def _resolve_ref(value: Any, fm: dict[str, Any]) -> Any:
    """Resolve a {colors.primary}-style token reference to its concrete value.
    If the reference cannot be resolved, return the original string unchanged so
    the export still produces something Tokens Studio can read."""
    if not isinstance(value, str):
        return value
    m = re.fullmatch(r"\{([\w.-]+)\}", value.strip())
    if not m:
        return value
    parts = m.group(1).split(".")
    cur: Any = fm
    for p in parts:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return value  # unresolved — pass through
    return cur


def build_tokens_tree(fm: dict[str, Any], dtcg: bool) -> dict[str, Any]:
    out: dict[str, Any] = {}

    # Colors
    colors = fm.get("colors")
    if isinstance(colors, dict):
        out["colors"] = {}
        for slot, hex_ in colors.items():
            if not isinstance(hex_, str):
                continue
            # Hex value must be uppercase #RRGGBB to round-trip cleanly
            v = hex_.strip()
            if not v.startswith("#"):
                continue
            out["colors"][slot] = _kv(v.upper(), "color", dtcg)

    # Typography — emit each slot as one composite token of type=typography
    typography = fm.get("typography")
    if isinstance(typography, dict):
        out["typography"] = {}
        for slot, block in typography.items():
            if not isinstance(block, dict):
                continue
            composite: dict[str, Any] = {}
            ff = block.get("fontFamily")
            if isinstance(ff, str):
                composite["fontFamily"] = ff
            fs = block.get("fontSize")
            if fs is not None:
                composite["fontSize"] = str(fs) if isinstance(fs, (int, float)) else fs
            fw = block.get("fontWeight")
            if fw is not None:
                composite["fontWeight"] = fw
            lh = block.get("lineHeight")
            if lh is not None:
                composite["lineHeight"] = lh
            ls = block.get("letterSpacing")
            if ls is not None:
                composite["letterSpacing"] = ls
            if composite:
                out["typography"][slot] = _kv(composite, "typography", dtcg)

    # Spacing
    spacing = fm.get("spacing")
    if isinstance(spacing, dict):
        out["spacing"] = {}
        for slot, val in spacing.items():
            if slot == "base":
                # `base` is documentation-only in DESIGN.md frontmatter; still emit
                # it so it survives round-trip.
                pass
            if val is None:
                continue
            out["spacing"][slot] = _kv(str(val), "spacing", dtcg)

    # Border radius — DESIGN.md uses `rounded:`, Tokens Studio uses `borderRadius`.
    rounded = fm.get("rounded")
    if isinstance(rounded, dict):
        out["borderRadius"] = {}
        for slot, val in rounded.items():
            if val is None:
                continue
            out["borderRadius"][slot] = _kv(str(val), "borderRadius", dtcg)

    # Components — emit as composite "componentTokens" (custom group, Tokens
    # Studio surfaces unknown types as raw strings, no breakage).
    components = fm.get("components")
    if isinstance(components, dict):
        out["components"] = {}
        for comp_name, comp_block in components.items():
            if not isinstance(comp_block, dict):
                continue
            comp_emit: dict[str, Any] = {}
            for prop, val in comp_block.items():
                resolved = _resolve_ref(val, fm)
                # Determine type heuristically
                ttype = "color" if isinstance(resolved, str) and resolved.startswith("#") else "other"
                if prop in ("padding", "margin", "gap"):
                    ttype = "spacing"
                elif prop == "rounded":
                    ttype = "borderRadius"
                comp_emit[prop] = _kv(resolved if isinstance(resolved, (str, int, float, dict)) else str(resolved), ttype, dtcg)
            if comp_emit:
                out["components"][comp_name] = comp_emit

    return out


def build_tokens_studio_doc(fm: dict[str, Any], dtcg: bool) -> dict[str, Any]:
    tree = build_tokens_tree(fm, dtcg)
    return {
        "global": tree,
        "$themes": [],
        "$metadata": {
            "tokenSetOrder": ["global"],
            "amwSource": "DESIGN.md",
            "amwName": fm.get("name", ""),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("design_md_path", help="Path to DESIGN.md")
    parser.add_argument("-o", "--output", required=True, help="Output figma-tokens.json path")
    parser.add_argument("--dtcg", action="store_true", help="Emit DTCG ($type/$value) form instead of classic (value/type)")

    args = parser.parse_args(argv)

    md_path = Path(args.design_md_path)
    if not md_path.is_file():
        sys.stderr.write(f"ERROR: DESIGN.md not found: {md_path}\n")
        return 2

    text = md_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    doc = build_tokens_studio_doc(fm, dtcg=args.dtcg)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    counts = {k: len(v) for k, v in doc["global"].items() if isinstance(v, dict)}
    sys.stderr.write(f"OK: wrote {out_path} (groups: {counts}).\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
