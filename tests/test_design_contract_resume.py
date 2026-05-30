"""Tests for `bin/amw-design-contract-validate.py --check-resumable`.

The `--check-resumable` flag is the binary resumable / not-resumable signal
the `amw-design-resume-agent` consumes. It exits 0 when the contract has
enough state to resume an interrupted workflow without re-elicitation,
exit 1 when more elicitation is needed (sparse contract), and exit 2 when
the underlying contract is BLOCK-malformed (same exit code as the regular
validator's BLOCK verdict — repair before resume).

Plain-stdlib pytest. Real fixtures synthesized in-test (no shared mutable
state in tests/fixtures/) so each test is hermetic. Subprocess invocations
exercise the real CLI exit codes the orchestrator relies on.

Test invariants (per TECH-design-resume.md):
- Complete contract → exit 0 (resumable=true).
- Sparse contract (missing any mandatory key) → exit 1.
- BLOCK contract (malformed JSON / wrong schema) → exit 2.
- pending_subagents semantics: contract at phase_a_locked with frozen spec
  but partial Phase B reports → resume into Phase B at the named pending
  sub-agents.

These tests run alongside the existing
`tests/test_amw_design_contract_validate.py` suite; both must pass after
this round.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "bin" / "amw-design-contract-validate.py"
TIMEOUT = 30


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _run(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the validator with the given args and return the result."""
    cmd = [sys.executable, str(SCRIPT), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=TIMEOUT)


def _make_contract(**overrides: Any) -> dict[str, Any]:
    """Build a canonical PASS-shape contract; tests override specific keys.

    Every mandatory key required by `--check-resumable` is populated. To
    produce a sparse contract, tests delete or blank specific keys after
    calling this builder.
    """
    base: dict[str, Any] = {
        "meta": {
            "schema_version": "1",
            "contract_id": "20260527-resume-test",
            "created_at": "2026-05-27T10:00:00+02:00",
            "updated_at": "2026-05-27T11:00:00+02:00",
            "phase": "phase_a_locked",
        },
        "user_intent": {
            "project_name": "Resume Test Project",
            "industry": "hospitality / wellness",
            "primary_audience": "couples 35-55 booking weekend retreats",
            "primary_action": "book a weekend package",
            "tone": "calm, luxurious",
            "reference_urls": ["https://example.com"],
            "success_metrics": ["bookings/visitor >= 3%"],
        },
        "brand_tokens": {
            "primary_color": "#1A2A2E",
            "color_mode": "DARK",
            "display_font": "Cormorant Garamond",
            "body_font": "Inter",
            "border_radius_bucket": "ROUND_EIGHT",
            "neutral_palette": ["#0E1417", "#F5F2EC"],
            "preset_fingerprint": "luxury-dark-serif",
        },
        "ia": {
            "pages": [{"name": "Home", "slug": "/", "purpose": "convert"}],
            "primary_nav": ["Home"],
        },
        "legal": {
            "jurisdictions": ["IT", "EU"],
            "mandatories": ["GDPR cookie banner"],
        },
        "target_stack": {
            "framework": "shadcn+next",
            "css_strategy": "tailwind v4",
        },
        "decisions_log": [
            {
                "timestamp": "2026-05-27T10:18:42+02:00",
                "decision": "Approved Variant B at satisfaction gate.",
                "actor": "user",
            },
        ],
    }
    # Apply overrides (shallow per top-level section).
    for key, value in overrides.items():
        base[key] = value
    return base


def _write_contract(tmp_path: Path, contract: dict[str, Any], name: str = "contract.json") -> Path:
    """Persist a contract dict to tmp_path/name and return the file path."""
    contract_path = tmp_path / name
    contract_path.write_text(json.dumps(contract, indent=2), encoding="utf-8")
    return contract_path


# ---------------------------------------------------------------------
# Tests — complete contract is resumable
# ---------------------------------------------------------------------

