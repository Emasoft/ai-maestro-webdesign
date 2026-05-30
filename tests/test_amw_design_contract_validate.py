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


def test_validate_returns_block_for_top_level_array(tmp_path: Path) -> None:
    """JSON that parses to a list (not object) is BLOCK at load time."""
    mod = _load_validator_module()
    tmp = tmp_path / "array.json"
    tmp.write_text("[1, 2, 3]", encoding="utf-8")
    verdict, findings = mod.validate(tmp)
    assert verdict == "BLOCK"
    codes = [f.code for f in findings]
    assert "B004" in codes


# =====================================================================
# Batch9 Wave 2 Round 3 (T-065) — PASS / FLAG / BLOCK trichotomy tests
# ---------------------------------------------------------------------
# These tests drive the validator against the three new edge-case
# fixtures under `tests/fixtures/contract/` (`warning-only.yaml`,
# `multi-block.yaml`, `empty-contract.yaml`) and assert the canonical
# verdict-to-exit-code mapping:
#
#   PASS  → exit 0  (every required field present, no advisories)
#   FLAG  → exit 1  (at least one F-code finding, no B-code finding)
#   BLOCK → exit 2  (at least one B-code finding)
#
# The .yaml extension on these fixtures is intentional: JSON is a
# strict subset of YAML 1.2, so the file is valid for both parsers.
# The validator always calls `json.loads` regardless of extension; the
# extension only signals to readers that the document is structured.
# =====================================================================

R3_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "contract"


def test_r3_warning_only_yaml_fixture_is_flag_exit_1() -> None:
    """A contract with every required field present but one empty
    advisory (reference_urls) yields verdict FLAG / exit 1."""
    result = _run(str(R3_FIXTURES / "warning-only.yaml"))
    assert result.returncode == 1, (
        f"warning-only.yaml should exit 1; got {result.returncode}\n"
        f"stdout:\n{result.stdout}"
    )
    assert "Verdict:  FLAG" in result.stdout
    # Exactly one FLAG finding — the empty reference_urls.
    assert "[F030]" in result.stdout
    assert "Findings: 1" in result.stdout


def test_r3_multi_block_yaml_fixture_is_block_exit_2() -> None:
    """A contract with every required section present but multiple
    BLOCK-level field violations yields verdict BLOCK / exit 2."""
    result = _run(str(R3_FIXTURES / "multi-block.yaml"))
    assert result.returncode == 2, (
        f"multi-block.yaml should exit 2; got {result.returncode}\n"
        f"stdout:\n{result.stdout}"
    )
    assert "Verdict:  BLOCK" in result.stdout
    # Both BLOCK codes for missing user_intent AND bad brand_tokens hex must be present.
    assert "[B030]" in result.stdout
    assert "[B041]" in result.stdout
    assert "[B042]" in result.stdout
    assert "[B043]" in result.stdout
    assert "[B070]" in result.stdout


def test_r3_empty_contract_yaml_fixture_is_block_exit_2() -> None:
    """A contract that is the literal JSON object `{}` yields BLOCK
    with one B010 finding per missing top-level section."""
    result = _run(str(R3_FIXTURES / "empty-contract.yaml"))
    assert result.returncode == 2
    assert "Verdict:  BLOCK" in result.stdout
    # 7 required top-level sections missing → 7 B010 findings.
    assert result.stdout.count("[B010]") == 7
    assert "Findings: 7" in result.stdout


def test_r3_warning_only_strict_flags_escalates_to_exit_2() -> None:
    """`--strict-flags` promotes the FLAG verdict to exit 2 while
    preserving the verdict string in stdout."""
    result = _run(str(R3_FIXTURES / "warning-only.yaml"), "--strict-flags")
    assert result.returncode == 2
    # The verdict reported on stdout is still FLAG; only the exit code escalates.
    assert "Verdict:  FLAG" in result.stdout


def test_r3_pass_fixture_complete_contract_is_exit_0() -> None:
    """The original `contract-pass.json` exercises the PASS leg of the
    trichotomy: every required field present, every advisory strong."""
    # Reuse the existing fixture (not in r3 subfolder) — it's the canonical
    # PASS example and the trichotomy isn't complete without it.
    result = _run(str(FIXTURES / "contract-pass.json"))
    assert result.returncode == 0
    assert "Verdict:  PASS" in result.stdout
    assert "All checks PASS" in result.stdout


