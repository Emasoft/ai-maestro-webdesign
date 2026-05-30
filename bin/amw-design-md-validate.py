#!/usr/bin/env python3
"""
amw-design-md-validate.py — Pure-Python validator for DESIGN.md.

Implements the structural and token-quality checks from canonical-spec-google-alpha.md
and community-9-section-spec.md. Runs offline (no npx, no network) so it works in
environments where the official linter is not available, and runs the V2-specific
checks the official linter does not understand.

Usage:
    python3 bin/amw-design-md-validate.py <DESIGN.md> [--variant 1|2|auto] [--json] [--check-references]

Exit codes:
    0  validation passes
    1  validation errors found
    2  invocation error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# YAML is the only optional dep; the script falls back to a tolerant parser if PyYAML is absent.
try:
    import yaml  # type: ignore
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# Variant 1 canonical sections (per spec.md L82-L92)
V1_SECTIONS = [
    ("Overview", "Brand & Style"),
    ("Colors",),
    ("Typography",),
    ("Layout", "Layout & Spacing"),
    ("Elevation & Depth", "Elevation"),
    ("Shapes",),
    ("Components",),
    ("Do's and Don'ts", "Dos and Donts"),
]

# Variant 2 9-section format (per community-9-section-spec.md)
V2_SECTIONS = [
    "Visual Theme & Atmosphere",
    "Color Palette & Roles",
    "Typography Rules",
    "Component Stylings",
    "Layout Principles",
    "Depth & Elevation",
    "Do's and Don'ts",
    "Responsive Behavior",
    "Agent Prompt Guide",
]


HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
DIMENSION_RE = re.compile(r"^[0-9.]+(px|em|rem)$|^calc\(.*\)$")
TOKEN_REF_RE = re.compile(r"^\{([a-zA-Z0-9._-]+)\}$")


class Finding:
    def __init__(self, severity: str, code: str, message: str, line: int | None = None):
        self.severity = severity      # P0 | P1 | P2 | warn
        self.code = code              # S1, T1, R1, A1, etc.
        self.message = message
        self.line = line

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "line": self.line,
        }

    def __str__(self) -> str:
        loc = f"L{self.line}: " if self.line else ""
        return f"[{self.severity}/{self.code}] {loc}{self.message}"


def detect_variant(content: str) -> int:
    """Inspect the file head and return 1 (canonical) or 2 (community)."""
    lines = content.splitlines()
    if not lines:
        return 1
    first = lines[0].strip()
    # Variant 1: starts with --- frontmatter
    if first == "---":
        return 1
    # Variant 2: starts with `# Design System Inspired by ...`
    if first.startswith("# Design System Inspired by"):
        return 2
    # Other: probably V1 with optional H1 title before frontmatter is invalid
    return 1


def split_frontmatter(content: str) -> tuple[str | None, str, int]:
    """Return (frontmatter_yaml_text, body_text, body_start_line)."""
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, content, 1

    # Find closing ---
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, content, 1

    fm = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    body_start_line = end_idx + 2  # 1-based: after closing ---
    return fm, body, body_start_line


def parse_yaml_safe(text: str) -> tuple[dict | None, str | None]:
    """Parse YAML; return (data, error_message). data is None on error."""
    if HAVE_YAML:
        try:
            return yaml.safe_load(text), None
        except yaml.YAMLError as e:
            return None, f"YAML parse error: {e}"
    # Fallback: very tolerant — only handles flat structures + 1 level of nesting
    # Used only when PyYAML isn't installed; we degrade rather than fail.
    return _parse_yaml_fallback(text)


def _parse_yaml_fallback(text: str) -> tuple[dict | None, str | None]:
    out: dict[str, Any] = {}
    current_key: str | None = None
    current_subkey: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        leading = len(line) - len(line.lstrip())
        stripped = line.strip()

        if leading == 0 and ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip('"\'')
            current_key = key
            current_subkey = None
            if val == "":
                out[key] = {}
            else:
                out[key] = val
        elif leading == 2 and current_key is not None and ":" in stripped:
            sk, _, sv = stripped.partition(":")
            sk = sk.strip()
            sv = sv.strip().strip('"\'')
            current_subkey = sk
            if sv == "":
                if not isinstance(out.get(current_key), dict):
                    out[current_key] = {}
                out[current_key][sk] = {}
            else:
                if not isinstance(out.get(current_key), dict):
                    out[current_key] = {}
                out[current_key][sk] = sv
        elif leading == 4 and current_key is not None and current_subkey is not None and ":" in stripped:
            sk, _, sv = stripped.partition(":")
            sk = sk.strip()
            sv = sv.strip().strip('"\'')
            parent = out.get(current_key, {}).get(current_subkey)
            if not isinstance(parent, dict):
                out[current_key][current_subkey] = {}
                parent = out[current_key][current_subkey]
            parent[sk] = sv
    return out, None


def find_section_headings(body: str, body_start_line: int) -> list[tuple[str, int]]:
    """Return list of (heading_text, absolute_line_number) for every ## heading."""
    out = []
    for i, line in enumerate(body.splitlines()):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            text = m.group(1).strip()
            # Strip leading "N. " for V2 numbered sections
            text_clean = re.sub(r"^\d+\.\s*", "", text)
            out.append((text_clean, body_start_line + i))
    return out


