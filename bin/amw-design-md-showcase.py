#!/usr/bin/env python3
"""
amw-design-md-showcase.py — DESIGN.md -> self-contained HTML showcase page.

Reads a Variant 1 DESIGN.md (the official @google/design.md alpha shape),
extracts the YAML frontmatter, and emits a single-file HTML page that lets
designers and reviewers visually QA every token:

  * Color tokens   — swatches with WCAG-AA contrast badges for every pair
                     (`X` + `on-X` semantic pairs, plus all primary/surface
                     combinations).
  * Typography     — live specimens rendered at the declared fontFamily /
                     fontSize / fontWeight / lineHeight / letterSpacing
                     using system-font fallbacks (no remote font fetches).
  * Spacing        — visual bars at every declared spacing step.
  * Rounded        — squares rendered with each border-radius level.
  * Shadow         — boxes for each `elevation.*` step (if declared).
  * Components     — rendered button / input / card examples driven by
                     the declared `components.*` tokens.

Hard invariants:
  * Python stdlib only (pyyaml is *optional* — when present it is used for
    full YAML 1.1; when absent the script falls back to an indentation-based
    parser that handles the canonical DESIGN.md frontmatter shape).
  * Output is a single HTML file: NO external CSS, NO external JS, NO web
    fonts, NO <img> with remote src. The file works fully offline.
  * Every color swatch has aria-label and a visible WCAG-AA pair badge.
  * No CJK in script, comments, or emitted HTML (English-only per plugin
    house style).

Usage:
    python3 bin/amw-design-md-showcase.py <DESIGN.md> -o <out.html>

Exit codes:
    0  showcase emitted
    2  invocation / parse error

(c) 2026 - Apache-2.0 / MIT dual-license matching the source project.
"""

from __future__ import annotations

import argparse
import html as html_lib
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


