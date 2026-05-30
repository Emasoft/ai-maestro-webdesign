"""🐌 Opt-in end-to-end test for the screenshot-parity orchestrator (bin/amw-verify-parity.sh).

This drives the FULL harness: dev-browser renders real pages (Chromium) at a
fixed viewport, then fcvvdp scores the pair. It is SLOW and needs three external
tools (fcvvdp, dev-browser, Chromium), so it is opt-in: it runs only when
AMW_VERIFY=1 is set AND all three tools are present. CI leaves AMW_VERIFY unset,
so this stays out of the fast gate (per the plan).

Run locally with:  AMW_VERIFY=1 uv run pytest tests/test_verify_parity.py -v
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
VERIFY = ROOT / "bin" / "amw-verify-parity.sh"
FCVVDP = Path(os.environ.get("AMW_FCVVDP_BIN", ROOT / "libs_dev/fcvvdp/zig-out/bin/fcvvdp"))

pytestmark = [
    pytest.mark.skipif(
        os.environ.get("AMW_VERIFY") != "1",
        reason="opt-in browser harness test; set AMW_VERIFY=1 to run",
    ),
    pytest.mark.skipif(not FCVVDP.exists(), reason="fcvvdp binary not built"),
    pytest.mark.skipif(shutil.which("dev-browser") is None, reason="dev-browser not on PATH"),
]

_WARM = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;font-family:Georgia,serif;background:#f4f1eb;color:#1a1a1a}
.hero{padding:48px;max-width:680px;margin:0 auto}h1{font-size:42px;margin:0 0 16px}
.cta{display:inline-block;margin-top:24px;padding:12px 28px;background:#4a5d4e;color:#fff;border-radius:6px}
</style></head><body><div class="hero"><h1>Parity Page</h1><p>Warm editorial sample.</p>
<a class="cta">Action</a></div></body></html>"""

_NEON = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;font-family:Arial,sans-serif;background:#0a0a12;color:#00ff41}
.hero{padding:80px 24px;text-align:center}h1{font-size:64px;margin:0;text-transform:uppercase}
.cta{display:inline-block;margin-top:40px;padding:20px 60px;background:#f0f;color:#000;border-radius:40px}
</style></head><body><div class="hero"><h1>NEON</h1><p>Cyberpunk sample.</p><a class="cta">CLICK</a></div></body></html>"""


TIMEOUT = 300


def _run(source: Path, mine: Path, out: Path, threshold: str = "9.0") -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "bash", str(VERIFY),
            "--id", "pytest", "--source", str(source), "--mine", str(mine),
            "--viewports", "1024x768", "--threshold", threshold, "--out", str(out),
        ],
        capture_output=True, text=True,
        timeout=TIMEOUT,
    )


def test_identical_pages_pass_parity(tmp_path):
    """Rendering the same page as source and mine scores JOD ≈ 10 and PASSes (exit 0)."""
    page = tmp_path / "warm.html"
    page.write_text(_WARM, encoding="utf-8")
    r = _run(page, page, tmp_path / "out-same", threshold="9.5")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "PASS" in (tmp_path / "out-same" / "verdict.md").read_text()


def test_different_pages_fail_parity(tmp_path):
    """A warm-editorial page vs a neon-cyberpunk page falls below the 9.0 bar and FAILs (exit 1)."""
    warm = tmp_path / "warm.html"
    neon = tmp_path / "neon.html"
    warm.write_text(_WARM, encoding="utf-8")
    neon.write_text(_NEON, encoding="utf-8")
    r = _run(warm, neon, tmp_path / "out-diff", threshold="9.0")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "FAIL" in (tmp_path / "out-diff" / "verdict.md").read_text()
