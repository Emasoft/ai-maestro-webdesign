"""Regression tests for bin/amw-validate-cross-refs.sh resolution semantics.

The validator gained two rules that need locking down:

1. A bare-basename "see also" ref (``TECH-01-yaml-frontmatter.md``) resolves by
   searching ``skills/`` + ``agents/`` for that filename, because a doc reorg
   split the reference corpus across sibling skills.
2. Refs into ``external/hyperframes/`` are skipped — an on-demand, gitignored
   runtime dependency that is never shipped.

The danger is that rule 1 becomes a loophole that green-lights genuinely broken
paths. These tests run the REAL script against a REAL fixture tree (the script
derives its plugin root from its own location, so we copy it into tmp_path) and
assert it still fails loudly on both a bare name that exists nowhere and a
path-bearing ref that does not resolve exactly as written.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "amw-validate-cross-refs.sh"

TIMEOUT = 60


def _fixture(tmp_path: Path, bullets: str) -> Path:
    """Build a minimal plugin tree in tmp_path and return its root."""
    (tmp_path / "bin").mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCRIPT, tmp_path / "bin" / SCRIPT.name)

    # A sibling skill that OWNS the real target file.
    beta_refs = tmp_path / "skills" / "beta" / "references"
    beta_refs.mkdir(parents=True, exist_ok=True)
    (beta_refs / "real-target.md").write_text("# real target\n", encoding="utf-8")

    alpha = tmp_path / "skills" / "alpha"
    alpha.mkdir(parents=True, exist_ok=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\ndescription: fixture\n---\n\n"
        "# Alpha\n\n## Cross-references\n\n" + bullets + "\n",
        encoding="utf-8",
    )
    return tmp_path


def _run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the copied validator inside the fixture root."""
    return subprocess.run(
        ["bash", str(root / "bin" / SCRIPT.name), *args],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def test_bare_basename_resolves_via_sibling_skill(tmp_path: Path) -> None:
    """A bare `<name>.md` owned by another skill's references/ resolves, not MISSING."""
    root = _fixture(tmp_path, "- `real-target.md` — cited by bare name from a sibling skill")
    res = _run(root, "--strict")
    assert "MISSING" not in res.stdout, res.stdout
    assert "found 0 broken references" in res.stdout
    assert res.returncode == 0


def test_bare_basename_absent_everywhere_is_still_missing(tmp_path: Path) -> None:
    """A bare `<name>.md` that exists nowhere must still be reported MISSING."""
    root = _fixture(tmp_path, "- `definitely-nonexistent-file.md` — nothing owns this")
    res = _run(root, "--strict")
    assert "MISSING" in res.stdout
    assert "definitely-nonexistent-file.md" in res.stdout
    assert res.returncode == 1


def test_path_bearing_ref_is_not_rescued_by_basename_fallback(tmp_path: Path) -> None:
    """A wrong PATH whose basename exists elsewhere must still be MISSING (no loophole)."""
    # `real-target.md` really exists at skills/beta/references/, but this cites it
    # under a skill directory that does not exist. The fallback must NOT rescue it.
    root = _fixture(
        tmp_path,
        "- `skills/gamma/references/real-target.md` — wrong path, right basename",
    )
    res = _run(root, "--strict")
    assert "MISSING" in res.stdout
    assert "skills/gamma/references/real-target.md" in res.stdout
    assert res.returncode == 1


def test_external_hyperframes_refs_are_skipped(tmp_path: Path) -> None:
    """Refs into the gitignored on-demand external/hyperframes/ dep are skipped."""
    root = _fixture(
        tmp_path,
        "- `external/hyperframes/CLAUDE.md` — on-demand external dep\n"
        "- `../external/hyperframes/` — relative form of the same dep",
    )
    res = _run(root, "--strict")
    assert "MISSING" not in res.stdout, res.stdout
    assert "found 0 broken references" in res.stdout
    assert res.returncode == 0


def test_vendored_external_path_is_still_validated(tmp_path: Path) -> None:
    """The hyperframes skip is narrow: other external/ paths stay validated."""
    root = _fixture(tmp_path, "- `external/mermaid-render/LICENSE` — vendored, must resolve")
    res = _run(root, "--strict")
    assert "MISSING" in res.stdout
    assert "external/mermaid-render/LICENSE" in res.stdout
    assert res.returncode == 1


def test_non_strict_mode_exits_zero_despite_broken_refs(tmp_path: Path) -> None:
    """Without --strict the validator reports breakage but exits 0."""
    root = _fixture(tmp_path, "- `definitely-nonexistent-file.md` — nothing owns this")
    res = _run(root)
    assert "MISSING" in res.stdout
    assert res.returncode == 0
