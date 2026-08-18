"""R22 enforcement: every GitHub-bound template ships the self-ID byline (TRDD-LR5ERAXT).

R22 (CLAUDE.md "GitHub writes", PRRD G1.1): every issue/comment/PR/review this
repo posts opens with a one-line self-identification, because all AI Maestro
agents share the repo-owner gh auth. The byline is prose written at gh-write
time, so a repo artifact cannot gate the WRITE itself — what CAN be gated is
every TEMPLATE the repo ships for GitHub-bound text: a template without the
byline mints byline-less comments forever. Today the repo ships no such
templates; this test asserts the byline the moment one is added.

No mocks: scans the real .github/ tree.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB = ROOT / ".github"

# The load-bearing phrase of the R22 byline (CLAUDE.md's canonical example is
# "This is the Claude responsible for the ai-maestro-webdesign project.").
BYLINE_MARKER = "responsible for the ai-maestro-webdesign"

# GitHub-bound template surfaces. Workflows are NOT templates (they are code,
# and gh-comment steps inside them are caught by the *_TEMPLATE dirs they read
# or by review) — scanning them would flag unrelated YAML.
TEMPLATE_GLOBS = (
    "ISSUE_TEMPLATE/*.md",
    "ISSUE_TEMPLATE/*.yml",
    "ISSUE_TEMPLATE/*.yaml",
    "PULL_REQUEST_TEMPLATE.md",
    "PULL_REQUEST_TEMPLATE/*.md",
    "DISCUSSION_TEMPLATE/*.yml",
    "DISCUSSION_TEMPLATE/*.yaml",
)


def _templates() -> list[Path]:
    return [p for g in TEMPLATE_GLOBS for p in GITHUB.glob(g) if p.is_file()]


def _missing_byline(paths: list[Path]) -> list[str]:
    return [
        str(p.relative_to(ROOT))
        for p in paths
        if BYLINE_MARKER not in p.read_text(encoding="utf-8")
    ]


def test_github_templates_carry_r22_byline() -> None:
    """Every shipped GitHub template contains the R22 self-ID byline."""
    missing = _missing_byline(_templates())
    assert not missing, (
        "GitHub template(s) missing the R22 self-ID byline "
        f"({BYLINE_MARKER!r}): {missing}. Every template this repo ships mints "
        "GitHub posts under the shared owner auth — add the byline line."
    )


def test_byline_scanner_positive_control(tmp_path: Path) -> None:
    """Positive control: a template WITHOUT the byline is caught by the scanner."""
    bad = tmp_path / "PULL_REQUEST_TEMPLATE.md"
    bad.write_text("## Summary\n\n<describe the change>\n", encoding="utf-8")
    good = tmp_path / "with_byline.md"
    good.write_text(
        "This is the Claude responsible for the ai-maestro-webdesign project.\n",
        encoding="utf-8",
    )
    flagged = [
        p.name for p in (bad, good) if BYLINE_MARKER not in p.read_text("utf-8")
    ]
    assert flagged == ["PULL_REQUEST_TEMPLATE.md"]
