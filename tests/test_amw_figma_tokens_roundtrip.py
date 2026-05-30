"""Round-trip tests for the Figma Tokens Studio JSON <-> DESIGN.md bridge.

Two bin scripts ship the bridge:
  - bin/amw-figma-tokens-import.py — figma-tokens.json -> DESIGN.md
  - bin/amw-figma-tokens-export.py — DESIGN.md -> figma-tokens.json

The round-trip contract is lossy-but-equivalent for the canonical token surface:
color hex (case-folded), font family, font size (px), font weight, line height,
spacing px, radius px. Shadow, gradient, composite-border tokens are dropped on
import and not reconstructed on export — those are documented in the bridge
reference, NOT asserted here.

All assertions are over real subprocess invocations of the bin scripts (per the
project's "no-mock" rule) against fixture files this test writes into a tmp dir.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PLUGIN_ROOT / "bin"
IMPORT_SCRIPT = BIN_DIR / "amw-figma-tokens-import.py"
EXPORT_SCRIPT = BIN_DIR / "amw-figma-tokens-export.py"


# A representative Tokens Studio JSON fixture covering every supported type.
# Keys are deliberately mixed-case / dotted to exercise the path-classifier.
FIXTURE_CLASSIC: dict = {
    "global": {
        "colors": {
            "primary": {"value": "#2563EB", "type": "color"},
            "secondary": {"value": "#F59E0B", "type": "color"},
            "neutral": {"value": "#0B0D12", "type": "color"},
            "surface": {"value": "#FFFFFF", "type": "color"},
            "on-surface": {"value": "#111827", "type": "color"},
            "error": {"value": "#EF4444", "type": "color"},
        },
        "typography": {
            "headline-lg": {
                "value": {
                    "fontFamily": "Inter",
                    "fontSize": "32px",
                    "fontWeight": 700,
                    "lineHeight": 1.2,
                    "letterSpacing": "-0.01em",
                },
                "type": "typography",
            },
            "body-md": {
                "value": {
                    "fontFamily": "Inter",
                    "fontSize": "16px",
                    "fontWeight": 400,
                    "lineHeight": 1.5,
                    "letterSpacing": "0em",
                },
                "type": "typography",
            },
            "label-md": {
                "value": {
                    "fontFamily": "Inter",
                    "fontSize": "14px",
                    "fontWeight": 500,
                    "lineHeight": 1.4,
                    "letterSpacing": "0.02em",
                },
                "type": "typography",
            },
        },
        "spacing": {
            "xs": {"value": "4px", "type": "spacing"},
            "sm": {"value": "8px", "type": "spacing"},
            "md": {"value": "16px", "type": "spacing"},
            "lg": {"value": "24px", "type": "spacing"},
            "xl": {"value": "48px", "type": "spacing"},
        },
        "borderRadius": {
            "none": {"value": "0px", "type": "borderRadius"},
            "sm": {"value": "4px", "type": "borderRadius"},
            "md": {"value": "8px", "type": "borderRadius"},
            "lg": {"value": "16px", "type": "borderRadius"},
            "full": {"value": "9999px", "type": "borderRadius"},
        },
    },
    "$themes": [],
    "$metadata": {"tokenSetOrder": ["global"]},
}


def _run(script: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


# ---------------------------------------------------------------------------
# IMPORT side: figma-tokens.json -> DESIGN.md
# ---------------------------------------------------------------------------

def test_import_writes_design_md_with_expected_frontmatter(tmp_path: Path) -> None:
    tokens_path = tmp_path / "figma-tokens.json"
    tokens_path.write_text(json.dumps(FIXTURE_CLASSIC), encoding="utf-8")
    md_path = tmp_path / "DESIGN.md"

    result = _run(IMPORT_SCRIPT, [str(tokens_path), "-o", str(md_path)])
    assert result.returncode == 0, f"import failed: {result.stderr}"
    assert md_path.is_file(), "DESIGN.md was not created"

    text = md_path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "DESIGN.md must start with YAML frontmatter"

    # Frontmatter must contain canonical Variant 1 sections
    assert "version: alpha" in text
    assert "colors:" in text
    assert "typography:" in text
    assert "rounded:" in text
    assert "spacing:" in text

    # Canonical color slots present
    for slot in ("primary", "secondary", "neutral", "surface", "on-surface", "error"):
        assert slot in text, f"missing color slot {slot} in DESIGN.md"

    # Color hex must be preserved
    assert "#2563EB" in text
    assert "#F59E0B" in text


def test_import_handles_dtcg_dollar_key_form(tmp_path: Path) -> None:
    """The importer must accept the DTCG ($value/$type) form as well."""
    dtcg_fixture = {
        "global": {
            "colors": {
                "primary": {"$value": "#123456", "$type": "color"},
            },
            "spacing": {
                "md": {"$value": "16px", "$type": "spacing"},
            },
        }
    }
    tokens_path = tmp_path / "dtcg.json"
    tokens_path.write_text(json.dumps(dtcg_fixture), encoding="utf-8")
    md_path = tmp_path / "DESIGN.md"

    result = _run(IMPORT_SCRIPT, [str(tokens_path), "-o", str(md_path)])
    assert result.returncode == 0, f"dtcg import failed: {result.stderr}"

    text = md_path.read_text(encoding="utf-8")
    assert "#123456" in text
    assert "primary:" in text


def test_import_short_hex_expands_to_six_digit_form(tmp_path: Path) -> None:
    fixture = {
        "global": {
            "colors": {
                "primary": {"value": "#abc", "type": "color"},
            }
        }
    }
    tokens_path = tmp_path / "short.json"
    tokens_path.write_text(json.dumps(fixture), encoding="utf-8")
    md_path = tmp_path / "DESIGN.md"
    assert _run(IMPORT_SCRIPT, [str(tokens_path), "-o", str(md_path)]).returncode == 0
    assert "#AABBCC" in md_path.read_text(encoding="utf-8")


def test_import_rgba_string_converted_to_hex_alpha(tmp_path: Path) -> None:
    fixture = {
        "global": {
            "colors": {
                "primary": {"value": "rgba(255, 0, 0, 0.5)", "type": "color"},
            }
        }
    }
    tokens_path = tmp_path / "rgba.json"
    tokens_path.write_text(json.dumps(fixture), encoding="utf-8")
    md_path = tmp_path / "DESIGN.md"
    assert _run(IMPORT_SCRIPT, [str(tokens_path), "-o", str(md_path)]).returncode == 0
    text = md_path.read_text(encoding="utf-8")
    # Half-alpha rounds to 0x80
    assert "#FF000080" in text


# ---------------------------------------------------------------------------
# EXPORT side: DESIGN.md -> figma-tokens.json
# ---------------------------------------------------------------------------

DESIGN_MD_FIXTURE = """---
version: alpha
name: Acme
colors:
  primary: "#2563EB"
  secondary: "#F59E0B"
  neutral: "#0B0D12"
  surface: "#FFFFFF"
  on-surface: "#111827"
  error: "#EF4444"
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0em
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  base: 16px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
---

