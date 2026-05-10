#!/usr/bin/env python3
"""
amw-design-md-convert-v2-to-v1.py — Convert Variant 2 (community 9-section) → Variant 1 (canonical).

Parses a Variant 2 DESIGN.md (no YAML frontmatter; 9 numbered prose sections) and emits
a Variant 1 DESIGN.md (YAML frontmatter + 8 canonical sections + optional non-normative
"Agent Prompt Guide" tail).

Usage:
    python3 bin/amw-design-md-convert-v2-to-v1.py <input-v2.md> <output-v1.md> [--name NAME]

Exit codes:
    0  conversion successful
    2  invocation / parse error
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
COLOR_BULLET_RE = re.compile(
    r"^\s*-\s*\*\*([^*]+?)\*\*\s*\(\s*`([#a-fA-F0-9]+)`(?:\s*[/,]\s*`[^`]*`)*\s*\)\s*:\s*(.+)$"
)
TYPOGRAPHY_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+(?:\.\d+)?)px[^|]*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$")
RADIUS_BULLET_RE = re.compile(r"^\s*-\s*`?([\w-]+)`?\s*:\s*(\d+(?:\.\d+)?)\s*(px|em|rem)\s*$")


def split_v2_sections(content: str) -> dict[int, str]:
    """Split V2 content by '## N. Section Name' boundaries. Returns {section_number: body_text}."""
    out: dict[int, str] = {}
    current_n: int | None = None
    current_lines: list[str] = []
    for line in content.splitlines():
        m = re.match(r"^##\s+(\d+)\.\s+(.+?)\s*$", line)
        if m:
            if current_n is not None:
                out[current_n] = "\n".join(current_lines)
            current_n = int(m.group(1))
            current_lines = []
        else:
            if current_n is not None:
                current_lines.append(line)
    if current_n is not None:
        out[current_n] = "\n".join(current_lines)
    return out


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "token"


def extract_colors_from_section(body: str) -> dict[str, str]:
    """Extract colors from V2 Section 2's bullets. Handle ### subsections (Primary, Secondary, etc.)."""
    out: dict[str, str] = {}
    current_subsection: str | None = None
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if h3:
            current_subsection = h3.group(1).lower().strip()
            continue
        m = COLOR_BULLET_RE.match(line)
        if m:
            descriptive_name = m.group(1).strip()
            hex_value = m.group(2).lower()
            if not HEX_RE.match(hex_value):
                continue
            slug = slugify(descriptive_name)
            # Disambiguate: if subsection hints at semantic role, prefer that
            if current_subsection:
                if "primary" in current_subsection and "primary" not in out:
                    slug = "primary"
                elif "secondary" in current_subsection and "secondary" not in out:
                    slug = "secondary"
                elif "tertiary" in current_subsection or "accent" in current_subsection:
                    if "tertiary" not in out:
                        slug = "tertiary"
                elif "surface" in current_subsection or "background" in current_subsection:
                    if "surface" not in out:
                        slug = "surface"
                elif "text" in current_subsection and "neutral" in current_subsection:
                    pass
                elif "semantic" in current_subsection or "status" in current_subsection:
                    pass
            if len(hex_value) == 4:
                hex_value = "#" + "".join(c * 2 for c in hex_value[1:])
            out[slug] = hex_value
    return out