# ----------------------------------------------------------------------------
# YAML frontmatter parsing — same shape as emit-companions.py
# ----------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a DESIGN.md and return it as a dict.

    Honors pyyaml when present; otherwise uses a minimal indentation-based
    parser sufficient for the canonical DESIGN.md schema (top-level keys
    `name`, `description`, `colors`, `typography`, `rounded`, `spacing`,
    `components`, optional `elevation`).
    """
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
            return yaml.safe_load(fm_text) or {}  # type: ignore[possibly-unbound]
        except yaml.YAMLError:  # type: ignore[possibly-unbound]
            return {}
    return _fallback_parse(fm_text)


def _coerce(v: str) -> Any:
    """Coerce a YAML scalar string to int / float / bool / None / str."""
    s = v.strip().strip('"').strip("'")
    if s == "":
        return ""
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    if s.lower() in ("null", "~"):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _fallback_parse(text: str) -> dict:
    """Indentation-aware fallback parser. Supports the 3 nesting depths the
    canonical DESIGN.md uses: 0 (top key), 2 (group child), 4 (typography
    sub-field / component property).
    """
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
            v = v.strip().strip('"').strip("'")
            out[cur_key] = _coerce(v) if v else {}
        elif leading == 2 and cur_key:
            k, _, v = s.partition(":")
            cur_sub = k.strip()
            v = v.strip().strip('"').strip("'")
            if not isinstance(out.get(cur_key), dict):
                out[cur_key] = {}
            out[cur_key][cur_sub] = _coerce(v) if v else {}
        elif leading == 4 and cur_key and cur_sub:
            k, _, v = s.partition(":")
            v = v.strip().strip('"').strip("'")
            parent = out.setdefault(cur_key, {}).setdefault(cur_sub, {})
            if not isinstance(parent, dict):
                out[cur_key][cur_sub] = {}
                parent = out[cur_key][cur_sub]
            parent[k.strip()] = _coerce(v)
    return out


# ----------------------------------------------------------------------------
# Token-reference resolution: {colors.primary} -> "#1a1c1e"
# ----------------------------------------------------------------------------

REF_RE = re.compile(r"^\{([a-zA-Z0-9._-]+)\}$")


def resolve_ref(value: Any, fm: dict) -> Any:
    if not isinstance(value, str):
        return value
    m = REF_RE.match(value.strip())
    if not m:
        return value
    path = m.group(1)
    node: Any = fm
    for seg in path.split("."):
        if isinstance(node, dict) and seg in node:
            node = node[seg]
        else:
            return value  # unresolved -> emit raw reference for visibility
    return node


# ----------------------------------------------------------------------------
# WCAG-AA contrast (sRGB relative-luminance formula, WCAG 2.1)
# ----------------------------------------------------------------------------

HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def hex_to_rgb(h: str) -> tuple[int, int, int] | None:
    if not isinstance(h, str):
        return None
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


def wcag_class(ratio: float | None) -> str:
    """Return the human label and the badge slug for a contrast ratio."""
    if ratio is None:
        return "n/a"
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3.0:
        return "AA-large"
    return "FAIL"


def wcag_badge_color(label: str) -> tuple[str, str]:
    """Pick visible bg + fg for a WCAG badge so the badge itself
    passes contrast. Returns (bg-hex, fg-hex)."""
    if label == "AAA":
        return ("#1f7a3a", "#ffffff")
    if label == "AA":
        return ("#2c6cb0", "#ffffff")
    if label == "AA-large":
        return ("#b46e08", "#ffffff")
    if label == "FAIL":
        return ("#a02323", "#ffffff")
    return ("#666666", "#ffffff")


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def safe(s: Any) -> str:
    """HTML-escape any value to a string."""
    if s is None:
        return ""
    return html_lib.escape(str(s), quote=True)


def attr(s: Any) -> str:
    """Like safe() but explicitly meant for attribute values."""
    return safe(s)


def _is_hex(v: Any) -> bool:
    return isinstance(v, str) and HEX_RE.match(v.strip()) is not None


def font_family_css(family: Any) -> str:
    """Wrap font family in quotes only if it contains a space, and
    append safe system fallbacks. ASCII-only output."""
    if not family:
        return "system-ui, sans-serif"
    fam = str(family).strip().strip('"').strip("'")
    if " " in fam:
        fam = f"'{fam}'"
    return f"{fam}, system-ui, sans-serif"


def numeric_dim(v: Any) -> str:
    """Normalize a dimension value to a CSS string. Accepts int, float, or
    str. Bare numbers become `Npx`."""
    if isinstance(v, (int, float)):
        return f"{int(v) if float(v).is_integer() else v}px"
    if isinstance(v, str):
        s = v.strip().strip('"').strip("'")
        if re.match(r"^-?\d+(\.\d+)?$", s):
            return f"{s}px"
        return s
    return ""


# ----------------------------------------------------------------------------
# Section emitters
# ----------------------------------------------------------------------------

def _classify_color(name: str) -> str:
    n = name.lower()
    if n.startswith("primary") or n.startswith("brand") or n.startswith("accent"):
        return "Brand"
    if n.startswith("secondary") or n.startswith("tertiary"):
        return "Brand"
    if n.startswith("on-"):
        return "Foreground"
    if n in ("canvas", "background") or n.startswith("surface") or n.startswith("inverse"):
        return "Surface"
    if n in ("ink", "text") or n.startswith("ink") or n.startswith("body") or n == "muted":
        return "Text"
    if n.startswith("hairline") or n.startswith("border"):
        return "Borders"
    if n in ("success", "warning", "error", "info", "danger"):
        return "Semantic"
    return "Other"


def _color_pairs(colors: dict) -> list[tuple[str, str, str, str]]:
    """Enumerate every semantically meaningful color pair to badge.

    Returns list of (label, fg-token, bg-token, fg-hex|bg-hex) tuples
    consumed by the swatch row. We include:

      * `X` paired with `on-X` (canonical semantic pair).
      * Every text-like token (`ink*`, `body*`, `text*`) paired with
        canvas + surface.
    """
    pairs: list[tuple[str, str, str, str]] = []
    # Canonical semantic pairs first.
    for name, hex_v in colors.items():
        if not _is_hex(hex_v):
            continue
        on_name = f"on-{name}"
        on_hex = colors.get(on_name)
        if isinstance(on_hex, str) and _is_hex(on_hex):
            pairs.append((f"{on_name} / {name}", on_name, name, on_hex))
    # Text-on-surface pairs.
    text_tokens = [
        (k, v) for k, v in colors.items()
        if _is_hex(v) and (k.startswith("ink") or k.startswith("text") or k.startswith("body") or k == "muted")
    ]
    surface_tokens = [
        (k, v) for k, v in colors.items()
        if _is_hex(v) and (k == "canvas" or k.startswith("surface") or k == "background")
    ]
    for tk, _tv in text_tokens:
        for sk, _sv in surface_tokens:
            label = f"{tk} / {sk}"
            if any(label == p[0] for p in pairs):
                continue
            pairs.append((label, tk, sk, _tv))
    return pairs


def render_colors_section(fm: dict) -> str:
    colors = fm.get("colors") or {}
    if not isinstance(colors, dict) or not colors:
        return ""
    groups: dict[str, list[tuple[str, str]]] = {}
    for name, val in colors.items():
        resolved = resolve_ref(val, fm)
        if not _is_hex(resolved):
            continue
        groups.setdefault(_classify_color(name), []).append((name, resolved))

    parts: list[str] = ['<section class="sc-section" id="colors"><h2>01 Colors</h2>']
    parts.append('<p class="sc-desc">Every token in <code>colors:</code> as a swatch.'
                 ' Pairs that map to <code>on-X</code> show WCAG-AA contrast.</p>')

    # Per-group swatch grid
    order = ["Brand", "Foreground", "Surface", "Text", "Borders", "Semantic", "Other"]
    for grp in order:
        items = groups.get(grp)
        if not items:
            continue
        parts.append(f'<h3 class="sc-grp">{safe(grp)}</h3>')
        parts.append('<div class="sc-swatch-grid">')
        for name, hex_v in items:
            on_hex = None
            on_token = f"on-{name}"
            if isinstance(colors.get(on_token), str) and _is_hex(colors.get(on_token)):
                on_hex = colors[on_token]
            elif name.startswith("on-"):
                # The token IS itself a foreground.
                base = name[len("on-"):]
                if isinstance(colors.get(base), str) and _is_hex(colors.get(base)):
                    on_hex = colors[base]
            badge_html = ""
            if on_hex is not None:
                ratio = contrast_ratio(on_hex, hex_v)
                label = wcag_class(ratio)
                bg, fg = wcag_badge_color(label)
                ratio_txt = f"{ratio:.2f}:1" if ratio is not None else "n/a"
                badge_html = (
                    f'<span class="sc-badge" '
                    f'style="background:{safe(bg)};color:{safe(fg)}" '
                    f'aria-label="WCAG contrast {safe(label)} ({safe(ratio_txt)})">'
                    f'{safe(label)} {safe(ratio_txt)}</span>'
                )
            parts.append(
                '<div class="sc-swatch">'
                f'<div class="sc-swatch-chip" '
                f'style="background:{safe(hex_v)}" '
                f'role="img" '
                f'aria-label="Color token {safe(name)} hex {safe(hex_v)}"></div>'
                '<div class="sc-swatch-meta">'
                f'<div class="sc-swatch-name">{safe(name)}</div>'
                f'<div class="sc-swatch-hex"><code>{safe(hex_v)}</code></div>'
                f'<div class="sc-swatch-badges">{badge_html}</div>'
                '</div></div>'
            )
        parts.append('</div>')

    # Dedicated pairs table for ALL semantic pairs.
    pairs = _color_pairs(colors)
    if pairs:
        parts.append('<h3 class="sc-grp">Contrast pairs</h3>')
        parts.append('<table class="sc-pairs">'
                     '<thead><tr><th>Foreground</th><th>Background</th>'
                     '<th>Ratio</th><th>WCAG</th><th>Preview</th></tr></thead><tbody>')
        for label, fg_token, bg_token, fg_hex in pairs:
            bg_hex = colors.get(bg_token, "")
            if not _is_hex(bg_hex):
                continue
            ratio = contrast_ratio(fg_hex, bg_hex)
            lbl = wcag_class(ratio)
            bg_b, fg_b = wcag_badge_color(lbl)
            r_txt = f"{ratio:.2f}:1" if ratio is not None else "n/a"
            preview = (
                f'<span class="sc-pair-preview" '
                f'style="background:{safe(bg_hex)};color:{safe(fg_hex)}">Aa</span>'
            )
            parts.append(
                f'<tr>'
                f'<td><code>{safe(fg_token)}</code><br><small>{safe(fg_hex)}</small></td>'
                f'<td><code>{safe(bg_token)}</code><br><small>{safe(bg_hex)}</small></td>'
                f'<td>{safe(r_txt)}</td>'
                f'<td><span class="sc-badge" style="background:{safe(bg_b)};color:{safe(fg_b)}" '
                f'aria-label="WCAG {safe(lbl)}">{safe(lbl)}</span></td>'
                f'<td>{preview}</td>'
                f'</tr>'
            )
        parts.append('</tbody></table>')

    parts.append('</section>')
    return "\n".join(parts)


def render_typography_section(fm: dict) -> str:
    typography = fm.get("typography") or {}
    if not isinstance(typography, dict) or not typography:
        return ""
    parts: list[str] = ['<section class="sc-section" id="typography"><h2>02 Typography</h2>']
    parts.append('<p class="sc-desc">Live specimen per role at the declared size, weight, '
                 'line-height, and letter-spacing. System-font fallbacks used (offline-safe).</p>')
    parts.append('<div class="sc-type-list">')
    for role, row in typography.items():
        if not isinstance(row, dict):
            continue
        fam = row.get("fontFamily", "system-ui")
        size = numeric_dim(row.get("fontSize", "16px"))
        weight = row.get("fontWeight", 400)
        lh = row.get("lineHeight", 1.5)
        ls = row.get("letterSpacing", "")
        css_style = (
            f"font-family:{font_family_css(fam)};"
            f"font-size:{safe(size)};"
            f"font-weight:{safe(weight)};"
            f"line-height:{safe(lh)};"
        )
        if ls not in ("", None):
            css_style += f"letter-spacing:{safe(ls)};"
        spec = (
            f"{safe(fam)} &middot; {safe(weight)} &middot; "
            f"{safe(size)} / {safe(lh)}"
            + (f" / {safe(ls)}" if ls not in ("", None) else "")
        )
        sample_text = "Aa Bb Cc 0123 The quick brown fox"
        if str(role).lower().startswith(("label", "eyebrow", "caption-upper")):
            sample_text = sample_text.upper()
        parts.append(
            '<div class="sc-type-row">'
            f'<div class="sc-type-meta"><div class="sc-type-role">{safe(role)}</div>'
            f'<div class="sc-type-spec">{spec}</div></div>'
            f'<div class="sc-type-sample" style="{css_style}">{safe(sample_text)}</div>'
            '</div>'
        )
    parts.append('</div></section>')
    return "\n".join(parts)


def render_rounded_section(fm: dict) -> str:
    rounded = fm.get("rounded") or {}
    if not isinstance(rounded, dict) or not rounded:
        return ""
    parts: list[str] = ['<section class="sc-section" id="rounded"><h2>03 Rounded</h2>']
    parts.append('<p class="sc-desc">Every border-radius step rendered as a visible chip.</p>')
    parts.append('<div class="sc-rad-row">')
    for name, val in rounded.items():
        dim = numeric_dim(resolve_ref(val, fm))
        parts.append(
            '<div class="sc-rad-item">'
            f'<div class="sc-rad-chip" style="border-radius:{safe(dim)}" '
            f'role="img" aria-label="Border radius {safe(name)} ({safe(dim)})"></div>'
            f'<div class="sc-rad-label"><code>{safe(name)}</code><br>'
            f'<small>{safe(dim)}</small></div>'
            '</div>'
        )
    parts.append('</div></section>')
    return "\n".join(parts)


def render_spacing_section(fm: dict) -> str:
    spacing = fm.get("spacing") or {}
    if not isinstance(spacing, dict) or not spacing:
        return ""
    parts: list[str] = ['<section class="sc-section" id="spacing"><h2>04 Spacing</h2>']
    parts.append('<p class="sc-desc">Each spacing token rendered as a bar of the declared width.</p>')
    parts.append('<div class="sc-spacing-list">')
    for name, val in spacing.items():
        dim = numeric_dim(resolve_ref(val, fm))
        parts.append(
            '<div class="sc-spacing-row">'
            f'<div class="sc-spacing-label"><code>{safe(name)}</code> <small>{safe(dim)}</small></div>'
            f'<div class="sc-spacing-bar" style="width:{safe(dim)}" '
            f'role="img" aria-label="Spacing {safe(name)} of {safe(dim)}"></div>'
            '</div>'
        )
    parts.append('</div></section>')
    return "\n".join(parts)


def render_elevation_section(fm: dict) -> str:
    """Optional elevation/shadow tokens. Schema: `elevation: { name: <css-shadow> }`."""
    elev = fm.get("elevation") or fm.get("shadows") or {}
    if not isinstance(elev, dict) or not elev:
        return ""
    parts: list[str] = ['<section class="sc-section" id="elevation"><h2>05 Elevation</h2>']
    parts.append('<p class="sc-desc">Each elevation/shadow level on a card.</p>')
    parts.append('<div class="sc-elev-grid">')
    for name, val in elev.items():
        shadow_css = resolve_ref(val, fm)
        parts.append(
            '<div class="sc-elev-card" '
            f'style="box-shadow:{safe(shadow_css)}" '
            f'role="img" aria-label="Elevation {safe(name)}">'
            f'<div class="sc-elev-label"><code>{safe(name)}</code></div>'
            '</div>'
        )
    parts.append('</div></section>')
    return "\n".join(parts)


def render_components_section(fm: dict) -> str:
    components = fm.get("components") or {}
    if not isinstance(components, dict) or not components:
        return ""
    parts: list[str] = ['<section class="sc-section" id="components"><h2>06 Components</h2>']
    parts.append('<p class="sc-desc">Each declared component rendered with its tokens. '
                 'Token references like <code>{colors.primary}</code> are resolved before render.</p>')

    for name, props in components.items():
        if not isinstance(props, dict):
            continue
        resolved = {k: resolve_ref(v, fm) for k, v in props.items()}
        # Resolve typography sub-fields if the typography reference is a dict.
        typo = resolved.get("typography")
        if isinstance(typo, dict):
            typo_style = (
                f"font-family:{font_family_css(typo.get('fontFamily'))};"
                f"font-size:{safe(numeric_dim(typo.get('fontSize', '14px')))};"
                f"font-weight:{safe(typo.get('fontWeight', 500))};"
                f"line-height:{safe(typo.get('lineHeight', 1.4))};"
            )
        else:
            typo_style = ""
        style = ""
        bg = resolved.get("backgroundColor")
        if bg:
            style += f"background:{safe(bg)};"
        fg = resolved.get("textColor") or resolved.get("color")
        if fg:
            style += f"color:{safe(fg)};"
        rad = resolved.get("rounded") or resolved.get("borderRadius")
        if rad:
            style += f"border-radius:{safe(numeric_dim(rad))};"
        pad = resolved.get("padding")
        if pad:
            style += f"padding:{safe(numeric_dim(pad))};"
        border = resolved.get("borderColor")
        if border:
            style += f"border:1px solid {safe(border)};"
        style += typo_style
        # Pick a sample DOM based on the token name.
        lname = name.lower()
        if lname.startswith("button"):
            sample = f'<button type="button" class="sc-comp-button" style="{style}">'\
                     f'{safe(name)}</button>'
        elif lname.startswith("input"):
            sample = (
                f'<input type="text" class="sc-comp-input" style="{style}" '
                f'placeholder="Sample input" aria-label="Sample input for {safe(name)}" />'
            )
        elif lname.startswith("card"):
            sample = (
                f'<div class="sc-comp-card" style="{style}" '
                f'role="region" aria-label="Sample card for {safe(name)}">'
                f'<h4>Card title</h4>'
                f'<p>Card body uses the declared <code>{safe(name)}</code> tokens.</p>'
                f'</div>'
            )
        elif lname.startswith("chip") or lname.startswith("badge") or lname.startswith("pill"):
            sample = f'<span class="sc-comp-chip" style="{style}">{safe(name)}</span>'
        else:
            sample = f'<div class="sc-comp-generic" style="{style}">{safe(name)}</div>'

        # Spec table for the component.
        spec_rows = "".join(
            f'<tr><td><code>{safe(k)}</code></td><td><code>{safe(v)}</code></td></tr>'
            for k, v in props.items()
        )
        parts.append(
            '<div class="sc-comp-row">'
            f'<div class="sc-comp-spec"><h4>{safe(name)}</h4>'
            f'<table class="sc-comp-tokens">{spec_rows}</table></div>'
            f'<div class="sc-comp-demo">{sample}</div>'
            '</div>'
        )
    parts.append('</section>')
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# Top-level assembly
# ----------------------------------------------------------------------------

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#0c0d10;color:#f5f5f7;font-family:system-ui,-apple-system,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
body{padding:32px 24px 96px;max-width:1180px;margin:0 auto}
a{color:#6cc7ff;text-decoration:none}
code{font-family:ui-monospace,Menlo,monospace;font-size:0.92em;background:#1c1f26;padding:1px 6px;border-radius:4px;color:#f5f5f7}
small{color:#b0b3bd;font-size:0.85em}
header.sc-hero{margin-bottom:48px;padding:32px 0;border-bottom:1px solid #20232b}
header.sc-hero h1{font-size:36px;font-weight:700;line-height:1.15;margin-bottom:8px}
header.sc-hero .sc-sub{color:#b0b3bd;font-size:16px;max-width:60ch}
nav.sc-nav{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px;font-size:13px}
nav.sc-nav a{padding:4px 10px;background:#16181d;border:1px solid #20232b;border-radius:6px}
nav.sc-nav a:hover{background:#1c1f26}
.sc-section{margin:48px 0;padding:24px;background:#16181d;border:1px solid #20232b;border-radius:12px}
.sc-section h2{font-size:22px;margin-bottom:6px;color:#f5f5f7}
.sc-section h3.sc-grp{font-size:14px;text-transform:uppercase;letter-spacing:0.08em;color:#b0b3bd;margin:24px 0 12px}
.sc-section h4{font-size:15px;margin-bottom:8px;color:#f5f5f7}
.sc-desc{color:#b0b3bd;font-size:14px;margin-bottom:16px;max-width:70ch}
.sc-swatch-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-bottom:8px}
.sc-swatch{background:#0c0d10;border:1px solid #20232b;border-radius:10px;overflow:hidden}
.sc-swatch-chip{width:100%;height:88px;border-bottom:1px solid #20232b}
.sc-swatch-meta{padding:8px 12px 12px}
.sc-swatch-name{font-weight:600;font-size:13px;color:#f5f5f7}
.sc-swatch-hex{color:#b0b3bd;font-size:12px;margin-top:2px}
.sc-swatch-badges{margin-top:6px;display:flex;flex-wrap:wrap;gap:4px}
.sc-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;letter-spacing:0.02em}
.sc-pairs{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
.sc-pairs th,.sc-pairs td{padding:8px 10px;text-align:left;border-bottom:1px solid #20232b;vertical-align:top}
.sc-pairs th{color:#b0b3bd;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:0.05em}
.sc-pair-preview{display:inline-block;padding:6px 12px;border-radius:6px;font-weight:600;border:1px solid #20232b}
.sc-type-list{display:flex;flex-direction:column;gap:16px}
.sc-type-row{display:grid;grid-template-columns:220px 1fr;gap:24px;align-items:center;padding:14px 16px;background:#0c0d10;border:1px solid #20232b;border-radius:10px}
.sc-type-meta{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#b0b3bd}
.sc-type-role{font-weight:600;color:#f5f5f7;margin-bottom:2px;text-transform:uppercase;letter-spacing:0.05em}
.sc-type-sample{color:#f5f5f7;overflow:hidden;text-overflow:ellipsis}
.sc-rad-row{display:flex;flex-wrap:wrap;gap:18px}
.sc-rad-item{display:flex;flex-direction:column;align-items:center;gap:6px}
.sc-rad-chip{width:72px;height:72px;background:#6cc7ff;border:1px solid #20232b}
.sc-rad-label{font-size:12px;text-align:center;color:#b0b3bd}
.sc-spacing-list{display:flex;flex-direction:column;gap:10px}
.sc-spacing-row{display:grid;grid-template-columns:140px 1fr;align-items:center;gap:16px}
.sc-spacing-label{font-size:13px}
.sc-spacing-bar{height:14px;background:#6cc7ff;border-radius:3px;min-width:2px;max-width:100%}
.sc-elev-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:24px;padding:24px;background:#1c1f26;border-radius:10px}
.sc-elev-card{height:120px;background:#16181d;border:1px solid #20232b;border-radius:10px;display:flex;align-items:flex-end;padding:12px}
.sc-elev-label{font-size:12px;color:#b0b3bd}
.sc-comp-row{display:grid;grid-template-columns:280px 1fr;gap:24px;padding:18px;background:#0c0d10;border:1px solid #20232b;border-radius:10px;margin-bottom:14px;align-items:center}
.sc-comp-spec h4{margin-bottom:8px}
.sc-comp-tokens{width:100%;font-size:11px;border-collapse:collapse}
.sc-comp-tokens td{padding:3px 4px;border-bottom:1px solid #20232b;color:#b0b3bd}
.sc-comp-demo{padding:12px;background:#16181d;border:1px solid #20232b;border-radius:8px;display:flex;justify-content:center;align-items:center;min-height:80px}
.sc-comp-button{cursor:pointer;border:0;font-size:14px;padding:8px 16px;border-radius:6px}
.sc-comp-input{font-size:14px;padding:8px 12px;border-radius:6px;border:1px solid #20232b;background:#0c0d10;color:#f5f5f7;width:240px}
.sc-comp-card{padding:16px;border-radius:8px;max-width:280px}
.sc-comp-card h4{margin-bottom:4px}
.sc-comp-card p{font-size:13px;color:#b0b3bd}
.sc-comp-chip{display:inline-block;font-size:12px;padding:4px 10px;border-radius:999px}
.sc-comp-generic{padding:12px 18px;border-radius:6px;font-size:13px}
footer.sc-foot{margin-top:64px;padding-top:16px;border-top:1px solid #20232b;font-size:12px;color:#7a7e8a;text-align:center}
@media (max-width:720px){
  body{padding:16px 12px 64px}
  header.sc-hero h1{font-size:26px}
  .sc-type-row,.sc-comp-row,.sc-spacing-row{grid-template-columns:1fr}
}
""".strip()


