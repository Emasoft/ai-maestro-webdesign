"""Tests for `bin/amw-design-md-validate.py`.

Covers the structural, token-quality, and reference-resolution checks
the validator emits against Variant 1 (canonical) and Variant 2
(community) DESIGN.md files. Every test invokes the real script as a
subprocess (so we exercise the CLI exit codes the orchestrator depends
on) AND, for the structural checks, imports the module directly so we
can call its helpers in isolation.

Exit-code contract under test:
  0 → PASS  (no findings, or only P2-severity informational findings)
  1 → FAIL  (at least one P0 or P1 finding)
  2 → invocation error (file not found, bad CLI args)

Plain-stdlib pytest. No mocks of the validator itself; everything is
exercised through real subprocess invocations and module imports.
Fixtures live under `tests/fixtures/design-md/` and are committed
alongside this test file so any regression in the validator surfaces
on the next CI run.

Authored for batch9 Wave 2 Round 3 (T-065 validator quality tests).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "bin" / "amw-design-md-validate.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "design-md"

TIMEOUT = 30


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _run(*args: str) -> subprocess.CompletedProcess[str]:
    """Invoke the validator as a subprocess and return the result."""
    cmd = [sys.executable, str(SCRIPT), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=TIMEOUT)


def _load_validator_module():
    """Import the script as a module so its helpers are directly testable.

    The filename contains a hyphen, which `import` won't accept; use
    `importlib.util.spec_from_file_location` instead.
    """
    spec = importlib.util.spec_from_file_location(
        "amw_design_md_validate", SCRIPT,
    )
    assert spec is not None and spec.loader is not None, "spec_from_file_location failed"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------
# Subprocess-driven fixture tests
# ---------------------------------------------------------------------

def test_good_fixture_passes_with_no_findings() -> None:
    """A clean Variant 1 DESIGN.md exits 0 with zero findings."""
    result = _run(str(FIXTURES / "good.md"))
    assert result.returncode == 0, (
        f"good.md should exit 0; got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "Verdict: PASS" in result.stdout
    assert "Findings: 0" in result.stdout


def test_bad_frontmatter_fixture_fails_with_s1_v1() -> None:
    """An unclosed frontmatter block produces a single P0/S1.V1 finding."""
    result = _run(str(FIXTURES / "bad-frontmatter.md"))
    assert result.returncode == 1
    assert "Verdict: FAIL" in result.stdout
    assert "[P0/S1.V1]" in result.stdout
    assert "Frontmatter not properly closed" in result.stdout


def test_bad_tokens_fixture_fails_with_r1_per_reference() -> None:
    """Every dangling {path.to.token} reference emits one P0/R1 finding."""
    result = _run(str(FIXTURES / "bad-tokens.md"))
    assert result.returncode == 1
    assert "Verdict: FAIL" in result.stdout
    # The fixture has 4 dangling references: 3 inside button-primary, 1 inside card.
    assert result.stdout.count("[P0/R1]") == 4, (
        f"expected exactly 4 [P0/R1] findings, got:\n{result.stdout}"
    )
    assert "Unresolved reference {colors.missing-primary}" in result.stdout


def test_malformed_color_fixture_fails_with_t1_per_color() -> None:
    """Every non-hex color value emits a P1/T1 finding."""
    result = _run(str(FIXTURES / "malformed-color.md"))
    assert result.returncode == 1
    # 4 invalid colors: primary, secondary, tertiary, quaternary (good-one is valid).
    assert result.stdout.count("[P1/T1]") == 4
    assert "invalid color value 'blueish'" in result.stdout
    assert "invalid color value '#FFFFFFG'" in result.stdout


def test_missing_brand_fixture_fails_with_t8_v1() -> None:
    """Missing required `name` frontmatter field is P1/T8.V1."""
    result = _run(str(FIXTURES / "missing-brand.md"))
    assert result.returncode == 1
    assert "[P1/T8.V1]" in result.stdout
    assert "Frontmatter missing required 'name' field" in result.stdout


def test_oversize_section_fixture_fails_with_s4_and_s5() -> None:
    """Out-of-order sections emit S4.V1; duplicates emit S5.V1."""
    result = _run(str(FIXTURES / "oversize-section.md"))
    assert result.returncode == 1
    # Out-of-order findings (Colors, Layout, Elevation, Colors-dup, Shapes are
    # all out of order relative to the typography-first ordering).
    assert "[P0/S4.V1]" in result.stdout
    # Duplicate Colors heading.
    assert "[P0/S5.V1]" in result.stdout
    assert "Duplicate section heading: ## Colors" in result.stdout


def test_json_output_mode_emits_machine_readable_payload() -> None:
    """`--json` produces a single JSON object with verdict + findings list."""
    result = _run(str(FIXTURES / "malformed-color.md"), "--json")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "FAIL"
    assert payload["variant"] == 1
    assert isinstance(payload["findings"], list)
    assert all(
        "severity" in f and "code" in f and "message" in f
        for f in payload["findings"]
    )
    # At least one finding cites the malformed color value.
    assert any("blueish" in f["message"] for f in payload["findings"])


def test_json_output_for_passing_file_has_empty_findings() -> None:
    """JSON mode on a clean file emits verdict=PASS and an empty list."""
    result = _run(str(FIXTURES / "good.md"), "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "PASS"
    assert payload["findings"] == []


def test_missing_file_exits_2() -> None:
    """A non-existent path produces an invocation error (exit 2)."""
    result = _run(str(FIXTURES / "does-not-exist.md"))
    assert result.returncode == 2
    assert "file not found" in result.stderr.lower()


def test_explicit_variant_1_flag_matches_auto_detect() -> None:
    """`--variant 1` on a V1 file yields the same verdict as auto-detect."""
    auto = _run(str(FIXTURES / "good.md"))
    explicit = _run(str(FIXTURES / "good.md"), "--variant", "1")
    assert auto.returncode == explicit.returncode == 0
    assert "Variant: 1" in explicit.stdout


def test_v2_complete_fixture_passes(tmp_path: Path) -> None:
    """A complete Variant 2 9-section file with XML tags and a mermaid block PASSes."""
    v2 = tmp_path / "v2-complete.md"
    v2.write_text(
        "# Design System Inspired by AMW r3 Tests\n\n"
        "## 1. Visual Theme & Atmosphere\nx\n\n"
        "## 2. Color Palette & Roles\nx\n\n"
        "## 3. Typography Rules\nx\n\n"
        "## 4. Component Stylings\nx\n\n"
        "## 5. Layout Principles\nx\n\n"
        "## 6. Depth & Elevation\nx\n\n"
        "## 7. Do's and Don'ts\nx\n\n"
        "## 8. Responsive Behavior\nx\n\n"
        "## 9. Agent Prompt Guide\nx\n\n"
        "<context>x</context>\n<design_tokens>x</design_tokens>\n<constraints>x</constraints>\n\n"
        "```mermaid\ngraph TD\nA --> B\n```\n",
        encoding="utf-8",
    )
    result = _run(str(v2))
    assert result.returncode == 0
    assert "Variant: 2" in result.stdout
    assert "Verdict: PASS" in result.stdout


def test_v2_incomplete_fixture_reports_missing_sections(tmp_path: Path) -> None:
    """A V2 file missing 7 of 9 numbered sections fails with one S1.V2 per missing."""
    v2 = tmp_path / "v2-incomplete.md"
    v2.write_text(
        "# Design System Inspired by Stripe\n\n"
        "## 1. Visual Theme & Atmosphere\nx\n\n"
        "## 5. Layout Principles\nx\n",
        encoding="utf-8",
    )
    result = _run(str(v2))
    assert result.returncode == 1
    # 7 missing numbered sections (2, 3, 4, 6, 7, 8, 9).
    assert result.stdout.count("[P1/S1.V2]") == 7


def test_v2_p2_only_findings_still_pass(tmp_path: Path) -> None:
    """A V2 file with all 9 sections but no XML tags / mermaid emits only P2s and still passes."""
    v2 = tmp_path / "v2-no-tags.md"
    v2.write_text(
        "# Design System Inspired by SomeBrand\n\n"
        "## 1. Visual Theme & Atmosphere\nx\n\n"
        "## 2. Color Palette & Roles\nx\n\n"
        "## 3. Typography Rules\nx\n\n"
        "## 4. Component Stylings\nx\n\n"
        "## 5. Layout Principles\nx\n\n"
        "## 6. Depth & Elevation\nx\n\n"
        "## 7. Do's and Don'ts\nx\n\n"
        "## 8. Responsive Behavior\nx\n\n"
        "## 9. Agent Prompt Guide\nx\n",
        encoding="utf-8",
    )
    result = _run(str(v2))
    # All four P2 findings present (3 XML tags + mermaid), but verdict is still PASS.
    assert result.returncode == 0, (
        f"P2-only findings should still PASS; got exit {result.returncode}\n"
        f"stdout:\n{result.stdout}"
    )
    assert "Verdict: PASS" in result.stdout
    assert "[P2/S2.V2]" in result.stdout  # XML tag advisory
    assert "[P2/S5.V2]" in result.stdout  # mermaid advisory


# ---------------------------------------------------------------------
# Direct-module invocations — exercise helpers in isolation
# ---------------------------------------------------------------------

def test_detect_variant_recognises_v1_frontmatter() -> None:
    """A file beginning with `---` is Variant 1."""
    mod = _load_validator_module()
    assert mod.detect_variant("---\nname: x\n---\n# Title\n") == 1


def test_detect_variant_recognises_v2_header() -> None:
    """A file beginning with `# Design System Inspired by` is Variant 2."""
    mod = _load_validator_module()
    assert mod.detect_variant("# Design System Inspired by Foo\n\n## 1. x\n") == 2


def test_split_frontmatter_returns_none_on_unclosed_block() -> None:
    """Frontmatter missing the closing `---` returns (None, body, 1)."""
    mod = _load_validator_module()
    fm, _, line = mod.split_frontmatter("---\nname: x\n# no closing\n")
    assert fm is None
    assert line == 1


def test_split_frontmatter_extracts_yaml_between_delimiters() -> None:
    """A well-formed frontmatter block returns the YAML text and body."""
    mod = _load_validator_module()
    content = "---\nname: Brand\n---\n# Title\nBody.\n"
    fm, body, line = mod.split_frontmatter(content)
    assert fm is not None
    assert "name: Brand" in fm
    assert "# Title" in body
    assert line == 4


def test_dimension_regex_accepts_px_em_rem_and_calc() -> None:
    """The DIMENSION_RE allows px / em / rem units AND calc() expressions."""
    mod = _load_validator_module()
    assert mod.DIMENSION_RE.match("16px")
    assert mod.DIMENSION_RE.match("1.5rem")
    assert mod.DIMENSION_RE.match("2em")
    assert mod.DIMENSION_RE.match("calc(100% - 16px)")
    assert not mod.DIMENSION_RE.match("16")          # bare number rejected
    assert not mod.DIMENSION_RE.match("16dpi")        # wrong unit rejected
    assert not mod.DIMENSION_RE.match("16 px")        # whitespace rejected


def test_hex_regex_accepts_three_six_and_eight_digit_forms() -> None:
    """HEX_RE accepts #RGB, #RRGGBB, and #RRGGBBAA."""
    mod = _load_validator_module()
    assert mod.HEX_RE.match("#FFF")
    assert mod.HEX_RE.match("#FFFFFF")
    assert mod.HEX_RE.match("#FFFFFF80")  # alpha channel
    assert not mod.HEX_RE.match("#FFFG")      # bad hex digit
    assert not mod.HEX_RE.match("FFFFFF")     # missing #
    assert not mod.HEX_RE.match("#FF")        # too short


