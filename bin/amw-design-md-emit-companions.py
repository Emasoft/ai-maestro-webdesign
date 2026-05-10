#!/usr/bin/env python3
"""
amw-design-md-emit-companions.py — Emit four companion files from a DESIGN.md.

Generates:
    tokens.css                 — :root CSS custom properties
    tokens.json                — W3C Design Tokens 2025.10 format
    component-inventory.md     — human-readable component listing
    usage-prompt.md            — drop-in agent system prompt

All four derive from a single source-of-truth DESIGN.md. Re-running regenerates them
from the current DESIGN.md state.

Usage:
    python3 bin/amw-design-md-emit-companions.py <DESIGN.md> [--out-dir DIR] [--targets css,json,inventory,prompt]

Exit codes:
    0  emitted
    2  invocation / parse error
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
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


def parse_frontmatter(content: str) -> dict:
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
    if HAVE_YAML:
        try:
            return yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            return {}
    # Minimal fallback parser: only the most common shapes
    return _fallback_parse(fm_text)


def _fallback_parse(text: str) -> dict:
    out: dict[str, Any] = {}
    cur_key = None
    cur_sub = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        leading = len(line) - len(line.lstrip())
        s = line.strip()
        if leading == 0 and ":" in s:
            k, _, v = s.partition(":")
            cur_key = k.strip()
            cur_sub = None
            v = v.strip().strip('"\'')
            out[cur_key] = v if v else {}
        elif leading == 2 and cur_key:
            k, _, v = s.partition(":")
            cur_sub = k.strip()
            v = v.strip().strip('"\'')
            if not isinstance(out.get(cur_key), dict):
                out[cur_key] = {}
            out[cur_key][cur_sub] = v if v else {}
        elif leading == 4 and cur_key and cur_sub:
            k, _, v = s.partition(":")
            v = v.strip().strip('"\'')
            parent = out.setdefault(cur_key, {}).setdefault(cur_sub, {})
            if not isinstance(parent, dict):
                out[cur_key][cur_sub] = {}
                parent = out[cur_key][cur_sub]
            try:
                v_typed = int(v)
            except (ValueError, TypeError):
                try:
                    v_typed = float(v)
                except (ValueError, TypeError):
                    v_typed = v
            parent[k.strip()] = v_typed
    return out


def resolve_ref(value: Any, fm: dict) -> Any:
    """If value is a {path.to.token}, walk the tree and return the resolved value. Else return as-is."""
    if not isinstance(value, str):
        return value
    m = re.match(r"^\{([a-zA-Z0-9._-]+)\}$", value.strip())
    if not m:
        return value
    path = m.group(1)
    node: Any = fm
    for seg in path.split("."):
        if isinstance(node, dict) and seg in node:
            node = node[seg]
        else:
            return value  # unresolved — return raw reference
    return node


def emit_tokens_css(fm: dict) -> str:
    lines = ["/* Auto-generated from DESIGN.md. Do not edit by hand. */", "", ":root {"]
    colors = fm.get("colors") or {}
    if isinstance(colors, dict) and colors:
        lines.append("  /* Colors */")
        for k, v in colors.items():
            resolved = resolve_ref(v, fm)
            lines.append(f"  --{k}: {resolved};")
        lines.append("")
    typography = fm.get("typography") or {}
    if isinstance(typography, dict) and typography:
        lines.append("  /* Typography */")
        # Emit one var per (level, sub-field)
        for tname, trow in typography.items():
            if not isinstance(trow, dict):
                continue
            for sub_field, css_var_suffix in [
                ("fontFamily", "font-family"),
                ("fontSize", "font-size"),
                ("fontWeight", "font-weight"),
                ("lineHeight", "line-height"),
                ("letterSpacing", "letter-spacing"),
            ]:
                v = trow.get(sub_field)
                if v is not None:
                    lines.append(f"  --{css_var_suffix}-{tname}: {v};")
        lines.append("")
    rounded = fm.get("rounded") or {}
    if isinstance(rounded, dict) and rounded:
        lines.append("  /* Rounded */")
        for k, v in rounded.items():
            lines.append(f"  --rounded-{k}: {resolve_ref(v, fm)};")
        lines.append("")
    spacing = fm.get("spacing") or {}
    if isinstance(spacing, dict) and spacing:
        lines.append("  /* Spacing */")
        for k, v in spacing.items():
            lines.append(f"  --space-{k}: {resolve_ref(v, fm)};")
        lines.append("")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def w3c_type_for_group(group: str) -> str:
    return {
        "colors": "color",
        "typography": "typography",
        "rounded": "dimension",
        "spacing": "dimension",
    }.get(group, "string")


def emit_tokens_json(fm: dict) -> str:
    out: dict[str, Any] = {}
    for group in ("colors", "typography", "rounded", "spacing", "components"):
        node = fm.get(group)
        if not isinstance(node, dict):
            continue
        out[group] = {}
        for k, v in node.items():
            if group == "typography" and isinstance(v, dict):
                out[group][k] = {"$value": v, "$type": "typography"}
            elif group == "components" and isinstance(v, dict):
                out[group][k] = {}
                for prop, pv in v.items():
                    out[group][k][prop] = {
                        "$value": pv,
                        "$type": _infer_type_for_property(prop),
                    }
            else:
                out[group][k] = {"$value": v, "$type": w3c_type_for_group(group)}
    return json.dumps(out, indent=2)


def _infer_type_for_property(prop: str) -> str:
    p = prop.lower()
    if "color" in p:
        return "color"
    if p in ("rounded", "padding", "size", "height", "width", "margin", "gap"):
        return "dimension"
    if p == "typography":
        return "typography"
    return "string"


def emit_component_inventory(fm: dict) -> str:
    lines = ["# Component Inventory", "",
             "Generated from DESIGN.md. Do not edit by hand.", ""]
    components = fm.get("components") or {}
    if not isinstance(components, dict) or not components:
        lines.append("No components declared in DESIGN.md frontmatter.")
        return "\n".join(lines)
    # Group by base name
    groups: dict[str, list[str]] = {}
    for cname in components:
        base = cname.split("-")[0]
        groups.setdefault(base, []).append(cname)

    for base, members in sorted(groups.items()):
        lines.append(f"## {base.title()}s")
        lines.append("")
        for cname in members:
            cdef = components[cname]
            if not isinstance(cdef, dict):
                continue
            lines.append(f"### `{cname}`")
            lines.append("")
            lines.append("| Property | Value (resolved) | Source |")
            lines.append("|---|---|---|")
            for prop, val in cdef.items():
                resolved = resolve_ref(val, fm)
                source = val if val != resolved else "(literal)"
                lines.append(f"| {prop} | `{resolved}` | `{source}` |")
            lines.append("")
    return "\n".join(lines)


def emit_usage_prompt(fm: dict) -> str:
    name = fm.get("name", "Design System")
    lines = [
        "# Design System Reference Prompt",
        "",
        f"You are generating UI for the {name} design system. Apply ALL of the following constraints when writing HTML, JSX, CSS, or Tailwind classes.",
        "",
        "## Colors (use semantic names; never inline hex)",
        "",
    ]
    colors = fm.get("colors") or {}
    if isinstance(colors, dict):
        for k, v in colors.items():
            resolved = resolve_ref(v, fm)
            lines.append(f"- {k}: `--{k}` ({resolved})")
        lines.append("")
    lines.append("## Typography")
    lines.append("")
    typography = fm.get("typography") or {}
    if isinstance(typography, dict):
        for tname, trow in typography.items():
            if not isinstance(trow, dict):
                continue
            ff = trow.get("fontFamily", "")
            fs = trow.get("fontSize", "")
            fw = trow.get("fontWeight", "")
            lines.append(f"- {tname}: {ff} {fs} / {fw}")
        lines.append("")
    lines.append("## Spacing")
    lines.append("")
    spacing = fm.get("spacing") or {}
    if isinstance(spacing, dict):
        for k, v in spacing.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    lines.append("## Rules (hard constraints)")
    lines.append("")
    lines.append("- DO maintain WCAG AA contrast (4.5:1 normal text, 3:1 large text).")
    lines.append("- DO use semantic token names; never inline hex values.")
    lines.append("- DO respect the spacing scale; never use one-off values.")
    lines.append("- DON'T mix rounded and sharp corners in the same view.")
    lines.append("- DON'T introduce new colors without updating DESIGN.md first.")
    lines.append("")
    lines.append("If a component or token isn't defined here, stop and ask. Do not invent values.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit companion files from a DESIGN.md.")
    parser.add_argument("path", help="Path to DESIGN.md")
    parser.add_argument("--out-dir", default=None, help="Output directory (default: same as DESIGN.md)")
    parser.add_argument("--targets", default="css,json,inventory,prompt", help="Comma-separated subset of: css,json,inventory,prompt")
    args = parser.parse_args()

    p = Path(args.path)
    if not p.is_file():
        print(f"Error: file not found: {p}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir) if args.out_dir else p.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    content = p.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    if not fm:
        print("Error: could not parse DESIGN.md frontmatter", file=sys.stderr)
        return 2

    targets = {t.strip() for t in args.targets.split(",")}

    written = []
    if "css" in targets:
        css = emit_tokens_css(fm)
        css_path = out_dir / "tokens.css"
        css_path.write_text(css, encoding="utf-8")
        written.append(str(css_path))

    if "json" in targets:
        js = emit_tokens_json(fm)
        json_path = out_dir / "tokens.json"
        json_path.write_text(js, encoding="utf-8")
        written.append(str(json_path))

    if "inventory" in targets:
        inv = emit_component_inventory(fm)
        inv_path = out_dir / "component-inventory.md"
        inv_path.write_text(inv, encoding="utf-8")
        written.append(str(inv_path))

    if "prompt" in targets:
        pr = emit_usage_prompt(fm)
        pr_path = out_dir / "usage-prompt.md"
        pr_path.write_text(pr, encoding="utf-8")
        written.append(str(pr_path))

    print("Emitted:")
    for w in written:
        print(f"  {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
