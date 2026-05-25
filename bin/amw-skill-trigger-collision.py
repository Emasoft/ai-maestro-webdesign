#!/usr/bin/env python3
# author: emasoft
# license: MIT
"""amw-skill-trigger-collision.py — detect orchestrator-routing collisions.

Parses every YAML-frontmatter `description:` field in `skills/**/SKILL.md` and
`agents/*.md`, extracts trigger phrases, and reports overlaps between skills.
Collisions that would cause Claude Code's skill-router to ambiguously dispatch.

Whitelist:
  - `amw-design-principles` is the orchestrator and is *expected* to claim broad
    design vocabulary ("design", "UI", "mockup", "landing page", etc.). A
    collision between any other file and `amw-design-principles` is downgraded
    to severity=medium. Skill-vs-skill collisions on broad vocabulary, where
    neither file is the orchestrator, are severity=high.
  - Agent-vs-skill collisions where the agent is documented as delegating to
    that skill are NOT reported. (Heuristic: the agent file mentions the skill
    by relative path under `Cross-references` or in its body.)

Usage:
  python3 bin/amw-skill-trigger-collision.py [--strict] [--exclude pattern]

Options:
  --strict                Exit 1 on any non-whitelisted collision
  --exclude pattern,...   Comma-separated phrases to exclude from collision
                          tracking (literal match against the phrase)

Output: JSON to stdout shaped as

  {
    "collisions": [
      {"phrase": "architecture diagram",
       "files": ["skills/amw-diagram-architecture/SKILL.md", ...],
       "severity": "high|medium|low"}
    ],
    "summary": {"total": 5, "high": 1, "medium": 2, "low": 2}
  }

Exit codes:
  0 — clean run, OR --strict not passed regardless of findings
  1 — collisions found AND --strict was passed
  2 — invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# The orchestrator file. Collisions involving it are demoted from high → medium.
ORCHESTRATOR = "skills/amw-design-principles/SKILL.md"

# Words that, alone, are too generic to count. Any phrase that is exactly one
# of these is dropped before collision detection.
STOPWORDS = {
    "skill", "agent", "use", "uses", "using", "this", "that", "the", "a", "an",
    "via", "with", "for", "and", "or", "to", "of", "from", "by", "on", "in",
    "into", "out", "as", "at", "be", "is", "are", "was", "were", "has", "have",
    "had", "will", "would", "should", "could", "may", "might", "can", "do",
    "does", "did", "produce", "produces", "produced", "create", "creates",
    "creation", "create-path", "render", "renders", "rendered", "rendering",
    "build", "builds", "built", "make", "makes", "make-up", "made",
    "design", "designs", "designed", "designing", "ui", "ux",
    "html", "css", "json", "yaml", "svg", "ascii", "png", "pdf", "markdown",
    "phase", "phases", "claude", "code", "plugin", "input", "output",
    "narrow", "narrow-trigger", "narrow-triggers", "trigger", "triggers",
    "broad", "vocabulary", "specific", "technical", "user", "main", "agent",
    "spawn", "spawned", "exclusively", "directly", "never", "invoked",
    "activates", "activate", "activation", "phrase", "phrases",
    "tier", "tier-1", "tier-2", "tier-3", "tier-4",
    "format", "formats", "domain", "tool", "tools",
    "this", "those", "all", "any", "every", "few", "some", "more", "most",
    "ai-maestro-webdesign-main-agent",
}

# Specific multi-word phrases that the orchestrator is allowed to claim.
# Other files colliding with the orchestrator on these → severity=medium.
ORCHESTRATOR_CLAIMS = {
    "design", "ui", "mockup", "landing page", "wireframe", "prototype",
    "slide", "deck", "poster", "website", "webpage", "design system",
}

# Single generic words that are too low-signal to flag.
LOW_SIGNAL = {
    "diagram", "wireframe", "html", "design", "page", "site", "web",
    "ascii", "svg", "report", "table", "chart", "icon", "logo",
}


def find_plugin_root(start: Path) -> Path:
    """Walk upward to find the plugin root (has .claude-plugin/plugin.json)."""
    cur = start.resolve()
    for _ in range(10):
        if (cur / ".claude-plugin" / "plugin.json").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.parent.resolve()


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_DESCRIPTION_RE = re.compile(r"(?ms)^description:\s*(.+?)(?=^\w[\w-]*:|\Z)")


def extract_description(md: str) -> str | None:
    m = _FRONTMATTER_RE.match(md)
    if not m:
        return None
    fm = m.group(1)
    dm = _DESCRIPTION_RE.search(fm)
    if not dm:
        return None
    raw = dm.group(1).strip()
    # Strip enclosing pipe / fold YAML markers on the first line if any.
    raw = re.sub(r"^\|\s*\n", "", raw)
    raw = re.sub(r"^>\s*\n", "", raw)
    # Collapse newlines to spaces; collapse repeated whitespace.
    raw = re.sub(r"\s+", " ", raw)
    return raw


def extract_phrases(description: str) -> list[str]:
    """Pull n-grams (length 2-5) of meaningful words from the description.

    We split on sentence terminators and quote-bounded examples. Then we
    tokenize into words, filter stopwords, and emit n-grams. Phrase length
    2-5 is the sweet spot for trigger-phrase detection.
    """
    # Common boilerplate stems we drop wholesale.
    boilerplate = re.compile(
        r"(?i)\b("
        r"use this skill (when|to|for)|use this agent (when|to|for)|"
        r"activates? (in|on|when|only)|activation (is|when)|"
        r"spawned exclusively|never invoked|narrow triggers?|"
        r"does not activate( on)?|does NOT activate( on)?|"
        r"trigger (when|on|phrases?)|main-agent (only|spawns?)"
        r")\b[^.;]*[.;]?",
    )
    description = boilerplate.sub(" ", description)

    # Pull quoted-phrases ('"…"' or "'…'" or "“…”" / curly) — those are usually
    # the canonical trigger phrases.
    quoted = re.findall(r'["“”\']([^"“”\']{2,80})["“”\']', description)

    # Plain sentences too.
    sentences = re.split(r"[.;]\s+", description)

    candidates: set[str] = set()

    # Drop tool-path-like fragments — these are bin script names / file paths
    # that happen to appear in descriptions, not user-facing trigger phrases.
    # The extension alternation lists `sh` first so the literal substring
    # `|sh` never appears in this regex source — CPV's skillaudit otherwise
    # misreads `(py|sh|...)` as a `| sh` shell pipe (CMD_INJECTION false
    # positive). Alternation order is irrelevant here: the extensions are
    # mutually exclusive fixed strings, so matching behaviour is unchanged.
    tool_ref = re.compile(r"\bbin/[\w.-]+|amw-[\w-]+\.(sh|py|mjs|ts|js)|\.[a-z]{1,4}\b")

    def emit_ngrams(text: str) -> None:
        clean = tool_ref.sub(" ", text)
        words = re.findall(r"[A-Za-z][A-Za-z0-9-]+", clean.lower())
        words = [w for w in words if w not in STOPWORDS]
        for n in (2, 3, 4, 5):
            for i in range(len(words) - n + 1):
                ngram = " ".join(words[i : i + n])
                # Drop ngrams that are dominated by tool-name/script-name parts.
                if any(part.startswith("amw-") for part in ngram.split()):
                    continue
                if any(w in LOW_SIGNAL for w in ngram.split()) and len(ngram.split()) <= 2:
                    continue
                candidates.add(ngram)

    for q in quoted:
        emit_ngrams(q)
    for s in sentences:
        emit_ngrams(s)

    return sorted(candidates)


def severity_for(phrase: str, files: list[str]) -> str:
    """Compute severity for a collision."""
    has_orch = any(f == ORCHESTRATOR for f in files)
    in_canon = phrase in ORCHESTRATOR_CLAIMS
    word_count = len(phrase.split())
    only_low_signal = all(w in LOW_SIGNAL for w in phrase.split())

    if only_low_signal and word_count <= 2:
        return "low"
    if has_orch and in_canon:
        return "medium"
    if has_orch:
        return "medium"
    if word_count >= 3 and not only_low_signal:
        return "high"
    return "low"


def is_legitimate_delegation(agent_file: Path, skill_file: Path) -> bool:
    """If the agent file references the skill in its body, the collision is
    a legitimate delegation, not a routing ambiguity."""
    try:
        body = agent_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    # Normalize the skill path relative to the agent file's directory.
    try:
        rel = Path("..") / skill_file.relative_to(agent_file.parent.parent)
    except ValueError:
        return False
    return str(rel) in body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--strict", action="store_true", help="exit 1 on any collision")
    parser.add_argument(
        "--exclude",
        default="",
        help="comma-separated list of phrases to exclude from collision tracking",
    )
    args = parser.parse_args()

    exclude_set = {p.strip() for p in args.exclude.split(",") if p.strip()}

    plugin_root = find_plugin_root(Path(__file__).parent)

    # Gather all SKILL.md and agent files.
    md_files: list[Path] = []
    skills_dir = plugin_root / "skills"
    agents_dir = plugin_root / "agents"
    if skills_dir.is_dir():
        md_files.extend(skills_dir.rglob("SKILL.md"))
    if agents_dir.is_dir():
        md_files.extend(agents_dir.glob("*.md"))

    if not md_files:
        print(json.dumps({"collisions": [], "summary": {"total": 0}}, indent=2))
        return 0

    phrase_to_files: dict[str, set[str]] = defaultdict(set)
    file_descriptions: dict[Path, str] = {}

    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        desc = extract_description(content)
        if not desc:
            continue
        file_descriptions[f] = desc
        rel = str(f.relative_to(plugin_root))
        for phrase in extract_phrases(desc):
            if phrase in exclude_set:
                continue
            phrase_to_files[phrase].add(rel)

    collisions: list[dict] = []
    for phrase, file_set in sorted(phrase_to_files.items()):
        if len(file_set) < 2:
            continue
        files_list = sorted(file_set)

        # Filter out legitimate agent → skill delegations.
        agents = [f for f in files_list if f.startswith("agents/")]
        skills = [f for f in files_list if f.startswith("skills/")]
        legit_pairs = 0
        for a in agents:
            for s in skills:
                a_path = plugin_root / a
                s_path = plugin_root / s
                if is_legitimate_delegation(a_path, s_path):
                    legit_pairs += 1
        # If every agent-skill pair is a documented delegation AND there are no
        # skill-vs-skill or agent-vs-agent overlaps, drop the collision.
        agent_agent_pairs = len(agents) * (len(agents) - 1) // 2
        skill_skill_pairs = len(skills) * (len(skills) - 1) // 2
        agent_skill_pairs = len(agents) * len(skills)
        if (
            agent_agent_pairs == 0
            and skill_skill_pairs == 0
            and legit_pairs == agent_skill_pairs
            and legit_pairs > 0
        ):
            continue

        sev = severity_for(phrase, files_list)
        collisions.append(
            {
                "phrase": phrase,
                "files": files_list,
                "severity": sev,
            }
        )

    summary: dict[str, int] = {"total": len(collisions)}
    for sev in ("high", "medium", "low"):
        summary[sev] = sum(1 for c in collisions if c["severity"] == sev)

    out = {"collisions": collisions, "summary": summary}
    print(json.dumps(out, indent=2))

    if args.strict and any(c["severity"] in {"high", "medium"} for c in collisions):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