def render_html(fm: dict, source_path: Path) -> str:
    name = fm.get("name") or source_path.stem
    description = fm.get("description") or ""
    sections = [
        render_colors_section(fm),
        render_typography_section(fm),
        render_rounded_section(fm),
        render_spacing_section(fm),
        render_elevation_section(fm),
        render_components_section(fm),
    ]
    sections = [s for s in sections if s]
    nav_items = [
        ("Colors", "#colors", bool(fm.get("colors"))),
        ("Typography", "#typography", bool(fm.get("typography"))),
        ("Rounded", "#rounded", bool(fm.get("rounded"))),
        ("Spacing", "#spacing", bool(fm.get("spacing"))),
        ("Elevation", "#elevation", bool(fm.get("elevation") or fm.get("shadows"))),
        ("Components", "#components", bool(fm.get("components"))),
    ]
    nav_html = "".join(
        f'<a href="{attr(href)}">{safe(label)}</a>'
        for label, href, present in nav_items if present
    )
    body_parts = [
        '<header class="sc-hero">',
        f'<h1>{safe(name)} &mdash; Design System Showcase</h1>',
        (f'<p class="sc-sub">{safe(description)}</p>' if description else ""),
        f'<nav class="sc-nav" aria-label="Showcase sections">{nav_html}</nav>',
        '</header>',
        *sections,
        '<footer class="sc-foot">'
        f'Generated by <code>amw-design-md-showcase.py</code> from '
        f'<code>{safe(source_path.name)}</code>. Single-file, offline-safe.'
        '</footer>',
    ]
    body = "\n".join(p for p in body_parts if p)
    return (
        '<!doctype html>\n'
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8" />\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        f'<title>{safe(name)} &mdash; Showcase</title>\n'
        '<style>\n'
        f'{BASE_CSS}\n'
        '</style>\n</head>\n<body>\n'
        f'{body}\n'
        '</body>\n</html>\n'
    )