def test_collect_token_paths_walks_nested_dicts() -> None:
    """`collect_token_paths` yields every dotted path in the YAML tree."""
    mod = _load_validator_module()
    fm = {
        "colors": {"primary": "#000", "secondary": "#fff"},
        "rounded": {"sm": "4px"},
    }
    paths = mod.collect_token_paths(fm)
    assert "colors" in paths
    assert "colors.primary" in paths
    assert "colors.secondary" in paths
    assert "rounded" in paths
    assert "rounded.sm" in paths


def test_validate_references_flags_unresolved_at_correct_path() -> None:
    """An unresolved {path} reference produces a P0/R1 finding with the parent path."""
    mod = _load_validator_module()
    fm = {
        "colors": {"primary": "#FF0000"},
        "components": {
            "button": {"bg": "{colors.does-not-exist}"},
        },
    }
    findings: list = []
    mod.validate_references(fm, findings)
    r1 = [f for f in findings if f.code == "R1"]
    assert len(r1) == 1
    assert "{colors.does-not-exist}" in r1[0].message
    assert "components.button.bg" in r1[0].message


def test_validate_references_passes_when_all_resolve() -> None:
    """No findings emitted when every reference resolves."""
    mod = _load_validator_module()
    fm = {
        "colors": {"primary": "#FF0000"},
        "components": {
            "button": {"bg": "{colors.primary}"},
        },
    }
    findings: list = []
    mod.validate_references(fm, findings)
    assert findings == []