def section_matches(actual: str, expected_options: tuple[str, ...]) -> bool:
    actual_l = actual.lower().strip()
    return any(actual_l == opt.lower().strip() for opt in expected_options)


def validate_v1_structure(content: str, findings: list[Finding]) -> dict | None:
    """Return parsed frontmatter dict or None on hard error."""
    if not content.startswith("---"):
        findings.append(Finding("P0", "S1.V1", "Frontmatter must start at line 1 with ---", 1))
        return None

    fm_text, body, body_start = split_frontmatter(content)
    if fm_text is None:
        findings.append(Finding("P0", "S1.V1", "Frontmatter not properly closed (missing closing --- )", None))
        return None

    fm_data, err = parse_yaml_safe(fm_text)
    if err:
        findings.append(Finding("P0", "S2.V1", err, None))
        return None
    if fm_data is None:
        fm_data = {}

    # Required: name
    if "name" not in fm_data or not str(fm_data.get("name", "")).strip():
        findings.append(Finding("P1", "T8.V1", "Frontmatter missing required 'name' field", None))

    # Section order
    headings = find_section_headings(body, body_start)
    seen_indices = []
    for h_text, h_line in headings:
        for idx, options in enumerate(V1_SECTIONS):
            if section_matches(h_text, options):
                seen_indices.append((idx, h_line, h_text))
                break

    # Detect duplicates
    seen_set = set()
    for idx, line, h_text in seen_indices:
        if idx in seen_set:
            findings.append(Finding("P0", "S5.V1", f"Duplicate section heading: ## {h_text}", line))
        seen_set.add(idx)

    # Detect out-of-order
    last_idx = -1
    for idx, line, h_text in seen_indices:
        if idx < last_idx:
            findings.append(Finding("P0", "S4.V1", f"Section out of order: ## {h_text} appears after a later canonical section", line))
        last_idx = max(last_idx, idx)

    return fm_data