# Acme Design System

A test fixture.

## Overview
Test.

## Colors
- Primary
## Typography
- Body
## Layout
- Grid
## Elevation & Depth
- Flat
## Shapes
- Rounded
## Components
- Buttons
## Do's and Don'ts
**Do:**
- Do
**Don't:**
- Don't
"""


def test_export_writes_classic_tokens_studio_shape(tmp_path: Path) -> None:
    md_path = tmp_path / "DESIGN.md"
    md_path.write_text(DESIGN_MD_FIXTURE, encoding="utf-8")
    tokens_path = tmp_path / "out.json"

    result = _run(EXPORT_SCRIPT, [str(md_path), "-o", str(tokens_path)])
    assert result.returncode == 0, f"export failed: {result.stderr}"

    doc = json.loads(tokens_path.read_text(encoding="utf-8"))
    assert "global" in doc
    assert "$themes" in doc
    assert "$metadata" in doc
    assert doc["$metadata"]["tokenSetOrder"] == ["global"]

    g = doc["global"]
    assert "colors" in g and "primary" in g["colors"]
    # Classic shape uses bare `value`/`type` keys
    assert g["colors"]["primary"]["type"] == "color"
    assert g["colors"]["primary"]["value"] == "#2563EB"
    # Typography composite
    assert g["typography"]["body-md"]["type"] == "typography"
    assert g["typography"]["body-md"]["value"]["fontFamily"] == "Inter"
    # Border radius uses Tokens Studio name (not `rounded`)
    assert "borderRadius" in g
    assert g["borderRadius"]["md"]["value"] == "8px"


def test_export_dtcg_flag_uses_dollar_keys(tmp_path: Path) -> None:
    md_path = tmp_path / "DESIGN.md"
    md_path.write_text(DESIGN_MD_FIXTURE, encoding="utf-8")
    tokens_path = tmp_path / "out.json"
    assert _run(EXPORT_SCRIPT, [str(md_path), "-o", str(tokens_path), "--dtcg"]).returncode == 0

    doc = json.loads(tokens_path.read_text(encoding="utf-8"))
    assert doc["global"]["colors"]["primary"]["$type"] == "color"
    assert doc["global"]["colors"]["primary"]["$value"] == "#2563EB"


# ---------------------------------------------------------------------------
# ROUND-TRIP: import -> export -> import (the contract)
# ---------------------------------------------------------------------------

def test_roundtrip_preserves_colors(tmp_path: Path) -> None:
    """A Tokens Studio file -> DESIGN.md -> Tokens Studio file -> DESIGN.md
    must preserve every canonical color slot's hex value."""
    src = tmp_path / "src.json"
    src.write_text(json.dumps(FIXTURE_CLASSIC), encoding="utf-8")
    md1 = tmp_path / "DESIGN-1.md"
    tokens2 = tmp_path / "tokens-2.json"
    md2 = tmp_path / "DESIGN-2.md"

    assert _run(IMPORT_SCRIPT, [str(src), "-o", str(md1)]).returncode == 0
    assert _run(EXPORT_SCRIPT, [str(md1), "-o", str(tokens2)]).returncode == 0
    assert _run(IMPORT_SCRIPT, [str(tokens2), "-o", str(md2)]).returncode == 0

    text1 = md1.read_text(encoding="utf-8")
    text2 = md2.read_text(encoding="utf-8")

    # Every canonical color hex from the original survives both legs
    for hex_ in ("#2563EB", "#F59E0B", "#0B0D12", "#FFFFFF", "#111827", "#EF4444"):
        assert hex_ in text1, f"{hex_} missing after first import"
        assert hex_ in text2, f"{hex_} missing after second import"


