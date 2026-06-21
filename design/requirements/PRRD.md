---
prrd-version: 1.7
updated: "2026-06-14T01:03:32+0200"
project: ai-maestro-webdesign
project-id: autonomous
canonical-source: design/requirements/PRRD.md
mirrors: []
---

# Project Requirements & Rules

ai-maestro-webdesign is a Claude Code plugin — an ASCII-first webpage / design-system
authoring system plus a cross-format diagram toolchain (one primary orchestrator agent,
19 specialized sub-agents, ~46 skills). These rules govern THIS project and override
general conventions where they conflict. Governance profile: solo / ungoverned (USER is
effectively MANAGER) — silver rules are edited with `prrd-edit.py --user`.

## §I. How to read this document

Rule citation form: `PRRD G<n>.<v>` or `PRRD S<n>.<v>`. See
`~/.claude/rules/prrd-design-rules.md` for the full spec.

## 🥇 GOLDEN — set by the USER (immutable to MANAGER)

- **G1.1** — Every agent that writes to GitHub (issue, PR, comment, review, discussion, release note) MUST begin the body with a one-line self-identification of which agent/role/plugin authored it, because all AI Maestro agents share the single human-owner GitHub identity (the owner gh CLI auth). Recommended leading line: I'm the Claude responsible for the ai-maestro-webdesign project. Commit messages SHOULD carry an 'Agent: ai-maestro-webdesign' trailer.

## 🥈 SILVER — MANAGER-mutable (agents propose via COS)

- **S2.1** — amw-design-principles owns the broad design vocabulary and MUST be the first skill activated on generic design intent; every other skill keeps its description narrowed to specific technical triggers so the orchestrator routes correctly. A description that re-claims general design vocabulary breaks orchestration.
- **S3.1** — The plan phase of every new-webpage design runs in ASCII via amw-ascii-sketch (about 1 percent of HTML-iteration token cost), not HTML. Iterate in ASCII until the user gives a canonical satisfaction token (yes / ship it / convert it / that is the one / perfect / done); then convert once via amw-ascii-to-html. Ambiguous acknowledgement is not approval.
- **S4.1** — Always produce at least three design variants (baseline, advanced, experimental). Single-answer output is a failure mode.
- **S5.1** — Reject AI-slop patterns: every HTML output runs a final check against amw-design-principles/ai-slop-avoid.md before delivery.
- **S6.1** — amw-dev-browser is the ONLY input-automation primitive for reading live-page state. Do not add Chrome DevTools MCP, Playwright MCP, or a new puppeteer wrapper; output-only render backends (export/preview) may keep their own engines.
- **S7.1** — Every ASCII artifact MUST pass bin/amw-validate-ascii.py (alignment, width, wide-char, forbidden-char gate) before delivery.
- **S8.1** — Gather design context (design system, brand tokens, or reference examples) before designing; the last-resort fallback is amw-ui-ux-reasoning, never guessing.