def validate_v1_tokens(fm: dict, findings: list[Finding]) -> None:
    # Color values
    colors = fm.get("colors") or {}
    if not isinstance(colors, dict):
        findings.append(Finding("P1", "T1", "colors: must be a map", None))
    else:
        for k, v in colors.items():
            if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
                continue  # token reference
            if not isinstance(v, str) or not HEX_RE.match(v):
                findings.append(Finding("P1", "T1", f"colors.{k}: invalid color value '{v}' (expected #xxxxxx hex)", None))

    # Typography rows
    typography = fm.get("typography") or {}
    if isinstance(typography, dict):
        for tname, trow in typography.items():
            if not isinstance(trow, dict):
                findings.append(Finding("P1", "T2", f"typography.{tname}: row must be a map", None))
                continue
            for required in ("fontFamily", "fontSize", "fontWeight", "lineHeight"):
                if required not in trow:
                    findings.append(Finding("P1", "T2", f"typography.{tname}: missing required field '{required}'", None))
            # fontWeight must be number 100-900 (or token-ref)
            fw = trow.get("fontWeight")
            if fw is not None and not (isinstance(fw, str) and fw.startswith("{")):
                try:
                    fw_int = int(fw)
                    if fw_int < 100 or fw_int > 900:
                        findings.append(Finding("P1", "T8", f"typography.{tname}.fontWeight {fw_int} out of 100-900 range", None))
                except (TypeError, ValueError):
                    findings.append(Finding("P1", "T8", f"typography.{tname}.fontWeight must be number 100-900, got '{fw}'", None))
            # fontSize must be Dimension
            fs = trow.get("fontSize")
            if fs is not None and not (isinstance(fs, str) and (DIMENSION_RE.match(str(fs)) or fs.startswith("{"))):
                findings.append(Finding("P1", "T1", f"typography.{tname}.fontSize '{fs}' missing px/em/rem unit", None))

    # Rounded
    rounded = fm.get("rounded") or {}
    if isinstance(rounded, dict):
        for k, v in rounded.items():
            if isinstance(v, str) and v.startswith("{"):
                continue
            if not isinstance(v, str) or not DIMENSION_RE.match(str(v)):
                findings.append(Finding("P1", "T1", f"rounded.{k}: '{v}' missing px/em/rem unit", None))

    # Spacing — accepts Dimension OR number
    spacing = fm.get("spacing") or {}
    if isinstance(spacing, dict):
        for k, v in spacing.items():
            if isinstance(v, str) and v.startswith("{"):
                continue
            if isinstance(v, (int, float)):
                continue  # bare number OK
            if not isinstance(v, str) or not DIMENSION_RE.match(str(v)):
                findings.append(Finding("P1", "T1", f"spacing.{k}: '{v}' must be Dimension (px/em/rem) or number", None))


def collect_token_paths(fm: dict) -> set[str]:
    """Walk the YAML tree and collect all dotted paths."""
    out = set()
    def walk(node: Any, prefix: str):
        if isinstance(node, dict):
            for k, v in node.items():
                path = f"{prefix}.{k}" if prefix else str(k)
                out.add(path)
                walk(v, path)
    walk(fm, "")
    return out


def validate_references(fm: dict, findings: list[Finding]) -> None:
    """Resolve all {path.to.token} references; report unresolved or scope violations."""
    available = collect_token_paths(fm)

    def check_node(node: Any, parent_path: str):
        if isinstance(node, str):
            m = TOKEN_REF_RE.match(node.strip())
            if m:
                ref_path = m.group(1)
                if ref_path not in available:
                    findings.append(Finding("P0", "R1", f"Unresolved reference {{{ref_path}}} at {parent_path}", None))
                else:
                    # Composite reference scope check: outside components.*, refs must point to primitives
                    if not parent_path.startswith("components."):
                        ref_value = _resolve_path(fm, ref_path)
                        if isinstance(ref_value, dict):
                            findings.append(Finding("P1", "R3", f"Composite reference {{{ref_path}}} not allowed at {parent_path}; must point to primitive", None))
        elif isinstance(node, dict):
            for k, v in node.items():
                child = f"{parent_path}.{k}" if parent_path else k
                check_node(v, child)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                check_node(v, f"{parent_path}[{i}]")

    check_node(fm, "")


def _resolve_path(fm: dict, path: str) -> Any:
    node: Any = fm
    for seg in path.split("."):
        if isinstance(node, dict) and seg in node:
            node = node[seg]
        else:
            return None
    return node