def test_roundtrip_preserves_spacing_and_radius(tmp_path: Path) -> None:
    src = tmp_path / "src.json"
    src.write_text(json.dumps(FIXTURE_CLASSIC), encoding="utf-8")
    md1 = tmp_path / "DESIGN-1.md"
    tokens2 = tmp_path / "tokens-2.json"

    assert _run(IMPORT_SCRIPT, [str(src), "-o", str(md1)]).returncode == 0
    assert _run(EXPORT_SCRIPT, [str(md1), "-o", str(tokens2)]).returncode == 0

    doc = json.loads(tokens2.read_text(encoding="utf-8"))
    g = doc["global"]
    # Every spacing slot from FIXTURE_CLASSIC survives
    for slot, expected in (("xs", "4px"), ("sm", "8px"), ("md", "16px"), ("lg", "24px"), ("xl", "48px")):
        assert g["spacing"][slot]["value"] == expected, f"spacing.{slot} drifted"
    # Border radius — note DESIGN.md uses `rounded`, Tokens Studio uses `borderRadius`
    for slot, expected in (("none", "0px"), ("sm", "4px"), ("md", "8px"), ("lg", "16px"), ("full", "9999px")):
        assert g["borderRadius"][slot]["value"] == expected, f"borderRadius.{slot} drifted"