def test_resumable_flag_exists_and_help_text_mentions_it() -> None:
    """The --check-resumable flag must be present in --help output."""
    result = _run("--help")
    assert result.returncode == 0
    # The help message must advertise the new flag so wrappers/agents can
    # discover it without reading source.
    assert "--check-resumable" in result.stdout, (
        f"--check-resumable flag is missing from --help output:\n{result.stdout}"
    )


def test_complete_contract_is_resumable_exit_zero(tmp_path: Path) -> None:
    """A canonical PASS-shape contract returns resumable=true / exit 0."""
    contract_path = _write_contract(tmp_path, _make_contract())
    result = _run(str(contract_path), "--check-resumable")
    assert result.returncode == 0, (
        f"Complete contract should be resumable (exit 0); got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_complete_contract_resumable_json_output(tmp_path: Path) -> None:
    """--check-resumable + --json emits a parseable structured payload."""
    contract_path = _write_contract(tmp_path, _make_contract())
    result = _run(str(contract_path), "--check-resumable", "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert "resumable" in payload, f"Missing 'resumable' key in JSON: {payload}"
    assert payload["resumable"] is True
    # The full validator findings must remain present so the agent can
    # surface FLAGs even on a resumable contract.
    assert "findings" in payload


# ---------------------------------------------------------------------
# Tests — sparse contracts (missing mandatory keys) are NOT resumable
# ---------------------------------------------------------------------

def test_missing_decisions_log_is_not_resumable(tmp_path: Path) -> None:
    """An empty decisions_log means no lock decision; not resumable."""
    contract = _make_contract()
    contract["decisions_log"] = []
    contract_path = _write_contract(tmp_path, contract)
    result = _run(str(contract_path), "--check-resumable")
    # Exit 1 means "needs more elicitation" — distinct from BLOCK (exit 2).
    assert result.returncode == 1, (
        f"Empty decisions_log should yield exit 1 (sparse), got {result.returncode}\n"
        f"stdout:\n{result.stdout}"
    )


def test_missing_user_intent_field_blanks_resumability(tmp_path: Path) -> None:
    """An empty required user_intent field blocks resumability AT THE BLOCK level.

    The underlying validator BLOCKs on empty required fields (B030). Since
    that is BLOCK, --check-resumable surfaces exit 2 — the contract is
    malformed, repair before retry, not "treat as sparse".
    """
    contract = _make_contract()
    contract["user_intent"]["project_name"] = ""
    contract_path = _write_contract(tmp_path, contract)
    result = _run(str(contract_path), "--check-resumable")
    assert result.returncode == 2, (
        f"Empty required field should be BLOCK (exit 2), got {result.returncode}\n"
        f"stdout:\n{result.stdout}"
    )


def test_missing_brand_token_blocks_resumability(tmp_path: Path) -> None:
    """An empty required brand_token field is BLOCK (exit 2)."""
    contract = _make_contract()
    contract["brand_tokens"]["primary_color"] = ""
    contract_path = _write_contract(tmp_path, contract)
    result = _run(str(contract_path), "--check-resumable")
    assert result.returncode == 2


def test_phase_a_discovery_with_empty_log_is_sparse(tmp_path: Path) -> None:
    """phase_a_discovery + empty log = fresh-start signal, not resumable."""
    contract = _make_contract()
    contract["meta"]["phase"] = "phase_a_discovery"
    contract["decisions_log"] = []
    contract_path = _write_contract(tmp_path, contract)
    result = _run(str(contract_path), "--check-resumable")
    # Sparse = exit 1 (treat as Phase A seed).
    assert result.returncode == 1


# ---------------------------------------------------------------------
# Tests — pending_subagents semantics (contract describes Phase B state)
# ---------------------------------------------------------------------

def test_phase_b_contract_with_decisions_is_resumable(tmp_path: Path) -> None:
    """A contract advanced to phase_b with a populated log is resumable.

    The resume-agent will then check the disk for completed/pending Phase B
    reports and recommend resume at the next pending sub-agent. The
    validator itself only confirms the contract has enough state.
    """
    contract = _make_contract()
    contract["meta"]["phase"] = "phase_b"
    contract["decisions_log"].append({
        "timestamp": "2026-05-27T12:00:00+02:00",
        "decision": "Fanned out to amw-wireframe-builder-agent.",
        "actor": "main-agent",
    })
    contract_path = _write_contract(tmp_path, contract)
    result = _run(str(contract_path), "--check-resumable")
    assert result.returncode == 0
    # JSON mode must include pending_subagents key (even if empty here —
    # the validator can't read disk; the resume-agent computes the actual
    # set difference). The validator's job is to confirm the contract
    # carries enough state to make that diff meaningful.
    json_result = _run(str(contract_path), "--check-resumable", "--json")
    payload = json.loads(json_result.stdout)
    assert payload["resumable"] is True
    # The payload always exposes resumable signal; pending_subagents
    # enumeration is the resume-agent's responsibility, not the
    # validator's, so it is NOT in the JSON (only the agent reads disk).
    # We assert the contract-level resume signal here.


# ---------------------------------------------------------------------
# Tests — non-resumable BLOCK cases (malformed contract)
# ---------------------------------------------------------------------

def test_malformed_json_blocks_resumability(tmp_path: Path) -> None:
    """Unparseable JSON exits 2 (BLOCK) even with --check-resumable."""
    bad = tmp_path / "bad.json"
    bad.write_text("{ not valid json", encoding="utf-8")
    result = _run(str(bad), "--check-resumable")
    assert result.returncode == 2, (
        f"Malformed JSON should be BLOCK (exit 2); got {result.returncode}"
    )


def test_schema_version_mismatch_blocks_resumability(tmp_path: Path) -> None:
    """A contract with wrong schema_version cannot be resumed."""
    contract = _make_contract()
    contract["meta"]["schema_version"] = "999"
    contract_path = _write_contract(tmp_path, contract)
    result = _run(str(contract_path), "--check-resumable")
    assert result.returncode == 2


def test_missing_file_exits_64_with_resumable_flag(tmp_path: Path) -> None:
    """A non-existent contract path is an invocation error, not BLOCK."""
    result = _run(str(tmp_path / "does-not-exist.json"), "--check-resumable")
    assert result.returncode == 64


# ---------------------------------------------------------------------
# Tests — backward compatibility (existing validator behavior unaffected)
# ---------------------------------------------------------------------

def test_existing_pass_fixture_still_passes_without_resumable_flag() -> None:
    """The PASS fixture must still exit 0 without --check-resumable."""
    fixtures = REPO_ROOT / "tests" / "fixtures"
    result = _run(str(fixtures / "contract-pass.json"))
    assert result.returncode == 0, "Existing PASS fixture broke"


def test_existing_flag_fixture_still_flags_without_resumable() -> None:
    """The FLAG fixture must still exit 1 (FLAG) without --check-resumable."""
    fixtures = REPO_ROOT / "tests" / "fixtures"
    result = _run(str(fixtures / "contract-flag.json"))
    assert result.returncode == 1, "Existing FLAG fixture broke"


def test_existing_block_fixture_still_blocks_without_resumable() -> None:
    """The BLOCK fixture must still exit 2 without --check-resumable."""
    fixtures = REPO_ROOT / "tests" / "fixtures"
    result = _run(str(fixtures / "contract-block.json"))
    assert result.returncode == 2, "Existing BLOCK fixture broke"


def test_resumable_flag_does_not_change_pass_to_block(tmp_path: Path) -> None:
    """A PASS contract stays exit 0 whether --check-resumable is on or off."""
    contract_path = _write_contract(tmp_path, _make_contract())
    without = _run(str(contract_path))
    with_flag = _run(str(contract_path), "--check-resumable")
    assert without.returncode == 0
    assert with_flag.returncode == 0


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
