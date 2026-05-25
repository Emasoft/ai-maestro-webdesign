"""Real tests for the fcvvdp screenshot-parity compare wrapper (bin/amw-screenshot-compare.sh).

These exercise the ACTUAL fcvvdp binary against deterministic PNG fixtures —
no mocks. fcvvdp lives in gitignored libs_dev/ and is not present in CI, so
every test self-skips when the binary is absent (keeping the fast CI gate
green while still running locally).

Fixtures are generated at runtime by tests/fixtures/gen_parity_fixtures.py
(pure stdlib PNG writer) so nothing binary is committed.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
COMPARE = ROOT / "bin" / "amw-screenshot-compare.sh"
FCVVDP = Path(os.environ.get("AMW_FCVVDP_BIN", ROOT / "libs_dev/fcvvdp/zig-out/bin/fcvvdp"))

sys.path.insert(0, str(ROOT / "tests" / "fixtures"))
import gen_parity_fixtures as gen  # noqa: E402  # pyright: ignore[reportMissingImports]

pytestmark = pytest.mark.skipif(
    not FCVVDP.exists(),
    reason="fcvvdp binary not built (libs_dev/fcvvdp); build it to run parity tests",
)


@pytest.fixture(scope="module")
def fixtures(tmp_path_factory) -> dict[str, Path]:
    """Generate the three PNG fixtures once for the module."""
    out = tmp_path_factory.mktemp("parity")
    return gen.generate(out)


def _run(*args: str | Path) -> subprocess.CompletedProcess:
    """Invoke the compare wrapper, returning the completed process."""
    return subprocess.run(
        ["bash", str(COMPARE), *map(str, args)],
        capture_output=True,
        text=True,
    )


def _jod(stdout: str) -> float:
    """Parse the JOD float out of the wrapper's 'JOD N.NNNN ...' stdout line."""
    m = re.search(r"JOD\s+([0-9.]+)", stdout)
    assert m, f"no JOD in output: {stdout!r}"
    return float(m.group(1))


def test_identical_images_score_perfect_and_pass(fixtures):
    """Byte-identical PNGs score JOD ≈ 10 and PASS the strict style bar (9.5)."""
    r = _run(fixtures["identical_a"], fixtures["identical_b"], "--threshold", "9.5")
    assert r.returncode == 0, r.stdout + r.stderr
    assert _jod(r.stdout) >= 9.5


def test_different_images_score_low_and_fail(fixtures):
    """A visually unrelated PNG scores well below the technique bar (9.0) and FAILs."""
    r = _run(fixtures["identical_a"], fixtures["different"], "--threshold", "9.0")
    assert r.returncode == 1, r.stdout + r.stderr
    assert _jod(r.stdout) < 9.0


def test_threshold_gate_passes_when_lowered(fixtures):
    """A low-JOD pair PASSes when the threshold is dropped below its score (gate honors --threshold)."""
    r = _run(fixtures["identical_a"], fixtures["different"], "--threshold", "1.0")
    assert r.returncode == 0, r.stdout + r.stderr


def test_score_json_written_to_out_dir(fixtures, tmp_path):
    """--out writes a parseable score.json sidecar containing the jod field."""
    out = tmp_path / "scoredir"
    r = _run(fixtures["identical_a"], fixtures["identical_b"], "--out", out)
    assert r.returncode == 0, r.stdout + r.stderr
    score = out / "score.json"
    assert score.exists()
    import json

    data = json.loads(score.read_text())
    assert data["jod"] >= 9.5


def test_missing_file_exits_bad_args(fixtures):
    """A nonexistent input path exits 2 (bad args), not 0/1."""
    r = _run(fixtures["identical_a"], fixtures["identical_a"].parent / "nope.png")
    assert r.returncode == 2, r.stdout + r.stderr