def test_r3_legal_block_when_mandatory_contradicts_target_stack(tmp_path: Path) -> None:
    """A contract where legal.mandatories has a cookie-banner directive
    but target_stack.framework is an email stack yields a hard BLOCK
    (B090) — emails cannot host cookie banners."""
    contract = {
        "meta": {
            "schema_version": "1",
            "contract_id": "20260527-contradiction",
            "created_at": "2026-05-27T10:00:00+02:00",
            "updated_at": "2026-05-27T10:00:00+02:00",
            "phase": "phase_a_locked",
        },
        "user_intent": {
            "project_name": "Email vs Cookie",
            "industry": "marketing automation",
            "primary_audience": "EU subscribers",
            "primary_action": "open the email",
            "tone": "professional",
            "reference_urls": ["https://example.com"],
            "success_metrics": ["open rate >= 25%"],
        },
        "brand_tokens": {
            "primary_color": "#0F4C81",
            "color_mode": "LIGHT",
            "display_font": "Inter",
            "body_font": "Inter",
            "border_radius_bucket": "ROUND_FOUR",
            "neutral_palette": ["#000000", "#ffffff"],
            "preset_fingerprint": "test-contradiction",
        },
        "ia": {
            "pages": [{"name": "Email", "slug": "/", "purpose": "broadcast"}],
            "primary_nav": ["Email"],
        },
        "legal": {
            "jurisdictions": ["EU"],
            "mandatories": ["GDPR cookie banner with reject-all parity"],
        },
        "target_stack": {
            "framework": "email-mjml",
            "css_strategy": "table-layout",
        },
        "decisions_log": [
            {
                "timestamp": "2026-05-27T10:00:00+02:00",
                "decision": "Locked Phase A.",
                "actor": "user",
            },
        ],
    }
    p = tmp_path / "contradiction.json"
    p.write_text(json.dumps(contract), encoding="utf-8")
    result = _run(str(p))
    assert result.returncode == 2
    assert "[B090]" in result.stdout


def test_r3_flag_propagates_per_advisory_independently(tmp_path: Path) -> None:
    """When several advisory fields are weak, each emits its own FLAG
    finding (and the verdict is still FLAG, not BLOCK)."""
    contract = {
        "meta": {
            "schema_version": "1",
            "contract_id": "20260527-many-flags",
            "created_at": "2026-05-27T10:00:00+02:00",
            "updated_at": "2026-05-27T10:00:00+02:00",
            "phase": "phase_a_locked",
        },
        "user_intent": {
            "project_name": "Weak Advisories Only",
            "industry": "test",
            "primary_audience": "validator",
            "primary_action": "exercise FLAG path",
            "tone": "test",
            # reference_urls and success_metrics intentionally absent → 2 FLAGs.
        },
        "brand_tokens": {
            "primary_color": "#FF0000",
            "color_mode": "LIGHT",
            "display_font": "Inter",
            "body_font": "Inter",
            "border_radius_bucket": "ROUND_FOUR",
            # neutral_palette + preset_fingerprint absent → 2 FLAGs.
        },
        "ia": {
            "pages": [{"name": "Home", "slug": "/", "purpose": "test"}],
            "primary_nav": ["Home"],
        },
        "legal": {
            "jurisdictions": [],
            "mandatories": [],
        },
        "target_stack": {
            "framework": "vanilla-html",
            # css_strategy absent → 1 FLAG.
        },
        "decisions_log": [
            {
                "timestamp": "2026-05-27T10:00:00+02:00",
                "decision": "Test fixture.",
                "actor": "test",
            },
        ],
    }
    p = tmp_path / "many-flags.json"
    p.write_text(json.dumps(contract), encoding="utf-8")
    result = _run(str(p))
    assert result.returncode == 1
    assert "Verdict:  FLAG" in result.stdout
    # 5 independent FLAG codes expected: F030, F031, F040, F041, F070.
    for code in ("F030", "F031", "F040", "F041", "F070"):
        assert f"[{code}]" in result.stdout, f"missing FLAG code {code}"
    # No BLOCK findings. The "BLOCK:" header is only emitted when
    # at least one BLOCK finding exists; its absence is a positive
    # signal that the verdict was reached purely via FLAGs.
    assert "BLOCK:" not in result.stdout


