---
name: amw-memory-recall
description: Recall the project's markdown memory BEFORE debugging a recurring problem, making a design/architecture decision, or acting on a repeated symptom or alert. Symptom-ranked search across the LOCAL, PROJECT, and USER note corpora via memgrep (plain-grep fallback). Use when about to repeat past work, hit a familiar-looking error, or decide something that may have been decided before — "have we hit this before?".
---

# amw-memory-recall — recall before acting

This is the webdesign plugin's RECALL half of the markdown memory system (the WRITE
half is `amw-memory-write`; the full protocol is `rules/memory-protocol.md`). It searches
the note corpus by SYMPTOM and surfaces the most relevant notes so you reuse a prior
solution instead of re-deriving (or re-breaking) it. Recall is cheap; skipping it is how
the same mistake gets made twice.

## The one law: search by the QUESTION, not the answer

A memory is found from the SYMPTOM — the user's words, the error text, the thing that went
wrong — NOT the jargon of the eventual fix. Build the recall query from what you OBSERVE
now, never from what you suspect the answer will be. (WRONG query: "keychain services".
RIGHT query: "every bash command hangs / stuck at password prompt".)

## Recall-before-acting protocol

Before debugging a recurring problem, making a design/architecture decision, or acting on a
recurring alert, RECALL first. Compose the three scope roots and search them in one call:

```bash
LOCAL_MEM="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"    # machine-private (paths, hostnames, creds hints)
PROJECT_MEM="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.claude/project/memory"  # git-tracked, in-repo, namespaced
USER_MEM="$HOME/.claude/plugins/data/ai-maestro-janitor-ai-maestro-plugins/memory"  # janitor's FIXED data dir (hard-coded, NOT ${CLAUDE_PLUGIN_DATA})
ROOTS=""; for d in "$LOCAL_MEM" "$PROJECT_MEM" "$USER_MEM"; do [ -d "$d" ] && ROOTS="$ROOTS $d"; done
SYMPTOM="the user's words / the error / the symptom"               # NOT the answer's jargon

if command -v memgrep >/dev/null 2>&1; then
  # shellcheck disable=SC2086
  memgrep recall "$SYMPTOM" $ROOTS        # symptom-ranked notes (lessons auto-appended), best first
else
  # shellcheck disable=SC2086
  grep -rliE "$SYMPTOM" $ROOTS            # fallback: recall degrades, never breaks
fi
```

Read the top 1–3 notes the recall returns — the answer is in their bodies.

## Scope precedence

A note's scope is its path: **LOCAL** (`~/.claude/projects/<slug>/memory/`) > **PROJECT**
(`<repo>/.claude/project/memory/`) > **USER** (`~/.claude/plugins/data/ai-maestro-janitor-ai-maestro-plugins/memory/`). When two scopes state conflicting
facts, the MORE SPECIFIC scope wins. If recall returns nothing, the memory does not exist
yet — solve the problem, then capture it with `amw-memory-write`.

## Read the notes whole

When a returned note carries `[^N]` references and a `## Notes and lessons learned` section,
read those lessons too — they are *why* the fact is the way it is and *what error not to
repeat*. `memgrep recall` appends each note's resolved lessons automatically (one call yields
body + every linked WHY); the grep fallback shows them inline in the file.

## When to use

- About to debug something that "feels familiar" → recall the symptom first.
- About to make a design / architecture decision → recall whether it was decided before.
- A recurring alert or error fires → recall the prior handling before re-investigating.
- NOT for a one-off fact you can read directly from the code or git history.
