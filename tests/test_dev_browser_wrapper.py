"""🐌 Opt-in regression test for bin/amw-dev-browser-wrapper.sh (QuickJS script API).

The wrapper was rewritten off the removed `dev-browser screenshot`/`eval`
subcommands onto the current script API (browser.newPage() → Playwright →
saveScreenshot()/writeFile()). This locks in shot + dom against regressions.

Needs dev-browser + Chromium; opt-in via AMW_VERIFY=1 so CI stays out of it.
Run locally with:  AMW_VERIFY=1 uv run pytest tests/test_dev_browser_wrapper.py -v
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WRAPPER = ROOT / "bin" / "amw-dev-browser-wrapper.sh"

pytestmark = [
    pytest.mark.skipif(
        os.environ.get("AMW_VERIFY") != "1",
        reason="opt-in browser test; set AMW_VERIFY=1 to run",
    ),
    pytest.mark.skipif(shutil.which("dev-browser") is None, reason="dev-browser not on PATH"),
]

_HTML = """<!doctype html><html><head><meta charset="utf-8"><title>Wrapper Test</title>
<style>body{background:#f4f1eb;color:#1a1a1a;font-family:Georgia,serif}
h1{font-size:40px}</style></head><body><h1>Heading Sample</h1>
<p>Body paragraph for DOM capture.</p><a href="#">A link</a></body></html>"""


TIMEOUT = 60

def _page(tmp_path: Path) -> str:
    p = tmp_path / "page.html"
    p.write_text(_HTML, encoding="utf-8")
    return f"file://{p}"


def test_shot_produces_a_png(tmp_path):
    """`shot <url> out.png` writes a real PNG file (magic bytes present)."""
    out = tmp_path / "shot.png"
    r = subprocess.run(
        ["bash", str(WRAPPER), "shot", _page(tmp_path), str(out)],
        capture_output=True, text=True, timeout=TIMEOUT,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert out.exists() and out.stat().st_size > 0
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_dom_returns_expected_json_shape(tmp_path):
    """`dom <url> out.json` writes parseable JSON carrying the design-extract subset."""
    out = tmp_path / "dom.json"
    r = subprocess.run(
        ["bash", str(WRAPPER), "dom", _page(tmp_path), str(out)],
        capture_output=True, text=True, timeout=TIMEOUT,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    for key in ("title", "url", "viewport", "scroll", "bodyBg", "bodyFont", "samples"):
        assert key in data, f"missing key {key}"
    assert data["title"] == "Wrapper Test"
    assert "rgb(244, 241, 235)" in data["bodyBg"]
    assert data["samples"]["h1"][0]["text"] == "Heading Sample"
