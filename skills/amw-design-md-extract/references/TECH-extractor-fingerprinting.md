<!--
Clean-room — algorithm derived from standard practice (deterministic JSON
canonicalization + SHA-256 over sorted token block). Cross-references MIT-licensed
DESIGN.md token schema from this repo. 2026-05-27.
-->

# TECH — Extractor Design-System Fingerprinting (T-096)

## Table of Contents

- [Goal](#goal)
- [Algorithm](#algorithm)
- [Concrete recipe (pure-Python, no extra deps)](#concrete-recipe-pure-python-no-extra-deps)
- [Interpretation guide](#interpretation-guide)
- [Non-goals (what fingerprinting is NOT)](#non-goals-what-fingerprinting-is-not)
- [Versioning the algorithm](#versioning-the-algorithm)
- [Validation gate](#validation-gate)
- [Cross-references](#cross-references)

How the extractors compute a **deterministic content hash** of a DESIGN.md's
canonical token set so that two pages, two codebases, or two captures of the
same page over time can be flagged as "same design system, different content"
(or "same design system, drifted token" when the hash changes only because
of a token value tweak). Activated by `--fingerprint`; the value is also
written to `DESIGN.assets.json#fingerprint_hash` when asset export is
running in the same pass.

## Goal

Two artifacts SHOULD have the same fingerprint when:

- A user extracts DESIGN.md from `https://example.com/page-a.html` and
  `https://example.com/page-b.html` and both pages share the same brand
  CSS variables — the fingerprints should match. The pages have different
  copy but the design system is shared.
- A user extracts DESIGN.md from the same URL twice within a release
  window — the fingerprints should match unless the design system shipped
  a change between runs.

Two artifacts MUST have DIFFERENT fingerprints when ANY of the canonical
tokens differ — color hex, font family, spacing value, rounded value, or
component variant list.

The fingerprint is **content-defined**, not byte-defined: comments,
ordering, whitespace, key casing, and prose section content do NOT affect
it.

## Algorithm

### Step 1 — Extract the canonical token block

From the produced DESIGN.md, the fingerprinter reads ONLY these YAML frontmatter
keys (everything else, including all 8 prose sections, is ignored):

| Key | Subkeys included |
|---|---|
| `colors` | all keys, all values |
| `typography` | family, size, weight, lineHeight, letterSpacing per role |
| `spacing` | the full scale (xs..3xl or numeric step list) |
| `rounded` | none, sm, md, lg, xl, full (or whatever scale was emitted) |
| `borders` | width values, color references |
| `shadows` | named elevation entries — full box-shadow strings |
| `breakpoints` | sm, md, lg, xl, 2xl numeric values |
| `components` | for each component: base token references, variants list, states list — NOT the prose description |
| `iconSystem` | family name + size scale (e.g. `lucide`, `16,20,24`) when present |

Excluded: `frameworks`, the `## Overview` paragraph, `## Voice & Tone`,
`## Do's and Don'ts`, every `# TODO:` comment, the `extraction-notes`
sidecar, the `warnings` list, the `_meta` block (which itself contains
the fingerprint, so it would be circular).

### Step 2 — Canonicalize

The block is transformed into a deterministic JSON form by:

1. **Resolve token references.** Every `{colors.primary}` reference is
   replaced by its resolved value (e.g. `#7c3aed`). Unresolved references
   become the string `"<UNRESOLVED:colors.primary>"` so a missing token
   contributes deterministically rather than being ignored.
2. **Lowercase all hex color values.** `#7C3AED` and `#7c3aed` hash
   identically.
3. **Normalize numeric units.** `16px` and `16` (in a numeric context like
   spacing scale) become `16`. Percent values stay as `<n>%`. `rem` values
   stay as `<n>rem` (rem is not equivalent to px without a known base).
4. **Sort all object keys recursively, ASCII-order.** Python's
   `json.dumps(..., sort_keys=True)` is the canonical encoder.
5. **Sort all list values where order is not semantic.** Variant lists,
   state lists, spacing scales, and breakpoint scales are sorted ASCII
   order. The original (potentially semantic) order is preserved separately
   in DESIGN.md; the hash uses the sorted form.
6. **Drop empty subkeys.** A `components.button.states: []` empty list is
   dropped before hashing. Two DESIGN.mds that differ only in whether they
   list an empty `states` field hash identically.
7. **Encode as UTF-8 JSON with no spaces.** `json.dumps(canonical, sort_keys=True, separators=(",", ":"))`.

### Step 3 — Hash

```
fingerprint = sha256(canonical_json_utf8_bytes).hexdigest()
```

The output is written as `sha256:<64-char-hex>` (the `sha256:` prefix is
mandatory — it allows future algorithm migration without ambiguity).

### Step 4 — Persist

The fingerprint is written to THREE places in priority order:

1. **DESIGN.md frontmatter `_meta.fingerprint`** — primary location. Auditor
   reads this to detect drift.
2. **`<output>.extraction-notes.md`** — for audit trail (canonicalized JSON
   bytes recorded under `## Canonical token block` so a human can re-compute
   if the hash is disputed).
3. **`DESIGN.assets.json#fingerprint_hash`** — convenience for asset-pipeline
   consumers (see [TECH-extractor-icon-asset-export](TECH-extractor-icon-asset-export.md)).

## Concrete recipe (pure-Python, no extra deps)

```python
import hashlib
import json
from typing import Any

FINGERPRINT_KEYS = (
    "colors",
    "typography",
    "spacing",
    "rounded",
    "borders",
    "shadows",
    "breakpoints",
    "components",
    "iconSystem",
)

UNORDERED_LIST_PATHS = frozenset({
    # path-tuples whose list values are sorted before hashing
    ("spacing",),
    ("breakpoints",),
})


def canonicalize(node: Any, path: tuple[str, ...] = ()) -> Any:
    """Recursively canonicalize a token-block value.

    - dict keys are sorted ASCII order
    - hex color strings are lowercased
    - empty subkeys are dropped
    - list values at known unordered paths are sorted
    """
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key in sorted(node.keys()):
            child = canonicalize(node[key], path + (key,))
            if child in (None, [], {}, ""):
                # Drop empty subkeys so absence and empty-presence hash the same.
                continue
            out[key] = child
        return out
    if isinstance(node, list):
        items = [canonicalize(item, path) for item in node]
        if path in UNORDERED_LIST_PATHS or _looks_like_variant_or_state(path):
            items = sorted(items, key=_stable_repr)
        return items
    if isinstance(node, str):
        # Lowercase hex colors. Token references are resolved upstream;
        # if we still see {x.y} here it stays verbatim (intentional).
        if _looks_like_hex(node):
            return node.lower()
        return node
    return node


def _looks_like_hex(s: str) -> bool:
    return (
        len(s) in (4, 7, 9)
        and s.startswith("#")
        and all(c in "0123456789abcdefABCDEF" for c in s[1:])
    )


def _looks_like_variant_or_state(path: tuple[str, ...]) -> bool:
    # components.<name>.variants.<axis> and components.<name>.states.* leaf-lists
    if len(path) < 2:
        return False
    return (
        path[0] == "components"
        and len(path) >= 3
        and path[2] in ("variants", "states", "sizes")
    )


def _stable_repr(item: Any) -> str:
    return json.dumps(item, sort_keys=True, separators=(",", ":"))


def fingerprint_design_md(parsed_frontmatter: dict) -> str:
    """Compute sha256 fingerprint of a parsed DESIGN.md frontmatter."""
    block = {k: parsed_frontmatter[k] for k in FINGERPRINT_KEYS if k in parsed_frontmatter}
    canonical = canonicalize(block)
    encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    return f"sha256:{digest}"
```

## Interpretation guide

| Comparison | Interpretation |
|---|---|
| Two DESIGN.mds, identical fingerprint | Same design system. Pages may differ only in copy / structure / prose. |
| Two DESIGN.mds, different fingerprint, same hosts / brand | Design system drifted. Run `bin/amw-design-md-diff.sh` to see which tokens changed. |
| Two DESIGN.mds, different fingerprint, different brands | Different design systems. No further inference. |
| Same URL extracted twice, different fingerprint | Source changed between runs OR extractor non-determinism. Inspect extraction-notes sidecars to see which tokens differ. |
| Fingerprint matches an entry in `~/.config/ai-maestro/design-library/` (cross-project DESIGN.md library, see [TECH-20-design-library](../../amw-design-md-convert/references/TECH-20-design-library.md)) | This is a known design system. The library entry's prose / brand-archetype labels can be reused. |

## Non-goals (what fingerprinting is NOT)

- **Not a similarity score.** A 1-character change in a hex color flips the
  hash. Use `bin/amw-design-md-diff.sh` for human-readable diffs and the
  upcoming structural-similarity score (proposed TRDD, out of scope here).
- **Not a brand identifier.** Two unrelated brands could in principle
  produce the same hash if their tokens are identical (e.g. two pages that
  both ship plain Tailwind defaults). The hash answers "are the tokens the
  same?" — not "are the brands the same?".
- **Not collision-resistant against adversaries.** SHA-256 is
  cryptographically secure, but an attacker could craft a DESIGN.md with
  arbitrary prose around an identical canonical token block to game the
  fingerprint. The fingerprint is a *content identity* signal, not a
  *trust* signal.
- **Not a substitute for the lint gate.** A DESIGN.md that fails P0 lint
  may still produce a stable fingerprint. Lint MUST pass before the
  fingerprint is recorded as canonical.

## Versioning the algorithm

The `sha256:` prefix exists exactly so a future version can introduce
`sha256-v2:`, `blake3:`, or `sha512:` without ambiguity. When the algorithm
changes, the extractor:

1. Computes the new-algorithm fingerprint as the canonical value.
2. Computes the previous-algorithm fingerprint as `_meta.fingerprint_legacy`
   for one release cycle so existing libraries can still cross-reference.

The current canonical algorithm is `sha256`. No legacy fingerprint is
shipped today because this is the first version.

## Validation gate

After the fingerprint is computed:

1. The extractor re-parses the produced DESIGN.md (round-trip) and
   re-computes the fingerprint from the re-parsed frontmatter. The two
   values MUST match. Mismatch indicates a bug in the writer (e.g. a key
   that wrote in non-canonical case) and the extractor fails fast with
   `status=failed`, `blocking_issues=["fingerprint round-trip mismatch — writer bug"]`.
2. If the fingerprint matches an entry in the cross-project design
   library (when present), the match is logged in `recommendations[]`:
   `"Fingerprint matches DESIGN.md previously extracted from
   '<library-entry-name>'. The extracted file may not need to be a
   separate library entry; consider an alias."`.

## Cross-references

- [TECH-extractor-component-detection](TECH-extractor-component-detection.md) —
  produces the `components` block that participates in the hash
- [TECH-extractor-icon-asset-export](TECH-extractor-icon-asset-export.md) —
  the asset manifest also receives the fingerprint for cross-pipeline
  reference
- [TECH-11-validation-and-lint](../../amw-design-md/references/TECH-11-validation-and-lint.md) — lint
  must PASS before the fingerprint is treated as canonical
- [TECH-20-design-library](../../amw-design-md-convert/references/TECH-20-design-library.md) — proposed
  cross-project library uses the fingerprint as a primary key
- [SKILL](../../amw-design-extract/SKILL.md) — sibling URL-extraction skill
  whose loose-format output can also be fingerprinted via this same
  algorithm if its tokens are first normalized into Variant 1 shape
