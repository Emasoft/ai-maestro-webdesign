"""Regression guard: a bare `@name` outside a code span pages a real GitHub
account (see CLAUDE.md "GitHub writes" / ~/.claude/rules/github-mentions.md).

Fenced/inline code is NOT stripped: these skills produce ASCII diagrams
whose stated destination is a GitHub PR description, so a fenced block's
content is copied OUT of the fence into a real comment box, where a bare
handle goes live. Code spans are scanned like any other text.

Fails if any *.md under skills/, commands/, agents/ contains a bare @handle
that isn't a known-safe CSS at-rule, decorator, or other real syntax.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ("skills", "commands", "agents")

# Known-safe bare-word categories that legitimately follow "@" in prose:
# CSS at-rules, Python/JS decorators, JSON-LD/schema.org keywords, Tailwind
# breakpoint variants, PlantUML directives, shadcn registry namespaces, and
# a few package/concept names that appear without a trailing "/" in this
# repo's docs.
ALLOWLIST = {
    "media", "theme", "keyframes", "layer", "container", "apply", "supports",
    "import", "font-face", "page", "charset", "namespace", "property",
    "scope", "starting-style", "source", "reference", "utility", "variant",
    "custom-media", "custom-selector", "custom-variant", "tailwind",
    "config", "plugin",
    "staticmethod", "classmethod", "dataclass", "lru_cache", "cache",
    "patch", "fixture", "pytest", "override", "abstractmethod",
    "contextmanager", "wraps", "functools",
    "google", "fontsource", "mentions",
    "type", "context", "id", "graph",
    "md", "xs", "sm", "lg", "xl",
    "view-transition", "scroll-timeline",
    "startuml", "enduml",
    "magic-ui", "expansions", "origin",
    "brand", "themes",
    "user-slot", "owner-slot",
}

# "@" at a word boundary (not preceded by alnum/./-/_//) followed by a letter.
HANDLE_RE = re.compile(r"(?<![A-Za-z0-9._/-])@([A-Za-z][A-Za-z0-9_-]*)")


def _scan_text(text: str) -> list[tuple[int, str]]:
    """Return (lineno, token) for every bare @handle in text that isn't an
    allowlisted syntax token or a scoped-package/version-pin reference."""
    findings = []
    for lineno, line in enumerate(text.split("\n"), start=1):
        for m in HANDLE_RE.finditer(line):
            word = m.group(1)
            if line[m.end():m.end() + 1] == "/":  # scoped pkg / pin
                continue
            if word.lower() in ALLOWLIST:
                continue
            findings.append((lineno, word))
    return findings


def test_no_bare_handles_in_markdown():
    """No *.md under skills/commands/agents contains a bare @handle that
    would page a real GitHub account if pasted outside a code span."""
    findings = []
    for scan_dir in SCAN_DIRS:
        for md_path in (REPO_ROOT / scan_dir).rglob("*.md"):
            raw = md_path.read_text(encoding="utf-8")
            rel = md_path.relative_to(REPO_ROOT)
            for lineno, word in _scan_text(raw):
                findings.append(f"{rel}:{lineno}: @{word}")

    assert not findings, (
        "Bare @handle(s) found — these page real GitHub accounts. Wrap in "
        "backticks or replace with <placeholder>:\n" + "\n".join(findings)
    )


def test_scan_text_catches_positive_control():
    """_scan_text detects bare handles in both fenced and prose text (the
    positive control that proves the guard isn't just finding nothing)."""
    fixture = REPO_ROOT / "tests" / "fixtures" / "handle_guard_positive_control.md"
    findings = _scan_text(fixture.read_text(encoding="utf-8"))
    words = {word for _, word in findings}
    assert "fakeuser123" in words
    assert "another-fake-team" in words
    assert len(findings) >= 2
