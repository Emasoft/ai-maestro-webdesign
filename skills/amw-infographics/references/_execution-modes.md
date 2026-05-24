# Execution modes — A · B · C

## Table of Contents

- [A. Interactive Builder](#a-interactive-builder--preview-each-component-live)
- [B. One-Shot](#b-one-shot--generate-the-full-infographic-in-one-pass)
- [C. Guided Creative](#c-guided-creative--two-composition-options-before-building)
- [Quality gate (before delivery)](#quality-gate-before-delivery)
- [Cross-references](#cross-references)

Three modes for driving an infographic build. Pick the mode that matches the user's request style, then follow the steps below.

## A. Interactive Builder — preview each component live

Use when the user says "show me each", "piece by piece", "step by step", "let me iterate", or asks for a single component.

1. **Start preview server** (once per session):
   ```bash
   python3 ../../bin/amw-preview-server.py --file .infographic/.preview.html --port 7883 &
   ```
   Tell the user once: *"Preview running at http://localhost:7883 — it auto-refreshes on every render."*
2. **Plan components** — state the archetype, density target, and component list. Get an explicit go-ahead.
3. **Render one component at a time** to `<.infographic/.preview.html>` as a full self-contained HTML document. Ask for approval before locking it in.
4. **Approval gate** — only write approved components to the state file `{cwd}/.infographic/{project}.json`. Verbatim HTML, no re-generation.
5. **Assemble** on user command (`assemble`, `finalize`, `done`) — stitch approved components, wrap with header/footer, run Reduction Pass, export via `html-export.py`.

Full builder protocol (state file schema, approval vocabulary, assembly rules): see [TECH-interactive-builder-mode](TECH-interactive-builder-mode.md) and the `create-infographics` upstream SKILL.md.

## B. One-Shot — generate the full infographic in one pass

Use when the user provides a complete data brief or says "create an infographic about X", "generate", "build this".

1. **Design Brief (3 questions)** — brand (color/logo), platform (default portrait-medium 1080×1440), key insight. Skip any already answered.
2. **Classify + Archetype + Layout Intent** — state in one sentence: content type (playbook or generic), composition archetype (Stacked Reference default), dominant component, density target. Example: *"Token-Economics playbook, Stacked Reference, dominated by allocation pie + vesting timeline, targeting 10 content blocks on portrait-medium."*
3. **Build** — single self-contained HTML, required `<head>` includes Google Fonts + Phosphor Icons + optional Chart.js. Apply playbook colors/fonts. All CSS inline, CSS custom properties at `:root`, no lorem ipsum.
4. **Anti-Frontend Checklist + Reduction Pass** — see Quality Gate below.
5. **Export** — `python3 ../../bin/amw-html-export.py -i {file}.html -o {name} -f all --width {W} --scale 2`.

## C. Guided Creative — two composition options before building

Use when the user says "help me figure out the design", "give me options", "show me two approaches", or is uncertain about style.

1. **Design Brief** — as in Mode B.
2. **Classify + Layout Intent** — understand the content and key insight.
3. **Present two composition options** — no code yet. Each option gets a short name, its archetype (two *different* archetypes from the five), a one-sentence description, and why it fits this data.
4. **User picks a direction.**
5. **One-shot build** using the chosen archetype. Follow Mode B Steps 2–5.

## Quality gate (before delivery)

Copy this checklist and track your progress as you run both passes:

**Anti-Frontend Checklist** (must all be ✓):
- [ ] No uniform card grids — at least 3 different component types used.
- [ ] No paragraph descriptions — body text is bullet points.
- [ ] Card padding 12–16px, body font 11–13px, gap 8–12px.
- [ ] Borders visible — minimum `rgba(primary, 0.25)`.
- [ ] Arrows/connectors present if content describes a process/flow.
- [ ] At least one table if data has comparisons/specs/rates.
- [ ] Content block count meets density target.

**Reduction Pass** — remove gridlines that aren't needed for reading values, axis tick marks where direct labels exist, decorative icons, borders/glows on elements already separated by whitespace, text that repeats what the visual shows. Strictness scales to aesthetic (see style-details reduction table in Resources). Do NOT reduce information density.

**Final quality check** — no fabricated data, display font is not banned, Phosphor CDN included, canvas width matches platform, background mode matches request, footer present (unless user said no), all labels directly on charts (annotation-first), logo present (95% of real pieces), type-specific playbook applied if one fits.

## Cross-references

- [SKILL](../SKILL.md) — parent skill (amw-infographics)
- [_template-registry](_template-registry.md) — 24 templates with selection table
- [TECH-anti-frontend-checklist](TECH-anti-frontend-checklist.md) — the full anti-frontend rules
- [TECH-reduction-pass](TECH-reduction-pass.md) if present — the reduction-pass detail
