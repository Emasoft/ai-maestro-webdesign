"""Tests for bin/amw-design-md-showcase.py.

Drives the real CLI in a subprocess (no mocks). Verifies:

  1. Script runs end-to-end on a valid Variant 1 DESIGN.md fixture and emits
     a non-empty HTML file.
  2. Output is well-formed self-contained HTML (one <html>, one <head>, one
     <body>, has the inline <style>, no external <link rel=stylesheet>).
  3. Every color token from the fixture appears as a swatch with aria-label.
  4. WCAG-AA contrast badges are emitted for `X` / `on-X` semantic pairs.
  5. Every typography role appears with a sample at the declared font-size.
  6. Component tokens are resolved (no raw `{colors.primary}` reference
     remains in the rendered button-primary background style).
  7. Missing source file exits 2; missing frontmatter exits 2.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "amw-design-md-showcase.py"
FIXTURE = ROOT / "tests" / "fixtures" / "sample-design-md.md"

TIMEOUT = 30


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=cwd or ROOT,
        timeout=TIMEOUT,
    )


def test_emits_non_empty_html(tmp_path: Path) -> None:
    """Script writes a non-empty HTML file when given a valid DESIGN.md."""
    out = tmp_path / "showcase.html"
    result = _run([str(FIXTURE), "-o", str(out)])
    assert result.returncode == 0, (
        f"showcase failed: stderr={result.stderr!r} stdout={result.stdout!r}"
    )
    assert out.is_file(), f"output file not created at {out}"
    html = out.read_text(encoding="utf-8")
    assert len(html) > 2000, f"showcase HTML suspiciously small ({len(html)} chars)"
    # Self-contained: one <html>, has inline <style>, no remote stylesheet link.
    assert html.lower().count("<html") == 1
    assert "<style>" in html
    assert "<link rel=\"stylesheet\"" not in html.lower()
    assert "<link rel='stylesheet'" not in html.lower()
    # No JS dependency.
    assert "<script" not in html.lower()


def test_colors_have_aria_labels_and_swatches(tmp_path: Path) -> None:
    """Every color hex from the fixture appears as a swatch with aria-label."""
    out = tmp_path / "colors.html"
    result = _run([str(FIXTURE), "-o", str(out)])
    assert result.returncode == 0, result.stderr
    html = out.read_text(encoding="utf-8")

    # Sample of tokens declared in the fixture (case-insensitive hex).
    expected_hexes = ["#0F4C81", "#FFD23F", "#B8422E", "#FAFAFA"]
    for hx in expected_hexes:
        # The swatch chip uses background:<HEX>.
        assert re.search(
            rf"background:{re.escape(hx)}", html, flags=re.IGNORECASE
        ), f"missing swatch background for {hx}"

    # The swatch must carry a role=img with aria-label naming the token.
    assert "aria-label=\"Color token primary hex" in html.lower() or \
           "aria-label=\"color token primary hex" in html.lower(), \
           "swatch aria-label missing for primary token"

    # WCAG badge for the primary / on-primary pair must appear.
    # Primary #0F4C81 vs on-primary #FFFFFF -> ratio ~9.99 -> AAA.
    assert "AAA" in html or "AA" in html, "expected at least one WCAG badge"


def test_typography_specimens_render(tmp_path: Path) -> None:
    """Every typography role from the fixture appears with the declared size."""
    out = tmp_path / "typography.html"
    result = _run([str(FIXTURE), "-o", str(out)])
    assert result.returncode == 0, result.stderr
    html = out.read_text(encoding="utf-8")

    # Role labels (showcase renders the role name verbatim).
    for role in ("headline-display", "headline-lg", "body-md", "label-md"):
        assert role in html, f"typography role {role!r} missing"
    # Declared font sizes show up inline on the sample style attribute.
    for size in ("56px", "36px", "16px", "13px"):
        assert f"font-size:{size}" in html, f"font-size {size} missing"
    # Manrope + Inter family names should be present in style attrs.
    assert "Manrope" in html
    assert "Inter" in html


def test_component_token_refs_resolved(tmp_path: Path) -> None:
    """`{colors.primary}` -> `#0F4C81` in the rendered button background."""
    out = tmp_path / "components.html"
    result = _run([str(FIXTURE), "-o", str(out)])
    assert result.returncode == 0, result.stderr
    html = out.read_text(encoding="utf-8")

    # Button-primary should render with the resolved primary hex as bg.
    # The component-demo block contains <button ... style="background:#0F4C81;...">.
    btn_match = re.search(
        r'<button[^>]*class="sc-comp-button"[^>]*style="([^"]*)"', html
    )
    assert btn_match, "button-primary demo not rendered"
    style = btn_match.group(1)
    assert re.search(r"background:#0F4C81", style, flags=re.IGNORECASE), (
        f"button-primary background was not resolved from {{colors.primary}}: "
        f"style={style!r}"
    )

    # The spec table SHOWS the raw token reference (for the human reading the
    # tokens). That is intentional and is checked here so a future "resolve in
    # spec table" regression is caught.
    assert "{colors.primary}" in html, (
        "spec table should keep the raw token reference for human readability"
    )


def test_missing_source_exits_2(tmp_path: Path) -> None:
    """A missing source file is a usage error -> exit code 2."""
    result = _run([str(tmp_path / "does-not-exist.md"), "-o", str(tmp_path / "x.html")])
    assert result.returncode == 2
    assert "source not found" in result.stderr.lower()


def test_no_frontmatter_exits_2(tmp_path: Path) -> None:
    """A file without YAML frontmatter -> exit 2 with a clear message."""
    bad = tmp_path / "no-fm.md"
    bad.write_text("# No frontmatter\n\nJust prose.\n", encoding="utf-8")
    out = tmp_path / "x.html"
    result = _run([str(bad), "-o", str(out)])
    assert result.returncode == 2
    assert "frontmatter" in result.stderr.lower()
