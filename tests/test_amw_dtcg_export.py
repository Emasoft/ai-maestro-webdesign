"""Unit + integration tests for bin/amw-dtcg-export.py.

The script must:

1. Convert a DESIGN.md (Variant 1 YAML frontmatter) into canonical DTCG
   JSON: every leaf has $type + $value, group-level $type is set when
   the group is monomorphic, aliases stay verbatim.
2. With --harmonize, rewrite a Figma-Tokens-style nested-group JSON
   (using bare `value`/`type`/`description` keys) into canonical DTCG
   ($-prefixed keys), inferring missing $type from value shape.
3. Reject DTCG that violates the contract (every leaf needs $type +
   $value, every alias must resolve).

No mocks — every assertion drives the real CLI via subprocess, OR
imports the module directly to exercise the pure-Python core.

Real invocations only (per project test rules).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "bin" / "amw-dtcg-export.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"
TIMEOUT = 30


# ---------------------------------------------------------------------------
# Import the module (bin scripts use hyphens — can't `import` natively).
# Loading via importlib lets us test the pure-Python helpers directly,
# without a subprocess. Subprocess tests below cover the CLI contract.
# ---------------------------------------------------------------------------

def _load_script_module():
    spec = importlib.util.spec_from_file_location("amw_dtcg_export", SCRIPT)
    assert spec is not None and spec.loader is not None, "could not locate amw-dtcg-export.py"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dtcg_mod = _load_script_module()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

CANONICAL_DESIGN_MD = """---
version: alpha
name: Test System
description: Smoke fixture for DTCG export

colors:
  primary: "#1a1c1e"
  secondary: "#6c7278"
  surface: "#ffffff"

typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6

rounded:
  none: 0px
  md: 8px
  full: 9999px

spacing:
  xs: 4px
  sm: 8px
  md: 16px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: 12px
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: 24px
---

# Test System Design