def test_roundtrip_preserves_typography_composite(tmp_path: Path) -> None:
    src = tmp_path / "src.json"
    src.write_text(json.dumps(FIXTURE_CLASSIC), encoding="utf-8")
    md1 = tmp_path / "DESIGN-1.md"
    tokens2 = tmp_path / "tokens-2.json"

    assert _run(IMPORT_SCRIPT, [str(src), "-o", str(md1)]).returncode == 0
    assert _run(EXPORT_SCRIPT, [str(md1), "-o", str(tokens2)]).returncode == 0

    doc = json.loads(tokens2.read_text(encoding="utf-8"))
    body = doc["global"]["typography"]["body-md"]["value"]
    assert body["fontFamily"] == "Inter"
    assert body["fontSize"] == "16px"
    assert body["fontWeight"] == 400


# ---------------------------------------------------------------------------
# Invocation errors
# ---------------------------------------------------------------------------

def test_import_missing_file_errors(tmp_path: Path) -> None:
    result = _run(IMPORT_SCRIPT, [str(tmp_path / "nope.json"), "-o", str(tmp_path / "out.md")])
    assert result.returncode == 2
    assert "not found" in result.stderr.lower()


def test_export_missing_file_errors(tmp_path: Path) -> None:
    result = _run(EXPORT_SCRIPT, [str(tmp_path / "nope.md"), "-o", str(tmp_path / "out.json")])
    assert result.returncode == 2


def test_import_invalid_json_errors(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not-json}", encoding="utf-8")
    result = _run(IMPORT_SCRIPT, [str(bad), "-o", str(tmp_path / "out.md")])
    assert result.returncode == 1


def test_export_missing_frontmatter_errors(tmp_path: Path) -> None:
    bad = tmp_path / "no-frontmatter.md"
    bad.write_text("# Just a title with no YAML\n", encoding="utf-8")
    result = _run(EXPORT_SCRIPT, [str(bad), "-o", str(tmp_path / "out.json")])
    assert result.returncode == 1


# ---------------------------------------------------------------------------
# Multi-set selection
# ---------------------------------------------------------------------------

def test_import_multi_set_merges_all_by_default(tmp_path: Path) -> None:
    multi = {
        "light": {
            "colors": {"primary": {"value": "#FFFFFF", "type": "color"}},
        },
        "dark": {
            # `dark` set overrides `light` for the primary color
            "colors": {"primary": {"value": "#000000", "type": "color"}},
        },
        "$themes": [],
        "$metadata": {"tokenSetOrder": ["light", "dark"]},
    }
    src = tmp_path / "multi.json"
    src.write_text(json.dumps(multi), encoding="utf-8")
    md_path = tmp_path / "DESIGN.md"
    assert _run(IMPORT_SCRIPT, [str(src), "-o", str(md_path)]).returncode == 0
    text = md_path.read_text(encoding="utf-8")
    # Last set wins → #000000 is the merged primary
    assert "#000000" in text
    assert "#FFFFFF" not in text


def test_import_multi_set_with_explicit_set_selection(tmp_path: Path) -> None:
    multi = {
        "light": {"colors": {"primary": {"value": "#FFFFFF", "type": "color"}}},
        "dark": {"colors": {"primary": {"value": "#000000", "type": "color"}}},
    }
    src = tmp_path / "multi.json"
    src.write_text(json.dumps(multi), encoding="utf-8")
    md_path = tmp_path / "DESIGN.md"
    assert _run(IMPORT_SCRIPT, [str(src), "-o", str(md_path), "--set", "light"]).returncode == 0
    text = md_path.read_text(encoding="utf-8")
    assert "#FFFFFF" in text
    assert "#000000" not in text


# ---------------------------------------------------------------------------
# Sanity: scripts byte-compile and respond to --help
# ---------------------------------------------------------------------------

def test_scripts_respond_to_help() -> None:
    for script in (IMPORT_SCRIPT, EXPORT_SCRIPT):
        result = _run(script, ["--help"])
        assert result.returncode == 0, f"{script.name} --help failed: {result.stderr}"
        assert "usage" in result.stdout.lower()