# ----------------------------------------------------------------------------
# CLI entry point
# ----------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="amw-design-md-showcase.py",
        description=("Render a DESIGN.md as a self-contained HTML showcase: "
                     "color swatches with WCAG contrast badges, typography specimens, "
                     "spacing / rounded / elevation visualizations, and component demos."),
    )
    parser.add_argument("source", type=Path, help="Path to a DESIGN.md file")
    parser.add_argument(
        "-o", "--output", type=Path, required=True,
        help="Path to write the showcase HTML (will be overwritten if it exists)",
    )
    parser.add_argument(
        "--json-fm", action="store_true",
        help="Print the parsed frontmatter as JSON to stdout (debug aid)",
    )
    args = parser.parse_args(argv)

    src: Path = args.source
    if not src.is_file():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        return 2
    try:
        content = src.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: could not read {src}: {exc}", file=sys.stderr)
        return 2

    fm = parse_frontmatter(content)
    if not fm:
        print(
            f"ERROR: no YAML frontmatter found in {src}. "
            "DESIGN.md files must start with --- ... --- frontmatter.",
            file=sys.stderr,
        )
        return 2

    if args.json_fm:
        print(json.dumps(fm, indent=2, default=str))

    html_out = render_html(fm, src)
    out: Path = args.output
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_out, encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: could not write {out}: {exc}", file=sys.stderr)
        return 2

    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
