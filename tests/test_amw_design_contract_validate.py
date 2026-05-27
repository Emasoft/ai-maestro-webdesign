"""Tests for `bin/amw-design-contract-validate.py`.

Covers the BLOCK / FLAG / PASS verdict aggregator, the per-section
checks, and the JSON parse-error path. Each test invokes the validator
as a subprocess (so we exercise the CLI exit codes the orchestrator
will rely on) AND imports the module for fine-grained checks.

Plain-stdlib pytest. No external fixtures, no mocks. Real fixtures
from `tests/fixtures/contract-{pass,flag,block}.json`.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "bin" / "amw-design-contract-validate.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def _load_validator_module():
    """Import the script as a module so we can call its helpers directly.

    The filename contains a hyphen, which `import` won't accept; use
    `importlib.util.spec_from_file_location` instead.
    """
    spec = importlib.util.spec_from_file_location(
        "amw_design_contract_validate", SCRIPT
    )
    assert spec is not None and spec.loader is not None, "spec_from_file_location failed"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------
# Subprocess invocations — exercise the real exit codes
# ---------------------------------------------------------------------

def _run(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the validator with the given args and return the result."""
    cmd = [sys.executable, str(SCRIPT), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_pass_fixture_exits_zero() -> None:
    """A clean contract returns PASS / exit 0."""
    result = _run(str(FIXTURES / "contract-pass.json"))
    assert result.returncode == 0, (
        f"PASS fixture should exit 0, got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "PASS" in result.stdout


def test_flag_fixture_exits_one() -> None:
    """A contract with empty advisory fields returns FLAG / exit 1."""
    result = _run(str(FIXTURES / "contract-flag.json"))
    assert result.returncode == 1, (
        f"FLAG fixture should exit 1, got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "FLAG" in result.stdout
    # The flag fixture has no reference URLs and no success metrics.
    assert "reference_urls" in result.stdout or "success_metrics" in result.stdout


def test_block_fixture_exits_two() -> None:
    """A malformed / missing-required contract returns BLOCK / exit 2."""
    result = _run(str(FIXTURES / "contract-block.json"))
    assert result.returncode == 2, (
        f"BLOCK fixture should exit 2, got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "BLOCK" in result.stdout


def test_missing_file_exits_64() -> None:
    """A non-existent contract path is an invocation error (exit 64)."""
    result = _run(str(FIXTURES / "does-not-exist.json"))
    assert result.returncode == 64
    assert "not found" in result.stderr.lower()


def test_malformed_json_blocks(tmp_path: Path) -> None:
    """Unparseable JSON is a hard BLOCK (exit 2), not an invocation error."""
    bad = tmp_path / "bad.json"
    bad.write_text("{ not valid json", encoding="utf-8")
    result = _run(str(bad))
    assert result.returncode == 2
    assert "Malformed JSON" in result.stdout


def test_json_output_mode_is_machine_readable() -> None:
    """`--json` emits a parseable JSON payload with verdict + findings."""
    result = _run(str(FIXTURES / "contract-flag.json"), "--json")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "FLAG"
    assert isinstance(payload["findings"], list)
    assert all("severity" in f and "code" in f for f in payload["findings"])


def test_strict_flags_promotes_flag_to_block_exit_code() -> None:
    """`--strict-flags` makes the FLAG fixture exit 2 instead of 1."""
    result = _run(str(FIXTURES / "contract-flag.json"), "--strict-flags")
    # Verdict in stdout is still FLAG; only the exit code changes.
    assert result.returncode == 2
    assert "FLAG" in result.stdout


# ---------------------------------------------------------------------
# Direct-module invocations — verify the check functions in isolation
# ---------------------------------------------------------------------

def test_schema_version_mismatch_blocks() -> None:
    """A contract whose schema_version differs from SUPPORTED is BLOCK."""
    mod = _load_validator_module()
    findings = mod.check_meta({
        "schema_version": "999",
        "contract_id": "x",
        "created_at": "2026-05-27T10:00:00+02:00",
        "updated_at": "2026-05-27T10:00:00+02:00",
        "phase": "phase_a_locked",
    })
    block_codes = [f.code for f in findings if f.severity == "BLOCK"]
    assert "B022" in block_codes


def test_hex_color_validation_catches_garbage() -> None:
    """A non-hex primary_color BLOCKs."""
    mod = _load_validator_module()
    findings = mod.check_brand_tokens({
        "primary_color": "blueish",
        "color_mode": "LIGHT",
        "display_font": "Inter",
        "body_font": "Inter",
        "border_radius_bucket": "ROUND_FOUR",
    })
    block_codes = [f.code for f in findings if f.severity == "BLOCK"]
    assert "B041" in block_codes


def test_email_stack_with_cookie_banner_is_contradiction() -> None:
    """legal.mandatories with cookie banner + email framework BLOCKs."""
    mod = _load_validator_module()
    contract = {
        "legal": {
            "jurisdictions": ["EU"],
            "mandatories": ["GDPR cookie banner"],
        },
        "target_stack": {"framework": "email-mjml"},
        "user_intent": {},
        "brand_tokens": {},
    }
    findings = mod.check_cross_section_consistency(contract)
    block_codes = [f.code for f in findings if f.severity == "BLOCK"]
    assert "B090" in block_codes


def test_luxury_light_mode_flags_but_does_not_block() -> None:
    """Tone='luxury' + LIGHT mode is FLAG (advisory), not BLOCK."""
    mod = _load_validator_module()
    contract = {
        "user_intent": {"tone": "luxury and premium"},
        "brand_tokens": {"color_mode": "LIGHT"},
        "legal": {"jurisdictions": [], "mandatories": []},
        "target_stack": {"framework": "shadcn+next"},
    }
    findings = mod.check_cross_section_consistency(contract)
    flag_codes = [f.code for f in findings if f.severity == "FLAG"]
    block_codes = [f.code for f in findings if f.severity == "BLOCK"]
    assert "F090" in flag_codes
    assert not block_codes


def test_empty_required_user_intent_field_blocks() -> None:
    """A blank string in a required user_intent field BLOCKs."""
    mod = _load_validator_module()
    findings = mod.check_user_intent({
        "project_name": "",
        "industry": "saas",
        "primary_audience": "devs",
        "primary_action": "trial",
        "tone": "technical",
    })
    block_codes = [f.code for f in findings if f.severity == "BLOCK"]
    assert "B030" in block_codes


def test_validate_returns_block_for_top_level_array() -> None:
    """JSON that parses to a list (not object) is BLOCK at load time."""
    mod = _load_validator_module()
    tmp = REPO_ROOT / "tests" / "fixtures" / "__tmp_array.json"
    try:
        tmp.write_text("[1, 2, 3]", encoding="utf-8")
        verdict, findings = mod.validate(tmp)
        assert verdict == "BLOCK"
        codes = [f.code for f in findings]
        assert "B004" in codes
    finally:
        if tmp.exists():
            tmp.unlink()
