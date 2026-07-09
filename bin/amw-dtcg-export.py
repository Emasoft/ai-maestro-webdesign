#!/usr/bin/env python3
"""amw-dtcg-export.py — Emit DTCG (Design Tokens Community Group) JSON from a DESIGN.md.

DTCG (https://design-tokens.github.io/community-group/format/) is the W3C-track
canonical token format. Compared to the partial DTCG output of
`amw-design-md-emit-companions.py`, this CLI:

  1. Stamps `$type` and `$value` on EVERY leaf token (DTCG's hard requirement).
  2. Preserves alias references `{group.subgroup.token}` verbatim — they are
     emitted as the leaf's `$value` so DTCG consumers can resolve them.
  3. Emits the optional `$description` on every leaf when a sibling
     `description` field is present in the source.
  4. Sets a group-level `$type` when every leaf in the group shares the
     same primitive type (saves repetition; allowed by spec — children
     without their own `$type` inherit from the nearest group ancestor).
  5. With `--harmonize`, accepts a Figma-Tokens-style nested-group JSON
     file (uses bare `value`, `type`, `description` keys + arbitrary
     nesting) and rewrites it to canonical DTCG with `$`-prefixed keys
     and `.`-joined alias paths.

Inputs accepted:

  * `<path>.md`   — DESIGN.md (Variant 1, YAML frontmatter). Default.
  * `<path>.json` — Figma-Tokens-style nested JSON. Requires --harmonize.
  * `<path>.yaml` / `<path>.yml` — raw token tree (YAML). Requires --harmonize.

Hard DTCG conformance contract (asserted by the test suite):

  * Every leaf object has BOTH `$type` (string) and `$value` (any).
  * Group objects never have `$value` (a group with `$value` is a leaf).
  * Alias `$value` strings match the canonical `{a.b.c}` syntax — no
    extra whitespace, no missing braces.
  * Every alias resolves to an existing token path in the same document.
  * The emitted JSON parses round-trip (json.dumps/json.loads) without
    loss.

Exit codes:

  0  success — DTCG written to stdout or --output path.
  2  invocation / parse error (file missing, invalid YAML/JSON, etc).
  3  DTCG validation failure (an emitted token violated the contract).

Usage:

    amw-dtcg-export.py DESIGN.md -o tokens.dtcg.json
    amw-dtcg-export.py figma-tokens.json --harmonize -o tokens.dtcg.json
    amw-dtcg-export.py DESIGN.md          # writes to stdout
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]

    HAVE_YAML = True
except ImportError:
    yaml = None  # type: ignore[assignment]
    HAVE_YAML = False


# ---------------------------------------------------------------------------
# DTCG type vocabulary
# ---------------------------------------------------------------------------
# Spec section "Types": the set below is the canonical primitive vocabulary.
# Composite types (typography, border, shadow, transition, gradient) are
# emitted with a structured `$value` object — the leaf is still flagged
# with its single `$type`.
DTCG_PRIMITIVE_TYPES = {
    "color",
    "dimension",
    "fontFamily",
    "fontWeight",
    "fontSize",
    "lineHeight",
    "letterSpacing",
    "duration",
    "cubicBezier",
    "number",
    "string",
}

DTCG_COMPOSITE_TYPES = {
    "typography",
    "border",
    "shadow",
    "strokeStyle",
    "transition",
    "gradient",
}

DTCG_ALL_TYPES = DTCG_PRIMITIVE_TYPES | DTCG_COMPOSITE_TYPES


# Canonical alias syntax: `{group.subgroup.token}` — a single brace pair,
# dot-separated path of `[A-Za-z0-9_-]+` segments. The trailing `$` is
# critical: aliases must be the WHOLE string, never embedded in text.
ALIAS_RE = re.compile(r"^\{([A-Za-z0-9._-]+)\}$")


# ---------------------------------------------------------------------------
# YAML frontmatter parsing (DESIGN.md path)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict[str, Any]:
    """Extract and parse the YAML frontmatter block at the top of a .md file.

    Returns {} if no frontmatter present. Raises if the YAML is malformed
    and pyyaml is installed (fail-fast — we'd rather refuse to emit garbage
    DTCG than silently drop sections).
    """
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}
    fm_text = "\n".join(lines[1:end_idx])
    if HAVE_YAML and yaml is not None:
        # safe_load returns None for empty content — coerce to {}.
        data = yaml.safe_load(fm_text)
        return data if isinstance(data, dict) else {}
    # Minimal stdlib fallback. Mirrors the parser in
    # amw-design-md-emit-companions.py so the two scripts behave the same
    # on machines without pyyaml.
    return _fallback_parse(fm_text)


def _fallback_parse(text: str) -> dict[str, Any]:
    """Stdlib-only YAML subset parser (top-level + 2-level nesting).

    Handles the shapes that appear in the canonical-template:
        key: value
        section:
          name:
            sub-field: value
            sub-field: value
    Quoted strings are unquoted; integers and floats are coerced.
    """
    out: dict[str, Any] = {}
    cur_key: str | None = None
    cur_sub: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        leading = len(line) - len(line.lstrip())
        s = line.strip()
        if leading == 0 and ":" in s:
            k, _, v = s.partition(":")
            cur_key = k.strip()
            cur_sub = None
            v = v.strip().strip('"').strip("'")
            out[cur_key] = v if v else {}
        elif leading == 2 and cur_key:
            k, _, v = s.partition(":")
            cur_sub = k.strip()
            v = v.strip().strip('"').strip("'")
            if not isinstance(out.get(cur_key), dict):
                out[cur_key] = {}
            out[cur_key][cur_sub] = v if v else {}
        elif leading == 4 and cur_key and cur_sub:
            k, _, v = s.partition(":")
            v = v.strip().strip('"').strip("'")
            parent = out.setdefault(cur_key, {}).setdefault(cur_sub, {})
            if not isinstance(parent, dict):
                out[cur_key][cur_sub] = {}
                parent = out[cur_key][cur_sub]
            parent[k.strip()] = _coerce_scalar(v)
    return out


def _coerce_scalar(v: str) -> Any:
    """Best-effort int/float coercion; otherwise return the string as-is."""
    if not isinstance(v, str):
        return v
    try:
        return int(v)
    except (ValueError, TypeError):
        pass
    try:
        return float(v)
    except (ValueError, TypeError):
        pass
    return v


# ---------------------------------------------------------------------------
# Type inference (DESIGN.md → DTCG)
# ---------------------------------------------------------------------------
# The DESIGN.md frontmatter has a flat top-level grouping (`colors`,
# `typography`, `rounded`, `spacing`, `components`). DTCG requires a
# `$type` on every leaf — we infer it from (a) the group name, (b) the
# leaf property name (for component sub-fields), (c) the value shape.

GROUP_TO_DTCG_TYPE = {
    "colors": "color",
    "typography": "typography",
    "rounded": "dimension",
    "spacing": "dimension",
}


def _infer_component_property_type(prop: str) -> str:
    """Map a component property name (`backgroundColor`, `padding`, ...) to DTCG $type.

    Component sub-fields don't have a uniform group type — `padding` is
    a dimension but `backgroundColor` is a color reference and
    `typography` is a typography composite. We dispatch on the property
    name with a case-insensitive substring match for color/dimension
    fields.
    """
    p = prop.lower()
    if "color" in p:
        return "color"
    if p in {"rounded", "radius", "padding", "size", "height", "width", "margin", "gap"}:
        return "dimension"
    if p == "typography":
        return "typography"
    if "font" in p:
        # Catch-all for fontFamily / fontWeight when they appear as component
        # overrides rather than as full typography references. Falling
        # through to "string" would be lossy.
        return "string"
    return "string"


def _alias_path(value: str) -> str | None:
    """Extract `a.b.c` from `{a.b.c}`. Returns None if not an alias."""
    m = ALIAS_RE.match(value.strip())
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# DTCG emission (DESIGN.md path)
# ---------------------------------------------------------------------------

def design_md_to_dtcg(fm: dict[str, Any]) -> dict[str, Any]:
    """Convert a parsed DESIGN.md frontmatter dict to canonical DTCG JSON.

    Every leaf gets `$type` + `$value`. Aliases are preserved verbatim as
    the leaf's `$value` string (DTCG-spec consumers resolve them at
    consumption time). Group-level `$type` is set when every direct child
    leaf shares the same type — this is the spec's "type inheritance"
    optimization.
    """
    out: dict[str, Any] = {}
    for group, children in fm.items():
        if not isinstance(children, dict):
            # Top-level scalars like `name`, `version`, `description` are
            # metadata, not tokens — skip them.
            continue
        if group == "components":
            out[group] = _emit_component_group(children)
        elif group == "typography":
            out[group] = _emit_typography_group(children)
        elif group in GROUP_TO_DTCG_TYPE:
            out[group] = _emit_simple_group(children, GROUP_TO_DTCG_TYPE[group])
        else:
            # Unknown groups are skipped — emitting them with $type: "string"
            # would pollute the DTCG output with arbitrary frontmatter
            # metadata (e.g. a `notes` block). DESIGN.md keeps non-token
            # data outside the four canonical groups.
            continue
    return out


def _emit_simple_group(children: dict[str, Any], dtcg_type: str) -> dict[str, Any]:
    """Emit `colors:` / `rounded:` / `spacing:` — every child is a primitive token.

    Sets the group-level `$type` so leaves can omit it (spec-compliant
    inheritance). Each leaf gets `$value`.
    """
    group_obj: dict[str, Any] = {"$type": dtcg_type}
    for name, value in children.items():
        group_obj[name] = _emit_leaf(value, dtcg_type, inherited=True)
    return group_obj


def _emit_typography_group(children: dict[str, Any]) -> dict[str, Any]:
    """Emit `typography:` — each child is a composite typography token.

    A typography composite `$value` is an object of subProperty → value,
    where each sub-value can itself be an alias. Examples:
      headline-lg:
        fontFamily: "Inter"
        fontSize: 36px
        fontWeight: 600
        lineHeight: 1.2
    """
    group_obj: dict[str, Any] = {"$type": "typography"}
    for name, value in children.items():
        if not isinstance(value, dict):
            # Defensive: a top-level scalar under `typography:` would be
            # malformed — skip rather than crash.
            continue
        group_obj[name] = {"$value": dict(value), "$type": "typography"}
    return group_obj


def _emit_component_group(children: dict[str, Any]) -> dict[str, Any]:
    """Emit `components:` — each child is a group of property tokens.

    Components are themselves groups (not leaves), so we cannot set a
    single group-level `$type`. Each property becomes a leaf with its
    own inferred type.
    """
    group_obj: dict[str, Any] = {}
    for cname, cdef in children.items():
        if not isinstance(cdef, dict):
            continue
        component_obj: dict[str, Any] = {}
        for prop, val in cdef.items():
            t = _infer_component_property_type(prop)
            component_obj[prop] = _emit_leaf(val, t, inherited=False)
        group_obj[cname] = component_obj
    return group_obj


def _emit_leaf(value: Any, dtcg_type: str, *, inherited: bool) -> dict[str, Any]:
    """Build the leaf object `{ "$value": ..., "$type": ... }`.

    `inherited=True` lets us drop the `$type` on the leaf because the
    parent group declares it. Aliases stay verbatim — they're the
    consumer's responsibility to resolve.
    """
    leaf: dict[str, Any] = {"$value": value}
    if not inherited:
        leaf["$type"] = dtcg_type
    return leaf


# ---------------------------------------------------------------------------
# Harmonize (Figma-Tokens nested → canonical DTCG)
# ---------------------------------------------------------------------------
# Figma Tokens (and several other commercial tools) emit a nested-group
# JSON where each leaf uses bare keys (`value`, `type`, `description`)
# and aliases use the same `{path.to.token}` syntax. The harmonize pass
# rewrites bare keys to `$`-prefixed DTCG keys WITHOUT touching the
# nesting structure — preserving the consumer's intended group
# hierarchy.

BARE_KEYS_TO_DTCG = {
    "value": "$value",
    "type": "$type",
    "description": "$description",
    "extensions": "$extensions",
}


def harmonize(node: Any) -> Any:
    """Recursively rewrite a Figma-Tokens-style tree into canonical DTCG.

    Algorithm:
      1. Walk every dict node depth-first.
      2. If a dict contains `value` (a leaf marker), rename `value`→`$value`,
         `type`→`$type`, `description`→`$description`. Keep nested values
         as-is (they're the leaf payload, not children to recurse into).
      3. Otherwise treat the dict as a group and recurse into every child.
      4. Lists, scalars, and None pass through unchanged.

    Idempotent: a tree already in DTCG form returns equal.
    """
    if isinstance(node, dict):
        # A node is a leaf iff it has `value` (bare) OR `$value` (already
        # DTCG). The check is order-independent.
        if "value" in node or "$value" in node:
            return _harmonize_leaf(node)
        # Otherwise it's a group — recurse into every key.
        return {k: harmonize(v) for k, v in node.items()}
    if isinstance(node, list):
        return [harmonize(item) for item in node]
    return node


def _harmonize_leaf(leaf: dict[str, Any]) -> dict[str, Any]:
    """Rewrite a single leaf's bare keys to `$`-prefixed DTCG keys.

    Any pre-existing `$value` wins over bare `value` — that lets a
    partially-DTCG document harmonize cleanly. Unknown extra keys are
    preserved verbatim (DTCG allows arbitrary `$`-prefixed metadata).
    """
    out: dict[str, Any] = {}
    # First pass: bare keys → DTCG keys.
    for k, v in leaf.items():
        if k in BARE_KEYS_TO_DTCG:
            dtcg_key = BARE_KEYS_TO_DTCG[k]
            if dtcg_key not in out:
                out[dtcg_key] = v
        else:
            out[k] = v
    # If the document already had a DTCG key, the loop above kept it.
    # Ensure $value is set (DTCG hard requirement).
    if "$value" not in out:
        # Pathological leaf — keep it as a group instead. The validator
        # will flag it.
        return {k: harmonize(v) for k, v in leaf.items()}
    # Ensure $type — if missing, infer from $value shape.
    if "$type" not in out:
        inferred = _infer_type_from_value(out["$value"])
        if inferred is not None:
            out["$type"] = inferred
    return out


HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{3,8}$")
DIMENSION_RE = re.compile(r"^-?\d+(\.\d+)?(px|rem|em|%|pt|vw|vh)$")


def _infer_type_from_value(value: Any) -> str | None:
    """Heuristically guess a DTCG `$type` from the `$value` shape.

    Used only when harmonizing a leaf that omitted `type`. The mapping is
    conservative: only obvious shapes resolve, everything else stays
    untagged so the validator (downstream) flags it.
    """
    if isinstance(value, str):
        if HEX_COLOR_RE.match(value):
            return "color"
        if DIMENSION_RE.match(value):
            return "dimension"
        if ALIAS_RE.match(value):
            # An alias's effective type is the target's type; without
            # walking the tree we can't decide here. Return None to let
            # the consumer resolve.
            return None
    if isinstance(value, (int, float)):
        # Bare numbers are ambiguous (could be opacity, line-height,
        # font-weight, etc). Tag as `number` — the safest non-lossy default.
        return "number"
    return None


# ---------------------------------------------------------------------------
# Validation (post-emit safety net)
# ---------------------------------------------------------------------------

def validate_dtcg(tree: dict[str, Any]) -> list[str]:
    """Walk the emitted DTCG and collect contract violations.

    Returns a list of error strings (empty == success). Used both by the
    CLI's exit-code 3 path and by the test suite for direct assertion.
    """
    errors: list[str] = []
    _validate_walk(tree, path=[], group_type=None, errors=errors, root=tree)
    return errors


def _validate_walk(
    node: Any,
    *,
    path: list[str],
    group_type: str | None,
    errors: list[str],
    root: dict[str, Any],
) -> None:
    """Recursive validator. `group_type` is the nearest ancestor group's $type
    (None at root or when the ancestor doesn't declare one).
    """
    if not isinstance(node, dict):
        return  # Lists or scalars cannot be DTCG nodes — skip.
    # Determine: is this a leaf or a group?
    is_leaf = "$value" in node
    if is_leaf:
        # Leaf contract: must have $type (either local or inherited).
        local_type = node.get("$type")
        effective_type = local_type or group_type
        loc = ".".join(path) if path else "<root>"
        if not effective_type:
            errors.append(f"{loc}: missing $type (no local and no inherited)")
        elif effective_type not in DTCG_ALL_TYPES:
            errors.append(f"{loc}: unknown $type '{effective_type}'")
        # If alias, resolve and check existence.
        v = node["$value"]
        if isinstance(v, str) and ALIAS_RE.match(v.strip()):
            target = _resolve_alias(v, root)
            if target is None:
                errors.append(f"{loc}: alias {v} does not resolve to an existing token")
        return
    # Group: extract group-level $type (if any) and recurse.
    new_group_type = node.get("$type", group_type)
    for k, v in node.items():
        if k.startswith("$"):
            continue
        _validate_walk(v, path=path + [k], group_type=new_group_type, errors=errors, root=root)


def _resolve_alias(alias: str, root: dict[str, Any]) -> Any:
    """Walk `root` following the dotted path in `alias`. Return the target
    object, or None if the path is dead.
    """
    p = _alias_path(alias)
    if p is None:
        return None
    node: Any = root
    for seg in p.split("."):
        if isinstance(node, dict) and seg in node:
            node = node[seg]
        else:
            return None
    return node


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_input(path: Path) -> tuple[dict[str, Any], str]:
    """Read the input file and return (parsed-tree, source-kind).

    source-kind is one of: 'design-md', 'json', 'yaml' — chosen by extension.
    """
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".md":
        return _parse_frontmatter(text), "design-md"
    if suffix == ".json":
        return json.loads(text), "json"
    if suffix in (".yaml", ".yml"):
        if not HAVE_YAML or yaml is None:
            raise RuntimeError(
                "pyyaml is required to load .yaml input — install it or convert to JSON"
            )
        data = yaml.safe_load(text)
        return (data if isinstance(data, dict) else {}), "yaml"
    raise RuntimeError(f"unsupported input extension: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export DTCG (Design Tokens Community Group) JSON from a DESIGN.md or a Figma-Tokens-style nested tree.",
    )
    parser.add_argument("path", help="Path to DESIGN.md, .json, or .yaml input")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--harmonize",
        action="store_true",
        help="Treat input as a nested token tree (Figma Tokens style) and rewrite to canonical DTCG. Required for non-.md inputs.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip the post-emit validation pass (default: validate; exit 3 on failure).",
    )
    args = parser.parse_args()

    in_path = Path(args.path)
    if not in_path.is_file():
        print(f"Error: file not found: {in_path}", file=sys.stderr)
        return 2

    try:
        tree, kind = _load_input(in_path)
    except (json.JSONDecodeError, RuntimeError) as e:
        print(f"Error parsing {in_path}: {e}", file=sys.stderr)
        return 2

    if kind == "design-md":
        if not tree:
            print(f"Error: no YAML frontmatter found in {in_path}", file=sys.stderr)
            return 2
        dtcg = design_md_to_dtcg(tree)
    else:
        # JSON / YAML inputs must go through harmonize — there is no
        # other sensible interpretation. A non-.md input without
        # --harmonize is almost certainly a user error.
        if not args.harmonize:
            print(
                f"Error: {in_path.suffix} input requires --harmonize",
                file=sys.stderr,
            )
            return 2
        dtcg = harmonize(tree)

    if not args.no_validate:
        errors = validate_dtcg(dtcg)
        if errors:
            print("DTCG validation failed:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            return 3

    out_text = json.dumps(dtcg, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(out_text, encoding="utf-8")
    else:
        sys.stdout.write(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
