"""Regression guard: every executed sibling-script reference in bin/ resolves.

The bin/ scripts were bulk-renamed to the `amw-` prefix, but several internal
delegation paths (subprocess targets, sourced helpers, validator hooks) kept the
OLD unprefixed name and silently broke: the `.is_file()` / `[ -f ]` existence
check fails, so the delegated step is quietly skipped or errors out. Examples
found and fixed: amw-diagram-ir.py delegating to `ascii-parse.py` /
`ascii-render.py` / `parse-<fmt>-diagram.py`; amw-dom-to-ir.py to
`dev-browser-wrapper.sh` / `parse-html-diagram.py`; amw-mermaid-render.sh to
`validate-ascii.py`.

This suite scans every bin/*.py and bin/*.sh for an EXECUTED reference to a
sibling script (Python `BIN_DIR / "name"`, shell `"$SCRIPT_DIR/name"` /
`"$PLUGIN_ROOT/bin/name"`) and asserts the referenced file exists on disk. A
future rename that misses an internal ref fails here instead of shipping a
silently-dead code path. Comment / docstring mentions are intentionally NOT
scanned — only executed path constructions.

No mocks: reads the real bin/ directory and the real script sources.
"""

from __future__ import annotations

import re
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"

# Python: BIN_DIR / "name.ext"  (static path construction, always executed).
_PY_STATIC = re.compile(r'BIN_DIR\s*/\s*"([^"]+\.(?:py|sh|pl|mjs|js|ts))"')
# Python: BIN_DIR / f"prefix{...}suffix.ext"  (one placeholder; glob the rest).
_PY_FSTRING = re.compile(
    r'BIN_DIR\s*/\s*f"([a-zA-Z0-9_.-]*)\{[^}]+\}([a-zA-Z0-9_.-]*\.(?:py|sh|pl|mjs|js))"'
)
# Shell: $VAR/.../name.ext  (executed ref; generic over the holding variable
# name — $SELF_DIR, $SCRIPT_DIR, $PLUGIN_ROOT, $VENDOR_DIR, ... — so a future
# script using a new var name is still covered). Quotes optional.
_SH_REF = re.compile(
    r"\$[A-Za-z_][A-Za-z0-9_]*(?:/[A-Za-z0-9_.-]+)*?/([a-z][a-z0-9_-]*\.(?:py|sh|pl|mjs|js))"
)


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_python_static_sibling_refs_resolve() -> None:
    """Every `BIN_DIR / "name"` static ref in bin/*.py points to a real file."""
    missing: list[str] = []
    for f in sorted(BIN.glob("*.py")):
        for name in _PY_STATIC.findall(_read(f)):
            if not (BIN / name).is_file():
                missing.append(f"{f.name}: BIN_DIR / \"{name}\" -> not found")
    assert not missing, "unresolved static sibling refs:\n" + "\n".join(missing)


def test_python_fstring_sibling_refs_resolve() -> None:
    """Every `BIN_DIR / f"...{x}...ext"` ref matches at least one real file."""
    missing: list[str] = []
    for f in sorted(BIN.glob("*.py")):
        for prefix, suffix in _PY_FSTRING.findall(_read(f)):
            if not list(BIN.glob(f"{prefix}*{suffix}")):
                missing.append(f"{f.name}: {prefix}*{suffix} -> no match")
    assert not missing, "unresolved f-string sibling refs:\n" + "\n".join(missing)


def _flag_shell_ref(name: str, real: set[str]) -> str | None:
    """Return a diagnosis for a broken shell sibling ref, or None if it's fine.

    Two bug shapes (TRDD-XDFOJS0O widened the second in — a plant of a
    fully-nonexistent amw- sibling previously passed 4/4):
    - unprefixed rename residue: `name` missing but `amw-name` exists;
    - fully-missing amw sibling: an `amw-*` basename that exists under NO name.
    Vendor / external refs (e.g. $VENDOR_DIR/scripts/render.mjs) do not carry
    the amw- prefix and are deliberately ignored — that exemption is why the
    missing-check is scoped to amw-* basenames instead of every basename.
    """
    if name in real:
        return None
    if f"amw-{name}" in real:
        return f"{name} -> use amw-{name}"
    if name.startswith("amw-"):
        return f"{name} -> no such sibling in bin/"
    return None


def test_shell_sibling_refs_resolve() -> None:
    """Every executed `$VAR/.../name` sibling ref in bin/*.sh resolves.

    Generic over the holding variable name. Flags both unprefixed rename
    residue AND amw-* refs that exist under no name (see _flag_shell_ref).
    Comment lines are skipped.
    """
    real = {p.name for p in BIN.iterdir() if p.is_file()}
    missing: list[str] = []
    for f in sorted(BIN.glob("*.sh")):
        for i, line in enumerate(_read(f).splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for name in _SH_REF.findall(line):
                diag = _flag_shell_ref(name, real)
                if diag:
                    missing.append(f"{f.name}:{i}: {diag}")
    assert not missing, "broken shell sibling refs:\n" + "\n".join(missing)


def test_shell_ref_flagger_positive_controls() -> None:
    """The shell-ref flagger fires on both bug shapes and stays quiet on vendor refs."""
    real = {"amw-validate-ascii.py", "amw-mermaid-render.sh"}
    # bug shape 1: unprefixed rename residue
    assert _flag_shell_ref("validate-ascii.py", real) == (
        "validate-ascii.py -> use amw-validate-ascii.py"
    )
    # bug shape 2: fully-nonexistent amw sibling (the hole this test closes)
    assert _flag_shell_ref("amw-totally-fake-script.py", real) == (
        "amw-totally-fake-script.py -> no such sibling in bin/"
    )
    # non-bugs: existing sibling, and a vendor ref without the amw- prefix
    assert _flag_shell_ref("amw-validate-ascii.py", real) is None
    assert _flag_shell_ref("render.mjs", real) is None


def test_the_scan_actually_finds_references() -> None:
    """Sanity: the scanners match the known real delegation sites (not a no-op)."""
    py_static = sum(len(_PY_STATIC.findall(_read(f))) for f in BIN.glob("*.py"))
    py_fstring = sum(len(_PY_FSTRING.findall(_read(f))) for f in BIN.glob("*.py"))
    sh_refs = 0
    for f in BIN.glob("*.sh"):
        for line in _read(f).splitlines():
            if not line.lstrip().startswith("#"):
                sh_refs += len(_SH_REF.findall(line))
    # amw-diagram-ir.py (2 static + 1 f-string), amw-dom-to-ir.py (2 static),
    # amw-page-to-ascii-layout.py (1 static); amw-validate-diagram.sh dispatches
    # to >=5 siblings + amw-mermaid-render.sh (validate-ascii + vendor render).
    assert py_static >= 5, f"expected >=5 python static refs, found {py_static}"
    assert py_fstring >= 1, f"expected >=1 python f-string ref, found {py_fstring}"
    assert sh_refs >= 5, f"expected >=5 shell refs, found {sh_refs}"