def test_validate_v1_tokens_flags_invalid_color() -> None:
    """`validate_v1_tokens` emits P1/T1 for a non-hex color."""
    mod = _load_validator_module()
    findings: list = []
    mod.validate_v1_tokens({"colors": {"primary": "not-a-hex"}}, findings)
    t1 = [f for f in findings if f.code == "T1"]
    assert any("primary" in f.message for f in t1)


def test_validate_v1_tokens_flags_missing_typography_field() -> None:
    """A typography row missing required keys emits one P1/T2 per missing key."""
    mod = _load_validator_module()
    findings: list = []
    mod.validate_v1_tokens(
        {
            "typography": {
                "body": {"fontFamily": "Inter"},  # missing fontSize/fontWeight/lineHeight
            }
        },
        findings,
    )
    t2 = [f for f in findings if f.code == "T2"]
    # Three required fields missing.
    assert len(t2) == 3


def test_validate_v1_tokens_flags_fontweight_out_of_range() -> None:
    """fontWeight outside 100-900 emits P1/T8."""
    mod = _load_validator_module()
    findings: list = []
    mod.validate_v1_tokens(
        {
            "typography": {
                "body": {
                    "fontFamily": "Inter",
                    "fontSize": "16px",
                    "fontWeight": 1200,
                    "lineHeight": "1.5",
                },
            }
        },
        findings,
    )
    t8 = [f for f in findings if f.code == "T8" and "fontWeight" in f.message]
    assert t8, f"expected fontWeight T8 finding, got {[f.code for f in findings]}"