def test_r3_json_mode_yaml_fixture_round_trip() -> None:
    """`--json` on a .yaml-named JSON fixture returns a parseable payload
    with verdict + findings list, identical in structure to JSON inputs."""
    result = _run(str(R3_FIXTURES / "warning-only.yaml"), "--json")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "FLAG"
    assert isinstance(payload["findings"], list)
    assert len(payload["findings"]) == 1
    assert payload["findings"][0]["code"] == "F030"
    assert payload["findings"][0]["severity"] == "FLAG"


def test_r3_block_overrides_flag_when_both_present() -> None:
    """Aggregation rule: any BLOCK finding ⇒ verdict BLOCK, regardless of
    how many FLAG findings are also present in the same run."""
    result = _run(str(R3_FIXTURES / "multi-block.yaml"))
    # multi-block.yaml has BOTH BLOCKs (B030, B041, …) AND FLAGs (F030, F031, F040, …).
    # The aggregator must pick BLOCK.
    assert result.returncode == 2
    assert "Verdict:  BLOCK" in result.stdout
    # Both severities are present in the rendered output.
    assert "BLOCK:" in result.stdout
    assert "FLAG:" in result.stdout


def test_r3_load_contract_helper_distinguishes_missing_from_malformed(
    tmp_path: Path,
) -> None:
    """`load_contract` returns B001 for missing file, B003 for bad JSON
    — the two cases must NOT collapse into the same finding code."""
    mod = _load_validator_module()
    missing = tmp_path / "does-not-exist.json"
    contract_missing, findings_missing = mod.load_contract(missing)
    assert contract_missing is None
    assert any(f.code == "B001" for f in findings_missing)

    bad = tmp_path / "bad.json"
    bad.write_text("not json at all", encoding="utf-8")
    contract_bad, findings_bad = mod.load_contract(bad)
    assert contract_bad is None
    assert any(f.code == "B003" for f in findings_bad)


def test_r3_check_top_level_shape_blocks_per_missing_section() -> None:
    """An empty object emits one B010 finding per missing required section."""
    mod = _load_validator_module()
    findings = mod.check_top_level_shape({})
    codes = [f.code for f in findings]
    # 7 required sections → 7 B010 findings, exactly.
    assert codes.count("B010") == 7


def test_r3_check_legal_blocks_when_mandatories_is_not_a_list() -> None:
    """legal.mandatories must be a list; a string value BLOCKs (B061)."""
    mod = _load_validator_module()
    findings = mod.check_legal({"jurisdictions": ["EU"], "mandatories": "GDPR"})
    assert any(f.code == "B061" for f in findings)


def test_r3_check_legal_flags_when_jurisdictions_set_but_mandatories_empty() -> None:
    """Having jurisdictions but no mandatories is a FLAG (F060) — the
    orchestrator should consult amw-legal-expert-agent."""
    mod = _load_validator_module()
    findings = mod.check_legal({"jurisdictions": ["EU", "US"], "mandatories": []})
    assert any(f.code == "F060" for f in findings)


def test_r3_check_decisions_log_blocks_on_non_dict_entry() -> None:
    """A decisions_log entry that isn't an object BLOCKs (B080)."""
    mod = _load_validator_module()
    findings = mod.check_decisions_log(["just a string"])
    assert any(f.code == "B080" for f in findings)


def test_r3_check_meta_flags_non_iso_timestamp_without_blocking() -> None:
    """A timestamp that isn't ISO-8601 emits a FLAG (F020), not a BLOCK."""
    mod = _load_validator_module()
    findings = mod.check_meta({
        "schema_version": "1",
        "contract_id": "x",
        "created_at": "yesterday at noon",
        "updated_at": "2026-05-27T10:00:00+02:00",
        "phase": "phase_a_locked",
    })
    flag_codes = [f.code for f in findings if f.severity == "FLAG"]
    block_codes = [f.code for f in findings if f.severity == "BLOCK"]
    assert "F020" in flag_codes
    # The non-ISO timestamp alone shouldn't BLOCK.
    assert all(c != "F020" for c in block_codes)


def test_r3_check_ia_blocks_on_non_list_pages() -> None:
    """ia.pages must be a list; a dict value BLOCKs (B051)."""
    mod = _load_validator_module()
    findings = mod.check_ia({"pages": {"Home": "/"}, "primary_nav": ["Home"]})
    assert any(f.code == "B051" for f in findings)
