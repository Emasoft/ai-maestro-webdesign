#!/usr/bin/env python3
"""
amw-design-md-from-codebase.py — Scan a project tree and draft a Variant 1 DESIGN.md.

Walks a project directory, extracts design tokens from Tailwind configs (regex-based),
CSS variables (`:root { --X: Y }`), package.json (frameworks + UI libraries + fonts),
and Tailwind utility-class frequency. Emits a draft DESIGN.md plus an extraction-notes.md.

Pure-Python; stdlib only (no jiti, no PyYAML required for output).

Usage:
    python3 bin/amw-design-md-from-codebase.py <project-root> [--max-files N] [--out PATH] [--name NAME]

Exit codes:
    0  DESIGN.md written
    2  invocation error
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
IGNORE_DIRS = {
    "node_modules", ".git", ".next", ".turbo", "dist", "build",
    "out", ".cache", "coverage", "__pycache__", ".venv", "venv",
    ".expo", ".vercel", ".svelte-kit", "target", ".pnpm-store", ".yarn",
}

SCAN_EXTS = {
    ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".vue", ".svelte", ".astro", ".html",
    ".json", ".yaml", ".yml",
}

TAILWIND_CONFIG_NAMES = {
    "tailwind.config.js", "tailwind.config.ts",
    "tailwind.config.mjs", "tailwind.config.cjs",
}

UI_LIBS = {
    "@radix-ui/": "radix",
    "class-variance-authority": "shadcn-style-cva",
    "@mui/material": "mui",
    "@chakra-ui/react": "chakra",
    "@mantine/": "mantine",
    "tailwind-merge": "tailwind-merge",
    "styled-components": "styled-components",
    "@emotion/": "emotion",
    "nativewind": "nativewind",
}

FONT_PACKAGES = {
    "@fontsource/": "fontsource",
    "next/font": "next-font",
}

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
CSS_VAR_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")
ROOT_BLOCK_RE = re.compile(r":root\s*(?:\[[^\]]+\])?\s*\{([^}]*)\}", re.DOTALL)
TW_CLASS_TEXT_RE = re.compile(r"\btext-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)\b")
TW_CLASS_FONT_RE = re.compile(r"\bfont-(sans|serif|mono|display)\b")
TW_CLASS_RADIUS_RE = re.compile(r"\brounded(?:-(none|sm|md|lg|xl|2xl|3xl|full))?\b")
TW_CLASS_PAD_RE = re.compile(r"\b(?:p|m|px|py|pt|pr|pb|pl|gap)-(\d+(?:\.\d+)?)\b")


def walk(root: Path, max_files: int) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in SCAN_EXTS or name in TAILWIND_CONFIG_NAMES or name == "package.json":
                out.append(p)
                if len(out) >= max_files:
                    return out
    return out


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def normalize_hex(h: str) -> str:
    h = h.lower()
    if len(h) == 4:
        return "#" + "".join(c * 2 for c in h[1:])
    if len(h) == 5:
        return "#" + "".join(c * 2 for c in h[1:])
    return h


def hsl_to_hex(h: float, s: float, l_val: float) -> str:
    s_n = s / 100.0
    l_n = l_val / 100.0
    def k(n: float) -> float: return (n + h / 30.0) % 12
    a = s_n * min(l_n, 1 - l_n)
    def f(n: float) -> float:
        kk = k(n)
        return l_n - a * max(-1.0, min(kk - 3, min(9 - kk, 1.0)))
    def to_hex(x: float) -> str:
        return "%02x" % int(round(255 * x))
    return f"#{to_hex(f(0))}{to_hex(f(8))}{to_hex(f(4))}"


def parse_hsl_string(raw: str) -> tuple[float, float, float] | None:
    parts = raw.strip().split()
    if len(parts) != 3:
        return None
    try:
        h = float(parts[0])
        s = float(parts[1].rstrip("%"))
        l_val = float(parts[2].rstrip("%"))
    except ValueError:
        return None
    return h, s, l_val


def extract_package_json(root: Path) -> dict:
    pkg = root / "package.json"
    if not pkg.exists():
        return {}
    try:
        data = json.loads(read(pkg))
    except json.JSONDecodeError:
        return {}
    deps = {**(data.get("dependencies") or {}), **(data.get("devDependencies") or {})}
    out = {
        "name": data.get("name"),
        "ui_libraries": [v for k, v in UI_LIBS.items() if any(d.startswith(k) for d in deps)],
        "font_packages": [v for k, v in FONT_PACKAGES.items() if any(d.startswith(k) for d in deps)],
        "frameworks": [],
    }
    for fw in ("next", "expo", "react-native", "astro", "vite", "nuxt", "@sveltejs/kit"):
        if fw in deps or any(d.startswith(fw) for d in deps):
            out["frameworks"].append(fw)
    if "tailwindcss" in deps:
        out["tailwind_version"] = deps["tailwindcss"]
    return out


def extract_css_vars(files: list[Path]) -> dict[str, str]:
    """Extract :root CSS vars across all .css/.scss files."""
    out: dict[str, str] = {}
    for p in files:
        if p.suffix.lower() not in {".css", ".scss", ".sass", ".less"}:
            continue
        content = read(p)
        for m_block in ROOT_BLOCK_RE.finditer(content):
            block = m_block.group(1)
            for m_var in CSS_VAR_RE.finditer(block):
                name, val = m_var.group(1).strip(), m_var.group(2).strip()
                # Try HSL triplet
                hsl = parse_hsl_string(val)
                if hsl:
                    out[name[2:]] = hsl_to_hex(*hsl)
                # Direct hex
                elif val.startswith("#") and HEX_RE.match(val):
                    out[name[2:]] = normalize_hex(val)
                else:
                    # Keep raw for non-color values (radius, etc.)
                    out[name[2:]] = val
    return out


def extract_tailwind_colors_regex(files: list[Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in files:
        if p.name not in TAILWIND_CONFIG_NAMES:
            continue
        content = read(p)
        # Regex extract every "key": "<#hex>" inside the colors block
        colors_match = re.search(r"colors\s*:\s*\{(.*?)\}\s*,?\s*(?:borderRadius|spacing|fontSize|fontFamily)", content, re.DOTALL)
        if not colors_match:
            continue
        block = colors_match.group(1)
        for m in re.finditer(r"['\"]?([\w-]+)['\"]?\s*:\s*['\"]?(#[0-9a-fA-F]{3,8})['\"]?", block):
            out[m.group(1)] = normalize_hex(m.group(2))
    return out


def collect_tailwind_class_freq(files: list[Path]) -> dict[str, Counter]:
    freq = {
        "text_size": Counter(),
        "font": Counter(),
        "radius": Counter(),
        "spacing": Counter(),
    }
    for p in files:
        if p.suffix.lower() not in {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".astro", ".html"}:
            continue
        content = read(p)
        for m in TW_CLASS_TEXT_RE.finditer(content):
            freq["text_size"][m.group(1)] += 1
        for m in TW_CLASS_FONT_RE.finditer(content):
            freq["font"][m.group(1)] += 1
        for m in TW_CLASS_RADIUS_RE.finditer(content):
            freq["radius"][m.group(1) or "default"] += 1
        for m in TW_CLASS_PAD_RE.finditer(content):
            freq["spacing"][m.group(1)] += 1
    return freq


def collect_hex_freq(files: list[Path]) -> Counter:
    freq: Counter = Counter()
    for p in files:
        if p.suffix.lower() not in {".css", ".scss", ".tsx", ".jsx", ".html"}:
            continue
        content = read(p)
        for m in HEX_RE.finditer(content):
            freq[normalize_hex(m.group(0))] += 1
    return freq


SEMANTIC_NAMES = ["primary", "secondary", "tertiary", "neutral", "surface", "on-surface", "border-subtle", "accent"]


def emit_design_md(name: str, root: Path, pkg: dict, css_vars: dict, tw_colors: dict, class_freq: dict, hex_freq: Counter) -> str:
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    lines = []
    lines.append("---")
    lines.append("version: alpha")
    lines.append(f'name: "{name}"')
    lines.append(f'description: "Auto-extracted from codebase at {root} on {now}"')
    lines.append("")

    # Colors: prefer CSS vars, then Tailwind regex, then hex frequency
    chosen_colors: dict[str, str] = {}
    if css_vars:
        for k, v in css_vars.items():
            if isinstance(v, str) and HEX_RE.match(v):
                # Normalize shadcn-style key: "primary-DEFAULT" → "primary"
                slug = re.sub(r"-DEFAULT$", "", k)
                chosen_colors[slug] = v
    elif tw_colors:
        chosen_colors = tw_colors
    else:
        # Fall back to top hex
        for i, (h, _c) in enumerate(hex_freq.most_common(8)):
            slug = SEMANTIC_NAMES[i] if i < len(SEMANTIC_NAMES) else f"discovered-{i}"
            chosen_colors[slug] = h

    if chosen_colors:
        lines.append("colors:")
        for k, v in chosen_colors.items():
            lines.append(f'  {k}: "{v}"')
        lines.append("")

    # Typography
    fonts = []
    if pkg.get("font_packages"):
        fonts = pkg["font_packages"]
    elif class_freq["font"]:
        fonts = list(class_freq["font"].keys())
    if fonts or class_freq["text_size"]:
        lines.append("typography:")
        # emit headline-display, headline-lg, headline-md, body-lg, body-md, body-sm, label-md with sane defaults
        common_levels = [
            ("headline-display", 48, 700, 1.1),
            ("headline-lg", 36, 600, 1.15),
            ("headline-md", 24, 600, 1.25),
            ("body-lg", 18, 400, 1.6),
            ("body-md", 16, 400, 1.6),
            ("body-sm", 14, 400, 1.5),
            ("label-md", 14, 500, 1.4),
        ]
        primary_font = "Inter"  # safe default
        if fonts:
            primary_font = fonts[0] if isinstance(fonts[0], str) else "Inter"
        for slug, size, weight, lh in common_levels:
            lines.append(f"  {slug}:")
            lines.append(f'    fontFamily: "{primary_font}"')
            lines.append(f'    fontSize: "{size}px"')
            lines.append(f"    fontWeight: {weight}")
            lines.append(f"    lineHeight: {lh}")
        lines.append("")

    # Rounded
    lines.append("rounded:")
    radii = {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"}
    if css_vars.get("radius"):
        # If `--radius: 0.5rem;` etc.
        lines.append(f'  md: "{css_vars["radius"]}"')
        for k in ("sm", "lg", "xl", "full"):
            lines.append(f'  {k}: "{radii[k]}"')
    else:
        for k, v in radii.items():
            lines.append(f'  {k}: "{v}"')
    lines.append("")

    # Spacing — default
    lines.append("spacing:")
    for k, v in [("base", "16px"), ("xs", "4px"), ("sm", "8px"), ("md", "16px"), ("lg", "32px"), ("xl", "64px")]:
        lines.append(f'  {k}: "{v}"')
    lines.append("")

    # Components — derive from chosen_colors if shadcn-style
    if "primary" in chosen_colors:
        lines.append("components:")
        lines.append("  button-primary:")
        lines.append('    backgroundColor: "{colors.primary}"')
        if "primary-foreground" in chosen_colors or "on-primary" in chosen_colors:
            text_ref = "primary-foreground" if "primary-foreground" in chosen_colors else "on-primary"
            lines.append(f'    textColor: "{{colors.{text_ref}}}"')
        lines.append('    typography: "{typography.label-md}"')
        lines.append('    rounded: "{rounded.md}"')
        lines.append('    padding: "12px"')
        if "secondary" in chosen_colors:
            lines.append("  button-secondary:")
            lines.append('    backgroundColor: "{colors.secondary}"')
            lines.append('    typography: "{typography.label-md}"')
            lines.append('    rounded: "{rounded.md}"')
            lines.append('    padding: "12px"')
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"# {name}")
    lines.append("")
    lines.append(f"> Auto-extracted from `{root}` on {now}.")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("This design system was auto-extracted from the codebase. The agent that ran the extraction inferred tokens from the project's Tailwind config, CSS custom properties, and utility-class usage frequency. Review every token before treating this file as canonical.")
    lines.append("")
    if pkg.get("frameworks"):
        lines.append(f"**Detected stack:** {', '.join(pkg['frameworks'])}")
    if pkg.get("ui_libraries"):
        lines.append(f"**UI libraries:** {', '.join(pkg['ui_libraries'])}")
    if pkg.get("font_packages"):
        lines.append(f"**Font sources:** {', '.join(pkg['font_packages'])}")
    lines.append("")
    lines.append("## Colors")
    lines.append("")
    if chosen_colors:
        for k, v in chosen_colors.items():
            lines.append(f"- **{k.title()} (`{v}`):** Auto-extracted. Verify role and contrast.")
    lines.append("")
    lines.append("## Typography")
    lines.append("")
    lines.append("Auto-extracted typography levels are starting input. Verify font sizes against the project's actual usage, and add/remove levels as needed.")
    lines.append("")
    lines.append("## Layout")
    lines.append("")
    lines.append("Spacing scale defaults to 8px-base. Verify against the project's actual padding/margin values.")
    lines.append("")
    lines.append("## Elevation & Depth")
    lines.append("")
    lines.append("Not auto-extracted. Document the project's shadow philosophy and per-level shadow formulas here.")
    lines.append("")
    lines.append("## Shapes")
    lines.append("")
    lines.append("Default radius scale extracted. Verify the project's actual border-radius usage.")
    lines.append("")
    lines.append("## Components")
    lines.append("")
    if "primary" in chosen_colors:
        lines.append("- **Button (primary):** Uses `colors.primary` as background; verify hover/disabled states are documented.")
    lines.append("")
    lines.append("## Do's and Don'ts")
    lines.append("")
    lines.append("- Do reference tokens by name in component code; never inline hex.")
    lines.append("- Do maintain WCAG AA contrast (4.5:1 normal text, 3:1 large text).")
    lines.append("- Do respect the 8px grid for every spatial value.")
    lines.append("- Do use the primary color only for the single most important action per screen.")
    lines.append("- Don't introduce new colors outside this palette without updating this file first.")
    lines.append("- Don't use more than two font weights on a single screen.")
    lines.append("- Don't mix rounded and sharp corners in the same view.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a project tree and draft a Variant 1 DESIGN.md.")
    parser.add_argument("root", help="Project root path")
    parser.add_argument("--max-files", type=int, default=1500)
    parser.add_argument("--out", default=None)
    parser.add_argument("--name", default=None)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: not a directory: {root}", file=sys.stderr)
        return 2

    files = walk(root, args.max_files)
    pkg = extract_package_json(root)
    css_vars = extract_css_vars(files)
    tw_colors = extract_tailwind_colors_regex(files)
    class_freq = collect_tailwind_class_freq(files)
    hex_freq = collect_hex_freq(files)

    name = args.name or pkg.get("name") or root.name
    out_path = Path(args.out) if args.out else (root / "DESIGN.md")
    notes_path = out_path.with_suffix(".extraction-notes.md")

    md = emit_design_md(name, root, pkg, css_vars, tw_colors, class_freq, hex_freq)
    out_path.write_text(md, encoding="utf-8")

    notes = [
        f"# Extraction notes for {out_path.name}",
        "",
        f"Generated: {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
        f"Project root: {root}",
        f"Files inspected: {len(files)}",
        "",
        "## Sources used",
        "",
        f"- package.json: {'yes' if pkg else 'absent'}",
        f"- CSS :root variables: {len(css_vars)} variables",
        f"- tailwind.config.* (regex): {len(tw_colors)} colors extracted",
        f"- Tailwind class frequency: {sum(sum(c.values()) for c in class_freq.values())} class hits",
        f"- Hex literal frequency: {len(hex_freq)} distinct values",
        "",
        "## Caveats",
        "",
        "- Tailwind regex extraction is heuristic; it cannot evaluate JS so dynamic configs are not handled. For high-fidelity Tailwind extraction, use `bin/amw-design-md-from-tailwind.mjs` instead.",
        "- Component inference is limited to the shadcn pattern (`primary` + `primary-foreground`). For other libraries, edit the components: section manually.",
        "- The do/don't section uses generic placeholder rules. Customize for the project's actual conventions.",
        "",
        "## Validation next steps",
        "",
        "```bash",
        "bash bin/amw-design-md-lint.sh DESIGN.md",
        "python3 bin/amw-design-md-validate.py DESIGN.md",
        "python3 bin/amw-design-md-contrast.py DESIGN.md",
        "```",
    ]
    notes_path.write_text("\n".join(notes), encoding="utf-8")

    print(f"Wrote {out_path}")
    print(f"Wrote {notes_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