def validate_v2(content: str, findings: list[Finding]) -> None:
    lines = content.splitlines()
    if not lines or not lines[0].strip().startswith("# Design System Inspired by"):
        findings.append(Finding("P1", "S1.V2", "Variant 2 must start with '# Design System Inspired by ...'", 1))

    headings = []
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(?:(\d+)\.\s+)?(.+?)\s*$", line)
        if m:
            num = m.group(1)
            text = m.group(2).strip()
            headings.append((int(num) if num else None, text, i + 1))

    # Check the 9 numbered sections are all present
    seen_nums = {n for n, _, _ in headings if n is not None}
    for n, expected_name in enumerate(V2_SECTIONS, start=1):
        if n not in seen_nums:
            findings.append(Finding("P1", "S1.V2", f"Variant 2 section {n}. {expected_name} not found", None))

    # Check ordering of numbered sections
    last = 0
    for n, _t, ln in headings:
        if n is not None:
            if n < last:
                findings.append(Finding("P0", "S4.V2", f"V2 section {n}. out of order at line {ln}", ln))
            last = n

    # XML boundary tags (recommended; soft check)
    if "<context>" not in content:
        findings.append(Finding("P2", "S2.V2", "<context> XML boundary tag missing", None))
    if "<design_tokens>" not in content:
        findings.append(Finding("P2", "S2.V2", "<design_tokens> XML boundary tag missing", None))
    if "<constraints>" not in content:
        findings.append(Finding("P2", "S2.V2", "<constraints> XML boundary tag missing", None))

    # Mermaid block (soft)
    if "```mermaid" not in content:
        findings.append(Finding("P2", "S5.V2", "No mermaid block found (V2 typically has a state diagram in Section 4)", None))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a DESIGN.md file (Variant 1 or Variant 2).")
    parser.add_argument("path", help="Path to DESIGN.md")
    parser.add_argument("--variant", choices=["1", "2", "auto"], default="auto", help="Which variant to validate against (default: auto-detect)")
    parser.add_argument("--check-references", action="store_true", help="Resolve {path.to.token} references")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of plain text")
    args = parser.parse_args()

    p = Path(args.path)
    if not p.is_file():
        print(f"Error: file not found: {p}", file=sys.stderr)
        return 2

    content = p.read_text(encoding="utf-8")
    findings: list[Finding] = []

    if args.variant == "auto":
        variant = detect_variant(content)
    else:
        variant = int(args.variant)

    if variant == 1:
        fm = validate_v1_structure(content, findings)
        if fm is not None:
            validate_v1_tokens(fm, findings)
            # Reference validation ALWAYS runs. The original guard was
            # `if args.check_references or True:` — the `or True` deliberately
            # forced this check on regardless of the flag, so dangling
            # {path.to.token} references are caught by default. --check-references
            # is retained for back-compat but does not gate this (see
            # test_bad_tokens_fixture_fails_with_r1_per_reference). Calling
            # unconditionally preserves that behavior without the tautology.
            validate_references(fm, findings)
    else:
        validate_v2(content, findings)

    # Sort: P0 first, then P1, P2, warn
    severity_order = {"P0": 0, "P1": 1, "P2": 2, "warn": 3}
    findings.sort(key=lambda f: (severity_order.get(f.severity, 99), f.line or 0))

    has_errors = any(f.severity in ("P0", "P1") for f in findings)

    if args.json:
        out = {
            "file": str(p),
            "variant": variant,
            "verdict": "FAIL" if has_errors else "PASS",
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(out, indent=2))
    else:
        print(f"File: {p}")
        print(f"Variant: {variant}")
        print(f"Verdict: {'FAIL' if has_errors else 'PASS'}")
        print(f"Findings: {len(findings)}")
        for f in findings:
            print(f"  {f}")

    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
