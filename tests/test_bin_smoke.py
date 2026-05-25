"""Smoke tests for every Python script in the plugin's bin/ directory.

Two parametrized checks, run against the dynamically-discovered set of
``bin/*.py`` scripts (no hardcoded list — new scripts are auto-covered):

1. ``test_python_script_imports_clean`` — every script byte-compiles without
   a SyntaxError (catches parse/syntax regressions across the whole bin/ set).
2. ``test_cli_help_exits_zero`` — every script that uses argparse responds to
   ``--help`` with returncode 0 and a usage line. Scripts with no CLI are
   skipped with an explicit reason.

Both checks run each script in a *fresh subprocess* (never a top-level import),
so collection itself triggers no side effects from scripts that do work at
import time. Real invocations only — no mocks.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

# bin/ sits next to tests/ at the plugin root. Resolve relative to THIS file
# so the suite works regardless of the pytest invocation cwd.
BIN_DIR = Path(__file__).resolve().parent.parent / "bin"

# Discover scripts once, at collection time, sorted for deterministic param
# ordering and stable test IDs across machines.
BIN_PY_SCRIPTS: list[Path] = sorted(BIN_DIR.glob("*.py"))

# Per-script subprocess timeout. --help on an argparse script returns
# instantly; this only guards against a script that hangs (e.g. starts a
# server) instead of printing help and exiting.
HELP_TIMEOUT_SECONDS = 30


def _uses_argparse(script: Path) -> bool:
    """True if the script's source text references argparse / add_argument.

    Read as text, never imported — importing would run module-level code and
    defeat the point of a subprocess-isolated smoke test.
    """
    source = script.read_text(encoding="utf-8", errors="replace")
    return "argparse" in source or "add_argument" in source


# Fail loudly at collection time if bin/ vanished or holds no scripts — a
# silent "0 collected" would otherwise masquerade as a green run.
if not BIN_PY_SCRIPTS:
    raise RuntimeError(f"No bin/*.py scripts discovered under {BIN_DIR} — check the path")


@pytest.mark.parametrize("script", BIN_PY_SCRIPTS, ids=lambda p: p.name)
def test_python_script_imports_clean(script: Path) -> None:
    """Every bin/*.py byte-compiles without a SyntaxError."""
    # py_compile.compile(doraise=True) raises PyCompileError on a SyntaxError
    # but does NOT execute the module body, so import-time side effects never
    # fire. Run it in a child interpreter so a hard crash can't take the
    # test process down with it.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import py_compile, sys; py_compile.compile(sys.argv[1], doraise=True)",
            str(script),
        ],
        capture_output=True,
        text=True,
        timeout=HELP_TIMEOUT_SECONDS,
    )
    assert result.returncode == 0, (
        f"{script.name} failed to compile:\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )


@pytest.mark.parametrize("script", BIN_PY_SCRIPTS, ids=lambda p: p.name)
def test_cli_help_exits_zero(script: Path) -> None:
    """argparse-based bin/*.py exit 0 on --help and print a usage line."""
    if not _uses_argparse(script):
        pytest.skip(f"{script.name} has no argparse CLI — no --help to test")

    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        timeout=HELP_TIMEOUT_SECONDS,
    )
    assert result.returncode == 0, (
        f"{script.name} --help exited {result.returncode}:\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    # argparse prints the auto-generated help (with a 'usage:' line) to stdout
    # when --help is requested. Assert it landed there, lowercased for safety.
    assert "usage" in result.stdout.lower(), (
        f"{script.name} --help produced no 'usage' line on stdout:\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