Sample body — not parsed by the emitter.
"""


@pytest.fixture
def design_md_file(tmp_path: Path) -> Path:
    p = tmp_path / "DESIGN.md"
    p.write_text(CANONICAL_DESIGN_MD, encoding="utf-8")
    return p


@pytest.fixture
def figma_fixture() -> Path:
    f = FIXTURES / "figma-tokens-nested.json"
    assert f.is_file(), f"missing fixture {f}"
    return f


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------

def _run(args: list[str], **kw) -> subprocess.CompletedProcess[str]:
    """Run the script with --output to stdout (or with -o if given)."""
    cmd = [sys.executable, str(SCRIPT), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        **kw,
    )


# ---------------------------------------------------------------------------
# Group 1: pure-Python core (no subprocess)
# ---------------------------------------------------------------------------

class TestDtcgConversionCore:
    """Direct unit tests against the pure-Python helpers."""

    def test_design_md_to_dtcg_emits_dtcg_keys_on_every_color_leaf(self):
        fm = {
            "colors": {"primary": "#1a1c1e", "secondary": "#6c7278"},
        }
        out = dtcg_mod.design_md_to_dtcg(fm)
        # Group-level $type set (inheritance optimization).
        assert out["colors"]["$type"] == "color"
        # Every leaf has $value; $type is inherited so omitted on leaf.
        assert out["colors"]["primary"] == {"$value": "#1a1c1e"}
        assert out["colors"]["secondary"] == {"$value": "#6c7278"}

    def test_typography_group_emits_composite_value_per_leaf(self):
        fm = {
            "typography": {
                "headline-lg": {
                    "fontFamily": "Inter",
                    "fontSize": "36px",
                    "fontWeight": 600,
                },
            },
        }
        out = dtcg_mod.design_md_to_dtcg(fm)
        assert out["typography"]["$type"] == "typography"
        leaf = out["typography"]["headline-lg"]
        assert leaf["$type"] == "typography"
        assert leaf["$value"]["fontFamily"] == "Inter"
        assert leaf["$value"]["fontSize"] == "36px"
        assert leaf["$value"]["fontWeight"] == 600

    def test_components_emit_per_property_type_and_preserve_aliases(self):
        fm = {
            "colors": {"primary": "#1a1c1e", "surface": "#ffffff"},
            "rounded": {"md": "8px"},
            "components": {
                "button-primary": {
                    "backgroundColor": "{colors.primary}",
                    "rounded": "{rounded.md}",
                    "padding": "12px",
                },
            },
        }
        out = dtcg_mod.design_md_to_dtcg(fm)
        btn = out["components"]["button-primary"]
        # Each property is a leaf — components is not monomorphic, so
        # $type is set per leaf (not inherited from the components group).
        assert btn["backgroundColor"]["$type"] == "color"
        assert btn["backgroundColor"]["$value"] == "{colors.primary}"  # alias preserved
        assert btn["rounded"]["$type"] == "dimension"
        assert btn["rounded"]["$value"] == "{rounded.md}"
        assert btn["padding"]["$type"] == "dimension"
        assert btn["padding"]["$value"] == "12px"

    def test_alias_path_extraction(self):
        assert dtcg_mod._alias_path("{a.b.c}") == "a.b.c"
        assert dtcg_mod._alias_path("{x}") == "x"
        assert dtcg_mod._alias_path("not-an-alias") is None
        assert dtcg_mod._alias_path("{a.b} trailing") is None

    def test_harmonize_renames_bare_keys_to_dollar_prefixed(self):
        figma = {
            "color": {
                "brand": {
                    "primary": {"value": "#abcdef", "type": "color", "description": "x"},
                },
            },
        }
        out = dtcg_mod.harmonize(figma)
        leaf = out["color"]["brand"]["primary"]
        assert leaf["$value"] == "#abcdef"
        assert leaf["$type"] == "color"
        assert leaf["$description"] == "x"
        # Bare keys must NOT remain.
        for forbidden in ("value", "type", "description"):
            assert forbidden not in leaf, f"bare '{forbidden}' leaked into DTCG output"

    def test_harmonize_is_idempotent_on_already_dtcg_tree(self):
        already_dtcg = {
            "color": {
                "primary": {"$value": "#abcdef", "$type": "color"},
            },
        }
        once = dtcg_mod.harmonize(already_dtcg)
        twice = dtcg_mod.harmonize(once)
        assert once == twice == already_dtcg

    def test_harmonize_preserves_nesting_depth(self):
        figma = {
            "a": {"b": {"c": {"d": {"value": "#000000", "type": "color"}}}},
        }
        out = dtcg_mod.harmonize(figma)
        assert out["a"]["b"]["c"]["d"]["$value"] == "#000000"
        assert out["a"]["b"]["c"]["d"]["$type"] == "color"

    def test_harmonize_infers_type_from_value_shape_when_missing(self):
        figma = {
            "guess-color": {"value": "#abcdef"},
            "guess-dim": {"value": "12px"},
            "guess-number": {"value": 0.5},
        }
        out = dtcg_mod.harmonize(figma)
        assert out["guess-color"]["$type"] == "color"
        assert out["guess-dim"]["$type"] == "dimension"
        assert out["guess-number"]["$type"] == "number"


# ---------------------------------------------------------------------------
# Group 2: DTCG validation contract
# ---------------------------------------------------------------------------

class TestDtcgValidation:
    """Every leaf must have $type + $value; every alias must resolve."""

    def test_validate_ok_on_well_formed_tree(self):
        tree = {
            "colors": {
                "$type": "color",
                "primary": {"$value": "#1a1c1e"},
                "ref": {"$value": "{colors.primary}"},
            },
        }
        errors = dtcg_mod.validate_dtcg(tree)
        assert errors == [], f"unexpected errors: {errors}"

    def test_validate_flags_leaf_missing_type(self):
        tree = {
            "colors": {  # no $type at group level
                "primary": {"$value": "#1a1c1e"},  # no $type at leaf
            },
        }
        errors = dtcg_mod.validate_dtcg(tree)
        assert any("missing $type" in e for e in errors), errors

    def test_validate_flags_unknown_type(self):
        tree = {
            "weird": {"$value": "x", "$type": "thingamajig"},
        }
        errors = dtcg_mod.validate_dtcg(tree)
        assert any("unknown $type" in e for e in errors), errors

    def test_validate_flags_dangling_alias(self):
        tree = {
            "colors": {
                "$type": "color",
                "ref": {"$value": "{colors.does-not-exist}"},
            },
        }
        errors = dtcg_mod.validate_dtcg(tree)
        assert any("does not resolve" in e for e in errors), errors

    def test_validate_accepts_resolvable_alias_chain(self):
        tree = {
            "a": {"$type": "color", "x": {"$value": "#000"}},
            "b": {"$type": "color", "y": {"$value": "{a.x}"}},
        }
        errors = dtcg_mod.validate_dtcg(tree)
        assert errors == [], errors


# ---------------------------------------------------------------------------
# Group 3: full CLI integration
# ---------------------------------------------------------------------------

class TestDtcgCli:
    """Drive the script as users will — through the CLI."""

    def test_help_exits_zero(self):
        cp = _run(["--help"])
        assert cp.returncode == 0
        assert "DTCG" in cp.stdout or "design tokens" in cp.stdout.lower()

    def test_missing_file_exits_2(self, tmp_path: Path):
        cp = _run([str(tmp_path / "nope.md")])
        assert cp.returncode == 2

    def test_design_md_to_stdout_is_valid_dtcg(self, design_md_file: Path):
        cp = _run([str(design_md_file)])
        assert cp.returncode == 0, cp.stderr
        # Parses as JSON
        tree = json.loads(cp.stdout)
        # Smoke: every expected top-level group is present
        assert "colors" in tree and "typography" in tree
        assert "rounded" in tree and "spacing" in tree
        assert "components" in tree
        # Every leaf has $value (the hard DTCG requirement)
        _walk_assert_value(tree)
        # Every leaf has effective $type (own or inherited)
        _walk_assert_type(tree, parent_type=None)

    def test_design_md_writes_output_file(self, design_md_file: Path, tmp_path: Path):
        out = tmp_path / "tokens.dtcg.json"
        cp = _run([str(design_md_file), "-o", str(out)])
        assert cp.returncode == 0, cp.stderr
        assert out.is_file()
        tree = json.loads(out.read_text(encoding="utf-8"))
        assert "colors" in tree

    def test_aliases_preserved_verbatim_in_components(self, design_md_file: Path):
        cp = _run([str(design_md_file)])
        assert cp.returncode == 0, cp.stderr
        tree = json.loads(cp.stdout)
        btn = tree["components"]["button-primary"]
        assert btn["backgroundColor"]["$value"] == "{colors.primary}"
        assert btn["rounded"]["$value"] == "{rounded.md}"

    def test_json_input_without_harmonize_errors(self, figma_fixture: Path):
        cp = _run([str(figma_fixture)])
        assert cp.returncode == 2
        assert "harmonize" in cp.stderr.lower()

    def test_harmonize_flat_dtcg_keys(self, figma_fixture: Path):
        cp = _run([str(figma_fixture), "--harmonize"])
        assert cp.returncode == 0, cp.stderr
        tree = json.loads(cp.stdout)
        # Every leaf has $value, no bare `value`
        _walk_assert_no_bare(tree)
        # Aliases preserved
        assert tree["color"]["surface"]["subtle"]["$value"] == "{color.brand.secondary}"
        # Inferred types
        assert tree["untyped"]["guess-color"]["$type"] == "color"
        assert tree["untyped"]["guess-dim"]["$type"] == "dimension"
        assert tree["untyped"]["guess-number"]["$type"] == "number"
        # Composite typography preserved
        h = tree["typography"]["headline-lg"]
        assert h["$type"] == "typography"
        assert h["$value"]["fontFamily"] == "Inter"
        assert h["$description"] == "Large headline composite token"

    def test_harmonize_then_validate_catches_bad_alias(self, tmp_path: Path):
        # A figma-style tree with one alias that points nowhere.
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({
            "color": {
                "primary": {"value": "#000", "type": "color"},
                "broken": {"value": "{color.does-not-exist}", "type": "color"},
            },
        }), encoding="utf-8")
        cp = _run([str(bad), "--harmonize"])
        # Validator catches it → exit 3
        assert cp.returncode == 3
        assert "does not resolve" in cp.stderr

    def test_no_validate_flag_suppresses_validation_exit(self, tmp_path: Path):
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({
            "color": {"broken": {"value": "{nope.nope}", "type": "color"}},
        }), encoding="utf-8")
        cp = _run([str(bad), "--harmonize", "--no-validate"])
        assert cp.returncode == 0, cp.stderr
        tree = json.loads(cp.stdout)
        assert tree["color"]["broken"]["$value"] == "{nope.nope}"


# ---------------------------------------------------------------------------
# Walk helpers (assertion utilities)
# ---------------------------------------------------------------------------

def _walk_assert_value(node, path=""):
    """Every dict that *looks* like a leaf must have $value.

    A node is a "leaf" if it has any $-prefixed token key (heuristic that
    matches DTCG's data shape). Groups are dicts without any such key.
    """
    if not isinstance(node, dict):
        return
    has_value = "$value" in node
    has_desc = "$description" in node
    looks_like_leaf = has_value or (has_desc and not any(
        isinstance(v, dict) and ("$value" in v or _is_groupy(v)) for v in node.values()
    ))
    if looks_like_leaf:
        assert "$value" in node, f"{path}: looks like a leaf but missing $value"
        return
    for k, v in node.items():
        if k.startswith("$"):
            continue
        _walk_assert_value(v, f"{path}.{k}" if path else k)


def _is_groupy(d):
    return isinstance(d, dict) and any(not k.startswith("$") for k in d)


def _walk_assert_type(node, parent_type, path=""):
    """Every leaf must have an effective $type (own or inherited from
    nearest group ancestor).
    """
    if not isinstance(node, dict):
        return
    if "$value" in node:
        effective = node.get("$type") or parent_type
        assert effective is not None, f"{path}: leaf without effective $type"
        return
    new_parent = node.get("$type", parent_type)
    for k, v in node.items():
        if k.startswith("$"):
            continue
        _walk_assert_type(v, new_parent, f"{path}.{k}" if path else k)


def _walk_assert_no_bare(node, path=""):
    """After harmonize, no leaf may keep a bare `value`/`type`/`description`."""
    if not isinstance(node, dict):
        return
    if "$value" in node:
        for bare in ("value", "type", "description"):
            assert bare not in node, (
                f"{path}: bare '{bare}' survived harmonize"
            )
        return
    for k, v in node.items():
        if k.startswith("$"):
            continue
        _walk_assert_no_bare(v, f"{path}.{k}" if path else k)