def test_validate_v1_tokens_accepts_token_reference_in_color_slot() -> None:
    """A `{...}` reference in a color slot is NOT flagged as invalid hex."""
    mod = _load_validator_module()
    findings: list = []
    mod.validate_v1_tokens({"colors": {"primary": "{colors.brand-base}"}}, findings)
    # Reference-handling is done by `validate_references`, not `validate_v1_tokens`.
    # The token-value check must skip token refs entirely.
    t1 = [f for f in findings if f.code == "T1"]
    assert not t1, f"token refs in color slots should not raise T1, got {[(f.code, f.message) for f in t1]}"


def test_finding_to_dict_round_trips() -> None:
    """`Finding.to_dict()` returns severity / code / message / line keys."""
    mod = _load_validator_module()
    f = mod.Finding("P0", "R1", "Unresolved reference {x.y}", 42)
    d = f.to_dict()
    assert d == {
        "severity": "P0",
        "code": "R1",
        "message": "Unresolved reference {x.y}",
        "line": 42,
    }


def test_finding_str_includes_severity_code_and_line() -> None:
    """`str(Finding)` formats as `[severity/code] L<line>: message`."""
    mod = _load_validator_module()
    s = str(mod.Finding("P1", "T1", "bad color", 12))
    assert "[P1/T1]" in s
    assert "L12" in s
    assert "bad color" in s


@pytest.mark.parametrize("fixture", [
    "good.md",
    "bad-frontmatter.md",
    "bad-tokens.md",
    "malformed-color.md",
    "missing-brand.md",
    "oversize-section.md",
])
def test_every_fixture_returns_consistent_json_shape(fixture: str) -> None:
    """Every fixture, pass or fail, emits a JSON object with the same top-level keys."""
    result = _run(str(FIXTURES / fixture), "--json")
    # Pass = 0, fail = 1. None of these fixtures should raise an invocation error.
    assert result.returncode in (0, 1), (
        f"{fixture} should never exit 2 (invocation error); got {result.returncode}"
    )
    payload = json.loads(result.stdout)
    assert set(payload.keys()) >= {"file", "variant", "verdict", "findings"}
    assert payload["verdict"] in ("PASS", "FAIL")
    assert isinstance(payload["findings"], list)
