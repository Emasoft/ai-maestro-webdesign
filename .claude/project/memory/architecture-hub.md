---
name: architecture-hub
description: "webdesign plugin architecture overview / where is X / how is the plugin structured / orchestrator-priority + ASCII-first + dev-browser-only invariants — PROJECT-scope landing page"
ocd: 2026-06-16
lmd: 2026-06-16
metadata:
  node_type: memory
  type: project
  tier: hub
  globs: ["skills/**", "agents/**", "bin/**", "commands/**", "hooks/**"]
---

PROJECT-scope wiki-memory hub for the **ai-maestro-webdesign** plugin (git-tracked + shared). This is the landing page for contributor-facing knowledge that is NOT derivable from the code or `CLAUDE.md` — add PROJECT-scope notes here and link them from this hub.

**Authoritative architecture lives in `CLAUDE.md`** (full plugin layout, the 4-tier agent roster, the `bin/` shared-script table, build state). Do NOT duplicate it here — this scope is for *lessons and decisions* a contributor needs that the code doesn't already state.

**Load-bearing invariants** (full rationale in `CLAUDE.md` + `skills/amw-design-principles/`):

- **Orchestrator-priority** — `amw-design-principles` owns the broad design vocabulary (design / UI / landing page / mockup / wireframe / …); every other skill carries narrow technical triggers only. Never let an executor skill re-claim broad design vocabulary — it breaks routing.
- **ASCII-first plan phase** — a new webpage iterates in ASCII (`/amw-sketch`) before any HTML; the Phase A → Phase B satisfaction gate (explicit approval tokens) is a hard invariant. Do not shortcut to HTML on a new-webpage intent.
- **dev-browser is the only input-automation primitive** — live-page inspection (screenshot / DOM / interactive fill) routes through `skills/amw-dev-browser/`; output-only render backends (Playwright, cairosvg) stay inside their emitters. No new puppeteer/Chrome-DevTools/Playwright MCP wrapper.
- **Three hard rules** — (1) gather context before designing (fallback: `amw-ui-ux-reasoning`, never "guess"); (2) always produce ≥3 variants; (3) reject AI-slop per `skills/amw-design-principles/ai-slop-avoid.md`.
- **Validation gates** — every ASCII emitter must pass `bin/amw-validate-ascii.py`; every HTML output is graded against `ai-slop-avoid.md` before delivery; diagrams pass `bin/amw-validate-diagram.sh`.
- **Memory system** — webdesign uses the ai-maestro 3-scope wiki memory (LOCAL / PROJECT / USER). PROJECT scope = THIS dir. See `rules/memory-protocol.md` + the global `~/.claude/rules/markdown-memory-recall.md`; recall via `amw-memory-recall` (or the janitor's `janitor-memory-recall`).

## Notes and lessons learned
