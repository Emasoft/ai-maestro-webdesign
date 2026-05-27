#!/usr/bin/env python3
"""
amw-design-contract-validate.py — Persistent Design Contract validator.

Implements the BLOCK / FLAG / PASS severity model from
design-forge's `references/contract-validator.md` (MIT, direct-port),
adapted to the AMW Persistent Design Contract schema documented at
`skills/amw-design-md/references/TECH-design-contract.md`.

The Persistent Design Contract is a JSON document the orchestrator
(`ai-maestro-webdesign-main-agent`) maintains across an entire session:
it carries user requirements + locked design decisions through Phase A
discovery and into every Phase B sub-agent call. This validator is the
mechanical gate that decides whether a contract is ready for Phase B.

Severity model
--------------
* PASS  — every required field present, every advisory field strong;
          exit 0.
* FLAG  — every required field present, but one or more advisory
          (weak / empty / inconsistent) fields warrant follow-up;
          exit 1.
* BLOCK — at least one hard rule violated (missing required field,
          malformed JSON, schema-version mismatch, contradictory hard
          constraints, fingerprint impossible to enforce); exit 2.

Usage
-----
    python3 bin/amw-design-contract-validate.py <CONTRACT.json>
    python3 bin/amw-design-contract-validate.py <CONTRACT.json> --json
    python3 bin/amw-design-contract-validate.py <CONTRACT.json> --strict-flags

Exit codes
----------
    0  PASS — contract is clean, Phase B may proceed.
    1  FLAG — Phase B may proceed but orchestrator should ask the
       user about flagged fields first.
    2  BLOCK — Phase B MUST NOT proceed. Contract is malformed,
       missing required fields, or self-contradictory.
   64  Invocation error (bad CLI arguments, file not found).

Stdlib only. No PyYAML, no requests, no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# The schema version this validator understands. Contracts that
# declare a different `schema_version` are BLOCKed so older / newer
# orchestrators do not silently accept incompatible documents.
SUPPORTED_SCHEMA_VERSION = "1"

# Sections every contract MUST contain to be considered well-formed.
# Missing or non-dict values BLOCK.
REQUIRED_TOP_LEVEL_SECTIONS = (
    "meta",
    "user_intent",
    "brand_tokens",
    "ia",
    "legal",
    "target_stack",
    "decisions_log",
)

# Required fields inside `meta`. Missing values BLOCK.
REQUIRED_META_FIELDS = (
    "schema_version",
    "contract_id",
    "created_at",
    "updated_at",
    "phase",
)

# Phase values the contract validator recognises. Anything else BLOCKs.
VALID_PHASES = ("phase_a_discovery", "phase_a_lowfi", "phase_a_locked", "phase_b")

# Required fields inside `user_intent`. Empty strings here BLOCK — the
# orchestrator must elicit at least one sentence per slot before the
# contract can be considered viable.
REQUIRED_USER_INTENT_FIELDS = (
    "project_name",
    "industry",
    "primary_audience",
    "primary_action",
    "tone",
)

# Required fields inside `brand_tokens`. These are the minimum a Phase B
# sub-agent needs to render anything resembling the user's brand.
REQUIRED_BRAND_TOKEN_FIELDS = (
    "primary_color",
    "color_mode",
    "display_font",
    "body_font",
    "border_radius_bucket",
)

# Required fields inside `ia` (information architecture).
REQUIRED_IA_FIELDS = ("pages", "primary_nav")

# Required fields inside `target_stack`.
REQUIRED_TARGET_STACK_FIELDS = ("framework",)

# Legal `mandatories` is an array; empty is acceptable (no mandates apply).
# `jurisdictions` is required even if empty.
REQUIRED_LEGAL_FIELDS = ("jurisdictions", "mandatories")

# Border-radius buckets mirror the design-forge spec exactly: ROUND_FOUR,
# ROUND_EIGHT, ROUND_TWELVE, ROUND_FULL. We accept the design-forge
# canonical spellings AND the lowercase / numeric shorthand the AMW
# orchestrator may emit.
VALID_RADIUS_BUCKETS = {
    "ROUND_FOUR", "ROUND_EIGHT", "ROUND_TWELVE", "ROUND_FULL",
    "round_four", "round_eight", "round_twelve", "round_full",
    "4px", "8px", "12px", "9999px", "full",
}

VALID_COLOR_MODES = {"LIGHT", "DARK", "light", "dark"}

# Hex color regex — accepts #RGB, #RRGGBB, #RRGGBBAA.
HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

# ISO-8601 datetime regex (lenient — accepts both `Z` and `±HH:MM` offset).
ISO_DT_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})$"
)


# ---------------------------------------------------------------------
# Finding model
# ---------------------------------------------------------------------

class Finding:
    """One validation observation. Severity drives exit code aggregation."""

    __slots__ = ("severity", "code", "message", "path")

    def __init__(self, severity: str, code: str, message: str, path: str = "") -> None:
        # severity must be one of: BLOCK, FLAG, PASS.
        # path is a dotted JSON-pointer-like locator into the contract,
        # e.g. "brand_tokens.primary_color", "ia.pages[2].name".
        self.severity = severity
        self.code = code
        self.message = message
        self.path = path

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


# ---------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------

def load_contract(contract_path: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    """Read + parse the contract JSON. Returns (contract_or_None, findings).

    A malformed JSON file or a file whose top-level is not a JSON object
    produces a single BLOCK finding and a None contract.
    """
    findings: list[Finding] = []
    try:
        raw = contract_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        findings.append(Finding(
            "BLOCK", "B001",
            f"Contract file not found: {contract_path}",
            path="",
        ))
        return None, findings
    except OSError as exc:
        # E.g. permission denied. Surface verbatim so the orchestrator
        # can act on it without re-running.
        findings.append(Finding(
            "BLOCK", "B002",
            f"Cannot read contract file: {exc}",
            path="",
        ))
        return None, findings

    try:
        contract = json.loads(raw)
    except json.JSONDecodeError as exc:
        findings.append(Finding(
            "BLOCK", "B003",
            f"Malformed JSON: {exc.msg} at line {exc.lineno} col {exc.colno}",
            path="",
        ))
        return None, findings

    if not isinstance(contract, dict):
        findings.append(Finding(
            "BLOCK", "B004",
            f"Top-level JSON must be an object; got {type(contract).__name__}",
            path="",
        ))
        return None, findings

    return contract, findings


# ---------------------------------------------------------------------
# Section-level checks
# ---------------------------------------------------------------------

def check_top_level_shape(contract: dict[str, Any]) -> list[Finding]:
    """Every contract MUST be a JSON object with the canonical sections."""
    findings: list[Finding] = []
    for section in REQUIRED_TOP_LEVEL_SECTIONS:
        if section not in contract:
            findings.append(Finding(
                "BLOCK", "B010",
                f"Required section `{section}` is missing.",
                path=section,
            ))
        elif not isinstance(contract[section], (dict, list)):
            # decisions_log is the only list-shaped section; everything
            # else is a dict.
            expected = "list" if section == "decisions_log" else "object"
            actual = type(contract[section]).__name__
            findings.append(Finding(
                "BLOCK", "B011",
                f"Section `{section}` must be a JSON {expected}; got {actual}.",
                path=section,
            ))
    return findings


def check_meta(meta: Any) -> list[Finding]:
    """`meta` MUST contain schema_version=1, IDs, timestamps, and phase."""
    findings: list[Finding] = []
    if not isinstance(meta, dict):
        # Already reported at top-level; do not double-emit.
        return findings

    for field in REQUIRED_META_FIELDS:
        if field not in meta:
            findings.append(Finding(
                "BLOCK", "B020",
                f"meta.{field} is missing.",
                path=f"meta.{field}",
            ))
            continue
        if meta[field] in (None, ""):
            findings.append(Finding(
                "BLOCK", "B021",
                f"meta.{field} is empty.",
                path=f"meta.{field}",
            ))

    # schema_version mismatch is a hard BLOCK — never silently accept.
    if str(meta.get("schema_version", "")) != SUPPORTED_SCHEMA_VERSION:
        findings.append(Finding(
            "BLOCK", "B022",
            f"meta.schema_version must be '{SUPPORTED_SCHEMA_VERSION}'; got "
            f"'{meta.get('schema_version')}'.",
            path="meta.schema_version",
        ))

    # Phase must be a recognised lifecycle value.
    phase = meta.get("phase")
    if phase and phase not in VALID_PHASES:
        findings.append(Finding(
            "BLOCK", "B023",
            f"meta.phase must be one of {VALID_PHASES}; got '{phase}'.",
            path="meta.phase",
        ))

    # Timestamps: lenient but must look like ISO-8601.
    for ts_field in ("created_at", "updated_at"):
        ts = meta.get(ts_field)
        if isinstance(ts, str) and ts and not ISO_DT_RE.match(ts):
            findings.append(Finding(
                "FLAG", "F020",
                f"meta.{ts_field} should be ISO-8601 with TZ offset; got '{ts}'.",
                path=f"meta.{ts_field}",
            ))

    return findings


def check_user_intent(user_intent: Any) -> list[Finding]:
    """`user_intent` carries the human-readable brief the contract is built from."""
    findings: list[Finding] = []
    if not isinstance(user_intent, dict):
        return findings

    for field in REQUIRED_USER_INTENT_FIELDS:
        val = user_intent.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            findings.append(Finding(
                "BLOCK", "B030",
                f"user_intent.{field} is missing or empty.",
                path=f"user_intent.{field}",
            ))

    # Free-form `reference_urls` is advisory but very helpful — FLAG when absent.
    refs = user_intent.get("reference_urls", [])
    if not refs:
        findings.append(Finding(
            "FLAG", "F030",
            "user_intent.reference_urls is empty — orchestrator should ask for "
            "competitor / inspiration URLs to ground the design.",
            path="user_intent.reference_urls",
        ))

    # `success_metrics` is advisory but absence is a known cause of post-ship
    # disagreement; FLAG so the orchestrator surfaces the gap.
    metrics = user_intent.get("success_metrics", [])
    if not metrics:
        findings.append(Finding(
            "FLAG", "F031",
            "user_intent.success_metrics is empty — orchestrator should "
            "elicit at least one measurable goal.",
            path="user_intent.success_metrics",
        ))

    return findings


def check_brand_tokens(brand_tokens: Any) -> list[Finding]:
    """`brand_tokens` must carry the minimum a Phase B agent needs to render."""
    findings: list[Finding] = []
    if not isinstance(brand_tokens, dict):
        return findings

    for field in REQUIRED_BRAND_TOKEN_FIELDS:
        val = brand_tokens.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            findings.append(Finding(
                "BLOCK", "B040",
                f"brand_tokens.{field} is missing or empty.",
                path=f"brand_tokens.{field}",
            ))

    # Primary color must be a hex string.
    pc = brand_tokens.get("primary_color")
    if isinstance(pc, str) and pc and not HEX_RE.match(pc):
        findings.append(Finding(
            "BLOCK", "B041",
            f"brand_tokens.primary_color must be hex (#RGB / #RRGGBB / "
            f"#RRGGBBAA); got '{pc}'.",
            path="brand_tokens.primary_color",
        ))

    # Color mode must be in the canonical set.
    cm = brand_tokens.get("color_mode")
    if isinstance(cm, str) and cm and cm not in VALID_COLOR_MODES:
        findings.append(Finding(
            "BLOCK", "B042",
            f"brand_tokens.color_mode must be one of {sorted(VALID_COLOR_MODES)}; "
            f"got '{cm}'.",
            path="brand_tokens.color_mode",
        ))

    # Border-radius bucket must be canonical.
    rb = brand_tokens.get("border_radius_bucket")
    if isinstance(rb, str) and rb and rb not in VALID_RADIUS_BUCKETS:
        findings.append(Finding(
            "BLOCK", "B043",
            f"brand_tokens.border_radius_bucket must be one of "
            f"{sorted(VALID_RADIUS_BUCKETS)}; got '{rb}'.",
            path="brand_tokens.border_radius_bucket",
        ))

    # Neutral palette is advisory but absence is a known cause of Phase B
    # producing thin / under-specified layouts.
    if not brand_tokens.get("neutral_palette"):
        findings.append(Finding(
            "FLAG", "F040",
            "brand_tokens.neutral_palette is empty — Phase B will fall back "
            "to a generic gray ramp.",
            path="brand_tokens.neutral_palette",
        ))

    # Preset fingerprint is the design-forge identity-check hook. Absence is
    # advisory but reduces validator power downstream.
    if not brand_tokens.get("preset_fingerprint"):
        findings.append(Finding(
            "FLAG", "F041",
            "brand_tokens.preset_fingerprint is empty — without it, the "
            "contract validator cannot enforce identity checks.",
            path="brand_tokens.preset_fingerprint",
        ))

    return findings


def check_ia(ia: Any) -> list[Finding]:
    """`ia` describes pages and primary navigation."""
    findings: list[Finding] = []
    if not isinstance(ia, dict):
        return findings

    for field in REQUIRED_IA_FIELDS:
        if field not in ia:
            findings.append(Finding(
                "BLOCK", "B050",
                f"ia.{field} is missing.",
                path=f"ia.{field}",
            ))
            continue
        val = ia[field]
        if not isinstance(val, list):
            findings.append(Finding(
                "BLOCK", "B051",
                f"ia.{field} must be a list; got {type(val).__name__}.",
                path=f"ia.{field}",
            ))
            continue
        if not val:
            findings.append(Finding(
                "BLOCK", "B052",
                f"ia.{field} is empty — at least one entry required.",
                path=f"ia.{field}",
            ))

    return findings


def check_legal(legal: Any) -> list[Finding]:
    """`legal` lists jurisdictions and mandatory legal elements."""
    findings: list[Finding] = []
    if not isinstance(legal, dict):
        return findings

    for field in REQUIRED_LEGAL_FIELDS:
        if field not in legal:
            findings.append(Finding(
                "BLOCK", "B060",
                f"legal.{field} is missing (use [] when none apply).",
                path=f"legal.{field}",
            ))
            continue
        if not isinstance(legal[field], list):
            findings.append(Finding(
                "BLOCK", "B061",
                f"legal.{field} must be a list; got "
                f"{type(legal[field]).__name__}.",
                path=f"legal.{field}",
            ))

    # If jurisdictions are listed but mandatories is empty, the orchestrator
    # should consult `amw-legal-expert-agent` before Phase B.
    jurisdictions = legal.get("jurisdictions", [])
    mandatories = legal.get("mandatories", [])
    if (isinstance(jurisdictions, list) and jurisdictions
            and isinstance(mandatories, list) and not mandatories):
        findings.append(Finding(
            "FLAG", "F060",
            f"legal.jurisdictions lists {len(jurisdictions)} jurisdiction(s) "
            "but legal.mandatories is empty — consult amw-legal-expert-agent "
            "to confirm.",
            path="legal.mandatories",
        ))

    return findings


def check_target_stack(target_stack: Any) -> list[Finding]:
    """`target_stack.framework` is the only required field."""
    findings: list[Finding] = []
    if not isinstance(target_stack, dict):
        return findings

    for field in REQUIRED_TARGET_STACK_FIELDS:
        val = target_stack.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            findings.append(Finding(
                "BLOCK", "B070",
                f"target_stack.{field} is missing or empty.",
                path=f"target_stack.{field}",
            ))

    if not target_stack.get("css_strategy"):
        findings.append(Finding(
            "FLAG", "F070",
            "target_stack.css_strategy is empty — Phase B will default to "
            "vanilla CSS unless tailwind/shadcn is inferred.",
            path="target_stack.css_strategy",
        ))

    return findings


def check_decisions_log(decisions_log: Any) -> list[Finding]:
    """`decisions_log` is the append-only history of locked choices."""
    findings: list[Finding] = []
    if not isinstance(decisions_log, list):
        return findings

    if not decisions_log:
        # An empty decisions log is allowed pre-Phase-A but the orchestrator
        # should NEVER hand a Phase-B-ready contract to a sub-agent with an
        # empty log — every locked decision is a row.
        findings.append(Finding(
            "FLAG", "F080",
            "decisions_log is empty — Phase B sub-agents expect at least the "
            "Phase A locking decision to be recorded.",
            path="decisions_log",
        ))
        return findings

    # Each entry should be an object with at minimum `timestamp` + `decision`.
    for idx, entry in enumerate(decisions_log):
        if not isinstance(entry, dict):
            findings.append(Finding(
                "BLOCK", "B080",
                f"decisions_log[{idx}] must be an object; got "
                f"{type(entry).__name__}.",
                path=f"decisions_log[{idx}]",
            ))
            continue
        for k in ("timestamp", "decision"):
            if k not in entry or not entry[k]:
                findings.append(Finding(
                    "BLOCK", "B081",
                    f"decisions_log[{idx}].{k} is missing or empty.",
                    path=f"decisions_log[{idx}].{k}",
                ))

    return findings


def check_cross_section_consistency(contract: dict[str, Any]) -> list[Finding]:
    """Catch contradictions across sections (BLOCK on hard contradictions)."""
    findings: list[Finding] = []

    _ui = contract.get("user_intent")
    user_intent: dict[str, Any] = _ui if isinstance(_ui, dict) else {}
    _bt = contract.get("brand_tokens")
    brand_tokens: dict[str, Any] = _bt if isinstance(_bt, dict) else {}

    # If user_intent.tone declares "luxury" but brand_tokens.color_mode is
    # LIGHT with neon primary, that's not a hard BLOCK but worth a FLAG.
    tone = (user_intent.get("tone") or "").lower()
    color_mode = (brand_tokens.get("color_mode") or "").upper()
    if "luxury" in tone and color_mode == "LIGHT":
        findings.append(Finding(
            "FLAG", "F090",
            "user_intent.tone mentions 'luxury' but brand_tokens.color_mode "
            "is LIGHT — design-forge convention is DARK for luxury presets; "
            "confirm with the user.",
            path="brand_tokens.color_mode",
        ))

    # Hard contradiction: legal.mandatories contains a "cookie banner"
    # directive but target_stack.framework is "email-mjml" — emails don't
    # have cookie banners.
    _lg = contract.get("legal")
    legal: dict[str, Any] = _lg if isinstance(_lg, dict) else {}
    _ts = contract.get("target_stack")
    target_stack: dict[str, Any] = _ts if isinstance(_ts, dict) else {}
    _md = legal.get("mandatories", [])
    mandatories: list[Any] = _md if isinstance(_md, list) else []
    framework = (target_stack.get("framework") or "").lower()
    if framework.startswith("email") and any(
        isinstance(m, str) and "cookie" in m.lower() for m in mandatories
    ):
        findings.append(Finding(
            "BLOCK", "B090",
            "legal.mandatories includes a cookie-banner directive but "
            "target_stack.framework is an email stack — emails cannot host "
            "cookie banners. Resolve the contradiction before Phase B.",
            path="legal.mandatories",
        ))

    return findings


# ---------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------

def validate(contract_path: Path) -> tuple[str, list[Finding]]:
    """Run every check in order. Returns (verdict, findings).

    Verdict is BLOCK / FLAG / PASS, aggregated as:
      * any BLOCK finding  -> BLOCK
      * else any FLAG      -> FLAG
      * else               -> PASS
    """
    contract, findings = load_contract(contract_path)
    if contract is None:
        return "BLOCK", findings

    findings.extend(check_top_level_shape(contract))
    # If the top-level shape is broken, stop here so we don't emit cascade
    # findings against missing sections.
    if any(f.severity == "BLOCK" and f.code in ("B010", "B011") for f in findings):
        return "BLOCK", findings

    findings.extend(check_meta(contract.get("meta")))
    findings.extend(check_user_intent(contract.get("user_intent")))
    findings.extend(check_brand_tokens(contract.get("brand_tokens")))
    findings.extend(check_ia(contract.get("ia")))
    findings.extend(check_legal(contract.get("legal")))
    findings.extend(check_target_stack(contract.get("target_stack")))
    findings.extend(check_decisions_log(contract.get("decisions_log")))
    findings.extend(check_cross_section_consistency(contract))

    if any(f.severity == "BLOCK" for f in findings):
        return "BLOCK", findings
    if any(f.severity == "FLAG" for f in findings):
        return "FLAG", findings
    return "PASS", findings


# ---------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------

def emit_human(verdict: str, findings: list[Finding], contract_path: Path) -> None:
    """Pretty-print the verdict + findings to stdout."""
    print(f"Contract: {contract_path}")
    print(f"Verdict:  {verdict}")
    print(f"Findings: {len(findings)}")
    blocks = [f for f in findings if f.severity == "BLOCK"]
    flags = [f for f in findings if f.severity == "FLAG"]
    if blocks:
        print("\nBLOCK:")
        for f in blocks:
            loc = f" @ {f.path}" if f.path else ""
            print(f"  [{f.code}]{loc}  {f.message}")
    if flags:
        print("\nFLAG:")
        for f in flags:
            loc = f" @ {f.path}" if f.path else ""
            print(f"  [{f.code}]{loc}  {f.message}")
    if not blocks and not flags:
        print("\nAll checks PASS.")


def emit_json(verdict: str, findings: list[Finding], contract_path: Path) -> None:
    """Emit a machine-readable JSON summary."""
    payload = {
        "contract": str(contract_path),
        "verdict": verdict,
        "findings": [f.to_dict() for f in findings],
    }
    print(json.dumps(payload, indent=2))


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="amw-design-contract-validate.py",
        description="Validate a Persistent Design Contract (BLOCK / FLAG / PASS).",
    )
    parser.add_argument(
        "contract",
        type=Path,
        help="Path to the contract JSON file.",
    )
    parser.add_argument(
        "--json",
        dest="emit_json",
        action="store_true",
        help="Emit findings as JSON (for orchestrator consumption).",
    )
    parser.add_argument(
        "--strict-flags",
        dest="strict_flags",
        action="store_true",
        help="Treat FLAG as BLOCK (exit 2 instead of 1).",
    )
    args = parser.parse_args(argv)

    if not args.contract.exists():
        # Surface a CLI-level error distinct from BLOCK so wrappers can
        # tell "you gave me a bad path" apart from "the contract is bad".
        print(f"ERROR: contract file not found: {args.contract}", file=sys.stderr)
        return 64

    verdict, findings = validate(args.contract)
    if args.emit_json:
        emit_json(verdict, findings, args.contract)
    else:
        emit_human(verdict, findings, args.contract)

    if verdict == "BLOCK":
        return 2
    if verdict == "FLAG":
        return 2 if args.strict_flags else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
