"""Real tests for the content-layer slop module (T-030) in bin/amw-ai-slop-check.py.

These invoke the actual script via subprocess on temp HTML files and parse its
JSON output — no mocks. They verify each content anti-pattern is flagged, that
clean prose is not, that <script>/<style> contents are masked (no CSS/JS false
positives), and that the default `high` gate ignores the low/medium content
findings while `--severity-threshold low` surfaces them.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "amw-ai-slop-check.py"


def _run(html: str, tmp_path: Path, *flags: str) -> tuple[int, dict]:
    f = tmp_path / "page.html"
    f.write_text(html, encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(f), *flags],
        capture_output=True,
        text=True,
    )
    return r.returncode, json.loads(r.stdout)


def _rules(report: dict) -> str:
    return " || ".join(v["rule"] for v in report["violations"])


SLOPPY = """<!doctype html><html><body>
<span>// SOLUTION</span>
<h1>We build tools — fast — reliable — always</h1>
<p>This is not just fast but reliable.</p>
<p>We leverage robust systems to seamlessly utilize your data.</p>
<p>In 2024, everything changed for the better.</p>
<blockquote>Best tool ever. Sarah J. — CEO at TechCorp</blockquote>
<h2>POWERFUL. RELIABLE. SCALABLE.</h2>
<li>➜ Learn more about the platform</li>
</body></html>"""

CLEAN = """<!doctype html><html><body>
<h1>Ship reports your finance team trusts</h1>
<p>Close the books in three days instead of ten. Connect your ledger, map the
accounts once, and every statement updates itself.</p>
<p>Pricing starts at 49 dollars a month for up to five seats.</p>
<a href="/signup">Start a free trial</a>
</body></html>"""


def test_sloppy_html_flags_each_content_pattern(tmp_path):
    """A page packed with content tells flags em-dash, not-just-but, filler, year-opener, persona, kicker, mono-caps, and glyph."""
    code, report = _run(SLOPPY, tmp_path, "--severity-threshold", "low")
    rules = _rules(report)
    assert "em-dashes as punctuation" in rules
    assert "not just X but Y" in rules
    assert "corporate filler word" in rules
    assert "'In <year>,' opener" in rules
    assert "fake persona byline" in rules
    assert "'//'-kicker" in rules
    assert "mono-caps filler" in rules
    assert "unicode-glyph used as decoration" in rules
    assert code == 1  # at --severity-threshold low, the medium findings trip the gate


def test_clean_prose_has_no_content_violations(tmp_path):
    """Ordinary marketing prose produces zero T-030 content findings."""
    _, report = _run(CLEAN, tmp_path, "--severity-threshold", "low")
    content = [v for v in report["violations"] if v["rule"].startswith("T-030 content")]
    assert content == [], content


def test_script_and_style_contents_are_masked(tmp_path):
    """Filler words inside <script>/<style> are NOT flagged (code-masking works)."""
    html = (
        "<!doctype html><html><head><style>/* leverage robust seamless utilize */"
        ".x{color:#333}</style></head><body><p>Plain honest copy here.</p>"
        "<script>const note = 'we leverage utilize seamless robust';</script></body></html>"
    )
    _, report = _run(html, tmp_path, "--severity-threshold", "low")
    content = [v for v in report["violations"] if v["rule"].startswith("T-030 content")]
    assert content == [], content


def test_passive_voice_flagged_when_dense(tmp_path):
    """A passive-heavy document (>=25% of sentences passive) is flagged."""
    html = (
        "<!doctype html><html><body><p>The report was generated overnight. "
        "The data is stored remotely. Results were computed by the engine. "
        "The dashboard was built last week.</p></body></html>"
    )
    _, report = _run(html, tmp_path, "--severity-threshold", "low")
    assert "passive voice" in _rules(report)


def test_default_high_gate_ignores_low_medium_content(tmp_path):
    """Content-only slop (no high-severity visual rule) passes the default `high` gate (exit 0)."""
    html = "<!doctype html><html><body><p>This is not just fast but reliable.</p></body></html>"
    code, report = _run(html, tmp_path)  # default threshold = high
    assert code == 0
    # but the finding is still recorded for review
    assert "not just X but Y" in _rules(report)
