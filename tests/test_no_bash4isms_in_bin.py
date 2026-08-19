"""Guard: shipped bin/*.sh must run on the system /bin/bash 3.2 (macOS).

The hub's panel e2e (report 20260819_150341, commit 1f9dbbd here) hit two
bash-3.2 crashes: a `local -n` nameref in a server helper and our own
empty-array `"${arr[@]}"` under `set -u`. macOS ships bash 3.2.57 as
/bin/bash forever (GPLv3), and `bash script.sh` resolves to it, so every
bash-4+ construct in a shipped script is a latent runtime crash that no
zsh-based local testing ever sees. Concept borrowed from the hub's
no-bash4isms guard (ai-maestro 25a16355). No mocks: parses the real files
with the real /bin/bash.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Runtime bash-4isms that /bin/bash -n cannot catch (they parse fine and
# explode at execution). Each pattern is matched against comment-stripped
# lines so documentation ABOUT a construct never trips the guard.
BASH4ISMS = {
    r"\blocal\s+-n\b": "local -n nameref (bash 4.3+)",
    r"\bdeclare\s+-n\b": "declare -n nameref (bash 4.3+)",
    r"\breadarray\b": "readarray (bash 4+; use read -ra / while-read)",
    r"\bmapfile\b": "mapfile (bash 4+; use read -ra / while-read)",
    r"\$\{[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?,,?\}": "${var,,} lowercase expansion (bash 4+)",
    r"\$\{[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\^\^?\}": "${var^^} uppercase expansion (bash 4+)",
    # Unguarded empty-array expansion under set -u is the family that broke
    # amw-panel-preview.sh. Only flag the arrays proven conditionally empty
    # is impossible statically, so flag ANY bare "${NAME[@]}" that is not
    # already spelled with the ${NAME[@]+...} guard — bin/ policy after
    # 1f9dbbd is the guarded spelling everywhere.
    r'(?<!\+)"\$\{[A-Za-z_][A-Za-z0-9_]*\[@\]\}"': 'bare "${arr[@]}" (guard as ${arr[@]+"${arr[@]}"} for bash 3.2 set -u)',
}

SH_FILES = sorted((ROOT / "bin").glob("*.sh"))


def _strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"(^|\s)#.*$", "", line) for line in text.splitlines())


def test_bin_shell_scripts_exist() -> None:
    """Positive control: the guard actually scans a non-empty file set."""
    assert len(SH_FILES) >= 8, f"expected shipped shell scripts under bin/, found {len(SH_FILES)}"


def test_no_bash4isms_in_shipped_scripts() -> None:
    """No shipped bin/*.sh uses a construct that crashes on /bin/bash 3.2."""
    offenders: list[str] = []
    for f in SH_FILES:
        clean = _strip_comments(f.read_text(encoding="utf-8"))
        for pat, why in BASH4ISMS.items():
            for m in re.finditer(pat, clean):
                line = clean[: m.start()].count("\n") + 1
                offenders.append(f"{f.relative_to(ROOT)}:{line}: {why}")
    assert not offenders, "bash-4isms in shipped scripts:\n" + "\n".join(offenders)


def test_bin_scripts_parse_under_system_bash() -> None:
    """Every shipped bin/*.sh passes `/bin/bash -n` (the macOS 3.2 parser)."""
    for f in SH_FILES:
        proc = subprocess.run(["/bin/bash", "-n", str(f)], capture_output=True, text=True)
        assert proc.returncode == 0, f"{f.name} fails /bin/bash -n: {proc.stderr.strip()}"