def extract_typography_from_section(body: str) -> dict[str, dict]:
    """Extract typography from V2 Section 3's hierarchy table."""
    out: dict[str, dict] = {}
    in_table = False
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if "| Role" in line and "Font" in line and "Size" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table:
            if not line.startswith("|"):
                in_table = False
                continue
            m = TYPOGRAPHY_ROW_RE.match(line)
            if m:
                role, font, size, weight, lh, ls, _notes = m.groups()
                slug = slugify(role)
                row: dict = {
                    "fontFamily": font.strip(),
                    "fontSize": f"{int(float(size))}px",
                }
                # weight may be a number or named; convert if needed
                w = weight.strip().lower()
                weight_map = {"regular": 400, "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800, "black": 900, "light": 300, "thin": 100}
                if w in weight_map:
                    row["fontWeight"] = weight_map[w]
                else:
                    try:
                        row["fontWeight"] = int(w)
                    except ValueError:
                        row["fontWeight"] = 400
                # lineHeight: parse decimal
                lh_clean = lh.strip().split()[0].replace("(", "").replace(")", "")
                try:
                    row["lineHeight"] = float(lh_clean)
                except ValueError:
                    row["lineHeight"] = 1.5
                # letterSpacing
                ls_clean = ls.strip()
                if ls_clean and ls_clean.lower() not in ("normal", "0"):
                    row["letterSpacing"] = ls_clean
                out[slug] = row
    return out


def extract_radius_from_section(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    in_radius_subsection = False
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if h3:
            in_radius_subsection = "radius" in h3.group(1).lower()
            continue
        if in_radius_subsection:
            m = RADIUS_BULLET_RE.match(line)
            if m:
                slug = slugify(m.group(1))
                out[slug] = f"{m.group(2)}{m.group(3)}"
    if not out:
        out = {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"}
    return out


def extract_spacing_from_section(body: str) -> dict[str, str]:
    """Extract spacing scale from V2 Section 5 'Spacing System'."""
    for raw_line in body.splitlines():
        line = raw_line.strip()
        m = re.match(r"^-\s*Scale:\s*(.+)$", line)
        if m:
            values = re.findall(r"(\d+(?:\.\d+)?)\s*px", m.group(1))
            if values:
                names = ["xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl"]
                out: dict[str, str] = {}
                for i, v in enumerate(values[:8]):
                    name = names[i] if i < len(names) else f"step-{i}"
                    out[name] = f"{int(float(v))}px"
                if "md" not in out:
                    out["md"] = "16px"
                out["base"] = "16px"
                return out
    return {"base": "16px", "xs": "4px", "sm": "8px", "md": "16px", "lg": "32px", "xl": "64px"}


def extract_components_from_section(body: str, colors: dict[str, str]) -> dict[str, dict]:
    """Extract component variants from V2 Section 4."""
    out: dict[str, dict] = {}
    component_subsection: str | None = None
    variant_name: str | None = None
    current_props: dict[str, str] = {}

    def flush():
        nonlocal current_props, variant_name
        if variant_name and current_props:
            cname = f"{component_subsection or 'unknown'}-{slugify(variant_name)}".strip("-")
            out[cname] = current_props.copy()
        variant_name = None
        current_props = {}

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if h3:
            flush()
            sub = h3.group(1).lower()
            if "button" in sub:
                component_subsection = "button"
            elif "card" in sub or "container" in sub:
                component_subsection = "card"
            elif "input" in sub or "form" in sub:
                component_subsection = "input"
            else:
                component_subsection = slugify(h3.group(1))
            continue

        # Variant header: **Primary** or **Primary White**
        vm = re.match(r"^\*\*(.+?)\*\*\s*$", line)
        if vm and component_subsection:
            flush()
            variant_name = vm.group(1).strip()
            continue

        if not variant_name:
            continue
        bullet = re.match(r"^-\s*(\w[\w\s]*):\s*(.+)$", line)
        if bullet:
            prop_name = slugify(bullet.group(1)).replace("-", "")
            val = bullet.group(2).strip().strip("`")
            mapping = {
                "background": "backgroundColor",
                "text": "textColor",
                "padding": "padding",
                "radius": "rounded",
                "font": None,  # ignored — handled via typography map
            }
            # Find matching key
            mapped = None
            for k, v in mapping.items():
                if prop_name.startswith(k):
                    mapped = v
                    break
            if not mapped:
                continue
            # Try to swap raw hex for token reference
            if mapped in ("backgroundColor", "textColor"):
                hm = HEX_RE.search(val)
                if hm:
                    matched_hex = hm.group(0).lower()
                    if len(matched_hex) == 4:
                        matched_hex = "#" + "".join(c * 2 for c in matched_hex[1:])
                    for cname, cval in colors.items():
                        if cval.lower() == matched_hex:
                            current_props[mapped] = "{colors." + cname + "}"
                            break
                    else:
                        current_props[mapped] = matched_hex
            elif mapped == "rounded":
                rm = re.match(r"(\d+(?:\.\d+)?)\s*(px|em|rem)", val)
                if rm:
                    current_props[mapped] = f"{rm.group(1)}{rm.group(2)}"
            else:
                rm = re.match(r"(\d+(?:\.\d+)?)\s*(px|em|rem)", val)
                if rm:
                    current_props[mapped] = f"{rm.group(1)}{rm.group(2)}"
                else:
                    current_props[mapped] = val
    flush()
    return out


def emit_v1(brand_name: str, src_path: str, sections: dict[int, str]) -> str:
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    colors = extract_colors_from_section(sections.get(2, ""))
    typography = extract_typography_from_section(sections.get(3, ""))
    components = extract_components_from_section(sections.get(4, ""), colors)
    rounded = extract_radius_from_section(sections.get(5, ""))
    spacing = extract_spacing_from_section(sections.get(5, ""))

    lines = []
    lines.append("<!--")
    lines.append(f"Converted from Variant 2 (community 9-section) to Variant 1 (canonical Google) on {now}.")
    lines.append(f"Source: {src_path}")
    lines.append("Preserved as prose (no Variant 1 token slot): shadow rgba formulas, z-index scale,")
    lines.append("agent prompt guide content, breakpoint table.")
    lines.append("Fully mapped: colors, typography, spacing, rounded, components.")
    lines.append("-->")
    lines.append("---")
    lines.append("version: alpha")
    lines.append(f'name: "{brand_name}"')
    lines.append(f'description: "Converted from Variant 2 community 9-section format on {now}"')
    lines.append("")

    if colors:
        lines.append("colors:")
        for k, v in colors.items():
            lines.append(f'  {k}: "{v}"')
        lines.append("")

    if typography:
        lines.append("typography:")
        for tname, trow in typography.items():
            lines.append(f"  {tname}:")
            lines.append(f'    fontFamily: "{trow["fontFamily"]}"')
            lines.append(f'    fontSize: "{trow["fontSize"]}"')
            lines.append(f"    fontWeight: {trow['fontWeight']}")
            lines.append(f"    lineHeight: {trow['lineHeight']}")
            if "letterSpacing" in trow:
                lines.append(f'    letterSpacing: "{trow["letterSpacing"]}"')
        lines.append("")

    if rounded:
        lines.append("rounded:")
        for k, v in rounded.items():
            lines.append(f'  {k}: "{v}"')
        lines.append("")

    if spacing:
        lines.append("spacing:")
        for k, v in spacing.items():
            lines.append(f'  {k}: "{v}"')
        lines.append("")

    if components:
        lines.append("components:")
        for cname, cdef in components.items():
            lines.append(f"  {cname}:")
            for prop, val in cdef.items():
                lines.append(f'    {prop}: "{val}"')
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"# {brand_name} Design System")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    section1_body = sections.get(1, "").strip()
    if section1_body:
        # Take the first paragraph
        para = section1_body.split("\n\n")[0]
        lines.append(para)
    else:
        lines.append("(Overview section was empty in source.)")
    lines.append("")
    lines.append("## Colors")
    lines.append("")
    section2_body = sections.get(2, "").strip()
    if section2_body:
        # Reuse the V2 prose verbatim (excluding ### subsection headers if desired)
        lines.append(section2_body)
    lines.append("")
    lines.append("## Typography")
    lines.append("")
    section3_body = sections.get(3, "").strip()
    if section3_body:
        lines.append(section3_body)
    lines.append("")
    lines.append("## Layout")
    lines.append("")
    section5_body = sections.get(5, "").strip()
    if section5_body:
        lines.append(section5_body)
    section8_body = sections.get(8, "").strip()
    if section8_body:
        lines.append("")
        lines.append("### Responsive")
        lines.append("")
        lines.append(section8_body)
    lines.append("")
    lines.append("## Elevation & Depth")
    lines.append("")
    section6_body = sections.get(6, "").strip()
    if section6_body:
        lines.append(section6_body)
    lines.append("")
    lines.append("## Shapes")
    lines.append("")
    lines.append("Border-radius scale extracted; see frontmatter `rounded:`. The shape language is determined by the radius scale's progression.")
    lines.append("")
    lines.append("## Components")
    lines.append("")
    section4_body = sections.get(4, "").strip()
    if section4_body:
        lines.append(section4_body)
    lines.append("")
    lines.append("## Do's and Don'ts")
    lines.append("")
    section7_body = sections.get(7, "").strip()
    if section7_body:
        lines.append(section7_body)
    lines.append("")
    section9_body = sections.get(9, "").strip()
    if section9_body:
        lines.append("## Agent Prompt Guide")
        lines.append("")
        lines.append("(Preserved from V2 source as non-normative section per spec.md L350.)")
        lines.append("")
        lines.append(section9_body)
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Variant 2 DESIGN.md → Variant 1.")
    parser.add_argument("input", help="Input Variant 2 DESIGN.md")
    parser.add_argument("output", help="Output Variant 1 DESIGN.md")
    parser.add_argument("--name", default=None, help="Design system name (default: extracted from H1)")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.is_file():
        print(f"Error: file not found: {in_path}", file=sys.stderr)
        return 2

    content = in_path.read_text(encoding="utf-8")

    # Extract brand name from "# Design System Inspired by NAME"
    brand_name = args.name
    if not brand_name:
        m = re.match(r"^#\s+Design System Inspired by\s+(.+?)\s*$", content.splitlines()[0] if content.splitlines() else "")
        brand_name = m.group(1) if m else in_path.stem.title()

    sections = split_v2_sections(content)
    if not sections:
        print("Error: no V2 numbered sections found in input", file=sys.stderr)
        return 2

    v1 = emit_v1(brand_name, str(in_path), sections)
    Path(args.output).write_text(v1, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
